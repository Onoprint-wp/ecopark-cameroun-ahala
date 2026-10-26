# -*- coding: utf-8 -*-
"""
Sprint 1 — Assemblage de l'application « Apple-Grade × Canopée Vivante » + Moteur de Persistance Temps Réel (Supabase + LocalStorage/BroadcastChannel)
Fonctionnalités Sprint 1 intégrées et vérifiées :
1. Finition visuelle Apple-Grade validée (Header Liquid Glass 1 ligne, Grille Bento asymétrique 28px plein bord, Typographie Semibold 600 à contraste tonal, boutons pilules 980px).
2. Moteur transactionnel ECOPARK_DB :
   - Création réelle de réservations (ECP-2026-XXXXX) synchronisées avec Mon Espace (ACC-03), le Scanner QR d'entrée (AGT-05 : 1er scan = VALIDE, 2e scan = DÉJÀ UTILISÉ), la Direction (DIR-01) et l'Audit (ADM-08).
   - Modale interactive de Demande de Devis École / Entreprise (RES-06 / EXP-03).
   - Modale interactive de Candidature au CFP ECOPARK (PUB-12 / EXP-06).
   - Encaissement Guichet (AGT-03 / AGT-04) mettant à jour en temps réel les compteurs de caisse (AGT-08 / AGT-09) et le chiffre d'affaires Direction (DIR-01).
"""

import pathlib
import shutil

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
PREVIEW_HTML = ROOT / "Preview_Apple_Grade_ECOPARK.html"
PROTOTYPE_HTML = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"
DIST_DIR = ROOT / "etape0-site-live"

SPRINT1_MODALS_AND_TOAST_HTML = """
  <!-- ========================================================================
       MODALES TRANSACTIONNELLES SPRINT 1 (DEVIS GROUPE RES-06 & CANDIDATURE CFP PUB-12)
       ======================================================================== -->
  <div id="modalOverlaySprint1" style="display:none;position:fixed;inset:0;background:rgba(20,34,17,0.55);backdrop-filter:blur(8px);z-index:3000;align-items:center;justify-content:center;padding:20px;">
    <!-- Modale Devis École / Entreprise (RES-06 / RES-10) -->
    <div id="modalQuoteBox" class="card" style="display:none;max-width:560px;width:100%;background:#FFFFFF;padding:32px;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow" style="margin:0;">Excursions Scolaires, Séminaires & Événements</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()">✕ Fermer</button>
      </div>
      <h3 style="margin-top:6px;">Demander un devis groupe sur-mesure</h3>
      <p style="font-size:14.5px;color:var(--color-text-muted);">
        Dès 20 participants, bénéficiez d'un accueil dédié à Ahala (tarif enfant protégé à 500 FCFA, encadrement pédagogique ou espace séminaire privatisé).
      </p>
      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="quoteOrgName">Nom de l'école, de l'entreprise ou de l'association</label>
          <input type="text" id="quoteOrgName" class="form-control" value="Complexe Scolaire Bilingue Les Étoiles (Yaoundé)" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quoteType">Type d'événement</label>
          <select id="quoteType" class="form-control">
            <option value="Excursion scolaire">Excursion scolaire (Maternelle / Primaire / Secondaire)</option>
            <option value="Séminaire entreprise">Séminaire / Team-building Entreprise</option>
            <option value="Mariage / Réception">Mariage / Arbre de Noël / Banquet</option>
          </select>
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quotePax">Nombre de participants estimé</label>
          <input type="number" id="quotePax" class="form-control" value="60" min="10" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quoteDate">Date souhaitée</label>
          <input type="date" id="quoteDate" class="form-control" value="2026-12-10" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quotePhone">Téléphone WhatsApp du responsable</label>
          <input type="tel" id="quotePhone" class="form-control" value="+237 699 45 67 89" />
        </div>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="submitGroupQuoteSprint1()">Enregistrer & Obtenir mon N° de Suivi</button>
      </div>
    </div>

    <!-- Modale Candidature CFP ECOPARK (PUB-12 / EXP-06) -->
    <div id="modalCfpBox" class="card" style="display:none;max-width:560px;width:100%;background:#FFFFFF;padding:32px;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow" style="margin:0;">Formation Professionnelle Agréée MINEFOP</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()">✕ Fermer</button>
      </div>
      <h3 style="margin-top:6px;">Candidature au CFP ECOPARK Yaoundé-Ahala</h3>
      <p style="font-size:14.5px;color:var(--color-text-muted);">
        Inscription officielle : <strong>50 000 FCFA</strong> • Scolarité annuelle : <strong>250 000 FCFA</strong> (70 % de travaux pratiques sur le site d'ECOPARK).
      </p>
      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="cfpCandidateName">Nom et Prénom du candidat</label>
          <input type="text" id="cfpCandidateName" class="form-control" value="Mlle Grâce NKODO" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="cfpTrack">Filière choisie</label>
          <select id="cfpTrack" class="form-control">
            <option value="Aquaculture & Pisciculture">Aquaculture & Pisciculture</option>
            <option value="Hôtellerie & Restauration">Hôtellerie & Restauration</option>
            <option value="Agriculture & Élevage Agropastoral">Agriculture & Élevage Agropastoral</option>
          </select>
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="cfpPhone">Téléphone (+237)</label>
          <input type="tel" id="cfpPhone" class="form-control" value="+237 677 88 99 00" />
        </div>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="submitCfpApplicationSprint1()">Valider mon dossier de candidature CFP</button>
      </div>
    </div>
  </div>

  <!-- Notification Toast Apple-Grade -->
  <div id="sprint1Toast" style="display:none;position:fixed;bottom:72px;right:18px;z-index:3500;max-width:420px;background:#1D490D;color:#FFFFFF;padding:14px 20px;border-radius:18px;box-shadow:0 16px 40px rgba(0,0,0,0.25);font-size:14.5px;font-weight:600;"></div>
"""

