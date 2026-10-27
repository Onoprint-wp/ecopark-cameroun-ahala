# -*- coding: utf-8 -*-
"""
Générateur du Prototype de Validation Visuelle de l'Administration ECOPARK (ADM-01 à ADM-08)
avec moteur CRUD complet (« Ajouter, Modifier, Dupliquer, Supprimer, Rechercher & Filtrer ») :
1. ADM-01 / ADM-02 : CRUD Catalogue & Grille Tarifaire FCFA (+ Ajouter, Modifier en modale, Dupliquer en 1 clic, Supprimer avec garde-fou, Recherche & Filtres par pôle) + Garde-fou SQL Enfant 500 FCFA.
2. ADM-03 : Quotas journaliers, stocks Cités Hôtelières & Bandeau Météo RN3 en direct.
3. ADM-04 : Mini-CMS CRUD Zéro Code (Onglets Agenda de la Semaine /agenda & Carte du Château des Saveurs /restaurant avec Ajouter, Modifier, Dupliquer, Supprimer).
4. ADM-05 : CRUD Comptes Équipe Ahala & Matrice RBAC des 7 Rôles (+ Nouvel Agent, Modifier Rôle, Dupliquer Poste, Suspendre/Activer).
5. ADM-06 / ADM-07 : Passerelles MTN MoMo / Orange Money / WhatsApp sans secrets exposés.
6. ADM-08 : Journal d'Audit Immuable traçant chaque action CRUD (Création, Modification, Duplication, Suppression, Garde-Fou).
"""

import pathlib
import re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "etape0-site-live" / "index.html"
PREVIEW_HTML = ROOT / "Preview_Administration_ECOPARK.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\7ee4ce6d-03a1-4262-8080-a7fbda05ab9a")
LOCAL_QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"

ADMIN_CONSOLE_CSS = r"""
    /* ==========================================================================
       CONSOLE D'ADMINISTRATION & MOTEUR CRUD METIER (ADM-01 A ADM-08)
       ========================================================================== */
    .adm-crud-modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(20, 34, 17, 0.58);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 3200;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .adm-crud-modal-overlay.open {
      display: flex;
    }
    .adm-crud-modal-card {
      max-width: 680px;
      width: 100%;
      background: #FFFFFF;
      padding: 26px 28px;
      border-radius: 20px;
      border: 1.5px solid rgba(29, 73, 13, 0.2);
      box-shadow: 0 28px 68px rgba(20, 34, 17, 0.25);
    }
    .adm-tier-switcher {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 18px;
    }
    @media (max-width: 960px) {
      .adm-tier-switcher {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    @media (max-width: 560px) {
      .adm-tier-switcher {
        grid-template-columns: 1fr;
      }
    }
    .adm-tier-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(29, 73, 13, 0.14);
      border-radius: 16px;
      padding: 13px 15px;
      text-align: left;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 6px;
      box-shadow: 0 8px 22px rgba(20, 34, 17, 0.04);
    }
    .adm-tier-card:hover {
      transform: translateY(-2px);
      border-color: #C47D2B;
      background: #FBF5EC;
    }
    .adm-tier-card.active {
      background: linear-gradient(180deg, #EDF4E7 0%, #FFFFFF 90%);
      border: 2px solid #1D490D;
      box-shadow: 0 12px 28px rgba(29, 73, 13, 0.12);
    }
    .adm-kpi-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 20px;
    }
    .adm-kpi-box {
      background: var(--color-surface-soft);
      border: 1px solid rgba(29, 73, 13, 0.14);
      border-radius: 14px;
      padding: 12px 15px;
    }
    .adm-kpi-box.ochre {
      background: #FBF5EC;
      border-color: rgba(196, 125, 43, 0.38);
    }
    .adm-crud-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      padding: 12px 14px;
      border-radius: 14px;
      background: var(--color-surface-soft);
      border: 1px solid rgba(29, 73, 13, 0.14);
      margin-bottom: 14px;
    }
    .adm-pole-pills {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .adm-pole-pill {
      padding: 6px 12px;
      border-radius: 980px;
      border: 1px solid rgba(29, 73, 13, 0.18);
      background: #FFFFFF;
      color: var(--color-text);
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .adm-pole-pill:hover {
      border-color: #C47D2B;
      background: #FBF5EC;
    }
    .adm-pole-pill.active {
      background: #1D490D;
      color: #FFFFFF;
      border-color: #1D490D;
    }
    .adm-price-cell {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
    }
    .adm-input-fcfa {
      width: 78px;
      padding: 4px 7px;
      border-radius: 8px;
      border: 1.5px solid rgba(29, 73, 13, 0.22);
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 14px;
      color: var(--color-brand-deep);
      background: #FFFFFF;
      text-align: right;
    }
    .adm-input-fcfa.locked-child {
      background: #EDF4E7;
      border-color: #1D490D;
      color: #1D490D;
    }
    .adm-crud-actions {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
    }
    .adm-action-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 5px 9px;
      border-radius: 8px;
      border: 1px solid rgba(29, 73, 13, 0.2);
      background: #FFFFFF;
      color: var(--color-brand-deep);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.18s ease;
    }
    .adm-action-btn:hover {
      background: #EDF4E7;
      border-color: #1D490D;
    }
    .adm-action-btn.duplicate {
      background: #FBF5EC;
      border-color: rgba(196, 125, 43, 0.45);
      color: #8E5617;
    }
    .adm-action-btn.duplicate:hover {
      background: #F5E6D0;
      border-color: #C47D2B;
    }
    .adm-action-btn.danger {
      color: #B3261E;
      border-color: rgba(179, 38, 30, 0.28);
    }
    .adm-action-btn.danger:hover {
      background: #FCEEEE;
      border-color: #B3261E;
    }
    .adm-row-duplicated {
      background: linear-gradient(90deg, #FBF5EC 0%, #FFFFFF 65%) !important;
    }
    .adm-guard-callout {
      padding: 12px 16px;
      border-radius: 12px;
      background: #EDF4E7;
      border: 1.5px solid rgba(29, 73, 13, 0.24);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 12px;
    }
    .adm-guard-callout.rejected {
      background: #FCEEEE;
      border-color: #B3261E;
      color: #B3261E;
    }
    .adm-quota-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 11px 14px;
      border-radius: 12px;
      background: var(--color-surface-soft);
      border: 1px solid rgba(29, 73, 13, 0.12);
      margin-bottom: 10px;
    }
    .adm-cms-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 10px 12px;
      border-radius: 12px;
      background: #FFFFFF;
      border: 1px solid rgba(29, 73, 13, 0.14);
      margin-bottom: 8px;
      flex-wrap: wrap;
    }
    .adm-cms-item img {
      width: 48px;
      height: 48px;
      border-radius: 9px;
      object-fit: cover;
      flex-shrink: 0;
      border: 1px solid rgba(29, 73, 13, 0.18);
    }
    .adm-gateway-card {
      padding: 10px 14px;
      border-radius: 12px;
      background: var(--color-surface-soft);
      border: 1px solid rgba(29, 73, 13, 0.14);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .adm-secret-mask {
      font-family: monospace;
      font-size: 12.5px;
      background: #FFFFFF;
      padding: 2px 7px;
      border-radius: 6px;
      border: 1px solid rgba(29, 73, 13, 0.18);
      color: var(--color-text);
    }
    .adm-audit-filter-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }
"""

