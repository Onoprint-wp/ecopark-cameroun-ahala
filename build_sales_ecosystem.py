# -*- coding: utf-8 -*-
"""
Intégration de la Stratégie de Vente & Maximisation du Panier Moyen (AOV) dans l'Écosystème ECOPARK Yaoundé-Ahala :
1. PUB-10 : 3 Cartes « Pass Tout-Inclus » (Pass Découverte Nature, Pass Journée Royale, Pack Escapade Couple VIP Ewondo) en ancrage au-dessus de la grille unitaire.
2. RES-03 : Sélecteur rapide de Pass en 1 clic + Section « Options Coup de Cœur & Coupe-File (Order Bumps) » (Sachet Nutrition Poissons +500 FCFA, Pergola Privée Lac +5 000 FCFA, Suite VIP Cité Ewondo +25 000 FCFA).
3. AGT-03 : Touches rapides d'Upsell au Guichet (Pass Royale & Sachet Nutrition).
4. EXP-04/05 & DIR-01..04 : Synchronisation en temps réel des précommandes cuisine Château des Saveurs, de la jauge Pergolas, de la disponibilité des Suites Ewondo et du Panier Moyen B2C.
"""

import pathlib

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
DIST_INDEX = ROOT / "etape0-site-live" / "index.html"
PROTO_HTML = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"

PUB10_BUNDLES_HTML = """            <div class="section-header">
              <span class="eyebrow"><span class="tech-code-tag"><span class="tech-code-tag">PUB-10 • </span></span>Transparence Tarifaire & Formules Packagées en Francs CFA</span>
              <h2>Nos Pass Tout-Inclus & Grille Tarifaire Officielle</h2>
              <p style="color:var(--color-text-muted);margin-top:8px;">
                Évitez les files d'attente aux différents stands en réservant un <strong>Pass Tout-Inclus sur un seul QR Code</strong>, ou composez votre visite à la carte en <strong>FCFA (XAF)</strong>. Gratuité d'accès au site pour les tout-petits de moins de 3 ans.
              </p>
            </div>

            <!-- 3 PASS TOUT-INCLUS (ANCRAGE COMMERCIAL & AUGMENTATION DU PANIER MOYEN) -->
            <div class="grid-12" style="margin-bottom:28px;gap:20px;" id="pubSalesBundlesGrid">
              <!-- Pass 1 : Découverte Nature -->
              <div class="col-4 card" style="display:flex;flex-direction:column;justify-content:space-between;border:1px solid var(--color-border);">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:8px;flex-wrap:wrap;">
                    <span class="status-badge status-success">Accès Coupe-File QR</span>
                    <span style="font-size:12.5px;font-weight:700;color:var(--color-brand-deep);">Économie -500 FCFA/adulte</span>
                  </div>
                  <h3 style="margin-bottom:6px;">Pass Découverte Nature</h3>
                  <p style="font-size:14px;color:var(--color-text-muted);margin-bottom:12px;">
                    Les 3 expériences plein air d'ECOPARK Ahala réunies sur un seul billet QR sans repasser en caisse.
                  </p>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
                    <span class="price-pill">Adulte : 2 500 FCFA</span>
                    <span class="price-pill">Enfant : 1 500 FCFA</span>
                  </div>
                  <ul style="padding-left:18px;font-size:14px;display:grid;gap:6px;margin-bottom:16px;">
                    <li><strong>Entrée Parc & Jardin Zoologique</strong> (Chimpanzés, tortues, paons)</li>
                    <li><strong>Balade en Pirogue</strong> sur le lac d'Ahala (gilet fourni)</li>
                    <li><strong>Tour à Cheval</strong> encadré ou manèges enfants</li>
                  </ul>
                </div>
                <button type="button" class="btn btn-secondary" style="width:100%;" onclick="applySalesBundle('PASS_DECOUVERTE', true)">Choisir le Pass Découverte</button>
              </div>

              <!-- Pass 2 : Pass Journée Royale (Le Plus Choisi — Ancrage Central) -->
              <div class="col-4 card" style="display:flex;flex-direction:column;justify-content:space-between;border:2px solid #C47D2B;background:linear-gradient(180deg, #FBF5EC 0%, #FFFFFF 48%);box-shadow:0 16px 36px rgba(196,125,43,0.14);">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:8px;flex-wrap:wrap;">
                    <span class="status-badge" style="background:#C47D2B;color:#FFFFFF;border:none;">Le Plus Choisi • Tout-Inclus</span>
                    <span style="font-size:12.5px;font-weight:700;color:#8E5617;">Économie -1 000 FCFA/pers.</span>
                  </div>
                  <h3 style="margin-bottom:6px;">Pass Journée Royale</h3>
                  <p style="font-size:14px;color:var(--color-text-muted);margin-bottom:12px;">
                    Activités phares + baignade + repas chaud réservé au <em>Château des Saveurs</em> sans attente à midi.
                  </p>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
                    <span class="price-pill">Adulte : 8 500 FCFA</span>
                    <span class="price-pill">Enfant : 4 500 FCFA</span>
                  </div>
                  <ul style="padding-left:18px;font-size:14px;display:grid;gap:6px;margin-bottom:16px;">
                    <li><strong>Entrée Parc & Zoo</strong> + <strong>Balade en Pirogue</strong></li>
                    <li><strong>Accès Piscine Semi-Olympique</strong> toute la journée</li>
                    <li><strong>Repas chaud inclus</strong> au <em>Château des Saveurs</em> (Poisson braisé d'Ahala ou Poulet DG)</li>
                    <li><strong>File prioritaire QR</strong> au portail d'Ahala</li>
                  </ul>
                </div>
                <button type="button" class="btn btn-primary" style="width:100%;" onclick="applySalesBundle('PASS_ROYALE', true)">Choisir le Pass Journée Royale</button>
              </div>

              <!-- Pass 3 : Pack Escapade Couple / VIP Week-end -->
              <div class="col-4 card" style="display:flex;flex-direction:column;justify-content:space-between;border:1px solid var(--color-border);">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:8px;flex-wrap:wrap;">
                    <span class="status-badge status-info" id="pubEwondoScarcityBadge">Plus que 2 Suites Ewondo</span>
                    <span style="font-size:12.5px;font-weight:700;color:var(--color-brand-deep);">Forfait Duo 2 Adultes</span>
                  </div>
                  <h3 style="margin-bottom:6px;">Pack Escapade Couple VIP</h3>
                  <p style="font-size:14px;color:var(--color-text-muted);margin-bottom:12px;">
                    Séjour prestige pour 2 adultes avec Suite climatisée, table au bord de l'eau et accès complet.
                  </p>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
                    <span class="price-pill">Forfait 2 Adultes : 45 000 FCFA</span>
                  </div>
                  <ul style="padding-left:18px;font-size:14px;display:grid;gap:6px;margin-bottom:16px;">
                    <li><strong>1 Suite VIP Cité Ewondo</strong> climatisée (Nuitée ou Day-Use)</li>
                    <li><strong>2 Repas gastronomiques</strong> au <em>Château des Saveurs</em></li>
                    <li><strong>Pergola privée réservée</strong> au bord du lac d'Ahala</li>
                    <li><strong>Accès Piscine, Zoo & Pirogue</strong> pour 2 personnes</li>
                  </ul>
                </div>
                <button type="button" class="btn btn-secondary btn-ochre-outline" style="width:100%;" onclick="applySalesBundle('PACK_COUPLE_EWONDO', true)">Réserver l'Escapade VIP</button>
              </div>
            </div>"""

