// ============================================================================
// ECOPARK — Tests de la migration « Gouvernance CRUD » (RLS, RPC, audit immuable)
// Exécution : cd supabase/tests && npm install && npm test
// Moteur : PGlite (PostgreSQL en WebAssembly) + émulation du schéma auth Supabase.
// ============================================================================
import { PGlite } from '@electric-sql/pglite';
import { pgcrypto } from '@electric-sql/pglite/contrib/pgcrypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const sql = (p) => readFileSync(join(here, p), 'utf8');

const STUB = sql('_supabase_stub.sql');
const M1 = sql('../migrations/20261026000001_ecopark_schema_rls.sql');
const M2 = sql('../migrations/20261028000001_admin_crud_governance.sql');
const M3 = sql('../migrations/20261028000002_realtime_publication.sql');
const M4 = sql('../migrations/20261028000003_publication_images.sql');
const M5 = sql('../migrations/20261029000001_operational_missions_alerts.sql');
const M6 = sql('../migrations/20261030000001_accounts_rating_accounting.sql');

const U = {
  dir:    { id: '00000000-0000-0000-0000-0000000000d1', name: 'Dr Christophe FOE NDI', role: 'direction', matricule: 'MAT-DIR-01', pole: 'DIRECTION_GENERALE' },
  adm:    { id: '00000000-0000-0000-0000-0000000000a1', name: 'Admin Plateforme ONOGRAPH', role: 'administrateur_plateforme', matricule: 'MAT-ADM-01', pole: 'DIRECTION_GENERALE' },
  exp:    { id: '00000000-0000-0000-0000-0000000000e1', name: "Chef d'Exploitation Ahala", role: 'responsable_exploitation', matricule: 'MAT-EXP-01', pole: 'GUICHET_CAISSE' },
  cpt:    { id: '00000000-0000-0000-0000-0000000000b9', name: 'M. Paul ETOUNDI', role: 'comptable', matricule: 'MAT-CPT-01', pole: 'FINANCE_COMPTA' },
  gui:    { id: '00000000-0000-0000-0000-0000000000b1', name: 'Mme Clarisse ATANGANA', role: 'agent_guichet', matricule: 'MAT-GUI-01', pole: 'GUICHET_CAISSE' },
  ctl:    { id: '00000000-0000-0000-0000-0000000000c1', name: 'Brigade Contrôle Portail', role: 'agent_controle', matricule: 'MAT-CTL-02', pole: 'CONTROLE_QR' },
  client: { id: '00000000-0000-0000-0000-0000000000f1' },
};
const ANON = { anon: true };

let passed = 0;
let failed = 0;
const failures = [];

function ok(cond, label, detail = '') {
  if (cond) { passed++; console.log(`  [OK]   ${label}`); }
  else { failed++; failures.push(label); console.log(`  [FAIL] ${label} ${detail}`); }
}

async function as(db, who, fn, aal = 'aal1') {
  return db.transaction(async (tx) => {
    const claims = who.anon ? { role: 'anon' } : { role: 'authenticated', sub: who.id, aal };
    await tx.query(`SELECT set_config('request.jwt.claims', $1, true)`, [JSON.stringify(claims)]);
    await tx.exec(`SET LOCAL ROLE ${who.anon ? 'anon' : 'authenticated'}`);
    return fn(tx);
  });
}
const asMfa = (db, who, fn) => as(db, who, fn, 'aal2');

async function expectError(promise, needle, label) {
  try {
    await promise;
    ok(false, label, '(aucune erreur levée)');
  } catch (e) {
    const msg = `${e.message} ${e.code || ''} ${e.hint || ''}`;
    ok(msg.includes(needle), label, `(erreur reçue : ${msg.trim()})`);
  }
}

