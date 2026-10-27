import os

FILES = [
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\etape0-site-live\index.html",
    r"c:\Users\PcGamerCm\Downloads\ECO-PARK\Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

CSS_OMISSIONS_UPGRADE = """
    /* ==========================================================================
       PACK 7 COMPLÉMENTS UX, MÉTIER & EXPLOITATION (ECOPARK YAOUNDÉ-AHALA)
       ========================================================================== */
    .ahala-live-weather-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      padding: 10px 16px;
      margin-bottom: 18px;
      border-radius: 980px;
      background: linear-gradient(90deg, #EDF4E7 0%, #FBF5EC 100%);
      border: 1px solid rgba(29, 73, 13, 0.16);
      font-size: 13.2px;
      color: var(--color-brand-deep);
    }
    .ahala-live-pulse-dot {
      display: inline-block;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #1F880B;
      box-shadow: 0 0 0 3px rgba(31, 136, 11, 0.22);
      margin-right: 6px;
    }
    .testimonial-card {
      background: #FFFFFF;
      border: 1px solid rgba(29, 73, 13, 0.12);
      border-radius: 22px;
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      box-shadow: 0 10px 28px rgba(20, 34, 17, 0.05);
    }
    .testimonial-quote {
      font-size: 14.5px;
      line-height: 1.55;
      color: var(--color-text);
      font-style: italic;
    }
    .testimonial-author {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      border-top: 1px dashed var(--color-border);
      padding-top: 10px;
      font-size: 13px;
    }
    .contextual-subpanel {
      margin-top: 6px;
      padding: 10px 12px;
      background: #FFFFFF;
      border: 1px dashed rgba(196, 125, 43, 0.55);
      border-radius: 10px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      font-size: 13px;
    }
    @media (max-width: 640px) {
      .contextual-subpanel {
        grid-template-columns: 1fr;
      }
      .ahala-live-weather-bar {
        border-radius: 16px;
      }
    }
    .mobile-quick-nav-strip {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      width: 100%;
      padding-bottom: 6px;
      margin-bottom: 6px;
      border-bottom: 1px solid rgba(29, 73, 13, 0.1);
      scrollbar-width: none;
    }
    .mobile-quick-nav-strip::-webkit-scrollbar {
      display: none;
    }
    .mobile-quick-pill {
      flex-shrink: 0;
      padding: 4px 10px;
      border-radius: 980px;
      border: 1px solid rgba(29, 73, 13, 0.18);
      background: var(--color-surface-soft);
      color: var(--color-brand-deep);
      font-size: 11.8px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
    }
    .acc-filter-pill {
      padding: 4px 10px;
      border-radius: 980px;
      border: 1px solid var(--color-border);
      background: #FFFFFF;
      color: var(--color-text);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
    }
    .acc-filter-pill.active {
      background: var(--color-brand-deep);
      color: #FFFFFF;
      border-color: var(--color-brand-deep);
    }
"""

HTML_LIVE_WEATHER_BAR = """
            <!-- OMISSION #6A : BANDEAU MÉTÉO, TRAFIC RN3 & AFFLUENCE EN DIRECT D'AHALA BARRIÈRE (PUB-13) -->
            <div class="ahala-live-weather-bar" id="ahalaLiveWeatherBar" role="status" aria-label="Météo et affluence en direct d'Ahala Barrière">
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
                <span class="price-pill" style="font-size:11.5px;padding:2px 9px;">Garantie Pluie : Report Gratuit 1 Clic</span>
              </div>
            </div>
"""

HTML_TESTIMONIALS_SECTION = """
        <!-- OMISSION #6B : PREUVE SOCIALE & AVIS VÉRIFIÉS DE NOS VISITEURS, ÉCOLES & ENTREPRISES (PUB-15) -->
        <div class="section" id="sec-PUB-15" style="padding-top:16px;">
          <div class="container">
            <div class="section-header">
              <span class="eyebrow"><span class="tech-code-tag">PUB-15 • </span>Preuve Sociale &amp; Retours d'Expérience Vérifiés à Yaoundé-Ahala</span>
              <h2><span class="tonal-muted">Ils ont vécu l'expérience ECOPARK.</span> Familles, écoles, ministères &amp; diplômés CFP.</h2>
            </div>
            <div class="grid-12" style="gap:16px;">
              <div class="col-3 testimonial-card">
                <div class="testimonial-quote">
                  « Enfin un espace calme et propre à 15 minutes du centre-ville ! Le tarif enfant à 500 FCFA a été scrupuleusement respecté, la piscine est bien surveillée par les maîtres-nageurs et notre poisson braisé commandé pour 13h00 était servi chaud sous la pergola au bord du lac. »
                </div>
                <div class="testimonial-author">
                  <div>
                    <strong style="color:var(--color-brand-deep);display:block;">Famille NKOA (Bastos)</strong>
                    <span style="color:var(--color-text-muted);">Pass Journée Royale • 2 Adultes, 3 Enfants</span>
                  </div>
                  <span class="status-badge status-success">Billet QR Vérifié</span>
                </div>
              </div>

              <div class="col-3 testimonial-card">
                <div class="testimonial-quote">
                  « Nous avons organisé notre excursion de 60 élèves avec la Facture Proforma générée en 2 minutes sur le site. La navette 32 places nous a récupérés à Mvan, et le parcours pédagogique autour du gorille "ToTo" et des bassins piscicoles a émerveillé les enfants. »
                </div>
                <div class="testimonial-author">
                  <div>
                    <strong style="color:var(--color-brand-deep);display:block;">École Bilingue Les Palmiers</strong>
                    <span style="color:var(--color-text-muted);">Direction Pédagogique • Excursion 60 élèves</span>
                  </div>
                  <span class="status-badge status-info">Devis École Validé</span>
                </div>
              </div>

              <div class="col-3 testimonial-card">
                <div class="testimonial-quote">
                  « Pour notre retraite stratégique de 45 cadres, la Salle Polyvalente "Menkii Essomba Anton" climatisée et le buffet du Château des Saveurs ont offert un cadre digne d'un resort. Nos intervenants logés à la Cité Ewondo VIP ont adoré le calme absolu. »
                </div>
                <div class="testimonial-author">
                  <div>
                    <strong style="color:var(--color-brand-deep);display:block;">DRH — ONG &amp; Partenaires</strong>
                    <span style="color:var(--color-text-muted);">Séminaire B2B &amp; Suites Cité Ewondo VIP</span>
                  </div>
                  <span class="status-badge badge-qr-prestige">Client Corporate</span>
                </div>
              </div>

              <div class="col-3 testimonial-card">
                <div class="testimonial-quote">
                  « Avec 50 000 FCFA d'inscription et ma scolarité réglée en 4 tranches, j'ai pu me former en Pisciculture et Hôtellerie directement sur les étangs et les loges d'ECOPARK Ahala avant d'obtenir mon diplôme reconnu par le MINEFOP. »
                </div>
                <div class="testimonial-author">
                  <div>
                    <strong style="color:var(--color-brand-deep);display:block;">Paulin NGAOUNDÉRÉ</strong>
                    <span style="color:var(--color-text-muted);">Lauréat CFP ECOPARK • Filière Aquaculture</span>
                  </div>
                  <span class="status-badge status-success">Diplômé MINEFOP</span>
                </div>
              </div>
            </div>
          </div>
        </div>
"""

HTML_KITCHEN_AND_SHUTTLE_SUBPANELS = """
                    <!-- OMISSION #4A : SÉLECTEUR CONTEXTUEL PRÉCOMMANDE CUISINE « ZÉRO ATTENTE 13H » (PUB-07 / EXP-05) -->
                    <div class="contextual-subpanel" id="kitchenPreorderSubpanel">
                      <div>
                        <label class="form-label" for="simDishSelect" style="font-size:12px;margin-bottom:2px;">Spécialité Château des Saveurs (Précommande)</label>
                        <select id="simDishSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Poisson Braisé d'Ahala (Étang frais)" selected>Poisson Braisé d'Ahala (Étang frais)</option>
                          <option value="Poulet DG Royal Plantain Mûr">Poulet DG Royal &amp; Plantain Mûr</option>
                          <option value="Ndolé Royal Crevettes & Miondo">Ndolé Royal Crevettes &amp; Miondo</option>
                          <option value="Menu Enfant & Grillades Douces">Menu Enfant &amp; Grillades Douces</option>
                        </select>
                      </div>
                      <div>
                        <label class="form-label" for="simMealSlotSelect" style="font-size:12px;margin-bottom:2px;">Heure de service à table garantie</label>
                        <select id="simMealSlotSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Service 12h30" selected>12h30 — Zéro attente (Prioritaire)</option>
                          <option value="Service 13h30">13h30 — Cœur de journée</option>
                          <option value="Service 15h00">15h00 — Après-midi au bord du lac</option>
                        </select>
                      </div>
                    </div>
"""

HTML_SHUTTLE_SUBPANEL = """
                    <!-- OMISSION #4B : SÉLECTEUR POINT DE RAMASSAGE NAVETTE CLIMATISÉE YAOUNDÉ (5 / 18 / 32 PLACES) -->
                    <div class="contextual-subpanel" id="shuttlePickupSubpanel">
                      <div>
                        <label class="form-label" for="simShuttlePickupSelect" style="font-size:12px;margin-bottom:2px;">Point d'embarquement Navette à Yaoundé</label>
                        <select id="simShuttlePickupSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Départ Poste Centrale (09h30)" selected>Poste Centrale (Départ 09h30 / Retour 17h30)</option>
                          <option value="Départ Carrefour Bastos (09h15)">Carrefour Bastos (Départ 09h15 / Retour 17h30)</option>
                          <option value="Départ Carrefour Mvan (09h45)">Carrefour Mvan / Tropicana (Départ 09h45)</option>
                          <option value="Départ Nsimeyong / Mendong (09h40)">Nsimeyong / Mendong (Départ 09h40)</option>
                        </select>
                      </div>
                      <div>
                        <label class="form-label" for="simShuttleFleetSelect" style="font-size:12px;margin-bottom:2px;">Format de véhicule souhaité</label>
                        <select id="simShuttleFleetSelect" class="form-control" style="min-height:32px;padding:3px 8px;font-size:12.5px;" onchange="recalcSimulator()">
                          <option value="Navette Standard Climatisée" selected>Places en Navette Climatisée (18 / 32 pl.)</option>
                          <option value="Véhicule VIP 5 places">Navette Privée VIP (5 places)</option>
                        </select>
                      </div>
                    </div>
"""

HTML_OFFLINE_TICKET_ACTIONS = """
                  <!-- OMISSION #2 : TÉLÉCHARGEMENT HORS-LIGNE (PNG) & IMPRESSION PDF DU BILLET QR (VISITEUR) -->
                  <div style="display:flex;gap:8px;flex-wrap:wrap;padding-top:8px;border-top:1px dashed var(--color-border);">
                    <button type="button" class="btn btn-primary btn-sm" id="btnDownloadQrPassOffline" style="flex:1;" onclick="downloadOfflineQrTicketPng()">
                      <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg> Télécharger Pass QR Hors-Ligne (Image PNG)
                    </button>
                    <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" id="btnPrintQrPassPdf" onclick="printOfficialDocument('TICKET')">
                      <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg> Imprimer / PDF
                    </button>
                  </div>
"""

HTML_ACC_SEARCH_BOX = """
                <!-- OMISSION #1 : RECHERCHE DE DOSSIER PAR RÉFÉRENCE OU TÉLÉPHONE +237 (RES-12 / ACC-01) -->
                <div style="margin-top:8px;padding:12px;background:#FBF5EC;border:1px solid rgba(196,125,43,0.38);border-radius:10px;">
                  <label class="form-label" for="accSearchInput" style="font-size:13px;color:var(--color-brand-deep);margin-bottom:4px;">Retrouver un Billet QR, Devis, RDV ou Dossier CFP (`RES-12`) :</label>
                  <div style="display:flex;gap:6px;">
                    <input type="text" id="accSearchInput" class="form-control" style="min-height:36px;padding:6px 10px;font-size:13.5px;" placeholder="Réf. (ECP-..., DEV-..., RDV-..., CFP-) ou Tél +237" oninput="filterAccDossiers()" />
                    <button type="button" class="btn btn-primary btn-sm" onclick="filterAccDossiers()">Chercher</button>
                  </div>
                  <div style="display:flex;gap:5px;flex-wrap:wrap;margin-top:8px;" id="accCategoryFilterBar">
                    <button type="button" class="acc-filter-pill active" onclick="setAccCategoryFilter('ALL', this)">Tous</button>
                    <button type="button" class="acc-filter-pill" onclick="setAccCategoryFilter('BOOKING', this)">Billets QR</button>
                    <button type="button" class="acc-filter-pill" onclick="setAccCategoryFilter('QUOTE', this)">Devis</button>
                    <button type="button" class="acc-filter-pill" onclick="setAccCategoryFilter('RDV', this)">RDV</button>
                    <button type="button" class="acc-filter-pill" onclick="setAccCategoryFilter('CFP', this)">Dossiers CFP</button>
                  </div>
                </div>
"""

HTML_RESCHEDULE_AND_PRINT_MODALS = """
    <!-- OMISSION #3 : MODALE DE REPORT DE DATE SANS FRAIS — GARANTIE MÉTÉO YAOUNDÉ (ACC-05) -->
    <div id="modalRescheduleBox" class="card" style="display:none;max-width:520px;width:100%;background:#FFFFFF;padding:28px;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow eyebrow-hospitality" style="margin:0;">Garantie Météo &amp; Flexibilité Ahala (ACC-05)</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()">Fermer</button>
      </div>
      <h3 style="margin-top:6px;">Reporter la date de mon dossier sans frais</h3>
      <p style="font-size:14px;color:var(--color-text-muted);">
        En cas d'averse tropicale à Yaoundé ou d'imprévu, votre billet QR ou votre rendez-vous ECOPARK est reportable gratuitement sur simple sélection d'une nouvelle date.
      </p>
      <input type="hidden" id="rescheduleTargetRef" value="ECP-2026-84920" />
      <input type="hidden" id="rescheduleTargetKind" value="BOOKING" />
      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-12" style="padding:10px 12px;background:var(--color-surface-soft);border-radius:8px;font-size:13.5px;">
          <strong>Dossier sélectionné :</strong> <span id="rescheduleRefLabel" style="color:var(--color-brand-deep);font-weight:700;">ECP-2026-84920</span>
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="rescheduleNewDate">Nouvelle date souhaitée <span style="color:#B42318;">*</span></label>
          <input type="date" id="rescheduleNewDate" class="form-control" value="2026-11-22" required />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="rescheduleReason">Motif du report</label>
          <select id="rescheduleReason" class="form-control">
            <option value="Garantie Pluie / Météo Yaoundé (Sans frais)" selected>Pluie / Météo Yaoundé (Garantie Gratuite)</option>
            <option value="Imprévu familial ou professionnel">Imprévu familial ou professionnel</option>
            <option value="Ajustement calendrier École / Entreprise">Ajustement calendrier École / Entreprise</option>
          </select>
        </div>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="confirmRescheduleSprint1()">Valider ma nouvelle date sans frais</button>
      </div>
    </div>

    <!-- OMISSION #2B & #7B : APERÇU IMPRIMABLE OFFICIEL (BILLET QR, FACTURE PROFORMA & PV CLÔTURE CAISSE) -->
    <div id="modalOfficialPrintBox" class="card" style="display:none;max-width:680px;width:100%;background:#FFFFFF;padding:28px;max-height:92vh;overflow-y:auto;">
      <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid var(--color-brand-deep);padding-bottom:12px;">
        <div>
          <strong style="font-family:var(--font-heading);font-size:1.35rem;color:var(--color-brand-deep);display:block;" id="officialPrintTitle">DOCUMENT OFFICIEL — ECOPARK CAMEROUN (YAOUNDÉ-AHALA)</strong>
          <span style="font-size:12.5px;color:var(--color-text-muted);">Route Nationale N°3, Ahala Barrière (Face Station Tradex Ahala) • Tél / WhatsApp : +237 697 13 62 03</span>
        </div>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()">Fermer</button>
      </div>
      <div id="officialPrintBody" style="padding:16px 0;font-size:14px;line-height:1.55;display:grid;gap:10px;"></div>
      <div style="display:flex;gap:10px;justify-content:flex-end;border-top:1px solid var(--color-border);padding-top:12px;">
        <button type="button" class="btn btn-secondary btn-sm" onclick="downloadOfflineQrTicketPng()">Télécharger Image PNG</button>
        <button type="button" class="btn btn-primary btn-sm" onclick="window.print()">Lancer l'impression / Enregistrer en PDF</button>
      </div>
    </div>
"""

JS_OMISSIONS_UPGRADE = """
    // ========================================================================
    // PACK 7 COMPLÉMENTS : RECHERCHE ACC-01/RES-12, PNG HORS-LIGNE, REPORT ACC-05,
    // CUISINE 13H & NAVETTE YAOUNDÉ, PROFORMA PDF & EXPORT CSV COMPTABLE (DIR-05)
    // ========================================================================
    window._accCategoryFilter = 'ALL';

    function setAccCategoryFilter(cat, btnEl) {
      window._accCategoryFilter = cat || 'ALL';
      document.querySelectorAll('#accCategoryFilterBar .acc-filter-pill').forEach(b => {
        b.classList.toggle('active', b === btnEl);
      });
      filterAccDossiers();
    }

    function filterAccDossiers() {
      syncAllViewsFromDB();
    }

    function hideExtraOmissionModals() {
      ['modalRescheduleBox', 'modalOfficialPrintBox'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });
    }
    const _origOpenQuote7 = openQuoteModalSprint1;
    openQuoteModalSprint1 = function() {
      hideExtraOmissionModals();
      _origOpenQuote7();
    };
    const _origOpenCfp7 = openCfpModalSprint1;
    openCfpModalSprint1 = function() {
      hideExtraOmissionModals();
      _origOpenCfp7();
    };
    const _origOpenRdv7 = openRdvModalSprint1;
    openRdvModalSprint1 = function(p) {
      hideExtraOmissionModals();
      _origOpenRdv7(p);
    };

    function loadBookingIntoQrPass(ref) {
      const db = loadDB();
      const found = (db.bookings || []).find(b => b.reference === ref);
      if (found) {
        const codeEls = document.querySelectorAll('#demoTicketCard div[style*="font-size:1.3rem"]');
        if (codeEls.length > 0) codeEls[0].textContent = found.reference;
        const hEl = document.getElementById('ticketHolder');
        if (hEl) hEl.textContent = found.holder;
        const dEl = document.getElementById('ticketDate');
        if (dEl) dEl.textContent = `${found.date} (09h00 – 18h00)`;
        const pEl = document.getElementById('ticketPax');
        if (pEl) pEl.textContent = found.paxSummary;
        const iEl = document.getElementById('ticketItems');
        if (iEl) iEl.textContent = found.paxSummary;
        const scanInput = document.getElementById('qrScanInput');
        if (scanInput) scanInput.value = found.reference;
      }
      navigateFamily('RES', 'RES-09');
      if (typeof triggerQrPass3DReveal === 'function') {
        setTimeout(() => triggerQrPass3DReveal(), 120);
      }
      showToastSprint1(`• Billet QR ${ref} chargé dans votre portefeuille électronique et prêt à être présenté au portail d'Ahala.`);
    }

    function openRescheduleModal(ref, kind) {
      closeSprint1Modals();
      const overlay = document.getElementById('modalOverlaySprint1');
      const box = document.getElementById('modalRescheduleBox');
      if (!overlay || !box) return;
      ['modalQuoteBox', 'modalCfpBox', 'modalRdvBox', 'modalOfficialPrintBox'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });
      document.getElementById('rescheduleTargetRef').value = ref || 'ECP-2026-84920';
      document.getElementById('rescheduleTargetKind').value = kind || 'BOOKING';
      const lbl = document.getElementById('rescheduleRefLabel');
      if (lbl) lbl.textContent = `${ref} (${kind === 'RDV' ? 'Rendez-Vous Direction' : 'Billet QR Visite'})`;
      overlay.style.display = 'flex';
      box.style.display = 'flex';
    }

    function confirmRescheduleSprint1() {
      const ref = (document.getElementById('rescheduleTargetRef') || {}).value || 'ECP-2026-84920';
      const kind = (document.getElementById('rescheduleTargetKind') || {}).value || 'BOOKING';
      const newDate = (document.getElementById('rescheduleNewDate') || {}).value || '2026-11-22';
      const reason = (document.getElementById('rescheduleReason') || {}).value || 'Garantie Météo Yaoundé';
      const db = ensureAppointmentsArray(loadDB());

      if (kind === 'RDV') {
        const r = (db.appointments || []).find(x => x.reference === ref);
        if (r) {
          r.date = newDate;
          r.status = `Reporté au ${newDate}`;
        }
      } else {
        const b = (db.bookings || []).find(x => x.reference === ref);
        if (b) {
          b.date = newDate;
          b.status = 'REPORTED';
        }
        const tDate = document.getElementById('ticketDate');
        if (tDate) tDate.textContent = `${newDate} (09h00 – 18h00 • Reporté sans frais)`;
      }

      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `Espace Client (ACC-05)`,
        action: `Report de date sans frais du dossier ${ref} au ${newDate} (${reason}).`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`• Dossier ${ref} reporté avec succès au ${newDate} sans aucun frais (${reason}) !`);
    }

    // Téléchargement d'une carte PNG Hors-Ligne haute définition du Billet QR (Zéro forfait data à Ahala)
    function downloadOfflineQrTicketPng() {
      const ref = getActiveTicketRef();
      const holder = (document.getElementById('ticketHolder') || {}).textContent || 'Visiteur ECOPARK';
      const dateStr = (document.getElementById('ticketDate') || {}).textContent || 'Valable 09h00 – 18h00';
      const itemsStr = (document.getElementById('ticketItems') || {}).textContent || 'Entrée Parc & Zoo, Piscine, Pirogue';
      const totalStr = (document.getElementById('grandTotalFCFA') || {}).textContent || '14 000 FCFA';

      const canvas = document.createElement('canvas');
      canvas.width = 920;
      canvas.height = 460;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        // Fond parchemin / canopée
        ctx.fillStyle = '#FBF5EC';
        ctx.fillRect(0, 0, 920, 460);
        ctx.strokeStyle = '#1D490D';
        ctx.lineWidth = 6;
        ctx.strokeRect(12, 12, 896, 436);

        // Bandeau supérieur Vert Canopée
        ctx.fillStyle = '#1D490D';
        ctx.fillRect(12, 12, 896, 86);
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 26px sans-serif';
        ctx.fillText('ECOPARK CAMEROUN • BILLET QR COUPE-FILE HORS-LIGNE', 34, 52);
        ctx.font = '16px sans-serif';
        ctx.fillStyle = '#EDF4E7';
        ctx.fillText('Yaoundé – Ahala Barrière (RN3, Face Station Tradex Ahala) • Tél : +237 697 13 62 03', 34, 80);

        // Détails du billet
        ctx.fillStyle = '#1D490D';
        ctx.font = 'bold 30px sans-serif';
        ctx.fillText('RÉFÉRENCE : ' + ref, 36, 150);

        ctx.fillStyle = '#1E281B';
        ctx.font = 'bold 20px sans-serif';
        ctx.fillText('Titulaire : ' + holder, 36, 198);
        ctx.font = '18px sans-serif';
        ctx.fillText('Date & Créneau : ' + dateStr, 36, 236);
        ctx.fillText('Prestations : ' + itemsStr.slice(0, 62), 36, 274);
        ctx.fillStyle = '#9A5B13';
        ctx.font = 'bold 24px sans-serif';
        ctx.fillText('Montant TTC : ' + totalStr + ' (Tarif enfant protégé 500 FCFA)', 36, 326);

        ctx.fillStyle = '#1D490D';
        ctx.font = '15px sans-serif';
        ctx.fillText("Billet valable même sans connexion Internet mobile • Contrôle unique au tourniquet d'Ahala.", 36, 395);

        // Dessin du QR Code stylisé à droite
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(680, 125, 190, 190);
        ctx.strokeStyle = '#1D490D';
        ctx.lineWidth = 4;
        ctx.strokeRect(680, 125, 190, 190);
        ctx.fillStyle = '#1D490D';
        ctx.fillRect(700, 145, 44, 44);
        ctx.fillRect(806, 145, 44, 44);
        ctx.fillRect(700, 251, 44, 44);
        ctx.fillRect(760, 195, 32, 32);
        ctx.fillStyle = '#1F880B';
        ctx.fillRect(800, 245, 48, 48);
      }

      try {
        const dataUrl = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = dataUrl;
        a.download = `Billet-QR-ECOPARK-${ref}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (e) {}
      showToastSprint1(`• Pass QR Hors-Ligne (${ref}.png) téléchargé ! Vous pouvez le présenter au portail d'Ahala même sans forfait Internet.`);
      return ref;
    }

    // Impression / Génération PDF Officielle (Billet QR, Facture Proforma École/B2B, PV Clôture de Caisse)
    function printOfficialDocument(docType) {
      const db = ensureAppointmentsArray(loadDB());
      const overlay = document.getElementById('modalOverlaySprint1');
      const box = document.getElementById('modalOfficialPrintBox');
      const titleEl = document.getElementById('officialPrintTitle');
      const bodyEl = document.getElementById('officialPrintBody');
      if (!overlay || !box || !bodyEl) return;

      ['modalQuoteBox', 'modalCfpBox', 'modalRdvBox', 'modalRescheduleBox'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });

      if (docType === 'PROFORMA') {
        const calc = computeQuoteBudgetSprint1();
        const org = ((document.getElementById('quoteOrgName') || {}).value || 'Établissement Scolaire / Ministère / Entreprise');
        const date = ((document.getElementById('quoteDate') || {}).value || '2026-12-10');
        const type = ((document.getElementById('quoteType') || {}).value || 'Excursion scolaire');
        const qRef = (db.quotes && db.quotes[0]) ? db.quotes[0].reference : 'DEV-2026-3104';
        if (titleEl) titleEl.textContent = `FACTURE PROFORMA OFFICIELLE N° ${qRef}`;
        bodyEl.innerHTML = `
          <div style="display:flex;justify-content:space-between;background:#FBF5EC;padding:12px;border-radius:8px;border:1px solid rgba(196,125,43,0.4);">
            <div><strong>Client / Institution :</strong> ${org}<br/><strong>Objet :</strong> ${type}</div>
            <div style="text-align:right;"><strong>Date prévue :</strong> ${date}<br/><strong>Effectif :</strong> ${calc.pax} participants</div>
          </div>
          <table style="width:100%;border-collapse:collapse;margin-top:8px;">
            <thead>
              <tr style="background:var(--color-surface-soft);">
                <th style="padding:8px;border:1px solid var(--color-border);text-align:left;">Désignation des Prestations ECOPARK Ahala</th>
                <th style="padding:8px;border:1px solid var(--color-border);text-align:right;">Montant (FCFA)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="padding:8px;border:1px solid var(--color-border);">${calc.pax} × ${calc.rateDesc}</td>
                <td style="padding:8px;border:1px solid var(--color-border);text-align:right;"><strong>${formatFCFA(calc.pax * calc.unitRate)}</strong></td>
              </tr>
              <tr>
                <td style="padding:8px;border:1px solid var(--color-border);">Options &amp; Logistique : ${calc.optionsSummary}</td>
                <td style="padding:8px;border:1px solid var(--color-border);text-align:right;"><strong>${formatFCFA(calc.hallCost + calc.shuttleCost)}</strong></td>
              </tr>
              <tr style="background:#EDF4E7;">
                <td style="padding:10px 8px;border:1px solid var(--color-border);"><strong>TOTAL NET TTC À PAYER (Francs CFA)</strong></td>
                <td style="padding:10px 8px;border:1px solid var(--color-border);text-align:right;font-size:1.2rem;color:var(--color-brand-deep);"><strong>${formatFCFA(calc.total)}</strong></td>
              </tr>
            </tbody>
          </table>
          <div style="font-size:12.8px;color:var(--color-text-muted);">
            <strong>Conditions :</strong> Tarif enfant (3–12 ans) garanti à 500 FCFA. Règlement par Mobile Money Marchand (Orange Money / MTN MoMo), virement ou espèces au Guichet Principal d'Ahala Barrière.
          </div>
        `;
      } else if (docType === 'CLOSURE') {
        if (titleEl) titleEl.textContent = `PV DE CLÔTURE DE CAISSE & RAPPORT D'EXPLOITATION (${nowStamp()})`;
        bodyEl.innerHTML = `
          <div class="grid-12" style="gap:10px;">
            <div class="col-4" style="padding:10px;background:var(--color-surface-soft);border-radius:8px;">
              <span>Espèces Guichet #1</span><br/><strong style="font-size:1.25rem;color:var(--color-brand-deep);">${formatFCFA(db.posStats.cashFcfa)}</strong>
            </div>
            <div class="col-4" style="padding:10px;background:var(--color-surface-soft);border-radius:8px;">
              <span>Mobile Money Guichet</span><br/><strong style="font-size:1.25rem;color:var(--color-brand-deep);">${formatFCFA(db.posStats.momoFcfa)}</strong>
            </div>
            <div class="col-4" style="padding:10px;background:var(--color-surface-soft);border-radius:8px;">
              <span>Entrées Tourniquet</span><br/><strong style="font-size:1.25rem;color:var(--color-brand-deep);">${db.posStats.validatedEntries} validées</strong>
            </div>
          </div>
          <div style="padding:10px;background:#FBF5EC;border-radius:8px;border:1px solid rgba(196,125,43,0.35);">
            <strong>Consolidation Direction Générale (DIR-01) :</strong> Recettes mensuelles : <strong>${formatFCFA(db.dirStats.monthlyRevenueFcfa)}</strong> • Dossiers actifs : <strong>${db.bookings.length} billets QR</strong>, <strong>${db.quotes.length} devis groupes</strong>, <strong>${db.appointments.length} RDV</strong>, <strong>${db.cfpApplications.length} candidatures CFP</strong>.
          </div>
        `;
      } else {
        const ref = getActiveTicketRef();
        const holder = (document.getElementById('ticketHolder') || {}).textContent || 'Visiteur ECOPARK';
        const dateStr = (document.getElementById('ticketDate') || {}).textContent || 'Valable 09h00 – 18h00';
        const itemsStr = (document.getElementById('ticketItems') || {}).textContent || 'Entrée Parc & Zoo, Piscine, Pirogue';
        const totalStr = (document.getElementById('grandTotalFCFA') || {}).textContent || '14 000 FCFA';
        if (titleEl) titleEl.textContent = `E-BILLET OFFICIEL COUPE-FILE — ${ref}`;
        bodyEl.innerHTML = `
          <div style="padding:14px;background:var(--color-surface-soft);border:2px solid var(--color-brand-deep);border-radius:12px;">
            <div style="font-size:1.2rem;font-weight:700;color:var(--color-brand-deep);margin-bottom:6px;">Code Référence : ${ref} • Total TTC : ${totalStr}</div>
            <div><strong>Titulaire :</strong> ${holder}</div>
            <div><strong>Date &amp; Validité :</strong> ${dateStr}</div>
            <div><strong>Prestations &amp; Logistique :</strong> ${itemsStr}</div>
            <div><strong>Repère GPS :</strong> Route Nationale N°3, Ahala Barrière (En face de la Station Tradex Ahala, Yaoundé)</div>
          </div>
        `;
      }

      overlay.style.display = 'flex';
      box.style.display = 'block';
    }

    // Export CSV (Excel) de toute la base d'exploitation (DIR-05 / AGT-09)
    function exportEcoparkDatabaseCSV() {
      const db = ensureAppointmentsArray(loadDB());
      const rows = [
        ['CATEGORIE', 'REFERENCE', 'TITULAIRE_OU_STRUCTURE', 'DATE_CRENEAU', 'PRESTATIONS_DETAILS', 'MONTANT_FCFA', 'STATUT']
      ];
      (db.bookings || []).forEach(b => {
        rows.push(['BILLET_QR', b.reference, b.holder, b.date, b.paxSummary, String(b.totalFcfa), b.scanned ? 'UTILISE' : b.status]);
      });
      (db.quotes || []).forEach(q => {
        rows.push(['DEVIS_GROUPE', q.reference, q.org, q.date, `${q.pax} pers. - ${q.type}`, String(q.budgetFcfa), q.status]);
      });
      (db.appointments || []).forEach(r => {
        rows.push(['RENDEZ_VOUS', r.reference, `${r.visitorName} (${r.org})`, `${r.date} ${r.slot}`, r.purposeLabel, '0', r.status]);
      });
      (db.cfpApplications || []).forEach(c => {
        rows.push(['CANDIDATURE_CFP', c.reference, c.name, 'Rentrée 2026', c.track, '50000', c.status]);
      });

      const csvContent = '\\uFEFF' + rows.map(r => r.map(v => `"${String(v || '').replace(/"/g, '""')}"`).join(';')).join('\\r\\n');
      try {
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ECOPARK_Ahala_Rapport_Exploitation_2026.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 1500);
      } catch (e) {}
      showToastSprint1(`• Export Comptable CSV (Excel) généré : ${rows.length - 1} dossiers (Billets QR, Devis, RDV & CFP) exportés !`);
      return rows.length - 1;
    }

    // Surcharger getActiveSimulatorItemsSummary pour inclure le plat / créneau 13h et le point de ramassage Navette
    if (typeof getActiveSimulatorItemsSummary === 'function') {
      const _origGetItemsSummary = getActiveSimulatorItemsSummary;
      getActiveSimulatorItemsSummary = function() {
        let base = _origGetItemsSummary();
        const repasChecked = (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) ||
                             (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked);
        if (repasChecked) {
          const dish = (document.getElementById('simDishSelect') || {}).value || "Poisson Braisé d'Ahala";
          const slot = (document.getElementById('simMealSlotSelect') || {}).value || 'Service 12h30';
          base += ` [${dish} • ${slot}]`;
        }
        if (document.getElementById('chkBumpNavette') && document.getElementById('chkBumpNavette').checked) {
          const pickup = (document.getElementById('simShuttlePickupSelect') || {}).value || 'Départ Poste Centrale (09h30)';
          base += ` [${pickup}]`;
        }
        return base;
      };
    }

    // Enrichir syncAllViewsFromDB pour gérer la recherche temps réel (RES-12 / ACC-01), les dossiers CFP et le bouton Reporter (ACC-05)
    const _prevSyncBefore7Omissions = syncAllViewsFromDB;
    syncAllViewsFromDB = function() {
      _prevSyncBefore7Omissions();
      const db = ensureAppointmentsArray(loadDB());
      const accTbody = document.querySelector('#view-ACC table tbody');
      if (!accTbody) return;

      const q = (((document.getElementById('accSearchInput') || {}).value || '')).trim().toLowerCase();
      const cat = window._accCategoryFilter || 'ALL';
      const matchQuery = (text) => !q || String(text || '').toLowerCase().includes(q);

      const htmlRows = [];

      if (cat === 'ALL' || cat === 'RDV') {
        (db.appointments || []).forEach(r => {
          const blob = `${r.reference} ${r.visitorName} ${r.org} ${r.phone || ''} ${r.purposeLabel} ${r.date}`;
          if (matchQuery(blob)) {
            htmlRows.push(`
              <tr data-dossier-kind="RDV">
                <td><strong>${r.reference}</strong></td>
                <td>${r.date} (${r.slot})</td>
                <td>RDV : ${r.purposeLabel} (${r.visitorName} — ${r.org})</td>
                <td><strong>Accueil Gratuit</strong></td>
                <td><span class="status-badge status-success">${r.status}</span></td>
                <td style="display:flex;gap:4px;flex-wrap:wrap;">
                  <button class="btn btn-secondary btn-sm" onclick="openRdvModalSprint1('${r.purposeCode}')">Voir RDV</button>
                  <button class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openRescheduleModal('${r.reference}', 'RDV')">Reporter date</button>
                </td>
              </tr>
            `);
          }
        });
      }

      if (cat === 'ALL' || cat === 'BOOKING') {
        (db.bookings || []).forEach(b => {
          const blob = `${b.reference} ${b.holder} ${b.phone || ''} ${b.paxSummary} ${b.date}`;
          if (matchQuery(blob)) {
            htmlRows.push(`
              <tr data-dossier-kind="BOOKING">
                <td><strong>${b.reference}</strong></td>
                <td>${b.date}</td>
                <td>${b.holder} • ${b.paxSummary}</td>
                <td><strong>${formatFCFA(b.totalFcfa)}</strong></td>
                <td><span class="status-badge ${b.scanned ? 'status-info' : 'status-success'}">${b.scanned ? 'Utilisé (' + b.scannedAt + ')' : (b.status === 'REPORTED' ? 'Date reportée (QR Actif)' : 'Confirmé (QR Actif)')}</span></td>
                <td style="display:flex;gap:4px;flex-wrap:wrap;">
                  <button class="btn btn-primary btn-sm" onclick="loadBookingIntoQrPass('${b.reference}')">Voir Billet QR</button>
                  <button class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openRescheduleModal('${b.reference}', 'BOOKING')">Reporter date</button>
                  <button class="btn btn-secondary btn-sm admin-only-control" onclick="document.getElementById('qrScanInput').value='${b.reference}'; navigateFamily('AGT', 'AGT-05')">Scanner</button>
                </td>
              </tr>
            `);
          }
        });
      }

      if (cat === 'ALL' || cat === 'QUOTE') {
        (db.quotes || []).forEach(qt => {
          const blob = `${qt.reference} ${qt.org} ${qt.type} ${qt.date}`;
          if (matchQuery(blob)) {
            htmlRows.push(`
              <tr data-dossier-kind="QUOTE">
                <td><strong>${qt.reference}</strong></td>
                <td>${qt.date}</td>
                <td>Devis ${qt.org} (${qt.pax} participants • ${qt.type})</td>
                <td><strong>${formatFCFA(qt.budgetFcfa)}</strong></td>
                <td><span class="status-badge status-info">${qt.status}</span></td>
                <td style="display:flex;gap:4px;flex-wrap:wrap;">
                  <button class="btn btn-secondary btn-sm" onclick="printOfficialDocument('PROFORMA')">Facture Proforma PDF</button>
                </td>
              </tr>
            `);
          }
        });
      }

      if (cat === 'ALL' || cat === 'CFP') {
        (db.cfpApplications || []).forEach(c => {
          const blob = `${c.reference} ${c.name} ${c.track} ${c.phone || ''}`;
          if (matchQuery(blob)) {
            htmlRows.push(`
              <tr data-dossier-kind="CFP">
                <td><strong>${c.reference}</strong></td>
                <td>Rentrée 2026</td>
                <td>Candidature CFP : ${c.name} • Filière ${c.track}</td>
                <td><strong>50 000 FCFA (Inscr.)</strong></td>
                <td><span class="status-badge status-success">${c.status}</span></td>
                <td>
                  <button class="btn btn-secondary btn-sm" onclick="openCfpModalSprint1()">Dossier CFP</button>
                </td>
              </tr>
            `);
          }
        });
      }

      if (htmlRows.length === 0) {
        accTbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:18px;color:var(--color-text-muted);">Aucun dossier ne correspond à votre recherche « ${q} ». Vérifiez la référence (ex: ECP-2026-84920) ou le numéro +237.</td></tr>`;
      } else {
        accTbody.innerHTML = htmlRows.join('');
      }
    };
    syncAllViewsFromDB();
"""


def upgrade_file(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject CSS before </style>
    if ".ahala-live-weather-bar" not in html:
        html = html.replace("  </style>", CSS_OMISSIONS_UPGRADE + "\n  </style>", 1)

    # 2. Inject Live Weather & Affluence bar at the top of #sec-PUB-01
    target_hero = '<div class="section" id="sec-PUB-01">\n          <div class="container">'
    if "ahalaLiveWeatherBar" not in html and target_hero in html:
        html = html.replace(target_hero, target_hero + "\n" + HTML_LIVE_WEATHER_BAR, 1)

    # 3. Inject Testimonials section (#sec-PUB-15) right before </section> of #view-PUB
    target_end_pub = '      <!-- ====================================================================\n           FAMILLE 3 : PRÉPARATION DE VISITE, DEVIS & RÉSERVATION (RES-01 à RES-12)'
    if 'id="sec-PUB-15"' not in html and target_end_pub in html:
        # Place right before closing </section> of #view-PUB
        split_idx = html.find(target_end_pub)
        last_sec_close = html.rfind("</section>", 0, split_idx)
        if last_sec_close != -1:
            html = html[:last_sec_close] + HTML_TESTIMONIALS_SECTION + "\n      " + html[last_sec_close:]

    # 4. Inject Kitchen Preorder Subpanel & Shuttle Pickup Subpanel in #sec-RES-03
    target_pergola_end = '<span class="price-pill" id="subBumpPergola">0 FCFA</span>\n                    </label>'
    if "kitchenPreorderSubpanel" not in html and target_pergola_end in html:
        html = html.replace(target_pergola_end, target_pergola_end + "\n" + HTML_KITCHEN_AND_SHUTTLE_SUBPANELS, 1)

    target_navette_end = '<span class="price-pill" id="subBumpNavette">0 FCFA</span>\n                    </label>'
    if "shuttlePickupSubpanel" not in html and target_navette_end in html:
        html = html.replace(target_navette_end, target_navette_end + "\n" + HTML_SHUTTLE_SUBPANEL, 1)

    # 5. Inject Offline QR Ticket Download & Print buttons on #demoTicketCard
    target_admin_ctrl_ticket = '<div class="admin-only-control" style="display:flex;gap:8px;flex-wrap:wrap;">\n                    <button type="button" class="btn btn-secondary btn-sm" onclick="navigateFamily(\'AGT\', \'AGT-05\')">Tester ce billet au Scanner d\'Entrée'
    if "btnDownloadQrPassOffline" not in html and target_admin_ctrl_ticket in html:
        html = html.replace(target_admin_ctrl_ticket, HTML_OFFLINE_TICKET_ACTIONS + "\n                  " + target_admin_ctrl_ticket, 1)

    # 6. Inject Printable Proforma button inside #modalQuoteBox
    target_quote_btns = '<button type="button" class="btn btn-primary" style="flex:1;" onclick="submitGroupQuoteSprint1()">Enregistrer &amp; Obtenir mon N° de Suivi</button>'
    if "printOfficialDocument('PROFORMA')" not in html and target_quote_btns in html:
        proforma_btn = '<button type="button" class="btn btn-secondary btn-sm" onclick="printOfficialDocument(\'PROFORMA\')">Imprimer / PDF Proforma</button>\n        '
        html = html.replace(target_quote_btns, proforma_btn + target_quote_btns, 1)

    # 7. Inject Live Lookup Input & Category Filter in #view-ACC
    target_acc_btn = '<button class="btn btn-secondary btn-sm" onclick="navigateFamily(\'RES\', \'RES-03\')">Créer une nouvelle réservation<span class="tech-code-tag"> (ACC-06)</span></button>'
    if "accSearchInput" not in html and target_acc_btn in html:
        html = html.replace(target_acc_btn, HTML_ACC_SEARCH_BOX + "\n                " + target_acc_btn, 1)

    # 8. Inject CSV Export & Cash Closure Print buttons in #view-AGT and #view-DIR
    target_agt_badge = '<span class="status-badge status-info">Écart constaté : 0 FCFA (Caisse conforme)</span>'
    if "btnExportCsvAgt" not in html and target_agt_badge in html:
        agt_actions = (
            '<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">'
            '<span class="status-badge status-info">Écart constaté : 0 FCFA (Caisse conforme)</span>'
            '<button type="button" class="btn btn-secondary btn-sm" id="btnPrintCashClosure" onclick="printOfficialDocument(\'CLOSURE\')">PV Clôture PDF</button>'
            '<button type="button" class="btn btn-primary btn-sm" id="btnExportCsvAgt" onclick="exportEcoparkDatabaseCSV()">Exporter CSV (Excel)</button>'
            '</div>'
        )
        html = html.replace(target_agt_badge, agt_actions, 1)

    target_dir_header = '<h2>Indicateurs Consolidés de Performance (en Francs CFA)</h2>'
    if "btnExportCsvDir" not in html and target_dir_header in html:
        dir_actions = (
            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">'
            '<h2>Indicateurs Consolidés de Performance (en Francs CFA)</h2>'
            '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
            '<button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="printOfficialDocument(\'CLOSURE\')">Rapport Exécutif Imprimable (DIR-05)</button>'
            '<button type="button" class="btn btn-primary btn-sm" id="btnExportCsvDir" onclick="exportEcoparkDatabaseCSV()">Exporter Base Complète CSV (Excel)</button>'
            '</div></div>'
        )
        html = html.replace(target_dir_header, dir_actions, 1)

    # 9. Upgrade #mobileStickyConversionBar with Mobile Quick Navigation Strip
    target_mobile_bar = '<div class="mobile-sticky-conversion-bar" id="mobileStickyConversionBar" aria-label="Accès rapide réservation et WhatsApp">'
    if "mobileQuickNavPills" not in html and target_mobile_bar in html:
        old_mobile_block = """  <div class="mobile-sticky-conversion-bar" id="mobileStickyConversionBar" aria-label="Accès rapide réservation et WhatsApp">
    <div>
      <span style="font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--color-text-muted);display:block;font-weight:700;" id="stickyBarPaxText">2 Adultes, 2 Enfants • Pass QR</span>
      <strong style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);" id="stickyBarTotalFcfa">14 000 FCFA</strong>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="padding:8px 12px;font-size:12.5px;" onclick="openStickyWhatsAppQuick()">
        <svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> WhatsApp
      </button>
      <button type="button" class="btn btn-primary btn-sm" style="padding:8px 14px;font-size:12.5px;" onclick="navigateFamily('RES', 'RES-03')">
        Réserver mon Pass
      </button>
    </div>
  </div>"""
        new_mobile_block = """  <div class="mobile-sticky-conversion-bar" id="mobileStickyConversionBar" style="flex-direction:column;align-items:stretch;" aria-label="Accès rapide réservation, navigation mobile et WhatsApp">
    <div class="mobile-quick-nav-strip" id="mobileQuickNavPills">
      <button type="button" class="mobile-quick-pill" onclick="navigateFamily('PUB', 'PUB-01')">Accueil</button>
      <button type="button" class="mobile-quick-pill" onclick="navigateFamily('PUB', 'PUB-10')">Tarifs FCFA</button>
      <button type="button" class="mobile-quick-pill" onclick="navigateFamily('PUB', 'PUB-08')">Hôtels</button>
      <button type="button" class="mobile-quick-pill" onclick="openRdvModalSprint1('reperage_mariage')">Prendre RDV</button>
      <button type="button" class="mobile-quick-pill" onclick="openQuoteModalSprint1()">Devis Groupe</button>
      <button type="button" class="mobile-quick-pill" onclick="openCfpModalSprint1()">Formation CFP</button>
      <button type="button" class="mobile-quick-pill" onclick="navigateFamily('ACC', 'ACC-02')">Mon Espace (QR)</button>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;width:100%;">
      <div>
        <span style="font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--color-text-muted);display:block;font-weight:700;" id="stickyBarPaxText">2 Adultes, 2 Enfants • Pass QR</span>
        <strong style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);" id="stickyBarTotalFcfa">14 000 FCFA</strong>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="padding:8px 12px;font-size:12.5px;" onclick="openStickyWhatsAppQuick()">
          <svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> WhatsApp
        </button>
        <button type="button" class="btn btn-primary btn-sm" style="padding:8px 14px;font-size:12.5px;" onclick="navigateFamily('RES', 'RES-03')">
          Réserver mon Pass
        </button>
      </div>
    </div>
  </div>"""
        if old_mobile_block in html:
            html = html.replace(old_mobile_block, new_mobile_block, 1)

    # 10. Inject Reschedule Modal & Official Print Modal inside #modalOverlaySprint1
    target_modal_overlay_end = "    </div>\n\n  </div>\n\n  <!-- LEVIER 3 : BARRE D'ACTION RAPIDE MOBILE"
    if "modalRescheduleBox" not in html and target_modal_overlay_end in html:
        html = html.replace(
            target_modal_overlay_end,
            "    </div>\n" + HTML_RESCHEDULE_AND_PRINT_MODALS + "\n  </div>\n\n  <!-- LEVIER 3 : BARRE D'ACTION RAPIDE MOBILE",
            1,
        )

    # 11. Inject JS functions before </script>
    if "function downloadOfflineQrTicketPng" not in html:
        html = html.replace("  </script>\n</body>", JS_OMISSIONS_UPGRADE + "\n  </script>\n</body>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Upgraded: {filepath} ({len(html)} bytes)")


if __name__ == "__main__":
    for path in FILES:
        if os.path.exists(path):
            upgrade_file(path)
