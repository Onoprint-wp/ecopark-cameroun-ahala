# -*- coding: utf-8 -*-
"""
Cure d'allègement visuel et structurel (Declutter Upgrade) pour ECOPARK Cameroun :
1. Correction du bug HTML (</div> surnuméraire dans #kitchenPreorderSubpanel) qui cassait la grille 2 colonnes (#resMainGrid) du Simulateur.
2. Divulgation progressive dans le Simulateur (#view-RES) :
   - Les sous-panneaux (Précommande Cuisine, Aperçu Cité Hôtelière, Point de ramassage Navette) ne s'affichent que lorsque leur option est cochée.
   - Le Baromètre de disponibilités (#liveAvailabilityBarometer), les conditions d'annulation (#resCancellationPolicyCard) et le Portefeuille WhatsApp (#whatsappConciergeCard) sont repliés proprement dans des accordéons élégants (<details class="clean-details-accordion">) pour supprimer l'effet "méga-cockpit de 5 000 px" et la triple redondance du panier.
3. Allègement du Header, de la Topbar, du Bandeau Météo (#ahalaLiveWeatherBar), du Hero (#sec-PUB-01) et de la Barre Mobile (#mobileStickyConversionBar) :
   - Suppression du doublon visuel de barre d'onglets en bas sur mobile (.mobile-quick-nav-strip masqué visuellement, réduisant la hauteur sticky de 186px à 62px).
   - Paragraphe d'accroche Hero condensé en 2 lignes éditoriales respirantes.
4. Épuration des 6 cartes Bento (#sec-PUB-03), de l'Agenda Hebdo (#sec-PUB-16) et de la section "Préparez votre venue" (#sec-PUB-13) :
   - Remplacement de l'affiche coupée sur la carte CFP (#sec-PUB-12) par le visuel campus CFP.
   - Masquage en mode visiteur des seconds boutons inactifs ("Fiche détail", "Détails sécurité", "Carte en FCFA", "Fiche Loge").
   - Suppression de la liste à puces redondante des Zones A à E au-dessus de la carte SVG interactive (#ahalaMapContainer).
5. Correction des défauts CSS (.card { justify-content: flex-start } pour supprimer les trous blancs de 200px dans la FAQ et Mon Espace, et correction des boutons multi-lignes de #modalQuoteBox).
"""

import os

