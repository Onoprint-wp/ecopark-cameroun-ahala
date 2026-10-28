# -*- coding: utf-8 -*-
"""
Phase 8 — Intégration et synchronisation 360° des 11 Services Officiels du Totem Physique ECOPARK :
  1. ZOO (←)
  2. MUSÉE (←)
  3. BIBLIOTHÈQUE (←)
  4. AIRE DE JEUX (←)
  5. HÔTELS
  6. RESTAURANTS
  7. SALLES DES FÊTES
  8. CENTRES DE FORMATION
  9. PISCINE (→)
  10. SUITES PRIVÉES (→)
  11. CRÈCHE-GARDERIE (←)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = [
    ROOT / "etape0-site-live" / "index.html",
    ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

TOTEM_PUB_START = "<!-- ECOPARK_TOTEM_11_SERVICES:START -->"
TOTEM_PUB_END = "<!-- ECOPARK_TOTEM_11_SERVICES:END -->"

TOTEM_RES_START = "<!-- ECOPARK_TOTEM_RES_CHECKS:START -->"
TOTEM_RES_END = "<!-- ECOPARK_TOTEM_RES_CHECKS:END -->"

TOTEM_POS_START = "<!-- ECOPARK_TOTEM_POS_BTNS:START -->"
TOTEM_POS_END = "<!-- ECOPARK_TOTEM_POS_BTNS:END -->"

TOTEM_EXP_START = "<!-- ECOPARK_TOTEM_EXP_GRID:START -->"
TOTEM_EXP_END = "<!-- ECOPARK_TOTEM_EXP_GRID:END -->"

TOTEM_JS_START = "// ECOPARK_PHASE8_TOTEM_SYNC:START"
TOTEM_JS_END = "// ECOPARK_PHASE8_TOTEM_SYNC:END"

TOTEM_PUB_HTML = """        <!-- ECOPARK_TOTEM_11_SERVICES:START -->
        <div class="section" id="sec-totem-11-services" style="padding-top:24px;padding-bottom:24px;">
          <div class="container">
            <div class="card" style="background:linear-gradient(135deg, #F4F9F0 0%, #FFFFFF 60%, #FBF5EC 100%);border:2px solid rgba(29,73,13,0.22);padding:26px 28px;">
              <div class="grid-12" style="align-items:center;gap:24px;">
                <div class="col-4">
                  <div style="position:relative;border-radius:18px;overflow:hidden;border:3px solid #1D490D;box-shadow:0 16px 38px rgba(20,34,17,0.16);background:#142211;max-height:540px;">
                    <img src="audit-assets/ecopark-real-media/totem-services-ecopark.png" alt="Totem officiel de signalétique des 11 services sur le site ECOPARK Cameroun à Yaoundé-Ahala" style="width:100%;height:520px;object-fit:cover;display:block;" />
                    <span style="position:absolute;top:12px;left:12px;background:rgba(20,34,17,0.85);color:#FFFFFF;font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:999px;">Signalétique Réelle • Domaine d'Ahala</span>
                  </div>
                </div>
                <div class="col-8">
                  <span class="eyebrow" style="margin-bottom:6px;"><span class="tech-code-tag">PUB-02 • </span>Signalétique Officielle du Domaine — Les 11 Services d'Ahala</span>
                  <h2 style="font-size:1.85rem;margin-bottom:8px;">Tous les pôles du Totem ECOPARK en 1 clic</h2>
                  <p style="font-size:14.5px;color:var(--color-text-muted);margin-bottom:16px;">
                    Retrouvez ci-dessous l'intégralité des <strong>11 services officiels</strong> présents sur le totem directionnel d'Ahala Barrière. Cliquez sur n'importe quel panneau pour l'ajouter directement à votre Billet QR Coupe-File, réserver une Suite Privée, demander un Devis Salle des Fêtes ou candidater au CFP.
                  </p>
                  <div id="totem11ServicesInteractiveGrid" style="display:grid;grid-template-columns:repeat(auto-fill, minmax(235px, 1fr));gap:9px;">
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('zoo')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#0F8A5F;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(15,138,95,0.25);">
                      <span>1. ZOO ←</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="zoo">500 / 1 000 FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('musee')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#F27D16;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(242,125,22,0.25);">
                      <span>2. MUSÉE ←</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="musee">500 / 1 000 FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('bibliotheque')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#1B3F8B;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(27,63,139,0.25);">
                      <span>3. BIBLIOTHÈQUE ←</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="bibliotheque">500 FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('aire_jeux')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#4B3296;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(75,50,150,0.25);">
                      <span>4. AIRE DE JEUX ←</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="aire_jeux">500 FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('hotels')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#5C3A21;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(92,58,33,0.25);">
                      <span>5. HÔTELS</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;">10k – 25k FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('saveurs')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#D99000;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(217,144,0,0.25);">
                      <span>6. RESTAURANTS</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="saveurs">2 500 / 5 000 FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('salles_fetes')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#B565A7;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(181,101,167,0.25);">
                      <span>7. SALLES DES FÊTES</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;">Devis Menkii</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('cfp')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#7A121C;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(122,18,28,0.25);">
                      <span>8. CENTRES DE FORMATION</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;">CFP 50k + 4 tr.</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('piscine')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#D81B60;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(216,27,96,0.25);">
                      <span>9. PISCINE →</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="piscine">1 500 / 2 500 FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('suites_privees')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#0288D1;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(2,136,209,0.25);">
                      <span>10. SUITES PRIVÉES →</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;">30k – 45k FCFA</span>
                    </button>
                    <button type="button" class="totem-plate-btn" onclick="selectTotemService('creche_garderie')" style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-radius:10px;border:none;background:#D32F2F;color:#FFFFFF;font-weight:800;font-size:13.5px;cursor:pointer;text-align:left;box-shadow:0 4px 10px rgba(211,47,47,0.25);">
                      <span>11. CRÈCHE-GARDERIE ←</span>
                      <span style="font-size:11.5px;background:rgba(255,255,255,0.22);padding:2px 8px;border-radius:999px;" data-totem-price="creche_garderie">1 500 FCFA</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- ECOPARK_TOTEM_11_SERVICES:END -->"""

TOTEM_RES_HTML = """                  <!-- ECOPARK_TOTEM_RES_CHECKS:START -->
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkMusee" onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Musée Culturel &amp; Patrimoine du Cameroun</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subMusee">0 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkBibliotheque" onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Bibliothèque &amp; Espace Lecture Jeunesse</strong> (Enfant : 500 FCFA • Adulte : 500 FCFA)
                    </span>
                    <span class="price-pill" id="subBibliotheque">0 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkAireJeux" onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Aire de Jeux Enfants, Toboggans &amp; Manèges</strong> (Enfant : 500 FCFA • Adulte : 500 FCFA)
                    </span>
                    <span class="price-pill" id="subAireJeux">0 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkCrecheGarderie" onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Crèche-Garderie &amp; Halte-Garderie Sécurisée</strong> (1 500 FCFA / enfant • 1 000 FCFA groupe)
                    </span>
                    <span class="price-pill" id="subCrecheGarderie">0 FCFA</span>
                  </label>
                  <!-- ECOPARK_TOTEM_RES_CHECKS:END -->"""

TOTEM_POS_HTML = """                  <!-- ECOPARK_TOTEM_POS_BTNS:START -->
                  <button class="col-6 btn btn-secondary" onclick="addPosItem('Musée Culturel ECOPARK', 1000)">+ Musée (500 / 1 000 FCFA)</button>
                  <button class="col-6 btn btn-secondary" onclick="addPosItem('Bibliothèque & Lecture', 500)">+ Bibliothèque (500 FCFA)</button>
                  <button class="col-6 btn btn-secondary" onclick="addPosItem('Aire de Jeux Enfants', 500)">+ Aire de Jeux (500 FCFA)</button>
                  <button class="col-6 btn btn-secondary" onclick="addPosItem('Crèche-Garderie Sécurisée', 1500)">+ Crèche-Garderie (1 500 FCFA)</button>
                  <button class="col-12 btn btn-secondary btn-ochre-outline" onclick="addPosItem('Suite Privée Prestige VIP (Day-Use / Nuit)', 30000)">+ Suite Privée Prestige VIP (30 000 FCFA)</button>
                  <!-- ECOPARK_TOTEM_POS_BTNS:END -->"""

TOTEM_EXP_HTML = """            <!-- ECOPARK_TOTEM_EXP_GRID:START -->
            <div class="card" id="expTotem11ServicesCard" style="margin-bottom:20px;padding:18px 20px;background:#FBFDF9;border:1.5px solid rgba(29,73,13,0.2);">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px;">
                <div>
                  <span class="eyebrow" style="margin:0;"><span class="tech-code-tag">EXP-01 &amp; EXP-02 • </span>Supervision des 11 Pôles Officiels du Totem d'Ahala</span>
                  <h3 style="margin-top:2px;font-size:1.25rem;">État Opérationnel en Direct des 11 Services du Domaine</h3>
                </div>
                <span class="status-badge status-success" id="expTotemActiveCountBadge">11 / 11 Services Ouverts &amp; Synchronisés</span>
              </div>
              <div id="expTotem11ServicesGrid" style="display:grid;grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));gap:10px;font-size:13px;">
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #0F8A5F;border-radius:8px;border:1px solid var(--color-border);"><strong>1. Zoo (« ToTo ») ←</strong><br/><span style="color:var(--color-text-muted);">500 / 1 000 FCFA • Capacité 1 200/j</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #F27D16;border-radius:8px;border:1px solid var(--color-border);"><strong>2. Musée Culturel ←</strong><br/><span style="color:var(--color-text-muted);">500 / 1 000 FCFA • Capacité 300/j</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #1B3F8B;border-radius:8px;border:1px solid var(--color-border);"><strong>3. Bibliothèque ←</strong><br/><span style="color:var(--color-text-muted);">500 FCFA • Capacité 150/j</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #4B3296;border-radius:8px;border:1px solid var(--color-border);"><strong>4. Aire de Jeux ←</strong><br/><span style="color:var(--color-text-muted);">500 FCFA • Capacité 350/j</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #5C3A21;border-radius:8px;border:1px solid var(--color-border);"><strong>5. Hôtels (3 Cités)</strong><br/><span style="color:var(--color-text-muted);">Bene, Chanthel, Ewondo (10k–25k)</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #D99000;border-radius:8px;border:1px solid var(--color-border);"><strong>6. Restaurants</strong><br/><span style="color:var(--color-text-muted);">Château des Saveurs &amp; Pergolas</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #B565A7;border-radius:8px;border:1px solid var(--color-border);"><strong>7. Salles des Fêtes</strong><br/><span style="color:var(--color-text-muted);">Salle Menkii Essomba Anton</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #7A121C;border-radius:8px;border:1px solid var(--color-border);"><strong>8. Centres de Formation</strong><br/><span style="color:var(--color-text-muted);">CFP MINEFOP (5 filières)</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #D81B60;border-radius:8px;border:1px solid var(--color-border);"><strong>9. Piscine →</strong><br/><span style="color:var(--color-text-muted);">1 500 / 2 500 FCFA • Surveillée</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #0288D1;border-radius:8px;border:1px solid var(--color-border);"><strong>10. Suites Privées →</strong><br/><span style="color:var(--color-text-muted);">30 000 – 45 000 FCFA • 6 suites VIP</span></div>
                <div style="padding:10px 12px;background:#FFFFFF;border-left:4px solid #D32F2F;border-radius:8px;border:1px solid var(--color-border);"><strong>11. Crèche-Garderie ←</strong><br/><span style="color:var(--color-text-muted);">1 500 FCFA • Capacité 80 enfants</span></div>
              </div>
            </div>
            <!-- ECOPARK_TOTEM_EXP_GRID:END -->"""

TOTEM_JS_BLOCK = """// ECOPARK_PHASE8_TOTEM_SYNC:START
  // ==========================================================================
  // PHASE 8 : SYNCHRONISATION 360° DES 11 SERVICES DU TOTEM OFFICIEL ECOPARK
  // ==========================================================================
  (function () {
    if (typeof VISUAL_APPRECIATION_CATALOG !== 'undefined' && VISUAL_APPRECIATION_CATALOG.LODGES) {
      VISUAL_APPRECIATION_CATALOG.LODGES.SUITES_PRIVEES = {
        title: 'Suites Privées Prestige — Salon Privé & Service VIP',
        rate: '30 000 – 45 000 FCFA / nuit ou Day-Use',
        desc: 'Suite privée haut standing avec salon climatisé, literie King-Size, service en chambre Château des Saveurs et accès coupe-file Piscine & Zoo.',
        src: 'audit-assets/ecopark-real-media/chambre.jpeg',
        lbIdx: 8
      };
    }

    var origGetSelectedLodgeDetails = window.getSelectedLodgeDetails;
    window.getSelectedLodgeDetails = function () {
      var cityEl = document.getElementById('lodgeCitySelect');
      var nightsEl = document.getElementById('lodgeNightsSelect');
      var city = cityEl ? cityEl.value : 'EWONDO';
      var nights = nightsEl ? (parseInt(nightsEl.value, 10) || 1) : 1;
      if (city === 'SUITES_PRIVEES') {
        var unit = 30000;
        if (window.EcoparkData && typeof EcoparkData.content === 'function') {
          var dynLodges = EcoparkData.content('lodge_cities') || [];
          dynLodges.forEach(function (l) {
            if (l && l.code === 'SUITES_PRIVEES' && l.status === 'PUBLISHED' && typeof l.min_price_fcfa === 'number' && l.min_price_fcfa > 0) {
              unit = l.min_price_fcfa;
            }
          });
        }
        return {
          city: 'SUITES_PRIVEES',
          nights: nights,
          unit: unit,
          total: unit * nights,
          summary: 'Suite Privée Prestige VIP (' + nights + ' nuit' + (nights > 1 ? 's' : '') + ')'
        };
      }
      return typeof origGetSelectedLodgeDetails === 'function' ? origGetSelectedLodgeDetails() : { city: city, nights: nights, unit: 25000, total: 25000 * nights, summary: 'Suite VIP Cité Ewondo' };
    };

    window.selectTotemService = function (serviceKey) {
      if (serviceKey === 'salles_fetes') {
        if (typeof openQuoteModalSprint1 === 'function') openQuoteModalSprint1();
        return;
      }
      if (serviceKey === 'cfp') {
        if (typeof openCfpModalSprint1 === 'function') openCfpModalSprint1();
        return;
      }
      if (serviceKey === 'hotels') {
        navigateFamily('RES', 'RES-03');
        var chkLodge = document.getElementById('chkBumpLodgeEwondo');
        var selCity = document.getElementById('lodgeCitySelect');
        if (chkLodge) chkLodge.checked = true;
        if (selCity && selCity.value === 'SUITES_PRIVEES') selCity.value = 'EWONDO';
        if (typeof recalcSimulator === 'function') recalcSimulator();
        showToastSprint1('• Hôtels ECOPARK sélectionnés : choisissez votre Cité (Ewondo, Chanthel ou Bene).');
        return;
      }
      if (serviceKey === 'suites_privees') {
        navigateFamily('RES', 'RES-03');
        var chkL = document.getElementById('chkBumpLodgeEwondo');
        var selC = document.getElementById('lodgeCitySelect');
        if (chkL) chkL.checked = true;
        if (selC) selC.value = 'SUITES_PRIVEES';
        if (typeof recalcSimulator === 'function') recalcSimulator();
        showToastSprint1('• Suites Privées Prestige VIP (30 000 FCFA) activées dans votre réservation !');
        return;
      }
      addActivityAndGo(serviceKey);
    };

    window.addActivityAndGo = function (actKey) {
      navigateFamily('RES', 'RES-03');
      var map = {
        zoo: 'chkZoo',
        piscine: 'chkPiscine',
        pirogue: 'chkPirogue',
        cheval: 'chkCheval',
        saveurs: 'chkRepas',
        musee: 'chkMusee',
        bibliotheque: 'chkBibliotheque',
        aire_jeux: 'chkAireJeux',
        creche_garderie: 'chkCrecheGarderie',
        nutrition_poissons: 'chkBumpNutrition',
        pergola_lac: 'chkBumpPergola',
        navette_yaounde: 'chkBumpNavette'
      };
      var targetId = map[actKey];
      if (targetId && document.getElementById(targetId)) {
        document.getElementById(targetId).checked = true;
      }
      if (typeof recalcSimulator === 'function') recalcSimulator();
    };

    var origRecalc = window.recalcSimulator;
    window.recalcSimulator = function () {
      if (typeof origRecalc === 'function') origRecalc();
      var totalPayingPax = (counts.adults || 0) + (counts.children || 0);
      var isGroup = totalPayingPax >= 20;

      var extraItems = [
        { slug: 'musee', chkId: 'chkMusee', subId: 'subMusee', label: 'Musée Culturel & Patrimoine ECOPARK' },
        { slug: 'bibliotheque', chkId: 'chkBibliotheque', subId: 'subBibliotheque', label: 'Bibliothèque & Espace Lecture' },
        { slug: 'aire_jeux', chkId: 'chkAireJeux', subId: 'subAireJeux', label: 'Aire de Jeux Enfants & Toboggans' },
        { slug: 'creche_garderie', chkId: 'chkCrecheGarderie', subId: 'subCrecheGarderie', label: 'Crèche-Garderie Sécurisée', childOnly: true }
      ];

      var extraTotal = 0;
      var extraLinesHtml = '';
      extraItems.forEach(function (it) {
        var chk = document.getElementById(it.chkId);
        var subEl = document.getElementById(it.subId);
        var cost = 0;
        if (chk && chk.checked) {
          var cUnit = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic(it.slug, isGroup, true) : 500;
          var aUnit = typeof getCatalogPriceDynamic === 'function' ? getCatalogPriceDynamic(it.slug, isGroup, false) : 1000;
          if (it.childOnly) {
            var kids = Math.max(1, (counts.children || 0) + (counts.toddlers || 0));
            cost = kids * cUnit;
          } else {
            cost = (counts.adults || 0) * aUnit + (counts.children || 0) * cUnit;
          }
          extraTotal += cost;
          extraLinesHtml += '<div style="display:flex;justify-content:space-between;"><span>' + escHtml(it.label) + '</span><strong>' + formatFCFA(cost) + '</strong></div>';
        }
        if (subEl) subEl.textContent = formatFCFA(cost);
      });

      if (extraTotal > 0) {
        var grandEl = document.getElementById('grandTotalFCFA');
        var baseGrand = grandEl ? (parseInt(String(grandEl.textContent || '').replace(/[^0-9]/g, ''), 10) || 0) : 0;
        var newGrand = baseGrand + extraTotal;
        if (grandEl) grandEl.textContent = formatFCFA(newGrand);
        var stickyEl = document.getElementById('stickyBarTotalFcfa');
        if (stickyEl) stickyEl.textContent = formatFCFA(newGrand);
        var ticketTotalEl = document.getElementById('ticketTotalPaid');
        if (ticketTotalEl) ticketTotalEl.textContent = formatFCFA(newGrand);
        var breakdownEl = document.getElementById('cartBreakdown');
        if (breakdownEl) breakdownEl.insertAdjacentHTML('beforeend', extraLinesHtml);
      }
    };

    var origSummary = window.getActiveSimulatorItemsSummary;
    window.getActiveSimulatorItemsSummary = function () {
      var base = typeof origSummary === 'function' ? origSummary() : '';
      var extras = [];
      if (document.getElementById('chkMusee') && document.getElementById('chkMusee').checked) extras.push('Musée Culturel');
      if (document.getElementById('chkBibliotheque') && document.getElementById('chkBibliotheque').checked) extras.push('Bibliothèque');
      if (document.getElementById('chkAireJeux') && document.getElementById('chkAireJeux').checked) extras.push('Aire de Jeux');
      if (document.getElementById('chkCrecheGarderie') && document.getElementById('chkCrecheGarderie').checked) extras.push('Crèche-Garderie');
      if (!extras.length) return base;
      return (base ? (base + ', ') : '') + extras.join(', ');
    };

    function fmtSpace(n) {
      return String(n || 0).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    }

    window.syncTotem11ServicesBadges = function () {
      if (!window.EcoparkData || typeof EcoparkData.content !== 'function') return;
      var acts = EcoparkData.content('catalog_activities') || [];
      acts.forEach(function (a) {
        if (!a || a.status !== 'PUBLISHED') return;
        var badge = document.querySelector('[data-totem-price="' + a.slug + '"]');
        if (badge) {
          if (a.child_price_fcfa > 0 && a.child_price_fcfa !== a.adult_price_fcfa) {
            badge.textContent = fmtSpace(a.child_price_fcfa) + ' / ' + fmtSpace(a.adult_price_fcfa) + ' FCFA';
          } else {
            badge.textContent = fmtSpace(a.adult_price_fcfa || a.child_price_fcfa || 500) + ' FCFA';
          }
        }
      });
    };

    var origRenderPubCat = window.renderPubCatalogFromData;
    window.renderPubCatalogFromData = function () {
      if (typeof origRenderPubCat === 'function') origRenderPubCat();
      syncTotem11ServicesBadges();
    };

    window.addEventListener('ecopark:sync', function () {
      syncTotem11ServicesBadges();
    });
    setTimeout(syncTotem11ServicesBadges, 50);
  })();
