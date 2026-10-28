# -*- coding: utf-8 -*-
"""
Phase 4 — Intégration de la console d'administration CRUD (ADM-01 à ADM-08) dans le site.

Met à jour etape0-site-live/index.html ET Prototype_Interactif_ECOPARK_NEW_LOOK.html :
  1. Styles de la console (préfixe .adm-, palette 60-30-10 + Ocre Bronze)
  2. Remplacement de la section #view-ADM par la nouvelle console
  3. Module etape0-site-live/js/ecopark-admin.js intégré (après la couche EcoparkData)
  4. Ouverture de la console à l'affichage de la vue ADM (navigateFamily)
  5. syncAllViewsFromDB() : l'ancien tableau d'audit (non échappé) est remplacé par un
     rafraîchissement de la console (échappement HTML systématique)

Ré-exécutable (blocs délimités par des marqueurs). À lancer APRÈS build_data_layer.py.
Usage : python build_admin_console.py
"""
import hashlib
import re
from pathlib import Path

from build_data_layer import TARGETS

ROOT = Path(__file__).resolve().parent
ADMIN_JS = ROOT / "etape0-site-live" / "js" / "ecopark-admin.js"

CSS_START, CSS_END = "/* ECOPARK_ADMIN_CSS:START */", "/* ECOPARK_ADMIN_CSS:END */"
VIEW_START, VIEW_END = "<!-- ECOPARK_ADMIN_VIEW:START -->", "<!-- ECOPARK_ADMIN_VIEW:END -->"
JS_START, JS_END = "<!-- ECOPARK_ADMIN_JS:START -->", "<!-- ECOPARK_ADMIN_JS:END -->"
NAV_MARK = "// ECOPARK_ADMIN_OPEN"
SYNC_MARK = "// ECOPARK_ADMIN_SYNC"