NEW_VIEW_ADM_HTML = """      <!-- ====================================================================
           FAMILLE 8 : ADMINISTRATION DE LA PLATEFORME (ADM-01 à ADM-08)
           ==================================================================== -->
      <section class="family-view" id="view-ADM">
        <div class="subnav-bar">
          <div class="container">
            <div class="subnav-list">
              <button class="subnav-pill active" onclick="inspectScreen('ADM-01')">ADM-01 Catalogue (CRUD)</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-02')">ADM-02 Tarifs &amp; Garde-Fou 500 F</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-03')">ADM-03 Jauges, Quotas &amp; Météo</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-04')">ADM-04 Mini-CMS Agenda &amp; Saveurs</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-05')">ADM-05 Comptes &amp; 7 Rôles RBAC</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-06')">ADM-06/07 Passerelles MoMo/OM</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-08')">ADM-08 Journal d'Audit Immuable</button>
            </div>
          </div>
        </div>

        <div class="section" style="padding-top:20px;">
          <div class="container">
            <div class="section-header" style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
              <div>
                <span class="eyebrow"><span class="tech-code-tag">ADM-01 à ADM-08 • </span>Architecture d'Administration « Zéro Casse, Zéro Coulage, Zéro Code »</span>
                <h2 style="margin-bottom:4px;">Poste de Gouvernance, Moteur CRUD Métier, Tarifs FCFA &amp; Audit Immuable</h2>
                <p style="color:var(--color-text-muted);max-width:840px;font-size:14.5px;">
                  Gérez l'intégralité du complexe d'Ahala (<strong>Ajouter, Modifier, Dupliquer en 1 clic, Mettre en pause ou Supprimer</strong> une prestation, un événement de l'Agenda, un plat du <em>Château des Saveurs</em> ou un compte agent) dans des formulaires cadrés qui préservent le design et verrouillent le tarif enfant à <strong>500 FCFA</strong>.
                </p>
              </div>
              <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openAdmCrudModal('CREATE', null)">+ Ajouter une Prestation / Offre</button>
                <button type="button" class="btn btn-primary btn-sm" onclick="exportEcoparkDatabaseCSV()">Exporter Base &amp; Audit CSV</button>
              </div>
            </div>

            <!-- AIGUILLAGE DES 4 ESPACES BACK-OFFICE CLOISONNÉS -->
            <div class="adm-tier-switcher" id="admTierSwitcher">
              <button type="button" class="adm-tier-card" onclick="navigateFamily('AGT', 'AGT-01')">
                <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
                  <span class="price-pill" style="font-size:11px;padding:2px 8px;">Niveau 1 • /guichet</span>
                  <span style="font-size:11.5px;color:var(--color-text-muted);font-weight:600;">AGT-01..09</span>
                </div>
                <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);">Guichet &amp; Tourniquet QR</strong>
                <span style="font-size:12.2px;color:var(--color-text-muted);">Caisse walk-in 1 clic, scan QR 7 verdicts, PV de clôture. Aucun droit sur les tarifs.</span>
              </button>

              <button type="button" class="adm-tier-card" onclick="navigateFamily('EXP', 'EXP-01')">
                <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
                  <span class="price-pill" style="font-size:11px;padding:2px 8px;">Niveau 2 • Exploitation</span>
                  <span style="font-size:11.5px;color:var(--color-text-muted);font-weight:600;">EXP-01..07</span>
                </div>
                <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);">Exploitation &amp; Closing WhatsApp</strong>
                <span style="font-size:12.2px;color:var(--color-text-muted);">Loges Ewondo/Chanthel/Bene, cuisine 13h, devis écoles/B2B &amp; admissions CFP.</span>
              </button>

              <button type="button" class="adm-tier-card" onclick="navigateFamily('DIR', 'DIR-01')">
                <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
                  <span class="price-pill" style="font-size:11px;padding:2px 8px;">Niveau 3 • /direction</span>
                  <span style="font-size:11.5px;color:var(--color-text-muted);font-weight:600;">DIR-01..05</span>
                </div>
                <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);">Pilotage Exécutif Promoteur</strong>
                <span style="font-size:12.2px;color:var(--color-text-muted);">Vue Dr FOE NDI &amp; M. Mgbatou Daryl : recettes FCFA, MoMo vs Espèces, export Excel.</span>
              </button>

              <button type="button" class="adm-tier-card active" onclick="inspectScreen('ADM-01')">
                <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
                  <span class="status-badge status-success" style="font-size:11px;padding:2px 8px;">Niveau 4 Actif • /admin</span>
                  <span style="font-size:11.5px;color:var(--color-brand-deep);font-weight:700;">ADM-01..08</span>
                </div>
                <strong style="font-family:var(--font-heading);font-size:1.1rem;color:var(--color-brand-deep);">Gouvernance, CRUD &amp; CMS</strong>
                <span style="font-size:12.2px;color:var(--color-text-muted);">Ajouter, modifier, dupliquer, supprimer (Offres, Agenda, Plats, Comptes) &amp; Audit.</span>
              </button>
            </div>

            <!-- BANDEAU KPI GOUVERNANCE & SÉCURITÉ -->
            <div class="adm-kpi-strip">
              <div class="adm-kpi-box">
                <span style="font-size:12.2px;color:var(--color-text-muted);">Catalogue &amp; Formules Actives</span>
                <strong style="font-family:var(--font-heading);font-size:1.4rem;color:var(--color-brand-deep);display:block;margin-top:2px;" id="admCatalogCountKpi">6 Prestations FCFA</strong>
                <span style="font-size:11.8px;color:var(--color-brand-deep);">CRUD complet • Enfant protégé à 500 F</span>
              </div>
              <div class="adm-kpi-box">
                <span style="font-size:12.2px;color:var(--color-text-muted);">Contrôle d'Accès (Supabase RLS)</span>
                <strong style="font-family:var(--font-heading);font-size:1.4rem;color:var(--color-brand-deep);display:block;margin-top:2px;" id="admUsersCountKpi">6 Comptes (7 Rôles)</strong>
                <span style="font-size:11.8px;color:var(--color-brand-deep);">8 tables protégées • 2FA Direction &amp; Admin</span>
              </div>
              <div class="adm-kpi-box ochre">
                <span style="font-size:12.2px;color:#8E5617;font-weight:600;">Passerelles Mobile Money</span>
                <strong style="font-family:var(--font-heading);font-size:1.4rem;color:var(--color-brand-deep);display:block;margin-top:2px;" id="admGatewayModeKpi">Webhook Signé Actif</strong>
                <span style="font-size:11.8px;color:#8E5617;">Orange Money &amp; MTN MoMo • 0 clé exposée</span>
              </div>
              <div class="adm-kpi-box">
                <span style="font-size:12.2px;color:var(--color-text-muted);">Journal d'Audit Immuable</span>
                <strong style="font-family:var(--font-heading);font-size:1.4rem;color:var(--color-brand-deep);display:block;margin-top:2px;" id="admAuditCountKpi">Traçabilité 24/7</strong>
                <span style="font-size:11.8px;color:var(--color-brand-deep);">Toute création/modif/suppression tracée</span>
              </div>
            </div>

            <!-- ==============================================================
                 BLOC 1 : ADM-01 & ADM-02 — GESTIONNAIRE CRUD DU CATALOGUE & TARIFS FCFA
                 ============================================================== -->
            <div class="grid-12" style="margin-bottom:22px;" id="sec-ADM-01">
              <div class="col-12 card" id="sec-ADM-02">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:10px;">
                  <div>
                    <span class="eyebrow" style="margin-bottom:2px;"><span class="tech-code-tag">ADM-01 &amp; ADM-02 • </span>Moteur CRUD du Catalogue Officiel &amp; Verrouillage Tarifaire SQL</span>
                    <h3 style="margin:0;"><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span> <span class="tech-code-tag">ADM-01 &amp; ADM-02 — </span>Catalogue des Prestations (Ajouter, Modifier, Dupliquer, Supprimer) &amp; Protection 500 FCFA</h3>
                  </div>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" id="btnTestChildGuard" onclick="admTestChildPriceViolation()">
                      Tester Garde-Fou : Enfant Groupe = 700 FCFA
                    </button>
                    <button type="button" class="btn btn-primary btn-sm" onclick="openAdmCrudModal('CREATE', null)">
                      + Ajouter une Prestation / Pack
                    </button>
                  </div>
                </div>

                <!-- BARRE D'OUTILS CRUD : FILTRES PAR PÔLE + RECHERCHE INSTANTANÉE -->
                <div class="adm-crud-toolbar">
                  <div class="adm-pole-pills" id="admPoleFilterPills">
                    <button type="button" class="adm-pole-pill active" onclick="admFilterCatalogByPole('ALL', this)">Tous les pôles (6)</button>
                    <button type="button" class="adm-pole-pill" onclick="admFilterCatalogByPole('NATURE_FAUNE', this)">Nature &amp; Faune</button>
                    <button type="button" class="adm-pole-pill" onclick="admFilterCatalogByPole('EAU_PLEIN_AIR', this)">Eau &amp; Loisirs</button>
                    <button type="button" class="adm-pole-pill" onclick="admFilterCatalogByPole('RESTAURATION', this)">Saveurs &amp; Packs</button>
                    <button type="button" class="adm-pole-pill" onclick="admFilterCatalogByPole('HEBERGEMENT', this)">Cités Hôtelières</button>
                  </div>
                  <div style="display:flex;gap:8px;align-items:center;">
                    <input type="search" id="admCatalogSearchInput" class="form-control" placeholder="Rechercher une activité, un pack, un prix..." style="min-height:36px;font-size:13px;width:250px;background:#FFFFFF;" oninput="admRenderCatalogTable()" />
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admSaveCatalogPrices()">Tout Enregistrer</button>
                  </div>
                </div>

                <div class="table-responsive">
                  <table id="admCatalogCrudTable">
                    <thead>
                      <tr>
                        <th>Prestation / Pôle ECOPARK</th>
                        <th>Enfant (3–12 ans)</th>
                        <th>Adulte (13+ ans)</th>
                        <th>Groupe Adulte</th>
                        <th>Groupe Enfant (SQL)</th>
                        <th>Jauge</th>
                        <th>Statut</th>
                        <th>Actions CRUD (Modifier • Dupliquer • Supprimer)</th>
                      </tr>
                    </thead>
                    <tbody id="admCatalogTbody">
                      <!-- Injecté dynamiquement par admRenderCatalogTable() -->
                    </tbody>
                  </table>
                </div>

                <!-- Bandeau de démonstration du Garde-Fou SQL Enfant 500 FCFA -->
                <div class="adm-guard-callout" id="admChildGuardBanner">
                  <div style="display:flex;align-items:center;gap:10px;">
                    <span class="icon-medallion" style="width:34px;height:34px;"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg></span>
                    <div>
                      <strong id="admChildGuardTitle">Garde-Fou SQL Actif (chk_child_group_price_never_higher_than_individual)</strong>
                      <div style="font-size:13px;" id="admChildGuardDesc">
                        Que vous créiez, modifiiez ou dupliquiez une prestation, le tarif enfant en groupe ne peut jamais dépasser le tarif individuel enfant (500 FCFA).
                      </div>
                    </div>
                  </div>
                  <span class="status-badge status-success" id="admChildGuardBadge">Conforme : Enfant = 500 FCFA</span>
                </div>
              </div>
            </div>

            <!-- ==============================================================
                 BLOC 2 : ADM-03 (JAUGES & MÉTÉO) & ADM-04 (MINI-CMS CRUD ZÉRO CODE)
                 ============================================================== -->
            <div class="grid-12" style="margin-bottom:22px;">
              <!-- ADM-03 : Quotas, Capacités & Météo Ahala -->
              <div class="col-5 card" id="sec-ADM-03">
                <span class="eyebrow" style="margin-bottom:2px;"><span class="tech-code-tag">ADM-03 • </span>Pilotage des Capacités &amp; Bandeau Météo RN3</span>
                <h3 style="margin-top:0;"><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><circle cx="12" cy="12" r="4"/></svg></span> <span class="tech-code-tag">ADM-03 — </span>Quotas, Stocks Loges &amp; Météo Directe</h3>

                <div style="margin-bottom:12px;padding:12px;border-radius:12px;background:#FBF5EC;border:1px solid rgba(196,125,43,0.35);">
                  <label class="form-label" for="admWeatherPresetSelect" style="font-size:13px;color:#8E5617;margin-bottom:6px;">
                    Bandeau Météo &amp; Trafic RN3 affiché en haut du site public :
                  </label>
                  <div style="display:flex;gap:8px;">
                    <select id="admWeatherPresetSelect" class="form-control" style="min-height:38px;font-size:13px;" onchange="admUpdateLiveWeatherBanner()">
                      <option value="SUNNY">27 °C Ensoleillé à Ahala Barrière • Accès RN3 Fluide</option>
                      <option value="RAIN_GUARANTEE">Averse Tropicale • Garantie Pluie (Report 90j Gratuit)</option>
                      <option value="WEEKEND_PEAK">Grand Dimanche Royal (29 °C) • Coupe-File Recommandé</option>
                    </select>
                    <button type="button" class="btn btn-primary btn-sm" onclick="admUpdateLiveWeatherBanner()">Publier</button>
                  </div>
                </div>

                <div class="adm-quota-row">
                  <div>
                    <strong>Cité Ewondo VIP (25 000 – 30 000 FCFA)</strong>
                    <div style="font-size:12px;color:var(--color-text-muted);">8 suites climatisées • Anti-surbooking actif</div>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;">
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admAdjustEwondoStock(-1)">-</button>
                    <strong id="admEwondoStockVal" style="min-width:86px;text-align:center;color:var(--color-brand-deep);">2 disponibles</strong>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admAdjustEwondoStock(1)">+</button>
                  </div>
                </div>

                <div class="adm-quota-row">
                  <div>
                    <strong>Pergolas Privées Bord du Lac (13h00)</strong>
                    <div style="font-size:12px;color:var(--color-text-muted);">10 pergolas • Précommande Saveurs</div>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;">
                    <span class="status-badge status-success" id="admPergolaStatusBadge">4 / 10 libres</span>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admTogglePoleStatus('PERGOLA')">Basculer Complet</button>
                  </div>
                </div>

                <div class="adm-quota-row" style="margin-bottom:0;">
                  <div>
                    <strong>Piscine Semi-Olympique &amp; Pirogues</strong>
                    <div style="font-size:12px;color:var(--color-text-muted);">Maître-nageur &amp; gilets contrôlés</div>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;">
                    <span class="status-badge status-success" id="admPoolStatusBadge">Ouvert (09h–18h)</span>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admTogglePoleStatus('POOL')">Maintenance</button>
                  </div>
                </div>
              </div>

              <!-- ADM-04 : Mini-CMS CRUD Zéro Code (Agenda & Restaurant) -->
              <div class="col-7 card" id="sec-ADM-04">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px;">
                  <div>
                    <span class="eyebrow" style="margin-bottom:2px;"><span class="tech-code-tag">ADM-04 • </span>Mini-CMS CRUD « Zéro Code HTML » (Agenda &amp; Saveurs)</span>
                    <h3 style="margin:0;"><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg></span> <span class="tech-code-tag">ADM-04 — </span>Gérer l'Agenda (/agenda) &amp; la Carte du Château des Saveurs</h3>
                  </div>
                  <button type="button" class="btn btn-primary btn-sm" onclick="admAddCmsItemPrompt()">+ Ajouter Événement / Plat</button>
                </div>

                <div id="admCmsListContainer">
                  <!-- Injecté dynamiquement par admRenderCmsList() avec boutons Modifier, Dupliquer, En stock/À la Une, Supprimer -->
                </div>

                <div style="background:var(--color-surface-soft);padding:10px 12px;border-radius:12px;border:1px solid rgba(29,73,13,0.14);margin-top:8px;">
                  <div style="font-size:12.2px;font-weight:700;color:var(--color-brand-deep);margin-bottom:6px;">
                    Ajout rapide à l'Agenda ou à la Carte du Restaurant (sans toucher au code HTML) :
                  </div>
                  <div style="display:grid;grid-template-columns:130px 1fr 115px auto;gap:6px;">
                    <select id="admQuickCmsType" class="form-control" style="min-height:36px;font-size:12.5px;padding:4px 8px;">
                      <option value="AGENDA">Agenda (/agenda)</option>
                      <option value="SAVEURS">Plat (/restaurant)</option>
                    </select>
                    <input type="text" id="admQuickEventTitle" class="form-control" style="min-height:36px;font-size:13px;" value="Samedi Grillades &amp; Balafon au Bord du Lac" />
                    <input type="text" id="admQuickEventPrice" class="form-control" style="min-height:36px;font-size:13px;" value="5 000 FCFA" />
                    <button type="button" class="btn btn-primary btn-sm" onclick="admPublishQuickAgendaUpdate()">+ Ajouter</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- ==============================================================
                 BLOC 3 : ADM-05 (CRUD ÉQUIPE 7 RÔLES RBAC) & ADM-06/07 (PASSERELLES)
                 ============================================================== -->
            <div class="grid-12" style="margin-bottom:22px;">
              <!-- ADM-05 : Utilisateurs Internes & Matrice des 7 Rôles -->
              <div class="col-7 card" id="sec-ADM-05">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px;">
                  <div>
                    <span class="eyebrow" style="margin-bottom:2px;"><span class="tech-code-tag">ADM-05 • </span>Gestion CRUD des Comptes Internes &amp; 7 Rôles (RBAC PostgreSQL)</span>
                    <h3 style="margin:0;"><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span> <span class="tech-code-tag">ADM-05 — </span>Comptes Nominatifs Équipe Ahala (Ajouter, Dupliquer Poste, Suspendre)</h3>
                  </div>
                  <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="admAddStaffMemberQuick()">+ Nouvel Agent / Compte</button>
                </div>
                <div class="table-responsive">
                  <table>
                    <thead>
                      <tr>
                        <th>Membre de l'Équipe / Poste</th>
                        <th>Rôle RBAC &amp; Périmètre Autorisé</th>
                        <th>Statut</th>
                        <th>Actions CRUD</th>
                      </tr>
                    </thead>
                    <tbody id="admStaffTbody">
                      <!-- Injecté dynamiquement par admRenderStaffTable() -->
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- ADM-06 & ADM-07 : Passerelles Paiement & Intégrations Sans Secrets Exposés -->
              <div class="col-5 card" id="sec-ADM-06">
                <div id="sec-ADM-07">
                  <span class="eyebrow" style="margin-bottom:2px;"><span class="tech-code-tag">ADM-06 &amp; ADM-07 • </span>Passerelles Marchandes &amp; Intégrations Serveur</span>
                  <h3 style="margin-top:0;"><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span> <span class="tech-code-tag">ADM-06 &amp; ADM-07 — </span>MTN MoMo, Orange Money &amp; WhatsApp (0 Secret Exposé)</h3>

                  <div class="adm-gateway-card">
                    <div>
                      <strong>Orange Money WebPay Cameroun</strong>
                      <div style="font-size:12px;color:var(--color-text-muted);">Clé Marchand Serveur : <span class="adm-secret-mask">••••••••••••9F2A</span></div>
                    </div>
                    <span class="status-badge status-success" id="admOmPingBadge">Webhook OK (16 ms)</span>
                  </div>

                  <div class="adm-gateway-card">
                    <div>
                      <strong>MTN MoMo Collection API</strong>
                      <div style="font-size:12px;color:var(--color-text-muted);">Clé Marchand Serveur : <span class="adm-secret-mask">••••••••••••4C81</span></div>
                    </div>
                    <span class="status-badge status-success" id="admMomoPingBadge">Webhook OK (19 ms)</span>
                  </div>

                  <div class="adm-gateway-card">
                    <div>
                      <strong>Guichet Unique WhatsApp Business</strong>
                      <div style="font-size:12px;color:var(--color-text-muted);">Numéro Centralisé : <strong>+237 697 13 62 03</strong> (5 lignes unifiées)</div>
                    </div>
                    <span class="status-badge status-success">Concierge Actif</span>
                  </div>

                  <div style="background:#FBF5EC;border:1px solid rgba(196,125,43,0.38);padding:12px 14px;border-radius:12px;margin-top:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
                      <div>
                        <strong style="font-size:13.5px;color:var(--color-brand-deep);">Environnement d'Encaissement :</strong>
                        <div style="font-size:12px;color:#8E5617;" id="admEnvModeDesc">Mode Démonstration Sécurisé (Aucun code PIN demandé sur le web)</div>
                      </div>
                      <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="admPingGateways()">
                        Tester Ping Webhooks
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- ==============================================================
                 BLOC 4 : ADM-08 — JOURNAL D'AUDIT IMMUABLE (PLEINE LARGEUR)
                 ============================================================== -->
            <div class="grid-12" id="sec-ADM-08">
              <div class="col-12 card">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:10px;">
                  <div>
                    <span class="eyebrow" style="margin-bottom:2px;"><span class="tech-code-tag">ADM-08 • </span>Traçabilité Comptable &amp; Opérationnelle Immuable</span>
                    <h3 style="margin:0;"><span class="icon-medallion"><svg class="svg-mono" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg></span> <span class="tech-code-tag">ADM-08 — </span>Journal d'Audit Immuable (Créations, Modifications, Duplications, Suppressions &amp; Scans QR)</h3>
                  </div>
                  <div class="adm-audit-filter-bar" style="margin-bottom:0;">
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admFilterAuditLogs('ALL')">Tout afficher</button>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admFilterAuditLogs('CRUD')">Actions CRUD</button>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admFilterAuditLogs('TARIF')">Tarifs &amp; Garde-Fou</button>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="admFilterAuditLogs('CAISSE')">Caisse &amp; Scans QR</button>
                  </div>
                </div>

                <div class="table-responsive">
                  <table id="admAuditLogTable">
                    <thead>
                      <tr>
                        <th>Horodatage</th>
                        <th>Acteur &amp; Rôle RBAC</th>
                        <th>Opération Enregistrée (Append-Only)</th>
                      </tr>
                    </thead>
                    <tbody id="admAuditLogTbody">
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>"""

