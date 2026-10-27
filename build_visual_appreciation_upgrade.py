# -*- coding: utf-8 -*-
import os

FILES = [
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\etape0-site-live\index.html",
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

CSS_VISUAL_APPRECIATION = """
    /* ==========================================================================
       DISPOSITIF « ZÉRO RÉSERVATION À L'AVEUGLE » — APPRÉCIATION VISUELLE TOTALE
       ========================================================================== */
    .agenda-card-media {
      position: relative;
      height: 152px;
      border-radius: 16px;
      overflow: hidden;
      margin-bottom: 10px;
      cursor: pointer;
      background: var(--color-surface-soft);
      border: 1px solid rgba(29, 73, 13, 0.12);
    }
    .agenda-card-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .agenda-event-card:hover .agenda-card-media img {
      transform: scale(1.06);
    }
    .agenda-card-zoom-tag {
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(20, 34, 17, 0.78);
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 980px;
      backdrop-filter: blur(6px);
    }
    .sim-item-thumb {
      width: 54px;
      height: 54px;
      border-radius: 10px;
      object-fit: cover;
      flex-shrink: 0;
      border: 1.5px solid rgba(29, 73, 13, 0.18);
      cursor: zoom-in;
      transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
      background: var(--color-surface-soft);
    }
    .sim-item-thumb:hover {
      transform: scale(1.08);
      border-color: #C47D2B;
      box-shadow: 0 6px 16px rgba(196, 125, 43, 0.25);
    }
    .lodge-visual-preview-card {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      border-radius: 12px;
      background: linear-gradient(90deg, #FFFFFF 0%, #FBF5EC 100%);
      border: 1px solid rgba(196, 125, 43, 0.38);
      margin-top: 4px;
    }
    .lodge-visual-preview-card img {
      width: 88px;
      height: 66px;
      border-radius: 10px;
      object-fit: cover;
      flex-shrink: 0;
      cursor: zoom-in;
      border: 1.5px solid rgba(196, 125, 43, 0.45);
    }
    .selected-visual-strip-box {
      padding: 10px 12px;
      border-radius: 12px;
      background: #FFFFFF;
      border: 1px solid rgba(29, 73, 13, 0.16);
      margin: 6px 0;
    }
    .selected-visual-strip-track {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 4px;
      margin-top: 6px;
      scrollbar-width: thin;
    }
    .selected-strip-chip {
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 5px 9px 5px 5px;
      border-radius: 10px;
      background: var(--color-surface-soft);
      border: 1px solid rgba(29, 73, 13, 0.14);
      flex-shrink: 0;
      cursor: pointer;
      transition: border-color 0.2s ease, background 0.2s ease;
    }
    .selected-strip-chip:hover {
      border-color: #C47D2B;
      background: #FBF5EC;
    }
    .selected-strip-chip img {
      width: 38px;
      height: 38px;
      border-radius: 7px;
      object-fit: cover;
    }
    .modal-visual-preview-banner {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      margin: 10px 0 6px;
      border-radius: 12px;
      background: linear-gradient(90deg, #EDF4E7 0%, #FBF5EC 100%);
      border: 1px solid rgba(29, 73, 13, 0.18);
    }
    .modal-visual-preview-banner img {
      width: 96px;
      height: 68px;
      border-radius: 10px;
      object-fit: cover;
      flex-shrink: 0;
      cursor: zoom-in;
      border: 1.5px solid rgba(29, 73, 13, 0.22);
    }
    .acc-row-thumb {
      width: 44px;
      height: 44px;
      border-radius: 8px;
      object-fit: cover;
      flex-shrink: 0;
      border: 1px solid rgba(29, 73, 13, 0.18);
      cursor: zoom-in;
    }
"""

JS_VISUAL_APPRECIATION = """
    // ========================================================================
    // MOTEUR D'APPRÉCIATION VISUELLE CONTEXTUELLE (« ZÉRO RÉSERVATION À L'AVEUGLE »)
    // ========================================================================
    const VISUAL_APPRECIATION_CATALOG = {
      ACTIVITIES: [
        {
          chkId: 'chkZoo',
          title: 'Parc Animalier (« ToTo ») & Forêt',
          price: '500 / 1 000 FCFA',
          src: 'audit-assets/ecopark-real-media/chimpanze.jpeg',
          lbIdx: 7
        },
        {
          chkId: 'chkPiscine',
          title: 'Piscine Semi-Olympique Surveillée',
          price: '1 500 / 2 500 FCFA',
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png',
          lbIdx: 1
        },
        {
          chkId: 'chkPirogue',
          title: "Balade en Pirogue sur le Lac d'Ahala",
          price: '500 / 1 000 FCFA',
          src: 'audit-assets/ecopark-real-media/balade_pirogue3.jpg',
          lbIdx: 0
        },
        {
          chkId: 'chkCheval',
          title: 'Équitation & Manèges Plein Air',
          price: '500 / 1 000 FCFA',
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png',
          lbIdx: 3
        },
        {
          chkId: 'chkRepas',
          title: 'Le Château des Saveurs (Gastronomie)',
          price: '2 500 / 5 000 FCFA',
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
          lbIdx: 2
        },
        {
          chkId: 'chkBumpNutrition',
          title: 'Nourrissage Poissons & Tortues',
          price: '500 FCFA / enfant',
          src: 'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg',
          lbIdx: 5
        },
        {
          chkId: 'chkBumpPergola',
          title: 'Pergola Privée Bord du Lac 13h',
          price: '+5 000 FCFA',
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
          lbIdx: 2
        },
        {
          chkId: 'chkBumpLodgeEwondo',
          title: 'Séjour Cités Hôtelières (Ewondo/Chanthel/Bene)',
          price: '10 000 – 30 000 FCFA',
          src: 'audit-assets/ecopark-real-media/chambre.jpeg',
          lbIdx: 8
        },
        {
          chkId: 'chkBumpNavette',
          title: 'Navette Climatisée A/R Yaoundé',
          price: '1 000 / 1 500 FCFA',
          src: 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg',
          lbIdx: 4
        },
        {
          chkId: 'chkBumpPeche',
          title: 'Pêche Ludique aux Étangs & Musée',
          price: '+2 000 FCFA',
          src: 'audit-assets/ecopark-real-media/balade_pirogue3.jpg',
          lbIdx: 0
        }
      ],
      LODGES: {
        EWONDO: {
          title: 'Cité Ewondo — Suite VIP Climatisée (Standing Prestige)',
          rate: '25 000 – 30 000 FCFA / nuit',
          desc: "Suite climatisée avec literie King-Size, coin salon, salle d'eau privative, petit-déjeuner et accès privilégié Piscine & Zoo.",
          src: 'audit-assets/ecopark-real-media/chambre.jpeg',
          lbIdx: 8
        },
        CHANTHEL: {
          title: 'Cité Chanthel — Loge Confort Familiale & Couples',
          rate: '15 000 – 25 000 FCFA / nuit',
          desc: "Chambre spacieuse au calme sous la canopée d'Ahala, salle de bain privative, terrasse ombragée et service en chambre depuis Le Château des Saveurs.",
          src: 'audit-assets/ecopark-real-media/chambre.jpeg',
          lbIdx: 8
        },
        BENE: {
          title: 'Cité Bene — Loge Standard Calme & Nature',
          rate: '10 000 – 15 000 FCFA / nuit',
          desc: "Idéal pour le repos en journée ou une nuitée nature accessible au cœur du parc d'Ahala (réception ouverte 24h/24).",
          src: 'audit-assets/ecopark-real-media/chambre.jpeg',
          lbIdx: 8
        }
      },
      DISHES: {
        "Poisson Braisé d'Ahala (Étang frais)": {
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
          lbIdx: 2,
          desc: 'Poisson frais pêché dans les étangs d’Ahala et braisé à la minute aux épices du terroir, servi avec plantains mûrs ou miondo.'
        },
        "Poulet DG Royal Plantain Mûr": {
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
          lbIdx: 2,
          desc: 'Le grand classique camerounais du Château des Saveurs : volaille fermière, plantains mûrs dorés, légumes frais et sauce parfumée.'
        },
        "Ndolé Royal Crevettes & Miondo": {
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
          lbIdx: 2,
          desc: 'Ndolé onctueux préparé selon la tradition avec crevettes, bœuf fondant et accompagnements chauds.'
        },
        "Menu Enfant & Grillades Douces": {
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png',
          lbIdx: 3,
          desc: 'Portion adaptée aux enfants (3–12 ans) avec grillades tendres, frites de plantain et jus naturel (Bissap / Ananas).'
        }
      },
      EVENTS: {
        EVT_MERCREDI_CFP: {
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png',
          lbIdx: 6
        },
        EVT_VENDREDI_AFTERWORK: {
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
          lbIdx: 2
        },
        EVT_SAMEDI_FAMILLE: {
          src: 'audit-assets/ecopark-real-media/balade_pirogue3.jpg',
          lbIdx: 0
        },
        EVT_DIMANCHE_ROYAL: {
          src: 'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg',
          lbIdx: 5
        }
      },
      RDV_PURPOSES: {
        reperage_mariage: {
          title: 'Aperçu : Salle Polyvalente « Menkii Essomba Anton » & Esplanade Gala',
          desc: 'Cadre prestigieux pour mariages, galas et réceptions avec service traiteur du Château des Saveurs.',
          src: 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg',
          lbIdx: 4
        },
        seminaire_b2b: {
          title: 'Aperçu : Configuration Séminaire B2B, Ministères, ONG & Loges VIP',
          desc: 'Salle équipée, pauses-café, déjeuners exécutifs et hébergement dans les Cités Ewondo, Chanthel & Bene.',
          src: 'audit-assets/ecopark-real-media/chambre.jpeg',
          lbIdx: 8
        },
        visite_ecole: {
          title: 'Aperçu : Circuit Pédagogique & Sécurité Excursions Scolaires',
          desc: 'Parcours encadré : Jardin Zoologique (« ToTo »), étangs piscicoles, pirogues avec gilets et piscine surveillée.',
          src: 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg',
          lbIdx: 4
        },
        orientation_cfp: {
          title: 'Aperçu : Campus & Ateliers Pratiques du CFP ECOPARK (MINEFOP)',
          desc: 'Immersion directe dans les 5 filières professionnelles (Hôtellerie, Restauration, Décoration, Agro, Pisciculture).',
          src: 'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png',
          lbIdx: 6
        }
      }
    };

    function mountSimulatorThumbnails() {
      VISUAL_APPRECIATION_CATALOG.ACTIVITIES.forEach(item => {
        const chk = document.getElementById(item.chkId);
        if (!chk) return;
        const container = chk.closest('label') || chk.parentElement;
        if (!container || container.querySelector('.sim-item-thumb')) return;
        const spanWrap = chk.parentElement;
        if (spanWrap) {
          spanWrap.style.display = 'inline-flex';
          spanWrap.style.alignItems = 'center';
          spanWrap.style.gap = '8px';
          const img = document.createElement('img');
          img.className = 'sim-item-thumb';
          img.src = item.src;
          img.alt = item.title;
          img.title = 'Cliquer pour apprécier la photo en grand format (HD)';
          img.onclick = function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            openEcoparkLightbox(item.lbIdx);
          };
          spanWrap.insertBefore(img, chk.nextSibling);
        }
      });
    }

    function syncVisualAppreciationSimulator() {
      // 1. Carte d'appréciation visuelle de la Cité Hôtelière sélectionnée
      const lodgeSelect = document.getElementById('lodgeCitySelect');
      const cityKey = (lodgeSelect && lodgeSelect.value) ? lodgeSelect.value : 'EWONDO';
      const lodgeMeta = VISUAL_APPRECIATION_CATALOG.LODGES[cityKey] || VISUAL_APPRECIATION_CATALOG.LODGES.EWONDO;
      const lodgeImg = document.getElementById('lodgeVisualPreviewImg');
      const lodgeTitle = document.getElementById('lodgeVisualPreviewTitle');
      const lodgeDesc = document.getElementById('lodgeVisualPreviewDesc');
      const lodgeRate = document.getElementById('lodgeVisualPreviewRate');
      if (lodgeImg) {
        lodgeImg.src = lodgeMeta.src;
        lodgeImg.onclick = () => openEcoparkLightbox(lodgeMeta.lbIdx);
      }
      if (lodgeTitle) lodgeTitle.textContent = lodgeMeta.title;
      if (lodgeDesc) lodgeDesc.textContent = lodgeMeta.desc;
      if (lodgeRate) lodgeRate.textContent = lodgeMeta.rate;

      // 2. Aperçu visuel du plat sélectionné dans #kitchenPreorderSubpanel
      const dishSelect = document.getElementById('simDishSelect');
      const slotSelect = document.getElementById('simMealSlotSelect');
      const dishKey = (dishSelect && dishSelect.value) || "Poisson Braisé d'Ahala (Étang frais)";
      const slotVal = (slotSelect && slotSelect.value) || 'Service 12h30';
      const dishMeta = VISUAL_APPRECIATION_CATALOG.DISHES[dishKey] || VISUAL_APPRECIATION_CATALOG.DISHES["Poisson Braisé d'Ahala (Étang frais)"];
      const dishImg = document.getElementById('kitchenVisualPreviewImg');
      const dishTitle = document.getElementById('kitchenVisualPreviewTitle');
      const dishDesc = document.getElementById('kitchenVisualPreviewDesc');
      if (dishImg) {
        dishImg.src = dishMeta.src;
        dishImg.onclick = () => openEcoparkLightbox(dishMeta.lbIdx);
      }
      if (dishTitle) dishTitle.textContent = `${dishKey} • ${slotVal}`;
      if (dishDesc) dishDesc.textContent = dishMeta.desc;

      // 3. Pellicule dynamique « Votre Visite Sélectionnée en Images » (#simSelectedVisualStripTrack)
      const track = document.getElementById('simSelectedVisualStripTrack');
      const countBadge = document.getElementById('simSelectedVisualCountBadge');
      if (track) {
        const activeItems = [];
        if (window._selectedWeeklyEventTitle && window._currentAgendaEventCode) {
          const evVis = VISUAL_APPRECIATION_CATALOG.EVENTS[window._currentAgendaEventCode] || VISUAL_APPRECIATION_CATALOG.EVENTS.EVT_DIMANCHE_ROYAL;
          activeItems.push({
            title: window._selectedWeeklyEventTitle,
            price: 'Événement Semaine',
            src: evVis.src,
            lbIdx: evVis.lbIdx
          });
        }
        VISUAL_APPRECIATION_CATALOG.ACTIVITIES.forEach(item => {
          const chk = document.getElementById(item.chkId);
          if (chk && chk.checked) {
            if (item.chkId === 'chkBumpLodgeEwondo') {
              activeItems.push({
                title: lodgeMeta.title.split('—')[0].trim(),
                price: lodgeMeta.rate,
                src: lodgeMeta.src,
                lbIdx: lodgeMeta.lbIdx
              });
            } else {
              activeItems.push(item);
            }
          }
        });

        if (countBadge) {
          countBadge.textContent = `${activeItems.length} expérience(s) en aperçu HD`;
        }
        track.innerHTML = activeItems.map(it => `
          <div class="selected-strip-chip" onclick="openEcoparkLightbox(${it.lbIdx})" title="Cliquer pour agrandir la photo en plein écran">
            <img src="${it.src}" alt="${it.title}" />
            <div>
              <strong style="display:block;font-size:12px;color:var(--color-brand-deep);line-height:1.2;">${it.title}</strong>
              <span style="font-size:11px;color:var(--color-text-muted);">${it.price}</span>
            </div>
          </div>
        `).join('');
      }
    }

    function syncModalsVisualAppreciation() {
      // A. Modale Devis Groupe (#modalQuoteBox)
      const qType = ((document.getElementById('quoteType') || {}).value || '');
      const qImg = document.getElementById('quoteVisualPreviewImg');
      const qTitle = document.getElementById('quoteVisualPreviewTitle');
      const qDesc = document.getElementById('quoteVisualPreviewDesc');
      if (qImg && qTitle && qDesc) {
        if (qType.includes('Séminaire')) {
          qImg.src = 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg';
          qImg.onclick = () => openEcoparkLightbox(4);
          qTitle.textContent = 'Salle Polyvalente « Menkii Essomba Anton » & Suites Cité Ewondo';
          qDesc.textContent = 'Configuration conférence climatisée, pauses-café, buffet Château des Saveurs et navettes 18/32 places.';
        } else if (qType.includes('Mariage') || qType.includes('Réunion')) {
          qImg.src = 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png';
          qImg.onclick = () => openEcoparkLightbox(2);
          qTitle.textContent = 'Réceptions, Mariages & Galas au Bord du Lac d’Ahala';
          qDesc.textContent = 'Privatisation Salle Menkii Essomba Anton + Esplanade Plein Air, décoration et banquet camerounais.';
        } else {
          qImg.src = 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg';
          qImg.onclick = () => openEcoparkLightbox(4);
          qTitle.textContent = 'Excursion Scolaire Pédagogique & Sécurisée à Ahala';
          qDesc.textContent = 'Tarif enfant protégé à 500 FCFA, visite guidée du Zoo (« ToTo »), étangs piscicoles et piscine surveillée.';
        }
      }

      // B. Modale Prise de RDV (#modalRdvBox)
      const rdvCode = ((document.getElementById('rdvPurposeCode') || {}).value || 'reperage_mariage');
      const rdvMeta = VISUAL_APPRECIATION_CATALOG.RDV_PURPOSES[rdvCode] || VISUAL_APPRECIATION_CATALOG.RDV_PURPOSES.reperage_mariage;
      const rImg = document.getElementById('rdvVisualPreviewImg');
      const rTitle = document.getElementById('rdvVisualPreviewTitle');
      const rDesc = document.getElementById('rdvVisualPreviewDesc');
      if (rImg && rTitle && rDesc) {
        rImg.src = rdvMeta.src;
        rImg.onclick = () => openEcoparkLightbox(rdvMeta.lbIdx);
        rTitle.textContent = rdvMeta.title;
        rDesc.textContent = rdvMeta.desc;
      }

      // C. Modale Candidature CFP (#modalCfpBox)
      const cfpTrack = ((document.getElementById('cfpTrack') || {}).value || 'Hôtellerie');
      const cImg = document.getElementById('cfpVisualPreviewImg');
      const cTitle = document.getElementById('cfpVisualPreviewTitle');
      const cDesc = document.getElementById('cfpVisualPreviewDesc');
      if (cImg && cTitle && cDesc) {
        if (cfpTrack === 'Hôtellerie') {
          cImg.src = 'audit-assets/ecopark-real-media/chambre.jpeg';
          cImg.onclick = () => openEcoparkLightbox(8);
          cTitle.textContent = 'Filière Hôtellerie — Stage Pratique dans nos 3 Cités (Ewondo, Chanthel, Bene)';
          cDesc.textContent = 'Apprentissage concret de la réception 24h/24, du gouvernantat et de la gestion hôtelière sur site.';
        } else if (cfpTrack === 'Restauration') {
          cImg.src = 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png';
          cImg.onclick = () => openEcoparkLightbox(2);
          cTitle.textContent = 'Filière Restauration — Stage Pratique au Château des Saveurs';
          cDesc.textContent = 'Maîtrise de la cuisine camerounaise et internationale, brigade, grillades et service banquet.';
        } else {
          cImg.src = 'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png';
          cImg.onclick = () => openEcoparkLightbox(6);
          cTitle.textContent = `Filière ${cfpTrack} — Campus & Bassins d'Application CFP ECOPARK`;
          cDesc.textContent = '70 % de travaux pratiques sur les installations réelles du complexe d’Ahala (Diplôme DQP / CQP MINEFOP).';
        }
      }
    }

    function decorateAccTableWithVisuals() {
      document.querySelectorAll('#view-ACC table tbody tr[data-dossier-kind]').forEach(tr => {
        const kind = tr.getAttribute('data-dossier-kind');
        const tdInfo = tr.children[2];
        if (!tdInfo || tdInfo.querySelector('.acc-row-thumb')) return;
        const text = tdInfo.textContent || '';
        let src = 'audit-assets/ecopark-real-media/balade_pirogue3.jpg';
        let lbIdx = 0;
        if (kind === 'CFP' || text.includes('CFP')) {
          src = 'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png';
          lbIdx = 6;
        } else if (kind === 'QUOTE' || text.includes('École') || text.includes('Scolaire')) {
          src = 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg';
          lbIdx = 4;
        } else if (text.includes('Ewondo') || text.includes('Chanthel') || text.includes('Bene')) {
          src = 'audit-assets/ecopark-real-media/chambre.jpeg';
          lbIdx = 8;
        } else if (text.includes('Saveurs') || text.includes('Dimanche') || text.includes('Poulet') || text.includes('Poisson')) {
          src = 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png';
          lbIdx = 2;
        } else if (kind === 'RDV') {
          src = 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg';
          lbIdx = 4;
        }
        const innerHtml = tdInfo.innerHTML;
        tdInfo.innerHTML = `
          <div style="display:flex;align-items:center;gap:10px;">
            <img src="${src}" alt="Aperçu réservation" class="acc-row-thumb" onclick="openEcoparkLightbox(${lbIdx})" title="Cliquer pour voir le visuel HD de cette prestation" />
            <div>${innerHtml}</div>
          </div>
        `;
      });
    }

    // Surcharger openWeeklyEventDetail & bookWeeklyEventInOneClick pour synchroniser la photo de l'événement
    if (typeof openWeeklyEventDetail === 'function') {
      const _prevOpenEvt = openWeeklyEventDetail;
      openWeeklyEventDetail = function(eventCode) {
        _prevOpenEvt(eventCode);
        const vis = VISUAL_APPRECIATION_CATALOG.EVENTS[eventCode] || VISUAL_APPRECIATION_CATALOG.EVENTS.EVT_DIMANCHE_ROYAL;
        const modalImg = document.getElementById('evtModalHeroImg');
        if (modalImg) {
          modalImg.src = vis.src;
          modalImg.onclick = () => openEcoparkLightbox(vis.lbIdx);
        }
      };
    }

    if (typeof bookWeeklyEventInOneClick === 'function') {
      const _prevBookEvt = bookWeeklyEventInOneClick;
      bookWeeklyEventInOneClick = function(eventCode) {
        const res = _prevBookEvt(eventCode);
        const vis = VISUAL_APPRECIATION_CATALOG.EVENTS[eventCode] || VISUAL_APPRECIATION_CATALOG.EVENTS.EVT_DIMANCHE_ROYAL;
        const simThumb = document.getElementById('activeEventSimThumb');
        if (simThumb) {
          simThumb.src = vis.src;
          simThumb.onclick = () => openEcoparkLightbox(vis.lbIdx);
        }
        syncVisualAppreciationSimulator();
        return res;
      };
    }

    const _origRecalcBeforeVisuals = recalcSimulator;
    recalcSimulator = function() {
      _origRecalcBeforeVisuals();
      syncVisualAppreciationSimulator();
    };

    const _origQuotePrevBeforeVisuals = recalcQuoteProformaPreview;
    recalcQuoteProformaPreview = function() {
      _origQuotePrevBeforeVisuals();
      syncModalsVisualAppreciation();
    };

    const _origSelectRdvBeforeVisuals = selectRdvPurpose;
    selectRdvPurpose = function(code, btnEl) {
      _origSelectRdvBeforeVisuals(code, btnEl);
      syncModalsVisualAppreciation();
    };

    const _origSyncAllBeforeVisuals = syncAllViewsFromDB;
    syncAllViewsFromDB = function() {
      _origSyncAllBeforeVisuals();
      decorateAccTableWithVisuals();
    };

    const cfpTrackEl = document.getElementById('cfpTrack');
    if (cfpTrackEl) {
      cfpTrackEl.addEventListener('change', syncModalsVisualAppreciation);
    }

    mountSimulatorThumbnails();
    syncVisualAppreciationSimulator();
    syncModalsVisualAppreciation();
    decorateAccTableWithVisuals();
"""


def inject_visual_appreciation(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject CSS
    if ".lodge-visual-preview-card" not in html:
        html = html.replace("  </style>", CSS_VISUAL_APPRECIATION + "\n  </style>", 1)

    # 2. Add HD Media Headers on the 4 Weekly Agenda Cards (#weeklyAgendaGrid)
    card1_target = """              <!-- Événement 1 : Mercredi & Jeudi -->
              <div class="col-3 agenda-event-card" data-agenda-day="MER_JEU">
                <div>"""
    card1_replace = """              <!-- Événement 1 : Mercredi & Jeudi -->
              <div class="col-3 agenda-event-card" data-agenda-day="MER_JEU">
                <div>
                  <div class="agenda-card-media" onclick="openEcoparkLightbox(6)">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png" alt="Journée Pédagogique Faune & Portes Ouvertes CFP ECOPARK" />
                    <span class="agenda-card-zoom-tag">Aperçu HD</span>
                  </div>"""
    if 'class="agenda-card-media"' not in html and card1_target in html:
        html = html.replace(card1_target, card1_replace, 1)

    card2_target = """              <!-- Événement 2 : Vendredi Afterwork -->
              <div class="col-3 agenda-event-card" data-agenda-day="VENDREDI">
                <div>"""
    card2_replace = """              <!-- Événement 2 : Vendredi Afterwork -->
              <div class="col-3 agenda-event-card" data-agenda-day="VENDREDI">
                <div>
                  <div class="agenda-card-media" onclick="openEcoparkLightbox(2)">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Afterwork Brise du Lac & Poisson Braisé d'Ahala" />
                    <span class="agenda-card-zoom-tag">Aperçu HD</span>
                  </div>"""
    if card2_target in html:
        html = html.replace(card2_target, card2_replace, 1)

    card3_target = """              <!-- Événement 3 : Samedi Famille -->
              <div class="col-3 agenda-event-card" data-agenda-day="SAMEDI">
                <div>"""
    card3_replace = """              <!-- Événement 3 : Samedi Famille -->
              <div class="col-3 agenda-event-card" data-agenda-day="SAMEDI">
                <div>
                  <div class="agenda-card-media" onclick="openEcoparkLightbox(0)">
                    <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Samedi Famille : Rencontre Gorille ToTo & Pirogues" />
                    <span class="agenda-card-zoom-tag">Aperçu HD</span>
                  </div>"""
    if card3_target in html:
        html = html.replace(card3_target, card3_replace, 1)

    card4_target = """              <!-- Événement 4 : Dimanche Royal (Mis en avant) -->
              <div class="col-3 agenda-event-card agenda-event-card-featured" data-agenda-day="DIMANCHE">
                <div>"""
    card4_replace = """              <!-- Événement 4 : Dimanche Royal (Mis en avant) -->
              <div class="col-3 agenda-event-card agenda-event-card-featured" data-agenda-day="DIMANCHE">
                <div>
                  <div class="agenda-card-media" onclick="openEcoparkLightbox(5)">
                    <img src="audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg" alt="Grand Dimanche Royal : Buffet Camerounais & Live" />
                    <span class="agenda-card-zoom-tag">Aperçu HD</span>
                  </div>"""
    if card4_target in html:
        html = html.replace(card4_target, card4_replace, 1)

    # 3. Add visual thumbnail in #activeEventBannerSimulator
    banner_sim_target = """                <div class="active-event-sim-banner" id="activeEventBannerSimulator">
                  <div>"""
    banner_sim_replace = """                <div class="active-event-sim-banner" id="activeEventBannerSimulator">
                  <div style="display:flex;align-items:center;gap:12px;">
                    <img id="activeEventSimThumb" src="audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg" alt="Aperçu événement sélectionné" class="sim-item-thumb" onclick="openEcoparkLightbox(5)" />
                    <div>"""
    banner_sim_end_target = """                    <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);" id="activeEventSimTitle">Grand Dimanche Royal : Buffet Camerounais &amp; Live</strong>
                  </div>"""
    banner_sim_end_replace = """                    <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);" id="activeEventSimTitle">Grand Dimanche Royal : Buffet Camerounais &amp; Live</strong>
                    </div>
                  </div>"""
    if "activeEventSimThumb" not in html and banner_sim_target in html:
        html = html.replace(banner_sim_target, banner_sim_replace, 1)
        html = html.replace(banner_sim_end_target, banner_sim_end_replace, 1)

    # 4. Add visual dish preview inside #kitchenPreorderSubpanel
    kitchen_target = """                        <select id="simMealSlotSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Service 12h30" selected>12h30 — Zéro attente (Prioritaire)</option>
                          <option value="Service 13h30">13h30 — Cœur de journée</option>
                          <option value="Service 15h00">15h00 — Après-midi au bord du lac</option>
                        </select>
                      </div>
                    </div>"""
    kitchen_replace = kitchen_target[:-26] + """                      </div>
                      <div id="kitchenVisualPreviewBox" style="grid-column:1 / -1;display:flex;align-items:center;gap:10px;padding:8px 10px;background:#FFFFFF;border-radius:8px;border:1px solid rgba(29,73,13,0.14);">
                        <img id="kitchenVisualPreviewImg" src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Aperçu spécialité Château des Saveurs" class="sim-item-thumb" onclick="openEcoparkLightbox(2)" />
                        <div style="font-size:12px;">
                          <strong style="color:var(--color-brand-deep);display:block;" id="kitchenVisualPreviewTitle">Poisson Braisé d'Ahala (Étang frais) • Service 12h30</strong>
                          <span style="color:var(--color-text-muted);" id="kitchenVisualPreviewDesc">Poisson frais pêché dans les étangs d’Ahala et braisé à la minute, servi sous pergola au bord de l'eau.</span>
                        </div>
                      </div>
                    </div>"""
    if "kitchenVisualPreviewBox" not in html and kitchen_target in html:
        html = html.replace(kitchen_target, kitchen_replace, 1)

    # 5. Add dynamic Lodge Visual Appreciation Card (#lodgeVisualPreviewCard) right under #lodgeCitySelect row
    lodge_row_target = """                        <span class="price-pill" id="subBumpLodge">0 FCFA</span>
                      </div>
                    </div>"""
    lodge_row_replace = lodge_row_target + """
                    <!-- APERÇU VISUEL DYNAMIQUE DE LA CITÉ HÔTELIÈRE SÉLECTIONNÉE -->
                    <div class="lodge-visual-preview-card" id="lodgeVisualPreviewCard">
                      <img id="lodgeVisualPreviewImg" src="audit-assets/ecopark-real-media/chambre.jpeg" alt="Aperçu chambre Cité Hôtelière ECOPARK" onclick="openEcoparkLightbox(8)" title="Cliquer pour agrandir la photo réelle de la chambre" />
                      <div style="flex:1;font-size:12.5px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;">
                          <strong style="color:var(--color-brand-deep);font-size:13.2px;" id="lodgeVisualPreviewTitle">Cité Ewondo — Suite VIP Climatisée (Standing Prestige)</strong>
                          <span class="price-pill" style="font-size:11px;padding:1px 8px;" id="lodgeVisualPreviewRate">25 000 – 30 000 FCFA / nuit</span>
                        </div>
                        <span style="color:var(--color-text-muted);display:block;margin-top:2px;" id="lodgeVisualPreviewDesc">Suite climatisée avec literie King-Size, coin salon, salle d'eau privative, petit-déjeuner et accès privilégié Piscine &amp; Zoo.</span>
                      </div>
                    </div>"""
    if "lodgeVisualPreviewCard" not in html and lodge_row_target in html:
        html = html.replace(lodge_row_target, lodge_row_replace, 1)

    # 6. Inject #simSelectedVisualStrip inside #resStickySummaryCol right after #cartBreakdown
    cart_target = """                  <div id="cartBreakdown" style="font-size:15px;display:grid;gap:6px;border-top:1px solid var(--color-border);border-bottom:1px solid var(--color-border);padding:12px 0;">
                    <!-- Injecté dynamiquement par recalcSimulator() -->
                  </div>"""
    cart_replace = cart_target + """
                  <!-- PELLICULE VISUELLE DYNAMIQUE « VOTRE SÉLECTION EN IMAGES » -->
                  <div class="selected-visual-strip-box" id="simSelectedVisualStrip">
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
                      <strong style="font-size:12.5px;color:var(--color-brand-deep);">Aperçu en images de votre sélection :</strong>
                      <span class="price-pill" style="font-size:11px;padding:1px 8px;" id="simSelectedVisualCountBadge">3 expérience(s) en aperçu HD</span>
                    </div>
                    <div class="selected-visual-strip-track" id="simSelectedVisualStripTrack"></div>
                  </div>"""
    if "simSelectedVisualStrip" not in html and cart_target in html:
        html = html.replace(cart_target, cart_replace, 1)

    # 7. Inject visual banners inside #modalQuoteBox, #modalCfpBox, #modalRdvBox, #modalEventDetailBox
    quote_modal_target = """      <h3 style="margin-top:6px;">Demander un devis groupe sur-mesure</h3>"""
    quote_modal_replace = quote_modal_target + """
      <div class="modal-visual-preview-banner" id="quoteVisualPreviewBanner">
        <img id="quoteVisualPreviewImg" src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg" alt="Aperçu espace groupe ECOPARK" onclick="openEcoparkLightbox(4)" />
        <div style="font-size:12.8px;">
          <strong style="color:var(--color-brand-deep);display:block;" id="quoteVisualPreviewTitle">Excursion Scolaire Pédagogique &amp; Sécurisée à Ahala</strong>
          <span style="color:var(--color-text-muted);" id="quoteVisualPreviewDesc">Tarif enfant protégé à 500 FCFA, visite guidée du Zoo (« ToTo »), étangs piscicoles et piscine surveillée.</span>
        </div>
      </div>"""
    if "quoteVisualPreviewBanner" not in html and quote_modal_target in html:
        html = html.replace(quote_modal_target, quote_modal_replace, 1)

    html = html.replace(
        "src: 'audit-assets/stitch-canopee-vivante/local_cameroon_school_excursion.png'",
        "src: 'audit-assets/ecopark-real-media/IMG_20260829_172016-1-scaled.jpg'",
    )

    cfp_modal_target = """      <h3 style="margin-top:6px;">Candidature au CFP ECOPARK Yaoundé-Ahala</h3>"""
    cfp_modal_replace = cfp_modal_target + """
      <div class="modal-visual-preview-banner" id="cfpVisualPreviewBanner">
        <img id="cfpVisualPreviewImg" src="audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png" alt="Aperçu Campus CFP ECOPARK" onclick="openEcoparkLightbox(6)" />
        <div style="font-size:12.8px;">
          <strong style="color:var(--color-brand-deep);display:block;" id="cfpVisualPreviewTitle">Campus &amp; Bassins d'Application CFP ECOPARK (Agréé MINEFOP)</strong>
          <span style="color:var(--color-text-muted);" id="cfpVisualPreviewDesc">70 % de travaux pratiques sur les installations réelles du complexe d’Ahala (Diplôme DQP / CQP MINEFOP).</span>
        </div>
      </div>"""
    if "cfpVisualPreviewBanner" not in html and cfp_modal_target in html:
        html = html.replace(cfp_modal_target, cfp_modal_replace, 1)

    rdv_modal_target = """      <h3 style="margin-top:4px;">Planifier un Rendez-Vous Personnalisé</h3>"""
    rdv_modal_replace = rdv_modal_target + """
      <div class="modal-visual-preview-banner" id="rdvVisualPreviewBanner">
        <img id="rdvVisualPreviewImg" src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg" alt="Aperçu lieu de rendez-vous ECOPARK" onclick="openEcoparkLightbox(4)" />
        <div style="font-size:12.8px;">
          <strong style="color:var(--color-brand-deep);display:block;" id="rdvVisualPreviewTitle">Aperçu : Salle Polyvalente « Menkii Essomba Anton » &amp; Esplanade Gala</strong>
          <span style="color:var(--color-text-muted);" id="rdvVisualPreviewDesc">Cadre prestigieux pour mariages, galas et réceptions avec service traiteur du Château des Saveurs.</span>
        </div>
      </div>"""
    if "rdvVisualPreviewBanner" not in html and rdv_modal_target in html:
        html = html.replace(rdv_modal_target, rdv_modal_replace, 1)

    evt_modal_target = """      <h3 style="margin-top:6px;" id="evtModalTitle">Grand Dimanche Royal : Buffet Camerounais &amp; Ambiance Acoustique Live</h3>"""
    evt_modal_replace = """      <div style="margin:10px 0;border-radius:14px;overflow:hidden;height:175px;position:relative;border:1px solid rgba(29,73,13,0.16);">
        <img id="evtModalHeroImg" src="audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg" alt="Aperçu événement de la semaine ECOPARK" style="width:100%;height:100%;object-fit:cover;cursor:zoom-in;" onclick="openEcoparkLightbox(5)" />
        <span class="agenda-card-zoom-tag">Cliquer pour agrandir en HD</span>
      </div>
""" + evt_modal_target
    if "evtModalHeroImg" not in html and evt_modal_target in html:
        html = html.replace(evt_modal_target, evt_modal_replace, 1)

    # 8. Inject JS_VISUAL_APPRECIATION before </script>
    if "function syncVisualAppreciationSimulator" not in html:
        html = html.replace("  </script>\n</body>", JS_VISUAL_APPRECIATION + "\n  </script>\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Injected Visual Appreciation Upgrade into {filepath} ({len(html)} bytes)")


if __name__ == "__main__":
    for p in FILES:
        if os.path.exists(p):
            inject_visual_appreciation(p)