async function main() {
  const db = await PGlite.create({ extensions: { pgcrypto } });

  console.log('\n1. Application des migrations');
  await db.exec(STUB);
  await db.exec(M1);
  await db.exec(M2);
  await db.exec(M3);
  await db.exec(M4);
  await db.exec(M5);
  await db.exec(M6);
  ok(true, 'Migrations Sprint 1, Gouvernance CRUD, temps réel, images et comptes/notation/compta appliquées');
  await db.exec(M2);
  await db.exec(M4);
  await db.exec(M5);
  await db.exec(M6);
  ok(true, 'Migrations Gouvernance CRUD, images et comptes/notation/compta ré-exécutables (idempotentes)');

  // Comptes de test
  for (const u of Object.values(U)) {
    await db.query('INSERT INTO auth.users (id, email) VALUES ($1, $2)', [u.id, `${u.id}@test.local`]);
  }
  for (const u of [U.dir, U.adm, U.exp, U.cpt, U.gui, U.ctl]) {
    await db.query('INSERT INTO public.staff_profiles (user_id, full_name, role, post_label, matricule, assigned_pole) VALUES ($1, $2, $3, $4, $5, $6)',
      [u.id, u.name, u.role, 'Poste test', u.matricule, u.pole]);
  }

  const zooId = (await db.query(`SELECT id FROM public.catalog_activities WHERE slug = 'zoo'`)).rows[0].id;
  const piscineId = (await db.query(`SELECT id FROM public.catalog_activities WHERE slug = 'piscine'`)).rows[0].id;

  console.log('\n2. Données initiales & corrections de schéma');
  const counts = (await db.query(`SELECT
      (SELECT count(*) FROM public.catalog_activities WHERE status = 'PUBLISHED')::int AS cat,
      (SELECT count(*) FROM public.agenda_events WHERE status = 'PUBLISHED')::int AS agenda,
      (SELECT count(*) FROM public.menu_items)::int AS menu,
      (SELECT count(*) FROM public.site_settings)::int AS settings,
      (SELECT count(*) FROM public.gateway_health)::int AS gw,
      (SELECT sku FROM public.catalog_activities WHERE slug = 'zoo') AS zoo_sku`)).rows[0];
  ok(counts.cat === 8, `8 activités publiées (reçu ${counts.cat})`);
  ok(counts.agenda === 4, `4 événements d'agenda publiés (reçu ${counts.agenda})`);
  ok(counts.menu === 4 && counts.settings === 2 && counts.gw === 3, 'Carte (4), réglages (2), passerelles (3) initialisés');
  ok(counts.zoo_sku === 'CAT-ZOO', `SKU affiché dans l'admin dérivé du slug (reçu ${counts.zoo_sku})`);
  await expectError(
    db.query(`INSERT INTO public.bookings (reference_code, visitor_name, visitor_phone, visit_date, total_fcfa, lodge_city)
              VALUES ('T-1', 'x', 'x', CURRENT_DATE, 0, 'PARIS')`),
    'chk_bookings_lodge_city', 'CHECK lodge_city désormais appliqué (valeur PARIS rejetée)');

  console.log('\n3. Visiteur anonyme');
  await as(db, ANON, async (tx) => {
    const cat = await tx.query('SELECT count(*)::int AS n FROM public.catalog_activities');
    ok(cat.rows[0].n === 8, 'Lit le catalogue publié');
    const audit = await tx.query('SELECT count(*)::int AS n FROM public.audit_logs');
    ok(audit.rows[0].n === 0, 'Ne voit aucune ligne du journal d\'audit');
    const gw = await tx.query('SELECT count(*)::int AS n FROM public.gateway_health');
    ok(gw.rows[0].n === 0, 'Ne voit pas l\'état des passerelles de paiement');
    const avail = await tx.query(`SELECT * FROM public.get_availability(CURRENT_DATE) WHERE slug = 'zoo'`);
    ok(avail.rows[0]?.remaining === 1200, 'Lit les disponibilités via get_availability() sans accès aux réservations');
    const prof = await tx.query('SELECT public.get_my_profile() AS p');
    ok(prof.rows[0].p.role === 'visiteur_anonyme', 'get_my_profile() renvoie visiteur_anonyme');
  });
  await expectError(as(db, ANON, (tx) => tx.query(
    `INSERT INTO public.catalog_activities (slug, sku, title, pole, description, child_price_fcfa, adult_price_fcfa,
       group_adult_price_fcfa, group_child_price_fcfa, status)
     VALUES ('pirate', 'CAT-PIRATE', 'x', 'x', 'x', 0, 0, 0, 0, 'DRAFT')`)),
    'row-level security', 'Ne peut pas créer d\'offre');
  await as(db, ANON, (tx) => tx.query(
    `INSERT INTO public.group_quotes (quote_reference, organization_name, contact_name, contact_phone, group_type,
       preferred_date, participants_count, estimated_budget_fcfa)
     VALUES ('DEV-T-1', 'École test', 'M. Test', '+237 600', 'ecole', CURRENT_DATE + 10, 40, 50000)`));
  ok(true, 'Peut déposer une demande de devis (statut EN_ETUDE)');
  await expectError(as(db, ANON, (tx) => tx.query(
    `INSERT INTO public.group_quotes (quote_reference, organization_name, contact_name, contact_phone, group_type,
       preferred_date, participants_count, estimated_budget_fcfa, status)
     VALUES ('DEV-T-2', 'École test', 'M. Test', '+237 600', 'ecole', CURRENT_DATE + 10, 40, 50000, 'VALIDE')`)),
    'row-level security', 'Ne peut pas déposer un devis déjà « VALIDE »');
  await expectError(as(db, ANON, (tx) => tx.query(
    `SELECT public.log_admin_event('GUARD_REJECT', 'catalog_activities', NULL, 'x')`)),
    'permission denied', 'Ne peut pas écrire dans le journal via log_admin_event()');

  console.log('\n4. Responsable d\'exploitation (prépare, ne publie pas les tarifs)');
  let draftId;
  await as(db, U.exp, async (tx) => {
    const r = await tx.query(`SELECT public.admin_duplicate('catalog_activities', $1) AS id`, [zooId]);
    draftId = r.rows[0].id;
  });
  const draft = (await db.query('SELECT * FROM public.catalog_activities WHERE id = $1', [draftId])).rows[0];
  ok(draft.status === 'DRAFT', 'Dupliquer crée un BROUILLON');
  ok(draft.slug === 'zoo-copie-1' && draft.sku === 'CAT-ZOO-COPIE-1', `Slug / SKU uniques (reçu ${draft.slug} / ${draft.sku})`);
  ok(draft.title.endsWith('(Copie)') && draft.duplicated_from === zooId, 'Titre « (Copie) » et lien vers l\'original');
  ok(draft.is_active === false, 'Le brouillon n\'est pas visible du public (is_active synchronisé)');

  await as(db, ANON, async (tx) => {
    const r = await tx.query(`SELECT count(*)::int AS n FROM public.catalog_activities WHERE id = $1`, [draftId]);
    ok(r.rows[0].n === 0, 'Le visiteur ne voit pas le brouillon');
  });

  await as(db, U.exp, (tx) => tx.query(
    `UPDATE public.catalog_activities SET adult_price_fcfa = 1200, version = 99 WHERE id = $1`, [draftId]));
  const v = (await db.query('SELECT version, adult_price_fcfa FROM public.catalog_activities WHERE id = $1', [draftId])).rows[0];
  ok(v.adult_price_fcfa === 1200 && v.version === 2, `Modifie son brouillon ; version incrémentée par le serveur (reçu v${v.version})`);

  await expectError(as(db, U.exp, (tx) => tx.query(
    `UPDATE public.catalog_activities SET adult_price_fcfa = 1500 WHERE id = $1`, [zooId])),
    'ECOPARK_PUBLISHED_PRICE_LOCKED', 'Ne peut pas modifier le prix d\'une offre en ligne');
  await as(db, U.exp, (tx) => tx.query(
    `UPDATE public.catalog_activities SET description = 'Nouvelle description' WHERE id = $1`, [zooId]));
  ok(true, 'Peut corriger un texte d\'une offre en ligne (hors prix)');
  await expectError(as(db, U.exp, (tx) => tx.query(
    `INSERT INTO public.catalog_activities (slug, sku, title, pole, description, child_price_fcfa, adult_price_fcfa,
       group_adult_price_fcfa, group_child_price_fcfa, status)
     VALUES ('tyrolienne', 'CAT-TYRO', 'Tyrolienne', 'EAU_PLEIN_AIR', 'x', 500, 1000, 800, 500, 'PUBLISHED')`)),
    'ECOPARK_PUBLISH_REQUIRES_DIRECTION', 'Ne peut pas créer une offre directement en ligne');
  await expectError(as(db, U.exp, (tx) => tx.query(
    `SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED', TRUE)`, [draftId])),
    'ECOPARK_PUBLISH_REQUIRES_DIRECTION', 'Ne peut pas publier un tarif');
  await expectError(as(db, U.exp, (tx) => tx.query(
    `SELECT public.admin_delete('catalog_activities', $1)`, [zooId])),
    'ECOPARK_FORBIDDEN', 'Ne peut pas supprimer / archiver une offre tarifaire');

  // Contenus éditoriaux : l'Exploitation publie elle-même
  const evtId = (await db.query(`SELECT id FROM public.agenda_events WHERE code = 'EVT_DIMANCHE_ROYAL'`)).rows[0].id;
  let evtCopy;
  await as(db, U.exp, async (tx) => {
    evtCopy = (await tx.query(`SELECT public.admin_duplicate('agenda_events', $1) AS id`, [evtId])).rows[0].id;
    await tx.query(`UPDATE public.agenda_events SET target_weekday = 1, day_filter = 'LUNDI_FERIE',
                    badge = 'Lundi férié • 12h00 – 17h30' WHERE id = $1`, [evtCopy]);
    await tx.query(`SELECT public.admin_set_status('agenda_events', $1, 'PUBLISHED', FALSE)`, [evtCopy]);
  });
  const evt = (await db.query('SELECT code, status, target_weekday FROM public.agenda_events WHERE id = $1', [evtCopy])).rows[0];
  ok(evt.status === 'PUBLISHED' && evt.code === 'EVT_DIMANCHE_ROYAL_COPIE_1' && evt.target_weekday === 1,
     'Duplique un événement d\'agenda vers un autre jour et le publie');

  console.log('\n5. Direction');
  await expectError(as(db, U.dir, (tx) => tx.query(
    `SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED', TRUE)`, [draftId])),
    'ECOPARK_PUBLISH_REQUIRES_DIRECTION', 'Sans MFA (aal1) : publication refusée');
  await asMfa(db, U.dir, async (tx) => {
    const r = await tx.query(`SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED', TRUE) AS id`, [draftId]);
    ok(r.rows[0].id === zooId, 'Avec MFA : publier le brouillon remplace l\'offre d\'origine');
  });
  const zoo = (await db.query('SELECT adult_price_fcfa, title, status, slug FROM public.catalog_activities WHERE id = $1', [zooId])).rows[0];
  const dr = (await db.query('SELECT status FROM public.catalog_activities WHERE id = $1', [draftId])).rows[0];
  ok(zoo.adult_price_fcfa === 1200 && zoo.slug === 'zoo' && !zoo.title.includes('(Copie)'),
     'Nouveau prix en ligne, slug public « zoo » conservé, suffixe « (Copie) » retiré');
  ok(dr.status === 'ARCHIVED', 'Le brouillon publié est archivé (historique conservé)');

  await expectError(asMfa(db, U.dir, (tx) => tx.query(
    `UPDATE public.catalog_activities SET group_child_price_fcfa = 700 WHERE id = $1`, [zooId])),
    'chk_child_group_price_never_higher_than_individual', 'Garde-fou : 700 FCFA enfant groupe rejeté sur le Zoo');
  await asMfa(db, U.dir, (tx) => tx.query(
    `UPDATE public.catalog_activities SET group_child_price_fcfa = 1500 WHERE id = $1`, [piscineId]));
  ok(true, 'Garde-fou relatif : 1 500 FCFA enfant groupe accepté sur la Piscine');

  console.log('\n6. Administrateur plateforme');
  let freshDraft;
  await asMfa(db, U.adm, async (tx) => {
    freshDraft = (await tx.query(
      `INSERT INTO public.catalog_activities (slug, sku, title, pole, description, child_price_fcfa, adult_price_fcfa,
         group_adult_price_fcfa, group_child_price_fcfa, status)
       VALUES ('tyrolienne', 'CAT-TYRO', 'Tyrolienne', 'EAU_PLEIN_AIR', 'Test', 500, 1000, 800, 500, 'DRAFT')
       RETURNING id`)).rows[0].id;
    const del = await tx.query(`SELECT public.admin_delete('catalog_activities', $1) AS r`, [freshDraft]);
    ok(del.rows[0].r === 'DELETED', 'Supprimer un brouillon jamais publié : suppression définitive');
    const arc = await tx.query(`SELECT public.admin_delete('catalog_activities', $1) AS r`, [piscineId]);
    ok(arc.rows[0].r === 'ARCHIVED', 'Supprimer une offre déjà publiée / référencée : archivage');
    const rest = await tx.query(`SELECT public.admin_set_status('catalog_activities', $1, 'DRAFT') AS id`, [piscineId]);
    ok(!!rest.rows[0].id, 'Restaurer une offre archivée en brouillon (annulation)');
  });
  await expectError(asMfa(db, U.adm, (tx) => tx.query(
    `SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED')`, [piscineId])),
    'ECOPARK_PUBLISH_REQUIRES_DIRECTION', 'L\'administrateur ne publie pas seul un tarif');
  await expectError(asMfa(db, U.adm, (tx) => tx.query(
    `UPDATE public.staff_profiles SET role = 'direction' WHERE user_id = $1`, [U.adm.id])),
    'ECOPARK_SELF_ROLE_CHANGE_FORBIDDEN', 'Ne peut pas modifier son propre rôle');
  await asMfa(db, U.adm, (tx) => tx.query(
    `UPDATE public.staff_profiles SET is_active = FALSE WHERE user_id = $1`, [U.ctl.id]));
  await as(db, U.ctl, async (tx) => {
    const p = await tx.query('SELECT public.get_my_profile() AS p');
    ok(p.rows[0].p.role === 'client_connecte', 'Agent suspendu : perd immédiatement son rôle d\'équipe');
  });

  console.log('\n7. Agent guichet');
  await as(db, U.gui, async (tx) => {
    const r = await tx.query(`UPDATE public.catalog_activities SET title = 'Piraté' WHERE id = $1`, [zooId]);
    ok(r.affectedRows === 0, 'Ne peut modifier aucune offre (0 ligne affectée)');
    const a = await tx.query('SELECT count(*)::int AS n FROM public.audit_logs');
    ok(a.rows[0].n === 0, 'Ne lit pas le journal d\'audit');
  });

  console.log('\n7 bis. Une image pour chaque publication');
  const imgCount = (await db.query(`SELECT count(*)::int AS n FROM public.catalog_activities WHERE status = 'PUBLISHED' AND image_src IS NULL`)).rows[0].n;
  ok(imgCount === 0, 'Toutes les offres déjà en ligne ont reçu une image par défaut');
  let noImg;
  await as(db, U.exp, async (tx) => {
    noImg = (await tx.query(
      `INSERT INTO public.catalog_activities (slug, sku, title, pole, description, child_price_fcfa, adult_price_fcfa,
         group_adult_price_fcfa, group_child_price_fcfa, status)
       VALUES ('accrobranche', 'CAT-ACCRO', 'Accrobranche', 'EAU_PLEIN_AIR', 'Parcours', 500, 1500, 1200, 500, 'DRAFT') RETURNING id`)).rows[0].id;
  });
  ok(true, 'Un brouillon peut être enregistré sans image');
  await expectError(asMfa(db, U.dir, (tx) => tx.query(`SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED')`, [noImg])),
    'ECOPARK_IMAGE_REQUIRED', 'Publication refusée tant que la fiche n\'a pas d\'image');
  await expectError(as(db, U.exp, (tx) => tx.query(
    `UPDATE public.catalog_activities SET image_src = 'javascript:alert(1)' WHERE id = $1`, [noImg])),
    'image_src_safe', 'Source d\'image dangereuse (javascript:) refusée');
  await expectError(as(db, U.exp, (tx) => tx.query(
    `UPDATE public.catalog_activities SET image_src = 'https://cdn.exemple.com/a.jpg" onerror="x' WHERE id = $1`, [noImg])),
    'image_src_safe', 'Source d\'image contenant des guillemets refusée');
  await as(db, U.exp, (tx) => tx.query(
    `UPDATE public.catalog_activities SET image_src = 'https://abc.supabase.co/storage/v1/object/public/ecopark-media/catalog_activities/2026-10/x.webp' WHERE id = $1`, [noImg]));
  const alt = (await db.query('SELECT image_alt FROM public.catalog_activities WHERE id = $1', [noImg])).rows[0].image_alt;
  ok(alt === 'Accrobranche', 'Texte alternatif rempli automatiquement avec le titre', alt);
  await asMfa(db, U.dir, (tx) => tx.query(`SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED')`, [noImg]));
  ok(true, 'Avec une image téléversée (stockage Supabase), la publication passe');
  let imgDup;
  await as(db, U.exp, async (tx) => { imgDup = (await tx.query(`SELECT public.admin_duplicate('catalog_activities', $1) AS id`, [noImg])).rows[0].id; });
  const dupImg = (await db.query('SELECT image_src FROM public.catalog_activities WHERE id = $1', [imgDup])).rows[0].image_src;
  ok(dupImg && dupImg.endsWith('x.webp'), 'La copie reprend l\'image de l\'original');
  await as(db, U.exp, (tx) => tx.query(`UPDATE public.catalog_activities SET image_src = 'audit-assets/ecopark-real-media/balade_pirogue3.jpg', image_alt = 'Nouvelle photo' WHERE id = $1`, [imgDup]));
  await asMfa(db, U.dir, (tx) => tx.query(`SELECT public.admin_set_status('catalog_activities', $1, 'PUBLISHED', TRUE)`, [imgDup]));
  const replaced = (await db.query('SELECT image_src, image_alt FROM public.catalog_activities WHERE id = $1', [noImg])).rows[0];
  ok(replaced.image_src.endsWith('balade_pirogue3.jpg') && replaced.image_alt === 'Nouvelle photo', 'Publier la version de travail remplace aussi l\'image en ligne');
  await expectError(asMfa(db, U.dir, (tx) => tx.query(`UPDATE public.catalog_activities SET image_src = NULL WHERE id = $1`, [noImg])),
    'ECOPARK_IMAGE_REQUIRED', 'Impossible de retirer l\'image d\'une offre en ligne');

  console.log('\n7 ter. Fiches de Mission A4, 3 Visas & Alertes de Poste (20261029000001)');
  const msnCount = (await db.query(`SELECT count(*)::int AS n FROM public.operational_missions`)).rows[0].n;
  const altCount = (await db.query(`SELECT count(*)::int AS n FROM public.operational_alerts`)).rows[0].n;
  ok(msnCount === 4 && altCount === 4, `4 Fiches de Mission A4 et 4 Alertes initiales (reçu ${msnCount} / ${altCount})`);

  await as(db, ANON, async (tx) => {
    const mAnon = await tx.query('SELECT count(*)::int AS n FROM public.operational_missions');
    const aAnon = await tx.query('SELECT count(*)::int AS n FROM public.operational_alerts');
    ok(mAnon.rows[0].n === 0 && aAnon.rows[0].n === 0, 'Visiteur anonyme : aucun accès aux Fiches de Mission ni aux Alertes');
  });

  await as(db, U.gui, async (tx) => {
    const r2 = (await tx.query(`SELECT public.sign_mission_visa('MSN-2026-103', 'visa2', 'M. Samuel MBARGA (MAT-SEC-04)') AS r`)).rows[0].r;
    ok(r2.status === 'EN_COURS' && r2.visas?.visa2?.signed === true, 'Agent guichet/terrain : émarge le Visa #2 (statut passe à EN_COURS)');
    const ack = (await tx.query(`SELECT public.acknowledge_operational_alert('ALT-2026-203') AS r`)).rows[0].r;
    ok(ack.acknowledged === true, 'Agent guichet/terrain : acquitte une alerte de poste via acknowledge_operational_alert()');
  });

  await expectError(as(db, U.gui, (tx) => tx.query(
    `SELECT public.sign_mission_visa('MSN-2026-103', 'visa3')`)),
    'ECOPARK_VISA_REQUIRES_EXPLOITATION', 'Agent guichet : ne peut pas signer seul le Visa #3 de clôture (réservé Exploitation / Direction)');

  await as(db, U.exp, async (tx) => {
    const r3 = (await tx.query(`SELECT public.rate_mission_on_visa3('MSN-2026-103', 38, 'Pavillons Ewondo impeccables à 14h00', 0, 'Chef d''Exploitation Ahala') AS r`)).rows[0].r;
    const allDone = Array.isArray(r3.checklist) && r3.checklist.every((c) => c.done === true);
    ok(r3.status === 'TERMINEE' && r3.visas?.visa3?.signed === true && allDone,
       'Responsable d\'exploitation : signe le Visa #3 (statut TERMINEE + 3/3 Visas + check-list complétée)');
    ok(r3.rating_auto_60 >= 54 && r3.rating_supervisor_40 === 38 && r3.rating_total_100 >= 92 && Number(r3.rating_stars) >= 4.5,
       `Notation agent au Visa #3 : ${r3.rating_total_100}/100 (${r3.rating_stars}/5 étoiles)`);
  });

  console.log('\n7 quater. Rôle Comptable (8e rôle) & Comptabilité Analytique (20261030000001)');
  await as(db, U.cpt, async (tx) => {
    const prof = (await tx.query('SELECT public.get_my_profile() AS p')).rows[0].p;
    ok(prof.role === 'comptable' && prof.matricule === 'MAT-CPT-01' && prof.assigned_pole === 'FINANCE_COMPTA',
       'get_my_profile() renvoie le rôle comptable, son matricule MAT-CPT-01 et son pôle FINANCE_COMPTA');
    const qRead = await tx.query('SELECT count(*)::int AS n FROM public.group_quotes');
    const aRead = await tx.query('SELECT count(*)::int AS n FROM public.audit_logs');
    ok(qRead.rows[0].n >= 1 && aRead.rows[0].n >= 1, 'Comptable : lit les devis B2B et le journal d\'audit financier');
    const ledger = await tx.query('SELECT * FROM public.get_analytical_accounting_ledger()');
    ok(ledger.rows.length === 6 && ledger.rows[0].analytical_code === 'ANA-01' && ledger.rows[5].analytical_code === 'ANA-06',
       'Comptable : exécute get_analytical_accounting_ledger() (6 axes analytiques ANA-01 à ANA-06)');
    const mut = await tx.query(`UPDATE public.catalog_activities SET adult_price_fcfa = 9999 WHERE id = $1`, [zooId]);
    ok(mut.affectedRows === 0, 'Comptable : lecture seule stricte sur les tarifs (0 ligne modifiée)');
  });
  await expectError(as(db, U.gui, (tx) => tx.query('SELECT * FROM public.get_analytical_accounting_ledger()')),
    'ECOPARK_FORBIDDEN', 'Agent guichet : ne peut pas accéder au grand-livre analytique comptable');

  console.log('\n8. Journal d\'audit immuable (ADM-08)');
  const ops = (await db.query(`SELECT DISTINCT operation FROM public.audit_logs`)).rows.map((r) => r.operation);
  for (const op of ['INSERT', 'UPDATE', 'DUPLICATE', 'PUBLISH', 'ARCHIVE', 'DELETE', 'RESTORE']) {
    ok(ops.includes(op), `Opération « ${op} » tracée`);
  }
  const dup = (await db.query(`SELECT actor_name, actor_role FROM public.audit_logs WHERE operation = 'DUPLICATE' ORDER BY seq LIMIT 1`)).rows[0];
  ok(dup.actor_name === U.exp.name && dup.actor_role === 'responsable_exploitation', 'Auteur nominatif et rôle enregistrés');

  await as(db, U.exp, (tx) => tx.query(
    `SELECT public.log_admin_event('GUARD_REJECT', 'catalog_activities', $1, 'Saisie 700 FCFA rejetée')`, [zooId]));
  const gr = (await db.query(`SELECT count(*)::int AS n FROM public.audit_logs WHERE operation = 'GUARD_REJECT'`)).rows[0].n;
  ok(gr === 1, 'Rejet du garde-fou journalisé via log_admin_event()');
  await expectError(as(db, U.exp, (tx) => tx.query(
    `SELECT public.log_admin_event('FAUX_CODE', NULL, NULL, 'x')`)),
    'ECOPARK_INVALID_EVENT_CODE', 'Code d\'événement hors liste refusé');

  await expectError(db.query(`UPDATE public.audit_logs SET description = 'falsifié'`),
    'ECOPARK_AUDIT_IMMUTABLE', 'UPDATE interdit même pour le propriétaire de la base');
  await expectError(db.query(`DELETE FROM public.audit_logs`),
    'ECOPARK_AUDIT_IMMUTABLE', 'DELETE interdit même pour le propriétaire de la base');
  await expectError(db.query(`TRUNCATE public.audit_logs`),
    'ECOPARK_AUDIT_IMMUTABLE', 'TRUNCATE interdit');
  await expectError(asMfa(db, U.adm, (tx) => tx.query(
    `INSERT INTO public.audit_logs (actor_name, action_code, description) VALUES ('x', 'x', 'x')`)),
    'row-level security', 'Insertion directe dans le journal refusée');

  await expectError(as(db, U.exp, (tx) => tx.query('SELECT * FROM public.verify_audit_chain()')),
    'ECOPARK_FORBIDDEN', 'Vérification de la chaîne réservée à la Direction / Admin');
  await asMfa(db, U.dir, async (tx) => {
    const r = (await tx.query('SELECT * FROM public.verify_audit_chain()')).rows[0];
    ok(r.is_valid === true && Number(r.checked_rows) > 10, `Chaîne SHA-256 intègre (${r.checked_rows} entrées)`);
  });

  // Falsification par un super-utilisateur qui désactive le trigger : détectée
  await db.exec(`ALTER TABLE public.audit_logs DISABLE TRIGGER trg_audit_logs_immutable;
                 UPDATE public.audit_logs SET description = 'falsifié' WHERE seq = 5;
                 ALTER TABLE public.audit_logs ENABLE TRIGGER trg_audit_logs_immutable;`);
  await asMfa(db, U.dir, async (tx) => {
    const r = (await tx.query('SELECT * FROM public.verify_audit_chain()')).rows[0];
    ok(r.is_valid === false && Number(r.first_broken_seq) === 5, `Falsification détectée à l'entrée n°${r.first_broken_seq}`);
  });

  console.log(`\n${passed} tests réussis, ${failed} en échec.`);
  if (failed) {
    console.log('Échecs :\n - ' + failures.join('\n - '));
    process.exit(1);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