FILES = [
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\etape0-site-live\index.html",
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

CSS_DECLUTTER = """
    /* ==========================================================================
       CURE D'ALLÈGEMENT VISUEL & RESPIRATION ÉDITORIALE (DECLUTTER UPGRADE)
       ========================================================================== */
    /* 1. Supprimer les trous blancs artificiels dans les cartes génériques (FAQ, Mon Espace, Simulateur) */
    .card {
      justify-content: flex-start !important;
    }
    .bento-card-body,
    .agenda-event-card,
    .testimonial-card,
    .quick-intent-card,
    #pubSalesBundlesGrid > .card {
      justify-content: space-between !important;
    }

    /* 2. Accordéons épurés pour désengorger le Simulateur et le Panier */
    details.clean-details-accordion {
      border: 1px solid rgba(29, 73, 13, 0.16);
      border-radius: 14px;
      background: #FFFFFF;
      overflow: hidden;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    details.clean-details-accordion[open] {
      border-color: rgba(196, 125, 43, 0.45);
      box-shadow: 0 8px 24px rgba(20, 34, 17, 0.06);
    }
    details.clean-details-accordion > summary {
      list-style: none;
      cursor: pointer;
      padding: 11px 14px;
      font-size: 13.5px;
      font-weight: 700;
      color: var(--color-brand-deep);
      background: linear-gradient(90deg, #EDF4E7 0%, #FBF5EC 100%);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      user-select: none;
    }
    details.clean-details-accordion > summary::-webkit-details-marker {
      display: none;
    }
    details.clean-details-accordion > summary::after {
      content: "▾ Afficher";
      font-size: 11.8px;
      font-weight: 700;
      color: #8E5617;
      background: rgba(255, 255, 255, 0.85);
      padding: 2px 9px;
      border-radius: 980px;
      border: 1px solid rgba(196, 125, 43, 0.32);
      white-space: nowrap;
      flex-shrink: 0;
    }
    details.clean-details-accordion[open] > summary::after {
      content: "▴ Réduire";
    }
    details.clean-details-accordion > .accordion-inner-body {
      padding: 12px 14px;
      border-top: 1px solid rgba(29, 73, 13, 0.1);
    }

    /* 3. Allègement de la barre mobile : masquer la 2e barre de pills redondante et les scrollbars grises */
    .mobile-quick-nav-strip {
      display: none !important;
    }
    .mobile-sticky-conversion-bar {
      padding: 8px 12px !important;
    }
    .mobile-sticky-conversion-bar .btn {
      min-height: 34px !important;
      padding: 5px 9px !important;
      font-size: 11.5px !important;
      white-space: nowrap !important;
    }
    #stickyBarPaxText {
      font-size: 9.5px !important;
      white-space: nowrap !important;
      max-width: 145px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #stickyBarTotalFcfa {
      font-size: 1.05rem !important;
      white-space: nowrap !important;
    }
    .main-nav,
    .site-topbar-inner {
      scrollbar-width: none;
    }
    .main-nav::-webkit-scrollbar,
    .site-topbar-inner::-webkit-scrollbar {
      display: none;
    }
    .ahala-live-weather-bar .price-pill,
    .ahala-live-weather-bar .btn {
      white-space: nowrap !important;
    }

    /* 4. Modales (Devis Groupe, CFP, RDV) : hauteur maîtrisée et boutons élancés */
    #modalQuoteBox,
    #modalCfpBox {
      max-width: 640px !important;
      max-height: 94vh !important;
      overflow-y: auto !important;
      padding: 16px 22px !important;
      gap: 6px !important;
    }
    #modalQuoteBox > p,
    #modalCfpBox > p {
      display: none !important;
    }
    #modalQuoteBox .modal-visual-preview-banner,
    #modalCfpBox .modal-visual-preview-banner,
    #modalRdvBox .modal-visual-preview-banner {
      margin: 2px 0 !important;
      padding: 7px 10px !important;
    }
    #modalQuoteBox .form-control,
    #modalCfpBox .form-control,
    #modalRdvBox .form-control {
      min-height: 36px !important;
      padding: 5px 10px !important;
      font-size: 13.5px !important;
    }
    #modalQuoteBox .btn,
    #modalCfpBox .btn,
    #modalRdvBox .btn,
    #modalEventDetailBox .btn,
    #modalRescheduleBox .btn {
      border-radius: 12px !important;
      line-height: 1.25 !important;
      padding: 10px 14px !important;
      font-size: 13px !important;
      min-height: 40px !important;
    }

    /* 5. Allègement visuel des capsules dans le grand tableau tarifaire et Mon Espace (#view-ACC) */
    #sec-PUB-10 .table-responsive td {
      padding: 10px 14px;
      font-size: 14.5px;
    }
    #view-ACC table th,
    #view-ACC table td {
      vertical-align: middle;
      padding: 10px 8px !important;
      font-size: 12.8px !important;
    }
    #view-ACC table td:nth-child(3) {
      min-width: 230px;
      max-width: 310px;
    }
    #view-ACC .status-badge {
      white-space: nowrap;
      font-size: 11.5px !important;
      padding: 3px 8px !important;
    }
    #view-ACC table td:last-child .btn {
      padding: 4px 10px !important;
      font-size: 11.5px !important;
      min-height: 28px !important;
      white-space: nowrap !important;
    }
    @media (max-width: 768px) {
      .ahala-live-weather-bar {
        padding: 8px 12px !important;
        gap: 6px !important;
        font-size: 12px !important;
      }
    }

    /* 6. Compacité des cartes Agenda Hebdomadaire */
    .agenda-meta-Highlight {
      display: none !important;
    }
"""

JS_DECLUTTER = """
    // ========================================================================
    // DIVULGATION PROGRESSIVE DU SIMULATEUR (MASQUER LES SOUS-OPTIONS NON COCHÉES)
    // ========================================================================
    function syncProgressiveDisclosureSimulator() {
      const repasOn = (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) ||
                      (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked);
      const kitchenPanel = document.getElementById('kitchenPreorderSubpanel');
      if (kitchenPanel) {
        kitchenPanel.style.display = repasOn ? 'grid' : 'none';
      }

      const lodgeOn = document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked;
      const lodgeCard = document.getElementById('lodgeVisualPreviewCard');
      if (lodgeCard) {
        lodgeCard.style.display = lodgeOn ? 'flex' : 'none';
      }

      const navetteOn = document.getElementById('chkBumpNavette') && document.getElementById('chkBumpNavette').checked;
      const shuttlePanel = document.getElementById('shuttlePickupSubpanel');
      if (shuttlePanel) {
        shuttlePanel.style.display = navetteOn ? 'grid' : 'none';
      }
    }

    const _origSyncVisualsBeforeDeclutter = syncVisualAppreciationSimulator;
    syncVisualAppreciationSimulator = function() {
      _origSyncVisualsBeforeDeclutter();
      syncProgressiveDisclosureSimulator();
    };

    if (typeof openStickyWhatsAppQuick === 'function') {
      const _origOpenStickyWa = openStickyWhatsAppQuick;
      openStickyWhatsAppQuick = function() {
        const acc = document.getElementById('waConciergeAccordion');
        if (acc) acc.open = true;
        _origOpenStickyWa();
      };
    }

    syncProgressiveDisclosureSimulator();
"""


def apply_declutter(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject or update CSS_DECLUTTER
    import re
    if "CURE D'ALLÈGEMENT VISUEL" in html:
        html = re.sub(
            r"\n    /\* ==========================================================================\n       CURE D'ALLÈGEMENT VISUEL.*?</style>",
            CSS_DECLUTTER + "\n  </style>",
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        html = html.replace("  </style>", CSS_DECLUTTER + "\n  </style>", 1)

    # 2. Fix the critical extra </div> bug inside #kitchenPreorderSubpanel that broke the 2-column grid in #view-RES
    broken_kitchen_div = """                        <select id="simMealSlotSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Service 12h30" selected>12h30 — Zéro attente (Prioritaire)</option>
                          <option value="Service 13h30">13h30 — Cœur de journée</option>
                          <option value="Service 15h00">15h00 — Après-midi au bord du lac</option>
                        </select>
                      </div>
                      </div>
                      <div id="kitchenVisualPreviewBox\""""

    fixed_kitchen_div = """                        <select id="simMealSlotSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Service 12h30" selected>12h30 — Zéro attente (Prioritaire)</option>
                          <option value="Service 13h30">13h30 — Cœur de journée</option>
                          <option value="Service 15h00">15h00 — Après-midi au bord du lac</option>
                        </select>
                      </div>
                      <div id="kitchenVisualPreviewBox\""""

    if broken_kitchen_div in html:
        html = html.replace(broken_kitchen_div, fixed_kitchen_div, 1)

    # 3. Simplify Topbar text
    old_topbar = """          <div><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg> <strong>Yaoundé – Ahala Barrière</strong> (Face station Tradex Ahala, route 100 % goudronnée • Parking sécurisé) • Mardi au Dimanche : <strong>09h00 – 18h00</strong></div>
          <div><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.58 2.81.7A2 2 0 0 1 22 16.92z"/></svg> WhatsApp &amp; Navettes : <a href="https://wa.me/237697136203" target="_blank" rel="noopener noreferrer" style="color:#FFFFFF;font-weight:700;">+237 697 13 62 03</a> / <a href="tel:+237675562655" style="color:#FFFFFF;font-weight:700;">+237 675 56 26 55</a> • <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg> <a href="mailto:info@ecopark-yaounde.com" style="color:#FFFFFF;">info@ecopark-yaounde.com</a></div>"""

    new_topbar = """          <div><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg> <strong>Yaoundé – Ahala Barrière</strong> (Face Tradex) • Mar–Dim : <strong>09h00–18h00</strong> • Parking gratuit</div>
          <div><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.58 2.81.7A2 2 0 0 1 22 16.92z"/></svg> WhatsApp : <a href="https://wa.me/237697136203" target="_blank" rel="noopener noreferrer" style="color:#FFFFFF;font-weight:700;">+237 697 13 62 03</a> • <a href="mailto:info@ecopark-yaounde.com" style="color:#FFFFFF;">info@ecopark-yaounde.com</a></div>"""

    if old_topbar in html:
        html = html.replace(old_topbar, new_topbar, 1)

    # 4. Simplify Weather Bar & Hero Lead Paragraph + 3rd redundant button
    old_weather = """            <div class="ahala-live-weather-bar" id="ahalaLiveWeatherBar" role="status" aria-label="Météo et affluence en direct d'Ahala Barrière">
              <div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px;">
                <span class="ahala-live-pulse-dot" aria-hidden="true"></span>
                <strong>En direct d'Ahala Barrière (RN3 Face Tradex) :</strong>
                <span>27 °C Ensoleillé &amp; Brise du Lac</span>
                <span>•</span>
                <span>Accès RN3 Fluide (15 min du centre)</span>
                <span>•</span>
                <span>Piscine, Pirogues &amp; Château des Saveurs Ouverts</span>
              </div>
              <div style="display:flex;align-items:center;gap:8px;">
                <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="padding:3px 10px;font-size:11.8px;min-height:26px;" onclick="navigateFamily('PUB', 'PUB-16')">Agenda de la Semaine (4 événements)</button>
                <span class="price-pill" style="font-size:11.5px;padding:2px 9px;">Garantie Pluie : Report Gratuit 1 Clic</span>
              </div>
            </div>"""

    new_weather = """            <div class="ahala-live-weather-bar" id="ahalaLiveWeatherBar" role="status" aria-label="Météo et affluence en direct d'Ahala Barrière">
              <div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px;">
                <span class="ahala-live-pulse-dot" aria-hidden="true"></span>
                <strong>En direct d'Ahala :</strong>
                <span>27 °C Ensoleillé • Accès RN3 fluide (15 min) • Tous les espaces ouverts</span>
              </div>
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="padding:3px 10px;font-size:11.8px;min-height:26px;" onclick="navigateFamily('PUB', 'PUB-16')">Agenda de la Semaine</button>
                <span class="price-pill" style="font-size:11.5px;padding:2px 9px;">Garantie Pluie : Report Gratuit</span>
              </div>
            </div>"""

    if old_weather in html:
        html = html.replace(old_weather, new_weather, 1)

    old_hero_copy = """                <p class="lead-editorial" style="margin:18px 0 26px;max-width:640px;">
                  À 15 minutes du centre de Yaoundé (<strong>Ahala Barrière, face station Tradex</strong> — route 100 % bitumée), offrez à votre famille ou à vos équipes une vraie parenthèse loin des embouteillages : <strong>parc animalier avec notre gorille star « ToTo »</strong>, <strong>balade en pirogue sur le lac</strong>, <strong>piscine moderne surveillée</strong>, <strong>poisson frais des étangs braisé à la minute au Château des Saveurs</strong>, nos <strong>3 hôtels au calme (Ewondo, Chanthel, Bene)</strong> et notre <strong>Centre de Formation Professionnelle (CFP)</strong>.
                </p>
                <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px;">
                  <button type="button" class="btn btn-primary" onclick="navigateFamily('RES', 'RES-03')">Simuler mon budget en FCFA & Réserver</button>
                  <button type="button" class="btn btn-secondary btn-ochre-outline" onclick="openRdvModalSprint1('reperage_mariage')"><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg> Prendre RDV (Mariage / Séminaire / CFP)</button>
                  <button type="button" class="btn btn-secondary" onclick="inspectScreen('PUB-10')">Tarifs officiels</button>
                </div>"""

    new_hero_copy = """                <p class="lead-editorial" style="margin:16px 0 22px;max-width:600px;">
                  À 15 minutes du centre de Yaoundé (<strong>Ahala Barrière, face station Tradex</strong>), ressourcez-vous au cœur d'un domaine verdoyant réunissant <strong>parc animalier, lac et pirogues, piscine semi-olympique, gastronomie camerounaise, loges hôtelières et campus CFP</strong>.
                </p>
                <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px;">
                  <button type="button" class="btn btn-primary" onclick="navigateFamily('RES', 'RES-03')">Simuler mon budget en FCFA & Réserver</button>
                  <button type="button" class="btn btn-secondary btn-ochre-outline" onclick="openRdvModalSprint1('reperage_mariage')"><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg> Prendre RDV (Mariage / Séminaire / CFP)</button>
                  <button type="button" class="btn btn-secondary admin-only-control" onclick="inspectScreen('PUB-10')">Tarifs officiels</button>
                </div>"""

    if old_hero_copy in html:
        html = html.replace(old_hero_copy, new_hero_copy, 1)

    # 5. Clean up Bento Cards (#sec-PUB-03) : hide dead secondary buttons in visitor mode & fix CFP image
    html = html.replace(
        '<button class="btn btn-secondary btn-sm" onclick="inspectScreen(\'PUB-04\')">Fiche détail<span class="tech-code-tag"> (PUB-04)</span></button>',
        '<button class="btn btn-secondary btn-sm admin-only-control" onclick="inspectScreen(\'PUB-04\')">Fiche détail<span class="tech-code-tag"> (PUB-04)</span></button>',
    )
    html = html.replace(
        '<button class="btn btn-secondary btn-sm" onclick="inspectScreen(\'PUB-06\')">Détails sécurité</button>',
        '<button class="btn btn-secondary btn-sm admin-only-control" onclick="inspectScreen(\'PUB-06\')">Détails sécurité</button>',
    )
    html = html.replace(
        '<button class="btn btn-secondary btn-sm" onclick="inspectScreen(\'PUB-07\')">Carte en FCFA</button>',
        '<button class="btn btn-secondary btn-sm admin-only-control" onclick="inspectScreen(\'PUB-07\')">Carte en FCFA</button>',
    )
    html = html.replace(
        '<button class="btn btn-secondary btn-sm" onclick="inspectScreen(\'PUB-09\')">Fiche Loge<span class="tech-code-tag"> (PUB-09)</span></button>',
        '<button class="btn btn-secondary btn-sm admin-only-control" onclick="inspectScreen(\'PUB-09\')">Fiche Loge<span class="tech-code-tag"> (PUB-09)</span></button>',
    )
    html = html.replace(
        '<img src="audit-assets/ecopark-real-media/1786968889976.jpg" alt="Centre de Formation Professionnelle CFP ECOPARK" />',
        '<img src="audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png" alt="Centre de Formation Professionnelle CFP ECOPARK" />',
    )
    html = html.replace(
        "Envoyer Proforma sur WhatsApp (+237 697 13 62 03)",
        "Envoyer sur WhatsApp",
    )

    # 6. Remove redundant 5-zone bullet list above the SVG interactive map in #sec-PUB-13
    old_zone_list = """                <ul style="padding-left:20px;font-size:15px;display:grid;gap:6px;">
                  <li><strong>Zone A (Entrée & Accueil)</strong> : Guichets billetterie, contrôle QR et boutique.</li>
                  <li><strong>Zone B (Cœur Vert)</strong> : Jardin zoologique, volières et allées botaniques ombragées.</li>
                  <li><strong>Zone C (Lac & Plein Air)</strong> : Embarcadère pirogues/pédalos, carrière équestre et aire de jeux.</li>
                  <li><strong>Zone D (Détente & Saveurs)</strong> : Piscine semi-olympique et restaurant <em>Le Château des Saveurs</em>.</li>
                  <li><strong>Zone E (Séjour & Formation)</strong> : Loges Ewondo, Chanthel, Bene et campus du CFP ECOPARK.</li>
                </ul>"""

    if old_zone_list in html:
        html = html.replace(old_zone_list, "", 1)

    # 7. Hide the redundant 3rd bullet line inside the 4 Weekly Agenda cards
    html = html.replace(
        '<div style="font-size:12.5px;color:var(--color-brand-deep);font-weight:600;">\n                    • Tarif enfant garanti à 500 FCFA • Immersion campus MINEFOP\n                  </div>',
        '<div class="agenda-meta-Highlight">• Tarif enfant garanti à 500 FCFA • Immersion campus MINEFOP</div>',
    )
    html = html.replace(
        '<div style="font-size:12.5px;color:#8E5617;font-weight:600;">\n                    • 4 pergolas disponibles • Parking sécurisé 150 places\n                  </div>',
        '<div class="agenda-meta-Highlight">• 4 pergolas disponibles • Parking sécurisé 150 places</div>',
    )
    html = html.replace(
        '<div style="font-size:12.5px;color:var(--color-brand-deep);font-weight:600;">\n                    • Pass Découverte tout-en-un • Sachet nutrition 500 FCFA\n                  </div>',
        '<div class="agenda-meta-Highlight">• Pass Découverte tout-en-un • Sachet nutrition 500 FCFA</div>',
    )
    html = html.replace(
        '<div style="font-size:12.5px;color:#8E5617;font-weight:700;">\n                    • Le plus réservé • Service prioritaire 12h30 / 13h30 sur QR\n                  </div>',
        '<div class="agenda-meta-Highlight">• Le plus réservé • Service prioritaire 12h30 / 13h30 sur QR</div>',
    )

    # 8. Wrap #liveAvailabilityBarometer in a compact <details class="clean-details-accordion">
    barom_start = '                <!-- VOLET A : BAROMÈTRE TEMPS RÉEL DES DISPONIBILITÉS (LIBRE / PRÉ-RÉSERVÉ 11H / OCCUPÉ-COMPLET) -->\n                <div class="availability-barometer-card" id="liveAvailabilityBarometer" aria-live="polite">'
    barom_end = """                      <span class="avail-dot-pill avail-dot-free" id="baromHallShuttleStatus">Salle Libre • Navettes dispo.</span>
                    </div>
                  </div>
                </div>"""

    if 'id="barometerAccordion"' not in html and barom_start in html and barom_end in html:
        html = html.replace(
            barom_start,
            """                <!-- VOLET A : BAROMÈTRE TEMPS RÉEL DES DISPONIBILITÉS (ACCORDÉON COMPACT) -->
                <details class="clean-details-accordion" id="barometerAccordion">
                  <summary>
                    <span>● Stock &amp; Disponibilités en direct (<span id="barometerDateLabel">Date sélectionnée</span>) : Loges, Pergolas 13h &amp; Salle Menkii</span>
                  </summary>
                  <div class="accordion-inner-body">
                    <div class="availability-barometer-card" id="liveAvailabilityBarometer" aria-live="polite" style="margin:0;border:none;padding:0;background:transparent;">""",
            1,
        )
        # Remove the duplicate id="barometerDateLabel" inside the inner row so there's only 1 ID
        html = html.replace(
            'État du Stock &amp; des Disponibilités en Direct (<span id="barometerDateLabel">Date sélectionnée</span>)',
            'Détail des quotas par espace (Protection anti-surréservation active)',
            1,
        )
        html = html.replace(
            barom_end,
            barom_end + "\n                  </div>\n                </details>",
            1,
        )

    # 9. Wrap #resCancellationPolicyCard in a compact <details class="clean-details-accordion">
    policy_start = '                  <!-- VOLET B : CHARTE OFFICIELLE REPORT GRATUIT (90J), ANNULATION & REMBOURSEMENT MOBILE MONEY -->\n                  <div class="policy-guarantee-card" id="resCancellationPolicyCard">'
    policy_end = """                      <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="flex:1;font-size:12px;" onclick="openRescheduleModal(getActiveTicketRef(), 'BOOKING', 'CANCEL_REFUND')">
                        Annuler / Demander un remboursement
                      </button>
                    </div>
                  </div>"""

    if 'id="policyAccordion"' not in html and policy_start in html and policy_end in html:
        html = html.replace(
            policy_start,
            """                  <!-- VOLET B : CHARTE OFFICIELLE REPORT GRATUIT (90J), ANNULATION & REMBOURSEMENT MOBILE MONEY -->
                  <details class="clean-details-accordion" id="policyAccordion">
                    <summary>
                      <span>Garantie Météo : Report 100 % Gratuit (90j) &amp; Remboursement Mobile Money</span>
                    </summary>
                    <div class="accordion-inner-body">
                      <div class="policy-guarantee-card" id="resCancellationPolicyCard" style="border:none;padding:0;background:transparent;">""",
            1,
        )
        html = html.replace(
            policy_end,
            policy_end + "\n                    </div>\n                  </details>",
            1,
        )

    # 10. Wrap #whatsappConciergeCard in a collapsible <details class="clean-details-accordion" id="waConciergeAccordion">
    wa_start = '                <div class="wa-concierge-shell" id="whatsappConciergeCard">'
    wa_end = """                      <button type="button" class="btn btn-secondary btn-sm" style="flex:1;background:#FFFFFF;color:var(--color-brand-deep);border-color:#FFFFFF;font-weight:700;" onclick="sendWhatsAppBooking()">
                        <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> Ouvrir dans mon WhatsApp (+237 697 13 62 03)
                      </button>
                    </div>
                  </div>
                </div>"""

    if 'id="waConciergeAccordion"' not in html and wa_start in html and wa_end in html:
        html = html.replace(
            wa_start,
            """                <details class="clean-details-accordion" id="waConciergeAccordion">
                  <summary>
                    <span>Guichet Unique &amp; Portefeuille WhatsApp (+237 697 13 62 03) — Bon pré-calculé</span>
                  </summary>
                  <div class="accordion-inner-body" style="padding:10px;">
                    <div class="wa-concierge-shell" id="whatsappConciergeCard" style="border:none;box-shadow:none;padding:8px;">""",
            1,
        )
        html = html.replace(
            wa_end,
            wa_end + "\n                  </div>\n                </details>",
            1,
        )

    # 11. Inject JS_DECLUTTER before </script>
    if "function syncProgressiveDisclosureSimulator" not in html:
        html = html.replace("  </script>\n</body>", JS_DECLUTTER + "\n  </script>\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Applied Declutter Upgrade to {filepath} ({len(html)} bytes)")


if __name__ == "__main__":
    for p in FILES:
        if os.path.exists(p):
            apply_declutter(p)