ADM_CRUD_MODAL_HTML = """
  <!-- MODALE UNIVERSELLE CRUD ADMINISTRATION (AJOUTER / MODIFIER / DUPLIQUER UNE PRESTATION OU FORMULE) -->
  <div class="adm-crud-modal-overlay" id="modalAdmCrudBox" role="dialog" aria-modal="true" aria-labelledby="admCrudModalTitle" onclick="if(event.target.id==='modalAdmCrudBox') closeAdmCrudModal()">
    <div class="adm-crud-modal-card" onclick="event.stopPropagation()">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
        <span class="eyebrow" style="margin:0;" id="admCrudModalEyebrow">ADM-01 &amp; ADM-02 • Éditeur CRUD Structuré</span>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeAdmCrudModal()">Fermer</button>
      </div>
      <h3 style="margin-top:4px;margin-bottom:10px;" id="admCrudModalTitle">Modifier une Prestation du Catalogue ECOPARK</h3>

      <div class="modal-visual-preview-banner" style="margin-bottom:12px;">
        <img id="admCrudPreviewImg" src="audit-assets/ecopark-real-media/chimpanze.jpeg" alt="Aperçu visuel prestation" style="width:76px;height:58px;border-radius:10px;object-fit:cover;" />
        <div style="flex:1;font-size:12.5px;">
          <strong style="color:var(--color-brand-deep);display:block;" id="admCrudPreviewLabel">Visuel Certifié ECOPARK Yaoundé-Ahala</strong>
          <span style="color:var(--color-text-muted);">Aucun risque de déformation ni de page vide : le gabarit Canopée Vivante formate automatiquement la carte.</span>
        </div>
      </div>

      <input type="hidden" id="admCrudItemId" value="" />
      <div class="grid-12" style="gap:10px;">
        <div class="col-8 form-group" style="margin:0;">
          <label class="form-label" for="admCrudTitleInput">Intitulé officiel de la prestation ou du pack :</label>
          <input type="text" id="admCrudTitleInput" class="form-control" value="Entrée Parc &amp; Jardin Zoologique" />
        </div>
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="admCrudPoleSelect">Pôle de rattachement :</label>
          <select id="admCrudPoleSelect" class="form-control" onchange="admSyncCrudModalThumb()">
            <option value="NATURE_FAUNE">Nature &amp; Faune</option>
            <option value="EAU_PLEIN_AIR">Eau &amp; Loisirs</option>
            <option value="RESTAURATION">Château des Saveurs &amp; Packs</option>
            <option value="HEBERGEMENT">Cités Hôtelières</option>
          </select>
        </div>

        <div class="col-12 form-group" style="margin:0;">
          <label class="form-label" for="admCrudSubtitleInput">Description courte affichée sur la carte :</label>
          <input type="text" id="admCrudSubtitleInput" class="form-control" value="Pôle Nature &amp; Faune • Gorille « ToTo », tortues géantes, paons et allées botaniques" />
        </div>

        <div class="col-3 form-group" style="margin:0;">
          <label class="form-label" for="admCrudChildPrice">Enfant (FCFA) :</label>
          <input type="number" id="admCrudChildPrice" class="form-control" value="500" step="100" />
        </div>
        <div class="col-3 form-group" style="margin:0;">
          <label class="form-label" for="admCrudAdultPrice">Adulte (FCFA) :</label>
          <input type="number" id="admCrudAdultPrice" class="form-control" value="1000" step="100" />
        </div>
        <div class="col-3 form-group" style="margin:0;">
          <label class="form-label" for="admCrudGrpAdultPrice">Groupe Adulte :</label>
          <input type="number" id="admCrudGrpAdultPrice" class="form-control" value="700" step="100" />
        </div>
        <div class="col-3 form-group" style="margin:0;">
          <label class="form-label" for="admCrudGrpChildPrice">Groupe Enfant (Verrou) :</label>
          <input type="number" id="admCrudGrpChildPrice" class="form-control" value="500" step="100" style="background:#EDF4E7;border-color:#1D490D;font-weight:700;" />
        </div>

        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="admCrudQuotaInput">Capacité / Jour (places) :</label>
          <input type="number" id="admCrudQuotaInput" class="form-control" value="1200" step="10" />
        </div>
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="admCrudStatusSelect">Statut de publication :</label>
          <select id="admCrudStatusSelect" class="form-control">
            <option value="ACTIF">Actif en ligne</option>
            <option value="VEDETTE">Offre Vedette</option>
            <option value="BROUILLON">En pause / Brouillon</option>
          </select>
        </div>
        <div class="col-4 form-group" style="margin:0;">
          <label class="form-label" for="admCrudImgSelect">Visuel associé :</label>
          <select id="admCrudImgSelect" class="form-control" onchange="document.getElementById('admCrudPreviewImg').src = this.value">
            <option value="audit-assets/ecopark-real-media/chimpanze.jpeg">Faune &amp; Zoo (Réelle)</option>
            <option value="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png">Piscine &amp; Eau</option>
            <option value="audit-assets/ecopark-real-media/balade_pirogue3.jpg">Pirogue Lac Ahala (Réelle)</option>
            <option value="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png">Château des Saveurs</option>
            <option value="audit-assets/ecopark-real-media/chambre.jpeg">Loges Ewondo/Chanthel (Réelle)</option>
          </select>
        </div>
      </div>

      <div id="admCrudModalGuardAlert" style="margin-top:10px;padding:8px 12px;border-radius:8px;background:#EDF4E7;font-size:12.5px;color:var(--color-brand-deep);">
        • Garde-fou SQL actif : si vous saisissez un tarif Groupe Enfant supérieur au tarif Enfant individuel, il sera automatiquement plafonné.
      </div>

      <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-top:14px;padding-top:12px;border-top:1px solid var(--color-border);">
        <div style="display:flex;gap:8px;">
          <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" id="admCrudBtnDuplicateModal" onclick="admDuplicateFromModal()">
            Dupliquer cette fiche
          </button>
          <button type="button" class="btn btn-secondary btn-sm" id="admCrudBtnDeleteModal" style="color:#B3261E;border-color:rgba(179,38,30,0.35);" onclick="admDeleteFromModal()">
            Supprimer
          </button>
        </div>
        <div style="display:flex;gap:8px;">
          <button type="button" class="btn btn-secondary btn-sm" onclick="closeAdmCrudModal()">Annuler</button>
          <button type="button" class="btn btn-primary btn-sm" onclick="saveAdmCrudModal()">Enregistrer &amp; Publier</button>
        </div>
      </div>
    </div>
  </div>
"""