ADMIN_CSS = CSS_START + r"""
    #view-ADM .adm-console { display: grid; gap: 22px; grid-template-columns: minmax(0, 1fr); }
    #view-ADM .adm-console > * { min-width: 0; }
    #view-ADM .adm-rolebar { display: flex; justify-content: space-between; align-items: center; gap: 14px; flex-wrap: wrap;
      background: var(--color-white); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 12px 16px; }
    #view-ADM .adm-rolebar-left { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
    #view-ADM .adm-rights { font-size: 13.5px; color: var(--color-text-muted); }
    #view-ADM .adm-inline { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--color-text-muted); }
    #view-ADM .adm-inline select { min-height: 36px; font-size: 13px; padding: 4px 10px; width: auto; }
    #view-ADM .adm-who { font-size: 13.5px; font-weight: 600; color: var(--color-brand-deep); }
    #view-ADM .adm-card { background: var(--color-white); border: 1px solid var(--color-border); border-radius: var(--radius-lg);
      box-shadow: var(--shadow-card); padding: 22px; }
    #view-ADM .adm-card > h3 { display: flex; align-items: center; gap: 8px; margin: 0 0 4px; }
    #view-ADM .adm-lead { margin: 0 0 14px; color: var(--color-text-muted); font-size: 14.5px; }
    #view-ADM .adm-badge { display: inline-flex; align-items: center; gap: 4px; border-radius: 999px; padding: 2px 10px; font-size: 12px;
      font-weight: 600; white-space: nowrap; border: 1px solid transparent; }
    #view-ADM .adm-badge-live { background: #EDF4E7; color: #1D490D; border-color: rgba(29, 73, 13, 0.2); }
    #view-ADM .adm-badge-draft { background: #FBF5EC; color: #9A5B13; border-color: rgba(196, 125, 43, 0.35); }
    #view-ADM .adm-badge-archived { background: #F3F4F1; color: #5B6657; border-color: #D9DED5; }
    #view-ADM .adm-badge-error { background: var(--color-error-bg); color: var(--color-error-text); border-color: var(--color-error-border); }
    #view-ADM .adm-tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
    #view-ADM .adm-tabs button { border: 1px solid var(--color-border); background: var(--color-white); color: var(--color-brand-deep);
      border-radius: 999px; padding: 6px 14px; font-size: 13.5px; font-weight: 600; cursor: pointer; }
    #view-ADM .adm-tabs button.active { background: var(--color-brand-deep); color: var(--color-white); border-color: var(--color-brand-deep); }
    #view-ADM .adm-toolbar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 10px; }
    #view-ADM .adm-toolbar .form-control { min-height: 38px; font-size: 13.5px; width: auto; }
    #view-ADM .adm-toolbar input[type="search"] { min-width: 240px; flex: 1; }
    #view-ADM .adm-kpis { display: flex; gap: 14px; flex-wrap: wrap; font-size: 13px; color: var(--color-text-muted); margin-bottom: 10px; }
    #view-ADM .adm-kpi b { color: var(--color-brand-deep); font-size: 15px; }
    #view-ADM .adm-table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
    #view-ADM .adm-table th { text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: .03em; color: var(--color-text-muted);
      padding: 8px 10px; border-bottom: 1px solid var(--color-border); white-space: nowrap; }
    #view-ADM .adm-table td { padding: 10px; border-bottom: 1px solid #EEF3EA; vertical-align: top; }
    #view-ADM .adm-col-offer { min-width: 240px; max-width: 360px; }
    #view-ADM .adm-sub { font-size: 12px; color: var(--color-text-muted); margin-top: 2px; }
    #view-ADM .adm-origin { color: #9A5B13; }
    #view-ADM .adm-prices { display: grid; gap: 2px; font-size: 12.5px; min-width: 200px; }
    #view-ADM .adm-prices em { color: var(--color-text-muted); font-style: normal; }
    #view-ADM .adm-actions { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    #view-ADM .adm-act { border: 1px solid var(--color-border-strong); background: var(--color-white); color: var(--color-brand-deep);
      border-radius: 8px; padding: 4px 10px; font-size: 12.5px; font-weight: 600; cursor: pointer; white-space: nowrap; }
    #view-ADM .adm-act:hover:not([disabled]) { background: #EDF4E7; }
    #view-ADM .adm-act[disabled] { opacity: .45; cursor: not-allowed; }
    #view-ADM .adm-act-dup { border-color: rgba(196, 125, 43, 0.55); color: #9A5B13; background: #FBF5EC; }
    #view-ADM .adm-act-pub { border-color: var(--color-brand-leaf); color: var(--color-white); background: var(--color-brand-leaf); }
    #view-ADM .adm-act-pub:hover:not([disabled]) { background: var(--color-brand-deep); }
    #view-ADM .adm-act-del { border-color: var(--color-error-border); color: var(--color-error-text); }
    #view-ADM .adm-row-new { background: #FBF5EC; box-shadow: inset 4px 0 0 #C47D2B; }
    #view-ADM .adm-row-archived { opacity: .62; }
    #view-ADM .adm-empty { color: var(--color-text-muted); text-align: center; padding: 18px; }
    #view-ADM .adm-cms-row { display: grid; gap: 8px; padding: 12px 0; border-bottom: 1px solid #EEF3EA; }
    #view-ADM .adm-cms-main strong { margin-right: 6px; }
    #view-ADM .adm-out { color: var(--color-error-text); }
    #view-ADM .adm-gw { display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap;
      border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 12px 14px; margin-bottom: 10px; }
    #view-ADM .adm-op { display: inline-block; border-radius: 6px; padding: 1px 8px; font-size: 12px; font-weight: 600; background: #EDF4E7; color: #1D490D; white-space: nowrap; }
    #view-ADM .adm-op-duplicate, #view-ADM .adm-op-guard_reject { background: #FBF5EC; color: #9A5B13; }
    #view-ADM .adm-op-delete, #view-ADM .adm-op-archive { background: var(--color-error-bg); color: var(--color-error-text); }
    #view-ADM .adm-nowrap { white-space: nowrap; }
    #view-ADM .adm-note { background: #FBF5EC; border: 1px solid rgba(196, 125, 43, 0.35); color: #6E420E; border-radius: 10px; padding: 10px 12px; font-size: 13.5px; margin: 10px 0; }
    #view-ADM .adm-note-ok { background: #EDF4E7; border-color: rgba(29, 73, 13, 0.2); color: #1D490D; }
    #view-ADM .adm-note-error { background: var(--color-error-bg); border-color: var(--color-error-border); color: var(--color-error-text); }
    #view-ADM .adm-note:empty { display: none; }
    #view-ADM .adm-rules { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
    #view-ADM .adm-rule { border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 12px 14px; font-size: 14px; }
    #view-ADM .adm-rule strong { display: block; color: var(--color-brand-deep); margin-bottom: 4px; }
    #view-ADM .adm-weather-preview { margin-top: 8px; font-size: 13.5px; background: #EDF4E7; border-radius: 10px; padding: 8px 12px; color: var(--color-brand-deep); }
    #view-ADM .adm-split { display: grid; gap: 22px; align-items: start; }
    #view-ADM .adm-split > div { min-width: 0; }
    #view-ADM .adm-split-quota { grid-template-columns: minmax(0, 3fr) minmax(260px, 2fr); }
    #view-ADM .adm-split-even { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    #view-ADM .adm-weather .form-control { width: 100%; max-width: none; }
    #view-ADM .adm-weather select.form-control { white-space: normal; text-overflow: ellipsis; }
    #view-ADM .adm-quota-table .adm-col-offer { min-width: 150px; max-width: 240px; }
    #view-ADM .adm-quota-table td { padding: 8px 6px; }
    #view-ADM .adm-quota-table td:last-child, #view-ADM .adm-quota-table td:nth-child(4) { white-space: nowrap; }
    #view-ADM .adm-quota-input { width: 96px; min-height: 34px !important; padding: 4px 8px; }
    #view-ADM .adm-quota-table .adm-actions { flex-wrap: nowrap; }
    @media (max-width: 1180px) {
      #view-ADM .adm-split-quota, #view-ADM .adm-split-even { grid-template-columns: 1fr; }
    }
    /* La barre de réservation des visiteurs n'a pas sa place dans le back-office */
    body:has(#view-ADM.active) #mobileStickyConversionBar { display: none !important; }
    @media (max-width: 640px) {
      #view-ADM .adm-quota-table thead { display: none; }
      #view-ADM .adm-quota-table, #view-ADM .adm-quota-table tbody { display: block; width: 100%; }
      #view-ADM .adm-quota-table tr { display: grid; grid-template-columns: auto 1fr; gap: 6px 10px; align-items: center;
        padding: 10px 12px; border-bottom: 1px solid #EEF3EA; }
      #view-ADM .adm-quota-table td { display: block; border: 0; padding: 0; max-width: none; min-width: 0; white-space: normal !important; }
      #view-ADM .adm-quota-table td:first-child { grid-column: 1 / -1; }
      #view-ADM .adm-quota-table td:nth-child(2)::before { content: 'Standard : '; color: var(--color-text-muted); }
      #view-ADM .adm-quota-table td:nth-child(4) { grid-column: 1 / -1; font-size: 12.5px; color: var(--color-text-muted); }
      #view-ADM .adm-quota-table td:last-child { grid-column: 1 / -1; }
      #view-ADM .adm-quota-input { width: 100%; }
    }
    #view-ADM .adm-modal-overlay { position: fixed; inset: 0; z-index: 3200; display: none; align-items: center; justify-content: center;
      background: rgba(20, 34, 17, 0.45); padding: 16px; }
    #view-ADM .adm-modal-overlay.open { display: flex; }
    #view-ADM .adm-modal-card { background: var(--color-white); border-radius: var(--radius-lg); box-shadow: 0 28px 68px rgba(20, 34, 17, 0.25);
      width: min(860px, 100%); max-height: calc(100vh - 32px); overflow: auto; padding: 22px 24px; }
    #view-ADM .adm-confirm-card { width: min(520px, 100%); }
    #view-ADM .adm-modal-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 8px; }
    #view-ADM .adm-modal-head h4, #view-ADM .adm-confirm-card h4 { margin: 2px 0 0; font-family: var(--font-heading); font-size: 1.35rem; color: var(--color-brand-deep); }
    #view-ADM .adm-eyebrow { font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: var(--color-brand-leaf); font-weight: 700; }
    #view-ADM .adm-form { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 14px; margin-top: 8px; }
    #view-ADM .adm-field-wide { grid-column: 1 / -1; }
    #view-ADM .adm-field { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
    #view-ADM .adm-field .form-label { display: block; margin: 0; font-size: 13px; font-weight: 600; }
    #view-ADM .adm-field .form-control { min-height: 38px; font-size: 14px; width: 100%; max-width: none; }
    #view-ADM .btn[disabled], #view-ADM button[disabled].btn-primary, #view-ADM button[disabled].btn-secondary { opacity: .45; cursor: not-allowed; box-shadow: none; }
    #view-ADM .adm-field-err { color: var(--color-error-text); font-size: 12.5px; min-height: 0; margin-top: 2px; }
    #view-ADM .adm-invalid { border-color: var(--color-error-border) !important; background: #FFF8F7; }
    #view-ADM .adm-check { display: flex; flex-direction: row; gap: 8px; align-items: center; font-size: 14px; padding-top: 22px; }
    #view-ADM .adm-diff { margin-top: 12px; font-size: 13px; color: var(--color-text-muted); }
    #view-ADM .adm-diff ul { margin: 4px 0 0; padding-left: 18px; color: var(--color-text); }
    #view-ADM .adm-modal-actions { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
    #view-ADM .adm-modal-actions > div { display: flex; gap: 8px; flex-wrap: wrap; }
    #view-ADM .adm-btn-danger { background: var(--color-error-text) !important; border-color: var(--color-error-text) !important; color: #fff !important; }
    #view-ADM .adm-toast { position: fixed; right: 18px; bottom: 18px; z-index: 3300; display: none; gap: 12px; align-items: center;
      background: var(--color-brand-deep); color: #fff; border-radius: 14px; padding: 12px 16px; max-width: 460px; font-size: 14px; box-shadow: var(--shadow-elevated); }
    #view-ADM .adm-toast.show { display: flex; }
    #view-ADM .adm-toast-error { background: var(--color-error-text); }
    #view-ADM .adm-toast-undo { background: #FBF5EC; color: #9A5B13; border: 0; border-radius: 8px; padding: 5px 12px; font-weight: 700; cursor: pointer; }
    @media (max-width: 760px) {
      #view-ADM .adm-form { grid-template-columns: 1fr; }
      #view-ADM .adm-card { padding: 16px; }
    }
    """ + CSS_END

