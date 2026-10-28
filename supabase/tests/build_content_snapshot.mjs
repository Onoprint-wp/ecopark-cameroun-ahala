// ============================================================================
// Génère la copie de secours du contenu public intégrée au HTML
// (etape0-site-live/content-snapshot.json), lue au premier affichage.
//
//   node supabase/tests/build_content_snapshot.mjs                  -> depuis les migrations (PGlite)
//   node supabase/tests/build_content_snapshot.mjs --from-supabase  -> depuis un projet Supabase
//        (variables SUPABASE_URL et SUPABASE_ANON_KEY ; seul le contenu PUBLIÉ est lisible)
// ============================================================================
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const OUT = resolve(here, '..', '..', 'etape0-site-live', 'content-snapshot.json');
const TABLES = ['catalog_activities', 'sales_bundles', 'lodge_cities', 'agenda_events', 'menu_items', 'site_settings'];
const ORDER = { site_settings: 'key' };

// Champs internes inutiles côté visiteur (et à ne pas exposer dans le HTML)
const STRIP = ['updated_by', 'duplicated_from'];
const clean = (row) => {
  const out = {};
  for (const [k, v] of Object.entries(row)) if (!STRIP.includes(k)) out[k] = v instanceof Date ? v.toISOString() : v;
  return out;
};

async function fromMigrations() {
  const { PGlite } = await import('@electric-sql/pglite');
  const { pgcrypto } = await import('@electric-sql/pglite/contrib/pgcrypto');
  const db = await PGlite.create({ extensions: { pgcrypto } });
  const sql = (p) => readFileSync(join(here, p), 'utf8');
  await db.exec(sql('_supabase_stub.sql'));
  await db.exec(sql('../migrations/20261026000001_ecopark_schema_rls.sql'));
  await db.exec(sql('../migrations/20261028000001_admin_crud_governance.sql'));
  await db.exec(sql('../migrations/20261028000002_realtime_publication.sql'));
  await db.exec(sql('../migrations/20261028000003_publication_images.sql'));
  const content = {};
  for (const t of TABLES) {
    const where = t === 'site_settings' ? 'WHERE is_public' : `WHERE status = 'PUBLISHED'`;
    const rows = (await db.query(`SELECT * FROM public.${t} ${where} ORDER BY ${ORDER[t] || 'sort_order'}`)).rows.map(clean);
    content[t] = t === 'site_settings' ? Object.fromEntries(rows.map((r) => [r.key, r.value])) : rows;
  }
  return { source: 'migrations', content };
}

async function fromSupabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_ANON_KEY;
  if (!url || !key) throw new Error('SUPABASE_URL et SUPABASE_ANON_KEY sont requis avec --from-supabase');
  const payload = JSON.parse(Buffer.from(key.split('.')[1] || '', 'base64').toString('utf8') || '{}');
  if (payload.role === 'service_role') throw new Error('Refus : clé service_role détectée. Utilisez la clé anon publique.');
  const content = {};
  for (const t of TABLES) {
    const res = await fetch(`${url}/rest/v1/${t}?select=*&order=${ORDER[t] || 'sort_order'}`, {
      headers: { apikey: key, Authorization: `Bearer ${key}` }
    });
    if (!res.ok) throw new Error(`${t} : HTTP ${res.status} ${await res.text()}`);
    const rows = (await res.json()).map(clean);
    content[t] = t === 'site_settings' ? Object.fromEntries(rows.map((r) => [r.key, r.value])) : rows;
  }
  return { source: url, content };
}

const snap = process.argv.includes('--from-supabase') ? await fromSupabase() : await fromMigrations();
snap.generatedAt = new Date().toISOString();
writeFileSync(OUT, JSON.stringify(snap, null, 2) + '\n', 'utf8');
const n = Object.entries(snap.content).map(([k, v]) => `${k}=${Array.isArray(v) ? v.length : Object.keys(v).length}`).join(' ');
console.log(`[OK] Copie de secours écrite : ${OUT}\n     Source : ${snap.source} | ${n}`);
