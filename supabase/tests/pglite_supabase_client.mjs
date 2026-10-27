// ============================================================================
// Client compatible supabase-js (sous-ensemble) exécuté sur PGlite.
// Permet de tester SupabaseDriver contre le VRAI SQL (RLS, triggers, RPC) sans
// Docker ni projet cloud. Ce n'est pas PostgREST : pas de HTTP, pas de temps réel.
// ============================================================================

export function createPgliteSupabaseClient(db) {
  let session = { anon: true, aal: 'aal1' };

  async function run(fn) {
    try {
      const data = await db.transaction(async (tx) => {
        const claims = session.anon ? { role: 'anon' } : { role: 'authenticated', sub: session.id, aal: session.aal };
        await tx.query(`SELECT set_config('request.jwt.claims', $1, true)`, [JSON.stringify(claims)]);
        await tx.exec(`SET LOCAL ROLE ${session.anon ? 'anon' : 'authenticated'}`);
        return fn(tx);
      });
      return { data: data.data, count: data.count ?? null, error: null };
    } catch (e) {
      return { data: null, count: null, error: { code: e.code, message: e.message, hint: e.hint, details: e.detail } };
    }
  }

  const ident = (s) => '"' + String(s).replace(/"/g, '""') + '"';
  const param = (v) => (v !== null && typeof v === 'object' && !Array.isArray(v) ? JSON.stringify(v) : v);

  class Builder {
    constructor(table) {
      this.table = table; this.op = 'select'; this.filters = []; this.orders = [];
      this.rangeV = null; this.singleMode = null; this.returning = false; this.countMode = null;
    }
    select(_cols, opts) {
      if (this.op === 'select') { this.countMode = opts && opts.count; } else { this.returning = true; }
      return this;
    }
    insert(row) { this.op = 'insert'; this.payload = row; return this; }
    update(patch) { this.op = 'update'; this.payload = patch; return this; }
    delete() { this.op = 'delete'; return this; }
    eq(col, val) { this.filters.push([col, val]); return this; }
    order(col, opts) { this.orders.push([col, !opts || opts.ascending !== false]); return this; }
    range(a, b) { this.rangeV = [a, b]; return this; }
    maybeSingle() { this.singleMode = 'maybe'; return this; }
    single() { this.singleMode = 'one'; return this; }

    _where(params) {
      if (!this.filters.length) return '';
      return ' WHERE ' + this.filters.map(([c, v]) => { params.push(param(v)); return `${ident(c)} = $${params.length}`; }).join(' AND ');
    }
    async _exec(tx) {
      const t = `public.${ident(this.table)}`;
      const params = [];
      let sqlText;
      if (this.op === 'select') {
        sqlText = `SELECT * FROM ${t}${this._where(params)}`;
        if (this.orders.length) sqlText += ' ORDER BY ' + this.orders.map(([c, asc]) => `${ident(c)} ${asc ? 'ASC' : 'DESC'}`).join(', ');
        if (this.rangeV) sqlText += ` LIMIT ${this.rangeV[1] - this.rangeV[0] + 1} OFFSET ${this.rangeV[0]}`;
      } else if (this.op === 'insert') {
        const rows = Array.isArray(this.payload) ? this.payload : [this.payload];
        const cols = Object.keys(rows[0]);
        const values = rows.map((r) => '(' + cols.map((c) => { params.push(param(r[c])); return `$${params.length}`; }).join(', ') + ')');
        sqlText = `INSERT INTO ${t} (${cols.map(ident).join(', ')}) VALUES ${values.join(', ')}${this.returning ? ' RETURNING *' : ''}`;
      } else if (this.op === 'delete') {
        sqlText = `DELETE FROM ${t}${this._where(params)}${this.returning ? ' RETURNING *' : ''}`;
      } else {
        const sets = Object.keys(this.payload).map((c) => { params.push(param(this.payload[c])); return `${ident(c)} = $${params.length}`; });
        sqlText = `UPDATE ${t} SET ${sets.join(', ')}${this._where(params)}${this.returning ? ' RETURNING *' : ''}`;
      }
      const res = await tx.query(sqlText, params);
      let count = null;
      if (this.countMode === 'exact') {
        const p2 = [];
        count = (await tx.query(`SELECT count(*)::int AS n FROM ${t}${this._where(p2)}`, p2)).rows[0].n;
      }
      let data = this.op !== 'select' && !this.returning ? null : res.rows;
      if (this.singleMode && data) {
        if (this.singleMode === 'one' && data.length !== 1) {
          throw Object.assign(new Error('JSON object requested, multiple (or no) rows returned'), { code: 'PGRST116' });
        }
        data = data[0] || null;
      }
      return { data, count };
    }
    then(resolve, reject) { return run((tx) => this._exec(tx)).then(resolve, reject); }
  }

  return {
    /** Simule une connexion : { id, aal } ou null pour un visiteur anonyme */
    setUser(user, aal = 'aal1') { session = user ? { anon: false, id: user.id, aal } : { anon: true, aal: 'aal1' }; },
    from(table) { return new Builder(table); },
    rpc(name, args = {}) {
      return {
        then(resolve, reject) {
          return run(async (tx) => {
            const meta = (await tx.query(
              `SELECT p.proretset, t.typtype FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
               JOIN pg_type t ON t.oid = p.prorettype WHERE n.nspname = 'public' AND p.proname = $1 LIMIT 1`, [name])).rows[0];
            const keys = Object.keys(args);
            const params = keys.map((k) => param(args[k]));
            const call = `public.${ident(name)}(${keys.map((k, i) => `${ident(k)} => $${i + 1}`).join(', ')})`;
            if (meta && (meta.proretset || meta.typtype === 'c')) {
              return { data: (await tx.query(`SELECT * FROM ${call}`, params)).rows };
            }
            const r = await tx.query(`SELECT ${call} AS result`, params);
            return { data: r.rows[0] ? r.rows[0].result : null };
          }).then(resolve, reject);
        }
      };
    }
  };
}
