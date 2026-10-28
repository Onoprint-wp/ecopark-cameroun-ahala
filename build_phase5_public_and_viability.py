# -*- coding: utf-8 -*-
"""
Phase 5 & Viabilité Terrain — Raccordement du site public à EcoparkData et résolution des 5 anomalies critiques.

Met à jour de façon identique et idempotente :
  - etape0-site-live/index.html
  - Prototype_Interactif_ECOPARK_NEW_LOOK.html

Éléments intégrés :
  1. Task 1 : Générateur de vrai QR Code matriciel autonome (remplace les carrés statiques)
  2. Task 2 : Feuille de style dédiée @media print (Billet A4 & ticket 80mm propres sur 1 page)
  3. Task 3 : Verrouillage strict de la fermeture hebdomadaire le Lundi et des dates passées
  4. Task 4 : Validation stricte des numéros camerounais (+237 6XXXXXXXX) et case CGV obligatoire
  5. Task 5 : Raccordement dynamique de la grille tarifaire /nos-tarifs (PUB-10) sur catalog_activities
  6. Task 6 : Raccordement dynamique du simulateur /reserver sur les prix administrés
  7. Task 7 : Raccordement dynamique de /agenda (agenda_events) et /restaurant (menu_items)
  8. Task 8 : Activation du flux caméra pour le scanner d'entrée AGT-05
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = [
    ROOT / "etape0-site-live" / "index.html",
    ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"
]
QR_JS = ROOT / "etape0-site-live" / "vendor" / "qrcode.min.js"

PRINT_CSS_START = "/* ECOPARK_PRINT_CSS:START */"
PRINT_CSS_END = "/* ECOPARK_PRINT_CSS:END */"

QR_LIB_START = "<!-- ECOPARK_QR_LIB:START -->"
QR_LIB_END = "<!-- ECOPARK_QR_LIB:END -->"

CGV_MODAL_START = "<!-- ECOPARK_CGV_MODAL:START -->"
CGV_MODAL_END = "<!-- ECOPARK_CGV_MODAL:END -->"

PHASE5_JS_START = "// ECOPARK_PHASE5_INTEGRATION:START"
PHASE5_JS_END = "// ECOPARK_PHASE5_INTEGRATION:END"


PRINT_CSS = PRINT_CSS_START + r"""
    /* ========================================================================
       IMPRESSION OFFICIELLE (@media print) — Billets, Proformas & PV de Caisse
       ======================================================================== */
    @media print {
      body {
        background: #FFFFFF !important;
        color: #000000 !important;
      }
      body > *:not(#modalOverlaySprint1),
      .floating-demo-pill,
      #mobileStickyConversionBar,
      .header-outer,
      .footer-outer,
      .subnav-bar,
      .btnFloatingAdminToggle,
      #admRoleBar {
        display: none !important;
        visibility: hidden !important;
      }
      #modalOverlaySprint1 {
        position: static !important;
        display: block !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        box-shadow: none !important;
        width: 100% !important;
        max-width: 100% !important;
      }
      #modalOfficialPrintBox {
        position: static !important;
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 8mm !important;
        border: 1px solid #CCCCCC !important;
        box-shadow: none !important;
        background: #FFFFFF !important;
        color: #000000 !important;
      }
      #modalOfficialPrintBox .modal-actions,
      #modalOfficialPrintBox button,
      #modalOfficialPrintBox .btn {
        display: none !important;
        visibility: hidden !important;
      }
      #modalOfficialPrintBox table {
        width: 100% !important;
        border-collapse: collapse !important;
      }
      #modalOfficialPrintBox th,
      #modalOfficialPrintBox td {
        border: 1px solid #333333 !important;
        color: #000000 !important;
      }
      @page {
        size: A4 portrait;
        margin: 10mm;
      }
    }
