# -*- coding: utf-8 -*-
"""
Intégration du module interactif « Prise de RDV » sur ECOPARK Cameroun (Yaoundé-Ahala) :
- Visite de repérage Mariage / Gala / Réception (Salle « Menkii Essomba Anton » & Château des Saveurs)
- Rendez-vous Direction B2B (Séminaires Ministères / ONG / Entreprises & Navettes 5/18/32 places)
- Visite préparatoire Excursion Scolaire (Parcours sécurité Zoo « ToTo », Piscine & Pirogues)
- Entretien d'Orientation & Visite du Campus CFP ECOPARK (5 filières MINEFOP)
Avec choix interactif du créneau horaire, persistance temps réel (RDV-2026-XXXX), synchronisation Mon Espace (ACC) / Exploitation (EXP) / Audit (ADM-08), confirmation WhatsApp (+237 697 13 62 03) et timeline HyperFrames window.__timelines["ecopark-rdv-flow"].
"""
import pathlib

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
TARGETS = [
    ROOT / "etape0-site-live" / "index.html",
    ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

RDV_CSS = """
    /* ==========================================================================
       MODULE INTERACTIF DE PRISE DE RENDEZ-VOUS (REPÉRAGE, B2B, ÉCOLES & CFP)
       ========================================================================== */
    .rdv-purpose-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-top: 8px;
    }
    @media (max-width: 640px) {
      .rdv-purpose-grid {
        grid-template-columns: 1fr;
      }
    }
    .rdv-purpose-card {
      text-align: left;
      padding: 12px 14px;
      border-radius: 16px;
      border: 1.5px solid rgba(29, 73, 13, 0.14);
      background: var(--color-surface-soft);
      color: var(--color-text-main);
      cursor: pointer;
      transition: all 0.35s var(--hf-ease-out-expo, cubic-bezier(0.16, 1, 0.3, 1));
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .rdv-purpose-card:hover {
      border-color: var(--color-accent-ochre);
      transform: translate3d(0, -2px, 0);
    }
    .rdv-purpose-card.active {
      background: var(--color-accent-ochre-soft);
      border-color: var(--color-accent-ochre);
      box-shadow: 0 10px 24px rgba(196, 125, 43, 0.14);
    }
    .rdv-purpose-card strong {
      font-family: var(--font-heading);
      font-size: 1rem;
      color: var(--color-brand-deep);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
    }
    .rdv-purpose-card.active strong {
      color: var(--color-accent-ochre-deep);
    }
    .rdv-purpose-card span {
      font-size: 12.8px;
      color: var(--color-text-muted);
      line-height: 1.35;
    }

    .rdv-slot-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 6px;
    }
    @media (max-width: 640px) {
      .rdv-slot-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    .rdv-slot-pill {
      padding: 9px 10px;
      border-radius: 12px;
      border: 1.5px solid rgba(29, 73, 13, 0.16);
      background: #FFFFFF;
      color: var(--color-brand-deep);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: all 0.28s var(--hf-ease-out-expo, cubic-bezier(0.16, 1, 0.3, 1));
    }
    .rdv-slot-pill:hover {
      border-color: var(--color-accent-ochre);
      background: var(--color-accent-ochre-soft);
    }
    .rdv-slot-pill.active {
      background: var(--color-brand-deep);
      color: #FFFFFF;
      border-color: var(--color-brand-deep);
      box-shadow: 0 6px 16px rgba(29, 73, 13, 0.22);
    }
    .rdv-slot-pill small {
      display: block;
      font-size: 11px;
      font-weight: 400;
      opacity: 0.82;
      margin-top: 2px;
    }

    .rdv-confirm-pass {
      margin-top: 14px;
      padding: 16px 18px;
      border-radius: 18px;
      background: linear-gradient(135deg, #FBF5EC 0%, #EDF4E7 100%);
      border: 1.5px solid var(--color-accent-ochre);
      display: none;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 14px 32px rgba(196, 125, 43, 0.16);
    }
    .rdv-confirm-pass.open {
      display: flex;
    }
"""

RDV_SECTION_HTML = """
              <!-- Module Dédié de Prise de Rendez-Vous sur Site ou à Distance (PUB-18 / RES-06) -->
              <div class="col-12 card clip" id="sec-PUB-18" data-composition-id="ecopark-rdv-flow" data-start="0" data-duration="0.8" data-track-index="1" style="background:linear-gradient(145deg, #FFFFFF 0%, #F4F9F0 65%, #FBF5EC 100%);border:1px solid rgba(196, 125, 43, 0.28);">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                  <div>
                    <span class="eyebrow eyebrow-hospitality" style="margin-bottom:4px;">Accueil Personnalisé • Direction, Événementiel &amp; CFP</span>
                    <h3><span class="icon-medallion medallion-hospitality"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/></svg></span> <span class="tech-code-tag">PUB-18 — </span>Prendre Rendez-Vous à ECOPARK Yaoundé-Ahala</h3>
                    <p style="font-size:15px;color:var(--color-text-muted);margin-top:4px;max-width:780px;">
                      Réservez un créneau dédié avec notre équipe du Mardi au Dimanche (09h30 à 17h00) pour une <strong>visite guidée de repérage</strong> (mariage, séminaire en Salle « Menkii Essomba Anton », sortie d'école) ou un <strong>entretien d'orientation au CFP ECOPARK</strong>.
                    </p>
                  </div>
                  <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                    <span class="price-pill" id="liveRdvCountBadge">Dernier RDV : RDV-2026-4102 (Confirmé)</span>
                    <button type="button" class="btn btn-primary" onclick="openRdvModalSprint1('reperage_mariage')">
                      <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg> Choisir mon créneau de RDV
                    </button>
                  </div>
                </div>

                <div class="grid-12" style="margin-top:14px;gap:14px;">
                  <div class="col-3 card" style="padding:16px;background:#FFFFFF;cursor:pointer;" onclick="openRdvModalSprint1('reperage_mariage')">
                    <span class="eyebrow eyebrow-hospitality" style="margin:0;font-size:11px;">1 • Mariages &amp; Galas</span>
                    <strong style="font-family:var(--font-heading);font-size:1.08rem;color:var(--color-brand-deep);">Visite de Repérage Réception</strong>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin:4px 0 10px;">Inspection de l'esplanade, de la Salle « Menkii Essomba Anton » et dégustation au Château des Saveurs.</p>
                    <span style="font-size:13px;font-weight:700;color:var(--color-accent-ochre-deep);">Planifier ce RDV →</span>
                  </div>
                  <div class="col-3 card" style="padding:16px;background:#FFFFFF;cursor:pointer;" onclick="openRdvModalSprint1('seminaire_b2b')">
                    <span class="eyebrow" style="margin:0;font-size:11px;">2 • Ministères, ONG &amp; B2B</span>
                    <strong style="font-family:var(--font-heading);font-size:1.08rem;color:var(--color-brand-deep);">RDV Séminaire &amp; Hébergement</strong>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin:4px 0 10px;">Configuration conférence, pauses-café, Cités Ewondo/Chanthel/Bene et navettes 5, 18 ou 32 places.</p>
                    <span style="font-size:13px;font-weight:700;color:var(--color-brand-deep);">Planifier ce RDV →</span>
                  </div>
                  <div class="col-3 card" style="padding:16px;background:#FFFFFF;cursor:pointer;" onclick="openRdvModalSprint1('visite_ecole')">
                    <span class="eyebrow" style="margin:0;font-size:11px;">3 • Écoles &amp; Associations</span>
                    <strong style="font-family:var(--font-heading);font-size:1.08rem;color:var(--color-brand-deep);">Repérage Excursion Scolaire</strong>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin:4px 0 10px;">Validation du circuit sécurité avec les enseignants : Zoo (« ToTo »), Piscine surveillée et Pirogues.</p>
                    <span style="font-size:13px;font-weight:700;color:var(--color-brand-deep);">Planifier ce RDV →</span>
                  </div>
                  <div class="col-3 card" style="padding:16px;background:#FFFFFF;cursor:pointer;" onclick="openRdvModalSprint1('orientation_cfp')">
                    <span class="eyebrow eyebrow-hospitality" style="margin:0;font-size:11px;">4 • Formation MINEFOP</span>
                    <strong style="font-family:var(--font-heading);font-size:1.08rem;color:var(--color-brand-deep);">RDV Orientation &amp; Campus CFP</strong>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin:4px 0 10px;">Visite des bassins piscicoles, cuisines et hôtels d'application (Inscription 50 000 FCFA • 4 tranches).</p>
                    <span style="font-size:13px;font-weight:700;color:var(--color-accent-ochre-deep);">Planifier ce RDV →</span>
                  </div>
                </div>
              </div>
"""

RDV_MODAL_HTML = """
    <!-- Modale Interactive de Prise de Rendez-Vous (PUB-18 / RES-06 / EXP-07) -->
    <div id="modalRdvBox" class="card" style="display:none;max-width:640px;width:100%;background:#FFFFFF;padding:28px 32px;max-height:92vh;overflow-y:auto;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow eyebrow-hospitality" style="margin:0;">Agenda Officiel ECOPARK • Yaoundé-Ahala (Face Station Tradex)</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()"><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg> Fermer</button>
      </div>
      <h3 style="margin-top:4px;">Planifier un Rendez-Vous Personnalisé</h3>
      <p style="font-size:14px;color:var(--color-text-muted);margin-bottom:6px;">
        Choisissez l'objet de votre venue, votre date et votre créneau horaire. Un conseiller dédié vous accueille à Ahala Barrière (parking gratuit 150 places) ou vous contacte sur WhatsApp.
      </p>

      <div>
        <label class="form-label" style="margin-bottom:4px;">1. Motif du rendez-vous</label>
        <input type="hidden" id="rdvPurposeCode" value="reperage_mariage" />
        <div class="rdv-purpose-grid" id="rdvPurposeGrid">
          <button type="button" class="rdv-purpose-card active" data-purpose="reperage_mariage" onclick="selectRdvPurpose('reperage_mariage', this)">
            <strong><span>Repérage Mariage &amp; Réception</span> <span class="price-pill" style="padding:2px 8px !important;font-size:11px;">Salle &amp; Traiteur</span></strong>
            <span>Visite de la Salle « Menkii Essomba Anton », esplanade et dégustation Château des Saveurs.</span>
          </button>
          <button type="button" class="rdv-purpose-card" data-purpose="seminaire_b2b" onclick="selectRdvPurpose('seminaire_b2b', this)">
            <strong><span>Séminaire B2B / Ministère / ONG</span> <span class="price-pill" style="padding:2px 8px !important;font-size:11px;">Devis &amp; Loges</span></strong>
            <span>Configuration salle climatisée, hébergement Cités Ewondo/Chanthel/Bene et navettes.</span>
          </button>
          <button type="button" class="rdv-purpose-card" data-purpose="visite_ecole" onclick="selectRdvPurpose('visite_ecole', this)">
            <strong><span>Repérage Excursion Scolaire</span> <span class="price-pill" style="padding:2px 8px !important;font-size:11px;">Enfant 500 F</span></strong>
            <span>Parcours sécurité avec les enseignants : Zoo (« ToTo »), Piscine surveillée et Pirogues.</span>
          </button>
          <button type="button" class="rdv-purpose-card" data-purpose="orientation_cfp" onclick="selectRdvPurpose('orientation_cfp', this)">
            <strong><span>Orientation &amp; Visite Campus CFP</span> <span class="price-pill" style="padding:2px 8px !important;font-size:11px;">5 Filières</span></strong>
            <span>Entretien pédagogique MINEFOP et visite des ateliers pratiques (Hôtellerie, Pisciculture...).</span>
          </button>
        </div>
      </div>

      <div class="grid-12" style="gap:12px;margin-top:12px;">
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="rdvDate">2. Date souhaitée (Mardi au Dimanche)</label>
          <input type="date" id="rdvDate" class="form-control" value="2026-11-18" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="rdvMode">Format du rendez-vous</label>
          <select id="rdvMode" class="form-control">
            <option value="Sur place à Ahala Barrière (Face station Tradex)">Sur place à Ahala Barrière (Accueil Direction)</option>
            <option value="Appel WhatsApp Vidéo / Téléphone (+237 697 13 62 03)">Appel WhatsApp Vidéo / Téléphone (+237)</option>
          </select>
        </div>
      </div>

      <div style="margin-top:10px;">
        <label class="form-label" style="margin-bottom:4px;">3. Créneau horaire garanti</label>
        <input type="hidden" id="rdvTimeSlot" value="11h00 – 12h00" />
        <div class="rdv-slot-grid" id="rdvSlotGrid">
          <button type="button" class="rdv-slot-pill" data-slot="09h30 – 10h30" onclick="selectRdvSlot('09h30 – 10h30', this)">
            09h30 – 10h30
            <small>Matinée fraîcheur</small>
          </button>
          <button type="button" class="rdv-slot-pill active" data-slot="11h00 – 12h00" onclick="selectRdvSlot('11h00 – 12h00', this)">
            11h00 – 12h00
            <small>Recommandé</small>
          </button>
          <button type="button" class="rdv-slot-pill" data-slot="14h00 – 15h00" onclick="selectRdvSlot('14h00 – 15h00', this)">
            14h00 – 15h00
            <small>Après-midi</small>
          </button>
          <button type="button" class="rdv-slot-pill" data-slot="16h00 – 17h00" onclick="selectRdvSlot('16h00 – 17h00', this)">
            16h00 – 17h00
            <small>Fin de journée</small>
          </button>
        </div>
      </div>

      <div class="grid-12" style="gap:12px;margin-top:12px;">
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="rdvVisitorName">Votre Nom &amp; Prénom</label>
          <input type="text" id="rdvVisitorName" class="form-control" value="Mme Solange ETOUNDI" />
        </div>
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="rdvOrgName">Structure / Événement</label>
          <input type="text" id="rdvOrgName" class="form-control" value="Comité Gala &amp; Mariage Yaoundé" />
        </div>
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="rdvPhone">Téléphone WhatsApp (+237)</label>
          <input type="tel" id="rdvPhone" class="form-control" value="+237 697 13 62 03" />
        </div>
      </div>

      <div id="rdvConfirmPass" class="rdv-confirm-pass">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
          <span class="status-badge badge-qr-prestige" style="font-weight:700;">Pass Rendez-Vous Confirmé</span>
          <strong id="rdvConfirmRef" style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);">RDV-2026-4102</strong>
        </div>
        <div id="rdvConfirmSummary" style="font-size:13.8px;color:var(--color-text-main);">
          Votre créneau est réservé auprès de la Direction d'Exploitation ECOPARK Ahala.
        </div>
      </div>

      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1.2;" onclick="submitRdvSprint1()">
          <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="m9 16 2 2 4-4"/></svg> Confirmer mon RDV &amp; Obtenir mon N°
        </button>
        <button type="button" class="btn btn-secondary btn-ochre-outline" style="flex:1;" onclick="sendWhatsAppRdvSprint1()">
          <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> Envoyer sur WhatsApp (+237 697 13 62 03)
        </button>
      </div>
    </div>
"""

RDV_JS = """
    // ========================================================================
    // MODULE INTERACTIF DE PRISE DE RENDEZ-VOUS (REPÉRAGE, B2B, ÉCOLES & CFP)
    // ========================================================================
    const RDV_PURPOSE_LABELS = {
      reperage_mariage: "Visite de repérage — Mariage, Gala & Salle Menkii Essomba Anton",
      seminaire_b2b: "Rendez-vous B2B — Séminaire Ministère / ONG / Entreprise & Loges",
      visite_ecole: "Visite préparatoire — Excursion Scolaire (Zoo ToTo, Piscine, Pirogues)",
      orientation_cfp: "Entretien d'Orientation & Visite du Campus CFP ECOPARK (5 filières)"
    };

    function ensureAppointmentsArray(db) {
      if (!Array.isArray(db.appointments)) {
        db.appointments = [
          {
            reference: "RDV-2026-4102",
            visitorName: "Mme Solange ETOUNDI",
            org: "Comité Gala & Mariage Yaoundé",
            phone: "+237 697 13 62 03",
            purposeCode: "reperage_mariage",
            purposeLabel: RDV_PURPOSE_LABELS.reperage_mariage,
            date: "18/11/2026",
            slot: "11h00 – 12h00",
            mode: "Sur place à Ahala Barrière (Face station Tradex)",
            status: "RDV Confirmé (Accueil Direction)"
          }
        ];
      }
      return db;
    }

    function openRdvModalSprint1(defaultPurpose) {
      const overlay = document.getElementById('modalOverlaySprint1');
      const quoteBox = document.getElementById('modalQuoteBox');
      const cfpBox = document.getElementById('modalCfpBox');
      const rdvBox = document.getElementById('modalRdvBox');
      if (overlay) overlay.style.display = 'flex';
      if (quoteBox) quoteBox.style.display = 'none';
      if (cfpBox) cfpBox.style.display = 'none';
      if (rdvBox) {
        rdvBox.style.display = 'block';
        if (rdvBox.animate && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          rdvBox.animate([
            { opacity: 0, transform: 'translate3d(0, 18px, 0) scale(0.97)' },
            { opacity: 1, transform: 'translate3d(0, 0, 0) scale(1)' }
          ], { duration: 420, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
        }
      }
      if (defaultPurpose && RDV_PURPOSE_LABELS[defaultPurpose]) {
        const btn = document.querySelector(`#rdvPurposeGrid .rdv-purpose-card[data-purpose="${defaultPurpose}"]`);
        selectRdvPurpose(defaultPurpose, btn);
      }
    }

    const _origOpenQuoteForRdv = openQuoteModalSprint1;
    openQuoteModalSprint1 = function() {
      const rdvBox = document.getElementById('modalRdvBox');
      if (rdvBox) rdvBox.style.display = 'none';
      _origOpenQuoteForRdv();
    };

    const _origOpenCfpForRdv = openCfpModalSprint1;
    openCfpModalSprint1 = function() {
      const rdvBox = document.getElementById('modalRdvBox');
      if (rdvBox) rdvBox.style.display = 'none';
      _origOpenCfpForRdv();
    };

    function selectRdvPurpose(code, btnEl) {
      const input = document.getElementById('rdvPurposeCode');
      if (input) input.value = code;
      document.querySelectorAll('#rdvPurposeGrid .rdv-purpose-card').forEach(b => {
        b.classList.toggle('active', b === btnEl || b.getAttribute('data-purpose') === code);
      });
    }

    function selectRdvSlot(slot, btnEl) {
      const input = document.getElementById('rdvTimeSlot');
      if (input) input.value = slot;
      document.querySelectorAll('#rdvSlotGrid .rdv-slot-pill').forEach(b => {
        b.classList.toggle('active', b === btnEl || b.getAttribute('data-slot') === slot);
      });
    }

    function submitRdvSprint1() {
      const db = ensureAppointmentsArray(loadDB());
      const visitorName = (document.getElementById('rdvVisitorName') || {}).value || 'Visiteur ECOPARK';
      const org = (document.getElementById('rdvOrgName') || {}).value || 'Particulier / Organisation';
      const phone = (document.getElementById('rdvPhone') || {}).value || '+237 697 13 62 03';
      const purposeCode = (document.getElementById('rdvPurposeCode') || {}).value || 'reperage_mariage';
      const purposeLabel = RDV_PURPOSE_LABELS[purposeCode] || RDV_PURPOSE_LABELS.reperage_mariage;
      const date = (document.getElementById('rdvDate') || {}).value || '2026-11-18';
      const slot = (document.getElementById('rdvTimeSlot') || {}).value || '11h00 – 12h00';
      const mode = (document.getElementById('rdvMode') || {}).value || 'Sur place à Ahala Barrière (Face station Tradex)';
      const ref = 'RDV-2026-' + Math.floor(1000 + Math.random() * 8999);

      const newRdv = {
        reference: ref,
        visitorName,
        org,
        phone,
        purposeCode,
        purposeLabel,
        date,
        slot,
        mode,
        status: 'RDV Confirmé (' + slot + ')'
      };
      db.appointments.unshift(newRdv);
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${visitorName} (${org})`,
        action: `Prise de rendez-vous ${ref} (${purposeLabel}) confirmée pour le ${date} à ${slot}.`
      });
      saveDB(db);
      syncRdvViews();

      const passEl = document.getElementById('rdvConfirmPass');
      const refEl = document.getElementById('rdvConfirmRef');
      const sumEl = document.getElementById('rdvConfirmSummary');
      if (refEl) refEl.textContent = ref;
      if (sumEl) {
        sumEl.innerHTML = `<strong>${visitorName} (${org})</strong> — <em>${purposeLabel}</em><br/>Date : <strong>${date}</strong> • Créneau : <strong>${slot}</strong> • Format : ${mode}`;
      }
      if (passEl) {
        passEl.classList.add('open');
        if (passEl.animate && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          passEl.animate([
            { transform: 'perspective(800px) rotateX(8deg) translateY(8px)', opacity: 0.4 },
            { transform: 'none', opacity: 1 }
          ], { duration: 620, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
        }
      }
      showToastSprint1(`• Rendez-vous ${ref} (${date} à ${slot}) enregistré ! Visible dans « Mon Espace » (ACC-04) et « Exploitation » (EXP-07).`);
      return ref;
    }

    function sendWhatsAppRdvSprint1() {
      const visitorName = (document.getElementById('rdvVisitorName') || {}).value || 'Visiteur ECOPARK';
      const org = (document.getElementById('rdvOrgName') || {}).value || '';
      const phone = (document.getElementById('rdvPhone') || {}).value || '';
      const purposeCode = (document.getElementById('rdvPurposeCode') || {}).value || 'reperage_mariage';
      const purposeLabel = RDV_PURPOSE_LABELS[purposeCode] || RDV_PURPOSE_LABELS.reperage_mariage;
      const date = (document.getElementById('rdvDate') || {}).value || '2026-11-18';
      const slot = (document.getElementById('rdvTimeSlot') || {}).value || '11h00 – 12h00';
      const mode = (document.getElementById('rdvMode') || {}).value || 'Sur place à Ahala Barrière';
      const ref = (document.getElementById('rdvConfirmRef') || {}).textContent || 'RDV-2026';

      const msg = [
        `Bonjour ECOPARK CAMEROUN (Yaoundé-Ahala),`,
        `Je souhaite confirmer ma prise de rendez-vous :`,
        `- Référence : ${ref}`,
        `- Objet : ${purposeLabel}`,
        `- Date & Créneau : ${date} (${slot})`,
        `- Format : ${mode}`,
        `- Contact : ${visitorName} (${org}) — ${phone}`,
        `Merci de me confirmer la disponibilité de l'équipe d'accueil.`
      ].join('\\n');
      const url = 'https://wa.me/237697136203?text=' + encodeURIComponent(msg);
      window.open(url, '_blank', 'noopener,noreferrer');
    }

    function syncRdvViews() {
      const db = ensureAppointmentsArray(loadDB());
      const latestRdv = db.appointments[0];
      const badgeEl = document.getElementById('liveRdvCountBadge');
      if (badgeEl && latestRdv) {
        badgeEl.textContent = `Dernier RDV : ${latestRdv.reference} (${latestRdv.date} • ${latestRdv.slot})`;
      }

      // Ajouter le dernier RDV dans le tableau Mon Espace (ACC)
      const accTbody = document.querySelector('#view-ACC table tbody');
      if (accTbody && latestRdv && !accTbody.innerHTML.includes(latestRdv.reference)) {
        const rdvRow = `
          <tr>
            <td><strong>${latestRdv.reference}</strong></td>
            <td>${latestRdv.date} (${latestRdv.slot})</td>
            <td>RDV : ${latestRdv.purposeLabel} (${latestRdv.org})</td>
            <td><strong>Accueil Gratuit</strong></td>
            <td><span class="status-badge status-success">${latestRdv.status}</span></td>
            <td><button class="btn btn-secondary btn-sm" onclick="openRdvModalSprint1('${latestRdv.purposeCode}')">Modifier RDV</button></td>
          </tr>
        `;
        accTbody.insertAdjacentHTML('afterbegin', rdvRow);
      }

      // Mettre à jour la ligne EXP-07 dans Exploitation avec le dernier RDV
      const expTables = document.querySelectorAll('#view-EXP table tbody');
      if (expTables.length >= 2 && latestRdv) {
        const rows = expTables[1].querySelectorAll('tr');
        if (rows.length >= 3) {
          rows[2].innerHTML = `
            <td><code>EXP-07</code> Agenda RDV</td>
            <td>${latestRdv.visitorName} — ${latestRdv.org} (${latestRdv.reference})</td>
            <td>${latestRdv.purposeLabel} • ${latestRdv.date} (${latestRdv.slot})</td>
            <td><span class="status-badge status-success">${latestRdv.status}</span></td>
          `;
        }
      }
    }

    const _origSyncAllViewsForRdv = syncAllViewsFromDB;
    syncAllViewsFromDB = function() {
      _origSyncAllViewsForRdv();
      syncRdvViews();
    };
    syncRdvViews();

    window.__timelines = window.__timelines || {};
    window.__timelines['ecopark-rdv-flow'] = {
      id: 'ecopark-rdv-flow',
      duration: 0.8,
      fps: 60,
      tracks: 1,
      play() { openRdvModalSprint1('reperage_mariage'); },
      seek() {}
    };

    (function checkRdvRoute() {
      const path = (window.location.pathname || '/').replace(/\\/+$/, '').toLowerCase();
      if (path === '/rdv' || path === '/rendez-vous') {
        setTimeout(() => {
          navigateFamily('PUB', 'PUB-18');
          openRdvModalSprint1('reperage_mariage');
        }, 90);
      }
    })();
"""


def inject_rdv_module(path: pathlib.Path):
    html = path.read_text(encoding="utf-8")

    # 1. Inject RDV CSS before </style>
    if "MODULE INTERACTIF DE PRISE DE RENDEZ-VOUS" not in html:
        html = html.replace("  </style>", RDV_CSS + "\n  </style>", 1)

    # 2. Add "Prendre RDV" button in Header CTA bar
    old_header_cta = """        <div style="display:flex;align-items:center;gap:10px;">
          <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openQuoteModalSprint1()">Devis École / Groupe</button>
          <button type="button" class="btn btn-primary btn-sm" onclick="navigateFamily('RES', 'RES-01')">Préparer ma visite & Billets</button>
        </div>"""
    new_header_cta = """        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <button type="button" class="btn btn-secondary btn-sm" id="btnHeaderRdv" onclick="openRdvModalSprint1('reperage_mariage')"><svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg> Prendre RDV</button>
          <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openQuoteModalSprint1()">Devis École / Groupe</button>
          <button type="button" class="btn btn-primary btn-sm" onclick="navigateFamily('RES', 'RES-01')">Préparer ma visite & Billets</button>
        </div>"""
    if old_header_cta in html:
        html = html.replace(old_header_cta, new_header_cta, 1)

    # 3. Add "Prendre RDV" button in Hero CTA bar (#sec-PUB-01)
    old_hero_cta = """                <div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:28px;">
                  <button type="button" class="btn btn-primary" onclick="navigateFamily('RES', 'RES-03')">Simuler mon budget en FCFA & Réserver</button>
                  <button type="button" class="btn btn-secondary" onclick="inspectScreen('PUB-10')">Consulter tous les tarifs officiels</button>
                </div>"""
    new_hero_cta = """                <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px;">
                  <button type="button" class="btn btn-primary" onclick="navigateFamily('RES', 'RES-03')">Simuler mon budget en FCFA & Réserver</button>
                  <button type="button" class="btn btn-secondary btn-ochre-outline" onclick="openRdvModalSprint1('reperage_mariage')"><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg> Prendre RDV (Repérage / B2B / CFP)</button>
                  <button type="button" class="btn btn-secondary" onclick="inspectScreen('PUB-10')">Tarifs officiels</button>
                </div>"""
    if old_hero_cta in html:
        html = html.replace(old_hero_cta, new_hero_cta, 1)

    # 4. Add RDV buttons to Bento Card 5 (#sec-PUB-11) and Bento Card 6 (#sec-PUB-12)
    old_bento5_btn = """                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">
                  <button class="btn btn-primary btn-sm" onclick="openQuoteModalSprint1()">Demander un devis groupe<span class="tech-code-tag"> (RES-06)</span></button>
                  </div>"""
    new_bento5_btn = """                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">
                  <button class="btn btn-primary btn-sm" onclick="openQuoteModalSprint1()">Demander un devis groupe<span class="tech-code-tag"> (RES-06)</span></button>
                  <button class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openRdvModalSprint1('seminaire_b2b')">Planifier un RDV de repérage</button>
                  </div>"""
    if old_bento5_btn in html:
        html = html.replace(old_bento5_btn, new_bento5_btn, 1)

    old_bento6_btn = """                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">
                  <button class="btn btn-primary btn-sm" onclick="openCfpModalSprint1()">Déposer une candidature CFP</button>
                  </div>"""
    new_bento6_btn = """                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">
                  <button class="btn btn-primary btn-sm" onclick="openCfpModalSprint1()">Déposer une candidature CFP</button>
                  <button class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openRdvModalSprint1('orientation_cfp')">RDV Orientation &amp; Visite Campus</button>
                  </div>"""
    if old_bento6_btn in html:
        html = html.replace(old_bento6_btn, new_bento6_btn, 1)

    # 5. Inject full-width RDV section (#sec-PUB-18) right before #sec-PUB-14
    gallery_anchor = '              <!-- Galerie Photographique Immersive Pleine Largeur (PUB-14) -->'
    if 'id="sec-PUB-18"' not in html and gallery_anchor in html:
        html = html.replace(gallery_anchor, RDV_SECTION_HTML + "\n" + gallery_anchor, 1)

    # 6. Inject #modalRdvBox inside #modalOverlaySprint1 right after #modalCfpBox
    cfp_modal_end = """      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="submitCfpApplicationSprint1()">Valider mon dossier de candidature CFP</button>
      </div>
    </div>"""
    if 'id="modalRdvBox"' not in html and cfp_modal_end in html:
        html = html.replace(cfp_modal_end, cfp_modal_end + "\n" + RDV_MODAL_HTML, 1)

    # 7. Inject RDV JS engine before </script>
    if "function openRdvModalSprint1" not in html:
        html = html.replace("  </script>", RDV_JS + "\n  </script>", 1)

    path.write_text(html, encoding="utf-8")
    print(f"Updated {path} with Prise de RDV module ({len(html.splitlines())} lines)")


if __name__ == "__main__":
    for p in TARGETS:
        inject_rdv_module(p)