// ECOPARK_PHASE8_TOTEM_SYNC:END"""


def replace_or_insert(html: str, start_marker: str, end_marker: str, new_block: str, anchor: str, before: bool = True) -> str:
    nl = "\r\n" if "\r\n" in html else "\n"
    block_nl = new_block.replace("\r\n", "\n").replace("\n", nl)
    if start_marker in html and end_marker in html:
        pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.S)
        return pattern.sub(lambda _: block_nl, html, count=1)
    assert anchor in html, f"Anchor not found: {anchor[:60]}"
    if before:
        return html.replace(anchor, block_nl + nl + nl + anchor, 1)
    else:
        return html.replace(anchor, anchor + nl + block_nl, 1)


def patch_file(path: Path):
    html = path.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in html else "\n"

    # 1. Section Totem 11 Services dans #view-PUB juste avant #sec-PUB-03
    html = replace_or_insert(
        html,
        TOTEM_PUB_START,
        TOTEM_PUB_END,
        TOTEM_PUB_HTML,
        '        <!-- CATALOGUE DES 6 PÔLES D\'EXPÉRIENCES (PUB-02 à PUB-09, PUB-11, PUB-12) -->',
        before=True,
    )

    # 2. Cases à cocher Musée, Bibliothèque, Aire de Jeux, Crèche-Garderie dans #view-RES
    res_anchor = '                    <span class="price-pill" id="subRepas">0 FCFA</span>' + nl + '                  </label>'
    html = replace_or_insert(
        html,
        TOTEM_RES_START,
        TOTEM_RES_END,
        TOTEM_RES_HTML,
        res_anchor,
        before=False,
    )

    # 2b. Option SUITES_PRIVEES dans #lodgeCitySelect
    lodge_opt_anchor = '<option value="EWONDO" selected>Cité Ewondo VIP (25 000 FCFA/nuit)</option>'
    suites_opt = '<option value="SUITES_PRIVEES">Suites Privées Prestige VIP (30 000 FCFA/nuit)</option>'
    if suites_opt not in html and lodge_opt_anchor in html:
        html = html.replace(lodge_opt_anchor, lodge_opt_anchor + nl + "                          " + suites_opt, 1)

    # 3. Boutons POS Walk-in dans #view-AGT
    pos_anchor = '<button class="col-6 btn btn-secondary btn-ochre-outline" onclick="addPosItem(\'Sachet Nutrition Poissons\', 500)">+ Sachet Nutrition Poissons (500 FCFA)</button>'
    html = replace_or_insert(
        html,
        TOTEM_POS_START,
        TOTEM_POS_END,
        TOTEM_POS_HTML,
        pos_anchor,
        before=False,
    )

    # 4. Grille des 11 Pôles du Totem dans #view-EXP
    exp_anchor = '            <!-- Bandeau Temps Réel : Impact de la Stratégie de Vente sur l\'Exploitation (Cuisine, Pergolas, Loges & Panier Moyen) -->'
    html = replace_or_insert(
        html,
        TOTEM_EXP_START,
        TOTEM_EXP_END,
        TOTEM_EXP_HTML,
        exp_anchor,
        before=True,
    )

    # 5. Nouveaux pôles dans #admPoleFilter
    adm_pole_anchor = '<option value="FORMATION_CFP">Formation CFP</option>'
    adm_new_poles = '<option value="CULTURE_EDUCATION">Musée &amp; Bibliothèque</option>' + nl + '                  <option value="FAMILLE_ENFANCE">Aire de Jeux &amp; Crèche-Garderie</option>'
    if 'value="CULTURE_EDUCATION"' not in html and adm_pole_anchor in html:
        html = html.replace(adm_pole_anchor, adm_pole_anchor + nl + "                  " + adm_new_poles, 1)

    # 6. Bloc JS de synchronisation Phase 8
    js_anchor = "// ECOPARK_PHASE7_ORCHESTRATION:END"
    html = replace_or_insert(
        html,
        TOTEM_JS_START,
        TOTEM_JS_END,
        TOTEM_JS_BLOCK,
        js_anchor,
        before=False,
    )

    path.write_text(html, encoding="utf-8")
    print(f"Patched {path.name} successfully.")


if __name__ == "__main__":
    for t in TARGETS:
        patch_file(t)