RES03_BUNDLES_AND_BUMPS_HTML = """                <h3 style="margin-top:8px;">2. Formules Packagées (1 clic) ou Choix à la Carte<span class="tech-code-tag"> (`RES-03`)</span></h3>
                <div id="bundleQuickSelector" style="display:grid;grid-template-columns:repeat(2, 1fr);gap:8px;margin-bottom:12px;">
                  <button type="button" class="btn btn-secondary btn-sm" id="btnBundleCustom" style="justify-content:space-between;border-color:var(--color-brand-deep);background:var(--color-surface-soft);" onclick="applySalesBundle('CUSTOM', false)">
                    <span>• Sélection à la carte</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">Sur-mesure</span>
                  </button>
                  <button type="button" class="btn btn-secondary btn-sm" id="btnBundleDecouverte" style="justify-content:space-between;" onclick="applySalesBundle('PASS_DECOUVERTE', false)">
                    <span>Pass Découverte Nature</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">2 500 / 1 500 FCFA</span>
                  </button>
                  <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" id="btnBundleRoyale" style="justify-content:space-between;" onclick="applySalesBundle('PASS_ROYALE', false)">
                    <span>Pass Journée Royale (Repas inclus)</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">8 500 / 4 500 FCFA</span>
                  </button>
                  <button type="button" class="btn btn-secondary btn-sm" id="btnBundleCouple" style="justify-content:space-between;" onclick="applySalesBundle('PACK_COUPLE_EWONDO', false)">
                    <span>Pack Escapade Couple VIP Ewondo</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">45 000 FCFA (Duo)</span>
                  </button>
                </div>

                <div style="display:grid;gap:10px;">
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkZoo" checked onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Entrée Parc & Jardin Zoologique</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subZoo">3 000 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkPiscine" checked onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Accès Piscine Semi-Olympique</strong> (Enfant : 1 500 FCFA • Adulte : 2 500 FCFA)
                    </span>
                    <span class="price-pill" id="subPiscine">8 000 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkPirogue" checked onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Balade en Pirogue sur le Lac</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subPirogue">3 000 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkCheval" onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Tour à Cheval / Manèges</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subCheval">0 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkRepas" onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Repas au Château des Saveurs</strong> (Enfant : 2 500 FCFA • Adulte : 5 000 FCFA)
                    </span>
                    <span class="price-pill" id="subRepas">0 FCFA</span>
                  </label>
                </div>

                <!-- ORDER BUMPS : OPTIONS COUP DE COEUR & PRIVILÈGES COUPE-FILE -->
                <div style="margin-top:14px;padding:14px;background:#FBF5EC;border:1px solid rgba(196,125,43,0.35);border-radius:12px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:6px;">
                    <strong style="color:#8E5617;font-size:14.5px;">Options Privilèges & Expériences Enfants (Order Bumps en 1 clic) :</strong>
                    <span style="font-size:12px;font-weight:600;color:var(--color-brand-deep);">Ajoutés directement sur votre QR Code</span>
                  </div>
                  <div style="display:grid;gap:8px;">
                    <label style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                      <span style="font-size:14px;">
                        <input type="checkbox" id="chkBumpNutrition" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Sachet Nutrition Poissons & Tortues</strong> (500 FCFA / enfant • nourrissage aux étangs)
                      </span>
                      <span class="price-pill" id="subBumpNutrition">0 FCFA</span>
                    </label>
                    <label style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                      <span style="font-size:14px;">
                        <input type="checkbox" id="chkBumpPergola" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Pergola Privée Bord du Lac & Service Prioritaire 13h</strong> (+5 000 FCFA forfait)
                      </span>
                      <span class="price-pill" id="subBumpPergola">0 FCFA</span>
                    </label>
                    <label style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                      <span style="font-size:14px;">
                        <input type="checkbox" id="chkBumpLodgeEwondo" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Suite VIP Cité Ewondo Climatisée</strong> (+25 000 FCFA • <span id="simEwondoRemainingText">2 suites disponibles</span>)
                      </span>
                      <span class="price-pill" id="subBumpLodge">0 FCFA</span>
                    </label>
                  </div>
                </div>"""

