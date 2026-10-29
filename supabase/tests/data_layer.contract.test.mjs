// ============================================================================
// ECOPARK — Tests de contrat de la couche d'accès aux données (Phase 3)
// La MÊME série est jouée contre les deux pilotes :
//   - LocalDemoDriver (localStorage simulé)
//   - SupabaseDriver branché sur le vrai SQL (PGlite : RLS, triggers, RPC)
// + convertisseurs (aller-retour), traduction des erreurs, choix du pilote.
// Exécution : cd supabase/tests && node data_layer.contract.test.mjs
// ============================================================================
import { PGlite } from '@electric-sql/pglite';
import { pgcrypto } from '@electric-sql/pglite/contrib/pgcrypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import { createPgliteSupabaseClient } from './pglite_supabase_client.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const sql = (p) => readFileSync(join(here, p), 'utf8');
await import(pathToFileURL(resolve(here, '..', '..', 'etape0-site-live', 'js', 'ecopark-data.js')).href);
const ED = globalThis.EcoparkData;
const SNAPSHOT = JSON.parse(readFileSync(resolve(here, '..', '..', 'etape0-site-live', 'content-snapshot.json'), 'utf8'));

const U = {
  dir: { id: '00000000-0000-0000-0000-0000000000d1', name: 'Dr Christophe FOE NDI', role: 'direction' },
  exp: { id: '00000000-0000-0000-0000-0000000000e1', name: "Chef d'Exploitation Ahala", role: 'responsable_exploitation' },
};

let passed = 0, failed = 0;
const fails = [];
const ok = (c, label, detail = '') => {
  if (c) { passed++; console.log(`    [OK]   ${label}${detail ? ' — ' + detail : ''}`); }
  else { failed++; fails.push(label); console.log(`    [FAIL] ${label}${detail ? ' — ' + detail : ''}`); }
};
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);

function memoryStorage() {
  const m = {};
  return { getItem: (k) => (k in m ? m[k] : null), setItem: (k, v) => { m[k] = String(v); }, removeItem: (k) => { delete m[k]; } };
}
const LEGACY_DEFAULTS = { bookings: [], quotes: [], cfpApplications: [], appointments: [], auditLogs: [], posStats: {}, dirStats: {} };

// --- Mise en place des deux pilotes ----------------------------------------
async function setupLocal() {
  globalThis.ECOPARK_CONFIG = { env: 'test', dataDriver: 'local' };
  ED.configureLegacy({ storageKey: 'ecopark_test_local', defaults: LEGACY_DEFAULTS, snapshot: SNAPSHOT });
  await ED.init({ storage: memoryStorage(), search: '', demoRole: 'responsable_exploitation' });
  return {
    name: 'LocalDemoDriver',
    as: async (u) => { ED.driver.role = u.role; },
    asNoMfa: null,
    serverRow: async (entity, col, val) => ED.store.content(entity).find((r) => r[col] === val),
    quotes: async () => ED.store.state.quotes,
  };
}
async function setupSupabase() {
  const db = await PGlite.create({ extensions: { pgcrypto } });
  await db.exec(sql('_supabase_stub.sql'));
  await db.exec(sql('../migrations/20261026000001_ecopark_schema_rls.sql'));
  await db.exec(sql('../migrations/20261028000001_admin_crud_governance.sql'));
  await db.exec(sql('../migrations/20261028000002_realtime_publication.sql'));
  await db.exec(sql('../migrations/20261028000003_publication_images.sql'));
  await db.exec(sql('../migrations/20261029000001_operational_missions_alerts.sql'));
  await db.exec(sql('../migrations/20261030000001_accounts_rating_accounting.sql'));
  for (const u of Object.values(U)) {
    await db.query('INSERT INTO auth.users (id, email) VALUES ($1, $2)', [u.id, `${u.id}@t.local`]);
    await db.query('INSERT INTO public.staff_profiles (user_id, full_name, role) VALUES ($1, $2, $3)', [u.id, u.name, u.role]);
  }
  const client = createPgliteSupabaseClient(db);
  client.setUser(U.exp, 'aal1');
  globalThis.ECOPARK_CONFIG = { env: 'test', dataDriver: 'supabase', supabaseUrl: 'http://pglite', supabaseAnonKey: 'anon' };
  ED.configureLegacy({ storageKey: 'unused', defaults: LEGACY_DEFAULTS, snapshot: SNAPSHOT });
  await ED.init({ storage: memoryStorage(), search: '', client, pollMs: 0 });
  return {
    name: 'SupabaseDriver (SQL réel via PGlite)',
    as: async (u) => { client.setUser(u, u.role === 'direction' ? 'aal2' : 'aal1'); },
    asNoMfa: async (u) => { client.setUser(u, 'aal1'); },
    serverRow: async (entity, col, val) => (await db.query(`SELECT * FROM public.${entity} WHERE ${col} = $1`, [val])).rows[0],
    quotes: async () => (await db.query('SELECT * FROM public.group_quotes')).rows,
    client,
  };
}