ADMIN_CONSOLE_JS = r"""
    // ========================================================================
    // MOTEUR CRUD COMPLET DE LA CONSOLE D'ADMINISTRATION (ADM-01 À ADM-08)
    // (Ajouter, Modifier, Dupliquer, Supprimer, Filtrer & Auditer)
    // ========================================================================
    window._admAuditFilter = 'ALL';
    window._admCurrentPoleFilter = 'ALL';

    const DEFAULT_ADM_CATALOG = [
      {
        id: 'CAT-ZOO',
        title: 'Entrée Parc & Jardin Zoologique',
        subtitle: 'Pôle Nature & Faune • Gorille « ToTo », tortues, paons',
        pole: 'NATURE_FAUNE',
        img: 'audit-assets/ecopark-real-media/chimpanze.jpeg',
        childPrice: 500,
        adultPrice: 1000,
        grpAdultPrice: 700,
        grpChildPrice: 500,
        quota: 1200,
        status: 'ACTIF',
        isCore: true
      },
      {
        id: 'CAT-POOL',
        title: 'Piscine Semi-Olympique Surveillée',
        subtitle: 'Pôle Eau & Loisirs • Semaine 1 500 F / Week-end 2 500 F',
        pole: 'EAU_PLEIN_AIR',
        img: 'audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png',
        childPrice: 1500,
        adultPrice: 2500,
        grpAdultPrice: 2000,
        grpChildPrice: 1500,
        quota: 300,
        status: 'ACTIF',
        isCore: true
      },
      {
        id: 'CAT-PIROGUE',
        title: 'Balade en Pirogue & Équitation (Tour à Cheval)',
        subtitle: 'Lac d’Ahala & Manèges • Gilets et encadrement inclus',
        pole: 'EAU_PLEIN_AIR',
        img: 'audit-assets/ecopark-real-media/balade_pirogue3.jpg',
        childPrice: 500,
        adultPrice: 1000,
        grpAdultPrice: 800,
        grpChildPrice: 500,
        quota: 250,
        status: 'ACTIF',
        isCore: false
      },
      {
        id: 'CAT-ROYALE',
        title: 'Pass Journée Royale Tout-Inclus (Zoo + Piscine + Pirogue + Repas)',
        subtitle: 'Bundling Phare B2C • Coupe-File QR + Précommande 13h',
        pole: 'RESTAURATION',
        img: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
        childPrice: 4500,
        adultPrice: 8500,
        grpAdultPrice: 7500,
        grpChildPrice: 4500,
        quota: 400,
        status: 'VEDETTE',
        isCore: false
      },
      {
        id: 'CAT-EWONDO',
        title: 'Cité Hôtelière Ewondo — Suite VIP Climatisée',
        subtitle: 'Hébergement Haut Standing • Petit-déjeuner & accès parc inclus',
        pole: 'HEBERGEMENT',
        img: 'audit-assets/ecopark-real-media/chambre.jpeg',
        childPrice: 0,
        adultPrice: 25000,
        grpAdultPrice: 25000,
        grpChildPrice: 0,
        quota: 8,
        status: 'ACTIF',
        isCore: false
      },
      {
        id: 'CAT-CHANTHEL',
        title: 'Cités Hôtelières Chanthel (15k) & Bene (10k)',
        subtitle: 'Pavillons Nature Confort & Détente au calme forestier d’Ahala',
        pole: 'HEBERGEMENT',
        img: 'audit-assets/ecopark-real-media/chambre.jpeg',
        childPrice: 0,
        adultPrice: 15000,
        grpAdultPrice: 12000,
        grpChildPrice: 0,
        quota: 22,
        status: 'ACTIF',
        isCore: false
      }
    ];

    const DEFAULT_ADM_CMS_ITEMS = [
      {
        id: 'CMS-EVT-1',
        kind: 'AGENDA',
        title: 'Agenda : Grand Dimanche Royal (Buffet & Live)',
        meta: 'Dimanche 10h00–18h00 • Pass Royale 8 500 FCFA / Enfant 4 500 FCFA',
        price: '8 500 FCFA',
        img: 'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg',
        badge: 'À la Une /agenda'
      },
      {
        id: 'CMS-SAV-1',
        kind: 'SAVEURS',
        title: 'Saveurs : Poisson Braisé Frais des Étangs d’Ahala',
        meta: 'Plantains mûrs, bâton de manioc & piment maison • Service 13h',
        price: '5 000 FCFA',
        img: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
        badge: 'En stock (13h)'
      },
      {
        id: 'CMS-EVT-2',
        kind: 'AGENDA',
        title: 'Agenda : Mercredi Pédagogique Écoles & Portes Ouvertes CFP',
        meta: 'Mercredi 09h00–16h30 • Tarif Enfant protégé à 500 FCFA',
        price: '500 FCFA',
        img: 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg',
        badge: 'Publié /agenda'
      }
    ];

    const DEFAULT_ADM_STAFF = [
      {
        id: 'USR-01',
        name: 'Dr Christophe FOE NDI',
        title: 'Promoteur ECOPARK',
        role: 'direction',
        scope: 'KPIs FCFA, Recettes MoMo/Guichet, Export CSV/PDF (/direction)',
        status: '2FA Actif'
      },
      {
        id: 'USR-02',
        name: 'M. Mgbatou Daryl',
        title: 'Gérant Délégué « NEW LOOK »',
        role: 'direction & exploitation',
        scope: 'Pilotage global, Validation Devis B2B & Admissions CFP',
        status: '2FA Actif'
      },
      {
        id: 'USR-03',
        name: 'Chef d’Exploitation Ahala',
        title: 'Supervision Réception & Saveurs',
        role: 'responsable_exploitation',
        scope: 'Planning Loges, Cuisine 13h, Console Closing WhatsApp (EXP-07)',
        status: 'Session Active'
      },
      {
        id: 'USR-04',
        name: 'Mme Clarisse ATANGANA',
        title: 'Caissière Principale Entrée RN3',
        role: 'agent_guichet',
        scope: 'Vente Walk-in, Clôture Caisse (Aucun accès modification tarifs)',
        status: 'Guichet #1'
      },
      {
        id: 'USR-05',
        name: 'Brigade Contrôle Tourniquet',
        title: 'Portail Principal & Bassin Piscine',
        role: 'agent_controle',
        scope: 'Scan QR 7 verdicts uniquement (Rejet auto double scan)',
        status: 'Terminal QR'
      },
      {
        id: 'USR-06',
        name: 'Administrateur Plateforme',
        title: 'Gouvernance & Support ONOGRAPH',
        role: 'administrateur_plateforme',
        scope: 'CRUD Catalogue FCFA, Quotas, Mini-CMS, Passerelles & Audit (/admin)',
        status: 'Clé Matérielle'
      }
    ];

    function admGetState() {
      const db = loadDB();
      if (!db.admCatalog || !Array.isArray(db.admCatalog) || db.admCatalog.length === 0) {
        db.admCatalog = JSON.parse(JSON.stringify(DEFAULT_ADM_CATALOG));
      }
      if (!db.admCmsItems || !Array.isArray(db.admCmsItems) || db.admCmsItems.length === 0) {
        db.admCmsItems = JSON.parse(JSON.stringify(DEFAULT_ADM_CMS_ITEMS));
      }
      if (!db.admStaff || !Array.isArray(db.admStaff) || db.admStaff.length === 0) {
        db.admStaff = JSON.parse(JSON.stringify(DEFAULT_ADM_STAFF));
      }
      saveDB(db);
      return db;
    }

    function admAppendAuditLog(actor, actionText) {
      const db = loadDB();
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: actor,
        action: actionText
      });
      saveDB(db);
      admRenderAuditTable();
    }

    // ------------------------------------------------------------------------
    // 1. CRUD CATALOGUE & GRILLE TARIFAIRE FCFA (ADM-01 & ADM-02)
    // ------------------------------------------------------------------------
    function admFilterCatalogByPole(pole, btnEl) {
      window._admCurrentPoleFilter = pole || 'ALL';
      document.querySelectorAll('#admPoleFilterPills .adm-pole-pill').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      admRenderCatalogTable();
    }

    function admRenderCatalogTable() {
      const db = admGetState();
      const tbody = document.getElementById('admCatalogTbody');
      if (!tbody) return;
      const poleFilter = window._admCurrentPoleFilter || 'ALL';
      const searchEl = document.getElementById('admCatalogSearchInput');
      const q = (searchEl && searchEl.value) ? searchEl.value.trim().toLowerCase() : '';

      const items = db.admCatalog.filter(item => {
        if (poleFilter !== 'ALL' && item.pole !== poleFilter) return false;
        if (q && !(item.title.toLowerCase().includes(q) || item.subtitle.toLowerCase().includes(q))) return false;
        return true;
      });

      const allPill = document.querySelector('#admPoleFilterPills .adm-pole-pill');
      if (allPill) allPill.textContent = `Tous les pôles (${db.admCatalog.length})`;
      const kpiCat = document.getElementById('admCatalogCountKpi');
      if (kpiCat) kpiCat.textContent = `${db.admCatalog.length} Prestations FCFA`;

      tbody.innerHTML = items.map(item => {
        let statusBadge = `<span class="status-badge status-success" style="cursor:pointer;" onclick="admToggleCatalogItemStatus('${item.id}')" title="Cliquer pour basculer Actif / Brouillon">Actif en ligne</span>`;
        if (item.status === 'VEDETTE') {
          statusBadge = `<span class="price-pill" style="font-size:11.5px;padding:2px 8px;cursor:pointer;" onclick="admToggleCatalogItemStatus('${item.id}')">Offre Vedette</span>`;
        } else if (item.status === 'BROUILLON') {
          statusBadge = `<span class="status-badge status-warning" style="cursor:pointer;" onclick="admToggleCatalogItemStatus('${item.id}')">Copie • Brouillon</span>`;
        }
        const rowClass = item.isDuplicated ? ' class="adm-row-duplicated"' : '';
        return `
          <tr${rowClass} data-adm-cat-id="${item.id}">
            <td>
              <div style="display:flex;align-items:center;gap:10px;">
                <img src="${item.img}" alt="${item.title}" style="width:40px;height:40px;border-radius:8px;object-fit:cover;flex-shrink:0;" />
                <div>
                  <strong>${item.title}</strong>
                  <div style="font-size:11.8px;color:var(--color-text-muted);">${item.subtitle}</div>
                </div>
              </div>
            </td>
            <td><div class="adm-price-cell"><input type="number" class="adm-input-fcfa" value="${item.childPrice}" step="100" onchange="admInlinePriceEdit('${item.id}', 'childPrice', this.value)" /> <span style="font-size:11.5px;">F</span></div></td>
            <td><div class="adm-price-cell"><input type="number" class="adm-input-fcfa" value="${item.adultPrice}" step="100" onchange="admInlinePriceEdit('${item.id}', 'adultPrice', this.value)" /> <span style="font-size:11.5px;">F</span></div></td>
            <td><div class="adm-price-cell"><input type="number" class="adm-input-fcfa" value="${item.grpAdultPrice}" step="100" onchange="admInlinePriceEdit('${item.id}', 'grpAdultPrice', this.value)" /> <span style="font-size:11.5px;">F</span></div></td>
            <td><div class="adm-price-cell"><input type="number" class="adm-input-fcfa locked-child" value="${item.grpChildPrice}" step="100" onchange="admInlinePriceEdit('${item.id}', 'grpChildPrice', this.value)" /> <span style="font-size:11px;font-weight:700;color:var(--color-brand-deep);">Max ${item.childPrice} F</span></div></td>
            <td><strong>${item.quota} pl.</strong></td>
            <td>${statusBadge}</td>
            <td>
              <div class="adm-crud-actions">
                <button type="button" class="adm-action-btn" onclick="openAdmCrudModal('EDIT', '${item.id}')" title="Modifier cette prestation">
                  <svg class="svg-mono" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg> Modifier
                </button>
                <button type="button" class="adm-action-btn duplicate" onclick="admDuplicateCatalogItem('${item.id}')" title="Dupliquer cette prestation en 1 clic">
                  <svg class="svg-mono" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg> Dupliquer
                </button>
                <button type="button" class="adm-action-btn danger" onclick="admDeleteCatalogItem('${item.id}')" title="Supprimer ou archiver cette prestation">
                  <svg class="svg-mono" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg> Suppr.
                </button>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    function admInlinePriceEdit(itemId, field, rawVal) {
      const db = admGetState();
      const item = db.admCatalog.find(x => x.id === itemId);
      if (!item) return;
      const num = Math.max(0, parseInt(rawVal, 10) || 0);
      if (field === 'grpChildPrice' && num > item.childPrice) {
        admTestChildPriceViolation();
        admRenderCatalogTable();
        return;
      }
      item[field] = num;
      if (field === 'childPrice' && item.grpChildPrice > num) {
        item.grpChildPrice = num;
      }
      saveDB(db);
      admRenderCatalogTable();
      admAppendAuditLog('Admin Plateforme (ADM-02)', `Modification tarifaire en ligne sur « ${item.title} » (${field} = ${formatFCFA(num)}).`);
      showToastSprint1(`• Tarif mis à jour sur « ${item.title} » : ${formatFCFA(num)}`);
    }

    function admToggleCatalogItemStatus(itemId) {
      const db = admGetState();
      const item = db.admCatalog.find(x => x.id === itemId);
      if (!item) return;
      item.status = (item.status === 'ACTIF' || item.status === 'VEDETTE') ? 'BROUILLON' : 'ACTIF';
      saveDB(db);
      admRenderCatalogTable();
      admAppendAuditLog('Admin Plateforme (ADM-01)', `Changement de statut de « ${item.title} » -> ${item.status}.`);
      showToastSprint1(`• Statut de « ${item.title} » basculé sur : ${item.status}`);
    }

    function admDuplicateCatalogItem(itemId) {
      const db = admGetState();
      const idx = db.admCatalog.findIndex(x => x.id === itemId);
      if (idx === -1) return null;
      const src = db.admCatalog[idx];
      const copyId = 'CAT-COPY-' + Math.floor(100 + Math.random() * 899);
      const clone = {
        id: copyId,
        title: src.title + ' (Copie — Promo Vacances)',
        subtitle: src.subtitle,
        pole: src.pole,
        img: src.img,
        childPrice: src.childPrice,
        adultPrice: src.adultPrice,
        grpAdultPrice: src.grpAdultPrice,
        grpChildPrice: src.grpChildPrice,
        quota: src.quota,
        status: 'BROUILLON',
        isCore: false,
        isDuplicated: true
      };
      db.admCatalog.splice(idx + 1, 0, clone);
      saveDB(db);
      admRenderCatalogTable();
      admAppendAuditLog(
        'Admin Plateforme (CRUD ADM-01)',
        `DUPLICATION en 1 clic de « ${src.title} » -> création de « ${clone.title} » (${copyId}) en mode Brouillon.`
      );
      showToastSprint1(`• Prestation dupliquée : « ${clone.title} » créée en mode Brouillon !`);
      return copyId;
    }

    function admDeleteCatalogItem(itemId) {
      const db = admGetState();
      const item = db.admCatalog.find(x => x.id === itemId);
      if (!item) return false;
      if (item.isCore) {
        admAppendAuditLog(
          'Protection Métier (CRUD ADM-01)',
          `Suppression directe refusée sur la prestation socle « ${item.title} » (billets QR actifs). Basculez-la en mode Pause/Brouillon si nécessaire.`
        );
        showToastSprint1(`• Garde-Fou CRUD : « ${item.title} » a des billets QR actifs. Utilisez le statut « En pause » plutôt que la suppression définitive.`);
        return false;
      }
      db.admCatalog = db.admCatalog.filter(x => x.id !== itemId);
      saveDB(db);
      admRenderCatalogTable();
      admAppendAuditLog(
        'Admin Plateforme (CRUD ADM-01)',
        `SUPPRESSION de la prestation « ${item.title} » (${itemId}) du catalogue.`
      );
      showToastSprint1(`• Prestation « ${item.title} » supprimée et tracée dans le Journal d'Audit.`);
      return true;
    }

    // ------------------------------------------------------------------------
    // MODALE UNIVERSELLE D'AJOUT / ÉDITION (openAdmCrudModal / saveAdmCrudModal)
    // ------------------------------------------------------------------------
    function openAdmCrudModal(mode, itemId) {
      const db = admGetState();
      const modal = document.getElementById('modalAdmCrudBox');
      if (!modal) return;
      const item = itemId ? db.admCatalog.find(x => x.id === itemId) : null;

      document.getElementById('admCrudItemId').value = item ? item.id : '';
      document.getElementById('admCrudModalTitle').textContent = item
        ? `Modifier : ${item.title}`
        : 'Ajouter une Nouvelle Prestation / Formule au Catalogue';
      document.getElementById('admCrudTitleInput').value = item ? item.title : 'Pack Week-end Détente & Pirogue Royale';
      document.getElementById('admCrudSubtitleInput').value = item ? item.subtitle : 'Nouvelle formule combinée ECOPARK Ahala • Billet QR Coupe-File inclus';
      document.getElementById('admCrudPoleSelect').value = item ? item.pole : 'EAU_PLEIN_AIR';
      document.getElementById('admCrudChildPrice').value = item ? item.childPrice : 500;
      document.getElementById('admCrudAdultPrice').value = item ? item.adultPrice : 3500;
      document.getElementById('admCrudGrpAdultPrice').value = item ? item.grpAdultPrice : 3000;
      document.getElementById('admCrudGrpChildPrice').value = item ? item.grpChildPrice : 500;
      document.getElementById('admCrudQuotaInput').value = item ? item.quota : 150;
      document.getElementById('admCrudStatusSelect').value = item ? item.status : 'ACTIF';
      const imgVal = item ? item.img : 'audit-assets/ecopark-real-media/balade_pirogue3.jpg';
      document.getElementById('admCrudImgSelect').value = imgVal;
      document.getElementById('admCrudPreviewImg').src = imgVal;

      const btnDup = document.getElementById('admCrudBtnDuplicateModal');
      const btnDel = document.getElementById('admCrudBtnDeleteModal');
      if (btnDup) btnDup.style.display = item ? 'inline-flex' : 'none';
      if (btnDel) btnDel.style.display = item ? 'inline-flex' : 'none';

      modal.classList.add('open');
    }

    function closeAdmCrudModal() {
      const modal = document.getElementById('modalAdmCrudBox');
      if (modal) modal.classList.remove('open');
    }

    function admSyncCrudModalThumb() {
      const pole = document.getElementById('admCrudPoleSelect').value;
      const map = {
        NATURE_FAUNE: 'audit-assets/ecopark-real-media/chimpanze.jpeg',
        EAU_PLEIN_AIR: 'audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png',
        RESTAURATION: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
        HEBERGEMENT: 'audit-assets/ecopark-real-media/chambre.jpeg'
      };
      const img = map[pole] || map.NATURE_FAUNE;
      document.getElementById('admCrudImgSelect').value = img;
      document.getElementById('admCrudPreviewImg').src = img;
    }

    function saveAdmCrudModal() {
      const db = admGetState();
      const id = document.getElementById('admCrudItemId').value.trim();
      const title = document.getElementById('admCrudTitleInput').value.trim() || 'Nouvelle Prestation ECOPARK';
      const subtitle = document.getElementById('admCrudSubtitleInput').value.trim() || 'Prestation officielle ECOPARK Yaoundé-Ahala';
      const pole = document.getElementById('admCrudPoleSelect').value;
      const childPrice = Math.max(0, parseInt(document.getElementById('admCrudChildPrice').value, 10) || 0);
      const adultPrice = Math.max(0, parseInt(document.getElementById('admCrudAdultPrice').value, 10) || 0);
      const grpAdultPrice = Math.max(0, parseInt(document.getElementById('admCrudGrpAdultPrice').value, 10) || 0);
      let grpChildPrice = Math.max(0, parseInt(document.getElementById('admCrudGrpChildPrice').value, 10) || 0);
      const quota = Math.max(1, parseInt(document.getElementById('admCrudQuotaInput').value, 10) || 100);
      const status = document.getElementById('admCrudStatusSelect').value;
      const img = document.getElementById('admCrudImgSelect').value;

      if (grpChildPrice > childPrice) {
        grpChildPrice = childPrice;
        admTestChildPriceViolation();
      }

      if (id) {
        const existing = db.admCatalog.find(x => x.id === id);
        if (existing) {
          existing.title = title;
          existing.subtitle = subtitle;
          existing.pole = pole;
          existing.childPrice = childPrice;
          existing.adultPrice = adultPrice;
          existing.grpAdultPrice = grpAdultPrice;
          existing.grpChildPrice = grpChildPrice;
          existing.quota = quota;
          existing.status = status;
          existing.img = img;
        }
        saveDB(db);
        admRenderCatalogTable();
        admAppendAuditLog('Admin Plateforme (CRUD ADM-01)', `MODIFICATION de la fiche « ${title} » (Adulte: ${formatFCFA(adultPrice)}, Enfant: ${formatFCFA(childPrice)}).`);
        showToastSprint1(`• Fiche « ${title} » modifiée et publiée !`);
      } else {
        const newId = 'CAT-NEW-' + Math.floor(100 + Math.random() * 899);
        db.admCatalog.unshift({
          id: newId,
          title,
          subtitle,
          pole,
          img,
          childPrice,
          adultPrice,
          grpAdultPrice,
          grpChildPrice,
          quota,
          status,
          isCore: false,
          isDuplicated: true
        });
        saveDB(db);
        admRenderCatalogTable();
        admAppendAuditLog('Admin Plateforme (CRUD ADM-01)', `AJOUT d'une nouvelle prestation « ${title} » (${newId} • ${formatFCFA(adultPrice)}).`);
        showToastSprint1(`• Nouvelle prestation « ${title} » ajoutée au catalogue !`);
      }
      closeAdmCrudModal();
    }

    function admDuplicateFromModal() {
      const id = document.getElementById('admCrudItemId').value.trim();
      closeAdmCrudModal();
      if (id) admDuplicateCatalogItem(id);
    }

    function admDeleteFromModal() {
      const id = document.getElementById('admCrudItemId').value.trim();
      closeAdmCrudModal();
      if (id) admDeleteCatalogItem(id);
    }

    // ------------------------------------------------------------------------
    // 2. MINI-CMS CRUD : AGENDA (/agenda) & CHÂTEAU DES SAVEURS (ADM-04)
    // ------------------------------------------------------------------------
    function admRenderCmsList() {
      const db = admGetState();
      const box = document.getElementById('admCmsListContainer');
      if (!box) return;
      box.innerHTML = db.admCmsItems.map(item => `
        <div class="adm-cms-item" data-cms-id="${item.id}">
          <div style="display:flex;align-items:center;gap:10px;flex:1;min-width:240px;">
            <img src="${item.img}" alt="${item.title}" />
            <div>
              <strong>${item.title}</strong>
              <div style="font-size:11.8px;color:var(--color-text-muted);">${item.meta} • <strong style="color:var(--color-brand-deep);">${item.price}</strong></div>
            </div>
          </div>
          <div class="adm-crud-actions">
            <span class="price-pill" style="font-size:11px;padding:2px 8px;cursor:pointer;" onclick="admToggleCmsBadge('${item.id}')">${item.badge}</span>
            <button type="button" class="adm-action-btn" onclick="admEditCmsItem('${item.id}')">Modifier</button>
            <button type="button" class="adm-action-btn duplicate" onclick="admDuplicateCmsItem('${item.id}')">Dupliquer</button>
            <button type="button" class="adm-action-btn danger" onclick="admDeleteCmsItem('${item.id}')">Suppr.</button>
          </div>
        </div>
      `).join('');
    }

    function admToggleCmsBadge(cmsId) {
      const db = admGetState();
      const item = db.admCmsItems.find(x => x.id === cmsId);
      if (!item) return;
      if (item.kind === 'SAVEURS') {
        item.badge = item.badge.includes('En stock') ? 'Épuisé ce midi' : 'En stock (13h)';
      } else {
        item.badge = item.badge.includes('À la Une') ? 'Archivé / Brouillon' : 'À la Une /agenda';
      }
      saveDB(db);
      admRenderCmsList();
      admAppendAuditLog('CMS Éditorial (CRUD ADM-04)', `Changement d'état sur « ${item.title} » -> ${item.badge}.`);
      showToastSprint1(`• Statut mis à jour : « ${item.title} » (${item.badge})`);
    }

    function admEditCmsItem(cmsId) {
      const db = admGetState();
      const item = db.admCmsItems.find(x => x.id === cmsId);
      if (!item) return;
      document.getElementById('admQuickCmsType').value = item.kind;
      document.getElementById('admQuickEventTitle').value = item.title;
      document.getElementById('admQuickEventPrice').value = item.price;
      document.getElementById('admQuickEventTitle').focus();
      showToastSprint1(`• Édition chargée dans le formulaire rapide : modifiez le titre ou le prix puis cliquez sur « + Ajouter / Mettre à jour ».`);
    }

    function admDuplicateCmsItem(cmsId) {
      const db = admGetState();
      const idx = db.admCmsItems.findIndex(x => x.id === cmsId);
      if (idx === -1) return;
      const src = db.admCmsItems[idx];
      const clone = {
        id: 'CMS-COPY-' + Math.floor(100 + Math.random() * 899),
        kind: src.kind,
        title: src.title + ' (Copie)',
        meta: src.meta,
        price: src.price,
        img: src.img,
        badge: 'Brouillon'
      };
      db.admCmsItems.splice(idx + 1, 0, clone);
      saveDB(db);
      admRenderCmsList();
      admAppendAuditLog('CMS Éditorial (CRUD ADM-04)', `DUPLICATION de l'élément CMS « ${src.title} » -> « ${clone.title} ».`);
      showToastSprint1(`• Élément CMS dupliqué : « ${clone.title} » !`);
    }

    function admDeleteCmsItem(cmsId) {
      const db = admGetState();
      const item = db.admCmsItems.find(x => x.id === cmsId);
      if (!item) return;
      db.admCmsItems = db.admCmsItems.filter(x => x.id !== cmsId);
      saveDB(db);
      admRenderCmsList();
      admAppendAuditLog('CMS Éditorial (CRUD ADM-04)', `SUPPRESSION de l'élément CMS « ${item.title} ».`);
      showToastSprint1(`• Élément « ${item.title} » supprimé.`);
    }

    function admAddCmsItemPrompt() {
      const input = document.getElementById('admQuickEventTitle');
      if (input) input.focus();
      admPublishQuickAgendaUpdate();
    }

    function admPublishQuickAgendaUpdate() {
      const db = admGetState();
      const kindEl = document.getElementById('admQuickCmsType');
      const titleEl = document.getElementById('admQuickEventTitle');
      const priceEl = document.getElementById('admQuickEventPrice');
      const kind = kindEl ? kindEl.value : 'AGENDA';
      const t = titleEl ? titleEl.value.trim() : 'Nouvel Événement Ahala';
      const p = priceEl ? priceEl.value.trim() : '5 000 FCFA';
      const newItem = {
        id: 'CMS-' + Math.floor(100 + Math.random() * 899),
        kind,
        title: (kind === 'AGENDA' ? 'Agenda : ' : 'Saveurs : ') + t.replace(/^(Agenda|Saveurs)\s*:\s*/i, ''),
        meta: kind === 'AGENDA' ? 'Programmation Hebdomadaire • Billet QR Coupe-File' : 'Spécialité Château des Saveurs • Précommande 13h',
        price: p,
        img: kind === 'AGENDA' ? 'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg' : 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
        badge: kind === 'AGENDA' ? 'Publié /agenda' : 'En stock (13h)'
      };
      db.admCmsItems.unshift(newItem);
      saveDB(db);
      admRenderCmsList();
      admAppendAuditLog('CMS Éditorial (CRUD ADM-04)', `AJOUT CMS (${kind}) : « ${newItem.title} » (${p}).`);
      showToastSprint1(`• « ${newItem.title} » (${p}) ajouté et publié !`);
    }

    // ------------------------------------------------------------------------
    // 3. CRUD COMPTES ÉQUIPE AHALA & 7 RÔLES RBAC (ADM-05)
    // ------------------------------------------------------------------------
    function admRenderStaffTable() {
      const db = admGetState();
      const tbody = document.getElementById('admStaffTbody');
      if (!tbody) return;
      const kpiUsers = document.getElementById('admUsersCountKpi');
      if (kpiUsers) kpiUsers.textContent = `${db.admStaff.length} Comptes (7 Rôles)`;

      tbody.innerHTML = db.admStaff.map(u => {
        const badgeCls = u.status === 'Suspendu' ? 'status-warning' : (u.status.includes('2FA') || u.status.includes('Active') || u.status.includes('Matérielle') ? 'status-success' : 'status-info');
        return `
          <tr>
            <td><strong>${u.name}</strong><div style="font-size:11.8px;color:var(--color-text-muted);">${u.title}</div></td>
            <td><code>${u.role}</code><div style="font-size:11.8px;color:var(--color-text-muted);margin-top:2px;">${u.scope}</div></td>
            <td><span class="status-badge ${badgeCls}">${u.status}</span></td>
            <td>
              <div class="adm-crud-actions">
                <button type="button" class="adm-action-btn duplicate" onclick="admDuplicateStaffMember('${u.id}')" title="Dupliquer ce profil de poste">Dupliquer</button>
                <button type="button" class="adm-action-btn" onclick="admToggleStaffStatus('${u.id}')" title="Suspendre ou réactiver cet accès">${u.status === 'Suspendu' ? 'Activer' : 'Suspendre'}</button>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    function admDuplicateStaffMember(userId) {
      const db = admGetState();
      const idx = db.admStaff.findIndex(x => x.id === userId);
      if (idx === -1) return;
      const src = db.admStaff[idx];
      const clone = {
        id: 'USR-' + Math.floor(100 + Math.random() * 899),
        name: src.name + ' (Poste Renfort #2)',
        title: src.title + ' — Vacation Week-end',
        role: src.role,
        scope: src.scope,
        status: 'Guichet #2 Actif'
      };
      db.admStaff.splice(idx + 1, 0, clone);
      saveDB(db);
      admRenderStaffTable();
      admAppendAuditLog('Gouvernance RBAC (CRUD ADM-05)', `DUPLICATION du profil de poste « ${src.name} » (${src.role}) -> création de « ${clone.name} ».`);
      showToastSprint1(`• Poste dupliqué : « ${clone.name} » créé avec le rôle ${clone.role} !`);
    }

    function admToggleStaffStatus(userId) {
      const db = admGetState();
      const u = db.admStaff.find(x => x.id === userId);
      if (!u) return;
      u.status = (u.status === 'Suspendu') ? 'Session Active' : 'Suspendu';
      saveDB(db);
      admRenderStaffTable();
      admAppendAuditLog('Gouvernance RBAC (CRUD ADM-05)', `Statut du compte « ${u.name} » (${u.role}) basculé sur : ${u.status}.`);
      showToastSprint1(`• Compte « ${u.name} » : ${u.status}`);
    }

    function admAddStaffMemberQuick() {
      const db = admGetState();
      const newStaff = {
        id: 'USR-' + Math.floor(100 + Math.random() * 899),
        name: 'M. Samuel ESSOMBA (Renfort Dimanche)',
        title: 'Agent Contrôle Tourniquet Piscine & Lac',
        role: 'agent_controle',
        scope: 'Scan QR 7 verdicts uniquement (Aucun droit sur les tarifs)',
        status: 'Terminal QR #2'
      };
      db.admStaff.unshift(newStaff);
      saveDB(db);
      admRenderStaffTable();
      admAppendAuditLog('Gouvernance RBAC (CRUD ADM-05)', `AJOUT d'un nouveau compte agent : « ${newStaff.name} » (rôle : ${newStaff.role}).`);
      showToastSprint1(`• Nouveau compte « ${newStaff.name} » ajouté avec succès !`);
    }

    // ------------------------------------------------------------------------
    // 4. JOURNAL D'AUDIT IMMUABLE & CONTRÔLES (ADM-02, ADM-03, ADM-07, ADM-08)
    // ------------------------------------------------------------------------
    function admRenderAuditTable() {
      const db = loadDB();
      const tbody = document.getElementById('admAuditLogTbody');
      if (!tbody) return;
      const filter = window._admAuditFilter || 'ALL';
      const filtered = (db.auditLogs || []).filter(item => {
        const txt = (item.actor + ' ' + item.action).toUpperCase();
        if (filter === 'CRUD') return txt.includes('CRUD') || txt.includes('DUPLICATION') || txt.includes('AJOUT') || txt.includes('MODIFICATION') || txt.includes('SUPPRESSION');
        if (filter === 'TARIF') return txt.includes('TARIF') || txt.includes('500 FCFA') || txt.includes('GARDE-FOU') || txt.includes('GRILLE');
        if (filter === 'CAISSE') return txt.includes('CAISSE') || txt.includes('GUICHET') || txt.includes('QR') || txt.includes('BILLET') || txt.includes('SCAN');
        return true;
      });
      tbody.innerHTML = filtered.slice(0, 8).map(log => `
        <tr>
          <td>${log.time}</td>
          <td><strong>${log.actor}</strong></td>
          <td>${log.action}</td>
        </tr>
      `).join('');
      const kpiEl = document.getElementById('admAuditCountKpi');
      if (kpiEl) kpiEl.textContent = `${db.auditLogs.length} événements tracés`;
    }

    function admFilterAuditLogs(category) {
      window._admAuditFilter = category || 'ALL';
      admRenderAuditTable();
      showToastSprint1(`• Filtre Journal d'Audit ADM-08 : ${category}`);
    }

    function admTestChildPriceViolation() {
      const bannerEl = document.getElementById('admChildGuardBanner');
      const titleEl = document.getElementById('admChildGuardTitle');
      const descEl = document.getElementById('admChildGuardDesc');
      const badgeEl = document.getElementById('admChildGuardBadge');
      if (bannerEl) bannerEl.classList.add('rejected');
      if (titleEl) titleEl.textContent = 'ALERTE SÉCURITÉ ADM-02 : Saisie 700 FCFA Rejetée par la Contrainte SQL';
      if (descEl) descEl.textContent = 'Violation bloquée (chk_child_group_price_never_higher_than_individual) : le tarif enfant en groupe a été automatiquement restauré à 500 FCFA.';
      if (badgeEl) {
        badgeEl.className = 'status-badge status-error';
        badgeEl.textContent = 'Bloqué : Maintenu à 500 FCFA';
      }
      admAppendAuditLog(
        'Système Garde-Fou SQL (ADM-02)',
        'Tentative de hausser le tarif Enfant Groupe à 700 FCFA rejetée automatiquement. Tarif Enfant maintenu à 500 FCFA.'
      );
      showToastSprint1('• Garde-Fou ADM-02 déclenché : Saisie 700 FCFA bloquée, tarif enfant restauré à 500 FCFA !');
    }

    function admSaveCatalogPrices() {
      const bannerEl = document.getElementById('admChildGuardBanner');
      const titleEl = document.getElementById('admChildGuardTitle');
      const descEl = document.getElementById('admChildGuardDesc');
      const badgeEl = document.getElementById('admChildGuardBadge');
      if (bannerEl) bannerEl.classList.remove('rejected');
      if (titleEl) titleEl.textContent = 'Garde-Fou SQL Actif (chk_child_group_price_never_higher_than_individual)';
      if (descEl) descEl.textContent = 'Grille tarifaire vérifiée et synchronisée en Francs CFA sur le simulateur et le guichet.';
      if (badgeEl) {
        badgeEl.className = 'status-badge status-success';
        badgeEl.textContent = 'Conforme : Enfant = 500 FCFA';
      }
      admAppendAuditLog(
        'Admin Plateforme (ADM-01/02)',
        'Publication de la grille tarifaire officielle en FCFA (Zoo 500/1 000 F, Piscine 1 500/2 500 F, Pass Royale 8 500 F).'
      );
      showToastSprint1('• Grille tarifaire FCFA vérifiée et synchronisée avec succès !');
      return true;
    }

    function admUpdateLiveWeatherBanner() {
      const sel = document.getElementById('admWeatherPresetSelect');
      const val = sel ? sel.value : 'SUNNY';
      const weatherTextEl = document.querySelector('#ahalaLiveWeatherBar span');
      let label = 'En direct d’Ahala Barrière (RN3 Face Tradex) : 27 °C Ensoleillé • Accès RN3 Fluide';
      if (val === 'RAIN_GUARANTEE') {
        label = 'Météo Ahala Barrière : Averse Tropicale Passagère • Garantie Pluie Active (Report 90j Gratuit en 1 Clic)';
      } else if (val === 'WEEKEND_PEAK') {
        label = 'Grand Dimanche Royal à Ahala (29 °C Ensoleillé) • Forte Affluence : Billet QR Coupe-File Recommandé';
      }
      if (weatherTextEl) weatherTextEl.textContent = label;
      admAppendAuditLog('Exploitation / Admin (ADM-03)', `Mise à jour du bandeau météo & trafic RN3 en direct : « ${label} ».`);
      showToastSprint1('• Bandeau météo & trafic RN3 mis à jour en direct sur le site public !');
    }

    function admAdjustEwondoStock(delta) {
      const db = loadDB();
      if (!db.opsMetrics) db.opsMetrics = { kitchenPreorders: 18, pergolasReserved: 6, fishPacks: 34, ewondoFree: 2 };
      db.opsMetrics.ewondoFree = Math.max(0, Math.min(8, (db.opsMetrics.ewondoFree || 2) + delta));
      saveDB(db);
      const el = document.getElementById('admEwondoStockVal');
      if (el) el.textContent = `${db.opsMetrics.ewondoFree} disponible(s)`;
      syncAllViewsFromDB();
      admAppendAuditLog('Admin / Réception Hôtels (ADM-03)', `Ajustement stock Cité Ewondo VIP : ${db.opsMetrics.ewondoFree} suite(s) disponible(s) sur 8.`);
      showToastSprint1(`• Stock Cité Ewondo VIP mis à jour : ${db.opsMetrics.ewondoFree} suite(s) disponible(s).`);
    }

    function admTogglePoleStatus(poleCode) {
      if (poleCode === 'PERGOLA') {
        const b = document.getElementById('admPergolaStatusBadge');
        if (b) {
          const isFull = b.textContent.includes('Complet');
          b.textContent = isFull ? '4 / 10 libres' : 'Complet (10/10)';
          b.className = isFull ? 'status-badge status-success' : 'status-badge status-warning';
          admAppendAuditLog('Admin Plateforme (ADM-03)', `Statut Pergolas du Lac basculé sur : ${b.textContent}.`);
        }
      } else if (poleCode === 'POOL') {
        const b = document.getElementById('admPoolStatusBadge');
        if (b) {
          const isMaint = b.textContent.includes('Maintenance');
          b.textContent = isMaint ? 'Ouvert (09h–18h)' : 'Maintenance / Orage';
          b.className = isMaint ? 'status-badge status-success' : 'status-badge status-warning';
          admAppendAuditLog('Admin Plateforme (ADM-03)', `Statut Piscine Semi-Olympique basculé sur : ${b.textContent}.`);
        }
      }
    }

    function admPingGateways() {
      const om = document.getElementById('admOmPingBadge');
      const momo = document.getElementById('admMomoPingBadge');
      if (om) om.textContent = 'Webhook OK (14 ms)';
      if (momo) momo.textContent = 'Webhook OK (17 ms)';
      admAppendAuditLog('Sécurité Passerelles (ADM-07)', 'Test de connectivité signé réussi : Orange Money WebPay (14 ms) & MTN MoMo Collection (17 ms).');
      showToastSprint1('• Passerelles Orange Money (14 ms) & MTN MoMo (17 ms) opérationnelles !');
    }

    // Initialiser les tableaux CRUD au démarrage
    admRenderCatalogTable();
    admRenderCmsList();
    admRenderStaffTable();
    admRenderAuditTable();
"""


