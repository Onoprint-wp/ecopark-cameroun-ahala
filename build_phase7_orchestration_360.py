# -*- coding: utf-8 -*-
"""
Builder Phase 7 — Orchestration Multi-Agents 360° & Optimisation de l'Existant (ECOPARK Yaoundé-Ahala)

Intègre de manière 100 % idempotente dans :
  - etape0-site-live/index.html
  - Prototype_Interactif_ECOPARK_NEW_LOOK.html

Les 5 leviers d'optimisation Phase 7 :
  1. SEO Structuré Schema.org JSON-LD Multi-Entités (#ecoparkSchemaJsonLd : TouristAttraction,
     LocalBusiness, LodgingBusiness, Restaurant, EducationalOrganization) dans <head>.
  2. Neuro-Copywriting AIDA : Bandeau d'ancrage d'aversion à la perte (#heroLossAversionCallout)
     et Carte de Soulagement Dopaminergique Post-Formulaire (#dopamineReliefCard) avec Pont
     Direct WhatsApp 1-Clic (+237 697 13 62 03).
  3. Back-Office : Module « Inbox Unifiée des Leads & Dossiers — Statuts en 1 Clic » (#admLeadsInboxCard)
     consolidant Billets QR, Devis Groupes B2B/Écoles, RDV et Candidatures CFP avec filtrage
     et transition de statut en 1 clic tracée dans le journal d'audit.
  4. Sécurité & Contrat d'Interface : Assainissement Anti-XSS systématique (sanitizeEcoparkInput)
     sur tous les formulaires et validateur contractuel (validateEcoparkLeadContract) conforme à
     lead-and-ticket-schema.json.
  5. Respect strict des invariants de production :
     - 0 caractère > U+25FF (zéro emoji OS)
     - 0 code technique (PUB-xx, ADM-xx...) visible en mode visiteur
     - Parité stricte octet par octet entre etape0-site-live/index.html et Prototype_Interactif_ECOPARK_NEW_LOOK.html
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
TARGETS = [
    ROOT / "etape0-site-live" / "index.html",
    ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

SCHEMA_START = "<!-- ECOPARK_SCHEMA_JSONLD:START -->"
SCHEMA_END = "<!-- ECOPARK_SCHEMA_JSONLD:END -->"

HERO_ANCHOR_START = "<!-- ECOPARK_HERO_NEURO_ANCHOR:START -->"
HERO_ANCHOR_END = "<!-- ECOPARK_HERO_NEURO_ANCHOR:END -->"

DOPAMINE_CARD_START = "<!-- ECOPARK_DOPAMINE_RELIEF:START -->"
DOPAMINE_CARD_END = "<!-- ECOPARK_DOPAMINE_RELIEF:END -->"

ADM_INBOX_START = "<!-- ECOPARK_ADM_LEADS_INBOX:START -->"
ADM_INBOX_END = "<!-- ECOPARK_ADM_LEADS_INBOX:END -->"

PHASE7_JS_START = "// ECOPARK_PHASE7_ORCHESTRATION:START"
PHASE7_JS_END = "// ECOPARK_PHASE7_ORCHESTRATION:END"


SCHEMA_JSONLD_HTML = SCHEMA_START + r"""
  <meta name="theme-color" content="#1D490D" />
  <script type="application/ld+json" id="ecoparkSchemaJsonLd">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": ["TouristAttraction", "LocalBusiness", "AmusementPark"],
        "@id": "https://ecopark-cameroun-ahala.vercel.app/#ecopark-ahala",
        "name": "ECOPARK CAMEROUN — Yaounde-Ahala",
        "alternateName": "EcoPark Cameroun Ahala Barriere",
        "description": "Complexe agro-ecotouristique, parc animalier (gorille ToTo), lac et pirogues, piscine semi-olympique surveillee, restaurant Le Chateau des Saveurs, Cites Hotelieres (Bene, Chanthel, Ewondo VIP), Salle Menkii Essomba Anton et CFP agree MINEFOP a Yaounde-Ahala (face station Tradex).",
        "url": "https://ecopark-cameroun-ahala.vercel.app/",
        "telephone": "+237 697 13 62 03",
        "email": "info@ecopark-yaounde.com",
        "priceRange": "500 FCFA - 30 000 FCFA",
        "currenciesAccepted": "XAF",
        "paymentAccepted": "Orange Money, MTN Mobile Money, Cash (FCFA)",
        "image": [
          "https://ecopark-cameroun-ahala.vercel.app/audit-assets/ecopark-real-media/balade_pirogue3.jpg",
          "https://ecopark-cameroun-ahala.vercel.app/audit-assets/ecopark-real-media/chimpanze.jpeg",
          "https://ecopark-cameroun-ahala.vercel.app/audit-assets/ecopark-real-media/chambre.jpeg"
        ],
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Route Nationale N3, Quartier Ahala Barriere, Face Station Tradex Ahala",
          "addressLocality": "Yaounde",
          "addressRegion": "Centre",
          "addressCountry": "CM"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": 3.7925,
          "longitude": 11.4882
        },
        "openingHoursSpecification": [
          {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "09:00",
            "closes": "18:00"
          }
        ],
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "4.9",
          "reviewCount": "214",
          "bestRating": "5"
        }
      },
      {
        "@type": ["Hotel", "LodgingBusiness"],
        "@id": "https://ecopark-cameroun-ahala.vercel.app/#cites-hotelieres",
        "name": "Cites Hotelieres ECOPARK — Bene, Chanthel & Ewondo VIP",
        "parentOrganization": { "@id": "https://ecopark-cameroun-ahala.vercel.app/#ecopark-ahala" },
        "description": "Trois cites d'hebergement au coeur de la verdure d'Ahala (reception 24h/24) : Cite Bene (10 000 a 15 000 FCFA), Cite Chanthel (15 000 a 25 000 FCFA) et Cite Ewondo VIP (Suites climatisees 25 000 a 30 000 FCFA).",
        "priceRange": "10 000 FCFA - 30 000 FCFA",
        "currenciesAccepted": "XAF",
        "telephone": "+237 697 13 62 03",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Ahala Barriere, Face Station Tradex RN3",
          "addressLocality": "Yaounde",
          "addressCountry": "CM"
        }
      },
      {
        "@type": "Restaurant",
        "@id": "https://ecopark-cameroun-ahala.vercel.app/#chateau-des-saveurs",
        "name": "Le Chateau des Saveurs — ECOPARK Ahala",
        "parentOrganization": { "@id": "https://ecopark-cameroun-ahala.vercel.app/#ecopark-ahala" },
        "servesCuisine": ["Camerounaise", "Africaine", "Grillades & Poisson braise d'Ahala", "Poulet DG Royal", "Ndole"],
        "priceRange": "3 500 FCFA - 8 500 FCFA",
        "currenciesAccepted": "XAF",
        "acceptsReservations": "True",
        "telephone": "+237 697 13 62 03"
      },
      {
        "@type": "EducationalOrganization",
        "@id": "https://ecopark-cameroun-ahala.vercel.app/#cfp-minefop",
        "name": "Centre de Formation Professionnelle (CFP) ECOPARK — Agree MINEFOP",
        "parentOrganization": { "@id": "https://ecopark-cameroun-ahala.vercel.app/#ecopark-ahala" },
        "description": "Formation professionnelle agreee par le MINEFOP (DQP/CQP en 12 mois, 70 % de pratique sur site a Ahala) dans 5 filieres : Hotellerie, Restauration, Decoration, Production Agropastorale et Pisciculture. Inscription 50 000 FCFA + scolarite 250 000 FCFA en 4 tranches.",
        "telephone": "+237 697 13 62 03",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Campus ECOPARK Ahala Barriere, RN3 Face Tradex",
          "addressLocality": "Yaounde",
          "addressCountry": "CM"
        }
      }
    ]
  }
  </script>
