// ============================================================================
// ECOPARK — Simulations métier sur la base (scénarios réalistes de bout en bout)
// Exécution : cd supabase/tests && node simulation_scenarios.mjs
// Chaque scénario rejoue une situation d'exploitation réelle à Ahala et vérifie
// le comportement de la migration « Gouvernance CRUD ».
// ============================================================================
import { PGlite } from '@electric-sql/pglite';
import { pgcrypto } from '@electric-sql/pglite/contrib/pgcrypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const sql = (p) => readFileSync(join(here, p), 'utf8');

const U = {
  dir: { id: '00000000-0000-0000-0000-0000000000d1', name: 'Dr Christophe FOE NDI', role: 'direction' },
  adm: { id: '00000000-0000-0000-0000-0000000000a1', name: 'Admin Plateforme ONOGRAPH', role: 'administrateur_plateforme' },
  exp: { id: '00000000-0000-0000-0000-0000000000e1', name: "Chef d'Exploitation Ahala", role: 'responsable_exploitation' },
  exp2: { id: '00000000-0000-0000-0000-0000000000e2', name: 'Adjointe Exploitation', role: 'responsable_exploitation' },
  gui: { id: '00000000-0000-0000-0000-0000000000b1', name: 'Mme Clarisse ATANGANA', role: 'agent_guichet' },
};
const ANON = { anon: true };

let passed = 0;
let failed = 0;
const fails = [];
const ok = (c, label, detail = '') => {
  if (c) { passed++; console.log(`    [OK]   ${label}${detail ? ' — ' + detail : ''}`); }
  else { failed++; fails.push(label); console.log(`    [FAIL] ${label}${detail ? ' — ' + detail : ''}`); }
};
const step = (t) => console.log(`  > ${t}`);

async function as(db, who, fn, aal = 'aal1') {
  return db.transaction(async (tx) => {
    const claims = who.anon ? { role: 'anon' } : { role: 'authenticated', sub: who.id, aal };
    await tx.query(`SELECT set_config('request.jwt.claims', $1, true)`, [JSON.stringify(claims)]);
    await tx.exec(`SET LOCAL ROLE ${who.anon ? 'anon' : 'authenticated'}`);
    return fn(tx);
  });
}
const mfa = (db, who, fn) => as(db, who, fn, 'aal2');
async function refused(promise) {
  try { await promise; return null; } catch (e) { return e.message; }
}

async function setup() {
  const db = await PGlite.create({ extensions: { pgcrypto } });
  await db.exec(sql('_supabase_stub.sql'));
  await db.exec(sql('../migrations/20261026000001_ecopark_schema_rls.sql'));
  await db.exec(sql('../migrations/20261028000001_admin_crud_governance.sql'));
  await db.exec(sql('../migrations/20261028000002_realtime_publication.sql'));
  await db.exec(sql('../migrations/20261028000003_publication_images.sql'));
  for (const u of Object.values(U)) {
    await db.query('INSERT INTO auth.users (id, email) VALUES ($1, $2)', [u.id, `${u.id}@ecopark.test`]);
    await db.query('INSERT INTO public.staff_profiles (user_id, full_name, role) VALUES ($1, $2, $3)', [u.id, u.name, u.role]);
  }
  return db;
}

const idOf = async (db, table, col, val) => (await db.query(`SELECT id FROM public.${table} WHERE ${col} = $1`, [val])).rows[0].id;