def build_and_capture():
    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Injecter le CSS de la console d'administration CRUD
    if "CONSOLE D'ADMINISTRATION & MOTEUR CRUD METIER" not in html:
        html = html.replace("</style>", ADMIN_CONSOLE_CSS + "\n  </style>", 1)

    # 2. Remplacer la section #view-ADM par la Console d'Administration CRUD complète (ADM-01 à ADM-08)
    old_adm_pattern = re.compile(
        r'<!-- ====================================================================\s*FAMILLE 8 : ADMINISTRATION DE LA PLATEFORME \(ADM-01 à ADM-08\)\s*==================================================================== -->\s*<section class="family-view" id="view-ADM">[\s\S]*?</section>',
        re.MULTILINE
    )
    html, n_adm = old_adm_pattern.subn(NEW_VIEW_ADM_HTML, html, count=1)
    assert n_adm == 1, f"Section #view-ADM introuvable (remplacements={n_adm})"

    # 3. Injecter la modale universelle CRUD (#modalAdmCrudBox)
    if 'id="modalAdmCrudBox"' not in html:
        html = html.replace(
            '<!-- ========================================================================\n       MODALES TRANSACTIONNELLES SPRINT 1',
            ADM_CRUD_MODAL_HTML + '\n  <!-- ========================================================================\n       MODALES TRANSACTIONNELLES SPRINT 1',
            1
        )

    # 4. Dans inspectScreen(), éviter que l'ouverture initiale de ADM-01 ne scrolle sous l'en-tête des 4 niveaux
    html = html.replace(
        "if (anchorSection && screenId !== 'PUB-01') {",
        "if (anchorSection && screenId !== 'PUB-01' && screenId !== 'ADM-01') {"
    )

    # 5. Cibler explicitement #admAuditLogTbody dans syncAllViewsFromDB() pour ne pas écraser le tableau ADM-01
    html = html.replace(
        "const admTbody = document.querySelector('#view-ADM table tbody');",
        "const admTbody = document.getElementById('admAuditLogTbody') || document.querySelector('#view-ADM table tbody');"
    )

    # 6. Injecter les fonctions JS interactives CRUD ADM-01..08
    if "function admDuplicateCatalogItem" not in html:
        html = html.replace("  </script>\n</body>", ADMIN_CONSOLE_JS + "\n  </script>\n</body>", 1)

    # Vérifier qu'aucun caractère > 0x25FF n'a été introduit
    high_chars = [ch for ch in html if ord(ch) > 0x25FF]
    assert len(high_chars) == 0, f"Caractères Unicode > 0x25FF détectés : {high_chars}"

    PREVIEW_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Preview Administration CRUD écrite : {PREVIEW_HTML} ({len(html)} octets)")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_QA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        page.goto(PREVIEW_HTML.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)

        # Basculer sur la vue Administration (/admin -> ADM-01) et rester tout en haut
        page.evaluate("navigateFamily('ADM', 'ADM-01'); window.scrollTo(0, 0);")
        page.wait_for_timeout(350)

        # Visuel 1 : Vue d'ensemble Gouvernance + Barre CRUD (+ Ajouter, Filtres Pôles, Recherche) + Tableau CRUD
        s1 = ARTIFACT_DIR / "admin_validation_1_gouvernance_4_niveaux_tarifs_fcfa.png"
        page.screenshot(path=str(s1), full_page=False)
        (LOCAL_QA_DIR / s1.name).write_bytes(s1.read_bytes())

        # Visuel 2 : Action « Dupliquer » en 1 clic sur une prestation + Déclenchement du Garde-Fou SQL Enfant 500 FCFA
        page.evaluate("""
            admDuplicateCatalogItem('CAT-ZOO');
            admTestChildPriceViolation();
            const el = document.getElementById('admChildGuardBanner');
            window.scrollTo(0, el.getBoundingClientRect().bottom + window.scrollY - 900);
            const toast = document.getElementById('toastSprint1');
            if (toast) toast.style.display = 'none';
        """)
        page.wait_for_timeout(350)
        s2 = ARTIFACT_DIR / "admin_validation_2_garde_fou_enfant_500_fcfa_bloque.png"
        page.screenshot(path=str(s2), full_page=False)
        (LOCAL_QA_DIR / s2.name).write_bytes(s2.read_bytes())

        # Visuel 3 : Modale universelle CRUD « Ajouter / Modifier / Dupliquer / Supprimer une Prestation » (#modalAdmCrudBox)
        page.evaluate("""
            openAdmCrudModal('EDIT', 'CAT-ZOO');
        """)
        page.wait_for_timeout(350)
        s3_modal = ARTIFACT_DIR / "admin_validation_3_modale_crud_ajouter_modifier_dupliquer.png"
        page.screenshot(path=str(s3_modal), full_page=False)
        (LOCAL_QA_DIR / s3_modal.name).write_bytes(s3_modal.read_bytes())
        page.evaluate("closeAdmCrudModal();")

        # Visuel 4 : ADM-03 (Quotas / Météo) & ADM-04 (Mini-CMS CRUD Agenda & Saveurs avec Duplication en 1 clic)
        page.evaluate("""
            admDuplicateCmsItem('CMS-EVT-1');
            const el = document.getElementById('sec-ADM-03');
            window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 82);
            const toast = document.getElementById('toastSprint1');
            if (toast) toast.style.display = 'none';
        """)
        page.wait_for_timeout(350)
        s4 = ARTIFACT_DIR / "admin_validation_4_cms_crud_agenda_saveurs_jauges.png"
        page.screenshot(path=str(s4), full_page=False)
        (LOCAL_QA_DIR / s4.name).write_bytes(s4.read_bytes())

        # Visuel 5 : ADM-05 (CRUD Comptes Équipe 7 Rôles RBAC : + Nouvel Agent, Dupliquer Poste, Suspendre) & ADM-06/07
        page.evaluate("""
            const el = document.getElementById('sec-ADM-05');
            window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 82);
        """)
        page.wait_for_timeout(350)
        s5 = ARTIFACT_DIR / "admin_validation_5_rbac_7_roles_crud_equipe_passerelles.png"
        page.screenshot(path=str(s5), full_page=False)
        (LOCAL_QA_DIR / s5.name).write_bytes(s5.read_bytes())

        # Visuel 6 : ADM-08 Journal d'Audit Immuable traçant toutes les opérations CRUD (Duplications, Garde-fou, etc.)
        page.evaluate("""
            const el = document.getElementById('sec-ADM-08');
            window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 120);
        """)
        page.wait_for_timeout(350)
        s6 = ARTIFACT_DIR / "admin_validation_6_journal_audit_immuable_traces_crud.png"
        page.screenshot(path=str(s6), full_page=False)
        (LOCAL_QA_DIR / s6.name).write_bytes(s6.read_bytes())

        browser.close()
    print("[OK] 6 visuels de validation CRUD de la Console d'Administration générés avec succès.")


if __name__ == "__main__":
    build_and_capture()
