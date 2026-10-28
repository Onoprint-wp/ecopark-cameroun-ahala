/*!
 * ECOPARK — Couche d'accès aux données (Phase 3)
 * ---------------------------------------------------------------------------
 * Un « magasin » local lu de façon synchrone par les écrans existants (loadDB),
 * alimenté par l'un des deux pilotes interchangeables :
 *   - LocalDemoDriver : localStorage (mode démo, comportement historique)
 *   - SupabaseDriver  : supabase-js + Realtime (production)
 *
 * Aucune dépendance. Compatible navigateur et Node (tests via vm).
 * Expose : window.EcoparkData
 */
(function (root) {
  'use strict';

  // ==========================================================================
  // 0. OUTILS
  // ==========================================================================
  var clone = function (v) { return v === undefined ? undefined : JSON.parse(JSON.stringify(v)); };
  var has = function (o, k) { return Object.prototype.hasOwnProperty.call(o, k); };
  var noop = function () {};

  function safeStorage() {
    try {
      var s = root.localStorage;
      var k = '__ecopark_probe__';
      s.setItem(k, '1');
      s.removeItem(k);
      return s;
    } catch (e) {
      var mem = {};
      return {
        getItem: function (k) { return has(mem, k) ? mem[k] : null; },
        setItem: function (k, v) { mem[k] = String(v); },
        removeItem: function (k) { delete mem[k]; }
      };
    }
  }

  // ==========================================================================
  // 1. CONVERTISSEURS (format base <-> format historique du site)
  // ==========================================================================
  var Mappers = {};

  /** '2026-11-15' -> '15/11/2026' (les valeurs déjà au format JJ/MM/AAAA sont conservées) */
  Mappers.isoToFr = function (iso) {
    if (!iso) return '';
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso));
    return m ? m[3] + '/' + m[2] + '/' + m[1] : String(iso);
  };
  /** '15/11/2026' ou '2026-11-15' -> '2026-11-15' ; null si invalide */
  Mappers.frToIso = function (fr) {
    if (!fr) return null;
    var s = String(fr).trim();
    var iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
    if (iso) return s;
    var m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(s);
    if (!m) return null;
    var d = ('0' + m[1]).slice(-2);
    var mo = ('0' + m[2]).slice(-2);
    return m[3] + '-' + mo + '-' + d;
  };
  /** '2026-10-26T08:45:00Z' -> '26/10/2026 09:45' (heure de Yaoundé, UTC+1) */
  Mappers.tsToFr = function (ts) {
    if (!ts) return '';
    var d = new Date(ts);
    if (isNaN(d.getTime())) return String(ts);
    var local = new Date(d.getTime() + 60 * 60 * 1000); // Africa/Douala = UTC+1, sans heure d'été
    var p = function (n) { return ('0' + n).slice(-2); };
    return p(local.getUTCDate()) + '/' + p(local.getUTCMonth() + 1) + '/' + local.getUTCFullYear() +
      ' ' + p(local.getUTCHours()) + ':' + p(local.getUTCMinutes());
  };
  Mappers.toFcfa = function (v) {
    var n = typeof v === 'number' ? v : parseInt(String(v == null ? '' : v).replace(/[^0-9-]/g, ''), 10);
    if (!isFinite(n) || n < 0) return 0;
    return Math.round(n);
  };

  function invert(map) {
    var out = {};
    Object.keys(map).forEach(function (k) { out[map[k]] = k; });
    return out;
  }

  // --- Devis groupes ---------------------------------------------------------
  var QUOTE_STATUS = { EN_ETUDE: 'Proforma générée', PROFORMA_ENVOYEE: 'Proposition envoyée', VALIDE: 'Validé', ANNULE: 'Annulé' };
  var QUOTE_STATUS_INV = Object.assign(invert(QUOTE_STATUS), { 'En étude': 'EN_ETUDE' });
  function quoteGroupType(label) {
    var t = String(label || '');
    if (/S[ée]minaire|Entreprise|ONG|Minist/i.test(t)) return 'entreprise';
    if (/Mariage|R[ée]ception|R[ée]union|Gala/i.test(t)) return 'mariage_evenement';
    return 'ecole';
  }
  var GROUP_TYPE_LABEL = { ecole: 'Excursion scolaire', entreprise: 'Séminaire & Conférence', mariage_evenement: 'Mariage / Réception' };

  // --- Candidatures CFP ------------------------------------------------------
  var CFP_STATUS = {
    DOSSIER_RECU: 'Dossier reçu (Inscription 50 000 FCFA)',
    INSCRIPTION_REGLEE: 'Inscription réglée (50 000 FCFA)',
    ADMIS: 'Admis Rentrée (50 000 FCFA réglés)'
  };
  var CFP_STATUS_INV = invert(CFP_STATUS);

  // --- Rendez-vous -----------------------------------------------------------
  var RDV_STATUS = { CONFIRME: 'RDV Confirmé', HONORE: 'RDV Honoré', REPORTE: 'RDV Reporté', ANNULE: 'RDV Annulé' };
  var RDV_MODE = { SUR_SITE: 'Sur site (Ahala Barrière)', WHATSAPP_APPEL: 'Appel WhatsApp' };

  // --- Réservations ----------------------------------------------------------
  // Statut historique du site <-> (payment_state, cancelled_at, rescheduled)
  function bookingLegacyStatus(row) {
    if (row.cancelled_at) return 'CANCELLED';
    if (row.rescheduled_from_date) return 'REPORTED';
    if (row.payment_state === 'PENDING') return 'HELD_11H';
    if (row.payment_state === 'CONFIRMED') return 'CONFIRMED';
    return row.payment_state || 'CONFIRMED';
  }

  /**
   * Registre des entités : table, clé primaire, lecture publique, temps réel,
   * clé de stockage dans le format historique (legacyKey) et convertisseurs.
   */
  var Registry = {
    catalog_activities: { key: 'id', publicRead: true, realtime: 'public', content: true, priceGoverned: true, order: 'sort_order' },
    sales_bundles:      { key: 'id', publicRead: true, realtime: 'public', content: true, priceGoverned: true, order: 'sort_order' },
    lodge_cities:       { key: 'id', publicRead: true, realtime: 'public', content: true, priceGoverned: true, order: 'sort_order' },
    agenda_events:      { key: 'id', publicRead: true, realtime: 'public', content: true, order: 'sort_order' },
    menu_items:         { key: 'id', publicRead: true, realtime: 'public', content: true, order: 'sort_order' },
    site_settings:      { key: 'key', publicRead: true, realtime: 'public', content: true, order: 'key' },
    group_quotes: {
      key: 'id', publicInsert: true, realtime: 'staff', legacyKey: 'quotes', legacyId: 'reference',
      fromRow: function (r) {
        return {
          reference: r.quote_reference,
          org: r.organization_name,
          contact: r.contact_name,
          phone: r.contact_phone,
          type: r.notes || GROUP_TYPE_LABEL[r.group_type] || r.group_type,
          pax: r.participants_count,
          date: Mappers.isoToFr(r.preferred_date),
          budgetFcfa: r.estimated_budget_fcfa,
          status: QUOTE_STATUS[r.status] || r.status,
          _id: r.id
        };
      },
      toRow: function (q) {
        var type = String(q.type || '');
        return {
          quote_reference: q.reference,
          organization_name: q.org,
          contact_name: q.contact || q.org,
          contact_phone: q.phone,
          group_type: quoteGroupType(type),
          preferred_date: Mappers.frToIso(q.date),
          participants_count: Math.max(10, parseInt(q.pax, 10) || 10),
          hall_menkii_included: /Menkii/i.test(type),
          shuttle_included: /Navette/i.test(type),
          estimated_budget_fcfa: Mappers.toFcfa(q.budgetFcfa),
          notes: type || null,
          status: QUOTE_STATUS_INV[q.status] || 'EN_ETUDE'
        };
      }
    },
    cfp_applications: {
      key: 'id', publicInsert: true, realtime: 'staff', legacyKey: 'cfpApplications', legacyId: 'reference',
      fromRow: function (r) {
        var plan = r.payment_plan === 'INTEGRAL' ? 'Paiement intégral (300 000 FCFA)' : 'Échéancier 4 tranches (100k + 3x50k FCFA)';
        return {
          reference: r.application_ref,
          name: r.candidate_name + ' (' + r.candidate_age + ' ans)',
          track: r.program_track + ' • ' + plan,
          phone: r.candidate_phone,
          status: CFP_STATUS[r.status] || r.status,
          _id: r.id
        };
      },
      toRow: function (a) {
        var nm = /^(.*?)\s*\((\d+)\s*ans\)\s*$/.exec(String(a.name || ''));
        var parts = String(a.track || '').split(' • ');
        return {
          application_ref: a.reference,
          candidate_name: nm ? nm[1] : String(a.name || ''),
          candidate_age: nm ? parseInt(nm[2], 10) : (parseInt(a.age, 10) || 19),
          candidate_phone: a.phone,
          program_track: parts[0] || 'Hôtellerie',
          payment_plan: /int[ée]gral/i.test(parts[1] || '') ? 'INTEGRAL' : '4_TRANCHES',
          status: CFP_STATUS_INV[a.status] || 'DOSSIER_RECU'
        };
      }
    },
    appointments: {
      key: 'id', publicInsert: true, realtime: 'staff', legacyKey: 'appointments', legacyId: 'reference',
      fromRow: function (r) {
        return {
          reference: r.appointment_ref,
          visitorName: r.visitor_name,
          org: r.organization_name || '',
          phone: r.visitor_phone,
          purposeCode: r.purpose_code,
          purposeLabel: r.purpose_label,
          date: Mappers.isoToFr(r.appointment_date),
          slot: r.time_slot,
          mode: RDV_MODE[r.meeting_mode] || r.meeting_mode,
          status: (RDV_STATUS[r.status] || r.status) + ' (' + r.time_slot + ')',
          _id: r.id
        };
      },
      toRow: function (a) {
        var st = String(a.status || '');
        var status = /Annul/i.test(st) ? 'ANNULE' : /Report/i.test(st) ? 'REPORTE' : /Honor/i.test(st) ? 'HONORE' : 'CONFIRME';
        return {
          appointment_ref: a.reference,
          visitor_name: a.visitorName,
          visitor_phone: a.phone,
          organization_name: a.org || null,
          purpose_code: a.purposeCode,
          purpose_label: a.purposeLabel,
          appointment_date: Mappers.frToIso(a.date),
          time_slot: a.slot,
          meeting_mode: /WhatsApp|Appel/i.test(String(a.mode || '')) ? 'WHATSAPP_APPEL' : 'SUR_SITE',
          status: status
        };
      }
    },
    bookings: {
      key: 'id', realtime: 'staff', legacyKey: 'bookings', legacyId: 'reference',
      fromRow: function (r) {
        var acts = (r.selected_bundle_code ? [r.selected_bundle_code] : []).concat(r.selected_activities || []);
        return {
          reference: r.reference_code,
          holder: r.visitor_name,
          phone: r.visitor_phone,
          date: Mappers.isoToFr(r.visit_date),
          paxSummary: r.adults_count + ' Adulte(s), ' + r.children_count + ' Enfant(s) • ' + (acts.join(' + ') || 'Visite'),
          totalFcfa: r.total_fcfa,
          payMethod: r.payment_method,
          lodgeCity: r.lodge_city || null,
          hasPergola: !!(r.has_pergola || r.pergola_reserved),
          status: bookingLegacyStatus(r),
          scanned: r.qr_status === 'USED' || !!r.scanned_at,
          scannedAt: r.scanned_at ? Mappers.tsToFr(r.scanned_at) : null,
          _id: r.id
        };
      },
      toRow: function (b) {
        var pax = /(\d+)\s*Adulte[^,]*,\s*(\d+)\s*Enfant/i.exec(String(b.paxSummary || ''));
        return {
          reference_code: b.reference,
          visitor_name: b.holder,
          visitor_phone: b.phone,
          visit_date: Mappers.frToIso(b.date),
          adults_count: pax ? parseInt(pax[1], 10) : 1,
          children_count: pax ? parseInt(pax[2], 10) : 0,
          total_fcfa: Mappers.toFcfa(b.totalFcfa),
          payment_method: b.payMethod || 'OM',
          payment_state: b.status === 'HELD_11H' ? 'PENDING' : 'CONFIRMED',
          lodge_city: b.lodgeCity || null,
          has_pergola: !!b.hasPergola
        };
      }
    },
    audit_logs: {
      key: 'id', realtime: 'governance', legacyKey: 'auditLogs', readOnly: true, order: 'seq',
      fromRow: function (r) {
        return {
          time: Mappers.tsToFr(r.created_at),
          actor: r.actor_name + (r.actor_role ? ' (' + r.actor_role + ')' : ''),
          action: r.description,
          operation: r.operation,
          seq: r.seq,
          _id: r.id
        };
      }
    },
    staff_profiles: { key: 'user_id', realtime: 'governance', order: 'full_name' },
    daily_quotas: { key: 'id', realtime: 'staff', order: 'quota_date' },
    gateway_health: { key: 'provider', realtime: 'governance', order: 'provider' }
  };
  Mappers.registry = Registry;

  // ==========================================================================
  // 2. ERREURS — traduction en français
  // ==========================================================================
  var Errors = {};
  Errors.make = function (code, message, hint, raw) {
    return { code: code, message: message, hint: hint || '', raw: raw || null };
  };
  /**
   * @param err  erreur PostgREST / Supabase ({code, message, hint, details}) ou Error
   * @param ctx  {entity, row, kind: 'NO_ROWS_RIGHTS' | 'VERSION_CONFLICT' | 'NETWORK'}
   */
  Errors.translate = function (err, ctx) {
    ctx = ctx || {};
    if (ctx.kind === 'VERSION_CONFLICT') {
      return Errors.make('VERSION_CONFLICT', 'Cette fiche vient d\'être modifiée par quelqu\'un d\'autre. Rechargez-la avant d\'enregistrer.');
    }
    if (ctx.kind === 'NO_ROWS_RIGHTS') {
      return Errors.make('NO_RIGHTS', 'Rien n\'a été enregistré : votre rôle ne permet pas de modifier cette fiche, ou votre double authentification a expiré.');
    }
    var msg = String((err && (err.message || err.error_description)) || err || '');
    var code = String((err && err.code) || '');
    var full = msg + ' ' + String((err && err.details) || '') + ' ' + String((err && err.hint) || '');
    var row = ctx.row || {};

    if (ctx.kind === 'NETWORK' || /Failed to fetch|NetworkError|network|ECONNREFUSED|timeout/i.test(msg)) {
      return Errors.make('NETWORK', 'Connexion perdue : rien n\'a été enregistré. Vérifiez le réseau puis réessayez.', '', err);
    }
    if (/JWT expired|invalid JWT|PGRST301|PGRST303/i.test(full)) {
      return Errors.make('SESSION_EXPIRED', 'Votre session a expiré. Reconnectez-vous pour continuer.', '', err);
    }
    if (/ECOPARK_IMAGE_REQUIRED/.test(full)) {
      return Errors.make('IMAGE_REQUIRED', 'Ajoutez une image à cette fiche avant de la publier.', '', err);
    }
    if (/mime type|invalid_mime_type/i.test(full)) {
      return Errors.make('IMAGE_TYPE', 'Format non accepté : choisissez une photo JPEG, PNG ou WebP.', '', err);
    }
    if (/too large|exceeded the maximum allowed size|Payload too large/i.test(full)) {
      return Errors.make('IMAGE_TOO_LARGE', 'Image trop lourde (5 Mo maximum).', '', err);
    }
    if (/_image_src_safe/.test(full)) {
      return Errors.make('IMAGE_SOURCE', 'Cette image ne provient pas d\'une source autorisée (photothèque du site ou téléversement).', '', err);
    }
    if (/ECOPARK_PUBLISH_REQUIRES_DIRECTION/.test(full)) {
      return Errors.make('PUBLISH_REQUIRES_DIRECTION', 'Seule la Direction peut publier ou retirer un tarif en ligne. Votre brouillon est enregistré.', '', err);
    }
    if (/ECOPARK_PUBLISHED_PRICE_LOCKED/.test(full)) {
      return Errors.make('PUBLISHED_PRICE_LOCKED', 'Ce tarif est en ligne : dupliquez la fiche en brouillon, puis faites-la publier par la Direction.', '', err);
    }
    if (/chk_child_group_price_never_higher_than_individual/.test(full)) {
      var child = row.child_price_fcfa;
      var grp = row.group_child_price_fcfa;
      var detail = (grp != null && child != null) ? ' (' + grp + ' FCFA saisis, plafond ' + child + ' FCFA)' : '';
      return Errors.make('CHILD_PRICE_GUARD', 'Le tarif enfant groupe ne peut pas dépasser le tarif enfant individuel' + detail + '.', '', err);
    }
    if (/ECOPARK_SELF_ROLE_CHANGE_FORBIDDEN/.test(full)) {
      return Errors.make('SELF_ROLE_CHANGE', 'Vous ne pouvez pas modifier votre propre rôle ni votre propre statut.', '', err);
    }
    if (/ECOPARK_AUDIT_IMMUTABLE/.test(full)) {
      return Errors.make('AUDIT_IMMUTABLE', 'Le journal d\'audit ne peut être ni modifié ni effacé.', '', err);
    }
    if (/ECOPARK_DUPLICATE_NOT_SUPPORTED/.test(full)) {
      return Errors.make('DUPLICATE_NOT_SUPPORTED', 'Ce type de fiche ne peut pas être dupliqué.', '', err);
    }
    if (/ECOPARK_NOT_FOUND/.test(full) || code === 'P0002') {
      return Errors.make('NOT_FOUND', 'Cette fiche n\'existe plus (elle a peut-être été supprimée).', '', err);
    }
    if (code === '23505' || /duplicate key/i.test(full)) {
      return Errors.make('DUPLICATE_KEY', 'Ce code (référence, SKU ou slug) existe déjà.', '', err);
    }
    if (code === '23514' || /violates check constraint/i.test(full)) {
      return Errors.make('INVALID_VALUE', 'Une valeur saisie est refusée par les règles métier (montant, nombre de participants, date...).', '', err);
    }
    if (code === '42501' || /row-level security|permission denied|ECOPARK_FORBIDDEN/i.test(full)) {
      return Errors.make('FORBIDDEN', 'Action non autorisée pour votre rôle.', '', err);
    }
    return Errors.make('UNKNOWN', 'L\'opération n\'a pas abouti. Réessayez ou contactez l\'administrateur.', msg, err);
  };

  // ==========================================================================
  // 3. CONFIGURATION & CHOIX DU PILOTE
  // ==========================================================================
  function readConfig() {
    var cfg = clone(root.ECOPARK_CONFIG || {}) || {};
    cfg.env = cfg.env || 'local';
    return cfg;
  }
  function resolveDriverName(cfg, search) {
    var params;
    try { params = new URLSearchParams(search || ''); } catch (e) { params = { get: function () { return null; } }; }
    if (params.get('demo') === '77') return 'local';
    if (cfg.dataDriver !== 'supabase') return 'local';
    if (!cfg.supabaseUrl || !cfg.supabaseAnonKey) return 'local';
    return 'supabase';
  }

  // ==========================================================================
  // 4. MAGASIN (état lu de façon synchrone par loadDB)
  // ==========================================================================
  function Store(opts) {
    this.storage = opts.storage;
    this.persistKey = opts.persistKey;        // null = mémoire uniquement
    this.persistFilter = opts.persistFilter;  // fonction(state) -> partie à persister
    this.defaults = clone(opts.defaults || {});
    this.listeners = [];
    this.state = this._read();
  }
  Store.prototype._read = function () {
    var base = clone(this.defaults);
    if (!this.persistKey) return base;
    try {
      var raw = this.storage.getItem(this.persistKey);
      return raw ? Object.assign(base, JSON.parse(raw)) : base;
    } catch (e) { return base; }
  };
  Store.prototype.persist = function () {
    if (!this.persistKey) return;
    try {
      var part = this.persistFilter ? this.persistFilter(this.state) : this.state;
      this.storage.setItem(this.persistKey, JSON.stringify(part));
    } catch (e) { /* quota plein : on reste en mémoire */ }
  };
  /** Relit l'état persistant (synchronisation entre onglets du même navigateur) */
  Store.prototype.reload = function () {
    this.state = this._read();
    return this.state;
  };
  /** Copie profonde, dans le format historique attendu par loadDB() */
  Store.prototype.snapshot = function () {
    return Object.assign(clone(this.defaults), clone(this.state));
  };
  Store.prototype.replace = function (next, meta) {
    this.state = clone(next);
    this.persist();
    this.emit(meta || { source: 'replace' });
  };
  Store.prototype.patch = function (fn, meta) {
    var draft = clone(this.state);
    var out = fn(draft);
    this.state = out || draft;
    this.persist();
    this.emit(meta || { source: 'patch' });
  };
  Store.prototype.subscribe = function (fn) {
    var self = this;
    self.listeners.push(fn);
    return function () { self.listeners = self.listeners.filter(function (l) { return l !== fn; }); };
  };
  Store.prototype.emit = function (meta) {
    this.listeners.slice().forEach(function (l) { try { l(meta); } catch (e) { /* écran défaillant isolé */ } });
  };
  Store.prototype.content = function (entity) {
    var c = this.state.content || {};
    return c[entity] || (entity === 'site_settings' ? {} : []);
  };

  // ==========================================================================
  // 5. RÈGLES MÉTIER PARTAGÉES (reproduites en démo, appliquées par la base en prod)
  // ==========================================================================
  var PRICE_COLS = {
    catalog_activities: ['child_price_fcfa', 'adult_price_fcfa', 'group_adult_price_fcfa', 'group_child_price_fcfa'],
    sales_bundles: ['adult_bundle_price_fcfa', 'child_bundle_price_fcfa'],
    lodge_cities: ['min_price_fcfa', 'max_price_fcfa']
  };
  var UNIQUE_COLS = {
    catalog_activities: [['slug', '-copie-'], ['sku', '-COPIE-']],
    sales_bundles: [['bundle_code', '_COPIE_'], ['sku', '-COPIE-']],
    agenda_events: [['code', '_COPIE_']],
    menu_items: [['sku', '-COPIE-']]
  };
  var TITLE_COL = { catalog_activities: 'title', sales_bundles: 'title', agenda_events: 'title', menu_items: 'name' };
  var Rules = {
    isPriceEntity: function (e) { return has(PRICE_COLS, e); },
    /** Toute fiche publiée doit avoir une image (règle appliquée aussi par la base) */
    needsImage: function (e) { return has(TITLE_COL, e) || e === 'lodge_cities'; },
    hasImage: function (row) { return !!(row && row.image_src && String(row.image_src).trim()); },
    /** Sources acceptées : photothèque du site, stockage https, ou image locale en mode démo */
    safeImageSrc: function (src) {
      return !src || /^(https:\/\/[A-Za-z0-9.-]+\/|audit-assets\/)[^"'<>\s]*$/.test(src) || /^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(src);
    },
    canPublish: function (entity, role) {
      if (Rules.isPriceEntity(entity)) return role === 'direction';
      return ['responsable_exploitation', 'direction', 'administrateur_plateforme'].indexOf(role) >= 0;
    },
    canEdit: function (role) {
      return ['responsable_exploitation', 'direction', 'administrateur_plateforme'].indexOf(role) >= 0;
    },
    canDelete: function (entity, role) {
      if (Rules.isPriceEntity(entity)) return role === 'direction' || role === 'administrateur_plateforme';
      return Rules.canEdit(role);
    },
    childGuard: function (entity, row) {
      if (entity !== 'catalog_activities') return null;
      if (row.group_child_price_fcfa > row.child_price_fcfa) {
        return { code: '23514', message: 'new row violates check constraint "chk_child_group_price_never_higher_than_individual"' };
      }
      return null;
    },
    uniqueCopy: function (rows, col, base, sep) {
      var b = String(base).replace(/(-|_)copie(-|_)\d+$/i, '');
      var n = 0;
      var candidate;
      var taken = {};
      rows.forEach(function (r) { taken[r[col]] = true; });
      do { n += 1; candidate = b + sep + n; } while (taken[candidate]);
      return candidate;
    }
  };

  // ==========================================================================
  // 5 bis. IMAGES DES PUBLICATIONS
  // ==========================================================================
  var IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
  var IMAGE_MAX_BYTES = 5 * 1024 * 1024;
  var IMAGE_DEMO_MAX_CHARS = 600000; // ~450 Ko : au-delà, le stockage du navigateur risque de saturer
  function blobToDataUrl(blob) {
    return blob.arrayBuffer().then(function (buf) {
      var bytes = new Uint8Array(buf);
      var bin = '';
      for (var i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
      var b64 = typeof btoa === 'function' ? btoa(bin) : Buffer.from(bin, 'binary').toString('base64');
      return 'data:' + (blob.type || 'image/jpeg') + ';base64,' + b64;
    });
  }
  function checkImageBlob(blob) {
    if (!blob || IMAGE_TYPES.indexOf(blob.type) < 0) {
      return Errors.make('IMAGE_TYPE', 'Format non accepté : choisissez une photo JPEG, PNG ou WebP.');
    }
    if (blob.size > IMAGE_MAX_BYTES) {
      return Errors.make('IMAGE_TOO_LARGE', 'Image trop lourde (5 Mo maximum après optimisation).');
    }
    return null;
  }

  // ==========================================================================
  // 6. PILOTE DÉMO (localStorage) — reproduit les règles de la base
  // ==========================================================================
  function LocalDemoDriver(store, opts) {
    this.name = 'local';
    this.store = store;
    this.role = (opts && opts.demoRole) || 'direction';
    this.uid = 0;
  }
  LocalDemoDriver.prototype.init = function () { return Promise.resolve({ ok: true }); };
  LocalDemoDriver.prototype._newId = function () {
    this.uid += 1;
    return 'demo-' + Date.now().toString(36) + '-' + this.uid;
  };
  LocalDemoDriver.prototype._rows = function (state, entity) {
    var reg = Registry[entity];
    if (!reg) throw new Error('Entité inconnue : ' + entity);
    if (reg.legacyKey) { state[reg.legacyKey] = state[reg.legacyKey] || []; return state[reg.legacyKey]; }
    state.content = state.content || {};
    state.content[entity] = state.content[entity] || [];
    return state.content[entity];
  };
  LocalDemoDriver.prototype._fail = function (raw, ctx) { return Promise.resolve({ ok: false, error: Errors.translate(raw, ctx) }); };
  LocalDemoDriver.prototype._audit = function (state, op, entity, label) {
    state.auditLogs = state.auditLogs || [];
    var verbs = { INSERT: 'Ajout', UPDATE: 'Modification', DELETE: 'Suppression définitive', DUPLICATE: 'Duplication (brouillon)', PUBLISH: 'Publication', ARCHIVE: 'Archivage', RESTORE: 'Restauration' };
    var d = new Date();
    var p = function (n) { return ('0' + n).slice(-2); };
    state.auditLogs.unshift({
      time: p(d.getDate()) + '/' + p(d.getMonth() + 1) + '/' + d.getFullYear() + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()),
      actor: 'Mode démonstration (' + this.role + ')',
      action: (verbs[op] || op) + ' — ' + entity + ' « ' + (label || '?') + ' »',
      operation: op
    });
  };
  LocalDemoDriver.prototype.list = function (entity, q) {
    q = q || {};
    var rows = clone(this._rows(this.store.state, entity));
    if (q.filters) {
      rows = rows.filter(function (r) {
        return Object.keys(q.filters).every(function (k) { return r[k] === q.filters[k]; });
      });
    }
    return Promise.resolve({ ok: true, data: rows });
  };
  LocalDemoDriver.prototype.get = function (entity, id) {
    var key = Registry[entity].legacyKey ? (Registry[entity].legacyId || 'reference') : Registry[entity].key;
    var row = this._rows(this.store.state, entity).filter(function (r) { return r[key] === id; })[0];
    return Promise.resolve(row ? { ok: true, data: clone(row) } : { ok: false, error: Errors.translate({ code: 'P0002' }) });
  };
  LocalDemoDriver.prototype.create = function (entity, data) {
    var self = this;
    var reg = Registry[entity];
    var row = clone(data);
    if (reg.content && entity !== 'site_settings') {
      if (!Rules.canEdit(self.role)) return self._fail({ code: '42501' });
      row.id = row.id || self._newId();
      row.status = row.status || 'DRAFT';
      if (Rules.isPriceEntity(entity) && row.status !== 'DRAFT' && self.role !== 'direction') {
        return self._fail({ message: 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' });
      }
      if (!Rules.safeImageSrc(row.image_src)) return self._fail({ message: 'chk_x_image_src_safe' });
      if (row.status === 'PUBLISHED' && Rules.needsImage(entity) && !Rules.hasImage(row)) {
        return self._fail({ message: 'ECOPARK_IMAGE_REQUIRED' });
      }
      if (Rules.hasImage(row) && !row.image_alt) row.image_alt = row[TITLE_COL[entity]] || row.name || '';
      var guard = Rules.childGuard(entity, row);
      if (guard) return self._fail(guard, { row: row });
      row.version = 1;
    }
    var dupKey = (UNIQUE_COLS[entity] || []).filter(function (uc) {
      return self._rows(self.store.state, entity).some(function (r) { return r[uc[0]] === row[uc[0]]; });
    })[0];
    if (dupKey) return self._fail({ code: '23505' });
    self.store.patch(function (s) {
      var rows = self._rows(s, entity);
      rows.unshift(row);
      if (reg.content) self._audit(s, 'INSERT', entity, row[TITLE_COL[entity]] || row.key);
    }, { source: 'local', entity: entity, op: 'create' });
    return Promise.resolve({ ok: true, data: clone(row) });
  };
  LocalDemoDriver.prototype.update = function (entity, id, patch, version) {
    var self = this;
    var reg = Registry[entity];
    var keyCol = reg.legacyKey ? (reg.legacyId || 'reference') : reg.key;
    var current = self._rows(self.store.state, entity).filter(function (r) { return r[keyCol] === id; })[0];
    if (!current) return self._fail({ code: 'P0002' });
    if (reg.content) {
      if (!Rules.canEdit(self.role)) return self._fail(null, { kind: 'NO_ROWS_RIGHTS' });
      if (version != null && current.version !== version) return self._fail(null, { kind: 'VERSION_CONFLICT' });
      var next = Object.assign(clone(current), patch);
      if (Rules.isPriceEntity(entity) && self.role !== 'direction') {
        if (next.status !== current.status && (next.status === 'PUBLISHED' || current.status === 'PUBLISHED')) {
          return self._fail({ message: 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' });
        }
        if (current.status === 'PUBLISHED' && PRICE_COLS[entity].some(function (c) { return next[c] !== current[c]; })) {
          return self._fail({ message: 'ECOPARK_PUBLISHED_PRICE_LOCKED' });
        }
      }
      var guard = Rules.childGuard(entity, next);
      if (guard) return self._fail(guard, { row: next });
      if (!Rules.safeImageSrc(next.image_src)) return self._fail({ message: 'chk_x_image_src_safe' });
      if (next.status === 'PUBLISHED' && Rules.needsImage(entity) && !Rules.hasImage(next)) {
        return self._fail({ message: 'ECOPARK_IMAGE_REQUIRED' });
      }
      if (Rules.hasImage(next) && !next.image_alt) patch = Object.assign({}, patch, { image_alt: next[TITLE_COL[entity]] || next.name || '' });
    }
    var saved;
    self.store.patch(function (s) {
      var rows = self._rows(s, entity);
      var idx = rows.findIndex(function (r) { return r[keyCol] === id; });
      saved = Object.assign(rows[idx], patch);
      if (reg.content) {
        saved.version = (current.version || 1) + 1;
        if (saved.status === 'PUBLISHED' && !saved.first_published_at) saved.first_published_at = new Date().toISOString();
        self._audit(s, 'UPDATE', entity, saved[TITLE_COL[entity]] || saved.key);
      }
    }, { source: 'local', entity: entity, op: 'update' });
    return Promise.resolve({ ok: true, data: clone(saved) });
  };
  LocalDemoDriver.prototype.duplicate = function (entity, id) {
    var self = this;
    if (!UNIQUE_COLS[entity]) return self._fail({ message: 'ECOPARK_DUPLICATE_NOT_SUPPORTED' });
    if (!Rules.canEdit(self.role)) return self._fail({ message: 'ECOPARK_FORBIDDEN' });
    var rows = self._rows(self.store.state, entity);
    var src = rows.filter(function (r) { return r.id === id; })[0];
    if (!src) return self._fail({ code: 'P0002' });
    var copy = clone(src);
    copy.id = self._newId();
    UNIQUE_COLS[entity].forEach(function (uc) { copy[uc[0]] = Rules.uniqueCopy(rows, uc[0], src[uc[0]], uc[1]); });
    var tc = TITLE_COL[entity];
    copy[tc] = src[tc] + ' (Copie)';
    if (entity === 'agenda_events') copy.short_label = src.short_label + ' (Copie)';
    if (entity === 'sales_bundles') copy.is_featured = false;
    copy.status = 'DRAFT';
    copy.duplicated_from = src.id;
    copy.first_published_at = null;
    copy.version = 1;
    copy.sort_order = (src.sort_order || 0) + 1;
    self.store.patch(function (s) {
      var list = self._rows(s, entity);
      var idx = list.findIndex(function (r) { return r.id === id; });
      list.splice(idx + 1, 0, copy);
      self._audit(s, 'DUPLICATE', entity, copy[tc]);
    }, { source: 'local', entity: entity, op: 'duplicate' });
    return Promise.resolve({ ok: true, data: copy.id });
  };
  LocalDemoDriver.prototype.setStatus = function (entity, id, status, replaceOriginal) {
    var self = this;
    var rows = self._rows(self.store.state, entity);
    var row = rows.filter(function (r) { return r.id === id; })[0];
    if (!row) return self._fail({ code: 'P0002' });
    var needsPublishRight = status === 'PUBLISHED' || (row.status === 'PUBLISHED' && status === 'DRAFT');
    if (needsPublishRight && !Rules.canPublish(entity, self.role)) return self._fail({ message: 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' });
    if (status === 'ARCHIVED' && !Rules.canDelete(entity, self.role)) return self._fail({ message: 'ECOPARK_FORBIDDEN' });
    if (status === 'PUBLISHED' && Rules.needsImage(entity) && !Rules.hasImage(row)) return self._fail({ message: 'ECOPARK_IMAGE_REQUIRED' });
    var origin = row.duplicated_from ? rows.filter(function (r) { return r.id === row.duplicated_from; })[0] : null;
    var target = id;
    self.store.patch(function (s) {
      var list = self._rows(s, entity);
      var draft = list.filter(function (r) { return r.id === id; })[0];
      if (status === 'PUBLISHED' && replaceOriginal && origin && origin.status === 'PUBLISHED') {
        var o = list.filter(function (r) { return r.id === origin.id; })[0];
        var keep = { id: o.id, status: o.status, version: o.version, first_published_at: o.first_published_at, duplicated_from: o.duplicated_from, sort_order: o.sort_order };
        (UNIQUE_COLS[entity] || []).forEach(function (uc) { keep[uc[0]] = o[uc[0]]; });
        Object.assign(o, clone(draft), keep);
        var tc = TITLE_COL[entity];
        o[tc] = String(o[tc]).replace(/\s*\(Copie\)$/, '');
        if (o.short_label) o.short_label = String(o.short_label).replace(/\s*\(Copie\)$/, '');
        o.version = (o.version || 1) + 1;
        draft.status = 'ARCHIVED';
        target = o.id;
        self._audit(s, 'PUBLISH', entity, o[tc]);
      } else {
        draft.status = status;
        draft.version = (draft.version || 1) + 1;
        if (status === 'PUBLISHED' && !draft.first_published_at) draft.first_published_at = new Date().toISOString();
        self._audit(s, status === 'PUBLISHED' ? 'PUBLISH' : status === 'ARCHIVED' ? 'ARCHIVE' : 'RESTORE', entity, draft[TITLE_COL[entity]]);
      }
    }, { source: 'local', entity: entity, op: 'setStatus' });
    return Promise.resolve({ ok: true, data: target });
  };
  LocalDemoDriver.prototype.remove = function (entity, id) {
    var self = this;
    if (!Rules.canDelete(entity, self.role)) return self._fail({ message: 'ECOPARK_FORBIDDEN' });
    var row = self._rows(self.store.state, entity).filter(function (r) { return r.id === id; })[0];
    if (!row) return self._fail({ code: 'P0002' });
    var hard = row.status === 'DRAFT' && !row.first_published_at;
    self.store.patch(function (s) {
      var list = self._rows(s, entity);
      var idx = list.findIndex(function (r) { return r.id === id; });
      if (hard) list.splice(idx, 1); else { list[idx].status = 'ARCHIVED'; list[idx].version = (list[idx].version || 1) + 1; }
      self._audit(s, hard ? 'DELETE' : 'ARCHIVE', entity, row[TITLE_COL[entity]]);
    }, { source: 'local', entity: entity, op: 'remove' });
    return Promise.resolve({ ok: true, data: hard ? 'DELETED' : 'ARCHIVED' });
  };
  LocalDemoDriver.prototype.rpc = function (name) {
    return Promise.resolve({ ok: false, error: Errors.make('NOT_AVAILABLE_IN_DEMO', 'Fonction serveur « ' + name + ' » indisponible en mode démonstration.') });
  };
  /** Démo : l'image est conservée dans le navigateur (format data:image), sans serveur */
  LocalDemoDriver.prototype.uploadImage = function (blob) {
    if (!Rules.canEdit(this.role)) return this._fail({ code: '42501' });
    var bad = checkImageBlob(blob);
    if (bad) return Promise.resolve({ ok: false, error: bad });
    return blobToDataUrl(blob).then(function (url) {
      if (url.length > IMAGE_DEMO_MAX_CHARS) {
        return { ok: false, error: Errors.make('IMAGE_TOO_HEAVY_DEMO', 'Image trop lourde pour le mode démonstration (450 Ko maximum après optimisation).') };
      }
      return { ok: true, data: { url: url, storage: 'demo' } };
    });
  };
  /** Suppression directe d'une ligne sans cycle de vie (ex. dérogation de quota) */
  LocalDemoDriver.prototype.removeRow = function (entity, id) {
    var self = this;
    var key = Registry[entity].key;
    if (!Rules.canEdit(self.role)) return self._fail({ code: '42501' });
    self.store.patch(function (s) {
      var rows = self._rows(s, entity);
      var idx = rows.findIndex(function (r) { return r[key] === id; });
      if (idx >= 0) rows.splice(idx, 1);
    }, { source: 'local', entity: entity, op: 'removeRow' });
    return Promise.resolve({ ok: true, data: 'DELETED' });
  };
  /** Réglage du site (site_settings est stocké comme un objet clé -> valeur) */
  LocalDemoDriver.prototype.saveSetting = function (key, value) {
    var self = this;
    if (!Rules.canEdit(self.role)) return self._fail({ code: '42501' });
    self.store.patch(function (s) {
      s.content = s.content || {};
      s.content.site_settings = s.content.site_settings || {};
      s.content.site_settings[key] = clone(value);
      self._audit(s, 'UPDATE', 'site_settings', key);
    }, { source: 'local', entity: 'site_settings', op: 'saveSetting' });
    return Promise.resolve({ ok: true, data: clone(value) });
  };
  LocalDemoDriver.prototype.logEvent = function (code, entity, id, description) {
    var self = this;
    self.store.patch(function (s) { self._audit(s, code, entity || '-', description); }, { source: 'local', op: 'logEvent' });
    return Promise.resolve({ ok: true });
  };
  LocalDemoDriver.prototype.subscribe = function () { return noop; };
  LocalDemoDriver.prototype.session = function () {
    return Promise.resolve({ ok: true, data: { role: this.role, full_name: 'Mode démonstration', mfa_satisfied: true, demo: true } });
  };
  LocalDemoDriver.prototype.refreshContent = function () { return Promise.resolve({ ok: true }); };

  // ==========================================================================
  // 7. PILOTE SUPABASE
  // ==========================================================================
  function SupabaseDriver(store, opts) {
    this.name = 'supabase';
    this.store = store;
    this.client = opts.client;
    this.channels = [];
    this.pending = {};
    this.debounceMs = opts.debounceMs == null ? 250 : opts.debounceMs;
    this.pollMs = opts.pollMs == null ? 60000 : opts.pollMs;
    this.pollTimer = null;
    this.realtimeHealthy = false;
    this.onStatus = opts.onStatus || noop;
  }
  SupabaseDriver.prototype._res = function (promise, ctx) {
    return Promise.resolve(promise).then(function (r) {
      if (r && r.error) return { ok: false, error: Errors.translate(r.error, ctx) };
      return { ok: true, data: r ? r.data : null, count: r ? r.count : null };
    }, function (e) {
      return { ok: false, error: Errors.translate(e, Object.assign({ kind: 'NETWORK' }, ctx || {})) };
    });
  };
  SupabaseDriver.prototype.init = function () {
    var self = this;
    return self.refreshContent().then(function (r) {
      self._subscribeContent();
      self._startPolling();
      return r;
    });
  };
  /** Relit tout le contenu public (lignes publiées ; tout le contenu si l'utilisateur est membre de l'équipe) */
  SupabaseDriver.prototype.refreshContent = function (only) {
    var self = this;
    var entities = only ? [].concat(only) : Object.keys(Registry).filter(function (e) { return Registry[e].content; });
    return Promise.all(entities.map(function (e) {
      return self._res(self.client.from(e).select('*').order(Registry[e].order || 'id')).then(function (r) { return [e, r]; });
    })).then(function (pairs) {
      var failed = pairs.filter(function (p) { return !p[1].ok; });
      self.store.patch(function (s) {
        s.content = s.content || {};
        pairs.forEach(function (p) {
          if (!p[1].ok) return;
          if (p[0] === 'site_settings') {
            var obj = {};
            (p[1].data || []).forEach(function (row) { obj[row.key] = row.value; });
            s.content.site_settings = obj;
          } else {
            s.content[p[0]] = p[1].data || [];
          }
        });
        s.contentFetchedAt = new Date().toISOString();
      }, { source: 'supabase', op: 'refreshContent', entities: entities });
      return failed.length ? { ok: false, error: failed[0][1].error } : { ok: true };
    });
  };
  SupabaseDriver.prototype._schedule = function (entity) {
    var self = this;
    if (self.pending[entity]) return;
    self.pending[entity] = setTimeout(function () {
      delete self.pending[entity];
      if (Registry[entity] && Registry[entity].content) self.refreshContent(entity);
      else self.store.emit({ source: 'realtime', entity: entity });
    }, self.debounceMs);
  };
  SupabaseDriver.prototype._subscribeContent = function () {
    var self = this;
    if (!self.client.channel) return;
    var ch = self.client.channel('ecopark-public-content');
    Object.keys(Registry).filter(function (e) { return Registry[e].realtime === 'public'; }).forEach(function (e) {
      ch = ch.on('postgres_changes', { event: '*', schema: 'public', table: e }, function () { self._schedule(e); });
    });
    ch.subscribe(function (status) {
      self.realtimeHealthy = status === 'SUBSCRIBED';
      self.onStatus(self.realtimeHealthy ? 'live' : 'paused');
    });
    self.channels.push(ch);
  };
  SupabaseDriver.prototype._startPolling = function () {
    var self = this;
    if (!self.pollMs || typeof setInterval === 'undefined') return;
    // Filet de sécurité : le temps réel ne prévient pas un visiteur qu'une fiche
    // publiée vient d'être archivée (la RLS masque la nouvelle ligne) -> relecture périodique.
    // Toutes les 60 s si le temps réel est coupé, toutes les 5 min s'il fonctionne.
    self.pollTimer = setInterval(function () {
      var hidden = root.document && root.document.visibilityState === 'hidden';
      var last = Date.parse(self.store.state.contentFetchedAt || 0) || 0;
      var maxAge = self.realtimeHealthy ? self.pollMs * 5 : self.pollMs;
      if (!hidden && Date.now() - last >= maxAge - 1000) self.refreshContent();
    }, self.pollMs);
  };
  SupabaseDriver.prototype.stop = function () {
    var self = this;
    if (self.pollTimer) clearInterval(self.pollTimer);
    self.channels.forEach(function (c) { try { self.client.removeChannel(c); } catch (e) { /* déjà fermé */ } });
    self.channels = [];
  };
  SupabaseDriver.prototype.list = function (entity, q) {
    q = q || {};
    var reg = Registry[entity];
    var query = this.client.from(entity).select('*', q.count ? { count: 'exact' } : undefined);
    if (q.filters) Object.keys(q.filters).forEach(function (k) { query = query.eq(k, q.filters[k]); });
    query = query.order(q.order || reg.order || reg.key, { ascending: q.ascending !== false });
    if (q.range) query = query.range(q.range[0], q.range[1]);
    return this._res(query).then(function (r) {
      if (r.ok && reg.fromRow && q.legacy) r.data = (r.data || []).map(reg.fromRow);
      return r;
    });
  };
  SupabaseDriver.prototype.get = function (entity, id) {
    return this._res(this.client.from(entity).select('*').eq(Registry[entity].key, id).maybeSingle());
  };
  SupabaseDriver.prototype.create = function (entity, data, opts) {
    var reg = Registry[entity];
    var row = reg.toRow && opts && opts.legacy ? reg.toRow(data) : clone(data);
    var q = this.client.from(entity).insert(row);
    // Le dépôt public (devis, CFP, RDV) n'a pas le droit de relire la ligne : pas de RETURNING.
    var publicSubmit = reg.publicInsert && opts && opts.anonymous;
    if (!publicSubmit) q = q.select('*').single();
    return this._res(q, { entity: entity, row: row });
  };
  SupabaseDriver.prototype.update = function (entity, id, patch, version) {
    var self = this;
    var reg = Registry[entity];
    // Fiche complète connue du magasin : permet de citer le plafond exact dans les messages d'erreur
    var known = reg.content ? (self.store.content(entity) || []).filter(function (r) { return r[reg.key] === id; })[0] : null;
    var ctxRow = Object.assign({}, known || {}, patch);
    var q = self.client.from(entity).update(patch).eq(reg.key, id);
    if (version != null) q = q.eq('version', version);
    return self._res(q.select('*'), { entity: entity, row: ctxRow }).then(function (r) {
      if (!r.ok) return r;
      if (r.data && r.data.length === 1) return { ok: true, data: r.data[0] };
      // 0 ligne : soit la version est périmée, soit la RLS a masqué la ligne (droits / MFA)
      return self._res(self.client.from(entity).select(reg.key + ',version').eq(reg.key, id).maybeSingle()).then(function (cur) {
        if (cur.ok && cur.data && version != null && cur.data.version !== version) {
          return { ok: false, error: Errors.translate(null, { kind: 'VERSION_CONFLICT' }), current: cur.data };
        }
        return { ok: false, error: Errors.translate(null, { kind: 'NO_ROWS_RIGHTS' }) };
      });
    });
  };
  SupabaseDriver.prototype.duplicate = function (entity, id) {
    return this._res(this.client.rpc('admin_duplicate', { p_entity: entity, p_id: id }), { entity: entity });
  };
  SupabaseDriver.prototype.setStatus = function (entity, id, status, replaceOriginal) {
    return this._res(this.client.rpc('admin_set_status', { p_entity: entity, p_id: id, p_status: status, p_replace_original: !!replaceOriginal }), { entity: entity });
  };
  SupabaseDriver.prototype.remove = function (entity, id) {
    return this._res(this.client.rpc('admin_delete', { p_entity: entity, p_id: id }), { entity: entity });
  };
  SupabaseDriver.prototype.rpc = function (name, args) {
    return this._res(this.client.rpc(name, args || {}));
  };
  /** Production : dépôt dans le stockage Supabase « ecopark-media » (lecture publique, dépôt réservé à l'équipe) */
  SupabaseDriver.prototype.uploadImage = function (blob, opts) {
    var self = this;
    opts = opts || {};
    var bad = checkImageBlob(blob);
    if (bad) return Promise.resolve({ ok: false, error: bad });
    if (!self.client.storage) return Promise.resolve({ ok: false, error: Errors.make('NOT_AVAILABLE', 'Stockage des images indisponible.') });
    var ext = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp' }[blob.type];
    var month = new Date().toISOString().slice(0, 7);
    var rand = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
    var folder = String(opts.entity || 'divers').replace(/[^a-z_]/g, '');
    var path = folder + '/' + month + '/' + rand + '.' + ext;
    var bucket = self.client.storage.from('ecopark-media');
    return Promise.resolve(bucket.upload(path, blob, { contentType: blob.type, cacheControl: '31536000', upsert: false })).then(function (r) {
      if (r && r.error) return { ok: false, error: Errors.translate(r.error) };
      var pub = bucket.getPublicUrl(path);
      return { ok: true, data: { url: pub && pub.data ? pub.data.publicUrl : null, path: path, storage: 'supabase' } };
    }, function (e) { return { ok: false, error: Errors.translate(e, { kind: 'NETWORK' }) }; });
  };
  SupabaseDriver.prototype.removeRow = function (entity, id) {
    var key = Registry[entity].key;
    return this._res(this.client.from(entity).delete().eq(key, id).select(key), { entity: entity }).then(function (r) {
      if (r.ok && (!r.data || !r.data.length)) return { ok: false, error: Errors.translate(null, { kind: 'NO_ROWS_RIGHTS' }) };
      return r.ok ? { ok: true, data: 'DELETED' } : r;
    });
  };
  SupabaseDriver.prototype.saveSetting = function (key, value) {
    var self = this;
    return self._res(self.client.from('site_settings').update({ value: value }).eq('key', key).select('key'), { entity: 'site_settings' })
      .then(function (r) {
        if (r.ok && (!r.data || !r.data.length)) return { ok: false, error: Errors.translate(null, { kind: 'NO_ROWS_RIGHTS' }) };
        return r;
      });
  };
  SupabaseDriver.prototype.logEvent = function (code, entity, id, description, payload) {
    return this._res(this.client.rpc('log_admin_event', {
      p_action_code: code, p_entity_table: entity || null, p_entity_id: id || null, p_description: description || '', p_payload: payload || null
    }));
  };
  SupabaseDriver.prototype.subscribe = function (entity, cb) {
    var self = this;
    if (!self.client.channel) return noop;
    var ch = self.client.channel('ecopark-' + entity + '-' + Math.random().toString(36).slice(2, 8))
      .on('postgres_changes', { event: '*', schema: 'public', table: entity }, function (payload) { cb(payload); })
      .subscribe();
    self.channels.push(ch);
    return function () { try { self.client.removeChannel(ch); } catch (e) { /* déjà fermé */ } };
  };
  SupabaseDriver.prototype.session = function () {
    return this._res(this.client.rpc('get_my_profile'));
  };

  // ==========================================================================
  // 8. FAÇADE PUBLIQUE
  // ==========================================================================
  var EcoparkData = {
    version: '3.0.0',
    Mappers: Mappers,
    Errors: Errors,
    Rules: Rules,
    Store: Store,
    LocalDemoDriver: LocalDemoDriver,
    SupabaseDriver: SupabaseDriver,
    resolveDriverName: resolveDriverName,
    driver: null,
    driverName: 'local',
    store: null,
    config: null,
    _legacy: null,
    _ready: null,
    _warned: {}
  };

  /**
   * Déclaré par index.html avant init() : clé de stockage historique et état par défaut.
   * @param {{storageKey: string, defaults: object, snapshot?: object}} legacy
   */
  EcoparkData.configureLegacy = function (legacy) {
    EcoparkData._legacy = legacy;
  };

  /**
   * Démarre la couche de données. Synchrone pour le magasin (loadDB utilisable aussitôt),
   * asynchrone pour l'hydratation réseau (promesse retournée).
   * @param {{client?: object, storage?: object, search?: string, demoRole?: string, pollMs?: number, debounceMs?: number, onStatus?: function}} [opts]
   */
  EcoparkData.init = function (opts) {
    opts = opts || {};
    var cfg = readConfig();
    var legacy = EcoparkData._legacy || { storageKey: 'ecopark_ahala_db_sprint1_v1', defaults: {} };
    var search = opts.search != null ? opts.search : (root.location ? root.location.search : '');
    var name = resolveDriverName(cfg, search);
    if (name === 'supabase' && !opts.client && !(root.supabase && root.supabase.createClient)) name = 'local';
    var storage = opts.storage || safeStorage();

    var defaults = clone(legacy.defaults || {});
    defaults.content = clone((legacy.snapshot && legacy.snapshot.content) || {});

    var store;
    if (name === 'local') {
      store = new Store({ storage: storage, persistKey: legacy.storageKey, defaults: defaults });
      if (!store.state.content || !Object.keys(store.state.content).length) store.state.content = clone(defaults.content);
      EcoparkData.driver = new LocalDemoDriver(store, { demoRole: opts.demoRole });
    } else {
      // Production : seul le contenu PUBLIC est persisté en cache (jamais les données d'équipe)
      store = new Store({
        storage: storage,
        persistKey: 'ecopark_cache_v2_' + cfg.env,
        defaults: defaults,
        persistFilter: function (s) { return { content: s.content, contentFetchedAt: s.contentFetchedAt, snapshotVersion: cfg.snapshotVersion || null }; }
      });
      if (store.state.snapshotVersion && store.state.snapshotVersion !== (cfg.snapshotVersion || null)) {
        store.state = clone(defaults); // nouvelle copie de secours publiée : cache obsolète
      }
      var client = opts.client || root.supabase.createClient(cfg.supabaseUrl, cfg.supabaseAnonKey, {
        auth: { persistSession: true, autoRefreshToken: true }
      });
      EcoparkData.driver = new SupabaseDriver(store, {
        client: client, pollMs: opts.pollMs, debounceMs: opts.debounceMs, onStatus: opts.onStatus
      });
    }
    EcoparkData.config = cfg;
    EcoparkData.store = store;
    EcoparkData.driverName = name;
    EcoparkData._ready = EcoparkData.driver.init();
    return EcoparkData._ready;
  };
  EcoparkData.ready = function () { return EcoparkData._ready || Promise.resolve({ ok: true }); };

  // --- Compatibilité avec loadDB / saveDB du site --------------------------
  /**
   * loadDB() historique. En démo, relit localStorage à chaque appel exactement comme
   * avant (zéro régression, y compris entre onglets). En production : magasin en mémoire.
   */
  EcoparkData.legacyLoad = function () {
    if (EcoparkData.driverName === 'local') EcoparkData.store.reload();
    return EcoparkData.store.snapshot();
  };
  /**
   * saveDB() historique. En démo : persistance locale comme avant.
   * En production : l'écran est mis à jour en mémoire uniquement, et l'appel non migré est signalé.
   */
  EcoparkData.legacySave = function (db, caller) {
    var store = EcoparkData.store;
    store.state = clone(db);
    store.persist();
    if (EcoparkData.driverName === 'supabase') {
      var who = caller || 'inconnu';
      if (!EcoparkData._warned[who] && root.console && root.console.warn) {
        EcoparkData._warned[who] = true;
        root.console.warn('[EcoparkData] saveDB() non migré (' + who + ') : modification visible sur cet écran uniquement, non enregistrée en base.');
      }
    }
  };

  // --- Actions (écritures) avec copie de sécurité et retour arrière --------
  function withRollback(fn, entity) {
    var store = EcoparkData.store;
    var backup = clone(store.state);
    return fn().then(function (r) {
      if (!r.ok) { store.replace(backup, { source: 'rollback', entity: entity }); return r; }
      // Production : relire le contenu concerné sans attendre l'événement temps réel
      if (EcoparkData.driverName === 'supabase' && entity && Registry[entity] && Registry[entity].content) {
        return EcoparkData.driver.refreshContent(entity).then(function () { return r; });
      }
      return r;
    }, function (e) {
      store.replace(backup, { source: 'rollback', entity: entity });
      return { ok: false, error: Errors.translate(e, { kind: 'NETWORK' }) };
    });
  }
  ['list', 'get', 'rpc', 'session', 'refreshContent'].forEach(function (m) {
    EcoparkData[m] = function () { var d = EcoparkData.driver; return d[m].apply(d, arguments); };
  });
  ['create', 'update', 'duplicate', 'setStatus', 'remove', 'logEvent', 'removeRow', 'saveSetting'].forEach(function (m) {
    EcoparkData[m] = function () {
      var d = EcoparkData.driver;
      var args = arguments;
      var entity = m === 'logEvent' ? null : (m === 'saveSetting' ? 'site_settings' : args[0]);
      // Affichage optimiste (production) : la modification apparaît tout de suite, puis
      // elle est confirmée par la base ou annulée par le retour arrière.
      if (m === 'update' && EcoparkData.driverName === 'supabase' && Registry[entity] && Registry[entity].content && entity !== 'site_settings') {
        var id = args[1];
        var patch = args[2];
        var backupForOptimistic = clone(EcoparkData.store.state);
        EcoparkData.store.patch(function (s) {
          var rows = (s.content && s.content[entity]) || [];
          rows.forEach(function (r) { if (r.id === id) Object.assign(r, patch); });
        }, { source: 'optimistic', entity: entity });
        return d.update.apply(d, args).then(function (r) {
          if (!r.ok) { EcoparkData.store.replace(backupForOptimistic, { source: 'rollback', entity: entity }); return r; }
          return d.refreshContent(entity).then(function () { return r; });
        });
      }
      return withRollback(function () { return d[m].apply(d, args); }, entity);
    };
  });
  EcoparkData.subscribe = function (entity, cb) { return EcoparkData.driver.subscribe(entity, cb); };
  /** Téléverse une image (Blob JPEG/PNG/WebP) ; renvoie { ok, data: { url } } */
  EcoparkData.uploadImage = function (blob, opts) { return EcoparkData.driver.uploadImage(blob, opts || {}); };
  EcoparkData.onChange = function (cb) { return EcoparkData.store.subscribe(cb); };
  /**
   * Annule un ajout fait par l'ancien code AVANT l'appel à la base (affichage anticipé) :
   * la copie de sécurité de withRollback contient déjà cet ajout, il faut donc le retirer
   * explicitement. Déclenche un redessin des écrans (source 'rollback').
   * @param {string} legacyKey  ex. 'quotes'
   * @param {function} predicate  ligne à retirer
   * @param {string} [auditNeedle]  retire aussi les entrées de journal local contenant ce texte
   */
  EcoparkData.revertLegacy = function (legacyKey, predicate, auditNeedle) {
    EcoparkData.store.patch(function (s) {
      s[legacyKey] = (s[legacyKey] || []).filter(function (row) { return !predicate(row); });
      if (auditNeedle) {
        s.auditLogs = (s.auditLogs || []).filter(function (l) { return String(l.action || '').indexOf(auditNeedle) === -1; });
      }
    }, { source: 'rollback', entity: legacyKey });
  };
  /** Contenu public courant (lignes publiées, triées) — lecture synchrone */
  EcoparkData.content = function (entity, opts) {
    var rows = EcoparkData.store.content(entity);
    if (entity === 'site_settings') return rows;
    var all = opts && opts.includeDrafts;
    return rows.filter(function (r) { return all || r.status === 'PUBLISHED'; })
      .slice().sort(function (a, b) { return (a.sort_order || 0) - (b.sort_order || 0); });
  };
  EcoparkData.setting = function (key) {
    var s = EcoparkData.store ? EcoparkData.store.content('site_settings') : {};
    return s[key];
  };

  root.EcoparkData = EcoparkData;
  if (typeof module !== 'undefined' && module.exports) module.exports = EcoparkData;
})(typeof window !== 'undefined' ? window : globalThis);