""" + SCHEMA_END


HERO_ANCHOR_HTML = HERO_ANCHOR_START + r"""
                <div id="heroLossAversionCallout" class="monochrome-callout" style="margin:0 0 18px 0;padding:10px 14px;border-radius:14px;background:#EDF4E7;border:1px solid rgba(29,73,13,0.18);font-size:13px;color:var(--color-brand-deep);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                  <span><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg> <strong>Zero attente au guichet RN3 :</strong> Economisez <strong>1 000 FCFA/pers.</strong> sur Pass QR • Tarif enfant garanti <strong>500 FCFA</strong></span>
                  <span class="price-pill" style="font-size:11.5px;padding:2px 9px;">Report Pluie 90j Gratuit</span>
                </div>
""" + HERO_ANCHOR_END


DOPAMINE_CARD_HTML = DOPAMINE_CARD_START + r"""
                <!-- CARTE DE SOULAGEMENT DOPAMINERGIQUE POST-FORMULAIRE & PONT DIRECT WHATSAPP 1-CLIC -->
                <div class="card" id="dopamineReliefCard" style="margin-top:14px;padding:16px 18px;background:linear-gradient(135deg, #EDF4E7 0%, #FBF5EC 100%);border:1.5px solid #C47D2B;border-radius:20px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;">
                    <span style="font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;color:#9A5B13;display:inline-flex;align-items:center;gap:5px;">
                      <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                      Confirmation &amp; Garantie Coupe-File Activee
                    </span>
                    <span class="price-pill" id="dopamineReliefRefBadge" style="font-size:12px;padding:2px 10px;">ECP-2026-84920</span>
                  </div>
                  <strong id="dopamineReliefTitle" style="font-family:var(--font-heading);font-size:1.12rem;color:var(--color-brand-deep);display:block;margin-bottom:4px;">
                    Respirez : votre accès prioritaire et vos tarifs en FCFA sont verrouillés à Ahala.
                  </strong>
                  <p id="dopamineReliefMessage" style="font-size:13.2px;color:var(--color-text-muted);line-height:1.45;margin:0 0 10px 0;">
                    Aucune attente au portail RN3 (face station Tradex). Votre Billet QR fonctionne même sans forfait Internet et bénéficie de la Garantie Météo 90 jours.
                  </p>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <button type="button" class="btn btn-primary btn-sm" id="btnDopamineWhatsAppBridge" style="flex:1;" data-wa-url="https://wa.me/237697136203?text=Bonjour%20ECOPARK%20Ahala%2C%20voici%20ma%20reference%20ECP-2026-84920" onclick="openDopamineWhatsAppBridge()">
                      <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
                      Recevoir mon Pass &amp; Point GPS sur WhatsApp (1-Clic)
                    </button>
                  </div>
                </div>