EXP_SALES_KPI_BAR_HTML = """            <div class="section-header">
              <span class="eyebrow"><span class="tech-code-tag"><span class="tech-code-tag">EXP-01 à EXP-07 • </span></span>Gestion Opérationnelle du Site d'Ahala</span>
              <h2>Pilotage Quotidien : Capacités, Devis, Loges Hôtelières & CFP</h2>
            </div>

            <!-- Bandeau Temps Réel : Impact de la Stratégie de Vente sur l'Exploitation (Cuisine, Pergolas, Loges & Panier Moyen) -->
            <div class="grid-12" style="margin-bottom:20px;gap:14px;" id="expSalesEcosystemBar">
              <div class="col-3 card" style="background:var(--color-surface-soft);padding:16px;">
                <span style="font-size:13px;color:var(--color-text-muted);">Précommandes Cuisine (EXP-05)</span>
                <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);display:block;margin-top:4px;" id="expKitchenPreordersVal">18 repas réservés</strong>
                <span style="font-size:12.5px;color:var(--color-brand-deep);">Poisson braisé d'Ahala & Poulet DG</span>
              </div>
              <div class="col-3 card" style="background:var(--color-surface-soft);padding:16px;">
                <span style="font-size:13px;color:var(--color-text-muted);">Pergolas Bord du Lac (EXP-05)</span>
                <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);display:block;margin-top:4px;" id="expPergolasVal">6 / 10 réservées</strong>
                <span style="font-size:12.5px;color:#8E5617;">4 pergolas disponibles à 13h00</span>
              </div>
              <div class="col-3 card" style="background:var(--color-surface-soft);padding:16px;">
                <span style="font-size:13px;color:var(--color-text-muted);">Sachets Nutrition Étangs (EXP-02)</span>
                <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);display:block;margin-top:4px;" id="expFishPacksVal">34 sachets commandés</strong>
                <span style="font-size:12.5px;color:var(--color-brand-deep);">Upsell famille à 500 FCFA</span>
              </div>
              <div class="col-3 card" style="background:#FBF5EC;border-color:rgba(196,125,43,0.4);padding:16px;">
                <span style="font-size:13px;color:#8E5617;font-weight:600;">Panier Moyen B2C en Ligne</span>
                <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);display:block;margin-top:4px;" id="expAvgBasketVal">14 000 FCFA</strong>
                <span style="font-size:12.5px;color:#8E5617;">Objectif Bundling : > 8 500 FCFA</span>
              </div>
            </div>"""

SALES_ENGINE_JS = """
    // ========================================================================
    // MOTEUR D'ANCRAGE COMMERCIAL : PASS TOUT-INCLUS & ORDER BUMPS (RES-03 / PUB-10)
    // ========================================================================
    window._activeBundleCode = 'CUSTOM';

    function updateBundleButtonsUI() {
      const mapping = {
        CUSTOM: 'btnBundleCustom',
        PASS_DECOUVERTE: 'btnBundleDecouverte',
        PASS_ROYALE: 'btnBundleRoyale',
        PACK_COUPLE_EWONDO: 'btnBundleCouple'
      };
      Object.keys(mapping).forEach(code => {
        const btn = document.getElementById(mapping[code]);
        if (!btn) return;
        if (window._activeBundleCode === code) {
          btn.style.borderColor = '#1D490D';
          btn.style.background = '#EDF4E7';
        } else {
          btn.style.borderColor = '';
          btn.style.background = '';
        }
      });
    }

    function onManualActivityToggle() {
      window._activeBundleCode = 'CUSTOM';
      updateBundleButtonsUI();
      recalcSimulator();
    }

    function applySalesBundle(bundleCode, shouldNavigate) {
      if (shouldNavigate) {
        navigateFamily('RES', 'RES-03');
      }
      window._activeBundleCode = bundleCode || 'CUSTOM';
      const z = document.getElementById('chkZoo');
      const p = document.getElementById('chkPiscine');
      const pir = document.getElementById('chkPirogue');
      const ch = document.getElementById('chkCheval');
      const rep = document.getElementById('chkRepas');
      const bumpNut = document.getElementById('chkBumpNutrition');
      const bumpPerg = document.getElementById('chkBumpPergola');
      const bumpLodge = document.getElementById('chkBumpLodgeEwondo');

      if (bundleCode === 'PASS_DECOUVERTE') {
        if (z) z.checked = true;
        if (p) p.checked = false;
        if (pir) pir.checked = true;
        if (ch) ch.checked = true;
        if (rep) rep.checked = false;
        if (bumpPerg) bumpPerg.checked = false;
        if (bumpLodge) bumpLodge.checked = false;
        showToastSprint1('• Pass Découverte Nature activé : Zoo + Pirogue + Cheval avec remise Pass (-500 FCFA/adulte) !');
      } else if (bundleCode === 'PASS_ROYALE') {
        if (z) z.checked = true;
        if (p) p.checked = true;
        if (pir) pir.checked = true;
        if (ch) ch.checked = false;
        if (rep) rep.checked = true;
        if (bumpLodge) bumpLodge.checked = false;
        showToastSprint1('• Pass Journée Royale activé : Zoo + Piscine + Pirogue + Repas Château des Saveurs (8 500 FCFA/adulte, 4 500 FCFA/enfant) !');
      } else if (bundleCode === 'PACK_COUPLE_EWONDO') {
        counts.adults = 2;
        counts.children = 0;
        counts.toddlers = 0;
        document.getElementById('countAdults').textContent = '2';
        document.getElementById('countChildren').textContent = '0';
        document.getElementById('countToddlers').textContent = '0';
        if (z) z.checked = true;
        if (p) p.checked = true;
        if (pir) pir.checked = true;
        if (ch) ch.checked = false;
        if (rep) rep.checked = true;
        if (bumpNut) bumpNut.checked = false;
        if (bumpPerg) bumpPerg.checked = true;
        if (bumpLodge) bumpLodge.checked = true;
        showToastSprint1('• Pack Escapade Couple VIP activé : Suite Cité Ewondo + 2 Repas + Pergola Lac + Piscine & Pirogue (Forfait 45 000 FCFA) !');
      }
      updateBundleButtonsUI();
      recalcSimulator();
    }
"""