async function main() {
  const db = await setup();
  const t0 = Date.now();

  // --------------------------------------------------------------------------
  console.log('\nSCÉNARIO 1 — Préparer et publier les tarifs des vacances de Pâques');
  const royaleId = await idOf(db, 'sales_bundles', 'bundle_code', 'PASS_ROYALE');
  let draft;
  step("L'Exploitation duplique le « Pass Journée Royale » et y saisit le tarif de Pâques (9 000 / 5 000 FCFA)");
  await as(db, U.exp, async (tx) => {
    draft = (await tx.query(`SELECT public.admin_duplicate('sales_bundles', $1) AS id`, [royaleId])).rows[0].id;
    await tx.query(`UPDATE public.sales_bundles SET adult_bundle_price_fcfa = 9000, child_bundle_price_fcfa = 5000,
                    savings_label = 'Spécial Pâques • Repas & Coupe-File inclus' WHERE id = $1`, [draft]);
  });
  step('Le site public pendant la préparation');
  await as(db, ANON, async (tx) => {
    const r = (await tx.query(`SELECT title, adult_bundle_price_fcfa AS adulte FROM public.sales_bundles WHERE bundle_code LIKE 'PASS_ROYALE%'`)).rows;
    ok(r.length === 1 && r[0].adulte === 8500, 'Les visiteurs voient toujours 8 500 FCFA (le brouillon reste invisible)');
  });
  step("L'Exploitation tente de publier elle-même");
  const e1 = await refused(as(db, U.exp, (tx) => tx.query(`SELECT public.admin_set_status('sales_bundles', $1, 'PUBLISHED', TRUE)`, [draft])));
  ok(e1?.includes('ECOPARK_PUBLISH_REQUIRES_DIRECTION'), 'Refusé : seule la Direction publie un tarif');
  step('Dr Foé Ndi (connecté avec double authentification) valide et publie');
  await mfa(db, U.dir, (tx) => tx.query(`SELECT public.admin_set_status('sales_bundles', $1, 'PUBLISHED', TRUE)`, [draft]));
  await as(db, ANON, async (tx) => {
    const r = (await tx.query(`SELECT bundle_code, adult_bundle_price_fcfa AS adulte, child_bundle_price_fcfa AS enfant
                               FROM public.sales_bundles WHERE bundle_code LIKE 'PASS_ROYALE%'`)).rows;
    ok(r.length === 1 && r[0].bundle_code === 'PASS_ROYALE' && r[0].adulte === 9000 && r[0].enfant === 5000,
       'Le site affiche 9 000 / 5 000 FCFA sous le même code PASS_ROYALE (réservations existantes intactes)');
  });
  step('Fin des vacances : la Direction remet le tarif normal en dupliquant à nouveau');
  await as(db, U.exp, async (tx) => {
    draft = (await tx.query(`SELECT public.admin_duplicate('sales_bundles', $1) AS id`, [royaleId])).rows[0].id;
    await tx.query(`UPDATE public.sales_bundles SET adult_bundle_price_fcfa = 8500, child_bundle_price_fcfa = 4500 WHERE id = $1`, [draft]);
  });
  await mfa(db, U.dir, (tx) => tx.query(`SELECT public.admin_set_status('sales_bundles', $1, 'PUBLISHED', TRUE)`, [draft]));
  const hist = (await db.query(`SELECT operation, actor_name, after_data->>'adult_bundle_price_fcfa' AS prix
                                FROM public.audit_logs WHERE entity_table = 'sales_bundles' ORDER BY seq`)).rows;
  const pubs = hist.filter((h) => h.operation === 'PUBLISH');
  ok(pubs.length === 2 && pubs.every((h) => h.actor_name === U.dir.name),
     'Historique : 2 publications, toutes signées par la Direction', pubs.map((h) => `${h.prix} FCFA`).join(' puis '));

  // --------------------------------------------------------------------------
  console.log('\nSCÉNARIO 2 — Lundi de Pâques férié : ouvrir un « Grand Dimanche Royal » le lundi');
  const dimId = await idOf(db, 'agenda_events', 'code', 'EVT_DIMANCHE_ROYAL');
  await as(db, U.exp, async (tx) => {
    const copy = (await tx.query(`SELECT public.admin_duplicate('agenda_events', $1) AS id`, [dimId])).rows[0].id;
    await tx.query(`UPDATE public.agenda_events SET target_weekday = 1, day_filter = 'LUNDI_FERIE',
                    badge = 'Lundi de Pâques • 12h00 – 17h30', title = 'Lundi de Pâques Royal : Buffet Camerounais & Live',
                    short_label = 'Lundi de Pâques Royal' WHERE id = $1`, [copy]);
    await tx.query(`SELECT public.admin_set_status('agenda_events', $1, 'PUBLISHED')`, [copy]);
  });
  await as(db, ANON, async (tx) => {
    const r = (await tx.query(`SELECT short_label, target_weekday FROM public.agenda_events ORDER BY target_weekday, sort_order`)).rows;
    ok(r.length === 5 && r.some((e) => e.target_weekday === 1 && e.short_label === 'Lundi de Pâques Royal'),
       "L'agenda public affiche 5 temps forts, dont le lundi férié", r.map((e) => e.short_label).join(' | '));
    ok(r.some((e) => e.short_label === 'Grand Dimanche Royal • Buffet & Live'), "L'événement du dimanche d'origine est intact");
  });

  // --------------------------------------------------------------------------
  console.log("\nSCÉNARIO 3 — Samedi de forte affluence : jauge piscine réduite et anti-surbooking");
  const piscineId = await idOf(db, 'catalog_activities', 'slug', 'piscine');
  const samedi = (await db.query(`SELECT (CURRENT_DATE + ((6 - EXTRACT(DOW FROM CURRENT_DATE)::int + 7) % 7 + 7))::date AS d`)).rows[0].d;
  step(`Maintenance d'un bassin : l'Exploitation ramène la jauge piscine de 300 à 60 places le ${samedi.toISOString().slice(0, 10)}`);
  await as(db, U.exp, (tx) => tx.query(
    `INSERT INTO public.daily_quotas (activity_id, quota_date, capacity, reason) VALUES ($1, $2, 60, 'Maintenance bassin nord')`,
    [piscineId, samedi]));
  step('Réservations du jour : confirmées, en attente, expirées, annulées et Pass Royale (qui inclut la piscine)');
  const B = [
    ['ECP-S-01', 2, 2, ['zoo', 'piscine'], null, 'CONFIRMED', null, null],          // compte : 4
    ['ECP-S-02', 2, 3, [], 'PASS_ROYALE', 'CONFIRMED', null, null],                 // compte via le pack : 5
    ['ECP-S-03', 4, 0, ['piscine'], null, 'PENDING', "NOW() + interval '20 minutes'", null], // pré-réservation active : 4
    ['ECP-S-04', 6, 0, ['piscine'], null, 'PENDING', "NOW() - interval '1 hour'", null],     // expirée : 0
    ['ECP-S-05', 3, 3, ['piscine'], null, 'CONFIRMED', null, 'NOW()'],                // annulée : 0
    ['ECP-S-06', 1, 1, ['zoo', 'pirogue'], null, 'CONFIRMED', null, null],          // sans piscine : 0
    ['ECP-S-07', 10, 30, ['piscine'], null, 'CONFIRMED', null, null],               // groupe scolaire : 40
  ];
  for (const [ref, a, c, acts, pack, state, hold, cancelled] of B) {
    await as(db, U.gui, (tx) => tx.query(
      `INSERT INTO public.bookings (reference_code, visitor_name, visitor_phone, visit_date, adults_count, children_count,
         selected_activities, selected_bundle_code, total_fcfa, payment_state, hold_expires_at, cancelled_at)
       VALUES ($1, 'Client simulation', '+237 6', $2, $3, $4, $5, $6, 0, $7, ${hold || 'NULL'}, ${cancelled || 'NULL'})`,
      [ref, samedi, a, c, acts, pack, state]));
  }
  const av = await as(db, ANON, async (tx) => (await tx.query(
    `SELECT slug, capacity, booked, remaining FROM public.get_availability($1) WHERE slug IN ('piscine', 'zoo', 'pirogue')`, [samedi])).rows);
  const pis = av.find((r) => r.slug === 'piscine');
  ok(pis.capacity === 60, 'La jauge du jour est bien de 60 places (dérogation appliquée)');
  ok(pis.booked === 53, 'Places piscine comptées : 4 + 5 (Pass Royale) + 4 (en attente) + 40 (école) = 53', `reçu ${pis.booked}`);
  ok(pis.remaining === 7, 'Il reste 7 places affichées aux visiteurs', `reçu ${pis.remaining}`);
  ok(av.find((r) => r.slug === 'zoo').booked === 11, 'Le Zoo compte 4 + 5 (Pass Royale) + 2 = 11 visiteurs', `reçu ${av.find((r) => r.slug === 'zoo').booked}`);
  const leak = await as(db, ANON, async (tx) => (await tx.query('SELECT count(*)::int AS n FROM public.bookings')).rows[0].n);
  ok(leak === 0, "Le visiteur obtient les disponibilités sans voir aucune réservation (noms, téléphones)");

  // --------------------------------------------------------------------------
  console.log('\nSCÉNARIO 4 — Deux responsables modifient la même fiche en même temps (verrou optimiste)');
  const menuId = await idOf(db, 'menu_items', 'sku', 'MNU-POISSON-BRAISE');
  const v = (await db.query('SELECT version FROM public.menu_items WHERE id = $1', [menuId])).rows[0].version;
  step(`Les deux ouvrent la fiche « Poisson Braisé » en version ${v}`);
  const r1 = await as(db, U.exp, (tx) => tx.query(
    'UPDATE public.menu_items SET price_fcfa = 5000 WHERE id = $1 AND version = $2', [menuId, v]));
  const r2 = await as(db, U.exp2, (tx) => tx.query(
    'UPDATE public.menu_items SET price_fcfa = 4000 WHERE id = $1 AND version = $2', [menuId, v]));
  const final = (await db.query('SELECT price_fcfa, version FROM public.menu_items WHERE id = $1', [menuId])).rows[0];
  ok(r1.affectedRows === 1, 'Le 1er enregistrement passe (5 000 FCFA)');
  ok(r2.affectedRows === 0, "Le 2e est bloqué : sa version est périmée, l'interface affichera « fiche modifiée par un autre administrateur »");
  ok(final.price_fcfa === 5000 && final.version === v + 1, 'Aucune modification perdue silencieusement', `prix ${final.price_fcfa}, v${final.version}`);

  // --------------------------------------------------------------------------
  console.log('\nSCÉNARIO 5 — Rupture du poisson à 14h et retour en stock');
  await as(db, U.exp, (tx) => tx.query('UPDATE public.menu_items SET in_stock = FALSE WHERE id = $1', [menuId]));
  let pub = await as(db, ANON, async (tx) => (await tx.query('SELECT in_stock FROM public.menu_items WHERE id = $1', [menuId])).rows[0]);
  ok(pub.in_stock === false, 'Le site voit le plat « en rupture » (il pourra être grisé dans la précommande)');
  await as(db, U.exp, (tx) => tx.query('UPDATE public.menu_items SET in_stock = TRUE WHERE id = $1', [menuId]));
  pub = await as(db, ANON, async (tx) => (await tx.query('SELECT in_stock FROM public.menu_items WHERE id = $1', [menuId])).rows[0]);
  ok(pub.in_stock === true, 'Retour en stock visible immédiatement');

  // --------------------------------------------------------------------------
  console.log("\nSCÉNARIO 6 — Agent guichet suspendu en cours de journée");
  const ok1 = await refused(as(db, U.gui, (tx) => tx.query(
    `INSERT INTO public.bookings (reference_code, visitor_name, visitor_phone, visit_date, total_fcfa)
     VALUES ('ECP-G-01', 'Walk-in', '+237 6', CURRENT_DATE, 2000)`)));
  ok(ok1 === null, 'Avant suspension : la vente au guichet fonctionne');
  await mfa(db, U.adm, (tx) => tx.query('UPDATE public.staff_profiles SET is_active = FALSE WHERE user_id = $1', [U.gui.id]));
  const ko = await refused(as(db, U.gui, (tx) => tx.query(
    `INSERT INTO public.bookings (reference_code, visitor_name, visitor_phone, visit_date, total_fcfa)
     VALUES ('ECP-G-02', 'Walk-in', '+237 6', CURRENT_DATE, 2000)`)));
  ok(ko?.includes('row-level security'), 'Après suspension : la vente suivante est refusée par la base');
  const susp = (await db.query(`SELECT actor_name, before_data->>'is_active' AS avant, after_data->>'is_active' AS apres
                                FROM public.audit_logs WHERE entity_table = 'staff_profiles' ORDER BY seq DESC LIMIT 1`)).rows[0];
  ok(susp.actor_name === U.adm.name && susp.avant === 'true' && susp.apres === 'false', 'La suspension est tracée avec son auteur (avant → après)');

  // --------------------------------------------------------------------------
  console.log('\nSCÉNARIO 7 — Tentatives de contournement');
  const tries = [
    ['Exploitation : baisser le prix du Zoo en ligne sans validation', as(db, U.exp, (tx) => tx.query(
      `UPDATE public.catalog_activities SET adult_price_fcfa = 100 WHERE slug = 'zoo'`)), 'ECOPARK_PUBLISHED_PRICE_LOCKED'],
    ['Administrateur : publier seul un tarif', mfa(db, U.adm, (tx) => tx.query(
      `UPDATE public.catalog_activities SET status = 'DRAFT' WHERE slug = 'pirogue'`)), 'ECOPARK_PUBLISH_REQUIRES_DIRECTION'],
    ['Visiteur : effacer le journal', as(db, ANON, (tx) => tx.query('DELETE FROM public.audit_logs')), 'permission denied'],
    ['Exploitation : supprimer une offre tarifaire (réservé Direction / Admin)', as(db, U.exp, (tx) => tx.query(
      `SELECT public.admin_delete('catalog_activities', (SELECT id FROM public.catalog_activities WHERE slug = 'zoo'))`)), 'ECOPARK_FORBIDDEN'],
  ];
  for (const [label, p, needle] of tries) {
    const msg = await refused(p);
    ok(msg?.includes(needle), `Bloqué — ${label}`, msg ? msg.split('\n')[0] : 'NON BLOQUÉ');
  }
  // Sans MFA, la Direction n'a plus de droit d'écriture : la RLS filtre la ligne (0 ligne modifiée, pas d'erreur).
  const zooBefore = (await db.query(`SELECT adult_price_fcfa FROM public.catalog_activities WHERE slug = 'zoo'`)).rows[0].adult_price_fcfa;
  const noMfa = await as(db, U.dir, (tx) => tx.query(`UPDATE public.catalog_activities SET adult_price_fcfa = 1100 WHERE slug = 'zoo'`));
  const zooAfter = (await db.query(`SELECT adult_price_fcfa FROM public.catalog_activities WHERE slug = 'zoo'`)).rows[0].adult_price_fcfa;
  ok(noMfa.affectedRows === 0 && zooAfter === zooBefore,
     'Bloqué — Direction sans double authentification : modifier un prix', `0 ligne modifiée, prix inchangé (${zooAfter} FCFA)`);

  // --------------------------------------------------------------------------
  console.log('\nSCÉNARIO 8 — Montée en charge du journal (500 modifications de jauge)');
  const tLoad = Date.now();
  const zooId = await idOf(db, 'catalog_activities', 'slug', 'zoo');
  await as(db, U.exp, async (tx) => {
    for (let i = 0; i < 500; i++) {
      await tx.query(`INSERT INTO public.daily_quotas (activity_id, quota_date, capacity, reason)
                      VALUES ($1, CURRENT_DATE + $2::int, $3, 'Simulation charge')`, [zooId, i + 1, 900 + (i % 300)]);
    }
  });
  const ms = Date.now() - tLoad;
  const chain = await mfa(db, U.dir, async (tx) => (await tx.query('SELECT * FROM public.verify_audit_chain()')).rows[0]);
  ok(Number(chain.checked_rows) > 500 && chain.is_valid, `Chaîne intègre après ${chain.checked_rows} entrées`, `500 écritures en ${ms} ms (moteur WebAssembly)`);

  // --------------------------------------------------------------------------
  console.log('\nRÉCAPITULATIF DU JOURNAL (ADM-08)');
  const summary = (await db.query(`SELECT operation, count(*)::int AS n FROM public.audit_logs GROUP BY operation ORDER BY n DESC`)).rows;
  console.log('  ' + summary.map((s) => `${s.operation}: ${s.n}`).join(' | '));

  console.log(`\n${passed} vérifications réussies, ${failed} en échec (${((Date.now() - t0) / 1000).toFixed(1)} s).`);
  if (failed) { console.log(' - ' + fails.join('\n - ')); process.exit(1); }
}

main().catch((e) => { console.error(e); process.exit(1); });