""" + DOPAMINE_CARD_END


ADM_INBOX_HTML = ADM_INBOX_START + r"""
            <div class="adm-card" id="admLeadsInboxCard">
              <span id="sec-ADM-09"></span>
              <h3><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg> <span class="tech-code-tag">ADM-09 — </span>Inbox Unifiée des Leads &amp; Réservations (Statuts en 1 Clic)</h3>
              <p class="adm-lead">Centralisation en temps réel des 4 canaux d'acquisition (Billets QR, Devis Groupes B2B/Écoles, Rendez-vous Repérage/Mariage, Candidatures CFP MINEFOP) avec qualification en 1 clic et relance directe WhatsApp.</p>

              <div class="adm-kpis" id="admLeadsKpiBar" style="margin-bottom:14px;">
                <span class="adm-kpi">Total Dossiers Actifs : <b id="admLeadsTotalCount">0</b></span>
                <span class="adm-kpi">Nouveaux / En attente : <b id="admLeadsPendingCount">0</b></span>
                <span class="adm-kpi">Confirmés / Validés : <b id="admLeadsConfirmedCount">0</b></span>
                <span class="adm-kpi">Traités / Clôturés : <b id="admLeadsProcessedCount">0</b></span>
                <span class="adm-kpi">Volume Cumulé : <b id="admLeadsVolumeFcfa">0 FCFA</b></span>
              </div>

              <div class="adm-toolbar" style="justify-content:space-between;">
                <div class="adm-tabs" id="admLeadsChannelTabs" style="margin-bottom:0;">
                  <button type="button" data-lead-channel="ALL" class="active" onclick="filterAdmLeadsInbox('ALL', this)">Tous les canaux</button>
                  <button type="button" data-lead-channel="BOOKING" onclick="filterAdmLeadsInbox('BOOKING', this)">Billets QR &amp; Loges</button>
                  <button type="button" data-lead-channel="QUOTE" onclick="filterAdmLeadsInbox('QUOTE', this)">Devis B2B / Écoles</button>
                  <button type="button" data-lead-channel="RDV" onclick="filterAdmLeadsInbox('RDV', this)">Rendez-vous</button>
                  <button type="button" data-lead-channel="CFP" onclick="filterAdmLeadsInbox('CFP', this)">Candidatures CFP</button>
                </div>
                <input type="search" class="form-control" id="admLeadsSearchInput" placeholder="Filtrer par référence, nom, école, téléphone (+237)..." aria-label="Rechercher dans l'Inbox des Leads" oninput="renderAdmLeadsInbox()" style="max-width:300px;" />
              </div>

              <div class="table-responsive">
                <table class="adm-table" id="admLeadsTable">
                  <thead>
                    <tr>
                      <th>Référence &amp; Canal</th>
                      <th>Contact &amp; Téléphone (+237)</th>
                      <th>Détail de la Demande &amp; Date</th>
                      <th>Montant (FCFA)</th>
                      <th>Statut Actuel</th>
                      <th>Actions en 1 Clic</th>
                    </tr>
                  </thead>
                  <tbody id="admLeadsTableBody"></tbody>
                </table>
              </div>
            </div>