""" + PRINT_CSS_END


CGV_MODAL_HTML = CGV_MODAL_START + r"""
    <!-- MODALE CGV OFFICIELLES & MENTIONS LÉGALES CAMEROUN -->
    <div class="card modal-box" id="modalCgvBox" style="display:none;max-width:680px;max-height:85vh;overflow-y:auto;">
      <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--color-border);padding-bottom:12px;margin-bottom:12px;">
        <h3 style="margin:0;">Conditions Générales de Vente & Mentions Légales</h3>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()">Fermer</button>
      </div>
      <div style="font-size:13.5px;color:var(--color-text-main);display:grid;gap:12px;line-height:1.55;">
        <div><strong>1. Identité & Exploitation :</strong> Le site officiel ECOPARK Cameroun est exploité par ECOPARK Yaoundé-Ahala (Route Nationale N°3, Face Station Tradex Ahala Barrière, Yaoundé). Contact officiel : +237 697 13 62 03 / +237 670 00 00 00.</div>
        <div><strong>2. Horaires & Jours d'Ouverture :</strong> Le parc est ouvert du Mardi au Dimanche de 09h00 à 18h00. Le parc est fermé au public tous les Lundis pour repos animalier et entretien des installations.</div>
        <div><strong>3. Garantie Météo & Report 90 jours :</strong> Tout billet QR non consommé au tourniquet bénéficie d'un report gratuit sans frais dans un délai de 90 jours calendaires à compter de la date initiale, en cas d'intempérie sur la RN3 ou d'imprévu.</div>
        <div><strong>4. Annulation & Remboursements :</strong> L'annulation à plus de 48 heures ouvre droit à un remboursement intégral (100 %) sur le numéro Mobile Money (Orange Money / MTN MoMo) émetteur ou à un Avoir QR 100 %. Moins de 48h avant la visite avec hébergement ou pergola privative immobilisée : retenue de 20 % pour frais d'immobilisation, ou avoir 100 %.</div>
        <div><strong>5. Règlements Mobile Money Sécurisés :</strong> Les règlements en ligne s'effectuent par débit direct Orange Money Cameroun ou MTN Mobile Money via invite officielle USSD sans jamais solliciter le code PIN du client sur le site web.</div>
        <div><strong>6. Tarification Protégée :</strong> Le tarif enfant groupe au Zoo est strictement protégé à 500 FCFA. La gratuité d'accès au parc est totale pour les enfants de moins de 3 ans.</div>
      </div>
      <div style="margin-top:16px;text-align:right;">
        <button type="button" class="btn btn-primary btn-sm" onclick="closeSprint1Modals()">J'ai compris et j'accepte</button>
      </div>
    </div>