ICON_LOCK = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
ICON_LIST = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/></svg>'
ICON_GAUGE = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>'
ICON_CAL = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/></svg>'
ICON_USERS = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
ICON_PLUG = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/></svg>'
ICON_SHIELD = '<svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'

ADMIN_VIEW = VIEW_START + f"""
      <section class="family-view" id="view-ADM">
        <div class="subnav-bar">
          <div class="container">
            <div class="subnav-list">
              <button class="subnav-pill active" onclick="inspectScreen('ADM-01')">ADM-01 Catalogue &amp; Tarifs</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-02')">ADM-02 Règles tarifaires</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-03')">ADM-03 Jauges &amp; Météo</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-04')">ADM-04 Agenda &amp; Carte</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-05')">ADM-05 Comptes équipe</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-06')">ADM-06/07 Passerelles</button>
              <button class="subnav-pill" onclick="inspectScreen('ADM-08')">ADM-08 Journal d'audit</button>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="container adm-console">
            <div class="section-header">
              <span class="eyebrow"><span class="tech-code-tag">ADM-01 à ADM-08 • </span>Gouvernance, tarifs, contenus &amp; audit</span>
              <h2>Administration de la plateforme ECOPARK</h2>
            </div>

            <div class="adm-rolebar" id="admRoleBar"></div>

            <div class="adm-card" id="sec-ADM-01">
              <h3>{ICON_LIST} <span class="tech-code-tag">ADM-01 — </span>Catalogue, formules &amp; cités hôtelières</h3>
              <p class="adm-lead">Ajouter, modifier, dupliquer, publier ou archiver une offre. Toute nouvelle fiche et toute copie restent en brouillon, invisibles du public, jusqu'à leur publication.</p>
              <div class="adm-tabs" id="admCatalogTabs">
                <button type="button" data-tab="catalog_activities" class="active">Activités</button>
                <button type="button" data-tab="sales_bundles">Formules (Pass)</button>
                <button type="button" data-tab="lodge_cities">Cités hôtelières</button>
              </div>
              <div class="adm-toolbar">
                <input type="search" class="form-control" id="admCatalogSearch" placeholder="Rechercher un intitulé, un code, une description..." aria-label="Rechercher dans le catalogue" />
                <select class="form-control" id="admPoleFilter" aria-label="Filtrer par pôle">
                  <option value="ALL">Tous les pôles</option>
                  <option value="NATURE_FAUNE">Nature &amp; Faune</option>
                  <option value="EAU_PLEIN_AIR">Eau &amp; Plein air</option>
                  <option value="RESTAURATION">Restauration</option>
                  <option value="HEBERGEMENT">Hébergement</option>
                  <option value="GROUPES_B2B">Groupes &amp; Navettes</option>
                  <option value="FORMATION_CFP">Formation CFP</option>
                </select>
                <select class="form-control" id="admStatusFilter" aria-label="Filtrer par statut">
                  <option value="ACTIVE">En ligne + brouillons</option>
                  <option value="PUBLISHED">En ligne</option>
                  <option value="DRAFT">Brouillons</option>
                  <option value="ARCHIVED">Archivées</option>
                  <option value="ALL">Toutes (y compris archives)</option>
                </select>
                <button type="button" class="btn btn-primary btn-sm" id="admAddOffer">+ Ajouter une offre</button>
              </div>
              <div class="adm-kpis" id="admCatalogKpis"></div>
              <div class="table-responsive">
                <table class="adm-table" id="admCatalogTable">
                  <thead><tr><th>Offre</th><th>Tarifs (FCFA)</th><th>Capacité</th><th>Statut</th><th>Actions</th></tr></thead>
                  <tbody id="admCatalogBody"></tbody>
                </table>
              </div>
            </div>

            <div class="adm-card" id="sec-ADM-02">
              <h3>{ICON_LOCK} <span class="tech-code-tag">ADM-02 — </span>Règles tarifaires appliquées par la base</h3>
              <div class="adm-rules">
                <div class="adm-rule"><strong>Tarif enfant protégé</strong>Le tarif enfant en groupe ne peut jamais dépasser le tarif enfant individuel de la même activité (500 FCFA au Zoo, 1 500 FCFA à la Piscine).</div>
                <div class="adm-rule"><strong>Publication par la Direction</strong>L'exploitation et l'administrateur préparent les brouillons ; seule la Direction met un tarif en ligne ou modifie un prix déjà publié.</div>
                <div class="adm-rule"><strong>Copie = brouillon</strong>Dupliquer crée une version de travail invisible du public. À la publication, elle peut remplacer l'offre d'origine sans changer son adresse.</div>
                <div class="adm-rule"><strong>Rien ne se perd</strong>Une fiche déjà publiée ou vendue est archivée, jamais effacée. Chaque action est inscrite au journal d'audit.</div>
              </div>
            </div>

            <div class="adm-card" id="sec-ADM-03">
              <h3>{ICON_GAUGE} <span class="tech-code-tag">ADM-03 — </span>Jauges du jour &amp; bandeau météo</h3>
              <div class="adm-split adm-split-quota">
                <div>
                  <div class="adm-toolbar">
                    <label class="adm-inline" for="admQuotaDate"><span>Jour concerné</span></label>
                    <input type="date" class="form-control" id="admQuotaDate" />
                  </div>
                  <div class="table-responsive">
                    <table class="adm-table adm-quota-table">
                      <thead><tr><th>Activité</th><th>Standard</th><th>Jauge du jour</th><th>Disponibilité</th><th></th></tr></thead>
                      <tbody id="admQuotaBody"></tbody>
                    </table>
                  </div>
                </div>
                <div class="adm-weather">
                  <label class="form-label" for="admWeatherPreset">Message affiché en haut du site</label>
                  <select class="form-control" id="admWeatherPreset"></select>
                  <label class="form-label" for="admWeatherCustom" style="margin-top:10px;">Message personnalisé (facultatif, remplace le préréglage)</label>
                  <textarea class="form-control" id="admWeatherCustom" rows="2" maxlength="160"></textarea>
                  <div class="adm-weather-preview" id="admWeatherPreview"></div>
                  <button type="button" class="btn btn-primary btn-sm" id="admWeatherSave" style="margin-top:10px;">Publier sur le site</button>
                </div>
              </div>
            </div>

            <div class="adm-card" id="sec-ADM-04">
              <h3>{ICON_CAL} <span class="tech-code-tag">ADM-04 — </span>Agenda de la semaine &amp; carte du Château des Saveurs</h3>
              <p class="adm-lead">Dupliquez un événement pour le reproduire un autre jour (jour férié, édition spéciale), réordonnez, ou signalez un plat en rupture.</p>
              <div class="adm-split adm-split-even">
                <div>
                  <div class="adm-toolbar"><strong>Agenda (/agenda)</strong><button type="button" class="btn btn-secondary btn-sm" id="admAddAgenda">+ Ajouter un événement</button></div>
                  <div id="admAgendaList"></div>
                </div>
                <div>
                  <div class="adm-toolbar"><strong>Carte du restaurant</strong><button type="button" class="btn btn-secondary btn-sm" id="admAddMenu">+ Ajouter un plat</button></div>
                  <div id="admMenuList"></div>
                </div>
              </div>
            </div>

            <div class="adm-card" id="sec-ADM-05">
              <h3>{ICON_USERS} <span class="tech-code-tag">ADM-05 — </span>Comptes de l'équipe &amp; rôles</h3>
              <div class="adm-toolbar"><span class="adm-rights">5 rôles d'équipe : guichet, contrôle, exploitation, direction, administrateur.</span>
                <button type="button" class="btn btn-secondary btn-sm" id="admStaffAdd">+ Nouveau compte</button></div>
              <div class="table-responsive">
                <table class="adm-table">
                  <thead><tr><th>Membre &amp; poste</th><th>Rôle</th><th>Statut</th><th>Actions</th></tr></thead>
                  <tbody id="admStaffBody"></tbody>
                </table>
              </div>
            </div>

            <div class="adm-card" id="sec-ADM-06">
              <span id="sec-ADM-07"></span>
              <h3>{ICON_PLUG} <span class="tech-code-tag">ADM-06 &amp; ADM-07 — </span>Passerelles de paiement &amp; WhatsApp</h3>
              <p class="adm-lead">État des connexions uniquement : aucune clé secrète n'est stockée ni affichée dans le navigateur.</p>
              <div id="admGatewayList"></div>
            </div>

            <div class="adm-card" id="sec-ADM-08">
              <h3>{ICON_SHIELD} <span class="tech-code-tag">ADM-08 — </span>Journal d'audit immuable</h3>
              <div class="adm-toolbar">
                <select class="form-control" id="admAuditOp" aria-label="Filtrer par opération">
                  <option value="ALL">Toutes les opérations</option>
                  <option value="INSERT">Ajouts</option>
                  <option value="UPDATE">Modifications</option>
                  <option value="DUPLICATE">Duplications</option>
                  <option value="PUBLISH">Publications</option>
                  <option value="ARCHIVE">Archivages</option>
                  <option value="DELETE">Suppressions</option>
                  <option value="RESTORE">Restaurations</option>
                  <option value="GUARD_REJECT">Garde-fou tarifaire</option>
                  <option value="EXPORT_CSV">Exports</option>
                </select>
                <input type="search" class="form-control" id="admAuditSearch" placeholder="Rechercher un acteur, une fiche..." aria-label="Rechercher dans le journal" />
                <button type="button" class="btn btn-secondary btn-sm" id="admAuditExport">Exporter (CSV)</button>
                <button type="button" class="btn btn-secondary btn-sm" id="admAuditVerify">Vérifier l'intégrité</button>
              </div>
              <div class="adm-note" id="admChainResult"></div>
              <div class="table-responsive">
                <table class="adm-table" id="admAuditTable">
                  <thead><tr><th>Horodatage</th><th>Opération</th><th>Acteur</th><th>Détail</th></tr></thead>
                  <tbody id="admAuditBody"></tbody>
                </table>
              </div>
              <div class="adm-toolbar" style="justify-content:space-between;margin-top:10px;">
                <span class="adm-rights" id="admAuditCount"></span>
                <span class="adm-actions"><button type="button" class="adm-act" id="admAuditPrev">Précédent</button><button type="button" class="adm-act" id="admAuditNext">Suivant</button></span>
              </div>
            </div>
          </div>
        </div>

        <div class="adm-modal-overlay" id="admEditor" role="dialog" aria-modal="true" aria-label="Édition d'une fiche"><div class="adm-modal-card" id="admEditorCard"></div></div>
        <div class="adm-modal-overlay" id="admConfirm" role="alertdialog" aria-modal="true" aria-label="Confirmation"><div class="adm-modal-card adm-confirm-card"></div></div>
        <div class="adm-toast" id="admToast" role="status" aria-live="polite"></div>
      </section>
      """ + VIEW_END