NEW_RECALC_SIMULATOR_JS = """    function recalcSimulator() {
      const totalPayingPax = counts.adults + counts.children;
      const isGroup20Plus = totalPayingPax >= 20;

      // RÈGLE MÉTIER STRICTE :
      // En groupe (>=20), l'entrée adulte passe de 1 000 à 700 FCFA,
      // MAIS l'entrée enfant reste protégée à 500 FCFA (jamais majorée à 700 FCFA !).
      const zooAdultUnit = isGroup20Plus ? 700 : 1000;
      const zooChildUnit = 500;

      const zooCost = document.getElementById('chkZoo').checked
        ? (counts.adults * zooAdultUnit + counts.children * zooChildUnit) : 0;
      const piscineCost = document.getElementById('chkPiscine').checked
        ? (counts.adults * 2500 + counts.children * 1500) : 0;
      const pirogueCost = document.getElementById('chkPirogue').checked
        ? (counts.adults * 1000 + counts.children * 500) : 0;
      const chevalCost = document.getElementById('chkCheval').checked
        ? (counts.adults * 1000 + counts.children * 500) : 0;
      const repasCost = document.getElementById('chkRepas').checked
        ? (counts.adults * 5000 + counts.children * 2500) : 0;

      // Options Order Bumps (en 1 clic)
      const bumpNutritionChecked = document.getElementById('chkBumpNutrition') && document.getElementById('chkBumpNutrition').checked;
      const bumpPergolaChecked = document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked;
      const bumpLodgeChecked = document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked;

      const nutritionPacksCount = bumpNutritionChecked ? Math.max(1, counts.children) : 0;
      const nutritionCost = nutritionPacksCount * 500;
      const pergolaCost = bumpPergolaChecked ? 5000 : 0;
      const lodgeCost = bumpLodgeChecked ? 25000 : 0;

      document.getElementById('subZoo').textContent = formatFCFA(zooCost);
      document.getElementById('subPiscine').textContent = formatFCFA(piscineCost);
      document.getElementById('subPirogue').textContent = formatFCFA(pirogueCost);
      document.getElementById('subCheval').textContent = formatFCFA(chevalCost);
      document.getElementById('subRepas').textContent = formatFCFA(repasCost);
      if (document.getElementById('subBumpNutrition')) document.getElementById('subBumpNutrition').textContent = formatFCFA(nutritionCost);
      if (document.getElementById('subBumpPergola')) document.getElementById('subBumpPergola').textContent = formatFCFA(pergolaCost);
      if (document.getElementById('subBumpLodge')) document.getElementById('subBumpLodge').textContent = formatFCFA(lodgeCost);

      let bundleDiscount = 0;
      let bundleLabel = '';
      if (window._activeBundleCode === 'PASS_DECOUVERTE' && !isGroup20Plus) {
        bundleDiscount = counts.adults * 500;
        bundleLabel = 'Remise Pass Découverte Nature (-500 FCFA/adulte)';
      } else if (window._activeBundleCode === 'PASS_ROYALE' && !isGroup20Plus) {
        bundleDiscount = (counts.adults * 1000) + (counts.children * 500);
        bundleLabel = 'Remise Pass Journée Royale (-1 000 FCFA/adulte, -500 FCFA/enfant)';
      } else if (window._activeBundleCode === 'PACK_COUPLE_EWONDO') {
        bundleDiscount = 4000;
        bundleLabel = 'Remise Forfait Escapade Couple VIP Ewondo (-4 000 FCFA)';
      }

      const rawSubtotal = zooCost + piscineCost + pirogueCost + chevalCost + repasCost + nutritionCost + pergolaCost + lodgeCost;
      const total = Math.max(0, rawSubtotal - bundleDiscount);
      document.getElementById('grandTotalFCFA').textContent = formatFCFA(total);

      const badge = document.getElementById('groupStatusBadge');
      if (isGroup20Plus) {
        badge.textContent = 'Groupe 20+ (Adulte 700 FCFA / Enfant protégé 500 FCFA)';
        badge.className = 'status-badge status-info';
      } else if (window._activeBundleCode && window._activeBundleCode !== 'CUSTOM') {
        const bNames = {
          PASS_DECOUVERTE: 'Pass Découverte Nature (Coupe-File)',
          PASS_ROYALE: 'Pass Journée Royale (Tout-Inclus)',
          PACK_COUPLE_EWONDO: 'Pack Escapade Couple VIP Ewondo'
        };
        badge.textContent = bNames[window._activeBundleCode] || 'Formule Packagée';
        badge.className = 'status-badge status-success';
      } else {
        badge.textContent = 'Tarif Individuel / Famille';
        badge.className = 'status-badge status-success';
      }

      const lines = [];
      lines.push(`<div><strong>Participants :</strong> ${counts.adults} Adulte(s), ${counts.children} Enfant(s) (3-12 ans), ${counts.toddlers} Tout-petit(s) (<3 ans : Gratuit)</div>`);
      if (zooCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Entrée Parc & Zoo (${counts.adults}×${zooAdultUnit} + ${counts.children}×${zooChildUnit})</span><strong>${formatFCFA(zooCost)}</strong></div>`);
      if (piscineCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Piscine Semi-Olympique</span><strong>${formatFCFA(piscineCost)}</strong></div>`);
      if (pirogueCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Balade en Pirogue (Lac d'Ahala)</span><strong>${formatFCFA(pirogueCost)}</strong></div>`);
      if (chevalCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Équitation / Manèges</span><strong>${formatFCFA(chevalCost)}</strong></div>`);
      if (repasCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Repas Le Château des Saveurs</span><strong>${formatFCFA(repasCost)}</strong></div>`);
      if (nutritionCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Order Bump : ${nutritionPacksCount}× Sachet(s) Nutrition Poissons</span><strong>${formatFCFA(nutritionCost)}</strong></div>`);
      if (pergolaCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Order Bump : Pergola Privée Bord du Lac (13h)</span><strong>${formatFCFA(pergolaCost)}</strong></div>`);
      if (lodgeCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Hébergement : Suite VIP Cité Ewondo Climatisée</span><strong>${formatFCFA(lodgeCost)}</strong></div>`);
      if (bundleDiscount > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:var(--color-brand-deep);font-weight:700;"><span>${bundleLabel}</span><strong>-${formatFCFA(bundleDiscount)}</strong></div>`);
      document.getElementById('cartBreakdown').innerHTML = lines.join('');
      document.getElementById('ticketPax').textContent = `${counts.adults} Adulte(s), ${counts.children} Enfant(s), ${counts.toddlers} Tout-petit(s)`;
    }"""