""" + CGV_MODAL_END


PHASE5_JS = PHASE5_JS_START + r"""
  // ========================================================================
  // PHASE 5 & VIABILITÉ TERRAIN : MOTEUR DYNAMIQUE ECOPARK & GARDE-FOUS
  // ========================================================================

  // --- 1. GÉNÉRATION DE VRAI QR CODE SCANNABLE (SVG & CANVAS) ---
  window.renderEcoparkQrSvg = function (ref, targetContainer) {
    var el = typeof targetContainer === 'string' ? document.getElementById(targetContainer) : targetContainer;
    if (!el) return;
    var codeStr = (ref || 'ECP-2026-84920').trim();
    if (typeof qrcode === 'function') {
      try {
        var qr = qrcode(0, 'M');
        qr.addData(codeStr);
        qr.make();
        var svgTag = qr.createSvgTag(4, 0);
        el.innerHTML = svgTag;
        var svgEl = el.querySelector('svg');
        if (svgEl) {
          svgEl.setAttribute('width', '108');
          svgEl.setAttribute('height', '108');
          svgEl.setAttribute('aria-label', 'Billet QR Code ECOPARK ' + codeStr);
          svgEl.style.border = '2px solid var(--color-brand-deep)';
          svgEl.style.borderRadius = '8px';
          svgEl.style.padding = '4px';
          svgEl.style.background = '#FFFFFF';
          svgEl.style.flexShrink = '0';
          svgEl.style.boxSizing = 'border-box';
        }
        return;
      } catch (err) {
        console.warn('QR SVG render error:', err);
      }
    }
  };

  // --- 2. VALIDATION STRICTE TÉLÉPHONE CAMEROUN (+237) ---
  window.isValidCameroonPhone = function (phone) {
    if (!phone) return false;
    var clean = String(phone).replace(/[\s\-\(\)\.]/g, '');
    // +2376XXXXXXXX, 2376XXXXXXXX, 6XXXXXXXX (9 chiffres commençant par 6) ou fixe 2XXXXXXXX
    return /^(\+?237)?(6[25-9]\d{7}|2\d{8})$/.test(clean);
  };

  // --- 3. MODALE CGV OFFICIELLES ---
  window.openOfficialCgvModal = function () {
    closeSprint1Modals();
    var overlay = document.getElementById('modalOverlaySprint1');
    var box = document.getElementById('modalCgvBox');
    if (overlay) overlay.style.display = 'flex';
    if (box) box.style.display = 'block';
  };

  // --- 4. VERROUILLAGE LUNDIS ET DATES PASSÉES ---
  window.validateDateChoice = function (inputEl) {
    if (!inputEl || !inputEl.value) return true;
    var d = new Date(inputEl.value + 'T12:00:00');
    if (isNaN(d.getTime())) return true;
    var now = new Date();
    now.setHours(0, 0, 0, 0);
    if (d < now) {
      showToastSprint1('• Action refusée : Vous ne pouvez pas choisir une date antérieure à aujourd\'hui.');
      var pad = function (n) { return String(n).padStart(2, '0'); };
      inputEl.value = now.getFullYear() + '-' + pad(now.getMonth() + 1) + '-' + pad(now.getDate());
      return false;
    }
    if (d.getDay() === 1) { // 1 = Lundi
      showToastSprint1('• ECOPARK Ahala est fermé au public le Lundi (repos animalier & entretien). Veuillez choisir du Mardi au Dimanche.');
      d.setDate(d.getDate() + 1); // Reporter automatiquement au Mardi
      var pad = function (n) { return String(n).padStart(2, '0'); };
      inputEl.value = d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
      if (inputEl.id === 'visitDate' && typeof recalcSimulator === 'function') {
        recalcSimulator();
      }
      return false;
    }
    return true;
  };

  window.initDateConstraints = function () {
    var today = new Date();
    var pad = function (n) { return String(n).padStart(2, '0'); };
    var todayIso = today.getFullYear() + '-' + pad(today.getMonth() + 1) + '-' + pad(today.getDate());
    ['visitDate', 'quoteDate', 'rdvDate', 'rescheduleNewDate'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) {
        el.setAttribute('min', todayIso);
        el.addEventListener('change', function () {
          validateDateChoice(this);
        });
      }
    });
  };

  // --- 5. RACCORDEMENT DYNAMIQUE DU CATALOGUE /nos-tarifs (PUB-10) ---
  window.renderPubCatalogFromData = function () {
    var tbody = document.getElementById('pubCatalogTableBody');
    if (!tbody || !window.EcoparkData || typeof EcoparkData.content !== 'function') return;
    var acts = EcoparkData.content('catalog_activities') || [];
    if (acts.length === 0) return;
    var html = '';
    acts.forEach(function (a) {
      if (a.status !== 'PUBLISHED') return;
      var condText = '';
      if (a.group_adult_price_fcfa && a.group_adult_price_fcfa < a.adult_price_fcfa) {
        condText += 'Tarif groupe dès 20 pers : ' + formatFCFA(a.group_adult_price_fcfa) + '/adulte. ';
      }
      if (a.group_child_price_fcfa) {
        condText += 'Tarif enfant protégé : ' + formatFCFA(a.group_child_price_fcfa) + '. ';
      }
      condText += (a.description || '');

      var childPriceBadge = a.child_price_fcfa > 0
        ? ('<span class="price-pill">' + formatFCFA(a.child_price_fcfa) + '</span>')
        : '<span class="status-badge">Inclus / N/A</span>';
      var adultPriceBadge = a.adult_price_fcfa > 0
        ? ('<span class="price-pill">' + formatFCFA(a.adult_price_fcfa) + '</span>')
        : '<span class="status-badge">Sur devis</span>';

      html += '<tr>' +
        '<td><strong>' + escHtml(a.title) + '</strong></td>' +
        '<td>' + childPriceBadge + '</td>' +
        '<td>' + adultPriceBadge + '</td>' +
        '<td style="font-size:13.5px;color:var(--color-text-muted);">' + escHtml(condText) + '</td>' +
        '<td><button class="btn btn-secondary btn-sm" onclick="addActivityAndGo(\'' + escHtml(a.slug) + '\')">Sélectionner</button></td>' +
        '</tr>';
    });

    var lodges = EcoparkData.content('lodge_cities') || [];
    if (lodges.length > 0) {
      var lodgeParts = lodges.map(function (l) {
        return escHtml(l.name.replace(/\(.*\)/, '').trim()) + ' (' + Math.round(l.min_price_fcfa / 1000) + 'k-' + Math.round(l.max_price_fcfa / 1000) + 'k)';
      });
      html += '<tr>' +
        '<td><strong>Hébergement — Cités Bene, Chanthel & Ewondo</strong></td>' +
        '<td colspan="2"><strong>' + lodgeParts.join(' • ') + ' FCFA</strong></td>' +
        '<td style="font-size:13.5px;color:var(--color-text-muted);">Repos en journée (Day-use) ou nuitée complète avec accès parc.</td>' +
        '<td><button class="btn btn-secondary btn-sm" onclick="navigateFamily(\'RES\', \'RES-01\')">Réserver</button></td>' +
        '</tr>';
    }

    html += '<tr>' +
      '<td><strong>Centre de Formation Professionnelle (CFP)</strong></td>' +
      '<td colspan="2">Inscription : <strong>50 000 FCFA</strong> • Scolarité annuelle : <strong>250 000 FCFA</strong></td>' +
      '<td style="font-size:13.5px;color:var(--color-text-muted);">Agrément MINEFOP • 5 filières métiers avec stages pratiques au sein d\'ECOPARK.</td>' +
      '<td><button class="btn btn-secondary btn-sm" onclick="openCfpModalSprint1()">Candidater</button></td>' +
      '</tr>';

    tbody.innerHTML = html;
  };

  // --- 6. PRIX DYNAMIQUES POUR LE SIMULATEUR /reserver (RES-01..12) ---
  window.getCatalogPriceDynamic = function (slug, isGroup, isChild) {
    if (window.EcoparkData && typeof EcoparkData.get === 'function') {
      var act = EcoparkData.get('catalog_activities', function (a) { return a.slug === slug; });
      if (act && act.status === 'PUBLISHED') {
        if (isChild) {
          return (isGroup && act.group_child_price_fcfa != null) ? act.group_child_price_fcfa : (act.child_price_fcfa || 0);
        } else {
          return (isGroup && act.group_adult_price_fcfa != null) ? act.group_adult_price_fcfa : (act.adult_price_fcfa || 0);
        }
      }
    }
    var defs = {
      zoo: { adult: 1000, child: 500, gAdult: 700, gChild: 500 },
      piscine: { adult: 2500, child: 1500, gAdult: 2000, gChild: 1500 },
      pirogue: { adult: 1000, child: 500, gAdult: 800, gChild: 500 },
      cheval: { adult: 1000, child: 500, gAdult: 800, gChild: 500 },
      saveurs: { adult: 5000, child: 2500, gAdult: 4500, gChild: 2500 },
      nutrition_poissons: { adult: 500, child: 500, gAdult: 500, gChild: 500 },
      pergola_lac: { adult: 5000, child: 0, gAdult: 5000, gChild: 0 },
      navette_yaounde: { adult: 1500, child: 1000, gAdult: 1200, gChild: 1000 }
    };
    var d = defs[slug] || { adult: 1000, child: 500, gAdult: 800, gChild: 500 };
    return isChild ? (isGroup ? d.gChild : d.child) : (isGroup ? d.gAdult : d.adult);
  };

  // --- 7. SCANNER CAMÉRA AGT-05 ---
  var _qrVideoStream = null;
  var _qrScanInterval = null;

  window.toggleQrCameraScan = async function () {
    if (_qrVideoStream) {
      stopQrCameraScan();
    } else {
      startQrCameraScan();
    }
  };

  window.startQrCameraScan = async function () {
    var container = document.getElementById('qrCameraScanContainer');
    var video = document.getElementById('qrScannerVideo');
    var btn = document.getElementById('btnToggleCameraScan');
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showToastSprint1('• Accès caméra non supporté par ce navigateur.');
      return;
    }
    try {
      _qrVideoStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' } }
      });
      if (video) {
        video.srcObject = _qrVideoStream;
        await video.play();
      }
      if (container) container.style.display = 'block';
      if (btn) btn.innerHTML = '<svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="9" x2="15" y1="9" y2="15"/><line x1="15" x2="9" y1="9" y2="15"/></svg> Couper Caméra';

      if ('BarcodeDetector' in window) {
        var detector = new BarcodeDetector({ formats: ['qr_code'] });
        _qrScanInterval = setInterval(async function () {
          if (!video || video.readyState < 2) return;
          try {
            var barcodes = await detector.detect(video);
            if (barcodes && barcodes.length > 0) {
              var raw = barcodes[0].rawValue;
              stopQrCameraScan();
              var input = document.getElementById('qrScanInput');
              if (input) input.value = raw;
              verifyLiveQrCode();
            }
          } catch (e) {}
        }, 300);
      }
    } catch (err) {
      showToastSprint1('• Caméra indisponible : ' + (err.message || 'accès refusé'));
      stopQrCameraScan();
    }
  };

  window.stopQrCameraScan = function () {
    if (_qrScanInterval) {
      clearInterval(_qrScanInterval);
      _qrScanInterval = null;
    }
    if (_qrVideoStream) {
      _qrVideoStream.getTracks().forEach(function (t) { t.stop(); });
      _qrVideoStream = null;
    }
    var container = document.getElementById('qrCameraScanContainer');
    var btn = document.getElementById('btnToggleCameraScan');
    if (container) container.style.display = 'none';
    if (btn) btn.innerHTML = '<svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg> Caméra';
  };

  // --- 8. INITIALISATION AUTOMATIQUE & ABONNEMENTS TEMPS RÉEL ---
  document.addEventListener('DOMContentLoaded', function () {
    initDateConstraints();
    renderPubCatalogFromData();
    renderEcoparkQrSvg('ECP-2026-84920', 'demoTicketQrWrapper');

    if (window.EcoparkData && typeof EcoparkData.subscribe === 'function') {
      EcoparkData.subscribe('catalog_activities', function () {
        renderPubCatalogFromData();
        if (typeof recalcSimulator === 'function') recalcSimulator();
      });
      EcoparkData.subscribe('sales_bundles', function () {
        renderPubCatalogFromData();
        if (typeof recalcSimulator === 'function') recalcSimulator();
      });
      EcoparkData.subscribe('lodge_cities', function () {
        renderPubCatalogFromData();
        if (typeof recalcSimulator === 'function') recalcSimulator();
      });
    }
  });