def patch(html: str) -> str:
    nl = "\r\n" if "\r\n" in html else "\n"
    to_nl = lambda s: s.replace("\r\n", "\n").replace("\n", nl)

    # 1. Styles
    css = to_nl(ADMIN_CSS)
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), lambda _: css, html, count=1, flags=re.S)
    else:
        idx = html.index("</style>")
        html = html[:idx] + "    " + css + nl + "  " + html[idx:]

    # 2. Vue #view-ADM
    view = to_nl(ADMIN_VIEW)
    if VIEW_START in html:
        html = re.sub(re.escape(VIEW_START) + r".*?" + re.escape(VIEW_END), lambda _: view, html, count=1, flags=re.S)
    else:
        old = re.compile(r'<section class="family-view" id="view-ADM">.*?</section>', re.S)
        m = old.search(html)
        assert m, "Section #view-ADM introuvable"
        html = html[: m.start()] + view.strip() + html[m.end():]

    # 3. Chargeur du module (le module lui-même n'est téléchargé qu'à l'ouverture de /admin :
    #    les visiteurs du site public ne le reçoivent jamais)
    version = hashlib.sha256(ADMIN_JS.read_bytes()).hexdigest()[:10]
    loader = (
        "window.ecoparkOpenAdmin = function () {\n"
        "  if (window.EcoparkAdmin) return EcoparkAdmin.open();\n"
        "  if (window._ecoparkAdminLoading) return window._ecoparkAdminLoading;\n"
        "  var base = '/js/';\n"
        "  if (location.protocol === 'file:') base = /etape0-site-live\\/index\\.html$/.test(location.pathname) ? 'js/' : 'etape0-site-live/js/';\n"
        "  window._ecoparkAdminLoading = new Promise(function (resolve, reject) {\n"
        "    var s = document.createElement('script');\n"
        f"    s.src = base + 'ecopark-admin.js?v={version}';\n"
        "    s.onload = resolve; s.onerror = reject;\n"
        "    document.head.appendChild(s);\n"
        "  }).then(function () { return EcoparkAdmin.open(); }, function () {\n"
        "    window._ecoparkAdminLoading = null;\n"
        "    var bar = document.getElementById('admRoleBar');\n"
        "    if (bar) bar.textContent = 'La console d\\'administration n\\'a pas pu être chargée. Vérifiez la connexion puis rechargez la page.';\n"
        "  });\n"
        "  return window._ecoparkAdminLoading;\n"
        "};"
    )
    js_block = to_nl(JS_START + "\n  <script id=\"ecoparkAdminLoader\">\n" + loader + "\n  </script>\n  " + JS_END)
    if JS_START in html:
        html = re.sub(re.escape(JS_START) + r".*?" + re.escape(JS_END), lambda _: js_block, html, count=1, flags=re.S)
    else:
        anchor = "<!-- ECOPARK_DATA_LAYER:END -->"
        assert html.count(anchor) == 1, "Lancer build_data_layer.py avant ce script"
        html = html.replace(anchor, anchor + nl + "  " + js_block, 1)

    # 4. Ouverture de la console à l'affichage de la vue ADM
    nav_line = "      if (family === 'ADM' && window.ecoparkOpenAdmin) ecoparkOpenAdmin(); " + NAV_MARK + nl
    if NAV_MARK in html:
        html = re.sub(r"[ \t]*if \(family === 'ADM'[^\n]*" + re.escape(NAV_MARK) + r"\r?\n", lambda _: nav_line, html, count=1)
    else:
        anchor = "      if (targetView) targetView.classList.add('active');" + nl
        assert html.count(anchor) == 1, "navigateFamily() introuvable"
        html = html.replace(anchor, anchor + nav_line, 1)

    # 5. Ancien tableau d'audit non échappé -> rafraîchissement de la console
    if SYNC_MARK not in html:
        old = re.compile(
            r"      const admTbody = document\.querySelector\('#view-ADM table tbody'\);\r?\n      if \(admTbody\) \{\r?\n.*?\r?\n      \}\r?\n", re.S)
        m = old.search(html)
        assert m, "Bloc d'audit de syncAllViewsFromDB() introuvable"
        html = html[: m.start()] + "      if (window.EcoparkAdmin) EcoparkAdmin.onDataChanged(); " + SYNC_MARK + nl + html[m.end():]
    return html


def main():
    for target in TARGETS:
        with open(target, "r", encoding="utf-8", newline="") as fh:
            html = fh.read()
        out = patch(html)
        high = [ch for ch in out if ord(ch) > 0x25FF]
        assert not high, f"Caractères interdits (> U+25FF) : {sorted(set(high))[:10]}"
        with open(target, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)
        print(f"[OK] {target.name} : console d'administration intégrée ({len(out)} octets)")


if __name__ == "__main__":
    main()
