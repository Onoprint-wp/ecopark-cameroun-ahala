import os

FILES = [
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\etape0-site-live\index.html",
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

CSS_WEEKLY_AGENDA = """
    /* ==========================================================================
       MODULE AGENDA DE LA SEMAINE & PROGRAMMATION ÉVÉNEMENTIELLE (PUB-15 / PUB-16)
       ========================================================================== */
    .agenda-privatization-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      padding: 12px 16px;
      margin-bottom: 16px;
      border-radius: 16px;
      background: linear-gradient(90deg, #EDF4E7 0%, #FBF5EC 100%);
      border: 1px solid rgba(29, 73, 13, 0.16);
      font-size: 13.5px;
      color: var(--color-brand-deep);
    }
    .agenda-filter-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }
    .agenda-day-pill {
      padding: 8px 15px;
      border-radius: 980px;
      border: 1.5px solid rgba(29, 73, 13, 0.16);
      background: #FFFFFF;
      color: var(--color-text);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .agenda-day-pill:hover {
      border-color: #C47D2B;
      background: #FBF5EC;
    }
    .agenda-day-pill.active {
      background: var(--color-brand-deep);
      color: #FFFFFF;
      border-color: var(--color-brand-deep);
      box-shadow: 0 6px 18px rgba(29, 73, 13, 0.18);
    }
    .agenda-event-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(29, 73, 13, 0.12);
      border-radius: 22px;
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      box-shadow: 0 12px 30px rgba(20, 34, 17, 0.05);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .agenda-event-card:hover {
      transform: translate3d(0, -4px, 0);
      border-color: #C47D2B;
      box-shadow: 0 18px 40px rgba(196, 125, 43, 0.15);
    }
    .agenda-event-card-featured {
      border: 2px solid #C47D2B;
      background: linear-gradient(180deg, #FBF5EC 0%, #FFFFFF 52%);
    }
    .agenda-day-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 980px;
      background: var(--color-surface-soft);
      color: var(--color-brand-deep);
      font-size: 11.8px;
      font-weight: 700;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }
    .active-event-sim-banner {
      display: none;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      padding: 12px 14px;
      margin-bottom: 14px;
      border-radius: 12px;
      background: linear-gradient(90deg, #FBF5EC 0%, #EDF4E7 100%);
      border: 1.5px solid #C47D2B;
      font-size: 13.5px;
    }
    .active-event-sim-banner.open {
      display: flex;
    }
"""

HTML_WEEKLY_AGENDA_SECTION = """
        <!-- AGENDA DE LA SEMAINE & PROGRAMMATION ÉVÉNEMENTIELLE À AHALA (PUB-15 & PUB-16) -->
        <div class="section" id="sec-PUB-16" style="padding-top:20px;padding-bottom:16px;">
          <div class="container">
            <div class="section-header" style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;">
              <div>
                <span class="eyebrow eyebrow-hospitality"><span class="tech-code-tag">PUB-15 &amp; PUB-16 • </span>Agenda Hebdomadaire &amp; Événements à l'Affiche à Yaoundé-Ahala</span>
                <h2><span class="tonal-muted">Chaque semaine, un nouveau rendez-vous.</span> Programmation ECOPARK (Mardi – Dimanche).</h2>
              </div>
              <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openRdvModalSprint1('reperage_mariage')">
                Privatiser un espace pour mon événement →
              </button>
            </div>

            <!-- Bandeau de transparence sur l'ouverture des espaces vs privatisations -->
            <div class="agenda-privatization-banner" id="agendaSpaceStatusBanner">
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <span class="ahala-live-pulse-dot" aria-hidden="true"></span>
                <strong>Disponibilité des Espaces cette Semaine :</strong>
                <span>Jardin Zoologique (« ToTo »), Piscine Semi-Olympique, Lac &amp; Château des Saveurs <strong>100 % ouverts aux familles (09h00 – 18h00)</strong></span>
              </div>
              <span class="status-badge status-info">Salle « Menkii Essomba Anton » : Dispo Dimanche &amp; Semaine</span>
            </div>

            <!-- Filtres par jour de la semaine -->
            <div class="agenda-filter-bar" id="weeklyAgendaFilterBar" role="tablist" aria-label="Filtrer la programmation par jour">
              <button type="button" class="agenda-day-pill active" data-day-filter="ALL" onclick="filterWeeklyAgenda('ALL', this)">Toute la semaine (4 temps forts)</button>
              <button type="button" class="agenda-day-pill" data-day-filter="MER_JEU" onclick="filterWeeklyAgenda('MER_JEU', this)">Mercredi &amp; Jeudi • Pédagogie &amp; CFP</button>
              <button type="button" class="agenda-day-pill" data-day-filter="VENDREDI" onclick="filterWeeklyAgenda('VENDREDI', this)">Vendredi • Afterwork &amp; Saveurs</button>
              <button type="button" class="agenda-day-pill" data-day-filter="SAMEDI" onclick="filterWeeklyAgenda('SAMEDI', this)">Samedi • Famille, Zoo &amp; Pirogues</button>
              <button type="button" class="agenda-day-pill" data-day-filter="DIMANCHE" onclick="filterWeeklyAgenda('DIMANCHE', this)">Dimanche • Grand Buffet Royal &amp; Live</button>
            </div>

            <!-- Grille des 4 événements programmés cette semaine -->
            <div class="grid-12" id="weeklyAgendaGrid" style="gap:16px;">
              <!-- Événement 1 : Mercredi & Jeudi -->
              <div class="col-3 agenda-event-card" data-agenda-day="MER_JEU">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
                    <span class="agenda-day-badge">Mer. &amp; Jeu. • 10h00–16h00</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">500 / 1 000 FCFA</span>
                  </div>
                  <h3 style="font-size:1.15rem;margin-bottom:6px;">Journée Pédagogique Faune &amp; Portes Ouvertes CFP</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin-bottom:10px;">
                    Parcours commenté des bassins piscicoles et du parc animalier pour élèves/familles + orientation gratuite dans les 5 filières du CFP ECOPARK.
                  </p>
                  <div style="font-size:12.5px;color:var(--color-brand-deep);font-weight:600;">
                    • Tarif enfant garanti à 500 FCFA • Immersion campus MINEFOP
                  </div>
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px dashed var(--color-border);">
                  <button type="button" class="btn btn-secondary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="openWeeklyEventDetail('EVT_MERCREDI_CFP')">Programme</button>
                  <button type="button" class="btn btn-primary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="bookWeeklyEventInOneClick('EVT_MERCREDI_CFP')">Réserver QR</button>
                </div>
              </div>

              <!-- Événement 2 : Vendredi Afterwork -->
              <div class="col-3 agenda-event-card" data-agenda-day="VENDREDI">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
                    <span class="agenda-day-badge" style="background:#FBF5EC;color:#8E5617;">Vendredi • 15h30–20h30</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">Dès 3 500 FCFA</span>
                  </div>
                  <h3 style="font-size:1.15rem;margin-bottom:6px;">Afterwork « Brise du Lac &amp; Poisson Braisé d'Ahala »</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin-bottom:10px;">
                    Décompressez loin des embouteillages du vendredi : poisson d'eau douce pêché et braisé à la minute, pergolas au bord de l'eau et suites Cité Ewondo.
                  </p>
                  <div style="font-size:12.5px;color:#8E5617;font-weight:600;">
                    • 4 pergolas disponibles • Parking sécurisé 150 places
                  </div>
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px dashed var(--color-border);">
                  <button type="button" class="btn btn-secondary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="openWeeklyEventDetail('EVT_VENDREDI_AFTERWORK')">Programme</button>
                  <button type="button" class="btn btn-primary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="bookWeeklyEventInOneClick('EVT_VENDREDI_AFTERWORK')">Bloquer Table</button>
                </div>
              </div>

              <!-- Événement 3 : Samedi Famille -->
              <div class="col-3 agenda-event-card" data-agenda-day="SAMEDI">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
                    <span class="agenda-day-badge">Samedi • 10h30 &amp; 15h00</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">1 500 / 2 500 FCFA</span>
                  </div>
                  <h3 style="font-size:1.15rem;margin-bottom:6px;">Samedi Famille : Rencontre « Gorille ToTo » &amp; Pirogues</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin-bottom:10px;">
                    Nourrissage guidé des poissons et tortues géantes avec les soigneurs à 10h30, traversée en pirogue sur le lac d'Ahala, tour à cheval et piscine surveillée.
                  </p>
                  <div style="font-size:12.5px;color:var(--color-brand-deep);font-weight:600;">
                    • Pass Découverte tout-en-un • Sachet nutrition 500 FCFA
                  </div>
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px dashed var(--color-border);">
                  <button type="button" class="btn btn-secondary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="openWeeklyEventDetail('EVT_SAMEDI_FAMILLE')">Programme</button>
                  <button type="button" class="btn btn-primary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="bookWeeklyEventInOneClick('EVT_SAMEDI_FAMILLE')">Pass Samedi</button>
                </div>
              </div>

              <!-- Événement 4 : Dimanche Royal (Mis en avant) -->
              <div class="col-3 agenda-event-card agenda-event-card-featured" data-agenda-day="DIMANCHE">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
                    <span class="agenda-day-badge" style="background:#C47D2B;color:#FFFFFF;">Dimanche • 12h00–17h30</span>
                    <span class="price-pill" style="font-size:11.5px;padding:2px 8px;">4 500 / 8 500 FCFA</span>
                  </div>
                  <h3 style="font-size:1.15rem;margin-bottom:6px;">Grand Dimanche Royal : Buffet Camerounais &amp; Live</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin-bottom:10px;">
                    Le grand rendez-vous dominical de Yaoundé : Poulet DG, Ndolé Royal, Poisson Braisé d'Ahala au Château des Saveurs, musique acoustique et accès Piscine + Zoo.
                  </p>
                  <div style="font-size:12.5px;color:#8E5617;font-weight:700;">
                    • Le plus réservé • Service prioritaire 12h30 / 13h30 sur QR
                  </div>
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;padding-top:10px;border-top:1px dashed var(--color-border);">
                  <button type="button" class="btn btn-secondary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="openWeeklyEventDetail('EVT_DIMANCHE_ROYAL')">Programme</button>
                  <button type="button" class="btn btn-primary btn-sm" style="flex:1;padding:6px 10px;font-size:12.5px;" onclick="bookWeeklyEventInOneClick('EVT_DIMANCHE_ROYAL')">Pass Dimanche</button>
                </div>
              </div>
            </div>
          </div>
        </div>
"""

HTML_EVENT_BANNER_SIMULATOR = """
                <!-- BANNIÈRE ÉVÉNEMENT DE LA SEMAINE SÉLECTIONNÉ (PUB-16 -> RES-03) -->
                <div class="active-event-sim-banner" id="activeEventBannerSimulator">
                  <div>
                    <span style="font-size:11.5px;text-transform:uppercase;letter-spacing:0.04em;color:#8E5617;font-weight:700;display:block;">Programmation Hebdomadaire Sélectionnée (Inscrite sur votre Pass QR)</span>
                    <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);" id="activeEventSimTitle">Grand Dimanche Royal : Buffet Camerounais &amp; Live</strong>
                  </div>
                  <button type="button" class="btn btn-secondary btn-sm" onclick="clearWeeklyEventSelection()">Retirer l'événement</button>
                </div>
"""

HTML_MODAL_EVENT_DETAIL = """
    <!-- FICHE DÉTAIL D'UN ÉVÉNEMENT DE LA SEMAINE (PUB-16) -->
    <div id="modalEventDetailBox" class="card" style="display:none;max-width:600px;width:100%;background:#FFFFFF;padding:28px;max-height:92vh;overflow-y:auto;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow eyebrow-hospitality" id="evtModalDayBadge" style="margin:0;">Dimanche • 12h00 – 17h30</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()">Fermer</button>
      </div>
      <h3 style="margin-top:6px;" id="evtModalTitle">Grand Dimanche Royal : Buffet Camerounais &amp; Ambiance Acoustique Live</h3>
      <p style="font-size:14.5px;color:var(--color-text-muted);margin-bottom:10px;" id="evtModalDesc">
        Profitez d'une journée complète en famille ou entre amis au bord du lac d'Ahala avec accès coupe-file aux activités et table garantie au Château des Saveurs.
      </p>
      <div style="padding:12px 14px;background:var(--color-surface-soft);border-radius:12px;font-size:13.8px;display:grid;gap:6px;" id="evtModalScheduleBox">
      </div>
      <div style="margin-top:10px;padding:10px 12px;background:#FBF5EC;border:1px solid rgba(196,125,43,0.4);border-radius:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <span style="font-size:13px;font-weight:700;color:var(--color-brand-deep);" id="evtModalPriceInfo">Tarif : 4 500 FCFA (Enfant) • 8 500 FCFA (Adulte)</span>
        <span class="status-badge status-success" id="evtModalSpotsBadge">Places garanties sur Pass QR</span>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="bookWeeklyEventInOneClick(window._currentAgendaEventCode)">
          Réserver mon Billet QR pour cet événement
        </button>
        <button type="button" class="btn btn-secondary btn-ochre-outline" onclick="sendWhatsAppWeeklyEvent(window._currentAgendaEventCode)">
          Réserver sur WhatsApp
        </button>
      </div>
    </div>
"""

JS_WEEKLY_AGENDA = """
    // ========================================================================
    // MOTEUR DE L'AGENDA DE LA SEMAINE & RÉSERVATION D'ÉVÉNEMENT EN 1 CLIC (PUB-15 / PUB-16)
    // ========================================================================
    window._currentAgendaEventCode = 'EVT_DIMANCHE_ROYAL';
    window._selectedWeeklyEventTitle = '';

    const WEEKLY_AGENDA_CATALOG = {
      EVT_MERCREDI_CFP: {
        code: 'EVT_MERCREDI_CFP',
        dayFilter: 'MER_JEU',
        targetWeekday: 3, // Mercredi
        badge: 'Mercredi & Jeudi • 10h00 – 16h00',
        title: 'Journée Pédagogique Faune & Portes Ouvertes Campus CFP',
        shortLabel: 'Mercredi Pédagogique & Portes Ouvertes CFP',
        priceText: 'Entrée : 500 FCFA (Enfant) / 1 000 FCFA (Adulte) • Orientation CFP Gratuite',
        spotsText: 'Accès libre & Groupes scolaires sur réservation',
        desc: 'Idéal pour les familles en semaine, les écoles maternelles/primaires et les futurs apprenants souhaitant visiter les ateliers pratiques du CFP ECOPARK agréé MINEFOP.',
        schedule: [
          "10h00 – 11h30 : Visite guidée du Jardin Zoologique (gorille « ToTo », tortues géantes, paons) et des allées botaniques.",
          "11h30 – 13h00 : Démonstration d'aquaculture sur les étangs d'Ahala & séance d'orientation CFP (5 filières, inscription 50 000 FCFA).",
          "13h00 – 16h00 : Déjeuner au Château des Saveurs, balade en pirogue et baignade surveillée."
        ],
        bundle: 'PASS_DECOUVERTE',
        dish: "Poisson Braisé d'Ahala (Étang frais)",
        mealSlot: 'Service 12h30',
        pergola: false,
        nutrition: true
      },
      EVT_VENDREDI_AFTERWORK: {
        code: 'EVT_VENDREDI_AFTERWORK',
        dayFilter: 'VENDREDI',
        targetWeekday: 5, // Vendredi
        badge: 'Vendredi • 15h30 – 20h30',
        title: "Afterwork « Brise du Lac & Poisson Braisé d'Ahala »",
        shortLabel: 'Vendredi Afterwork Brise du Lac & Grillades',
        priceText: 'Plats dès 3 500 FCFA • Pergola Privée Bord du Lac : +5 000 FCFA',
        spotsText: 'Plus que 4 pergolas disponibles ce vendredi',
        desc: 'Évitez les embouteillages du vendredi soir à Yaoundé : rejoignez Ahala Barrière (face station Tradex) pour savourer le poisson frais des étangs braisé à la minute sous une pergola privée.',
        schedule: [
          "15h30 – 17h30 : Accueil coupe-file, promenade au bord du lac d'Ahala et installation sous pergola privée.",
          "17h30 – 20h30 : Service grillades & Poisson Braisé d'Ahala au Château des Saveurs, ambiance musicale douce.",
          "Option Séjour : Possibilité de prolonger en nuitée dans les Cités Bene (10k), Chanthel (15k) ou Ewondo VIP (25k FCFA)."
        ],
        bundle: 'CUSTOM',
        dish: "Poisson Braisé d'Ahala (Étang frais)",
        mealSlot: 'Service 15h00',
        pergola: true,
        nutrition: false
      },
      EVT_SAMEDI_FAMILLE: {
        code: 'EVT_SAMEDI_FAMILLE',
        dayFilter: 'SAMEDI',
        targetWeekday: 6, // Samedi
        badge: 'Samedi • 10h30 & 15h00',
        title: 'Samedi Famille : Rencontre Soigneurs « Gorille ToTo » & Régate Pirogues',
        shortLabel: 'Samedi Famille • Gorille ToTo & Pirogues',
        priceText: 'Pass Découverte : 1 500 FCFA (Enfant) • 2 500 FCFA (Adulte)',
        spotsText: 'Tarif enfant strictement garanti à 500 FCFA (entrée)',
        desc: 'La sortie préférée des enfants à Yaoundé : nourrissage commenté aux étangs, rencontre avec le gorille « ToTo », balade sécurisée en pirogue avec gilet et piscine semi-olympique.',
        schedule: [
          '10h30 – 12h00 : Rencontre avec les soigneurs du Zoo (« ToTo ») & nourrissage des poissons et tortues aux étangs.',
          '12h30 – 14h30 : Déjeuner familial au Château des Saveurs (Menu Enfant 2 500 FCFA & spécialités camerounaises).',
          '14h30 – 17h30 : Traversée en pirogue sur le lac, initiation équestre encadrée et piscine surveillée par maître-nageur.'
        ],
        bundle: 'PASS_DECOUVERTE',
        dish: 'Menu Enfant & Grillades Douces',
        mealSlot: 'Service 12h30',
        pergola: false,
        nutrition: true
      },
      EVT_DIMANCHE_ROYAL: {
        code: 'EVT_DIMANCHE_ROYAL',
        dayFilter: 'DIMANCHE',
        targetWeekday: 0, // Dimanche
        badge: 'Dimanche • 12h00 – 17h30',
        title: 'Grand Dimanche Royal : Buffet Camerounais & Ambiance Acoustique Live',
        shortLabel: 'Grand Dimanche Royal • Buffet & Live',
        priceText: 'Pass Journée Royale Tout-Inclus : 4 500 FCFA (Enfant) • 8 500 FCFA (Adulte)',
        spotsText: 'Réservation QR fortement conseillée (Service 12h30 / 13h30 garanti)',
        desc: "Le grand rendez-vous dominical d'ECOPARK Ahala : grands classiques du Château des Saveurs (Poulet DG Royal, Ndolé Crevettes, Poisson Braisé), ambiance acoustique au bord du lac et accès illimité Parc + Piscine + Pirogue.",
        schedule: [
          "09h30 – 12h00 : Accès coupe-file au Portail d'Ahala (QR Code), visite du Zoo et balade matinale en pirogue.",
          "12h30 – 15h00 : Grand Service Dominical au Château des Saveurs (zéro attente pour les détenteurs du Pass QR) & animation acoustique.",
          "15h00 – 18h00 : Détente à la Piscine Semi-Olympique et sous les pergolas ombragées."
        ],
        bundle: 'PASS_ROYALE',
        dish: 'Poulet DG Royal Plantain Mûr',
        mealSlot: 'Service 13h30',
        pergola: true,
        nutrition: true
      }
    };

    function getNextDateForWeekday(targetDay) {
      const d = new Date();
      const current = d.getDay();
      let diff = (targetDay - current + 7) % 7;
      if (diff === 0) diff = 7;
      d.setDate(d.getDate() + diff);
      const pad = n => String(n).padStart(2, '0');
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    }

    function filterWeeklyAgenda(dayCode, btnEl) {
      document.querySelectorAll('#weeklyAgendaFilterBar .agenda-day-pill').forEach(b => {
        b.classList.toggle('active', b === btnEl || b.getAttribute('data-day-filter') === dayCode);
      });
      document.querySelectorAll('#weeklyAgendaGrid .agenda-event-card').forEach(card => {
        const cardDay = card.getAttribute('data-agenda-day');
        if (!dayCode || dayCode === 'ALL' || cardDay === dayCode) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function openWeeklyEventDetail(eventCode) {
      const ev = WEEKLY_AGENDA_CATALOG[eventCode] || WEEKLY_AGENDA_CATALOG.EVT_DIMANCHE_ROYAL;
      window._currentAgendaEventCode = ev.code;
      if (typeof hideExtraOmissionModals === 'function') hideExtraOmissionModals();
      ['modalQuoteBox', 'modalCfpBox', 'modalRdvBox', 'modalRescheduleBox', 'modalOfficialPrintBox'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });
      const overlay = document.getElementById('modalOverlaySprint1');
      const box = document.getElementById('modalEventDetailBox');
      if (!overlay || !box) return;

      document.getElementById('evtModalDayBadge').textContent = ev.badge;
      document.getElementById('evtModalTitle').textContent = ev.title;
      document.getElementById('evtModalDesc').textContent = ev.desc;
      document.getElementById('evtModalPriceInfo').textContent = ev.priceText;
      document.getElementById('evtModalSpotsBadge').textContent = ev.spotsText;
      document.getElementById('evtModalScheduleBox').innerHTML = ev.schedule.map(s => `<div>• ${s}</div>`).join('');

      overlay.style.display = 'flex';
      box.style.display = 'block';
    }

    function clearWeeklyEventSelection() {
      window._selectedWeeklyEventTitle = '';
      const banner = document.getElementById('activeEventBannerSimulator');
      if (banner) banner.classList.remove('open');
      recalcSimulator();
      showToastSprint1("• Sélection d'événement retirée. Vous êtes en mode réservation libre.");
    }

    function bookWeeklyEventInOneClick(eventCode) {
      const ev = WEEKLY_AGENDA_CATALOG[eventCode] || WEEKLY_AGENDA_CATALOG.EVT_DIMANCHE_ROYAL;
      window._currentAgendaEventCode = ev.code;
      window._selectedWeeklyEventTitle = ev.shortLabel;
      closeSprint1Modals();

      const nextDateIso = getNextDateForWeekday(ev.targetWeekday);
      const vDate = document.getElementById('visitDate');
      if (vDate) vDate.value = nextDateIso;

      if (ev.bundle && ev.bundle !== 'CUSTOM') {
        applySalesBundle(ev.bundle, false);
      } else {
        applySalesBundle('CUSTOM', false);
        if (document.getElementById('chkZoo')) document.getElementById('chkZoo').checked = true;
        if (document.getElementById('chkRepas')) document.getElementById('chkRepas').checked = true;
      }

      if (document.getElementById('chkBumpPergola')) document.getElementById('chkBumpPergola').checked = !!ev.pergola;
      if (document.getElementById('chkBumpNutrition')) document.getElementById('chkBumpNutrition').checked = !!ev.nutrition;
      if (document.getElementById('simDishSelect') && ev.dish) document.getElementById('simDishSelect').value = ev.dish;
      if (document.getElementById('simMealSlotSelect') && ev.mealSlot) document.getElementById('simMealSlotSelect').value = ev.mealSlot;

      const banner = document.getElementById('activeEventBannerSimulator');
      const bannerTitle = document.getElementById('activeEventSimTitle');
      if (banner) banner.classList.add('open');
      if (bannerTitle) bannerTitle.textContent = `${ev.title} (Date pré-remplie : ${nextDateIso})`;

      recalcSimulator();
      navigateFamily('RES', 'RES-03');
      showToastSprint1(`• Événement « ${ev.shortLabel} » (${nextDateIso}) pré-configuré sur votre Billet QR !`);
      return nextDateIso;
    }

    function sendWhatsAppWeeklyEvent(eventCode) {
      const ev = WEEKLY_AGENDA_CATALOG[eventCode] || WEEKLY_AGENDA_CATALOG.EVT_DIMANCHE_ROYAL;
      const nextDateIso = bookWeeklyEventInOneClick(ev.code);
      const total = (document.getElementById('grandTotalFCFA') || {}).textContent || '14 000 FCFA';
      const msg = [
        `Bonjour ECOPARK CAMEROUN (Yaoundé-Ahala),`,
        `Je souhaite réserver pour l'événement programmé à l'Agenda de la Semaine :`,
        `- Événement : ${ev.title}`,
        `- Créneau & Date : ${ev.badge} (${nextDateIso})`,
        `- Formule & Budget estimé : ${total} (${ev.priceText})`,
        `Merci de me confirmer mon E-Billet QR Coupe-File.`
      ].join('\\n');
      window.open('https://wa.me/237697136203?text=' + encodeURIComponent(msg), '_blank', 'noopener,noreferrer');
    }

    // S'assurer que hideExtraOmissionModals masque aussi modalEventDetailBox
    if (typeof hideExtraOmissionModals === 'function') {
      const _prevHideExtra = hideExtraOmissionModals;
      hideExtraOmissionModals = function() {
        _prevHideExtra();
        const el = document.getElementById('modalEventDetailBox');
        if (el) el.style.display = 'none';
      };
    }

    // Inclure l'événement sélectionné dans le récapitulatif des prestations du Billet QR & de WhatsApp
    if (typeof getActiveSimulatorItemsSummary === 'function') {
      const _prevGetItemsForAgenda = getActiveSimulatorItemsSummary;
      getActiveSimulatorItemsSummary = function() {
        let s = _prevGetItemsForAgenda();
        if (window._selectedWeeklyEventTitle) {
          s = `[Événement : ${window._selectedWeeklyEventTitle}] ` + s;
        }
        return s;
      };
    }

    (function checkAgendaRoute() {
      const path = (window.location.pathname || '/').replace(/\\/+$/, '').toLowerCase();
      if (path === '/agenda' || path === '/evenements') {
        setTimeout(() => {
          navigateFamily('PUB', 'PUB-16');
        }, 90);
      }
    })();
"""


def inject_weekly_agenda(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. CSS
    if ".agenda-event-card" not in html:
        html = html.replace("  </style>", CSS_WEEKLY_AGENDA + "\n  </style>", 1)

    # 2. Add "Agenda de la Semaine" button inside #ahalaLiveWeatherBar
    target_weather_btn = '<span class="price-pill" style="font-size:11.5px;padding:2px 9px;">Garantie Pluie : Report Gratuit 1 Clic</span>'
    if "navigateFamily('PUB', 'PUB-16')" not in html and target_weather_btn in html:
        replacement_weather = (
            '<button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="padding:3px 10px;font-size:11.8px;min-height:26px;" onclick="navigateFamily(\'PUB\', \'PUB-16\')">Agenda de la Semaine (4 événements)</button>\n                '
            + target_weather_btn
        )
        html = html.replace(target_weather_btn, replacement_weather, 1)

    # 3. Inject #sec-PUB-16 right before #sec-PUB-15
    target_pub_15 = '        <!-- OMISSION #6B : PREUVE SOCIALE & AVIS VÉRIFIÉS DE NOS VISITEURS, ÉCOLES & ENTREPRISES (PUB-15) -->'
    if 'id="sec-PUB-16"' not in html and target_pub_15 in html:
        html = html.replace(target_pub_15, HTML_WEEKLY_AGENDA_SECTION + "\n" + target_pub_15, 1)

    # 4. Inject #activeEventBannerSimulator at top of #resMainGrid left card
    target_res_h3 = '<h3>1. Composition du groupe & Date de visite<span class="tech-code-tag"> (`RES-01` / `RES-02`)</span></h3>'
    if "activeEventBannerSimulator" not in html and target_res_h3 in html:
        html = html.replace(target_res_h3, HTML_EVENT_BANNER_SIMULATOR + "\n                " + target_res_h3, 1)

    # 5. Add "Agenda" pill in #mobileQuickNavPills
    target_mob_pill = '<button type="button" class="mobile-quick-pill" onclick="navigateFamily(\'PUB\', \'PUB-10\')">Tarifs FCFA</button>'
    if "Agenda Semaine" not in html and target_mob_pill in html:
        html = html.replace(
            target_mob_pill,
            '<button type="button" class="mobile-quick-pill" onclick="navigateFamily(\'PUB\', \'PUB-16\')">Agenda Semaine</button>\n      ' + target_mob_pill,
            1,
        )

    # 6. Inject #modalEventDetailBox inside #modalOverlaySprint1
    target_print_box_end = """      <div style="display:flex;gap:10px;justify-content:flex-end;border-top:1px solid var(--color-border);padding-top:12px;">
        <button type="button" class="btn btn-secondary btn-sm" onclick="downloadOfflineQrTicketPng()">Télécharger Image PNG</button>
        <button type="button" class="btn btn-primary btn-sm" onclick="window.print()">Lancer l'impression / Enregistrer en PDF</button>
      </div>
    </div>"""
    if "modalEventDetailBox" not in html and target_print_box_end in html:
        html = html.replace(target_print_box_end, target_print_box_end + "\n" + HTML_MODAL_EVENT_DETAIL, 1)

    # 7. Inject JS_WEEKLY_AGENDA before </script>
    if "function bookWeeklyEventInOneClick" not in html:
        html = html.replace("  </script>\n</body>", JS_WEEKLY_AGENDA + "\n  </script>\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Injected Weekly Agenda into {filepath} ({len(html)} bytes)")


if __name__ == "__main__":
    for p in FILES:
        if os.path.exists(p):
            inject_weekly_agenda(p)