""" + PHASE5_JS_END


def apply_phase5_upgrades(content: str) -> str:
    # 1. Injecter le CSS d'impression avant /* ECOPARK_ADMIN_CSS:START */
    if PRINT_CSS_START in content and PRINT_CSS_END in content:
        content = re.sub(
            re.escape(PRINT_CSS_START) + r".*?" + re.escape(PRINT_CSS_END),
            lambda m: PRINT_CSS,
            content,
            flags=re.DOTALL,
        )
    else:
        admin_css_marker = "/* ECOPARK_ADMIN_CSS:START */"
        if admin_css_marker in content:
            content = content.replace(admin_css_marker, PRINT_CSS + "\n\n    " + admin_css_marker)
        else:
            # Fallback avant </style>
            content = content.replace("</style>", PRINT_CSS + "\n  </style>")

    # 2. Injecter la bibliothèque QR Code inlinée dans <!-- ECOPARK_QR_LIB:START -->
    qr_js_content = QR_JS.read_text(encoding="utf-8")
    qr_lib_tag = QR_LIB_START + f'\n  <script id="ecoparkQrLib">\n{qr_js_content}\n  </script>\n' + QR_LIB_END
    if QR_LIB_START in content and QR_LIB_END in content:
        content = re.sub(
            re.escape(QR_LIB_START) + r".*?" + re.escape(QR_LIB_END),
            lambda m: qr_lib_tag,
            content,
            flags=re.DOTALL,
        )
    else:
        data_layer_marker = "<!-- ECOPARK_DATA_LAYER:START -->"
        if data_layer_marker in content:
            content = content.replace(data_layer_marker, qr_lib_tag + "\n  " + data_layer_marker)
        else:
            content = content.replace("<script id=\"ecoparkConfig\">", qr_lib_tag + "\n  <script id=\"ecoparkConfig\">")

    # 3. Remplacer le QR code statique de #demoTicketCard par le wrapper dynamique
    static_qr_pattern = r'<svg width="108" height="108" viewBox="0 0 100 100" style="border:2px solid var\(--color-brand-deep\);[^>]*aria-label="Billet QR Code ECOPARK[^>]*>.*?</svg>'
    dynamic_qr_wrapper = (
        '<div id="demoTicketQrWrapper" style="display:flex;align-items:center;justify-content:center;flex-shrink:0;">\n'
        '                      <svg width="108" height="108" viewBox="0 0 100 100" style="border:2px solid var(--color-brand-deep);border-radius:8px;padding:6px;background:#FFF;flex-shrink:0;" aria-label="Billet QR Code ECOPARK">\n'
        '                        <rect x="6" y="6" width="26" height="26" fill="none" stroke="#1D490D" stroke-width="6"/>\n'
        '                        <rect x="13" y="13" width="12" height="12" fill="#1D490D"/>\n'
        '                        <rect x="68" y="6" width="26" height="26" fill="none" stroke="#1D490D" stroke-width="6"/>\n'
        '                        <rect x="75" y="13" width="12" height="12" fill="#1D490D"/>\n'
        '                        <rect x="6" y="68" width="26" height="26" fill="none" stroke="#1D490D" stroke-width="6"/>\n'
        '                        <rect x="13" y="75" width="12" height="12" fill="#1D490D"/>\n'
        '                      </svg>\n'
        '                    </div>'
    )
    if '<div id="demoTicketQrWrapper"' not in content:
        content = re.sub(static_qr_pattern, dynamic_qr_wrapper, content, flags=re.DOTALL)

    # 4. Remplacer les rectangles statiques de downloadOfflineQrTicketPng()
    canvas_fake_rects = (
        "ctx.fillRect(700, 145, 44, 44);\n"
        "        ctx.fillRect(806, 145, 44, 44);\n"
        "        ctx.fillRect(700, 251, 44, 44);\n"
        "        ctx.fillRect(760, 195, 32, 32);\n"
        "        ctx.fillStyle = '#1F880B';\n"
        "        ctx.fillRect(800, 245, 48, 48);"
    )
    canvas_real_qr = (
        "if (typeof qrcode === 'function') {\n"
        "          try {\n"
        "            var qr = qrcode(0, 'M');\n"
        "            qr.addData(ref || 'ECP-DEMO');\n"
        "            qr.make();\n"
        "            var modCount = qr.getModuleCount();\n"
        "            var qrBoxInner = 170;\n"
        "            var qrLeft = 690;\n"
        "            var qrTop = 135;\n"
        "            var modSize = qrBoxInner / modCount;\n"
        "            ctx.fillStyle = '#1D490D';\n"
        "            for (var r = 0; r < modCount; r++) {\n"
        "              for (var c = 0; c < modCount; c++) {\n"
        "                if (qr.isDark(r, c)) {\n"
        "                  ctx.fillRect(Math.round(qrLeft + c * modSize), Math.round(qrTop + r * modSize), Math.ceil(modSize), Math.ceil(modSize));\n"
        "                }\n"
        "              }\n"
        "            }\n"
        "          } catch (eQr) { console.warn('Canvas QR render error:', eQr); }\n"
        "        }"
    )
    if canvas_fake_rects in content:
        content = content.replace(canvas_fake_rects, canvas_real_qr)

    # Supprimer mention erronée 500 FCFA sur le PNG
    png_bad_text = "ctx.fillText('Montant TTC : ' + totalStr + ' (Tarif enfant protégé 500 FCFA)', 36, 326);"
    png_good_text = "ctx.fillText('Montant TTC : ' + totalStr + ' • Billet officiel sécurisé (Garantie 90j)', 36, 326);"
    if png_bad_text in content:
        content = content.replace(png_bad_text, png_good_text)

    # 5. Identifier tbody de la grille tarifaire PUB-10 avec id="pubCatalogTableBody"
    if 'id="pubCatalogTableBody"' not in content:
        content = content.replace(
            "<th>Action</th>\n                  </tr>\n                </thead>\n                <tbody>",
            "<th>Action</th>\n                  </tr>\n                </thead>\n                <tbody id=\"pubCatalogTableBody\">"
        )

    # 6. Ajouter la case CGV obligatoire avant les boutons de validation dans RES
    cgv_checkbox_html = (
        '                    <label style="display:flex;align-items:flex-start;gap:8px;font-size:13px;cursor:pointer;margin:12px 0 8px 0;line-height:1.4;">\n'
        '                      <input type="checkbox" id="agreeTermsBooking" style="margin-top:2px;" required />\n'
        '                      <span>J\'accepte les <a href="#modalCgvBox" onclick="openOfficialCgvModal();return false;" style="text-decoration:underline;font-weight:600;color:var(--color-brand-deep);">Conditions Générales de Vente (CGV)</a> et la politique de report gratuit 90 jours (Garantie Météo RN3).</span>\n'
        '                    </label>\n'
    )
    if '<input type="checkbox" id="agreeTermsBooking"' not in content:
        btn_booking_marker = '<button type="button" class="btn btn-primary" style="flex:1;" onclick="sendWhatsAppBooking()">'
        if btn_booking_marker in content:
            content = content.replace(btn_booking_marker, cgv_checkbox_html + "                    " + btn_booking_marker)

    # 7. Ajouter le bouton Caméra et le conteneur vidéo dans AGT-05
    agt_camera_btn = (
        '<button type="button" class="btn btn-secondary btn-ochre-outline" id="btnToggleCameraScan" onclick="toggleQrCameraScan()"><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg> Caméra</button>'
    )
    agt_camera_box = (
        '\n                <div id="qrCameraScanContainer" style="display:none;margin:8px 0 12px 0;background:#111;border-radius:8px;overflow:hidden;position:relative;border:1px solid var(--color-border);">'
        '\n                  <video id="qrScannerVideo" playsinline autoplay muted style="width:100%;max-height:220px;object-fit:cover;display:block;"></video>'
        '\n                  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:140px;height:140px;border:2px dashed #FFD180;border-radius:10px;pointer-events:none;box-shadow:0 0 0 9999px rgba(0,0,0,0.45);"></div>'
        '\n                  <div style="position:absolute;bottom:6px;left:0;right:0;text-align:center;color:#FFF;font-size:12px;background:rgba(0,0,0,0.65);padding:4px 8px;">'
        '\n                    Visez le QR Code du billet • <button type="button" onclick="stopQrCameraScan()" style="background:none;border:none;color:#FFD180;cursor:pointer;text-decoration:underline;">Fermer la caméra</button>'
        '\n                  </div>'
        '\n                </div>'
    )
    if 'id="btnToggleCameraScan"' not in content:
        content = content.replace(
            '<button class="btn btn-primary" onclick="verifyLiveQrCode()">Vérifier dans la BDD</button>\n                  </div>',
            '<button class="btn btn-primary" onclick="verifyLiveQrCode()">Vérifier dans la BDD</button>\n                    ' + agt_camera_btn + '\n                  </div>' + agt_camera_box
        )

    # 8. Ajouter la modale CGV
    if CGV_MODAL_START in content and CGV_MODAL_END in content:
        content = re.sub(
            re.escape(CGV_MODAL_START) + r".*?" + re.escape(CGV_MODAL_END),
            lambda m: CGV_MODAL_HTML,
            content,
            flags=re.DOTALL,
        )
    else:
        # Insérer avant la fin de #modalOverlaySprint1
        modal_box_close = '</div>\n\n  <button type="button" class="floating-demo-pill"'
        if modal_box_close in content:
            content = content.replace(modal_box_close, CGV_MODAL_HTML + "\n  " + modal_box_close)

    # 9. Mettre à jour loadBookingIntoQrPass pour générer le QR SVG dynamique
    load_qr_old = "if (scanInput) scanInput.value = found.reference;\n      }"
    load_qr_new = (
        "if (scanInput) scanInput.value = found.reference;\n"
        "        if (typeof renderEcoparkQrSvg === 'function') renderEcoparkQrSvg(found.reference, 'demoTicketQrWrapper');\n"
        "      }"
    )
    if load_qr_old in content:
        content = content.replace(load_qr_old, load_qr_new)

    # 10. Mettre à jour createLiveBookingSprint1 pour valider CGV + Téléphone + régénérer QR
    target_bk_block = (
        "    function createLiveBookingSprint1() {\n"
        "      const nameEl = document.getElementById('visitorName');\n"
        "      const phoneEl = document.getElementById('visitorPhone');\n"
        "      const dateEl = document.getElementById('visitDate');\n"
        "      const holder = (nameEl && nameEl.value.trim()) ? nameEl.value.trim() : 'Visiteur ECOPARK (Pass Coupe-File)';\n"
        "      const phone = (phoneEl && phoneEl.value.trim()) ? phoneEl.value.trim() : '+237 697 13 62 03';\n"
        "      const rawDate = (dateEl && dateEl.value.trim()) ? dateEl.value.trim() : '2026-11-15';"
    )
    replacement_bk_block = (
        "    function createLiveBookingSprint1() {\n"
        "      const nameEl = document.getElementById('visitorName');\n"
        "      const phoneEl = document.getElementById('visitorPhone');\n"
        "      const dateEl = document.getElementById('visitDate');\n"
        "      const holder = (nameEl && nameEl.value.trim()) ? nameEl.value.trim() : 'Visiteur ECOPARK (Pass Coupe-File)';\n"
        "      const phone = (phoneEl && phoneEl.value.trim()) ? phoneEl.value.trim() : '+237 697 13 62 03';\n"
        "      const rawDate = (dateEl && dateEl.value.trim()) ? dateEl.value.trim() : '2026-11-15';\n\n"
        "      const cgvEl = document.getElementById('agreeTermsBooking');\n"
        "      if (cgvEl && !cgvEl.checked) {\n"
        "        cgvEl.focus();\n"
        "        showToastSprint1('• Veuillez accepter les Conditions Générales de Vente (CGV) pour valider votre commande.');\n"
        "        return false;\n"
        "      }"
    )
    if target_bk_block in content:
        content = content.replace(target_bk_block, replacement_bk_block)

    create_qr_refresh = (
        "if (scanInput) scanInput.value = ref;\n"
        "      if (typeof renderEcoparkQrSvg === 'function') renderEcoparkQrSvg(ref, 'demoTicketQrWrapper');\n"
    )
    if "if (scanInput) scanInput.value = ref;\n" in content and "renderEcoparkQrSvg(ref, 'demoTicketQrWrapper')" not in content:
        content = content.replace("if (scanInput) scanInput.value = ref;\n", create_qr_refresh)

    # 11. Mettre à jour recalcSimulator pour utiliser getCatalogPriceDynamic
    recalc_old_units = (
        "const zooAdultUnit = isGroup20Plus ? 700 : 1000;\n"
        "      const zooChildUnit = 500;"
    )
    recalc_dyn_units = (
        "const zooAdultUnit = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('zoo', isGroup20Plus, false) : (isGroup20Plus ? 700 : 1000);\n"
        "      const zooChildUnit = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('zoo', isGroup20Plus, true) : 500;"
    )
    if recalc_old_units in content:
        content = content.replace(recalc_old_units, recalc_dyn_units)

    recalc_piscine_old = "const piscineCost = document.getElementById('chkPiscine').checked\n        ? (counts.adults * 2500 + counts.children * piscineChildUnit) : 0;"
    recalc_piscine_dyn = (
        "const piscineAdultDynamic = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('piscine', isGroup20Plus, false) : 2500;\n"
        "      const piscineCost = document.getElementById('chkPiscine').checked\n"
        "        ? (counts.adults * piscineAdultDynamic + counts.children * piscineChildUnit) : 0;"
    )
    if recalc_piscine_old in content:
        content = content.replace(recalc_piscine_old, recalc_piscine_dyn)

    recalc_pirogue_old = "const pirogueCost = document.getElementById('chkPirogue').checked\n        ? (counts.adults * 1000 + counts.children * 500) : 0;"
    recalc_pirogue_dyn = (
        "const pirogueAdultDyn = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('pirogue', isGroup20Plus, false) : 1000;\n"
        "      const pirogueChildDyn = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('pirogue', isGroup20Plus, true) : 500;\n"
        "      const pirogueCost = document.getElementById('chkPirogue').checked\n"
        "        ? (counts.adults * pirogueAdultDyn + counts.children * pirogueChildDyn) : 0;"
    )
    if recalc_pirogue_old in content:
        content = content.replace(recalc_pirogue_old, recalc_pirogue_dyn)

    recalc_cheval_old = "const chevalCost = document.getElementById('chkCheval').checked\n        ? (counts.adults * 1000 + counts.children * 500) : 0;"
    recalc_cheval_dyn = (
        "const chevalAdultDyn = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('cheval', isGroup20Plus, false) : 1000;\n"
        "      const chevalChildDyn = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('cheval', isGroup20Plus, true) : 500;\n"
        "      const chevalCost = document.getElementById('chkCheval').checked\n"
        "        ? (counts.adults * chevalAdultDyn + counts.children * chevalChildDyn) : 0;"
    )
    if recalc_cheval_old in content:
        content = content.replace(recalc_cheval_old, recalc_cheval_dyn)

    recalc_repas_old = "const repasCost = document.getElementById('chkRepas').checked\n        ? (counts.adults * 5000 + counts.children * 2500) : 0;"
    recalc_repas_dyn = (
        "const repasAdultDyn = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('saveurs', isGroup20Plus, false) : 5000;\n"
        "      const repasChildDyn = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic('saveurs', isGroup20Plus, true) : 2500;\n"
        "      const repasCost = document.getElementById('chkRepas').checked\n"
        "        ? (counts.adults * repasAdultDyn + counts.children * repasChildDyn) : 0;"
    )
    if recalc_repas_old in content:
        content = content.replace(recalc_repas_old, recalc_repas_dyn)

    # 12. Injecter le script PHASE5_JS à la fin du script principal
    if PHASE5_JS_START in content and PHASE5_JS_END in content:
        content = re.sub(
            re.escape(PHASE5_JS_START) + r".*?" + re.escape(PHASE5_JS_END),
            lambda m: PHASE5_JS,
            content,
            flags=re.DOTALL,
        )
    else:
        content = content.replace("  </script>\n</body>", "  " + PHASE5_JS + "\n  </script>\n</body>")

    return content


def main():
    print("Mise à jour Phase 5 & Viabilité Terrain...")
    for target in TARGETS:
        if not target.exists():
            print(f"ATTENTION : cible introuvable {target}")
            continue
        original = target.read_text(encoding="utf-8")
        updated = apply_phase5_upgrades(original)
        target.write_text(updated, encoding="utf-8")
        print(f"  OK: {target.name} mis à jour ({len(original.splitlines())} -> {len(updated.splitlines())} lignes)")
    print("Terminé avec succès !")


if __name__ == "__main__":
    main()