""" + ADM_INBOX_END


PHASE7_JS = PHASE7_JS_START + r"""
  // ==========================================================================
  // PHASE 7 : ORCHESTRATION MULTI-AGENTS 360° — CONTRAT JSON, ANTI-XSS,
  //           SOULAGEMENT DOPAMINERGIQUE WHATSAPP & INBOX LEADS 1-CLIC
  // ==========================================================================

  // --- 1. ASSAINISSEMENT ANTI-XSS & VALIDATION DU CONTRAT DE DONNÉES ---
  window.sanitizeEcoparkInput = function (raw) {
    if (raw === null || raw === undefined) return '';
    var s = String(raw);
    // Suppression des balises script et gestionnaires d'evenements inline
    s = s.replace(/<\s*script[^>]*>[\s\S]*?<\s*\/\s*script\s*>/gi, '');
    s = s.replace(/on[a-z]+\s*=\s*(['"][^'"]*['"]|[^\s>]+)/gi, '');
    s = s.replace(/javascript\s*:/gi, '');
    // Suppression de toutes les balises HTML (<...>) et chevrons
    s = s.replace(/<[^>]*>/g, '');
    s = s.replace(/[<>]/g, '');
    return s.trim();
  };

  window.validateEcoparkLeadContract = function (channel, payload) {
    var errors = [];
    if (!payload || typeof payload !== 'object') {
      return { valid: false, errors: ['Payload manquant ou invalide'] };
    }
    var ref = String(payload.reference || '');
    var phone = String(payload.phone || '');
    if (channel === 'BOOKING') {
      if (!/^ECP-2026-\d{5}$/.test(ref)) errors.push('Format reference Booking invalide');
      if (typeof payload.totalFcfa !== 'number' || payload.totalFcfa < 500) errors.push('Montant totalFcfa < 500 FCFA');
    } else if (channel === 'QUOTE') {
      if (!/^DEV-2026-\d{4}$/.test(ref)) errors.push('Format reference Quote invalide');
      if (typeof payload.pax !== 'number' || payload.pax < 10) errors.push('Effectif groupe < 10 participants');
    } else if (channel === 'RDV') {
      if (!/^RDV-2026-\d{4}$/.test(ref)) errors.push('Format reference RDV invalide');
    } else if (channel === 'CFP') {
      if (!/^CFP-2026-\d{4}$/.test(ref)) errors.push('Format reference CFP invalide');
    }
    if (channel === 'CFP' && payload.age !== undefined && (Number(payload.age) < 16 || Number(payload.age) > 65)) { errors.push('Age candidat CFP hors plage reglementaire MINEFOP (16-65 ans)'); }
    if (!phone || !isValidCameroonPhone(phone)) {
      errors.push('Numero Cameroun (+237) non conforme');
    }
    return { valid: errors.length === 0, errors: errors };
  };

  // --- 2. SOULAGEMENT DOPAMINERGIQUE POST-FORMULAIRE & PONT WHATSAPP 1-CLIC ---
  window._lastDopamineWhatsAppUrl = 'https://wa.me/237697136203?text=' + encodeURIComponent(
    'Bonjour ECOPARK CAMEROUN (Yaounde-Ahala), je souhaite recevoir mon Pass QR Coupe-File et le point GPS face station Tradex Ahala.'
  );

  window.triggerDopamineRelief = function (channel, data) {
    data = data || {};
    var ref = sanitizeEcoparkInput(data.reference || 'ECP-2026-84920');
    var name = sanitizeEcoparkInput(data.name || 'Visiteur ECOPARK');
    var amountTxt = data.amountFcfa ? formatFCFA(data.amountFcfa) : '';
    var title = '';
    var msg = '';
    var waLines = [];

    if (channel === 'BOOKING') {
      title = 'Place bloquée ! Votre Pass Coupe-File ' + ref + ' est actif.';
      msg = 'Titulaire : ' + name + ' • Total verrouillé : ' + (amountTxt || '14 000 FCFA') + '. Zéro attente au portail RN3 Ahala, utilisable hors-ligne et protégé par la Garantie Pluie 90 jours.';
      waLines = [
        'Bonjour ECOPARK CAMEROUN (Yaounde-Ahala),',
        'Mon Billet QR Coupe-File est genere :',
        '- Reference : ' + ref,
        '- Titulaire : ' + name,
        '- Prestations : ' + sanitizeEcoparkInput(data.summary || 'Visite & Loisirs'),
        '- Total : ' + (amountTxt || '14 000 FCFA'),
        'Merci de confirmer mon accueil prioritaire face station Tradex Ahala.'
      ];
    } else if (channel === 'QUOTE') {
      title = 'Proforma ' + ref + ' générée ! Tarif enfant 500 FCFA sanctuarisé.';
      msg = 'Organisation : ' + name + ' • Budget officiel : ' + (amountTxt || 'Sur mesure') + '. Notre équipe Exploitation réserve votre créneau et vos navettes.';
      waLines = [
        'Bonjour Service Groupes & B2B ECOPARK Ahala,',
        'Je viens de generer la Facture Proforma officielle :',
        '- Reference : ' + ref,
        '- Structure : ' + name,
        '- Formule : ' + sanitizeEcoparkInput(data.summary || 'Groupe / Seminaire'),
        '- Budget TTC : ' + (amountTxt || '67 500 FCFA'),
        'Merci de bloquer notre date et nos loges/salle Menkii Essomba Anton.'
      ];
    } else if (channel === 'RDV') {
      title = 'Rendez-vous ' + ref + ' confirmé avec notre équipe à Ahala !';
      msg = 'Visiteur : ' + name + ' • Créneau : ' + sanitizeEcoparkInput(data.summary || '11h00 - 12h00') + '. Accueil VIP réservé au portail face station Tradex.';
      waLines = [
        'Bonjour Direction ECOPARK Yaounde-Ahala,',
        'Je confirme mon Rendez-vous de reperage :',
        '- Reference : ' + ref,
        '- Contact : ' + name,
        '- Detail : ' + sanitizeEcoparkInput(data.summary || 'Reperage sur site'),
        'A tres bientot a Ahala Barriere (face station Tradex).'
      ];
    } else if (channel === 'CFP') {
      title = 'Dossier CFP ' + ref + ' enregistré ! Votre place en stage pratique est réservée.';
      msg = 'Candidat(e) : ' + name + ' • Filière agréée MINEFOP (' + sanitizeEcoparkInput(data.summary || '70% pratique') + '). Inscription 50 000 FCFA + 4 tranches.';
      waLines = [
        'Bonjour Campus CFP ECOPARK (Agree MINEFOP),',
        'Ma candidature est enregistree :',
        '- N Dossier : ' + ref,
        '- Candidat(e) : ' + name,
        '- Filiere & Echeancier : ' + sanitizeEcoparkInput(data.summary || 'Filiere CFP'),
        'Merci de m\'indiquer la procedure Mobile Money pour les 50 000 FCFA d\'inscription.'
      ];
    }

    var waUrl = 'https://wa.me/237697136203?text=' + encodeURIComponent(waLines.join('\n'));
    window._lastDopamineWhatsAppUrl = waUrl;

    var badgeEl = document.getElementById('dopamineReliefRefBadge');
    var titleEl = document.getElementById('dopamineReliefTitle');
    var msgEl = document.getElementById('dopamineReliefMessage');
    var btnEl = document.getElementById('btnDopamineWhatsAppBridge');

    if (badgeEl) badgeEl.textContent = ref;
    if (titleEl && title) titleEl.textContent = title;
    if (msgEl && msg) msgEl.textContent = msg;
    if (btnEl) btnEl.setAttribute('data-wa-url', waUrl);

    return { reference: ref, title: title, message: msg, whatsappUrl: waUrl };
  };

  window.openDopamineWhatsAppBridge = function () {
    var btnEl = document.getElementById('btnDopamineWhatsAppBridge');
    var url = (btnEl && btnEl.getAttribute('data-wa-url')) || window._lastDopamineWhatsAppUrl;
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
    return url;
  };

  // --- 3. INBOX UNIFIÉE DES LEADS & RÉSERVATIONS (STATUTS EN 1 CLIC — ADM-09) ---
  window._admLeadsActiveChannel = 'ALL';

  window.getUnifiedLeadsList = function () {
    var db = typeof loadDB === 'function' ? loadDB() : { bookings: [], quotes: [], cfpApplications: [], appointments: [] };
    var items = [];

    (db.bookings || []).forEach(function (b) {
      var normStatus = 'CONFIRMED';
      if (b.leadStatus === 'NEW' || b.leadStatus === 'CONFIRMED' || b.leadStatus === 'PROCESSED') normStatus = b.leadStatus;
      else if (b.scanned) normStatus = 'PROCESSED';
      else if (b.status === 'HELD_11H') normStatus = 'NEW';
      items.push({
        channel: 'BOOKING',
        channelLabel: 'Billet QR',
        reference: sanitizeEcoparkInput(b.reference || 'ECP-2026-00000'),
        contactName: sanitizeEcoparkInput(b.holder || 'Visiteur ECOPARK'),
        phone: sanitizeEcoparkInput(b.phone || '+237 697 13 62 03'),
        summary: sanitizeEcoparkInput((b.paxSummary || 'Visite Parc') + ' (' + (b.date || '') + ')'),
        amountFcfa: Number(b.totalFcfa) || 0,
        rawStatus: sanitizeEcoparkInput(b.scanned ? ('Scanne ' + (b.scannedAt || '')) : (b.status || 'CONFIRMED')),
        leadStatus: normStatus
      });
    });

    (db.quotes || []).forEach(function (q) {
      var st = String(q.status || '');
      var normStatus = q.leadStatus || (st.indexOf('Valid') !== -1 || st.indexOf('Confirm') !== -1 ? 'CONFIRMED' : (st.indexOf('Clotur') !== -1 || st.indexOf('Trait') !== -1 ? 'PROCESSED' : 'NEW'));
      items.push({
        channel: 'QUOTE',
        channelLabel: 'Devis B2B/École',
        reference: sanitizeEcoparkInput(q.reference || 'DEV-2026-0000'),
        contactName: sanitizeEcoparkInput(q.org || 'Organisation'),
        phone: sanitizeEcoparkInput(q.phone || '+237 697 13 62 03'),
        summary: sanitizeEcoparkInput((q.pax || 20) + ' pers. • ' + (q.type || 'Excursion') + ' (' + (q.date || '') + ')'),
        amountFcfa: Number(q.budgetFcfa) || 0,
        rawStatus: sanitizeEcoparkInput(q.status || 'Proforma generee'),
        leadStatus: normStatus
      });
    });

    (db.appointments || []).forEach(function (r) {
      var st = String(r.status || '');
      var normStatus = r.leadStatus || (st.indexOf('Trait') !== -1 ? 'PROCESSED' : (st.indexOf('Confirm') !== -1 ? 'CONFIRMED' : 'NEW'));
      items.push({
        channel: 'RDV',
        channelLabel: 'Rendez-vous',
        reference: sanitizeEcoparkInput(r.reference || 'RDV-2026-0000'),
        contactName: sanitizeEcoparkInput((r.visitorName || 'Visiteur') + (r.org ? ' (' + r.org + ')' : '')),
        phone: sanitizeEcoparkInput(r.phone || '+237 697 13 62 03'),
        summary: sanitizeEcoparkInput((r.purposeLabel || 'Reperage') + ' • ' + (r.date || '') + ' (' + (r.slot || '') + ')'),
        amountFcfa: 0,
        rawStatus: sanitizeEcoparkInput(r.status || 'Créneau réservé'),
        leadStatus: normStatus
      });
    });

    (db.cfpApplications || []).forEach(function (c) {
      var st = String(c.status || '');
      var normStatus = c.leadStatus || (st.indexOf('Admis') !== -1 ? 'CONFIRMED' : (st.indexOf('Trait') !== -1 ? 'PROCESSED' : 'NEW'));
      items.push({
        channel: 'CFP',
        channelLabel: 'Candidature CFP',
        reference: sanitizeEcoparkInput(c.reference || 'CFP-2026-0000'),
        contactName: sanitizeEcoparkInput(c.name || 'Candidat CFP'),
        phone: sanitizeEcoparkInput(c.phone || '+237 697 13 62 03'),
        summary: sanitizeEcoparkInput(c.track || 'Filiere MINEFOP'),
        amountFcfa: 300000,
        rawStatus: sanitizeEcoparkInput(c.status || 'Dossier recu'),
        leadStatus: normStatus
      });
    });

    return items;
  };

  window.filterAdmLeadsInbox = function (channel, btnEl) {
    window._admLeadsActiveChannel = channel || 'ALL';
    var tabs = document.querySelectorAll('#admLeadsChannelTabs button');
    tabs.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-lead-channel') === window._admLeadsActiveChannel);
    });
    if (btnEl) btnEl.classList.add('active');
    renderAdmLeadsInbox();
  };

  window.setLeadInboxStatus = function (channel, reference, newStatus) {
    var db = loadDB();
    var statusLabelMap = {
      NEW: 'En attente de traitement',
      CONFIRMED: 'Confirmé & Validé',
      PROCESSED: 'Traité & Clôturé'
    };
    var humanStatus = statusLabelMap[newStatus] || 'Confirmé & Validé';
    var updated = false;

    if (channel === 'BOOKING') {
      (db.bookings || []).forEach(function (b) {
        if (b.reference === reference) {
          b.leadStatus = newStatus;
          b.status = newStatus === 'NEW' ? 'HELD_11H' : 'CONFIRMED';
          if (newStatus === 'PROCESSED') {
            if (!b.scanned) {
              b.scanned = true;
              b.scannedAt = b.scannedAt || nowStamp();
              if (db.posStats && typeof db.posStats.validatedEntries === 'number') {
                db.posStats.validatedEntries += 1;
              }
            }
          } else if (b.scanned) {
            b.scanned = false;
            b.scannedAt = null;
            if (db.posStats && typeof db.posStats.validatedEntries === 'number') {
              db.posStats.validatedEntries = Math.max(0, db.posStats.validatedEntries - 1);
            }
          }
          updated = true;
        }
      });
    } else if (channel === 'QUOTE') {
      (db.quotes || []).forEach(function (q) {
        if (q.reference === reference) {
          q.leadStatus = newStatus;
          q.status = humanStatus;
          updated = true;
        }
      });
    } else if (channel === 'RDV') {
      if (typeof ensureAppointmentsArray === 'function') ensureAppointmentsArray(db);
      (db.appointments || []).forEach(function (r) {
        if (r.reference === reference) {
          r.leadStatus = newStatus;
          r.status = humanStatus;
          updated = true;
        }
      });
    } else if (channel === 'CFP') {
      (db.cfpApplications || []).forEach(function (c) {
        if (c.reference === reference) {
          c.leadStatus = newStatus;
          c.status = newStatus === 'CONFIRMED' ? 'Admis Rentrée (50 000 FCFA réglés)' : humanStatus;
          updated = true;
        }
      });
    }

    if (updated) {
      db.auditLogs = db.auditLogs || [];
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: 'Inbox Leads Back-Office (ADM-09)',
        action: 'Statut du dossier ' + reference + ' (' + channel + ') basculé en 1 clic vers : ' + humanStatus + '.'
      });
      saveDB(db);
      renderAdmLeadsInbox();
      showToastSprint1('Dossier ' + reference + ' mis à jour en 1 clic : ' + humanStatus);
    }
    return updated;
  };

  window.openLeadWhatsAppFollowup = function (reference) {
    var all = getUnifiedLeadsList();
    var item = all.find(function (x) { return x.reference === reference; });
    if (!item) return null;
    var cleanDigits = String(item.phone || '').replace(/[^0-9]/g, '');
    if (cleanDigits.length === 9) cleanDigits = '237' + cleanDigits;
    if (!cleanDigits) cleanDigits = '237697136203';
    var msg = 'Bonjour ' + item.contactName + ', ici la Conciergerie ECOPARK CAMEROUN (Yaoundé-Ahala). Concernant votre dossier ' + item.reference + ' (' + item.summary + '), votre statut est : ' + item.rawStatus + '.';
    var url = 'https://wa.me/' + cleanDigits + '?text=' + encodeURIComponent(msg);
    window.open(url, '_blank', 'noopener,noreferrer');
    return url;
  };

  window.renderAdmLeadsInbox = function () {
    var tbody = document.getElementById('admLeadsTableBody');
    if (!tbody) return;
    var all = getUnifiedLeadsList();

    var totalCount = all.length;
    var pendingCount = all.filter(function (x) { return x.leadStatus === 'NEW'; }).length;
    var confirmedCount = all.filter(function (x) { return x.leadStatus === 'CONFIRMED'; }).length;
    var processedCount = all.filter(function (x) { return x.leadStatus === 'PROCESSED'; }).length;
    var volumeFcfa = all.reduce(function (acc, x) { return acc + (x.amountFcfa || 0); }, 0);

    var elTot = document.getElementById('admLeadsTotalCount');
    var elPend = document.getElementById('admLeadsPendingCount');
    var elConf = document.getElementById('admLeadsConfirmedCount');
    var elProc = document.getElementById('admLeadsProcessedCount');
    var elVol = document.getElementById('admLeadsVolumeFcfa');

    if (elTot) elTot.textContent = String(totalCount);
    if (elPend) elPend.textContent = String(pendingCount);
    if (elConf) elConf.textContent = String(confirmedCount);
    if (elProc) elProc.textContent = String(processedCount);
    if (elVol) elVol.textContent = formatFCFA(volumeFcfa);

    var chFilter = window._admLeadsActiveChannel || 'ALL';
    var searchEl = document.getElementById('admLeadsSearchInput');
    var q = (searchEl && searchEl.value) ? searchEl.value.trim().toLowerCase() : '';

    var filtered = all.filter(function (item) {
      if (chFilter !== 'ALL' && item.channel !== chFilter) return false;
      if (q) {
        var hay = (item.reference + ' ' + item.contactName + ' ' + item.phone + ' ' + item.summary + ' ' + item.rawStatus).toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="adm-empty">Aucun dossier ne correspond aux critères sélectionnés.</td></tr>';
      return;
    }

    tbody.innerHTML = filtered.map(function (item) {
      var badgeClass = item.leadStatus === 'CONFIRMED'
        ? 'adm-badge-live'
        : (item.leadStatus === 'NEW' ? 'adm-badge-draft' : 'adm-badge-archived');
      var statusBadgeLabel = item.leadStatus === 'CONFIRMED'
        ? 'Confirmé'
        : (item.leadStatus === 'NEW' ? 'Nouveau / Attente' : 'Traité / Clôturé');

      var amountCell = item.amountFcfa > 0 ? ('<strong>' + formatFCFA(item.amountFcfa) + '</strong>') : '<span class="adm-sub">Sur place / Devis</span>';

      return '<tr data-lead-ref="' + escHtml(item.reference) + '" data-lead-channel="' + escHtml(item.channel) + '" data-lead-status="' + escHtml(item.leadStatus) + '">' +
        '<td><strong>' + escHtml(item.reference) + '</strong><div class="adm-sub">' + escHtml(item.channelLabel) + '</div></td>' +
        '<td><strong>' + escHtml(item.contactName) + '</strong><div class="adm-sub">' + escHtml(item.phone) + '</div></td>' +
        '<td>' + escHtml(item.summary) + '<div class="adm-sub">' + escHtml(item.rawStatus) + '</div></td>' +
        '<td class="adm-nowrap">' + amountCell + '</td>' +
        '<td><span class="adm-badge ' + badgeClass + '">' + escHtml(statusBadgeLabel) + '</span></td>' +
        '<td><div class="adm-actions">' +
          '<button type="button" class="adm-act ' + (item.leadStatus === 'NEW' ? 'adm-act-dup' : '') + '" onclick="setLeadInboxStatus(\'' + escHtml(item.channel) + '\', \'' + escHtml(item.reference) + '\', \'NEW\')">Attente</button>' +
          '<button type="button" class="adm-act ' + (item.leadStatus === 'CONFIRMED' ? 'adm-act-pub' : '') + '" onclick="setLeadInboxStatus(\'' + escHtml(item.channel) + '\', \'' + escHtml(item.reference) + '\', \'CONFIRMED\')">Confirmer</button>' +
          '<button type="button" class="adm-act" onclick="setLeadInboxStatus(\'' + escHtml(item.channel) + '\', \'' + escHtml(item.reference) + '\', \'PROCESSED\')">Clôturer</button>' +
          '<button type="button" class="adm-act adm-act-dup" onclick="openLeadWhatsAppFollowup(\'' + escHtml(item.reference) + '\')">WhatsApp</button>' +
        '</div></td>' +
      '</tr>';
    }).join('');
  };

  // --- 4. ENCAPSULATION DES SOUMISSIONS DE FORMULAIRES (ANTI-XSS + DOPAMINE + INBOX SYNC) ---
  (function wrapFormHandlersPhase7() {
    var FormFieldIds = [
      'visitorName', 'visitorPhone',
      'quoteOrgName', 'quotePhone',
      'cfpCandidateName', 'cfpPhone',
      'rdvVisitorName', 'rdvOrgName', 'rdvPhone', 'rescheduleReason', 'closureIncidentJustification'
    ];

    function sanitizeActiveFormFields() {
      FormFieldIds.forEach(function (id) {
        var el = document.getElementById(id);
        if (el && typeof el.value === 'string' && el.value) {
          el.value = sanitizeEcoparkInput(el.value);
        }
      });
    }

    var _origBooking = window.createLiveBookingSprint1;
    if (typeof _origBooking === 'function' && !_origBooking._phase7Wrapped) {
      window.createLiveBookingSprint1 = function () {
        sanitizeActiveFormFields();
        var res = _origBooking.apply(this, arguments);
        if (res) {
          var db = loadDB();
          var latest = db.bookings && db.bookings[0];
          if (latest) {
            latest.holder = sanitizeEcoparkInput(latest.holder);
            latest.phone = sanitizeEcoparkInput(latest.phone);
            saveDB(db);
            triggerDopamineRelief('BOOKING', {
              reference: latest.reference,
              name: latest.holder,
              summary: latest.paxSummary,
              amountFcfa: latest.totalFcfa
            });
          }
          renderAdmLeadsInbox();
        }
        return res;
      };
      window.createLiveBookingSprint1._phase7Wrapped = true;
    }

    var _origQuote = window.submitGroupQuoteSprint1;
    if (typeof _origQuote === 'function' && !_origQuote._phase7Wrapped) {
      window.submitGroupQuoteSprint1 = function () {
        sanitizeActiveFormFields();
        var ref = _origQuote.apply(this, arguments);
        if (ref) {
          var db = loadDB();
          var latest = db.quotes && db.quotes[0];
          if (latest) {
            latest.org = sanitizeEcoparkInput(latest.org);
            latest.phone = sanitizeEcoparkInput(latest.phone || '+237 697 13 62 03');
            saveDB(db);
            triggerDopamineRelief('QUOTE', {
              reference: latest.reference,
              name: latest.org,
              summary: latest.type,
              amountFcfa: latest.budgetFcfa
            });
          }
          renderAdmLeadsInbox();
        }
        return ref;
      };
      window.submitGroupQuoteSprint1._phase7Wrapped = true;
    }

    var _origWaQuote = window.sendWhatsAppQuoteSprint1;
    if (typeof _origWaQuote === 'function' && !_origWaQuote._phase7Wrapped) {
      window.sendWhatsAppQuoteSprint1 = function () {
        sanitizeActiveFormFields();
        var res = _origWaQuote.apply(this, arguments);
        var db = loadDB();
        var latest = db.quotes && db.quotes[0];
        if (latest) {
          latest.org = sanitizeEcoparkInput(latest.org);
          latest.phone = sanitizeEcoparkInput(latest.phone || '+237 697 13 62 03');
          saveDB(db);
          triggerDopamineRelief('QUOTE', {
            reference: latest.reference,
            name: latest.org,
            summary: latest.type,
            amountFcfa: latest.budgetFcfa
          });
        }
        renderAdmLeadsInbox();
        return res;
      };
      window.sendWhatsAppQuoteSprint1._phase7Wrapped = true;
    }

    var _origCfp = window.submitCfpApplicationSprint1;
    if (typeof _origCfp === 'function' && !_origCfp._phase7Wrapped) {
      window.submitCfpApplicationSprint1 = function () {
        sanitizeActiveFormFields();
        var ref = _origCfp.apply(this, arguments);
        if (ref) {
          var db = loadDB();
          var latest = db.cfpApplications && db.cfpApplications[0];
          if (latest) {
            latest.name = sanitizeEcoparkInput(latest.name);
            latest.phone = sanitizeEcoparkInput(latest.phone);
            saveDB(db);
            triggerDopamineRelief('CFP', {
              reference: latest.reference,
              name: latest.name,
              summary: latest.track,
              amountFcfa: 50000
            });
          }
          renderAdmLeadsInbox();
        }
        return ref;
      };
      window.submitCfpApplicationSprint1._phase7Wrapped = true;
    }

    var _origRdv = window.submitRdvSprint1;
    if (typeof _origRdv === 'function' && !_origRdv._phase7Wrapped) {
      window.submitRdvSprint1 = function () {
        sanitizeActiveFormFields();
        var ref = _origRdv.apply(this, arguments);
        if (ref) {
          var db = loadDB();
          var latest = db.appointments && db.appointments[0];
          if (latest) {
            latest.visitorName = sanitizeEcoparkInput(latest.visitorName);
            latest.org = sanitizeEcoparkInput(latest.org);
            latest.phone = sanitizeEcoparkInput(latest.phone);
            saveDB(db);
            triggerDopamineRelief('RDV', {
              reference: latest.reference,
              name: latest.visitorName,
              summary: (latest.purposeLabel || '') + ' (' + (latest.date || '') + ' ' + (latest.slot || '') + ')'
            });
          }
          renderAdmLeadsInbox();
        }
        return ref;
      };
      window.submitRdvSprint1._phase7Wrapped = true;
    }

    var _origReschedule = window.confirmRescheduleSprint1;
    if (typeof _origReschedule === 'function' && !_origReschedule._phase7Wrapped) {
      window.confirmRescheduleSprint1 = function () {
        sanitizeActiveFormFields();
        var dateEl = document.getElementById('rescheduleNewDate');
        if (dateEl && typeof window.validateDateChoice === 'function') {
          window.validateDateChoice(dateEl);
        }
        var r = _origReschedule.apply(this, arguments);
        if (typeof renderAdmLeadsInbox === 'function') renderAdmLeadsInbox();
        return r;
      };
      window.confirmRescheduleSprint1._phase7Wrapped = true;
    }

    var _origSync = window.syncAllViewsFromDB;
    if (typeof _origSync === 'function' && !_origSync._phase7Wrapped) {
      window.syncAllViewsFromDB = function () {
        var r = _origSync.apply(this, arguments);
        if (typeof renderAdmLeadsInbox === 'function') renderAdmLeadsInbox();
        return r;
      };
      window.syncAllViewsFromDB._phase7Wrapped = true;
    }
  })();

  document.addEventListener('DOMContentLoaded', function () {
    renderAdmLeadsInbox();
  });
  renderAdmLeadsInbox();
""" + PHASE7_JS_END


def upsert_block(html: str, start_marker: str, end_marker: str, block: str, anchor: str, before: bool = True) -> str:
    pattern = re.compile(re.escape(start_marker) + r"[\s\S]*?" + re.escape(end_marker))
    if pattern.search(html):
        return pattern.sub(lambda _: block, html)
    if anchor not in html:
        raise RuntimeError(f"Anchor not found for {start_marker}: {anchor[:80]}")
    if before:
        return html.replace(anchor, block + "\n" + anchor, 1)
    else:
        return html.replace(anchor, anchor + "\n" + block, 1)


def main():
    src = TARGETS[0]
    html = src.read_text(encoding="utf-8")

    # 1. Inject Schema.org JSON-LD before <link rel="preconnect" href="https://fonts.googleapis.com">
    html = upsert_block(
        html,
        SCHEMA_START,
        SCHEMA_END,
        SCHEMA_JSONLD_HTML,
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        before=True,
    )

    # 2. Inject Hero Loss-Aversion Anchor right before <div class="grid-12" style="gap:12px;"> in #sec-PUB-01
    hero_kpi_anchor = '<div class="grid-12" style="gap:12px;">\n                  <div class="col-4 card hero-kpi-sync-card kpi-active-sync" id="heroKpiCard0"'
    if hero_kpi_anchor not in html:
        hero_kpi_anchor = '<div class="grid-12" style="gap:12px;">\r\n                  <div class="col-4 card hero-kpi-sync-card kpi-active-sync" id="heroKpiCard0"'
    html = upsert_block(
        html,
        HERO_ANCHOR_START,
        HERO_ANCHOR_END,
        HERO_ANCHOR_HTML,
        hero_kpi_anchor,
        before=True,
    )

    # 3. Inject Dopamine Relief Card right before <details class="clean-details-accordion" id="waConciergeAccordion">
    html = upsert_block(
        html,
        DOPAMINE_CARD_START,
        DOPAMINE_CARD_END,
        DOPAMINE_CARD_HTML,
        '<details class="clean-details-accordion" id="waConciergeAccordion">',
        before=True,
    )

    # 4. Inject Admin Unified Leads Inbox right before <div class="adm-card" id="sec-ADM-08">
    html = upsert_block(
        html,
        ADM_INBOX_START,
        ADM_INBOX_END,
        ADM_INBOX_HTML,
        '<div class="adm-card" id="sec-ADM-08">',
        before=True,
    )

    # 5. Inject Phase 7 JS right before </script>\n</body>
    script_end_anchor = "</script>\n</body>"
    if script_end_anchor not in html:
        script_end_anchor = "</script>\r\n</body>"
    html = upsert_block(
        html,
        PHASE7_JS_START,
        PHASE7_JS_END,
        PHASE7_JS,
        script_end_anchor,
        before=True,
    )

    # 6. Verify 0 character > U+25FF invariant
    high_chars = [ch for ch in html if ord(ch) > 0x25FF]
    if high_chars:
        raise RuntimeError(f"Detected {len(high_chars)} characters > U+25FF: {set(high_chars)}")

    # 7. Write identically to both target files
    for target in TARGETS:
        target.write_text(html, encoding="utf-8", newline="\n")
        print(f"[OK] Updated {target.relative_to(ROOT)} ({len(html):,} chars, 0 chars > U+25FF)")


if __name__ == "__main__":
    main()
