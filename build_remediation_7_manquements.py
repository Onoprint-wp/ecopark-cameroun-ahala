# -*- coding: utf-8 -*-
"""
Script d'intégration des 7 remédiations ("Manquements Obligatoire vs Facultatif") :
1. Modale CFP (#modalCfpBox) : 5 filières MINEFOP + Champ Âge (>= 16 ans obligatoire) + Sélecteur d'échéancier (4 tranches vs intégral) + Bouton WhatsApp CFP.
2. Vue WhatsApp Interactive (#whatsappConciergeCard & EXP-07) : Synchronisation intégrale des nouvelles options (3 Cités Hôtelières, Nuitées, Navette A/R, Pêche Ludique).
3. Sélecteur des 3 Cités Hôtelières (Ewondo 25k, Chanthel 15k, Bene 10k) + Nombre de nuitées (1 à 3 nuits) dans le simulateur (RES-03).
4. Calculateur réaliste de Devis B2B / Écoles / Mariages (#modalQuoteBox) avec différenciation tarifaire, options Salle Menkii Essomba Anton & Navette 18/32 places, et Aperçu Proforma Officielle en direct (#quoteProformaPreview).
5. Ajout des options Navette Climatisée A/R Yaoundé (#chkBumpNavette) et Pêche Ludique / Musée & Forêt (#chkBumpPeche) dans le simulateur (RES-03).
6. Sélecteur Tarif Piscine Semaine/Prévente Enfant (1 500 FCFA) vs Tarif Guichet Week-end & Jours Fériés (2 500 FCFA) (#poolRatePeriod dans RES-01/02).
7. Validation stricte des champs obligatoires (attributs required, format téléphone Cameroun +237, âge CFP >= 16 ans).

Respect strict des invariants :
- Zéro caractère Unicode > 0x25FF (aucun emoji OS)
- Odomètre initial = 14 000 FCFA, +1 adulte = 18 500 FCFA
- 12 Stagger clips intacts
- Aucune fuite de code technique hors .tech-code-tag
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "etape0-site-live" / "index.html"
PROTO_PATH = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"


def apply_remediations():
    raw_bytes = INDEX_PATH.read_bytes()
    has_crlf = b"\r\n" in raw_bytes
    text = raw_bytes.decode("utf-8").replace("\r\n", "\n")

    # -------------------------------------------------------------------------
    # 1. RES-01 / RES-02 : Sélecteur Tarif Piscine Semaine/Prévente (1 500 F)
    #    vs Week-end/Jours Fériés (2 500 F) + attribut required sur visitDate
    # -------------------------------------------------------------------------
    old_step1 = """                <div class="grid-12" style="gap:16px;">
                  <div class="col-6 form-group">
                    <label class="form-label" for="visitDate">Date de visite souhaitée</label>
                    <input type="date" id="visitDate" class="form-control" value="2026-11-15" />
                  </div>
                  <div class="col-6 form-group">
                    <label class="form-label" for="visitProfile">Profil de sortie</label>
                    <select id="visitProfile" class="form-control" onchange="recalcSimulator()">
                      <option value="famille">Famille &amp; Enfants (Prendre le frais le week-end)</option>
                      <option value="amis">Couple / Groupe d'amis / Grande Réunion</option>
                      <option value="ecole">Excursion scolaire (Devis conseillé)</option>
                      <option value="entreprise">Séminaire Ministère / ONG / Entreprise (Salle Menkii Essomba Anton)</option>
                    </select>
                  </div>
                </div>"""

    new_step1 = """                <div class="grid-12" style="gap:16px;">
                  <div class="col-4 form-group">
                    <label class="form-label" for="visitDate">Date de visite souhaitée <span style="color:#B42318;">*</span></label>
                    <input type="date" id="visitDate" class="form-control" value="2026-11-15" required />
                  </div>
                  <div class="col-4 form-group">
                    <label class="form-label" for="visitProfile">Profil de sortie</label>
                    <select id="visitProfile" class="form-control" onchange="recalcSimulator()">
                      <option value="famille">Famille &amp; Enfants (Prendre le frais le week-end)</option>
                      <option value="amis">Couple / Groupe d'amis / Grande Réunion</option>
                      <option value="ecole">Excursion scolaire (Devis conseillé)</option>
                      <option value="entreprise">Séminaire Ministère / ONG / Entreprise (Salle Menkii Essomba Anton)</option>
                    </select>
                  </div>
                  <div class="col-4 form-group">
                    <label class="form-label" for="poolRatePeriod">Période Tarifaire Piscine</label>
                    <select id="poolRatePeriod" class="form-control" onchange="recalcSimulator()">
                      <option value="SEMAINE_PROMO" selected>Prévente En Ligne / Semaine (Enfant 1 500 FCFA)</option>
                      <option value="WEEKEND_PLEIN">Guichet Week-end &amp; Fériés (Enfant 2 500 FCFA)</option>
                    </select>
                  </div>
                </div>"""

    assert old_step1 in text, "old_step1 introuvable"
    text = text.replace(old_step1, new_step1, 1)

    # Mettre un span dynamique sur le libellé Piscine pour refléter 1 500 vs 2 500 FCFA
    old_piscine_lbl = """                      <input type="checkbox" id="chkPiscine" checked onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Accès Piscine Semi-Olympique</strong> (Enfant : 1 500 FCFA • Adulte : 2 500 FCFA)"""
    new_piscine_lbl = """                      <input type="checkbox" id="chkPiscine" checked onchange="onManualActivityToggle()" />
                      <strong style="margin-left:8px;">Accès Piscine Semi-Olympique</strong> <span id="lblPiscineRateInfo">(Enfant : 1 500 FCFA • Adulte : 2 500 FCFA)</span>"""
    assert old_piscine_lbl in text, "old_piscine_lbl introuvable"
    text = text.replace(old_piscine_lbl, new_piscine_lbl, 1)

    # -------------------------------------------------------------------------
    # 2. RES-03 ORDER BUMPS : 3 Cités Hôtelières (Ewondo, Chanthel, Bene) +
    #    Nombre de nuitées (1 à 3) + Navette A/R Yaoundé + Pêche Ludique
    # -------------------------------------------------------------------------
    old_order_bumps = """                    <label style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                      <span style="font-size:14px;">
                        <input type="checkbox" id="chkBumpLodgeEwondo" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Suite VIP Cité Ewondo Climatisée</strong> (+25 000 FCFA • <span id="simEwondoRemainingText">2 suites disponibles</span>)
                      </span>
                      <span class="price-pill" id="subBumpLodge">0 FCFA</span>
                    </label>
                  </div>
                </div>"""

    new_order_bumps = """                    <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;gap:8px;flex-wrap:wrap;">
                      <label style="font-size:14px;cursor:pointer;display:inline-flex;align-items:center;">
                        <input type="checkbox" id="chkBumpLodgeEwondo" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Hébergement Cités Hôtelières</strong>
                        <span style="font-size:12px;color:var(--color-text-muted);margin-left:6px;">(<span id="simEwondoRemainingText">2 suites disponibles</span>)</span>
                      </label>
                      <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                        <select id="lodgeCitySelect" class="form-control" style="min-height:32px;padding:2px 8px;font-size:12.5px;width:auto;" aria-label="Choix de la Cité Hôtelière" onchange="document.getElementById('chkBumpLodgeEwondo').checked=true; recalcSimulator()">
                          <option value="EWONDO" selected>Cité Ewondo VIP (25 000 FCFA/nuit)</option>
                          <option value="CHANTHEL">Cité Chanthel Confort (15 000 FCFA/nuit)</option>
                          <option value="BENE">Cité Bene Standard (10 000 FCFA/nuit)</option>
                        </select>
                        <select id="lodgeNightsSelect" class="form-control" style="min-height:32px;padding:2px 8px;font-size:12.5px;width:auto;" aria-label="Nombre de nuitées" onchange="document.getElementById('chkBumpLodgeEwondo').checked=true; recalcSimulator()">
                          <option value="1" selected>1 nuit / Jour</option>
                          <option value="2">2 nuitées</option>
                          <option value="3">3 nuitées</option>
                        </select>
                        <span class="price-pill" id="subBumpLodge">0 FCFA</span>
                      </div>
                    </div>
                    <label style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                      <span style="font-size:14px;">
                        <input type="checkbox" id="chkBumpNavette" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Navette Climatisée A/R Yaoundé — Ahala</strong> (Adulte : 1 500 FCFA • Enfant : 1 000 FCFA)
                      </span>
                      <span class="price-pill" id="subBumpNavette">0 FCFA</span>
                    </label>
                    <label style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#FFFFFF;border:1px solid var(--color-border);border-radius:8px;cursor:pointer;">
                      <span style="font-size:14px;">
                        <input type="checkbox" id="chkBumpPeche" onchange="recalcSimulator()" />
                        <strong style="margin-left:6px;">Pêche Ludique aux Étangs &amp; Visite Guidée Musée / Forêt</strong> (+2 000 FCFA forfait)
                      </span>
                      <span class="price-pill" id="subBumpPeche">0 FCFA</span>
                    </label>
                  </div>
                </div>"""

    assert old_order_bumps in text, "old_order_bumps introuvable"
    text = text.replace(old_order_bumps, new_order_bumps, 1)

    # -------------------------------------------------------------------------
    # 3. RES-05 : Attributs required et indicateurs obligatoires sur Coordonnées
    # -------------------------------------------------------------------------
    old_coords = """                  <div class="col-6 form-group">
                    <label class="form-label" for="visitorName">Nom et Prénom (ou Établissement)</label>
                    <input type="text" id="visitorName" class="form-control" value="M. Jean-Paul MBARGA" />
                  </div>
                  <div class="col-6 form-group">
                    <label class="form-label" for="visitorPhone">Téléphone Cameroun (WhatsApp / Mobile Money)</label>
                    <input type="tel" id="visitorPhone" class="form-control" value="+237 694 12 34 56" />
                  </div>"""

    new_coords = """                  <div class="col-6 form-group">
                    <label class="form-label" for="visitorName">Nom et Prénom (ou Établissement) <span style="color:#B42318;">*</span></label>
                    <input type="text" id="visitorName" class="form-control" value="M. Jean-Paul MBARGA" required />
                  </div>
                  <div class="col-6 form-group">
                    <label class="form-label" for="visitorPhone">Téléphone Cameroun (+237 WhatsApp / MoMo) <span style="color:#B42318;">*</span></label>
                    <input type="tel" id="visitorPhone" class="form-control" value="+237 694 12 34 56" pattern="^\\+?237[0-9\\s]{8,13}$" required />
                  </div>"""

    assert old_coords in text, "old_coords introuvable"
    text = text.replace(old_coords, new_coords, 1)

    # -------------------------------------------------------------------------
    # 4. MODALE DEVIS (#modalQuoteBox) & MODALE CFP (#modalCfpBox)
    # -------------------------------------------------------------------------
    old_modals = """      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="quoteOrgName">Nom de l'école, de l'entreprise ou de l'association</label>
          <input type="text" id="quoteOrgName" class="form-control" value="Complexe Scolaire Bilingue Les Étoiles (Yaoundé)" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quoteType">Type d'événement</label>
          <select id="quoteType" class="form-control">
            <option value="Excursion scolaire">Excursion scolaire (Maternelle / Primaire / Secondaire)</option>
            <option value="Séminaire Ministère / ONG / Entreprise">Séminaire Ministère / ONG / Entreprise (Salle Menkii Essomba Anton)</option>
            <option value="Grande Réunion / Mariage / Réception">Grande Réunion d'Association / Mariage / Arbre de Noël</option>
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
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="submitGroupQuoteSprint1()">Enregistrer &amp; Obtenir mon N° de Suivi</button>
        <button type="button" class="btn btn-secondary btn-ochre-outline" style="flex:1;" onclick="sendWhatsAppQuoteSprint1()"><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> Envoyer sur WhatsApp (+237 697 13 62 03)</button>
      </div>
    </div>

    <!-- Modale Candidature CFP ECOPARK (PUB-12 / EXP-06) -->
    <div id="modalCfpBox" class="card" style="display:none;max-width:560px;width:100%;background:#FFFFFF;padding:32px;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow" style="margin:0;">Formation Professionnelle Agréée MINEFOP</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()"><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg> Fermer</button>
      </div>
      <h3 style="margin-top:6px;">Candidature au CFP ECOPARK Yaoundé-Ahala</h3>
      <p style="font-size:14.5px;color:var(--color-text-muted);">
        Accessible dès 16 ans • Inscription : <strong>50 000 FCFA</strong> • Scolarité : <strong>250 000 FCFA (payable en 4 tranches)</strong> • Diplômes délivrés : <strong>DQP, CQP et Attestation reconnue par l'État</strong> avec stage pratique garanti au sein même d'ECOPARK.
      </p>
      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="cfpCandidateName">Nom et Prénom du candidat</label>
          <input type="text" id="cfpCandidateName" class="form-control" value="Mlle Grâce NKODO" />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="cfpTrack">Filière choisie</label>
          <select id="cfpTrack" class="form-control">
            <option value="Hôtellerie">1. Hôtellerie (Stage Hôtels Ewondo, Chanthel &amp; Bene)</option>
            <option value="Restauration">2. Restauration (Stage Le Château des Saveurs)</option>
            <option value="Décoration">3. Décoration (Événementiel &amp; Espaces de réception)</option>
            <option value="Agropastorale">4. Agropastorale (Cuniculture, Aviculture, Apiculture, Porciculture)</option>
            <option value="Pisciculture">5. Pisciculture &amp; Aquaculture (Bassins d'Ahala)</option>
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
    </div>"""

    new_modals = """      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="quoteOrgName">Nom de l'école, de l'entreprise ou de l'association <span style="color:#B42318;">*</span></label>
          <input type="text" id="quoteOrgName" class="form-control" value="Complexe Scolaire Bilingue Les Étoiles (Yaoundé)" oninput="recalcQuoteProformaPreview()" required />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quoteType">Type d'événement</label>
          <select id="quoteType" class="form-control" onchange="recalcQuoteProformaPreview()">
            <option value="Excursion scolaire">Excursion scolaire (Forfait protégé : 1 500 FCFA / élève)</option>
            <option value="Séminaire Ministère / ONG / Entreprise">Séminaire Ministère / ONG / Entreprise (12 500 FCFA / pers.)</option>
            <option value="Grande Réunion / Mariage / Réception">Grande Réunion / Mariage / Gala (15 000 FCFA / invité)</option>
          </select>
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quotePax">Nombre de participants estimé <span style="color:#B42318;">*</span></label>
          <input type="number" id="quotePax" class="form-control" value="60" min="10" oninput="recalcQuoteProformaPreview()" required />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quoteDate">Date souhaitée <span style="color:#B42318;">*</span></label>
          <input type="date" id="quoteDate" class="form-control" value="2026-12-10" onchange="recalcQuoteProformaPreview()" required />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="quotePhone">Téléphone WhatsApp du responsable <span style="color:#B42318;">*</span></label>
          <input type="tel" id="quotePhone" class="form-control" value="+237 699 45 67 89" required />
        </div>
        <div class="col-12" style="display:grid;gap:6px;margin-top:4px;">
          <label style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;background:var(--color-surface-soft);border:1px solid var(--color-border);border-radius:8px;font-size:13.5px;cursor:pointer;">
            <span>
              <input type="checkbox" id="quoteOptHall" onchange="recalcQuoteProformaPreview()" />
              <strong style="margin-left:6px;">Privatisation Salle Polyvalente « Menkii Essomba Anton » &amp; Sonorisation</strong> (Inclus en Séminaire/Mariage • +75 000 FCFA en option)
            </span>
          </label>
          <label style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;background:var(--color-surface-soft);border:1px solid var(--color-border);border-radius:8px;font-size:13.5px;cursor:pointer;">
            <span>
              <input type="checkbox" id="quoteOptShuttle" onchange="recalcQuoteProformaPreview()" />
              <strong style="margin-left:6px;">Location Navette Climatisée A/R Yaoundé (Bus 18 ou 32 places)</strong> (+45 000 FCFA forfait rotation)
            </span>
          </label>
        </div>
        <div class="col-12" id="quoteProformaPreview" style="padding:12px;background:#FBF5EC;border:1px solid rgba(196,125,43,0.4);border-radius:10px;font-size:13.5px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <strong style="color:var(--color-brand-deep);">Aperçu Facture Proforma Officielle (Simulation temps réel)</strong>
            <span class="price-pill" id="quoteProformaTotalText" style="font-size:14px;">90 000 FCFA</span>
          </div>
          <div id="quoteProformaBreakdownText" style="color:var(--color-text-muted);font-size:12.8px;">
            60 participants × 1 500 FCFA (Tarif entrée enfant protégé 500 FCFA + Piscine/Pirogue encadrée).
          </div>
        </div>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="submitGroupQuoteSprint1()">Enregistrer &amp; Obtenir mon N° de Suivi</button>
        <button type="button" class="btn btn-secondary btn-ochre-outline" style="flex:1;" onclick="sendWhatsAppQuoteSprint1()"><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> Envoyer Proforma sur WhatsApp (+237 697 13 62 03)</button>
      </div>
    </div>

    <!-- Modale Candidature CFP ECOPARK (PUB-12 / EXP-06) -->
    <div id="modalCfpBox" class="card" style="display:none;max-width:580px;width:100%;background:#FFFFFF;padding:32px;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="eyebrow" style="margin:0;">Formation Professionnelle Agréée MINEFOP</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeSprint1Modals()"><svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg> Fermer</button>
      </div>
      <h3 style="margin-top:6px;">Candidature au CFP ECOPARK Yaoundé-Ahala</h3>
      <p style="font-size:14.5px;color:var(--color-text-muted);">
        Accessible dès 16 ans • Inscription : <strong>50 000 FCFA</strong> • Scolarité : <strong>250 000 FCFA (payable en 4 tranches)</strong> • Diplômes délivrés : <strong>DQP, CQP et Attestation reconnue par l'État</strong> avec stage pratique garanti au sein même d'ECOPARK.
      </p>
      <div class="grid-12" style="gap:12px;margin-top:8px;">
        <div class="col-8 form-group" style="margin:0;">
          <label class="form-label" for="cfpCandidateName">Nom et Prénom du candidat <span style="color:#B42318;">*</span></label>
          <input type="text" id="cfpCandidateName" class="form-control" value="Mlle Grâce NKODO" required />
        </div>
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="cfpAge">Âge (Min. 16 ans) <span style="color:#B42318;">*</span></label>
          <input type="number" id="cfpAge" class="form-control" value="19" min="16" max="65" required />
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="cfpTrack">Filière officielle MINEFOP (5 filières)</label>
          <select id="cfpTrack" class="form-control">
            <option value="Hôtellerie">1. Hôtellerie (Stage Hôtels Ewondo, Chanthel &amp; Bene)</option>
            <option value="Restauration">2. Restauration (Stage Le Château des Saveurs)</option>
            <option value="Décoration">3. Décoration (Événementiel &amp; Espaces de réception)</option>
            <option value="Agropastorale">4. Agropastorale (Cuniculture, Aviculture, Apiculture, Porciculture)</option>
            <option value="Pisciculture">5. Pisciculture &amp; Aquaculture (Bassins d'Ahala)</option>
          </select>
        </div>
        <div class="col-6 form-group" style="margin:0;">
          <label class="form-label" for="cfpPhone">Téléphone (+237) <span style="color:#B42318;">*</span></label>
          <input type="tel" id="cfpPhone" class="form-control" value="+237 677 88 99 00" required />
        </div>
        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="cfpPaymentPlan">Modalité de règlement de la scolarité (Inscription : 50 000 FCFA)</label>
          <select id="cfpPaymentPlan" class="form-control">
            <option value="Échéancier 4 tranches (100k + 3x50k FCFA)" selected>Échéancier 4 tranches : 100 000 FCFA + 3 × 50 000 FCFA (Total Scolarité : 250 000 FCFA)</option>
            <option value="Paiement intégral (300 000 FCFA)">Paiement intégral à l'inscription : 50 000 FCFA + 250 000 FCFA (300 000 FCFA)</option>
          </select>
        </div>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;">
        <button type="button" class="btn btn-primary" style="flex:1;" onclick="submitCfpApplicationSprint1()">Valider mon dossier de candidature CFP</button>
        <button type="button" class="btn btn-secondary btn-ochre-outline" style="flex:1;" onclick="sendWhatsAppCfpSprint1()"><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> Envoyer dossier CFP sur WhatsApp</button>
      </div>
    </div>"""

    assert old_modals in text, "old_modals introuvable"
    text = text.replace(old_modals, new_modals, 1)

    # -------------------------------------------------------------------------
    # 5. MISE À JOUR DE applySalesBundle & recalcSimulator
    # -------------------------------------------------------------------------
    old_recalc_block = """      } else if (bundleCode === 'PACK_COUPLE_EWONDO') {
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

    function recalcSimulator() {
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
      if (bundleDiscount > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:var(--color-brand-deep);font-weight:700;"><span>${bundleLabel}</span><strong>-${formatFCFA(bundleDiscount)}</strong></div>`);"""

    new_recalc_block = """      } else if (bundleCode === 'PACK_COUPLE_EWONDO') {
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
        const citySel = document.getElementById('lodgeCitySelect');
        const nightsSel = document.getElementById('lodgeNightsSelect');
        if (citySel) citySel.value = 'EWONDO';
        if (nightsSel) nightsSel.value = '1';
        showToastSprint1('• Pack Escapade Couple VIP activé : Suite Cité Ewondo + 2 Repas + Pergola Lac + Piscine & Pirogue (Forfait 45 000 FCFA) !');
      }
      updateBundleButtonsUI();
      recalcSimulator();
    }

    function getSelectedLodgeDetails() {
      const cityEl = document.getElementById('lodgeCitySelect');
      const nightsEl = document.getElementById('lodgeNightsSelect');
      const city = cityEl ? cityEl.value : 'EWONDO';
      const nights = nightsEl ? (parseInt(nightsEl.value, 10) || 1) : 1;
      const map = {
        EWONDO: { label: 'Suite VIP Cité Ewondo Climatisée', unit: 25000 },
        CHANTHEL: { label: 'Loge Cité Chanthel Confort', unit: 15000 },
        BENE: { label: 'Pavillon Cité Bene Calme', unit: 10000 }
      };
      const cfg = map[city] || map.EWONDO;
      return {
        city,
        nights,
        unit: cfg.unit,
        total: cfg.unit * nights,
        summary: `${cfg.label} (${nights} nuit${nights > 1 ? 's' : ''})`
      };
    }

    function recalcSimulator() {
      const totalPayingPax = counts.adults + counts.children;
      const isGroup20Plus = totalPayingPax >= 20;

      // RÈGLE MÉTIER STRICTE :
      // En groupe (>=20), l'entrée adulte passe de 1 000 à 700 FCFA,
      // MAIS l'entrée enfant reste protégée à 500 FCFA (jamais majorée à 700 FCFA !).
      const zooAdultUnit = isGroup20Plus ? 700 : 1000;
      const zooChildUnit = 500;

      // Tarif Piscine Enfant : 1 500 FCFA (Prévente En Ligne / Semaine) vs 2 500 FCFA (Guichet Week-end & Jours Fériés)
      const poolPeriodEl = document.getElementById('poolRatePeriod');
      const isWeekendFullRate = poolPeriodEl && poolPeriodEl.value === 'WEEKEND_PLEIN';
      const piscineChildUnit = isWeekendFullRate ? 2500 : 1500;
      const lblPiscineInfo = document.getElementById('lblPiscineRateInfo');
      if (lblPiscineInfo) {
        lblPiscineInfo.textContent = isWeekendFullRate
          ? '(Enfant Week-end/Férié : 2 500 FCFA • Adulte : 2 500 FCFA)'
          : '(Enfant Prévente/Semaine : 1 500 FCFA • Adulte : 2 500 FCFA)';
      }

      const zooCost = document.getElementById('chkZoo').checked
        ? (counts.adults * zooAdultUnit + counts.children * zooChildUnit) : 0;
      const piscineCost = document.getElementById('chkPiscine').checked
        ? (counts.adults * 2500 + counts.children * piscineChildUnit) : 0;
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
      const bumpNavetteChecked = document.getElementById('chkBumpNavette') && document.getElementById('chkBumpNavette').checked;
      const bumpPecheChecked = document.getElementById('chkBumpPeche') && document.getElementById('chkBumpPeche').checked;

      const nutritionPacksCount = bumpNutritionChecked ? Math.max(1, counts.children) : 0;
      const nutritionCost = nutritionPacksCount * 500;
      const pergolaCost = bumpPergolaChecked ? 5000 : 0;
      const lodgeDetails = getSelectedLodgeDetails();
      const lodgeCost = bumpLodgeChecked ? lodgeDetails.total : 0;
      const navetteCost = bumpNavetteChecked ? (counts.adults * 1500 + counts.children * 1000) : 0;
      const pecheCost = bumpPecheChecked ? 2000 : 0;

      document.getElementById('subZoo').textContent = formatFCFA(zooCost);
      document.getElementById('subPiscine').textContent = formatFCFA(piscineCost);
      document.getElementById('subPirogue').textContent = formatFCFA(pirogueCost);
      document.getElementById('subCheval').textContent = formatFCFA(chevalCost);
      document.getElementById('subRepas').textContent = formatFCFA(repasCost);
      if (document.getElementById('subBumpNutrition')) document.getElementById('subBumpNutrition').textContent = formatFCFA(nutritionCost);
      if (document.getElementById('subBumpPergola')) document.getElementById('subBumpPergola').textContent = formatFCFA(pergolaCost);
      if (document.getElementById('subBumpLodge')) document.getElementById('subBumpLodge').textContent = formatFCFA(lodgeCost);
      if (document.getElementById('subBumpNavette')) document.getElementById('subBumpNavette').textContent = formatFCFA(navetteCost);
      if (document.getElementById('subBumpPeche')) document.getElementById('subBumpPeche').textContent = formatFCFA(pecheCost);

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

      const rawSubtotal = zooCost + piscineCost + pirogueCost + chevalCost + repasCost + nutritionCost + pergolaCost + lodgeCost + navetteCost + pecheCost;
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
      if (piscineCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Piscine Semi-Olympique (${isWeekendFullRate ? 'Tarif Week-end' : 'Tarif Prévente/Semaine'})</span><strong>${formatFCFA(piscineCost)}</strong></div>`);
      if (pirogueCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Balade en Pirogue (Lac d'Ahala)</span><strong>${formatFCFA(pirogueCost)}</strong></div>`);
      if (chevalCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Équitation / Manèges</span><strong>${formatFCFA(chevalCost)}</strong></div>`);
      if (repasCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;"><span>Repas Le Château des Saveurs</span><strong>${formatFCFA(repasCost)}</strong></div>`);
      if (nutritionCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Order Bump : ${nutritionPacksCount}× Sachet(s) Nutrition Poissons</span><strong>${formatFCFA(nutritionCost)}</strong></div>`);
      if (pergolaCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Order Bump : Pergola Privée Bord du Lac (13h)</span><strong>${formatFCFA(pergolaCost)}</strong></div>`);
      if (lodgeCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Hébergement : ${lodgeDetails.summary}</span><strong>${formatFCFA(lodgeCost)}</strong></div>`);
      if (navetteCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Logistique : Navette Climatisée A/R Yaoundé</span><strong>${formatFCFA(navetteCost)}</strong></div>`);
      if (pecheCost > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:#8E5617;"><span>+ Découverte : Pêche Ludique &amp; Musée/Forêt</span><strong>${formatFCFA(pecheCost)}</strong></div>`);
      if (bundleDiscount > 0) lines.push(`<div style="display:flex;justify-content:space-between;color:var(--color-brand-deep);font-weight:700;"><span>${bundleLabel}</span><strong>-${formatFCFA(bundleDiscount)}</strong></div>`);"""

    assert old_recalc_block in text, "old_recalc_block introuvable"
    text = text.replace(old_recalc_block, new_recalc_block, 1)

    # -------------------------------------------------------------------------
    # 6. MISE À JOUR DE getActiveSimulatorItemsSummary()
    # -------------------------------------------------------------------------
    old_items_summary = """      if (document.getElementById('chkBumpNutrition') && document.getElementById('chkBumpNutrition').checked) acts.push('Sachet Nutrition Poissons (+500 F)');
      if (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked) acts.push('Pergola Privée 13h (+5 000 F)');
      if (document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked) acts.push('Suite VIP Cité Ewondo (+25 000 F)');
      return acts.join(', ') || 'Accès Parc & Détente';"""

    new_items_summary = """      if (document.getElementById('chkBumpNutrition') && document.getElementById('chkBumpNutrition').checked) acts.push('Sachet Nutrition Poissons (+500 F)');
      if (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked) acts.push('Pergola Privée 13h (+5 000 F)');
      if (document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked) {
        const ld = typeof getSelectedLodgeDetails === 'function' ? getSelectedLodgeDetails() : { summary: 'Suite VIP Cité Ewondo', total: 25000 };
        acts.push(`${ld.summary} (+${formatFCFA(ld.total)})`);
      }
      if (document.getElementById('chkBumpNavette') && document.getElementById('chkBumpNavette').checked) acts.push('Navette Climatisée A/R Yaoundé');
      if (document.getElementById('chkBumpPeche') && document.getElementById('chkBumpPeche').checked) acts.push('Pêche Ludique & Musée/Forêt (+2 000 F)');
      return acts.join(', ') || 'Accès Parc & Détente';"""

    assert old_items_summary in text, "old_items_summary introuvable"
    text = text.replace(old_items_summary, new_items_summary, 1)

    # -------------------------------------------------------------------------
    # 7. VALIDATION STRICTE + CALCULATEUR PROFORMA B2B/ÉCOLE/MARIAGE + CFP >= 16 ANS
    # -------------------------------------------------------------------------
    old_booking_and_modals_js = """    // Génération et persistance d'un nouveau billet QR depuis le simulateur (RES-09)
    function createLiveBookingSprint1() {
      const db = loadDB();
      const holder = (document.getElementById('visitorName') || {}).value || 'Visiteur ECOPARK';
      const phone = (document.getElementById('visitorPhone') || {}).value || '+237 694 12 34 56';
      const rawDate = (document.getElementById('visitDate') || {}).value || '2026-11-15';
      const totalText = (document.getElementById('grandTotalFCFA') || {}).textContent || '14 000 FCFA';
      const totalNum = parseInt(totalText.replace(/[^0-9]/g, ''), 10) || 14000;

      const acts = [];
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
      }

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

      showToastSprint1(`• Réservation ${ref} enregistrée ! Billet disponible dans « Mon Espace » et prêt à être scanné au Guichet.`);
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
      showToastSprint1(`Devis ${ref} enregistré ! Retrouvez-le dans « Mon Espace » (ACC-04) et dans « Exploitation » (EXP-03).`);
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
      showToastSprint1(`Candidature ${ref} (${track}) enregistrée et visible dans l'espace Exploitation (EXP-06) !`);
    }"""

    new_booking_and_modals_js = """    function isValidCameroonPhone(phoneStr) {
      const digits = String(phoneStr || '').replace(/[^0-9]/g, '');
      return digits.length >= 8;
    }

    // Génération et persistance d'un nouveau billet QR depuis le simulateur (RES-09)
    function createLiveBookingSprint1() {
      const nameEl = document.getElementById('visitorName');
      const phoneEl = document.getElementById('visitorPhone');
      const dateEl = document.getElementById('visitDate');
      const holder = nameEl ? nameEl.value.trim() : 'M. Jean-Paul MBARGA';
      const phone = phoneEl ? phoneEl.value.trim() : '+237 694 12 34 56';
      const rawDate = dateEl ? dateEl.value.trim() : '2026-11-15';

      if (!holder || holder.length < 2) {
        if (nameEl) nameEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez renseigner le Nom et Prénom du visiteur (RES-05).');
        return false;
      }
      if (!isValidCameroonPhone(phone)) {
        if (phoneEl) phoneEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez saisir un numéro WhatsApp / Mobile Money Cameroun valide (+237).');
        return false;
      }
      if ((counts.adults + counts.children) < 1) {
        showToastSprint1('• Veuillez sélectionner au moins 1 participant payant (Adulte ou Enfant).');
        return false;
      }

      const db = loadDB();
      const totalText = (document.getElementById('grandTotalFCFA') || {}).textContent || '14 000 FCFA';
      const totalNum = parseInt(totalText.replace(/[^0-9]/g, ''), 10) || 14000;

      const acts = [];
      if (window._activeBundleCode && window._activeBundleCode !== 'CUSTOM') acts.push(window._activeBundleCode);
      if (document.getElementById('chkZoo') && document.getElementById('chkZoo').checked) acts.push('Zoo');
      if (document.getElementById('chkPiscine') && document.getElementById('chkPiscine').checked) acts.push('Piscine');
      if (document.getElementById('chkPirogue') && document.getElementById('chkPirogue').checked) acts.push('Pirogue');
      if (document.getElementById('chkCheval') && document.getElementById('chkCheval').checked) acts.push('Équitation');
      if (document.getElementById('chkRepas') && document.getElementById('chkRepas').checked) acts.push('Saveurs');
      if (document.getElementById('chkBumpNutrition') && document.getElementById('chkBumpNutrition').checked) acts.push('Nutrition Poissons');
      if (document.getElementById('chkBumpPergola') && document.getElementById('chkBumpPergola').checked) acts.push('Pergola Lac');
      if (document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked) {
        const ld = typeof getSelectedLodgeDetails === 'function' ? getSelectedLodgeDetails() : { summary: 'Suite Ewondo' };
        acts.push(ld.summary);
      }
      if (document.getElementById('chkBumpNavette') && document.getElementById('chkBumpNavette').checked) acts.push('Navette A/R');
      if (document.getElementById('chkBumpPeche') && document.getElementById('chkBumpPeche').checked) acts.push('Pêche & Musée');

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
        const ld = typeof getSelectedLodgeDetails === 'function' ? getSelectedLodgeDetails() : { city: 'EWONDO' };
        if (ld.city === 'EWONDO') {
          db.opsMetrics.ewondoFree = Math.max(0, db.opsMetrics.ewondoFree - 1);
        }
      }

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

      showToastSprint1(`• Réservation ${ref} enregistrée ! Billet disponible dans « Mon Espace » et prêt à être scanné au Guichet.`);
      return true;
    }

    function computeQuoteBudgetSprint1() {
      const type = ((document.getElementById('quoteType') || {}).value || 'Excursion scolaire');
      const pax = Math.max(10, parseInt(((document.getElementById('quotePax') || {}).value || '60'), 10) || 60);
      const optHall = document.getElementById('quoteOptHall') && document.getElementById('quoteOptHall').checked;
      const optShuttle = document.getElementById('quoteOptShuttle') && document.getElementById('quoteOptShuttle').checked;

      let unitRate = 1500;
      let rateDesc = 'Forfait Excursion Scolaire (Entrée enfant protégée 500 FCFA + Piscine/Pirogue encadrée)';
      let hallCost = optHall ? 75000 : 0;

      if (type.includes('Séminaire')) {
        unitRate = 12500;
        rateDesc = 'Forfait Séminaire B2B (Salle Menkii Essomba Anton + Pause-café + Déjeuner Château des Saveurs)';
        hallCost = 0; // Déjà inclus dans le forfait Séminaire
      } else if (type.includes('Mariage') || type.includes('Grande Réunion')) {
        unitRate = 15000;
        rateDesc = 'Forfait Réception / Mariage (Salle Menkii Essomba Anton / Esplanade + Buffet Royal)';
        hallCost = 0; // Inclus dans le forfait Réception
      }

      const shuttleCost = optShuttle ? 45000 : 0;
      const total = (pax * unitRate) + hallCost + shuttleCost;
      const opts = [];
      if (type.includes('Séminaire') || type.includes('Mariage') || optHall) opts.push('Salle Menkii Essomba Anton');
      if (optShuttle) opts.push('Navette Climatisée A/R (18/32 places)');
      return {
        pax,
        unitRate,
        hallCost,
        shuttleCost,
        total,
        rateDesc,
        optionsSummary: opts.join(' + ') || 'Prestations Parc & Encadrement'
      };
    }

    function recalcQuoteProformaPreview() {
      const calc = computeQuoteBudgetSprint1();
      const totEl = document.getElementById('quoteProformaTotalText');
      const brkEl = document.getElementById('quoteProformaBreakdownText');
      if (totEl) totEl.textContent = formatFCFA(calc.total);
      if (brkEl) {
        const extras = [];
        if (calc.hallCost > 0) extras.push(`+ Salle Menkii Essomba Anton (${formatFCFA(calc.hallCost)})`);
        if (calc.shuttleCost > 0) extras.push(`+ Navette A/R (${formatFCFA(calc.shuttleCost)})`);
        brkEl.textContent = `${calc.pax} participants × ${formatFCFA(calc.unitRate)} — ${calc.rateDesc}${extras.length ? ' ' + extras.join(' ') : ''}.`;
      }
    }

    function openQuoteModalSprint1() {
      document.getElementById('modalOverlaySprint1').style.display = 'flex';
      document.getElementById('modalQuoteBox').style.display = 'flex';
      document.getElementById('modalCfpBox').style.display = 'none';
      recalcQuoteProformaPreview();
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
      const orgEl = document.getElementById('quoteOrgName');
      const phoneEl = document.getElementById('quotePhone');
      const org = orgEl ? orgEl.value.trim() : '';
      const phone = phoneEl ? phoneEl.value.trim() : '';
      if (!org || org.length < 2) {
        if (orgEl) orgEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez indiquer le nom de l\'établissement, entreprise ou association.');
        return false;
      }
      if (!isValidCameroonPhone(phone)) {
        if (phoneEl) phoneEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez indiquer un numéro WhatsApp valide (+237).');
        return false;
      }

      const db = loadDB();
      const type = document.getElementById('quoteType').value || 'Excursion scolaire';
      const date = document.getElementById('quoteDate').value || '2026-12-10';
      const calc = computeQuoteBudgetSprint1();
      const ref = 'DEV-2026-' + Math.floor(1000 + Math.random() * 8999);

      db.quotes.unshift({
        reference: ref,
        org: org,
        type: `${type} (${calc.optionsSummary})`,
        pax: calc.pax,
        date: date,
        budgetFcfa: calc.total,
        status: 'Proforma générée (Exploitation)'
      });
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${org} (Groupe)`,
        action: `Demande de devis ${ref} (${calc.pax} pers., ${formatFCFA(calc.total)} • ${calc.optionsSummary}) transmise à l'Exploitation.`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`Devis Proforma ${ref} (${formatFCFA(calc.total)}) enregistré ! Retrouvez-le dans « Mon Espace » (ACC-04) et « Exploitation » (EXP-03).`);
      return ref;
    }

    function submitCfpApplicationSprint1() {
      const nameEl = document.getElementById('cfpCandidateName');
      const ageEl = document.getElementById('cfpAge');
      const phoneEl = document.getElementById('cfpPhone');
      const name = nameEl ? nameEl.value.trim() : '';
      const age = ageEl ? parseInt(ageEl.value, 10) : 19;
      const phone = phoneEl ? phoneEl.value.trim() : '';

      if (!name || name.length < 2) {
        if (nameEl) nameEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez saisir le Nom et Prénom du candidat CFP.');
        return false;
      }
      if (isNaN(age) || age < 16) {
        if (ageEl) ageEl.focus();
        showToastSprint1('• Condition réglementaire MINEFOP : Le candidat doit être âgé d\'au moins 16 ans révolus.');
        return false;
      }
      if (!isValidCameroonPhone(phone)) {
        if (phoneEl) phoneEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez saisir un numéro de téléphone Cameroun (+237) valide.');
        return false;
      }

      const db = loadDB();
      const track = (document.getElementById('cfpTrack') || {}).value || 'Pisciculture';
      const plan = (document.getElementById('cfpPaymentPlan') || {}).value || 'Échéancier 4 tranches (100k + 3x50k FCFA)';
      const ref = 'CFP-2026-' + Math.floor(1000 + Math.random() * 8999);

      db.cfpApplications.unshift({
        reference: ref,
        name: `${name} (${age} ans)`,
        track: `${track} • ${plan}`,
        phone: phone,
        status: 'Dossier reçu (Inscription 50 000 FCFA)'
      });
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${name} (Candidat CFP, ${age} ans)`,
        action: `Candidature CFP ${ref} déposée en filière « ${track} » (${plan}).`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`Candidature ${ref} (${track} • ${age} ans • ${plan}) enregistrée dans l'espace Exploitation (EXP-06) !`);
      return ref;
    }

    function sendWhatsAppCfpSprint1() {
      const ref = submitCfpApplicationSprint1();
      if (!ref) return;
      const name = (document.getElementById('cfpCandidateName') || {}).value || 'Candidat CFP';
      const age = (document.getElementById('cfpAge') || {}).value || '19';
      const track = (document.getElementById('cfpTrack') || {}).value || 'Hôtellerie';
      const phone = (document.getElementById('cfpPhone') || {}).value || '+237 677 88 99 00';
      const plan = (document.getElementById('cfpPaymentPlan') || {}).value || 'Échéancier 4 tranches';
      const msg = [
        `Bonjour CFP ECOPARK CAMEROUN (Yaoundé-Ahala),`,
        `Je souhaite valider mon dossier d'admission au Centre de Formation Professionnelle agréé MINEFOP :`,
        `- N° Dossier : ${ref}`,
        `- Candidat(e) : ${name} (${age} ans) — ${phone}`,
        `- Filière choisie : ${track} (Stage garanti au sein d'ECOPARK)`,
        `- Modalité choisie : Inscription 50 000 FCFA + ${plan}`,
        `- Diplômes visés : DQP / CQP / Attestation reconnue par l'État`,
        `Merci de m'indiquer la procédure de règlement des 50 000 FCFA d'inscription.`
      ].join('\\n');
      const url = 'https://wa.me/237697136203?text=' + encodeURIComponent(msg);
      window.open(url, '_blank', 'noopener,noreferrer');
    }"""

    assert old_booking_and_modals_js in text, "old_booking_and_modals_js introuvable"
    text = text.replace(old_booking_and_modals_js, new_booking_and_modals_js, 1)

    # -------------------------------------------------------------------------
    # 8. MISE À JOUR DE sendWhatsAppQuoteSprint1() POUR UTILISER computeQuoteBudgetSprint1()
    # -------------------------------------------------------------------------
    old_wa_quote = """    function sendWhatsAppQuoteSprint1() {
      const db = loadDB();
      const org = (document.getElementById('quoteOrgName') || {}).value || 'Groupe ECOPARK';
      const type = (document.getElementById('quoteType') || {}).value || 'Excursion scolaire';
      const pax = parseInt((document.getElementById('quotePax') || {}).value, 10) || 40;
      const date = (document.getElementById('quoteDate') || {}).value || '2026-12-10';
      const ref = 'DEV-2026-' + Math.floor(1000 + Math.random() * 8999);
      const budget = pax * 1500;

      db.quotes.unshift({
        reference: ref,
        org: org,
        type: type,
        pax: pax,
        date: date,
        budgetFcfa: budget,
        status: 'Demande WhatsApp & Exploitation'
      });
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${org} (Groupe B2B/École)`,
        action: `Demande de proforma WhatsApp ${ref} (${pax} pers., ~${formatFCFA(budget)}) transmise au Guichet Unique.`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`• Devis ${ref} enregistré et prêt dans WhatsApp ! Visible dans « Mon Espace » (ACC-04) et « Exploitation » (EXP-03 / EXP-07).`);

      const msg = [
        `Bonjour ECOPARK CAMEROUN (Yaoundé-Ahala),`,
        `Je souhaite obtenir une Proforma Officielle en 2 minutes (Guichet Unique WhatsApp) :`,
        `- Référence Dossier : ${ref}`,
        `- Établissement / Organisation : ${org}`,
        `- Type d'événement : ${type}`,
        `- Effectif prévu : ${pax} participants (Tarif enfant protégé à 500 FCFA)`,
        `- Date souhaitée : ${date}`,
        `- Estimation de base : ${formatFCFA(budget)}`,
        `- Options : Salle Polyvalente Menkii Essomba Anton & Navettes (5/18/32 places)`,
        `Merci de m'envoyer la Proforma PDF officielle dans cette discussion.`
      ].join('\\n');
      const url = 'https://wa.me/237697136203?text=' + encodeURIComponent(msg);
      window.open(url, '_blank', 'noopener,noreferrer');
    }"""

    new_wa_quote = """    function sendWhatsAppQuoteSprint1() {
      const orgEl = document.getElementById('quoteOrgName');
      const phoneEl = document.getElementById('quotePhone');
      const org = orgEl ? orgEl.value.trim() : 'Groupe ECOPARK';
      const phone = phoneEl ? phoneEl.value.trim() : '+237 699 45 67 89';
      if (!org || org.length < 2) {
        if (orgEl) orgEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez indiquer le nom de l\'établissement ou de l\'entreprise.');
        return false;
      }
      if (!isValidCameroonPhone(phone)) {
        if (phoneEl) phoneEl.focus();
        showToastSprint1('• Champ obligatoire : Veuillez indiquer un numéro WhatsApp valide (+237).');
        return false;
      }

      const db = loadDB();
      const type = (document.getElementById('quoteType') || {}).value || 'Excursion scolaire';
      const date = (document.getElementById('quoteDate') || {}).value || '2026-12-10';
      const calc = computeQuoteBudgetSprint1();
      const ref = 'DEV-2026-' + Math.floor(1000 + Math.random() * 8999);

      db.quotes.unshift({
        reference: ref,
        org: org,
        type: `${type} (${calc.optionsSummary})`,
        pax: calc.pax,
        date: date,
        budgetFcfa: calc.total,
        status: 'Proforma WhatsApp & Exploitation'
      });
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: `${org} (Groupe B2B/École)`,
        action: `Demande de proforma WhatsApp ${ref} (${calc.pax} pers., ${formatFCFA(calc.total)} • ${calc.optionsSummary}) transmise au Guichet Unique.`
      });
      saveDB(db);
      closeSprint1Modals();
      showToastSprint1(`• Devis Proforma ${ref} (${formatFCFA(calc.total)}) enregistré et prêt dans WhatsApp ! Visible dans ACC-04 et EXP-03 / EXP-07.`);

      const msg = [
        `Bonjour ECOPARK CAMEROUN (Yaoundé-Ahala),`,
        `Je souhaite obtenir une Proforma Officielle en 2 minutes (Guichet Unique WhatsApp) :`,
        `- Référence Dossier : ${ref}`,
        `- Établissement / Organisation : ${org} (${phone})`,
        `- Type d'événement : ${type}`,
        `- Effectif prévu : ${calc.pax} participants (${calc.rateDesc})`,
        `- Date souhaitée : ${date}`,
        `- Prestations & Logistique : ${calc.optionsSummary}`,
        `- Total Proforma Estimé TTC : ${formatFCFA(calc.total)}`,
        `Merci de m'envoyer la Proforma PDF officielle dans cette discussion.`
      ].join('\\n');
      const url = 'https://wa.me/237697136203?text=' + encodeURIComponent(msg);
      window.open(url, '_blank', 'noopener,noreferrer');
    }"""

    assert old_wa_quote in text, "old_wa_quote introuvable"
    text = text.replace(old_wa_quote, new_wa_quote, 1)

    # -------------------------------------------------------------------------
    # VÉRIFICATION STRICTE : ZÉRO CARACTÈRE UNICODE > 0x25FF
    # -------------------------------------------------------------------------
    bad_chars = [(i, ch, hex(ord(ch))) for i, ch in enumerate(text) if ord(ch) > 0x25FF]
    if bad_chars:
        raise ValueError(f"Caractères > 0x25FF détectés : {bad_chars[:10]}")

    out_bytes = (text.replace("\n", "\r\n") if has_crlf else text).encode("utf-8")
    INDEX_PATH.write_bytes(out_bytes)
    shutil.copyfile(INDEX_PATH, PROTO_PATH)
    print(f"SUCCÈS : 7 remédiations appliquées à {INDEX_PATH.name} et synchronisées vers {PROTO_PATH.name} ({len(text.splitlines())} lignes, 0 caractère > 0x25FF).")


if __name__ == "__main__":
    apply_remediations()