def apply_sales_ecosystem():
    html = DIST_INDEX.read_text(encoding="utf-8")
    if "pubSalesBundlesGrid" in html:
        html = html.replace(
            "bundleDiscount = (counts.adults * 1000) + (counts.children * 1000);",
            "bundleDiscount = (counts.adults * 1000) + (counts.children * 500);",
        ).replace(
            "bundleLabel = 'Remise Pass Journée Royale (-1 000 FCFA/pers.)';",
            "bundleLabel = 'Remise Pass Journée Royale (-1 000 FCFA/adulte, -500 FCFA/enfant)';",
        )
        DIST_INDEX.write_text(html, encoding="utf-8")
        PROTO_HTML.write_text(html, encoding="utf-8")
        print("[OK] Ecosysteme de Vente deja present dans index.html (mis a jour et idempotent).")
        return

    # 1. Remplacer l'en-tête PUB-10 pour inclure les 3 Pass Tout-Inclus
    target_pub10 = """            <div class="section-header">
              <span class="eyebrow"><span class="tech-code-tag"><span class="tech-code-tag">PUB-10 • </span></span>Transparence Tarifaire en Francs CFA</span>
              <h2>Grille Tarifaire Officielle ECOPARK Yaoundé-Ahala</h2>
              <p style="color:var(--color-text-muted);margin-top:8px;">
                Tous nos tarifs sont exprimés en <strong>FCFA (XAF)</strong>. Gratuité d'accès au site pour les tout-petits de moins de 3 ans accompagnés d'un parent.
              </p>
            </div>"""
    if target_pub10 not in html and "\r\n" in html:
        target_pub10 = target_pub10.replace("\n", "\r\n")
    assert target_pub10 in html, "Target PUB-10 non trouve"
    html = html.replace(target_pub10, PUB10_BUNDLES_HTML, 1)

    # 2. Remplacer l'étape 2 de RES-03 pour ajouter le sélecteur de Pass en 1 clic et les 3 Order Bumps
    target_res03 = """                <h3 style="margin-top:8px;">2. Choix des expériences et prestations<span class="tech-code-tag"> (`RES-03`)</span></h3>
                <div style="display:grid;gap:10px;">
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkZoo" checked onchange="recalcSimulator()" />
                      <strong style="margin-left:8px;">Entrée Parc & Jardin Zoologique</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subZoo">3 000 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkPiscine" checked onchange="recalcSimulator()" />
                      <strong style="margin-left:8px;">Accès Piscine Semi-Olympique</strong> (Enfant : 1 500 FCFA • Adulte : 2 500 FCFA)
                    </span>
                    <span class="price-pill" id="subPiscine">8 000 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkPirogue" checked onchange="recalcSimulator()" />
                      <strong style="margin-left:8px;">Balade en Pirogue sur le Lac</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subPirogue">3 000 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkCheval" onchange="recalcSimulator()" />
                      <strong style="margin-left:8px;">Tour à Cheval / Manèges</strong> (Enfant : 500 FCFA • Adulte : 1 000 FCFA)
                    </span>
                    <span class="price-pill" id="subCheval">0 FCFA</span>
                  </label>
                  <label style="display:flex;justify-content:space-between;align-items:center;padding:12px;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                    <span>
                      <input type="checkbox" id="chkRepas" onchange="recalcSimulator()" />
                      <strong style="margin-left:8px;">Repas au Château des Saveurs</strong> (Enfant : 2 500 FCFA • Adulte : 5 000 FCFA)
                    </span>
                    <span class="price-pill" id="subRepas">0 FCFA</span>
                  </label>
                </div>"""
    if target_res03 not in html and "\r\n" in html:
        target_res03 = target_res03.replace("\n", "\r\n")
    assert target_res03 in html, "Target RES-03 non trouve"
    html = html.replace(target_res03, RES03_BUNDLES_AND_BUMPS_HTML, 1)

    # 3. Ajouter les 2 boutons d'Upsell rapide au Guichet (AGT-03)
    target_agt03 = """                  <button class="col-6 btn btn-secondary" onclick="addPosItem('Pirogue Enfant', 500)">+ Pirogue Enfant (500 FCFA)</button>
                  <button class="col-6 btn btn-secondary" onclick="addPosItem('Pirogue Adulte', 1000)">+ Pirogue Adulte (1 000 FCFA)</button>"""
    replacement_agt03 = target_agt03 + """
                  <button class="col-6 btn btn-secondary btn-ochre-outline" onclick="addPosItem('Pass Journée Royale (Tout-Inclus)', 8500)">+ Pass Royale Adulte (8 500 FCFA)</button>
                  <button class="col-6 btn btn-secondary btn-ochre-outline" onclick="addPosItem('Sachet Nutrition Poissons', 500)">+ Sachet Nutrition Poissons (500 FCFA)</button>"""
    if target_agt03 not in html and "\r\n" in html:
        target_agt03 = target_agt03.replace("\n", "\r\n")
    assert target_agt03 in html, "Target AGT-03 non trouve"
    html = html.replace(target_agt03, replacement_agt03, 1)

    # 4. Ajouter le bandeau temps réel d'Impact Écosystème dans EXP
    target_exp = """            <div class="section-header">
              <span class="eyebrow"><span class="tech-code-tag"><span class="tech-code-tag">EXP-01 à EXP-07 • </span></span>Gestion Opérationnelle du Site d'Ahala</span>
              <h2>Pilotage Quotidien : Capacités, Devis, Loges Hôtelières & CFP</h2>
            </div>"""
    if target_exp not in html and "\r\n" in html:
        target_exp = target_exp.replace("\n", "\r\n")
    assert target_exp in html, "Target EXP non trouve"
    html = html.replace(target_exp, EXP_SALES_KPI_BAR_HTML, 1)

    # 5. Remplacer recalcSimulator() par la nouvelle version supportant les Pass & Order Bumps
    old_recalc = """    function recalcSimulator() {
      const totalPayingPax = counts.adults + counts.children;
      const isGroup20Plus = totalPayingPax >= 20;

      // RÈGLE MÉTIER STRICTE :
      // En groupe (>=20), l'entrée adulte passe de 1 000 à 700 FCFA,
      // MAIS l'entrée enfant reste protégée à 500 FCFA (jamais majorée à 700 FCFA !).
      const zooAdultUnit = isGroup20Plus ? 700 : 1000;
      const zooChildUnit = 500;

      const zooCost = document.getElementById('chkZoo').checked
        ? (counts.adults * zooAdultUnit + counts.children * zooChildUnit) : 0;
      const piscineCost = document.getElementById('chkPiscine').checked
        ? (counts.adults * 2500 + counts.children * 1500) : 0;
      const pirogueCost = document.getElementById('chkPirogue').checked
        ? (counts.adults * 1000 + counts.children * 500) : 0;
      const chevalCost = document.getElementById('chkCheval').checked
        ? (counts.adults * 1000 + counts.children * 500) : 0;
      const repasCost = document.getElementById('chkRepas').checked
        ? (counts.adults * 5000 + counts.children * 2500) : 0;

      document.getElementById('subZoo').textContent = formatFCFA(zooCost);
      document.getElementById('subPiscine').textContent = formatFCFA(piscineCost);
      document.getElementById('subPirogue').textContent = formatFCFA(pirogueCost);
      document.getElementById('subCheval').textContent = formatFCFA(chevalCost);
      document.getElementById('subRepas').textContent = formatFCFA(repasCost);

      const total = zooCost + piscineCost + pirogueCost + chevalCost + repasCost;
      document.getElementById('grandTotalFCFA').textContent = formatFCFA(total);

      const badge = document.getElementById('groupStatusBadge');
      if (isGroup20Plus) {
        badge.textContent = 'Groupe 20+ (Adulte 700 FCFA / Enfant protégé 500 FCFA)';
        badge.className = 'status-badge status-info';
      } else {
        badge.textContent = 'Tarif Individuel / Famille';
        badge.className = 'status-badge status-success';
      }

      const lines = [];
      lines.push(`<div><strong>Participants :</strong> ${counts.adults} Adulte(s), ${counts.children} Enfant(s) (3-12 ans), ${counts.toddlers} Tout-petit(s) (<3 ans : Gratuit)</div>`);
      if (zooCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Entrée Parc & Zoo (${counts.adults}×${zooAdultUnit} + ${counts.children}×${zooChildUnit})</span><strong>${formatFCFA(zooCost)}</strong></div>`);
      if (piscineCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Piscine Semi-Olympique</span><strong>${formatFCFA(piscineCost)}</strong></div>`);
      if (pirogueCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Balade en Pirogue (Lac d'Ahala)</span><strong>${formatFCFA(pirogueCost)}</strong></div>`);
      if (chevalCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Équitation / Manèges</span><strong>${formatFCFA(chevalCost)}</strong></div>`);
      if (repasCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Repas Le Château des Saveurs</span><strong>${formatFCFA(repasCost)}</strong></div>`);
      document.getElementById('cartBreakdown').innerHTML = lines.join('');
      document.getElementById('ticketPax').textContent = `${counts.adults} Adulte(s), ${counts.children} Enfant(s), ${counts.toddlers} Tout-petit(s)`;
    }"""
    if old_recalc not in html and "\r\n" in html:
        old_recalc = old_recalc.replace("\n", "\r\n")
    assert old_recalc in html, "old_recalc non trouve"
    html = html.replace(old_recalc, SALES_ENGINE_JS + "\n" + NEW_RECALC_SIMULATOR_JS, 1)

    # 6. Enrichir createLiveBookingSprint1() et syncAllViewsFromDB() pour propager les Order Bumps (Repas, Pergola, Nutrition, Suite Ewondo) dans l'Exploitation
    old_acts_block = """      const acts = [];
      if (document.getElementById('chkZoo') && document.getElementById('chkZoo').checked) acts.push('Zoo');
      if (document.getElementById('chkPiscine') && document.getElementById('chkPiscine').checked) acts.push('Piscine');
      if (document.getElementById('chkPirogue') && document.getElementById('chkPirogue').checked) acts.push('Pirogue');
      if (document.getElementById('chkCheval') && document.getElementById('chkCheval').checked) acts.push('Équitation');
      if (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) acts.push('Saveurs');"""
    new_acts_block = """      const acts = [];
      if (window._activeBundleCode && window._activeBundleCode !== 'CUSTOM') acts.push(window._activeBundleCode);
      if (document.getElementById('chkZoo') && document.getElementById('chkZoo').checked) acts.push('Zoo');
      if (document.getElementById('chkPiscine') && document.getElementById('chkPiscine').checked) acts.push('Piscine');
      if (document.getElementById('chkPirogue') && document.getElementById('chkPirogue').checked) acts.push('Pirogue');
      if (document.getElementById('chkCheval') && document.getElementById('chkCheval').checked) acts.push('Équitation');
      if (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) acts.push('Saveurs');
      if (document.getElementById('chkBumpNutrition') && document.getElementById('chkBumpNutrition').checked) acts.push('Nutrition Poissons');
      if (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked) acts.push('Pergola Lac');
      if (document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked) acts.push('Suite Ewondo');

      db.opsMetrics = db.opsMetrics || { kitchenPreorders: 18, pergolasReserved: 6, fishPacks: 34, ewondoFree: 2 };
      if (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) {
        db.opsMetrics.kitchenPreorders += (counts.adults + counts.children);
      }
      if (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked) {
        db.opsMetrics.pergolasReserved = Math.min(10, db.opsMetrics.pergolasReserved + 1);
      }
      if (document.getElementById('chkBumpNutrition') && document.getElementById('chkBumpNutrition').checked) {
        db.opsMetrics.fishPacks += Math.max(1, counts.children);
      }
      if (document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked) {
        db.opsMetrics.ewondoFree = Math.max(0, db.opsMetrics.ewondoFree - 1);
      }"""
    if old_acts_block not in html and "\r\n" in html:
        old_acts_block = old_acts_block.replace("\n", "\r\n")
    assert old_acts_block in html, "old_acts_block non trouve"
    html = html.replace(old_acts_block, new_acts_block, 1)

    # 7. Mettre à jour syncAllViewsFromDB() pour rafraîchir le bandeau Exploitation (#expSalesEcosystemBar) et la rareté Ewondo
    old_sync_end = """      // 5. Mettre à jour le Journal d'Audit (ADM-08)
      const admTbody = document.querySelector('#view-ADM table tbody');
      if (admTbody) {
        admTbody.innerHTML = db.auditLogs.slice(0, 6).map(log => `
          <tr>
            <td>${log.time}</td>
            <td><strong>${log.actor}</strong></td>
            <td>${log.action}</td>
          </tr>
        `).join('');
      }
    }"""
    new_sync_end = """      // 5. Mettre à jour le Journal d'Audit (ADM-08)
      const admTbody = document.querySelector('#view-ADM table tbody');
      if (admTbody) {
        admTbody.innerHTML = db.auditLogs.slice(0, 6).map(log => `
          <tr>
            <td>${log.time}</td>
            <td><strong>${log.actor}</strong></td>
            <td>${log.action}</td>
          </tr>
        `).join('');
      }

      // 6. Mettre à jour les indicateurs d'impact Écosystème Vente (EXP-04/05 & Panier Moyen B2C)
      const ops = db.opsMetrics || { kitchenPreorders: 18, pergolasReserved: 6, fishPacks: 34, ewondoFree: 2 };
      const kEl = document.getElementById('expKitchenPreordersVal');
      const pEl = document.getElementById('expPergolasVal');
      const fEl = document.getElementById('expFishPacksVal');
      const avgEl = document.getElementById('expAvgBasketVal');
      if (kEl) kEl.textContent = `${ops.kitchenPreorders} repas réservés`;
      if (pEl) pEl.textContent = `${ops.pergolasReserved} / 10 réservées`;
      if (fEl) fEl.textContent = `${ops.fishPacks} sachets commandés`;
      if (avgEl && db.bookings && db.bookings.length > 0) {
        const sumB = db.bookings.reduce((acc, b) => acc + (b.totalFcfa || 0), 0);
        const avgB = Math.round(sumB / db.bookings.length);
        avgEl.textContent = formatFCFA(avgB);
      }
      const scarcityBadge = document.getElementById('pubEwondoScarcityBadge');
      const simEwondoTxt = document.getElementById('simEwondoRemainingText');
      if (scarcityBadge) {
        scarcityBadge.textContent = ops.ewondoFree > 0 ? `Plus que ${ops.ewondoFree} Suite(s) Ewondo` : 'Suites Ewondo Complètes';
      }
      if (simEwondoTxt) {
        simEwondoTxt.textContent = ops.ewondoFree > 0 ? `${ops.ewondoFree} suite(s) disponible(s)` : 'Complet ce soir';
      }
    }"""
    if old_sync_end not in html and "\r\n" in html:
        old_sync_end = old_sync_end.replace("\n", "\r\n")
    assert old_sync_end in html, "old_sync_end non trouve"
    html = html.replace(old_sync_end, new_sync_end, 1)

    # Vérification stricte : zéro caractère > 0x25FF
    high_chars = [ch for ch in html if ord(ch) > 0x25FF]
    assert len(high_chars) == 0, f"Caractères > 0x25FF détectés : {high_chars}"

    DIST_INDEX.write_text(html, encoding="utf-8")
    PROTO_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Ecosysteme de Vente (Pass Tout-Inclus + Order Bumps + KPIs Exploitation) integre ({len(html)} octets, 0 emoji OS).")