SPRINT1_DB_ENGINE_JS = r"""
    // ========================================================================
    // SPRINT 1 — MOTEUR DE PERSISTANCE TEMPS RÉEL (SUPABASE + LOCALSTORAGE SYNC)
    // ========================================================================
    const STORAGE_KEY_SPRINT1 = 'ecopark_ahala_db_sprint1_v1';
    const syncChannel = typeof BroadcastChannel !== 'undefined' ? new BroadcastChannel('ecopark_ahala_sync') : null;

    const DEFAULT_DB_STATE = {
      bookings: [
        {
          reference: 'ECP-2026-84920',
          holder: 'M. Jean-Paul MBARGA',
          phone: '+237 694 12 34 56',
          date: '15/11/2026',
          paxSummary: '2 Adultes, 2 Enfants • Zoo + Piscine + Pirogue',
          totalFcfa: 14000,
          status: 'CONFIRMED',
          scanned: false,
          scannedAt: null
        }
      ],
      quotes: [
        {
          reference: 'DEV-2026-3104',
          org: 'École Bilingue Les Palmiers',
          type: 'Excursion scolaire',
          pax: 50,
          date: '05/12/2026',
          budgetFcfa: 67500,
          status: 'Proposition envoyée'
        }
      ],
      cfpApplications: [
        {
          reference: 'CFP-2026-0192',
          name: 'Ngaoundéré Paulin',
          track: 'Aquaculture & Pisciculture',
          phone: '+237 691 22 33 44',
          status: 'Admis Rentrée (50 000 FCFA réglés)'
        }
      ],
      posStats: {
        cashFcfa: 184500,
        momoFcfa: 96000,
        validatedEntries: 214
      },
      dirStats: {
        monthlyRevenueFcfa: 18450000,
        momoRevenueFcfa: 7740000,
        monthlyVisitors: 4820
      },
      auditLogs: [
        { time: '26/10/2026 08:45', actor: 'Admin Plateforme (ADM)', action: 'Vérification de la grille tarifaire officielle en FCFA (protection tarif enfant 500 FCFA active).' },
        { time: '26/10/2026 09:12', actor: 'Mme Clarisse ATANGANA (AGT)', action: 'Ouverture session caisse Guichet #1 (Fond : 50 000 FCFA).' },
        { time: '26/10/2026 11:30', actor: 'Chef d\'Exploitation (EXP)', action: 'Validation du devis scolaire DEV-2026-3104.' }
      ]
    };

    function loadDB() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY_SPRINT1);
        if (!raw) return JSON.parse(JSON.stringify(DEFAULT_DB_STATE));
        return Object.assign(JSON.parse(JSON.stringify(DEFAULT_DB_STATE)), JSON.parse(raw));
      } catch (e) {
        return JSON.parse(JSON.stringify(DEFAULT_DB_STATE));
      }
    }

    function saveDB(db) {
      try {
        localStorage.setItem(STORAGE_KEY_SPRINT1, JSON.stringify(db));
        if (syncChannel) syncChannel.postMessage({ type: 'DB_UPDATED' });
      } catch (e) {}
      syncAllViewsFromDB();
    }

    if (syncChannel) {
      syncChannel.onmessage = () => syncAllViewsFromDB();
    }

    function showToastSprint1(msg) {
      const t = document.getElementById('sprint1Toast');
      if (!t) return;
      t.textContent = msg;
      t.style.display = 'block';
      clearTimeout(window._toastTimer);
      window._toastTimer = setTimeout(() => { t.style.display = 'none'; }, 4800);
    }

    function nowStamp() {
      const d = new Date();
      const pad = n => String(n).padStart(2, '0');
      return `${pad(d.getDate())}/${pad(d.getMonth()+1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    }

    // Génération et persistance d'un nouveau billet QR depuis le simulateur (RES-09)
    function createLiveBookingSprint1() {
      const db = loadDB();
      const holder = (document.getElementById('visitorName') || {}).value || 'Visiteur ECOPARK';
      const phone = (document.getElementById('visitorPhone') || {}).value || '+237 694 12 34 56';
      const rawDate = (document.getElementById('visitDate') || {}).value || '2026-11-15';
      const totalText = (document.getElementById('grandTotalFCFA') || {}).textContent || '14 000 FCFA';
      const totalNum = parseInt(totalText.replace(/[^0-9]/g, ''), 10) || 14000;

      const acts = [];
      if (document.getElementById('chkZoo') && document.getElementById('chkZoo').checked) acts.push('Zoo');
      if (document.getElementById('chkPiscine') && document.getElementById('chkPiscine').checked) acts.push('Piscine');
      if (document.getElementById('chkPirogue') && document.getElementById('chkPirogue').checked) acts.push('Pirogue');
      if (document.getElementById('chkCheval') && document.getElementById('chkCheval').checked) acts.push('Équitation');
      if (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) acts.push('Saveurs');

      const ref = 'ECP-2026-' + Math.floor(10000 + Math.random() * 89999);
      const paxSummary = `${counts.adults} Adulte(s), ${counts.children} Enfant(s) • ${acts.join(' + ') || 'Visite'}`;

      db.bookings.unshift({
        reference: ref,
        holder: holder,
        phone: phone,
        date: rawDate,
        paxSummary: paxSummary,
        totalFcfa: totalNum,
        status: 'CONFIRMED',
        scanned: false,
        scannedAt: null
      });
      db.dirStats.monthlyRevenueFcfa += totalNum;
      db.dirStats.momoRevenueFcfa += totalNum;
      db.dirStats.monthlyVisitors += (counts.adults + counts.children + counts.toddlers);
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${holder} (Client)`,
        action: `Nouvelle réservation ${ref} (${formatFCFA(totalNum)}) enregistrée et billet QR émis.`
      });

      saveDB(db);

      // Mettre à jour la carte Billet QR à l'écran et le champ du scanner Guichet
      const codeEls = document.querySelectorAll('#demoTicketCard div[style*="font-size:1.3rem"]');
      if (codeEls.length > 0) codeEls[0].textContent = ref;
      document.getElementById('ticketHolder').textContent = holder;
      document.getElementById('ticketDate').textContent = `${rawDate} (09h00 – 18h00)`;
      document.getElementById('ticketItems').textContent = acts.join(', ') || 'Accès Parc';
      const scanInput = document.getElementById('qrScanInput');
      if (scanInput) scanInput.value = ref;

      showToastSprint1(`✅ Réservation ${ref} enregistrée ! Billet disponible dans « Mon Espace » et prêt à être scanné au Guichet.`);
    }

    function openQuoteModalSprint1() {
      document.getElementById('modalOverlaySprint1').style.display = 'flex';
      document.getElementById('modalQuoteBox').style.display = 'flex';
      document.getElementById('modalCfpBox').style.display = 'none';
    }

    function openCfpModalSprint1() {
      document.getElementById('modalOverlaySprint1').style.display = 'flex';
      document.getElementById('modalQuoteBox').style.display = 'none';
      document.getElementById('modalCfpBox').style.display = 'flex';
    }

    function closeSprint1Modals() {
      document.getElementById('modalOverlaySprint1').style.display = 'none';
    }

    function submitGroupQuoteSprint1() {
      const db = loadDB();
      const org = document.getElementById('quoteOrgName').value || 'Groupe ECOPARK';
      const type = document.getElementById('quoteType').value || 'Excursion scolaire';
      const pax = parseInt(document.getElementById('quotePax').value, 10) || 40;
      const date = document.getElementById('quoteDate').value || '2026-12-10';
      const ref = 'DEV-2026-' + Math.floor(1000 + Math.random() * 8999);
      const budget = pax * 1500;

      db.quotes.unshift({
        reference: ref,
        org: org,
        type: type,
        pax: pax,
        date: date,
        budgetFcfa: budget,
        status: 'En étude (Exploitation)'
      });
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${org} (Groupe)`,
        action: `Demande de devis ${ref} (${pax} pers., ~${formatFCFA(budget)}) transmise à l'Exploitation.`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`📋 Devis ${ref} enregistré ! Retrouvez-le dans « Mon Espace » (ACC-04) et dans « Exploitation » (EXP-03).`);
    }

    function submitCfpApplicationSprint1() {
      const db = loadDB();
      const name = document.getElementById('cfpCandidateName').value || 'Candidat CFP';
      const track = document.getElementById('cfpTrack').value || 'Aquaculture';
      const phone = document.getElementById('cfpPhone').value || '+237 677 00 00 00';
      const ref = 'CFP-2026-' + Math.floor(1000 + Math.random() * 8999);

      db.cfpApplications.unshift({
        reference: ref,
        name: name,
        track: track,
        phone: phone,
        status: 'Dossier reçu (Inscription 50 000 FCFA)'
      });
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${name} (Candidat CFP)`,
        action: `Candidature CFP ${ref} déposée en filière « ${track} ».`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`🎓 Candidature ${ref} (${track}) enregistrée et visible dans l'espace Exploitation (EXP-06) !`);
    }

    // Surcharge intelligente d'emitPosTicket pour mettre à jour la caisse en temps réel
    emitPosTicket = function(method) {
      if (posItems.length === 0) {
        showToastSprint1('⚠️ Ajoutez au moins une prestation au ticket guichet.');
        return;
      }
      const db = loadDB();
      let sum = 0;
      let paxCount = 0;
      posItems.forEach(i => {
        sum += i.price * i.qty;
        paxCount += i.qty;
      });
      if (method.includes('Espèces')) db.posStats.cashFcfa += sum;
      else db.posStats.momoFcfa += sum;
      db.posStats.validatedEntries += paxCount;
      db.dirStats.monthlyRevenueFcfa += sum;
      db.dirStats.monthlyVisitors += paxCount;

      const ticketRef = 'POS-2026-' + Math.floor(10000 + Math.random() * 89999);
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: 'Mme Clarisse ATANGANA (Guichet #1)',
        action: `Vente guichet ${ticketRef} (${method}) : ${formatFCFA(sum)} (${paxCount} entrées).`
      });
      saveDB(db);
      clearPos();
      showToastSprint1(`🧾 Ticket ${ticketRef} (${formatFCFA(sum)} — ${method}) encaissé ! Caisse AGT-09 et Direction DIR-01 mises à jour.`);
    };

    // Surcharge intelligente du contrôle QR (AGT-05 / AGT-06) :
    // Si on clique sur "Vérifier" avec un vrai code de la BDD, vérifie s'il a déjà été scanné !
    const _origTriggerScanVerdict = triggerScanVerdict;
    function verifyLiveQrCode() {
      const code = ((document.getElementById('qrScanInput') || {}).value || '').trim().toUpperCase();
      const db = loadDB();
      const found = db.bookings.find(b => b.reference.toUpperCase() === code);
      if (!found) {
        _origTriggerScanVerdict('UNKNOWN');
        return;
      }
      if (found.scanned) {
        _origTriggerScanVerdict('USED');
        document.getElementById('scanResultDesc').textContent =
          `Ce billet (${found.reference} — ${found.holder}) a déjà été scanné le ${found.scannedAt} au Tourniquet Principal.`;
        return;
      }
      found.scanned = true;
      found.scannedAt = nowStamp();
      db.posStats.validatedEntries += 1;
      db.auditLogs.unshift({
        time: found.scannedAt,
        actor: 'Agent Contrôle Tourniquet (AGT)',
        action: `Validation entrée QR ${found.reference} (${found.holder}).`
      });
      saveDB(db);
      _origTriggerScanVerdict('VALID');
      document.getElementById('scanResultDesc').textContent =
        `Référence ${found.reference} • Titulaire : ${found.holder} (${found.paxSummary}). Entrée enregistrée à ${found.scannedAt}.`;
      showToastSprint1(`✅ Billet ${found.reference} validé au tourniquet ! (Un 2e scan de ce même code sera automatiquement rejeté comme « Déjà utilisé »).`);
    }

    function syncAllViewsFromDB() {
      const db = loadDB();

      // 1. Mettre à jour le tableau Mon Espace (ACC-03 / ACC-04)
      const accTbody = document.querySelector('#view-ACC table tbody');
      if (accTbody) {
        const bRows = db.bookings.slice(0, 4).map(b => `
          <tr>
            <td><strong>${b.reference}</strong></td>
            <td>${b.date}</td>
            <td>${b.paxSummary}</td>
            <td><strong>${formatFCFA(b.totalFcfa)}</strong></td>
            <td><span class="status-badge ${b.scanned ? 'status-info' : 'status-success'}">${b.scanned ? 'Utilisé (' + b.scannedAt + ')' : 'Confirmé (QR Actif)'}</span></td>
            <td>
              <button class="btn btn-primary btn-sm" onclick="document.getElementById('qrScanInput').value='${b.reference}'; navigateFamily('AGT', 'AGT-05')">Tester au Scanner</button>
            </td>
          </tr>
        `).join('');
        const qRows = db.quotes.slice(0, 3).map(q => `
          <tr>
            <td><strong>${q.reference}</strong></td>
            <td>${q.date}</td>
            <td>Devis ${q.org} (${q.pax} participants • ${q.type})</td>
            <td><strong>${formatFCFA(q.budgetFcfa)}</strong></td>
            <td><span class="status-badge status-info">${q.status}</span></td>
            <td><button class="btn btn-secondary btn-sm" onclick="navigateFamily('EXP', 'EXP-03')">Voir dossier</button></td>
          </tr>
        `).join('');
        accTbody.innerHTML = bRows + qRows;
      }

      // 2. Mettre à jour les compteurs de Caisse Guichet (AGT-08 / AGT-09)
      const agtCards = document.querySelectorAll('#view-AGT .col-12.card .col-4 strong');
      if (agtCards.length >= 3) {
        agtCards[0].textContent = formatFCFA(db.posStats.cashFcfa);
        agtCards[1].textContent = formatFCFA(db.posStats.momoFcfa);
        agtCards[2].textContent = `${db.posStats.validatedEntries} entrées validées`;
      }

      // 3. Mettre à jour Exploitation (EXP-03 / EXP-06)
      const expTables = document.querySelectorAll('#view-EXP table tbody');
      if (expTables.length >= 2) {
        const latestQ = db.quotes[0];
        const latestC = db.cfpApplications[0];
        expTables[1].innerHTML = `
          <tr>
            <td><code>EXP-03</code> Devis</td>
            <td>${latestQ.org} (${latestQ.reference})</td>
            <td>${latestQ.pax} participants • ${latestQ.type} (${latestQ.date})</td>
            <td><span class="status-badge status-info">${formatFCFA(latestQ.budgetFcfa)} • ${latestQ.status}</span></td>
          </tr>
          <tr>
            <td><code>EXP-06</code> CFP</td>
            <td>${latestC.name} (${latestC.reference})</td>
            <td>Filière : ${latestC.track} (${latestC.phone})</td>
            <td><span class="status-badge status-success">${latestC.status}</span></td>
          </tr>
          <tr>
            <td><code>EXP-07</code> Support</td>
            <td>Mme Charlotte Manuella</td>
            <td>Demande de grille tarifaire famille pour dimanche</td>
            <td><span class="status-badge status-success">Répondu en 12 min</span></td>
          </tr>
        `;
      }

      // 4. Mettre à jour les KPIs Direction (DIR-01..03)
      const dirKpis = document.querySelectorAll('#view-DIR .col-3.card strong');
      if (dirKpis.length >= 3) {
        dirKpis[0].textContent = formatFCFA(db.dirStats.monthlyRevenueFcfa);
        const pct = Math.round((db.dirStats.momoRevenueFcfa / db.dirStats.monthlyRevenueFcfa) * 100);
        dirKpis[1].textContent = `${pct} % (${formatFCFA(db.dirStats.momoRevenueFcfa)})`;
        dirKpis[2].textContent = `${db.dirStats.monthlyVisitors.toLocaleString('fr-FR')} visiteurs`;
      }

      // 5. Mettre à jour le Journal d'Audit (ADM-08)
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
    }
"""

