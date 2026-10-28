/*!
 * ECOPARK — Console d'administration CRUD (Phase 4, ADM-01 à ADM-08)
 * ---------------------------------------------------------------------------
 * Branchée exclusivement sur window.EcoparkData : fonctionne à l'identique en
 * mode démonstration (localStorage) et en production (Supabase + RLS).
 * Règles appliquées : brouillon par défaut, copie toujours en brouillon,
 * publication des tarifs réservée à la Direction, suppression = archivage dès
 * qu'une fiche a été publiée, annulation 8 s, verrou de version, échappement HTML.
 * Expose : window.EcoparkAdmin
 */
(function (root) {
  'use strict';

  var doc = root.document;
  var ED = function () { return root.EcoparkData; };
  var $ = function (id) { return doc.getElementById(id); };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var fcfa = function (n) {
    if (n === null || n === undefined || n === '') return 'Prix non affiché';
    return String(Math.round(Number(n))).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' FCFA';
  };
  var clone = function (v) { return v == null ? v : JSON.parse(JSON.stringify(v)); };
  var todayIso = function () {
    var d = new Date(Date.now() + 60 * 60 * 1000); // Yaoundé (UTC+1)
    return d.toISOString().slice(0, 10);
  };

  // ==========================================================================
  // 1. RÉFÉRENTIELS
  // ==========================================================================
  var ROLE_LABELS = {
    visiteur_anonyme: 'Visiteur anonyme',
    client_connecte: 'Client connecté',
    agent_guichet: 'Agent guichet (caisse)',
    agent_controle: 'Agent contrôle (scanner QR)',
    responsable_exploitation: "Responsable d'exploitation",
    direction: 'Direction',
    administrateur_plateforme: 'Administrateur plateforme'
  };
  var STAFF_ROLES = ['agent_guichet', 'agent_controle', 'responsable_exploitation', 'direction', 'administrateur_plateforme'];
  var POLES = {
    NATURE_FAUNE: 'Nature & Faune', EAU_PLEIN_AIR: 'Eau & Plein air', RESTAURATION: 'Restauration',
    HEBERGEMENT: 'Hébergement', GROUPES_B2B: 'Groupes & Navettes', FORMATION_CFP: 'Formation CFP', CULTURE_EDUCATION: 'Musée & Bibliothèque', FAMILLE_ENFANCE: 'Aire de Jeux & Crèche-Garderie'
  };
  var STATUS = {
    DRAFT: { label: 'Brouillon', cls: 'adm-badge-draft' },
    PUBLISHED: { label: 'En ligne', cls: 'adm-badge-live' },
    ARCHIVED: { label: 'Archivé', cls: 'adm-badge-archived' }
  };
  var WEEKDAYS = [['0', 'Dimanche'], ['1', 'Lundi'], ['2', 'Mardi'], ['3', 'Mercredi'], ['4', 'Jeudi'], ['5', 'Vendredi'], ['6', 'Samedi']];
  var ENTITY_LABEL = {
    catalog_activities: 'Activités', sales_bundles: 'Formules', lodge_cities: 'Cités hôtelières',
    agenda_events: 'Agenda', menu_items: 'Carte du restaurant', staff_profiles: 'Comptes équipe'
  };
  var TITLE_FIELD = { catalog_activities: 'title', sales_bundles: 'title', lodge_cities: 'name', agenda_events: 'title', menu_items: 'name', staff_profiles: 'full_name' };
  var OP_LABELS = {
    INSERT: 'Ajout', UPDATE: 'Modification', DUPLICATE: 'Duplication', PUBLISH: 'Publication', ARCHIVE: 'Archivage',
    DELETE: 'Suppression', RESTORE: 'Restauration', GUARD_REJECT: 'Garde-fou', EXPORT_CSV: 'Export CSV', GATEWAY_TEST: 'Test passerelle'
  };
  // Photothèque : photos déjà présentes sur le site (complétée par les images des fiches existantes)
  var PHOTO_LIBRARY = [
    ['audit-assets/ecopark-real-media/chimpanze.jpeg', 'Chimpanzé du jardin zoologique'],
    ['audit-assets/ecopark-real-media/balade_pirogue3.jpg', 'Balade en pirogue sur le lac'],
    ['audit-assets/ecopark-real-media/chambre.jpeg', 'Chambre des cités hôtelières'],
    ['audit-assets/ecopark-real-media/totem-services-ecopark.png', 'Totem officiel des 11 services ECOPARK'],
    ['audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg', 'Grand dimanche au bord du lac'],
    ['audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg', 'Groupe et événement en plein air'],
    ['audit-assets/ecopark-real-media/IMG_20260829_172016-1-scaled.jpg', 'Événement avec du public à ECOPARK'],
    ['audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png', 'Piscine et lac (illustration)'],
    ['audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png', 'Repas sous pergola (illustration)'],
    ['audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png', 'Famille sous la canopée (illustration)'],
    ['audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png', 'Apprenants du CFP (illustration)']
  ];
  var IMAGE_FIELDS = [
    { k: 'image_src', l: 'Image de la publication', t: 'image', wide: true },
    { k: 'image_alt', l: "Description de l'image (lue par les lecteurs d'écran)", t: 'text', wide: true, max: 180 }
  ];

  // Schémas de formulaire (modale universelle)
  var SCHEMAS = {
    catalog_activities: [
      { k: 'title', l: 'Intitulé affiché', t: 'text', req: true, wide: true },
      { k: 'slug', l: 'Adresse courte (slug)', t: 'text', req: true, pattern: /^[a-z0-9]+(?:[-_][a-z0-9]+)*$/, hint: 'minuscules, chiffres et tirets' },
      { k: 'sku', l: 'Code interne (SKU)', t: 'text', req: true },
      { k: 'pole', l: 'Pôle', t: 'select', req: true, opts: Object.keys(POLES).map(function (k) { return [k, POLES[k]]; }) },
      { k: 'daily_capacity', l: 'Capacité par jour', t: 'int', req: true },
      { k: 'description', l: 'Description', t: 'textarea', req: true, wide: true },
      { k: 'child_price_fcfa', l: 'Enfant (individuel)', t: 'fcfa', req: true, price: true },
      { k: 'adult_price_fcfa', l: 'Adulte (individuel)', t: 'fcfa', req: true, price: true },
      { k: 'group_adult_price_fcfa', l: 'Adulte (groupe dès 10)', t: 'fcfa', req: true, price: true },
      { k: 'group_child_price_fcfa', l: 'Enfant (groupe dès 10)', t: 'fcfa', req: true, price: true }
    ].concat(IMAGE_FIELDS),
    sales_bundles: [
      { k: 'title', l: 'Nom de la formule', t: 'text', req: true, wide: true },
      { k: 'subtitle', l: 'Contenu (sous-titre)', t: 'text', req: true, wide: true },
      { k: 'bundle_code', l: 'Code formule', t: 'text', req: true },
      { k: 'sku', l: 'Code interne (SKU)', t: 'text', req: true },
      { k: 'included_slugs', l: 'Activités incluses (slugs séparés par des virgules)', t: 'list', wide: true },
      { k: 'adult_bundle_price_fcfa', l: 'Prix adulte', t: 'fcfa', req: true, price: true },
      { k: 'child_bundle_price_fcfa', l: 'Prix enfant', t: 'fcfa', req: true, price: true },
      { k: 'savings_label', l: 'Argument affiché', t: 'text', req: true, wide: true },
      { k: 'is_featured', l: 'Mise en avant', t: 'check' }
    ].concat(IMAGE_FIELDS),
    lodge_cities: [
      { k: 'name', l: 'Nom de la cité', t: 'text', req: true, wide: true },
      { k: 'category', l: 'Catégorie', t: 'text', req: true },
      { k: 'code', l: 'Code (figé)', t: 'text', ro: true },
      { k: 'min_price_fcfa', l: 'Prix minimum / nuit', t: 'fcfa', req: true, price: true },
      { k: 'max_price_fcfa', l: 'Prix maximum / nuit', t: 'fcfa', req: true, price: true },
      { k: 'total_rooms', l: 'Nombre de chambres', t: 'int', req: true },
      { k: 'available_rooms', l: 'Chambres disponibles', t: 'int', req: true },
      { k: 'amenities', l: 'Équipements (séparés par des virgules)', t: 'list', wide: true }
    ].concat(IMAGE_FIELDS),
    agenda_events: [
      { k: 'title', l: 'Titre', t: 'text', req: true, wide: true },
      { k: 'short_label', l: 'Libellé court', t: 'text', req: true },
      { k: 'code', l: 'Code événement', t: 'text', req: true },
      { k: 'target_weekday', l: 'Jour', t: 'select', req: true, opts: WEEKDAYS, num: true },
      { k: 'day_filter', l: 'Filtre agenda', t: 'select', req: true, opts: [['MER_JEU', 'Mercredi & Jeudi'], ['VENDREDI', 'Vendredi'], ['SAMEDI', 'Samedi'], ['DIMANCHE', 'Dimanche'], ['LUNDI_FERIE', 'Lundi férié'], ['MARDI', 'Mardi']] },
      { k: 'badge', l: 'Badge horaire', t: 'text', req: true },
      { k: 'price_text', l: 'Texte tarif', t: 'text', wide: true },
      { k: 'from_price_fcfa', l: 'Prix « à partir de »', t: 'fcfa' },
      { k: 'spots_text', l: 'Disponibilités affichées', t: 'text', wide: true },
      { k: 'description', l: 'Description', t: 'textarea', wide: true },
      { k: 'schedule', l: 'Programme (une ligne par créneau)', t: 'lines', wide: true },
      { k: 'bundle_code', l: 'Formule associée', t: 'select', opts: [['PASS_DECOUVERTE', 'Pass Découverte'], ['PASS_ROYALE', 'Pass Journée Royale'], ['PACK_COUPLE_EWONDO', 'Pack Couple Ewondo'], ['CUSTOM', 'À la carte']] },
      { k: 'dish', l: 'Plat mis en avant', t: 'text' },
      { k: 'meal_slot', l: 'Service', t: 'select', opts: [['Service 12h30', '12h30'], ['Service 13h30', '13h30'], ['Service 15h00', '15h00']] },
      { k: 'pergola', l: 'Pergola proposée', t: 'check' },
      { k: 'nutrition', l: 'Sachet nutrition proposé', t: 'check' }
    ].concat(IMAGE_FIELDS),
    menu_items: [
      { k: 'name', l: 'Nom du plat', t: 'text', req: true, wide: true },
      { k: 'sku', l: 'Code interne (SKU)', t: 'text', req: true },
      { k: 'category', l: 'Catégorie', t: 'select', req: true, opts: [['ENTREE', 'Entrée'], ['PLAT', 'Plat'], ['GRILLADE', 'Grillade'], ['MENU_ENFANT', 'Menu enfant'], ['DESSERT', 'Dessert'], ['BOISSON', 'Boisson'], ['FORMULE', 'Formule']] },
      { k: 'price_fcfa', l: 'Prix (vide = non affiché)', t: 'fcfa' },
      { k: 'description', l: 'Description', t: 'textarea', wide: true },
      { k: 'is_signature', l: 'Spécialité maison', t: 'check' },
      { k: 'in_stock', l: 'Disponible aujourd\'hui', t: 'check' },
      { k: 'preorder_enabled', l: 'Proposé en précommande', t: 'check' }
    ].concat(IMAGE_FIELDS),
    staff_profiles: [
      { k: 'full_name', l: 'Nom et prénom', t: 'text', req: true, wide: true },
      { k: 'post_label', l: 'Poste', t: 'text', wide: true },
      { k: 'role', l: 'Rôle', t: 'select', req: true, opts: STAFF_ROLES.map(function (r) { return [r, ROLE_LABELS[r]]; }) }
    ]
  };
  var DEFAULTS = {
    catalog_activities: { pole: 'NATURE_FAUNE', daily_capacity: 200, child_price_fcfa: 500, adult_price_fcfa: 1000, group_adult_price_fcfa: 800, group_child_price_fcfa: 500 },
    sales_bundles: { included_slugs: [], adult_bundle_price_fcfa: 0, child_bundle_price_fcfa: 0, is_featured: false },
    agenda_events: { target_weekday: 6, day_filter: 'SAMEDI', schedule: [], bundle_code: 'CUSTOM', meal_slot: 'Service 12h30', pergola: false, nutrition: false },
    menu_items: { category: 'PLAT', in_stock: true, preorder_enabled: true, is_signature: false, price_fcfa: null },
    staff_profiles: { role: 'agent_guichet' }
  };
  var DEMO_STAFF = [
    { user_id: 'demo-dir', full_name: 'Dr Christophe FOÉ NDI', post_label: 'Promoteur — Direction générale', role: 'direction', is_active: true },
    { user_id: 'demo-gerant', full_name: 'M. Daryl MGBATOU', post_label: 'Gérant délégué', role: 'direction', is_active: true },
    { user_id: 'demo-exp', full_name: "Chef d'exploitation Ahala", post_label: 'Réception, Château des Saveurs & loges', role: 'responsable_exploitation', is_active: true },
    { user_id: 'demo-gui', full_name: 'Mme Clarisse ATANGANA', post_label: 'Caissière principale — Guichet #1 (RN3)', role: 'agent_guichet', is_active: true },
    { user_id: 'demo-ctl', full_name: 'Brigade contrôle portail', post_label: 'Scanner QR — Entrée principale', role: 'agent_controle', is_active: true },
    { user_id: 'demo-adm', full_name: 'Administrateur plateforme', post_label: 'Support technique ONOGRAPH', role: 'administrateur_plateforme', is_active: true }
  ];
  var DEMO_GATEWAYS = [
    { provider: 'ORANGE_MONEY', display_name: 'Orange Money WebPay Cameroun', mode: 'SANDBOX', status: 'UNKNOWN', key_last4: null, last_webhook_at: null },
    { provider: 'MTN_MOMO', display_name: 'MTN MoMo Collection API', mode: 'SANDBOX', status: 'UNKNOWN', key_last4: null, last_webhook_at: null },
    { provider: 'WHATSAPP_BUSINESS', display_name: 'Guichet unique WhatsApp Business', mode: 'SANDBOX', status: 'UNKNOWN', key_last4: null, last_webhook_at: null }
  ];

  // ==========================================================================
  // 2. ÉTAT DE LA CONSOLE
  // ==========================================================================
  var S = {
    tab: 'catalog_activities', q: '', pole: 'ALL', status: 'ACTIVE', highlight: null,
    role: 'direction', profileName: '', mfaOk: true,
    staff: [], gateways: [], quotas: [], availability: {}, quotaDate: todayIso(),
    audit: { rows: [], total: 0 }, auditPage: 0, auditOp: 'ALL', auditQ: '', pageSize: 25,
    editor: null, loaded: false, renderQueued: false
  };
  var isDemo = function () { return ED() && ED().driverName === 'local'; };
  var rules = function () { return ED().Rules; };
  var canEdit = function () { return rules().canEdit(S.role); };
  var canPublish = function (entity) { return rules().canPublish(entity, S.role); };
  var canDelete = function (entity) { return rules().canDelete(entity, S.role); };
  var isGovernance = function () { return S.role === 'direction' || S.role === 'administrateur_plateforme'; };

  // ==========================================================================
  // 3. NOTIFICATIONS, CONFIRMATIONS, ANNULATION
  // ==========================================================================
  function toast(msg, kind) {
    var el = $('admToast');
    if (!el) return;
    el.className = 'adm-toast show ' + (kind === 'error' ? 'adm-toast-error' : '');
    el.innerHTML = '<span>' + esc(msg) + '</span>';
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { el.className = 'adm-toast'; }, kind === 'error' ? 7000 : 4500);
  }
  function undoToast(msg, onUndo) {
    var el = $('admToast');
    if (!el) return;
    el.className = 'adm-toast show';
    el.innerHTML = '<span>' + esc(msg) + '</span><button type="button" class="adm-toast-undo" id="admUndoBtn">Annuler</button>';
    clearTimeout(toast._t);
    var done = false;
    $('admUndoBtn').onclick = function () {
      if (done) return;
      done = true;
      el.className = 'adm-toast';
      onUndo();
    };
    toast._t = setTimeout(function () { done = true; el.className = 'adm-toast'; }, 8000);
  }
  function confirmDialog(opts) {
    return new Promise(function (resolve) {
      var box = $('admConfirm');
      var actions = (opts.actions || []).map(function (a, i) {
        return '<button type="button" class="btn btn-sm ' + (a.primary ? 'btn-primary' : 'btn-secondary') + (a.danger ? ' adm-btn-danger' : '') +
          '" data-i="' + i + '">' + esc(a.label) + '</button>';
      }).join('');
      box.querySelector('.adm-confirm-card').innerHTML =
        '<h4>' + esc(opts.title) + '</h4><p>' + esc(opts.body) + '</p>' +
        '<div class="adm-modal-actions"><button type="button" class="btn btn-secondary btn-sm" data-i="-1">Retour</button>' + actions + '</div>';
      box.classList.add('open');
      box.querySelectorAll('button[data-i]').forEach(function (b) {
        b.onclick = function () {
          box.classList.remove('open');
          var i = Number(b.getAttribute('data-i'));
          resolve(i < 0 ? null : opts.actions[i].value);
        };
      });
    });
  }
  function report(res, okMsg) {
    if (res && res.ok) { if (okMsg) toast(okMsg); return true; }
    toast((res && res.error && res.error.message) || 'L\'opération n\'a pas abouti.', 'error');
    return false;
  }

  // ==========================================================================
  // 4. DONNÉES (lectures)
  // ==========================================================================
  function rowsOf(entity) {
    if (entity === 'staff_profiles') return S.staff;
    return ED().content(entity, { includeDrafts: true });
  }
  function findRow(entity, id) {
    var key = entity === 'staff_profiles' ? 'user_id' : 'id';
    return rowsOf(entity).filter(function (r) { return r[key] === id; })[0];
  }
  function demoSeed() {
    if (!isDemo()) return;
    var st = ED().store.state;
    st.content = st.content || {};
    if (!st.content.staff_profiles || !st.content.staff_profiles.length) st.content.staff_profiles = clone(DEMO_STAFF);
    if (!st.content.gateway_health || !st.content.gateway_health.length) st.content.gateway_health = clone(DEMO_GATEWAYS);
    if (!st.content.daily_quotas) st.content.daily_quotas = [];
    ED().store.persist();
  }
  function loadServerLists() {
    var d = ED();
    if (isDemo()) {
      demoSeed();
      var c = d.store.state.content || {};
      S.staff = clone(c.staff_profiles || []);
      S.gateways = clone(c.gateway_health || []);
      S.quotas = (c.daily_quotas || []).filter(function (q) { return q.quota_date === S.quotaDate; });
      S.availability = {};
      return Promise.resolve();
    }
    return Promise.all([
      d.list('staff_profiles'),
      d.list('gateway_health'),
      d.list('daily_quotas', { filters: { quota_date: S.quotaDate } }),
      d.rpc('get_availability', { p_date: S.quotaDate })
    ]).then(function (r) {
      S.staff = r[0].ok ? r[0].data : [];
      S.gateways = r[1].ok ? r[1].data : [];
      S.quotas = r[2].ok ? r[2].data : [];
      S.availability = {};
      (r[3].ok ? r[3].data : []).forEach(function (a) { S.availability[a.slug] = a; });
    });
  }
  function auditOpOf(log) {
    if (log.operation) return log.operation;
    var a = String(log.action || '').toUpperCase();
    if (a.indexOf('DUPLICATION') >= 0) return 'DUPLICATE';
    if (a.indexOf('SUPPRESSION') >= 0) return 'DELETE';
    if (a.indexOf('ARCHIV') >= 0) return 'ARCHIVE';
    if (a.indexOf('PUBLICATION') >= 0) return 'PUBLISH';
    if (a.indexOf('MODIFICATION') >= 0) return 'UPDATE';
    if (a.indexOf('AJOUT') >= 0 || a.indexOf('NOUVELLE') >= 0) return 'INSERT';
    return 'AUTRE';
  }
  function loadAudit() {
    var d = ED();
    var q = S.auditQ.toLowerCase();
    var matches = function (l) {
      return (S.auditOp === 'ALL' || auditOpOf(l) === S.auditOp) &&
        (!q || (String(l.actor) + ' ' + String(l.action)).toLowerCase().indexOf(q) >= 0);
    };
    if (isDemo()) {
      var all = (d.store.state.auditLogs || []).filter(matches);
      S.audit = { rows: all.slice(S.auditPage * S.pageSize, (S.auditPage + 1) * S.pageSize), total: all.length, all: all };
      return Promise.resolve();
    }
    var filters = S.auditOp === 'ALL' ? null : { operation: S.auditOp };
    return d.list('audit_logs', { order: 'seq', ascending: false, count: true, filters: filters,
      range: [S.auditPage * S.pageSize, (S.auditPage + 1) * S.pageSize - 1] }).then(function (r) {
      var map = d.Mappers.registry.audit_logs.fromRow;
      var rows = r.ok ? (r.data || []).map(map) : [];
      S.audit = { rows: q ? rows.filter(matches) : rows, total: r.ok ? (r.count || rows.length) : 0, error: r.ok ? null : r.error };
    });
  }

  // ==========================================================================
  // 5. RENDU
  // ==========================================================================
  function badge(status) {
    var s = STATUS[status] || { label: status || '?', cls: 'adm-badge-archived' };
    return '<span class="adm-badge ' + s.cls + '">' + esc(s.label) + '</span>';
  }
  function thumb(r) {
    return r && r.image_src
      ? '<img class="adm-thumb" src="' + esc(r.image_src) + '" alt="' + esc(r.image_alt || '') + '" loading="lazy" />'
      : '<span class="adm-thumb adm-thumb-missing">Sans image</span>';
  }
  function publishBlock(entity, r) {
    if (rules().needsImage(entity) && !rules().hasImage(r)) return 'Ajoutez une image avant de publier';
    if (!canPublish(entity)) return rules().isPriceEntity(entity) ? 'Publication des tarifs réservée à la Direction' : 'Rôle insuffisant';
    return '';
  }
  function btn(label, action, attrs, cls) {
    return '<button type="button" class="adm-act ' + (cls || '') + '" data-act="' + action + '" ' + (attrs || '') + '>' + esc(label) + '</button>';
  }
  function disabledAttr(cond, why) { return cond ? '' : 'disabled title="' + esc(why) + '"'; }

  function renderRoleBar() {
    var el = $('admRoleBar');
    if (!el) return;
    var right;
    if (isDemo()) {
      right = '<label class="adm-inline"><span>Rôle simulé (démo)</span><select class="form-control" id="admDemoRole">' +
        ['direction', 'administrateur_plateforme', 'responsable_exploitation', 'agent_guichet'].map(function (r) {
          return '<option value="' + r + '"' + (r === S.role ? ' selected' : '') + '>' + esc(ROLE_LABELS[r]) + '</option>';
        }).join('') + '</select></label>';
    } else {
      right = '<span class="adm-who">' + esc(S.profileName || 'Session') + ' — ' + esc(ROLE_LABELS[S.role] || S.role) +
        (S.mfaOk ? '' : ' <span class="adm-badge adm-badge-error">Double authentification requise</span>') + '</span>';
    }
    var mode = isDemo()
      ? '<span class="adm-badge adm-badge-draft">Mode démonstration — données de ce navigateur uniquement</span>'
      : '<span class="adm-badge adm-badge-live">Connecté à la base ECOPARK</span>';
    var rights = canEdit()
      ? (S.role === 'direction' ? 'Vous pouvez préparer, publier et archiver les tarifs.'
        : S.role === 'administrateur_plateforme' ? 'Vous préparez et archivez ; la publication des tarifs revient à la Direction.'
          : 'Vous préparez les brouillons et publiez agenda et carte ; les tarifs sont publiés par la Direction.')
      : 'Consultation seule : votre rôle ne permet pas de modifier le contenu.';
    el.innerHTML = '<div class="adm-rolebar-left">' + mode + '<span class="adm-rights">' + esc(rights) + '</span></div><div>' + right + '</div>';
    var sel = $('admDemoRole');
    if (sel) sel.onchange = function () {
      S.role = sel.value;
      ED().driver.role = sel.value;
      render();
      toast('Rôle simulé : ' + ROLE_LABELS[sel.value]);
    };
  }

  function priceCell(entity, r) {
    if (entity === 'catalog_activities') {
      return '<div class="adm-prices">' +
        '<span>Enfant <b>' + esc(fcfa(r.child_price_fcfa)) + '</b></span><span>Adulte <b>' + esc(fcfa(r.adult_price_fcfa)) + '</b></span>' +
        '<span>Groupe adulte <b>' + esc(fcfa(r.group_adult_price_fcfa)) + '</b></span>' +
        '<span>Groupe enfant <b>' + esc(fcfa(r.group_child_price_fcfa)) + '</b> <em>(plafond ' + esc(fcfa(r.child_price_fcfa)) + ')</em></span></div>';
    }
    if (entity === 'sales_bundles') {
      return '<div class="adm-prices"><span>Adulte <b>' + esc(fcfa(r.adult_bundle_price_fcfa)) + '</b></span><span>Enfant <b>' +
        esc(fcfa(r.child_bundle_price_fcfa)) + '</b></span><span>Inclus : ' + esc((r.included_slugs || []).join(', ') || '—') + '</span></div>';
    }
    return '<div class="adm-prices"><span>De <b>' + esc(fcfa(r.min_price_fcfa)) + '</b> à <b>' + esc(fcfa(r.max_price_fcfa)) + '</b> / nuit</span></div>';
  }
  function capacityCell(entity, r) {
    if (entity === 'catalog_activities') return esc(r.daily_capacity) + ' places / jour';
    if (entity === 'lodge_cities') return esc(r.available_rooms) + ' libres sur ' + esc(r.total_rooms);
    return r.is_featured ? 'Mise en avant' : '—';
  }
  function lifecycleActions(entity, r, opts) {
    opts = opts || {};
    var id = esc(r.id);
    var a = [btn('Modifier', 'edit', 'data-entity="' + entity + '" data-id="' + id + '"' + (canEdit() ? '' : ' disabled title="Consultation seule"'))];
    if (opts.duplicable !== false) a.push(btn('Dupliquer', 'duplicate', 'data-entity="' + entity + '" data-id="' + id + '" ' + disabledAttr(canEdit(), 'Consultation seule'), 'adm-act-dup'));
    if (r.status !== 'PUBLISHED') {
      var why = publishBlock(entity, r);
      a.push(btn('Publier', 'publish', 'data-entity="' + entity + '" data-id="' + id + '" ' + disabledAttr(!why, why), 'adm-act-pub'));
    }
    if (r.status === 'ARCHIVED') {
      a.push(btn('Remettre en brouillon', 'restore', 'data-entity="' + entity + '" data-id="' + id + '" ' + disabledAttr(canEdit(), 'Consultation seule')));
    } else {
      var hard = r.status === 'DRAFT' && !r.first_published_at;
      a.push(btn(hard ? 'Supprimer' : 'Archiver', 'delete', 'data-entity="' + entity + '" data-id="' + id + '" ' +
        disabledAttr(canDelete(entity), 'Réservé à la Direction / Administrateur'), 'adm-act-del'));
    }
    return '<div class="adm-actions">' + a.join('') + '</div>';
  }

  function renderCatalog() {
    var wrap = $('admCatalogBody');
    if (!wrap) return;
    var entity = S.tab;
    var all = rowsOf(entity);
    var q = S.q.trim().toLowerCase();
    var rows = all.filter(function (r) {
      if (S.status === 'ACTIVE' && r.status === 'ARCHIVED') return false;
      if (['DRAFT', 'PUBLISHED', 'ARCHIVED'].indexOf(S.status) >= 0 && r.status !== S.status) return false;
      if (entity === 'catalog_activities' && S.pole !== 'ALL' && r.pole !== S.pole) return false;
      if (!q) return true;
      return [r.title, r.name, r.sku, r.slug, r.code, r.bundle_code, r.description, r.subtitle].join(' ').toLowerCase().indexOf(q) >= 0;
    });
    var count = function (st) { return all.filter(function (r) { return r.status === st; }).length; };
    var noImg = all.filter(function (r) { return r.status !== 'ARCHIVED' && !rules().hasImage(r); }).length;
    $('admCatalogKpis').innerHTML =
      '<span class="adm-kpi"><b>' + count('PUBLISHED') + '</b> en ligne</span><span class="adm-kpi"><b>' + count('DRAFT') +
      '</b> brouillon(s)</span><span class="adm-kpi"><b>' + count('ARCHIVED') + '</b> archivée(s)</span>' +
      (noImg ? '<span class="adm-kpi adm-kpi-warn"><b>' + noImg + '</b> sans image (publication bloquée)</span>' : '');
    $('admPoleFilter').style.display = entity === 'catalog_activities' ? '' : 'none';
    $('admAddOffer').disabled = !canEdit() || entity === 'lodge_cities';
    $('admAddOffer').title = entity === 'lodge_cities' ? 'Les cités hôtelières ne se créent pas depuis la console (codes figés)' : '';
    document.querySelectorAll('#admCatalogTabs [data-tab]').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-tab') === entity);
    });
    if (!rows.length) {
      wrap.innerHTML = '<tr><td colspan="5" class="adm-empty">Aucune fiche ne correspond à ces filtres.</td></tr>';
      return;
    }
    wrap.innerHTML = rows.map(function (r) {
      var t = r[TITLE_FIELD[entity]];
      var origin = r.duplicated_from ? findRow(entity, r.duplicated_from) : null;
      return '<tr class="' + (S.highlight === r.id ? 'adm-row-new' : '') + (r.status === 'ARCHIVED' ? ' adm-row-archived' : '') + '" data-row-id="' + esc(r.id) + '">' +
        '<td class="adm-col-offer"><div class="adm-offer-cell">' + thumb(r) + '<div><strong>' + esc(t) + '</strong><div class="adm-sub">' + esc(r.sku || r.code || '') +
        (entity === 'catalog_activities' ? ' · ' + esc(POLES[r.pole] || r.pole) : '') + '</div>' +
        (origin ? '<div class="adm-sub adm-origin">Version de travail de « ' + esc(origin[TITLE_FIELD[entity]]) + ' »</div>' : '') + '</div></div></td>' +
        '<td>' + priceCell(entity, r) + '</td><td>' + capacityCell(entity, r) + '</td><td>' + badge(r.status) + '</td>' +
        '<td>' + lifecycleActions(entity, r, { duplicable: entity !== 'lodge_cities' }) + '</td></tr>';
    }).join('');
  }

  function renderCms() {
    ['agenda_events', 'menu_items'].forEach(function (entity) {
      var box = $(entity === 'agenda_events' ? 'admAgendaList' : 'admMenuList');
      if (!box) return;
      var rows = rowsOf(entity).filter(function (r) { return r.status !== 'ARCHIVED' || S.status === 'ARCHIVED'; });
      if (!rows.length) { box.innerHTML = '<p class="adm-empty">Aucun élément.</p>'; return; }
      box.innerHTML = rows.map(function (r, i) {
        var t = entity === 'agenda_events' ? (r.short_label || r.title) : r[TITLE_FIELD[entity]];
        var meta = entity === 'agenda_events'
          ? esc(r.badge) + ' · ' + esc(r.price_text || '') + '<br/>Titre complet : ' + esc(r.title)
          : esc(fcfa(r.price_fcfa)) + (r.is_signature ? ' · Spécialité' : '') + (r.in_stock ? '' : ' · <b class="adm-out">En rupture</b>');
        var extra = entity === 'menu_items'
          ? btn(r.in_stock ? 'Marquer en rupture' : 'Remettre en stock', 'stock', 'data-id="' + esc(r.id) + '" ' + disabledAttr(canEdit(), 'Consultation seule'))
          : '';
        return '<div class="adm-cms-row' + (S.highlight === r.id ? ' adm-row-new' : '') + '">' +
          '<div class="adm-cms-main adm-offer-cell">' + thumb(r) + '<div><strong>' + esc(t) + '</strong> ' + badge(r.status) + '<div class="adm-sub">' + meta + '</div></div></div>' +
          '<div class="adm-actions">' +
          btn('Monter', 'move', 'data-entity="' + entity + '" data-id="' + esc(r.id) + '" data-dir="-1" ' + disabledAttr(canEdit() && i > 0, 'Déjà en tête')) +
          btn('Descendre', 'move', 'data-entity="' + entity + '" data-id="' + esc(r.id) + '" data-dir="1" ' + disabledAttr(canEdit() && i < rows.length - 1, 'Déjà en dernier')) +
          extra + '</div>' + lifecycleActions(entity, r) + '</div>';
      }).join('');
    });
  }

  function renderQuotas() {
    var body = $('admQuotaBody');
    if (!body) return;
    $('admQuotaDate').value = S.quotaDate;
    var acts = ED().content('catalog_activities');
    body.innerHTML = acts.map(function (a) {
      var q = S.quotas.filter(function (x) { return x.activity_id === a.id; })[0];
      var av = S.availability[a.slug];
      var cap = q ? q.capacity : a.daily_capacity;
      return '<tr><td class="adm-col-offer"><strong>' + esc(a.title) + '</strong></td><td>' + esc(a.daily_capacity) + '</td>' +
        '<td><input type="number" min="0" step="1" class="form-control adm-quota-input" data-activity="' + esc(a.id) + '" value="' + (q ? esc(q.capacity) : '') +
        '" placeholder="Standard" ' + (canEdit() ? '' : 'disabled') + ' /></td>' +
        '<td>' + (av ? esc(av.booked) + ' réservées · <b>' + esc(av.remaining) + '</b> restantes' : esc(cap) + ' places') + '</td>' +
        '<td><div class="adm-actions">' + btn('Enregistrer', 'quota-save', 'data-activity="' + esc(a.id) + '" ' + disabledAttr(canEdit(), 'Consultation seule')) +
        (q ? btn('Standard', 'quota-reset', 'data-activity="' + esc(a.id) + '" title="Revenir à la capacité standard" ' + disabledAttr(canEdit(), 'Consultation seule')) : '') + '</div></td></tr>';
    }).join('');

    var wb = ED().setting('weather_banner') || { presets: {}, active_preset: '' };
    var sel = $('admWeatherPreset');
    sel.innerHTML = Object.keys(wb.presets || {}).map(function (k) {
      return '<option value="' + esc(k) + '"' + (k === wb.active_preset ? ' selected' : '') + '>' + esc(wb.presets[k]) + '</option>';
    }).join('');
    sel.disabled = !canEdit();
    $('admWeatherCustom').value = wb.custom_message || '';
    $('admWeatherCustom').disabled = !canEdit();
    $('admWeatherSave').disabled = !canEdit();
    updateWeatherPreview();
  }
  function updateWeatherPreview() {
    var wb = ED().setting('weather_banner') || { presets: {} };
    var custom = $('admWeatherCustom').value.trim();
    $('admWeatherPreview').textContent = custom || (wb.presets || {})[$('admWeatherPreset').value] || '';
  }

  function renderStaff() {
    var body = $('admStaffBody');
    if (!body) return;
    var admin = S.role === 'administrateur_plateforme' || (isDemo() && isGovernance());
    var inviteOk = admin && isDemo();
    $('admStaffAdd').disabled = !inviteOk;
    $('admStaffAdd').title = isDemo() ? '' : "L'invitation par e-mail s'active avec Supabase Auth (Phase 2).";
    body.innerHTML = S.staff.map(function (u) {
      var id = esc(u.user_id);
      return '<tr><td class="adm-col-offer"><strong>' + esc(u.full_name) + '</strong><div class="adm-sub">' + esc(u.post_label || '') + '</div></td>' +
        '<td>' + esc(ROLE_LABELS[u.role] || u.role) + '</td>' +
        '<td>' + (u.is_active ? '<span class="adm-badge adm-badge-live">Actif</span>' : '<span class="adm-badge adm-badge-error">Suspendu</span>') + '</td>' +
        '<td><div class="adm-actions">' +
        btn('Modifier', 'staff-edit', 'data-id="' + id + '" ' + disabledAttr(admin, "Réservé à l'administrateur")) +
        btn('Dupliquer le poste', 'staff-dup', 'data-id="' + id + '" ' + disabledAttr(inviteOk, isDemo() ? "Réservé à l'administrateur" : "Disponible avec Supabase Auth (Phase 2)"), 'adm-act-dup') +
        btn(u.is_active ? 'Suspendre' : 'Réactiver', 'staff-toggle', 'data-id="' + id + '" ' + disabledAttr(admin, "Réservé à l'administrateur"), u.is_active ? 'adm-act-del' : 'adm-act-pub') +
        '</div></td></tr>';
    }).join('') || '<tr><td colspan="4" class="adm-empty">Aucun compte visible avec votre rôle.</td></tr>';
  }

  function renderGateways() {
    var box = $('admGatewayList');
    if (!box) return;
    var modeLabel = { OFF: 'Désactivée', SANDBOX: 'Mode test', LIVE: 'Production' };
    var stLabel = { UNKNOWN: ['Jamais testée', 'adm-badge-archived'], OK: ['Opérationnelle', 'adm-badge-live'], DEGRADED: ['Dégradée', 'adm-badge-draft'], DOWN: ['Hors service', 'adm-badge-error'] };
    box.innerHTML = S.gateways.map(function (g) {
      var st = stLabel[g.status] || stLabel.UNKNOWN;
      return '<div class="adm-gw"><div><strong>' + esc(g.display_name) + '</strong><div class="adm-sub">' + esc(modeLabel[g.mode] || g.mode) +
        ' · Clé : ' + (g.key_last4 ? '•••• ' + esc(g.key_last4) : 'non configurée') +
        ' · Dernier webhook : ' + (g.last_webhook_at ? esc(ED().Mappers.tsToFr(g.last_webhook_at)) : 'aucun') + '</div></div>' +
        '<div class="adm-actions"><span class="adm-badge ' + st[1] + '">' + st[0] + '</span>' +
        btn('Tester', 'gw-test', 'data-id="' + esc(g.provider) + '" ' + disabledAttr(isGovernance(), 'Réservé à la Direction / Administrateur')) + '</div></div>';
    }).join('') || '<p class="adm-empty">Passerelles visibles par la Direction et l\'administrateur uniquement.</p>';
  }

  var TABLE_LABELS = {
    catalog_activities: 'Activité', sales_bundles: 'Formule', lodge_cities: 'Cité hôtelière', agenda_events: 'Agenda',
    menu_items: 'Carte', site_settings: 'Réglage du site', staff_profiles: 'Compte équipe', daily_quotas: 'Jauge du jour',
    gateway_health: 'Passerelle', audit_logs: 'Journal', bookings: 'Réservation', group_quotes: 'Devis',
    cfp_applications: 'Candidature CFP', appointments: 'Rendez-vous', weather_banner: 'bandeau météo'
  };
  /** Rend lisible une ligne du journal : noms de tables et codes techniques traduits */
  function humanizeAudit(text) {
    var s = String(text == null ? '' : text).replace(/^(GUARD_REJECT|EXPORT_CSV|GATEWAY_TEST|PRINT_REPORT|LOGIN|LOGOUT)\s+—\s+/, '');
    return s.replace(/\b(catalog_activities|sales_bundles|lodge_cities|agenda_events|menu_items|site_settings|staff_profiles|daily_quotas|gateway_health|audit_logs|bookings|group_quotes|cfp_applications|appointments|weather_banner)\b/g,
      function (m) { return TABLE_LABELS[m] || m; });
  }

  function renderAudit() {
    var body = $('admAuditBody');
    if (!body) return;
    var pages = Math.max(1, Math.ceil((S.audit.total || 0) / S.pageSize));
    $('admAuditOp').value = S.auditOp;
    $('admAuditCount').textContent = (S.audit.total || 0) + ' événement(s) · page ' + (S.auditPage + 1) + ' / ' + pages;
    $('admAuditPrev').disabled = S.auditPage <= 0;
    $('admAuditNext').disabled = S.auditPage >= pages - 1;
    body.innerHTML = S.audit.rows.map(function (l) {
      var op = auditOpOf(l);
      return '<tr><td class="adm-nowrap">' + esc(l.time) + '</td><td><span class="adm-op adm-op-' + esc(op.toLowerCase()) + '">' + esc(OP_LABELS[op] || op) +
        '</span></td><td><strong>' + esc(humanizeAudit(l.actor)) + '</strong></td><td>' + esc(humanizeAudit(l.action)) + '</td></tr>';
    }).join('') || '<tr><td colspan="4" class="adm-empty">' + esc(S.audit.error ? S.audit.error.message : 'Aucun événement pour ce filtre.') + '</td></tr>';
  }

  function render() {
    if (!ED() || !ED().store || !$('admCatalogBody')) return;
    renderRoleBar();
    renderCatalog();
    renderCms();
    renderQuotas();
    renderStaff();
    renderGateways();
    renderAudit();
  }
  function scheduleRender(reloadAudit) {
    if (S.renderQueued) return;
    S.renderQueued = true;
    var run = function () {
      S.renderQueued = false;
      var p = reloadAudit ? loadAudit() : Promise.resolve();
      if (isDemo()) loadServerLists();
      p.then(render);
    };
    if (root.requestAnimationFrame) root.requestAnimationFrame(run); else setTimeout(run, 0);
  }

  // ==========================================================================
  // 6. MODALE UNIVERSELLE (Ajouter / Modifier)
  // ==========================================================================
  function fieldValue(f, el) {
    if (f.t === 'check') return !!el.checked;
    if (f.t === 'image') return el.value.trim() || null;
    var v = el.value;
    if (f.t === 'fcfa' || f.t === 'int') {
      if (String(v).trim() === '') return null;
      return Number(v);
    }
    if (f.num) return Number(v);
    if (f.t === 'list') return v.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (f.t === 'lines') return v.split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
    return v.trim();
  }
  function displayValue(f, v) {
    if (f.t === 'image') return v ? (String(v).indexOf('data:') === 0 ? 'photo téléversée' : String(v).split('/').pop()) : '(aucune)';
    if (f.t === 'check') return v ? 'oui' : 'non';
    if (f.t === 'fcfa') return fcfa(v);
    if (f.t === 'select') {
      var o = (f.opts || []).filter(function (x) { return String(x[0]) === String(v); })[0];
      return o ? o[1] : String(v);
    }
    if (Array.isArray(v)) return v.join(f.t === 'lines' ? ' / ' : ', ') || '(vide)';
    return v === null || v === undefined || v === '' ? '(vide)' : String(v);
  }
  function openEditor(entity, row, opts) {
    opts = opts || {};
    var schema = SCHEMAS[entity];
    var base = row ? clone(row) : Object.assign({}, clone(DEFAULTS[entity] || {}), opts.prefill || {});
    var lockPrices = row && rules().isPriceEntity(entity) && row.status === 'PUBLISHED' && S.role !== 'direction';
    S.editor = { entity: entity, row: row, base: base, lockPrices: lockPrices, mode: row ? 'edit' : 'create' };
    var form = schema.map(function (f) {
      var v = base[f.k];
      var id = 'admF_' + f.k;
      var dis = f.ro || (f.price && lockPrices) || !canEdit() ? ' disabled' : '';
      var input;
      if (f.t === 'textarea' || f.t === 'lines') {
        input = '<textarea class="form-control" id="' + id + '" rows="' + (f.t === 'lines' ? 4 : 3) + '"' + dis + '>' +
          esc(Array.isArray(v) ? v.join('\n') : (v == null ? '' : v)) + '</textarea>';
      } else if (f.t === 'select') {
        input = '<select class="form-control" id="' + id + '"' + dis + '>' + f.opts.map(function (o) {
          return '<option value="' + esc(o[0]) + '"' + (String(o[0]) === String(v) ? ' selected' : '') + '>' + esc(o[1]) + '</option>';
        }).join('') + '</select>';
      } else if (f.t === 'check') {
        input = '<label class="adm-check"><input type="checkbox" id="' + id + '"' + (v ? ' checked' : '') + dis + ' /> <span>' + esc(f.l) + '</span></label>';
      } else if (f.t === 'image') {
        input = '<div class="adm-image-field">' +
          '<input type="hidden" id="' + id + '" value="' + esc(v || '') + '" />' +
          '<div class="adm-image-preview" id="admImgPreview">' + imagePreview(v) + '</div>' +
          '<div class="adm-image-actions">' +
          '<button type="button" class="adm-act" id="admImgLibBtn"' + dis + '>Choisir dans la photothèque</button>' +
          '<label class="adm-act adm-act-dup adm-upload' + (dis ? ' adm-disabled' : '') + '">Téléverser une photo' +
          '<input type="file" id="admImgFile" accept="image/jpeg,image/png,image/webp"' + dis + ' /></label>' +
          '<button type="button" class="adm-act adm-act-del" id="admImgRemove"' + dis + '>Retirer</button></div>' +
          '<div class="adm-sub">JPEG, PNG ou WebP. La photo est optimisée automatiquement (1 600 px maximum). <b>Obligatoire pour publier.</b></div>' +
          '<div class="adm-image-library" id="admImgLibrary" hidden></div></div>';
      } else {
        var type = f.t === 'fcfa' || f.t === 'int' ? 'number' : 'text';
        input = '<input type="' + type + '" class="form-control" id="' + id + '"' + (type === 'number' ? ' min="0" step="1"' : '') +
          ' value="' + esc(Array.isArray(v) ? v.join(', ') : (v == null ? '' : v)) + '"' + dis + ' />';
      }
      return '<div class="adm-field' + (f.wide ? ' adm-field-wide' : '') + '">' +
        (f.t === 'check' ? '' : '<label class="form-label" for="' + id + '">' + esc(f.l) + (f.req ? ' *' : '') + '</label>') + input +
        '<div class="adm-field-err" id="' + id + '_err"></div></div>';
    }).join('');

    var title = row ? 'Modifier — ' + (row[TITLE_FIELD[entity]] || '') : 'Ajouter — ' + ENTITY_LABEL[entity];
    var footerLeft = '';
    if (row && entity !== 'staff_profiles') {
      footerLeft = (entity !== 'lodge_cities' ? '<button type="button" class="btn btn-secondary btn-sm" id="admEdDup"' + (canEdit() ? '' : ' disabled') + '>Dupliquer cette fiche</button>' : '') +
        (row.status !== 'PUBLISHED' ? '<button type="button" class="btn btn-secondary btn-sm" id="admEdPub"' +
          (publishBlock(entity, row) ? ' disabled title="' + esc(publishBlock(entity, row)) + '"' : '') + '>Publier</button>' : '');
    }
    $('admEditorCard').innerHTML =
      '<div class="adm-modal-head"><div><span class="adm-eyebrow">' + esc(ENTITY_LABEL[entity]) + '</span><h4>' + esc(title) + '</h4></div>' +
      (row && row.status ? badge(row.status) : '<span class="adm-badge adm-badge-draft">Sera créé en brouillon</span>') + '</div>' +
      (lockPrices ? '<div class="adm-note">Ce tarif est en ligne : les prix sont verrouillés. Utilisez « Dupliquer cette fiche » pour préparer un nouveau tarif, que la Direction publiera.</div>' : '') +
      (entity === 'staff_profiles' && !row ? '<div class="adm-note">Démonstration : le compte est créé localement. En production, un e-mail d\'invitation sera envoyé (Supabase Auth, Phase 2).</div>' : '') +
      '<div class="adm-form">' + form + '</div>' +
      '<div class="adm-diff" id="admEdDiff"></div><div class="adm-field-err" id="admEdError"></div>' +
      '<div class="adm-modal-actions"><div>' + footerLeft + '</div><div>' +
      '<button type="button" class="btn btn-secondary btn-sm" id="admEdCancel">Annuler</button>' +
      '<button type="button" class="btn btn-primary btn-sm" id="admEdSave">' + (row ? 'Enregistrer' : 'Créer le brouillon') + '</button></div></div>';
    $('admEditor').classList.add('open');
    schema.forEach(function (f) {
      var el = $('admF_' + f.k);
      if (el) el.addEventListener(f.t === 'check' || f.t === 'select' ? 'change' : 'input', validateEditor);
    });
    $('admEdCancel').onclick = closeEditor;
    $('admEdSave').onclick = saveEditor;
    if ($('admImgLibBtn')) bindImageField(entity);
    if ($('admEdDup')) $('admEdDup').onclick = function () { closeEditor(); duplicate(entity, row.id); };
    if ($('admEdPub')) $('admEdPub').onclick = function () { closeEditor(); publish(entity, row.id); };
    validateEditor();
    var first = $('admEditorCard').querySelector('input:not([disabled]),textarea:not([disabled]),select:not([disabled])');
    if (first) first.focus();
  }
  // --- Champ image : aperçu, photothèque, téléversement optimisé -------------
  function imagePreview(src) {
    return src
      ? '<img src="' + esc(src) + '" alt="Aperçu de l\'image de la publication" />'
      : '<span class="adm-image-empty">Aucune image : la fiche peut être enregistrée en brouillon, mais pas publiée.</span>';
  }
  function setImage(src, altSuggestion) {
    var input = $('admF_image_src');
    if (!input) return;
    input.value = src || '';
    $('admImgPreview').innerHTML = imagePreview(src);
    var alt = $('admF_image_alt');
    if (alt && src && !alt.value.trim() && altSuggestion) alt.value = altSuggestion.slice(0, 180);
    if (alt && !src) alt.value = '';
    validateEditor();
  }
  function libraryImages() {
    var seen = {};
    var out = [];
    PHOTO_LIBRARY.forEach(function (p) { if (!seen[p[0]]) { seen[p[0]] = 1; out.push(p); } });
    ['catalog_activities', 'sales_bundles', 'lodge_cities', 'agenda_events', 'menu_items'].forEach(function (e) {
      rowsOf(e).forEach(function (r) {
        if (r.image_src && !seen[r.image_src]) { seen[r.image_src] = 1; out.push([r.image_src, r.image_alt || r[TITLE_FIELD[e]] || '']); }
      });
    });
    return out;
  }
  function canvasToBlob(canvas, type, quality) {
    return new Promise(function (resolve) { canvas.toBlob(resolve, type, quality); });
  }
  /** Redimensionne (1600 px max) et recompresse ; réduit encore si la limite de poids n'est pas tenue */
  function compressImage(file, maxBytes) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () { resolve(img); };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('Image illisible : le fichier est peut-être endommagé.')); };
      img.src = url;
    }).then(function (img) {
      var probe = doc.createElement('canvas');
      var type = probe.toDataURL('image/webp').indexOf('data:image/webp') === 0 ? 'image/webp' : 'image/jpeg';
      var steps = [[1600, 0.82], [1280, 0.78], [1024, 0.72], [800, 0.68], [640, 0.62]];
      var attempt = function (i) {
        var s = steps[i];
        var ratio = Math.min(1, s[0] / Math.max(img.naturalWidth, img.naturalHeight));
        var c = doc.createElement('canvas');
        c.width = Math.max(1, Math.round(img.naturalWidth * ratio));
        c.height = Math.max(1, Math.round(img.naturalHeight * ratio));
        var ctx = c.getContext('2d');
        if (type === 'image/jpeg') { ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, c.width, c.height); }
        ctx.drawImage(img, 0, 0, c.width, c.height);
        return canvasToBlob(c, type, s[1]).then(function (blob) {
          if (!blob) throw new Error('Optimisation impossible dans ce navigateur.');
          if (blob.size <= maxBytes || i === steps.length - 1) return blob;
          return attempt(i + 1);
        });
      };
      return attempt(0).then(function (blob) { URL.revokeObjectURL(img.src); return blob; });
    });
  }
  function processImageFile(file, entity) {
    var err = $('admF_image_src_err');
    err.textContent = '';
    if (!file) return;
    if (['image/jpeg', 'image/png', 'image/webp'].indexOf(file.type) < 0) {
      err.textContent = 'Format non accepté : choisissez une photo JPEG, PNG ou WebP.';
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      err.textContent = 'Fichier trop volumineux (15 Mo maximum avant optimisation).';
      return;
    }
    $('admImgPreview').innerHTML = '<span class="adm-image-empty">Optimisation et envoi de la photo…</span>';
    $('admEdSave').disabled = true;
    var limit = isDemo() ? 420 * 1024 : 1500 * 1024;
    compressImage(file, limit).then(function (blob) {
      return ED().uploadImage(blob, { entity: entity });
    }).then(function (res) {
      if (!res.ok) { err.textContent = res.error.message; setImage($('admF_image_src').value); return; }
      var titleEl = $('admF_title') || $('admF_name');
      setImage(res.data.url, titleEl ? titleEl.value.trim() : '');
      toast(isDemo() ? 'Photo ajoutée (mode démonstration : conservée dans ce navigateur).' : 'Photo téléversée.');
    }).catch(function (e) {
      err.textContent = e.message || 'La photo n\'a pas pu être traitée.';
      setImage($('admF_image_src').value);
    });
  }
  function bindImageField(entity) {
    $('admImgLibBtn').onclick = function () {
      var lib = $('admImgLibrary');
      if (!lib.hidden) { lib.hidden = true; return; }
      lib.innerHTML = libraryImages().map(function (p, i) {
        return '<button type="button" class="adm-lib-item" data-lib="' + i + '"><img src="' + esc(p[0]) + '" alt="" loading="lazy" /><span>' + esc(p[1]) + '</span></button>';
      }).join('');
      var items = libraryImages();
      lib.querySelectorAll('[data-lib]').forEach(function (b) {
        b.onclick = function () {
          var p = items[Number(b.getAttribute('data-lib'))];
          setImage(p[0], p[1]);
          lib.hidden = true;
        };
      });
      lib.hidden = false;
    };
    $('admImgFile').onchange = function (e) { processImageFile(e.target.files && e.target.files[0], entity); e.target.value = ''; };
    $('admImgRemove').onclick = function () { setImage(''); };
  }

  function closeEditor() { $('admEditor').classList.remove('open'); S.editor = null; }
  function collectEditor() {
    var ed = S.editor;
    var values = {};
    var errors = {};
    SCHEMAS[ed.entity].forEach(function (f) {
      var el = $('admF_' + f.k);
      if (!el || f.ro) return;
      var v = fieldValue(f, el);
      values[f.k] = v;
      if (f.req && (v === null || v === '' || (Array.isArray(v) && !v.length && f.t !== 'list'))) errors[f.k] = 'Champ obligatoire';
      else if ((f.t === 'fcfa' || f.t === 'int') && v !== null && (!isFinite(v) || v < 0 || Math.floor(v) !== v)) errors[f.k] = 'Nombre entier positif (FCFA sans centimes)';
      else if (f.pattern && v && !f.pattern.test(v)) errors[f.k] = 'Format attendu : ' + f.hint;
      else if (f.max && v && String(v).length > f.max) errors[f.k] = f.max + ' caractères maximum';
      else if (f.t === 'image' && v && !rules().safeImageSrc(v)) errors[f.k] = 'Source d\'image non autorisée';
    });
    if (ed.row && ed.row.status === 'PUBLISHED' && rules().needsImage(ed.entity) && 'image_src' in values && !values.image_src) {
      errors.image_src = 'Une fiche en ligne doit garder une image (remplacez-la plutôt que de la retirer).';
    }
    if (ed.entity === 'catalog_activities' && values.group_child_price_fcfa != null && values.child_price_fcfa != null &&
        values.group_child_price_fcfa > values.child_price_fcfa) {
      errors.group_child_price_fcfa = 'Garde-fou : ne peut pas dépasser le tarif enfant individuel (' + fcfa(values.child_price_fcfa) + ')';
    }
    if (ed.entity === 'lodge_cities') {
      if (values.max_price_fcfa < values.min_price_fcfa) errors.max_price_fcfa = 'Doit être supérieur ou égal au prix minimum';
      if (values.available_rooms > values.total_rooms) errors.available_rooms = 'Ne peut pas dépasser le nombre de chambres';
    }
    var patch = {};
    var diff = [];
    SCHEMAS[ed.entity].forEach(function (f) {
      if (!(f.k in values)) return;
      if (ed.mode === 'create' || JSON.stringify(values[f.k]) !== JSON.stringify(ed.base[f.k] === undefined ? null : ed.base[f.k])) {
        patch[f.k] = values[f.k];
        if (ed.mode === 'edit') diff.push(f.l + ' : ' + displayValue(f, ed.base[f.k]) + ' → ' + displayValue(f, values[f.k]));
      }
    });
    return { values: values, errors: errors, patch: patch, diff: diff };
  }
  function validateEditor() {
    if (!S.editor) return;
    var c = collectEditor();
    SCHEMAS[S.editor.entity].forEach(function (f) {
      var e = $('admF_' + f.k + '_err');
      if (e) e.textContent = c.errors[f.k] || '';
      var el = $('admF_' + f.k);
      if (el) el.classList.toggle('adm-invalid', !!c.errors[f.k]);
    });
    var nErr = Object.keys(c.errors).length;
    $('admEdDiff').innerHTML = S.editor.mode === 'edit'
      ? (c.diff.length ? '<b>' + c.diff.length + ' modification(s) :</b><ul>' + c.diff.map(function (d) { return '<li>' + esc(d) + '</li>'; }).join('') + '</ul>' : 'Aucune modification pour l\'instant.')
      : '';
    $('admEdSave').disabled = !canEdit() || nErr > 0 || (S.editor.mode === 'edit' && !c.diff.length);
  }
  function saveEditor() {
    var ed = S.editor;
    var c = collectEditor();
    if (Object.keys(c.errors).length) return;
    var btnSave = $('admEdSave');
    btnSave.disabled = true;
    btnSave.textContent = 'Enregistrement…';
    var p;
    if (ed.entity === 'staff_profiles') {
      p = ed.mode === 'edit'
        ? ED().update('staff_profiles', ed.row.user_id, c.patch)
        : ED().create('staff_profiles', Object.assign({ user_id: 'demo-' + Date.now().toString(36), is_active: true }, c.values));
    } else if (ed.mode === 'edit') {
      p = ED().update(ed.entity, ed.row.id, c.patch, ed.row.version);
    } else {
      p = ED().create(ed.entity, Object.assign({}, c.values, { status: 'DRAFT' }));
    }
    p.then(function (res) {
      if (!res.ok) {
        $('admEdError').textContent = res.error.message;
        btnSave.disabled = false;
        btnSave.textContent = ed.mode === 'edit' ? 'Enregistrer' : 'Créer le brouillon';
        if (res.error.code === 'CHILD_PRICE_GUARD') {
          ED().logEvent('GUARD_REJECT', ed.entity, ed.row ? ed.row.id : null, 'Saisie refusée : ' + res.error.message);
        }
        return;
      }
      closeEditor();
      if (res.data && res.data.id) S.highlight = res.data.id;
      toast(ed.mode === 'edit' ? 'Modifications enregistrées.' : 'Brouillon créé. Il reste invisible du public jusqu\'à sa publication.');
      refreshAfterWrite(ed.entity);
    });
  }
  function refreshAfterWrite(entity) {
    if (entity === 'staff_profiles' || entity === 'daily_quotas' || entity === 'gateway_health') {
      loadServerLists().then(function () { return loadAudit(); }).then(render);
    } else {
      loadAudit().then(render);
    }
  }

  // ==========================================================================
  // 7. ACTIONS DU CYCLE DE VIE
  // ==========================================================================
  function duplicate(entity, id) {
    ED().duplicate(entity, id).then(function (res) {
      if (!report(res)) return;
      S.highlight = res.data;
      if (S.status === 'PUBLISHED' || S.status === 'ARCHIVED') S.status = 'ACTIVE';
      loadAudit().then(function () {
        render();
        var row = findRow(entity, res.data);
        toast('Copie créée en brouillon : ajustez-la puis publiez-la.');
        if (row) openEditor(entity, row);
      });
    });
  }
  function publish(entity, id) {
    var row = findRow(entity, id);
    if (!row) return;
    var origin = row.duplicated_from ? findRow(entity, row.duplicated_from) : null;
    var stillCopy = /\(Copie\)\s*$/.test(String(row[TITLE_FIELD[entity]] || '')) || /\(Copie\)\s*$/.test(String(row.short_label || ''));
    var copyHint = stillCopy ? ' Attention : si vous la publiez comme nouvelle offre, son titre se termine encore par « (Copie) » ; renommez-la d\'abord.' : '';
    var step = origin && origin.status === 'PUBLISHED'
      ? confirmDialog({
        title: 'Publier cette version ?',
        body: 'Cette fiche est une version de travail de « ' + origin[TITLE_FIELD[entity]] + ' ». La remplacer conserve la même adresse sur le site et les réservations existantes.' + copyHint,
        actions: [{ label: 'Publier comme nouvelle offre', value: 'NEW' }, { label: "Remplacer l'offre en ligne", value: 'REPLACE', primary: true }]
      })
      : confirmDialog({
        title: 'Publier « ' + row[TITLE_FIELD[entity]] + ' » ?',
        body: 'La fiche sera visible immédiatement par tous les visiteurs du site.',
        actions: [{ label: 'Publier', value: 'NEW', primary: true }]
      });
    step.then(function (choice) {
      if (!choice) return;
      ED().setStatus(entity, id, 'PUBLISHED', choice === 'REPLACE').then(function (res) {
        if (!report(res, choice === 'REPLACE' ? 'Nouvelle version en ligne. L\'ancienne est conservée dans l\'historique.' : 'Fiche publiée.')) return;
        S.highlight = res.data;
        refreshAfterWrite(entity);
      });
    });
  }
  function removeFlow(entity, id) {
    var row = findRow(entity, id);
    if (!row) return;
    var hard = row.status === 'DRAFT' && !row.first_published_at;
    var name = row[TITLE_FIELD[entity]];
    confirmDialog({
      title: hard ? 'Supprimer ce brouillon ?' : 'Archiver « ' + name + ' » ?',
      body: hard
        ? 'Ce brouillon n\'a jamais été publié : il sera supprimé définitivement (annulation possible pendant 8 secondes).'
        : 'La fiche disparaîtra du site mais restera dans l\'historique (ventes, journal). Vous pourrez la remettre en brouillon.',
      actions: [{ label: hard ? 'Supprimer' : 'Archiver', value: true, primary: true, danger: true }]
    }).then(function (yes) {
      if (!yes) return;
      var snapshot = clone(row);
      ED().remove(entity, id).then(function (res) {
        if (!report(res)) return;
        refreshAfterWrite(entity);
        undoToast(res.data === 'DELETED' ? '« ' + name + ' » supprimé.' : '« ' + name + ' » archivé.', function () {
          var undo = res.data === 'DELETED'
            ? ED().create(entity, (function () {
              var s = clone(snapshot);
              delete s.version; delete s.updated_at; delete s.updated_by; delete s.first_published_at;
              s.status = 'DRAFT';
              return s;
            })())
            : ED().setStatus(entity, id, snapshot.status === 'PUBLISHED' ? 'PUBLISHED' : 'DRAFT');
          undo.then(function (r) { if (report(r, 'Action annulée.')) refreshAfterWrite(entity); });
        });
      });
    });
  }
  function restore(entity, id) {
    ED().setStatus(entity, id, 'DRAFT').then(function (res) {
      if (report(res, 'Fiche remise en brouillon.')) { S.highlight = id; refreshAfterWrite(entity); }
    });
  }
  function move(entity, id, dir) {
    var rows = rowsOf(entity).filter(function (r) { return r.status !== 'ARCHIVED'; });
    var i = rows.findIndex(function (r) { return r.id === id; });
    var j = i + dir;
    if (i < 0 || j < 0 || j >= rows.length) return;
    var a = rows[i];
    var b = rows[j];
    var sa = a.sort_order === b.sort_order ? a.sort_order + dir : b.sort_order;
    var sb = a.sort_order === b.sort_order ? b.sort_order : a.sort_order;
    ED().update(entity, a.id, { sort_order: sa }, a.version).then(function (r1) {
      if (!report(r1)) return;
      var fresh = findRow(entity, b.id);
      ED().update(entity, b.id, { sort_order: sb }, fresh ? fresh.version : b.version).then(function (r2) {
        if (report(r2, 'Ordre mis à jour.')) refreshAfterWrite(entity);
      });
    });
  }
  function toggleStock(id) {
    var r = findRow('menu_items', id);
    if (!r) return;
    ED().update('menu_items', id, { in_stock: !r.in_stock }, r.version).then(function (res) {
      if (report(res, r.in_stock ? '« ' + r.name + ' » marqué en rupture.' : '« ' + r.name + ' » de nouveau disponible.')) refreshAfterWrite('menu_items');
    });
  }
  function saveQuota(activityId, reset) {
    var input = doc.querySelector('.adm-quota-input[data-activity="' + activityId + '"]');
    var existing = S.quotas.filter(function (q) { return q.activity_id === activityId; })[0];
    var raw = input ? input.value.trim() : '';
    var p;
    if (reset || raw === '') {
      if (!existing) { toast('Capacité standard déjà appliquée.'); return; }
      p = ED().removeRow('daily_quotas', existing.id);
    } else {
      var cap = Number(raw);
      if (!isFinite(cap) || cap < 0 || Math.floor(cap) !== cap) { toast('Capacité : nombre entier positif.', 'error'); return; }
      p = existing
        ? ED().update('daily_quotas', existing.id, { capacity: cap }, existing.version)
        : ED().create('daily_quotas', { activity_id: activityId, quota_date: S.quotaDate, capacity: cap, reason: 'Ajustement console ADM-03' });
    }
    p.then(function (res) { if (report(res, 'Jauge du ' + ED().Mappers.isoToFr(S.quotaDate) + ' enregistrée.')) refreshAfterWrite('daily_quotas'); });
  }
  function saveWeather() {
    var wb = clone(ED().setting('weather_banner') || { presets: {} });
    wb.active_preset = $('admWeatherPreset').value;
    wb.custom_message = $('admWeatherCustom').value.trim() || null;
    ED().saveSetting('weather_banner', wb).then(function (res) {
      if (report(res, 'Bandeau publié sur le site.')) {
        if (typeof root.renderWeatherBannerFromData === 'function') root.renderWeatherBannerFromData();
        loadAudit().then(render);
      }
    });
  }
  function staffToggle(id) {
    var u = S.staff.filter(function (x) { return x.user_id === id; })[0];
    if (!u) return;
    confirmDialog({
      title: (u.is_active ? 'Suspendre ' : 'Réactiver ') + u.full_name + ' ?',
      body: u.is_active ? 'Le compte perd immédiatement ses droits sur la base. (La coupure des sessions ouvertes arrive avec Supabase Auth, Phase 2.)' : 'Le compte retrouve les droits de son rôle.',
      actions: [{ label: u.is_active ? 'Suspendre' : 'Réactiver', value: true, primary: true, danger: u.is_active }]
    }).then(function (yes) {
      if (!yes) return;
      ED().update('staff_profiles', id, { is_active: !u.is_active }).then(function (res) {
        if (report(res, u.is_active ? 'Compte suspendu.' : 'Compte réactivé.')) refreshAfterWrite('staff_profiles');
      });
    });
  }
  function exportCsv() {
    var rows = isDemo() ? (S.audit.all || S.audit.rows) : S.audit.rows;
    var csvEsc = function (v) { return '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"'; };
    var lines = [['Horodatage', 'Opération', 'Acteur', 'Action'].map(csvEsc).join(';')].concat(rows.map(function (l) {
      var op = auditOpOf(l);
      return [l.time, OP_LABELS[op] || op, humanizeAudit(l.actor), humanizeAudit(l.action)].map(csvEsc).join(';');
    }));
    try {
      var blob = new Blob(['\ufeff' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
      var a = doc.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'journal-audit-ecopark-' + todayIso() + '.csv';
      doc.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) { /* navigateur sans Blob : on journalise quand même */ }
    ED().logEvent('EXPORT_CSV', 'audit_logs', null, 'Export CSV du journal (' + rows.length + ' lignes)').then(function () { loadAudit().then(render); });
    toast(rows.length + ' ligne(s) exportée(s).');
    return rows.length;
  }
  function verifyChain() {
    ED().rpc('verify_audit_chain').then(function (res) {
      var el = $('admChainResult');
      if (!res.ok) { el.className = 'adm-note'; el.textContent = res.error.message; return; }
      var r = (res.data || [])[0] || {};
      el.className = r.is_valid ? 'adm-note adm-note-ok' : 'adm-note adm-note-error';
      el.textContent = r.is_valid
        ? 'Chaîne intègre : ' + r.checked_rows + ' entrées vérifiées, aucune altération.'
        : 'ALERTE : altération détectée à l\'entrée n°' + r.first_broken_seq + '.';
    });
  }

  // ==========================================================================
  // 8. BRANCHEMENT DES ÉVÉNEMENTS (délégation)
  // ==========================================================================
  function bind() {
    var view = $('view-ADM');
    if (!view || view._admBound) return;
    view._admBound = true;
    view.addEventListener('click', function (e) {
      var b = e.target.closest('[data-act]');
      if (!b || b.disabled) return;
      var act = b.getAttribute('data-act');
      var entity = b.getAttribute('data-entity');
      var id = b.getAttribute('data-id');
      if (act === 'edit') openEditor(entity, findRow(entity, id));
      else if (act === 'duplicate') duplicate(entity, id);
      else if (act === 'publish') publish(entity, id);
      else if (act === 'delete') removeFlow(entity, id);
      else if (act === 'restore') restore(entity, id);
      else if (act === 'move') move(entity, id, Number(b.getAttribute('data-dir')));
      else if (act === 'stock') toggleStock(id);
      else if (act === 'quota-save') saveQuota(b.getAttribute('data-activity'), false);
      else if (act === 'quota-reset') saveQuota(b.getAttribute('data-activity'), true);
      else if (act === 'staff-edit') openEditor('staff_profiles', S.staff.filter(function (u) { return u.user_id === id; })[0]);
      else if (act === 'staff-dup') {
        var src = S.staff.filter(function (u) { return u.user_id === id; })[0];
        openEditor('staff_profiles', null, { prefill: { role: src.role, post_label: src.post_label, full_name: '' } });
      } else if (act === 'staff-toggle') staffToggle(id);
      else if (act === 'gw-test') {
        ED().logEvent('GATEWAY_TEST', 'gateway_health', id, 'Test manuel de la passerelle ' + id).then(function (res) {
          if (report(res, 'Test enregistré dans le journal. Le test réel de connexion arrive avec les Edge Functions (Phase 7).')) loadAudit().then(render);
        });
      }
    });
    document.querySelectorAll('#admCatalogTabs [data-tab]').forEach(function (b) {
      b.onclick = function () { S.tab = b.getAttribute('data-tab'); S.highlight = null; renderCatalog(); };
    });
    $('admCatalogSearch').addEventListener('input', function (e) { S.q = e.target.value; renderCatalog(); });
    $('admPoleFilter').addEventListener('change', function (e) { S.pole = e.target.value; renderCatalog(); });
    $('admStatusFilter').addEventListener('change', function (e) { S.status = e.target.value; renderCatalog(); renderCms(); });
    $('admAddOffer').onclick = function () { openEditor(S.tab, null); };
    $('admAddAgenda').onclick = function () { openEditor('agenda_events', null); };
    $('admAddMenu').onclick = function () { openEditor('menu_items', null); };
    $('admStaffAdd').onclick = function () { openEditor('staff_profiles', null); };
    $('admQuotaDate').addEventListener('change', function (e) {
      S.quotaDate = e.target.value || todayIso();
      loadServerLists().then(render);
    });
    $('admWeatherPreset').addEventListener('change', updateWeatherPreview);
    $('admWeatherCustom').addEventListener('input', updateWeatherPreview);
    $('admWeatherSave').onclick = saveWeather;
    $('admAuditOp').addEventListener('change', function (e) { S.auditOp = e.target.value; S.auditPage = 0; loadAudit().then(renderAudit); });
    $('admAuditSearch').addEventListener('input', function (e) { S.auditQ = e.target.value; S.auditPage = 0; loadAudit().then(renderAudit); });
    $('admAuditPrev').onclick = function () { S.auditPage = Math.max(0, S.auditPage - 1); loadAudit().then(renderAudit); };
    $('admAuditNext').onclick = function () { S.auditPage += 1; loadAudit().then(renderAudit); };
    $('admAuditExport').onclick = exportCsv;
    $('admAuditVerify').onclick = verifyChain;
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && $('admEditor').classList.contains('open')) closeEditor();
    });
  }

  // ==========================================================================
  // 9. API PUBLIQUE
  // ==========================================================================
  var EcoparkAdmin = {
    /** Appelé à l'ouverture de la vue /admin */
    open: function () {
      if (!ED() || !ED().store || !$('admCatalogBody')) return Promise.resolve();
      bind();
      return ED().ready().then(function () { return ED().session(); }).then(function (r) {
        if (r && r.ok && r.data) {
          S.role = isDemo() ? (ED().driver.role || 'direction') : (r.data.role || 'visiteur_anonyme');
          S.profileName = r.data.full_name || '';
          S.mfaOk = r.data.mfa_satisfied !== false;
        }
        return loadServerLists();
      }).then(loadAudit).then(function () { S.loaded = true; render(); });
    },
    /** Appelé quand le magasin change (temps réel, retour arrière, onglet voisin) */
    onDataChanged: function () {
      var view = $('view-ADM');
      if (!S.loaded || !view || !view.classList.contains('active')) return;
      scheduleRender(true);
    },
    render: render,
    state: S,
    _test: { openEditor: openEditor, duplicate: duplicate, publish: publish, removeFlow: removeFlow, exportCsv: exportCsv }
  };
  root.EcoparkAdmin = EcoparkAdmin;
})(typeof window !== 'undefined' ? window : globalThis);