def verify_local_sales_ecosystem():
    from playwright.sync_api import sync_playwright
    url = DIST_INDEX.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url, wait_until="networkidle")

        # 1. Check initial odometer (+1 adult = 18500)
        page.evaluate("navigateFamily('RES', 'RES-03'); changeCount('adults', 1);")
        t1 = page.locator("#grandTotalFCFA").get_attribute("data-target-fcfa")
        page.evaluate("changeCount('adults', -1);")
        assert t1 == "18500", f"Expected 18500, got {t1}"

        # 2. Test Pass Journee Royale + Order Bumps (Nutrition + Pergola)
        page.evaluate("applySalesBundle('PASS_ROYALE', false);")
        t_royale = page.locator("#grandTotalFCFA").get_attribute("data-target-fcfa")
        assert t_royale == "26000", f"Expected 26000 for Pass Royale (2A+2E), got {t_royale}"

        page.evaluate("document.getElementById('chkBumpNutrition').checked = true; document.getElementById('chkBumpPergola').checked = true; recalcSimulator();")
        t_bumps = page.locator("#grandTotalFCFA").get_attribute("data-target-fcfa")
        assert t_bumps == "32000", f"Expected 32000 with Order Bumps, got {t_bumps}"

        # 3. Create live booking and verify Ecosystem impact in EXP and DIR
        page.evaluate("createLiveBookingSprint1();")
        exp_kitchen = page.locator("#expKitchenPreordersVal").inner_text()
        exp_pergola = page.locator("#expPergolasVal").inner_text()
        exp_fish = page.locator("#expFishPacksVal").inner_text()
        exp_avg = page.locator("#expAvgBasketVal").inner_text()

        print(f"  [OK] Odometer initial (+1A): {t1} FCFA")
        print(f"  [OK] Pass Journee Royale (2A+2E): {t_royale} FCFA")
        print(f"  [OK] Pass Royale + Order Bumps (Nutrition + Pergola): {t_bumps} FCFA")
        print(f"  [OK] Impact EXP -> Cuisine: {exp_kitchen} | Pergolas: {exp_pergola} | Sachets: {exp_fish} | Panier Moyen: {exp_avg}")
        assert exp_kitchen == "22 repas réservés"
        assert exp_pergola == "7 / 10 réservées"
        assert exp_fish == "36 sachets commandés"
        assert exp_avg == "23 000 FCFA"

        # 4. Test Pack Escapade Couple VIP Ewondo (45 000 FCFA & Scarcity decrement)
        page.evaluate("applySalesBundle('PACK_COUPLE_EWONDO', false);")
        t_couple = page.locator("#grandTotalFCFA").get_attribute("data-target-fcfa")
        assert t_couple == "45000", f"Expected 45000 for Pack Couple VIP, got {t_couple}"
        page.evaluate("createLiveBookingSprint1();")
        scarcity_txt = page.locator("#pubEwondoScarcityBadge").inner_text()
        print(f"  [OK] Pack Escapade Couple VIP: {t_couple} FCFA | Rarete Cité Ewondo mise a jour: '{scarcity_txt}'")
        assert "1 Suite(s) Ewondo" in scarcity_txt

        assert len(errors) == 0, f"JS errors: {errors}"
        browser.close()
    print("[ALL E2E SALES ECOSYSTEM CHECKS PASSED]")


if __name__ == "__main__":
    apply_sales_ecosystem()
    verify_local_sales_ecosystem()