// --- Série de contrat commune -----------------------------------------------
async function contract(env) {
  console.log(`\n  ${env.name}`);
  const cat = () => ED.content('catalog_activities', { includeDrafts: true });
  ok(ED.content('catalog_activities').length >= 8, 'Hydratation : 8+ activités publiées dans le magasin (incl. Totem)');
  ok(ED.content('agenda_events').length === 4, 'Hydratation : 4 événements d\'agenda');
  const wb = ED.setting('weather_banner');
  ok(wb && wb.active_preset === 'SUNNY' && /Ensoleillé/.test(wb.presets.SUNNY), 'Réglage « bandeau météo » lisible de façon synchrone');

  await env.as(U.exp);
  const zoo = cat().find((r) => r.slug === 'zoo');
  const dup = await ED.duplicate('catalog_activities', zoo.id);
  ok(dup.ok, 'Dupliquer (Exploitation) réussit', dup.ok ? '' : dup.error.message);
  const copy = cat().find((r) => r.id === dup.data);
  ok(copy && copy.status === 'DRAFT' && copy.slug === 'zoo-copie-1' && /\(Copie\)$/.test(copy.title), 'Copie en brouillon, slug zoo-copie-1, titre « (Copie) »', copy ? `${copy.slug} / ${copy.status}` : 'absente du magasin');
  ok(ED.content('catalog_activities').every((r) => r.id !== dup.data), 'La copie n\'apparaît pas dans le contenu publié');

  const up = await ED.update('catalog_activities', copy.id, { adult_price_fcfa: 1200 }, copy.version);
  ok(up.ok && up.data.version === copy.version + 1, 'Modifier le brouillon avec la bonne version', up.ok ? `v${up.data.version}` : up.error.message);
  const stale = await ED.update('catalog_activities', copy.id, { adult_price_fcfa: 1300 }, copy.version);
  ok(!stale.ok && stale.error.code === 'VERSION_CONFLICT', 'Version périmée : conflit détecté', stale.ok ? '' : stale.error.message);

  const before = JSON.stringify(ED.store.state.content.catalog_activities);
  const locked = await ED.update('catalog_activities', zoo.id, { adult_price_fcfa: 100 }, zoo.version);
  ok(!locked.ok && locked.error.code === 'PUBLISHED_PRICE_LOCKED', 'Prix en ligne verrouillé pour l\'Exploitation', locked.ok ? '' : locked.error.message);
  ok(JSON.stringify(ED.store.state.content.catalog_activities) === before, 'Retour arrière : le magasin est revenu à l\'état précédent');

  const pubKo = await ED.setStatus('catalog_activities', copy.id, 'PUBLISHED', true);
  ok(!pubKo.ok && pubKo.error.code === 'PUBLISH_REQUIRES_DIRECTION', 'Publication refusée à l\'Exploitation');

  await env.as(U.dir);
  const pub = await ED.setStatus('catalog_activities', copy.id, 'PUBLISHED', true);
  ok(pub.ok && pub.data === zoo.id, 'Direction : publier remplace la fiche d\'origine', pub.ok ? '' : pub.error.message);
  const zooNow = ED.content('catalog_activities').find((r) => r.slug === 'zoo');
  ok(zooNow && zooNow.adult_price_fcfa === 1200 && !/Copie/.test(zooNow.title), 'Magasin à jour : Zoo à 1 200 FCFA sous le slug « zoo »');
  const srv = await env.serverRow('catalog_activities', 'slug', 'zoo');
  ok(srv && srv.adult_price_fcfa === 1200, 'Valeur enregistrée côté stockage du pilote');

  const guard = await ED.update('catalog_activities', zooNow.id, { group_child_price_fcfa: 700 }, zooNow.version);
  ok(!guard.ok && guard.error.code === 'CHILD_PRICE_GUARD', 'Garde-fou enfant : message français dédié', guard.ok ? '' : guard.error.message);

  const fresh = await ED.create('catalog_activities', {
    slug: 'tyrolienne', sku: 'CAT-TYRO', title: 'Tyrolienne', pole: 'EAU_PLEIN_AIR', description: 'Test',
    child_price_fcfa: 500, adult_price_fcfa: 1000, group_adult_price_fcfa: 800, group_child_price_fcfa: 500, status: 'DRAFT'
  });
  ok(fresh.ok, 'Ajouter une offre en brouillon', fresh.ok ? '' : fresh.error.message);
  const dupKey = await ED.create('catalog_activities', {
    slug: 'tyrolienne', sku: 'CAT-TYRO', title: 'Doublon', pole: 'EAU_PLEIN_AIR', description: 'Test',
    child_price_fcfa: 500, adult_price_fcfa: 1000, group_adult_price_fcfa: 800, group_child_price_fcfa: 500, status: 'DRAFT'
  });
  ok(!dupKey.ok && dupKey.error.code === 'DUPLICATE_KEY', 'Doublon de SKU / slug refusé');
  const del1 = await ED.remove('catalog_activities', fresh.data.id);
  ok(del1.ok && del1.data === 'DELETED', 'Supprimer un brouillon jamais publié : DELETED');
  const pir = ED.content('catalog_activities').find((r) => r.slug === 'pirogue');
  const del2 = await ED.remove('catalog_activities', pir.id);
  ok(del2.ok && del2.data === 'ARCHIVED', 'Supprimer une offre publiée : ARCHIVED');
  ok(!ED.content('catalog_activities').some((r) => r.slug === 'pirogue'), 'L\'offre archivée disparaît du contenu public');
  const restore = await ED.setStatus('catalog_activities', pir.id, 'PUBLISHED');
  ok(restore.ok && ED.content('catalog_activities').some((r) => r.slug === 'pirogue'), 'Annulation : republication par la Direction');

  await env.as(U.exp);
  const evt = ED.content('agenda_events').find((e) => e.code === 'EVT_DIMANCHE_ROYAL');
  const evtDup = await ED.duplicate('agenda_events', evt.id);
  const evtPub = evtDup.ok ? await ED.setStatus('agenda_events', evtDup.data, 'PUBLISHED') : evtDup;
  ok(evtPub.ok && ED.content('agenda_events').length === 5, 'Agenda : l\'Exploitation duplique et publie elle-même');

  // Dépôt public d'un devis depuis le format historique du site
  const legacyQuote = {
    reference: 'DEV-2026-7001', org: 'École Bilingue Les Palmiers', phone: '+237 677 11 22 33',
    type: 'Excursion scolaire (Esplanade / Salle Menkii Essomba Anton & Encadrement Parc)', pax: 60,
    date: '2026-12-10', budgetFcfa: 90000, status: 'Proforma générée'
  };
  if (env.client) env.client.setUser(null);
  const q = ED.driverName === 'supabase'
    ? await ED.create('group_quotes', legacyQuote, { legacy: true, anonymous: true })
    : await ED.create('group_quotes', legacyQuote);
  ok(q.ok, 'Devis déposé par un visiteur anonyme', q.ok ? '' : q.error.message);
  const stored = (await env.quotes()).find((r) => (r.quote_reference || r.reference) === 'DEV-2026-7001');
  ok(!!stored, 'Le devis est bien stocké');
  if (ED.driverName === 'supabase') {
    ok(stored.group_type === 'ecole' && stored.preferred_date && stored.status === 'EN_ETUDE' && stored.hall_menkii_included === true,
       'Conversion vers la base : type ecole, date ISO, statut EN_ETUDE, salle Menkii détectée');
    const reread = await ED.list('group_quotes');
    ok(reread.ok && reread.data.length === 0, 'Le visiteur ne peut relire aucun devis (RLS)');
  }

  // Une image pour chaque publication
  await env.as(U.exp);
  const sansImg = await ED.create('catalog_activities', {
    slug: 'accrobranche', sku: 'CAT-ACCRO', title: 'Accrobranche', pole: 'EAU_PLEIN_AIR', description: 'Parcours',
    child_price_fcfa: 500, adult_price_fcfa: 1500, group_adult_price_fcfa: 1200, group_child_price_fcfa: 500, status: 'DRAFT'
  });
  ok(sansImg.ok, 'Brouillon sans image accepté', sansImg.ok ? '' : sansImg.error.message);
  await env.as(U.dir);
  const pubSans = await ED.setStatus('catalog_activities', sansImg.data.id, 'PUBLISHED');
  ok(!pubSans.ok && pubSans.error.code === 'IMAGE_REQUIRED', 'Publication sans image refusée (message dédié)', pubSans.ok ? '' : pubSans.error.message);
  const PNG = Uint8Array.from(Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==', 'base64'));
  await env.as(U.exp);
  const upImg = await ED.uploadImage(new Blob([PNG], { type: 'image/png' }), { entity: 'catalog_activities' });
  const expectedPrefix = ED.driverName === 'supabase' ? 'https://test-project.supabase.co/storage/v1/object/public/ecopark-media/catalog_activities/' : 'data:image/png;base64,';
  ok(upImg.ok && upImg.data.url.startsWith(expectedPrefix), 'Téléversement d\'une photo', upImg.ok ? upImg.data.url.slice(0, 70) : upImg.error.message);
  if (env.client) {
    const last = env.client._uploads[env.client._uploads.length - 1];
    ok(last && last.bucket === 'ecopark-media' && last.contentType === 'image/png' && last.upsert === false, 'Dépôt dans l\'espace « ecopark-media », sans écrasement');
  }
  const badType = await ED.uploadImage(new Blob(['<svg onload=alert(1)>'], { type: 'image/svg+xml' }), { entity: 'catalog_activities' });
  ok(!badType.ok && badType.error.code === 'IMAGE_TYPE', 'Format SVG refusé (risque d\'injection)');
  const cur = ED.content('catalog_activities', { includeDrafts: true }).find((r) => r.slug === 'accrobranche');
  const setImg = await ED.update('catalog_activities', cur.id, { image_src: upImg.data.url }, cur.version);
  ok(setImg.ok, 'Image associée au brouillon', setImg.ok ? '' : setImg.error.message);
  const badSrc = await ED.update('catalog_activities', cur.id, { image_src: 'javascript:alert(1)' }, setImg.ok ? setImg.data.version : cur.version);
  ok(!badSrc.ok && badSrc.error.code === 'IMAGE_SOURCE', 'Source d\'image dangereuse refusée', badSrc.ok ? '' : badSrc.error.code);
  await env.as(U.dir);
  const pubAvec = await ED.setStatus('catalog_activities', cur.id, 'PUBLISHED');
  const live = ED.content('catalog_activities').find((r) => r.slug === 'accrobranche');
  ok(pubAvec.ok && live && live.image_src === upImg.data.url && live.image_alt === 'Accrobranche', 'Avec une image : publiée, texte alternatif rempli', pubAvec.ok ? '' : pubAvec.error.message);

  // Réglages du site et dérogations de jauge (console ADM-03)
  await env.as(U.exp);
  const wbNow = ED.setting('weather_banner');
  const sv = await ED.saveSetting('weather_banner', Object.assign({}, wbNow, { active_preset: 'RAIN_GUARANTEE' }));
  ok(sv.ok && ED.setting('weather_banner').active_preset === 'RAIN_GUARANTEE', 'Bandeau météo enregistré et relu (saveSetting)', sv.ok ? '' : sv.error.message);
  const pisc = ED.content('catalog_activities').find((r) => r.slug === 'piscine');
  const qc = await ED.create('daily_quotas', { activity_id: pisc.id, quota_date: '2026-11-07', capacity: 60, reason: 'Contrat' });
  ok(qc.ok, 'Dérogation de jauge créée', qc.ok ? '' : qc.error.message);
  const ql = await ED.list('daily_quotas', { filters: { quota_date: '2026-11-07' } });
  const qrow = ql.ok && ql.data.find((r) => r.activity_id === pisc.id);
  ok(!!qrow && qrow.capacity === 60, 'Dérogation relue pour la date');
  const qd = qrow ? await ED.removeRow('daily_quotas', qrow.id) : { ok: false };
  const ql2 = await ED.list('daily_quotas', { filters: { quota_date: '2026-11-07' } });
  ok(qd.ok && ql2.ok && !ql2.data.some((r) => r.activity_id === pisc.id), 'Retour à la jauge standard (removeRow)');

  // Fiches de Mission A4, 3 Visas & Alertes de Poste
  const msnCreate = await ED.create('operational_missions', {
    id: 'MSN-2026-901', orderRef: 'EPK-2026-9901', orderCustomer: 'Famille Test Contrat', orderTotalFcfa: 14000,
    orderSummary: '2 Adultes, 2 Enfants • Pass Découverte', pole: 'GUICHET_CAISSE', poleLabel: 'Guichet & Caisse RN3',
    badgeClass: 'eco-cat-nature', agentName: 'Mme Clarisse ATANGANA', agentMatricule: 'MAT-GUI-01',
    agentRole: 'Caissière Principale Guichet RN3', date: '2026-11-20', shift: 'Matinée (08h30 – 14h30)',
    priority: 'HAUTE', status: 'ASSIGNEE', title: 'Accueil Guichet & Bracelets — EPK-2026-9901',
    location: 'Guichet Principal RN3 Ahala', objective: 'Contrôler billet et remettre bracelets.',
    equipment: 'Caisse POS #01', guardrail: 'Tarif enfant 500 FCFA protégé.',
    checklist: [{ text: 'Vérifier référence EPK-2026-9901', done: false }], assignedBy: "Chef d'Exploitation Ahala"
  }, { legacy: true });
  ok(msnCreate.ok, 'Création d\'une Fiche de Mission A4 via EcoparkData', msnCreate.ok ? '' : msnCreate.error.message);

  const altCreate = await ED.create('operational_alerts', {
    alertId: 'ALT-2026-901', missionId: 'MSN-2026-901', orderRef: 'EPK-2026-9901', customerName: 'Famille Test Contrat',
    orderSummary: '2 Adultes, 2 Enfants', amountFcfa: 14000, pole: 'GUICHET_CAISSE', poleLabel: 'Guichet & Caisse RN3',
    badgeClass: 'eco-cat-nature', agentName: 'Mme Clarisse ATANGANA', agentMatricule: 'MAT-GUI-01',
    title: 'Accueil Guichet & Bracelets — EPK-2026-9901', acknowledged: false
  }, { legacy: true });
  ok(altCreate.ok, 'Création d\'une Alerte de Poste via EcoparkData', altCreate.ok ? '' : altCreate.error.message);

  const v2 = await ED.signMissionVisa('MSN-2026-901', 'visa2', 'Mme Clarisse ATANGANA (MAT-GUI-01)');
  ok(v2.ok && v2.data.status === 'EN_COURS' && v2.data.visas?.visa2?.signed === true, 'Signature du Visa #2 via EcoparkData.signMissionVisa()', v2.ok ? '' : v2.error.message);

  const ackRes = await ED.acknowledgeAlert('ALT-2026-901');
  ok(ackRes.ok && ackRes.data.acknowledged === true, 'Acquittement de l\'alerte via EcoparkData.acknowledgeAlert()', ackRes.ok ? '' : ackRes.error.message);

  const v3 = await ED.signMissionVisa('MSN-2026-901', 'visa3', "Chef d'Exploitation Ahala");
  ok(v3.ok && v3.data.status === 'TERMINEE' && v3.data.visas?.visa3?.signed === true, 'Signature du Visa #3 (clôture) via EcoparkData.signMissionVisa()', v3.ok ? '' : v3.error.message);

  const rated = await ED.rateMissionOnVisa3('MSN-2026-901', 38, 'Excellent accueil et caisse exacte', "Chef d'Exploitation Ahala");
  const ratedTotal = rated.data && (rated.data.rating_total_100 ?? rated.data.ratingTotal100);
  const ratedStars = rated.data && Number(rated.data.rating_stars ?? rated.data.ratingStars);
  ok(rated.ok && ratedTotal === 98 && ratedStars === 4.9, 'Notation agent sur Visa #3 (98/100 • 4.9/5) via EcoparkData.rateMissionOnVisa3()', rated.ok ? '' : rated.error.message);

  const ana = await ED.getAnalyticalLedger('2026-01-01', '2026-12-31');
  ok(ana.ok && Array.isArray(ana.data) && ana.data.length === 6 && ana.data[0].analytical_code === 'ANA-01', 'Grand Livre Analytique (6 centres de profit ANA-01 à ANA-06) via EcoparkData.getAnalyticalLedger()', ana.ok ? '' : ana.error.message);

  if (env.asNoMfa) {
    await env.asNoMfa(U.dir);
    const z = ED.content('catalog_activities').find((r) => r.slug === 'zoo');
    const noMfa = await ED.update('catalog_activities', z.id, { adult_price_fcfa: 1100 }, z.version);
    ok(!noMfa.ok && noMfa.error.code === 'NO_RIGHTS', 'Direction sans double authentification : « rien n\'a été enregistré »', noMfa.ok ? '' : noMfa.error.message);
    ok(ED.content('catalog_activities').find((r) => r.slug === 'zoo').adult_price_fcfa === 1200, 'Affichage optimiste annulé (1 200 FCFA conservés)');
  }
}

// --- Tests unitaires ---------------------------------------------------------
function unit() {
  console.log('\n  Convertisseurs (aller-retour format historique <-> base)');
  const M = ED.Mappers;
  ok(M.isoToFr('2026-11-15') === '15/11/2026' && M.frToIso('15/11/2026') === '2026-11-15' && M.frToIso('5/1/2027') === '2027-01-05', 'Dates JJ/MM/AAAA <-> ISO');
  ok(M.frToIso('n\'importe quoi') === null, 'Date invalide rejetée (null)');
  ok(M.tsToFr('2026-10-26T07:45:00Z') === '26/10/2026 08:45', 'Horodatage affiché à l\'heure de Yaoundé (UTC+1)');
  ok(M.toFcfa('14 000 FCFA') === 14000 && M.toFcfa(-5) === 0 && M.toFcfa(1500.6) === 1501, 'Montants FCFA entiers et positifs');

  const R = M.registry;
  const quote = { reference: 'DEV-1', org: 'Ministère X', phone: '+237 6', type: 'Séminaire & Conférence (Navette Climatisée A/R)', pax: 50, date: '10/12/2026', budgetFcfa: 670000, status: 'Proposition envoyée' };
  const qBack = R.group_quotes.fromRow(Object.assign({ id: 'x' }, R.group_quotes.toRow(quote)));
  ok(R.group_quotes.toRow(quote).group_type === 'entreprise' && R.group_quotes.toRow(quote).shuttle_included === true, 'Devis : séminaire -> entreprise, navette détectée');
  ok(['reference', 'org', 'phone', 'type', 'pax', 'date', 'budgetFcfa', 'status'].every((k) => eq(qBack[k], quote[k])), 'Devis : aller-retour sans perte');

  const cfp = { reference: 'CFP-1', name: 'Ngaoundéré Paulin (19 ans)', track: 'Pisciculture • Échéancier 4 tranches (100k + 3x50k FCFA)', phone: '+237 6', status: 'Dossier reçu (Inscription 50 000 FCFA)' };
  const cRow = R.cfp_applications.toRow(cfp);
  const cBack = R.cfp_applications.fromRow(Object.assign({ id: 'x' }, cRow));
  ok(cRow.candidate_age === 19 && cRow.program_track === 'Pisciculture' && cRow.payment_plan === '4_TRANCHES' && cRow.status === 'DOSSIER_RECU', 'CFP : âge, filière, échéancier et statut extraits');
  ok(['reference', 'name', 'track', 'phone', 'status'].every((k) => eq(cBack[k], cfp[k])), 'CFP : aller-retour sans perte');

  const rdv = { reference: 'RDV-1', visitorName: 'Mme Essomba', org: 'Mairie', phone: '+237 6', purposeCode: 'reperage_mariage', purposeLabel: 'Repérage mariage', date: '20/11/2026', slot: '11h00', mode: 'Sur site (Ahala Barrière)', status: 'RDV Confirmé (11h00)' };
  const rBack = R.appointments.fromRow(Object.assign({ id: 'x' }, R.appointments.toRow(rdv)));
  ok(Object.keys(rdv).every((k) => eq(rBack[k], rdv[k])), 'Rendez-vous : aller-retour sans perte');

  const bk = { reference: 'ECP-1', holder: 'M. Mbarga', phone: '+237 6', date: '15/11/2026', paxSummary: '2 Adulte(s), 2 Enfant(s) • Visite', totalFcfa: 14000, payMethod: 'OM', lodgeCity: null, hasPergola: false, status: 'HELD_11H', scanned: false, scannedAt: null };
  const bRow = Object.assign({ id: 'x', selected_activities: [], selected_bundle_code: null, qr_status: 'VALID' }, R.bookings.toRow(bk));
  const bBack = R.bookings.fromRow(bRow);
  ok(bRow.payment_state === 'PENDING' && bRow.adults_count === 2 && bRow.children_count === 2, 'Réservation : pré-réservation 11h -> PENDING, participants extraits');
  ok(['reference', 'holder', 'phone', 'date', 'paxSummary', 'totalFcfa', 'status', 'scanned'].every((k) => eq(bBack[k], bk[k])), 'Réservation : aller-retour sans perte');

  console.log('\n  Traduction des erreurs');
  const T = ED.Errors.translate;
  ok(T({ message: 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' }).code === 'PUBLISH_REQUIRES_DIRECTION', 'Publication réservée à la Direction');
  ok(/1 500 FCFA|1500 FCFA/.test(T({ code: '23514', message: 'violates check constraint "chk_child_group_price_never_higher_than_individual"' }, { row: { child_price_fcfa: 1500, group_child_price_fcfa: 2000 } }).message), 'Garde-fou : le plafond propre à la ligne est cité');
  ok(T({ code: '23505', message: 'duplicate key' }).code === 'DUPLICATE_KEY', 'Doublon');
  ok(T({ code: '42501', message: 'new row violates row-level security policy' }).code === 'FORBIDDEN', 'RLS -> action non autorisée');
  ok(T(new TypeError('Failed to fetch')).code === 'NETWORK', 'Réseau coupé');
  ok(T({ message: 'JWT expired' }).code === 'SESSION_EXPIRED', 'Session expirée');
  ok(T({ message: 'boom' }).code === 'UNKNOWN', 'Erreur inconnue : message générique');
  const all = ['VERSION_CONFLICT', 'NO_ROWS_RIGHTS'].map((k) => T(null, { kind: k }).message);
  ok(all.every((m) => /^[A-ZÀ-Ü]/.test(m) && m.length > 30), 'Messages en français, phrases complètes');

  console.log('\n  Choix du pilote');
  const r = ED.resolveDriverName;
  const full = { dataDriver: 'supabase', supabaseUrl: 'https://x.supabase.co', supabaseAnonKey: 'k' };
  ok(r({}, '') === 'local', 'Sans configuration : démo locale (comportement actuel)');
  ok(r(full, '') === 'supabase', 'Configuration complète : Supabase');
  ok(r(full, '?demo=77') === 'local', '?demo=77 force le mode démo même en production');
  ok(r({ dataDriver: 'supabase', supabaseUrl: 'https://x' }, '') === 'local', 'Configuration incomplète : repli sur la démo');
}

unit();
console.log('\n  Contrat commun aux deux pilotes');
await contract(await setupLocal());
await contract(await setupSupabase());
console.log(`\n${passed} vérifications réussies, ${failed} en échec.`);
if (failed) { console.log(' - ' + fails.join('\n - ')); process.exit(1); }