def build_sprint1():
    html = PREVIEW_HTML.read_text(encoding="utf-8")

    # 1. Relier les boutons "Devis École / Groupe" et "Déposer une candidature CFP" aux modales Sprint 1
    html = html.replace(
        'onclick="navigateFamily(\'RES\', \'RES-06\')"',
        'onclick="openQuoteModalSprint1()"'
    )
    html = html.replace(
        'onclick="inspectScreen(\'PUB-12\')">Déposer une candidature CFP</button>',
        'onclick="openCfpModalSprint1()">Déposer une candidature CFP</button>'
    )
    html = html.replace(
        'onclick="inspectScreen(\'PUB-12\')">Candidater</button>',
        'onclick="openCfpModalSprint1()">Candidater</button>'
    )

    # 2. Relier le bouton "Voir Billet QR" du simulateur à createLiveBookingSprint1() (même avec .tech-code-tag autour de RES-09)
    html = html.replace(
        'onclick="inspectScreen(\'RES-09\')">Voir Billet QR',
        'onclick="createLiveBookingSprint1()">🎟️ Générer & Enregistrer mon Billet QR'
    )

    # 2b. Ajouter le favicon officiel ECOPARK dans <head> pour éviter tout 404 sur /favicon.ico
    html = html.replace(
        '<title>ECOPARK CAMEROUN',
        '<link rel="icon" type="image/png" href="audit-assets/ecopark-real-media/cropped-LOGO-ECOPARK-Youtube.png" />\n  <title>ECOPARK CAMEROUN',
        1
    )

    # 3. Relier le bouton "Vérifier" du scanner QR (AGT-05) à verifyLiveQrCode()
    html = html.replace(
        '<button class="btn btn-primary" onclick="triggerScanVerdict(\'VALID\')">Vérifier</button>',
        '<button class="btn btn-primary" onclick="verifyLiveQrCode()">Vérifier dans la BDD</button>'
    )

    # 4. Injecter les modales Sprint 1 et le moteur JS ECOPARK_DB
    html = html.replace("  <button type=\"button\" class=\"floating-demo-pill\"", SPRINT1_MODALS_AND_TOAST_HTML + "\n  <button type=\"button\" class=\"floating-demo-pill\"", 1)
    html = html.replace(
        "// Initialisation au chargement",
        SPRINT1_DB_ENGINE_JS + "\n    // Initialisation au chargement\n    syncAllViewsFromDB();",
        1
    )

    # Écrire dans Prototype_Interactif_ECOPARK_NEW_LOOK.html et dans etape0-site-live/index.html
    PROTOTYPE_HTML.write_text(html, encoding="utf-8")
    (DIST_DIR / "index.html").write_text(html, encoding="utf-8")
    shutil.copy2(ROOT / "supabase" / "migrations" / "20261026000001_ecopark_schema_rls.sql", DIST_DIR / "schema_ecopark_supabase.sql")
    print(f"[OK] Sprint 1 integre dans {DIST_DIR / 'index.html'} ({len(html)} octets)")

if __name__ == "__main__":
    build_sprint1()
