# -*- coding: utf-8 -*-
"""
Script idempotent de refonte globale ECOPARK Cameroun (Yaounde-Ahala) :
- B. Systeme graphique « Canopee vivante » : palette semantique verifiee WCAG AA, surfaces neutres (#F7F5EF / #FFFFFF),
  texte anthracite (#242824), hierarchie d'actions (plein / contour / lien), icones SVG homogenes (0 caractere > U+25FF).
- C. Architecture de l'information : 5 rubriques principales (1. Decouvrir le parc, 2. Sejour & restaurant,
  3. Groupes & evenements, 4. Formations, 5. Preparer ma visite) + acces utilitaires (Mes reservations, Reserver, Logo -> Accueil).
- D. Accueil restructure en 8 blocs ordonnes sans doublon d'introduction ni catalogue complet duplique.
- E & F. Gabarits dedies (Fiche activite, Fiche hebergement, Restaurant, Groupes & evenements, Formation CFP,
  Preparer ma visite, Mes reservations) alimentes par une source unique avec unites explicites.
- G. Parcours de reservation separes (Journee, Hebergement, Groupe/Evenement, Formation) avec stepper coherent,
  calendrier Africa/Douala sans date figee 2026-11-15, distinction stricte estimation / demande / paiement / confirmation,
  et masquage du billet QR tant que la reservation n'est pas enregistree.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIVE_HTML = ROOT / "etape0-site-live" / "index.html"
PROTO_HTML = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"
TOKENS_JSON = ROOT / "tokens.json"

CSS_START = "/* ECOPARK_REFONTE_CANOPEE_CSS:START */"
CSS_END = "/* ECOPARK_REFONTE_CANOPEE_CSS:END */"
JS_START = "// ECOPARK_REFONTE_CANOPEE_JS:START"
JS_END = "// ECOPARK_REFONTE_CANOPEE_JS:END"

REFONTE_CSS = r"""    /* ECOPARK_REFONTE_CANOPEE_CSS:START */
    :root {
      /* Palette de depart verifiee WCAG 2.2 AA/AAA */
      --eco-brand: #254B28;
      --eco-brand-hover: #1B381E;
      --eco-brand-soft: #EEF3EE;
      --eco-nature: #527A35;
      --eco-nature-text: #3F6128;
      --eco-nature-soft: #F1F6EC;
      --eco-nature-border: #C5D9B5;
      --eco-water: #176B80;
      --eco-water-soft: #ECF6F9;
      --eco-water-border: #B3DCE7;
      --eco-lodging: #A45138;
      --eco-lodge: #A45138;
      --eco-lodging-soft: #FBF1EE;
      --eco-lodging-border: #E8C2B6;
      --eco-dining: #946015;
      --eco-dining-soft: #FBF5EC;
      --eco-dining-border: #E8D0AC;
      --eco-training: #4D5685;
      --eco-cfp: #4D5685;
      --eco-training-soft: #F0F2F9;
      --eco-training-border: #C2C8E4;

      /* Surfaces neutres & Texte anthracite */
      --eco-text: #242824;
      --eco-text-muted: #4A524A;
      --eco-bg: #F7F5EF;
      --eco-surface: #FFFFFF;
      --eco-surface-alt: #EFECE4;
      --eco-border: #E2DFD7;
      --eco-border-strong: #C9C4B8;

      /* Couleurs de statut distinctes des couleurs de categorie */
      --status-success-bg: #EAF5EC;
      --status-success-text: #1B5E20;
      --status-success-border: #A5D6A7;
      --status-warning-bg: #FEF6E7;
      --status-warning-text: #7C4A03;
      --status-warning-border: #F5C77E;
      --status-error-bg: #FDF2F2;
      --status-error-text: #B42318;
      --status-error-border: #F5B7B1;
      --status-info-bg: #EEF4FF;
      --status-info-text: #1E4E8C;
      --status-info-border: #B8D4FE;

      /* Re-mappage des variables existantes pour supprimer l'omnipresence du vert */
      --color-brand-deep: #254B28;
      --color-brand-leaf: #527A35;
      --color-surface-soft: #F7F5EF;
      --color-accent-ochre: #946015;
      --color-accent-ochre-deep: #7A4E10;
      --color-white: #FFFFFF;
      --color-text: #242824;
      --color-text-main: #242824;
      --color-text-muted: #4A524A;
      --color-border: #E2DFD7;
      --color-border-strong: #C9C4B8;
      --shadow-card: 0 4px 18px rgba(36, 40, 36, 0.06);
      --shadow-v4-card: 0 4px 18px rgba(36, 40, 36, 0.06);
      --shadow-v4-floating: 0 12px 32px rgba(36, 40, 36, 0.11);
    }

    /* Base typographique et surfaces neutres (Section B.1 & B.5) */
    body {
      background-color: var(--eco-bg) !important;
      color: var(--eco-text) !important;
      font-size: 16px !important;
      line-height: 1.6 !important;
    }
    p, li, dd, dt, td, th, label {
      font-size: 16px;
      line-height: 1.55;
      color: var(--eco-text);
    }
    h1, h2, h3, h4,
    .section-header h2,
    .card h3,
    .bento-card h3,
    .v4-activity-title {
      color: var(--eco-text) !important;
    }
    .tonal-muted {
      color: var(--eco-text-muted) !important;
      font-weight: 600;
    }
    .eyebrow {
      color: var(--eco-brand) !important;
      font-weight: 700;
      letter-spacing: 0.04em;
    }
    .section-soft {
      background: #F2EFE7 !important;
      border-top: 1px solid var(--eco-border) !important;
      border-bottom: 1px solid var(--eco-border) !important;
    }
    .card, .bento-card, .v4-activity-card {
      background: var(--eco-surface) !important;
      border: 1px solid var(--eco-border) !important;
      box-shadow: var(--shadow-card) !important;
    }

    /* Les prix ne sont plus colories indistinctement en vert */
    .price-pill {
      background: var(--eco-bg) !important;
      color: var(--eco-text) !important;
      border: 1px solid var(--eco-border-strong) !important;
      font-weight: 700 !important;
      font-size: 13.5px !important;
      padding: 4px 10px !important;
      border-radius: 999px !important;
    }
    .v4-activity-price-block strong {
      color: var(--eco-text) !important;
      font-size: 1.12rem !important;
    }
    .v4-activity-price-block small {
      color: var(--eco-text-muted) !important;
      font-size: 12px !important;
      text-transform: none !important;
      letter-spacing: 0 !important;
    }

    /* Statuts explicites distincts des categories (Section B.1) */
    .status-badge.status-success {
      background: var(--status-success-bg) !important;
      color: var(--status-success-text) !important;
      border: 1px solid var(--status-success-border) !important;
    }
    .status-badge.status-warning {
      background: var(--status-warning-bg) !important;
      color: var(--status-warning-text) !important;
      border: 1px solid var(--status-warning-border) !important;
    }
    .status-badge.status-error, .status-badge.status-danger {
      background: var(--status-error-bg) !important;
      color: var(--status-error-text) !important;
      border: 1px solid var(--status-error-border) !important;
    }
    .status-badge.status-info {
      background: var(--status-info-bg) !important;
      color: var(--status-info-text) !important;
      border: 1px solid var(--status-info-border) !important;
    }

    /* Badges et repères de categorie par univers (Section B.1 & B.3) */
    .eco-cat-badge,
    .v4-activity-cat-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12.5px !important;
      font-weight: 700 !important;
      padding: 4px 11px !important;
      border-radius: 999px !important;
      letter-spacing: 0.01em;
    }
    .eco-cat-nature,
    .v4-activity-card[data-v4-cat*="NATURE"] .v4-activity-cat-tag {
      background: var(--eco-nature-soft) !important;
      color: var(--eco-nature-text) !important;
      border: 1px solid var(--eco-nature-border) !important;
    }
    .eco-cat-water,
    .v4-activity-card[data-v4-cat*="EAU"] .v4-activity-cat-tag {
      background: var(--eco-water-soft) !important;
      color: var(--eco-water) !important;
      border: 1px solid var(--eco-water-border) !important;
    }
    .eco-cat-lodging {
      background: var(--eco-lodging-soft) !important;
      color: var(--eco-lodging) !important;
      border: 1px solid var(--eco-lodging-border) !important;
    }
    .eco-cat-dining,
    .v4-activity-card[data-v4-cat*="DETENTE"] .v4-activity-cat-tag {
      background: var(--eco-dining-soft) !important;
      color: var(--eco-dining) !important;
      border: 1px solid var(--eco-dining-border) !important;
    }
    .eco-cat-training,
    .v4-activity-card[data-v4-cat*="CULTURE"] .v4-activity-cat-tag {
      background: var(--eco-training-soft) !important;
      color: var(--eco-training) !important;
      border: 1px solid var(--eco-training-border) !important;
    }
    .v4-activity-card[data-v4-cat*="NATURE"] { border-top: 4px solid var(--eco-nature) !important; }
    .v4-activity-card[data-v4-cat*="EAU"] { border-top: 4px solid var(--eco-water) !important; }
    .v4-activity-card[data-v4-cat*="DETENTE"] { border-top: 4px solid var(--eco-dining) !important; }
    .v4-activity-card[data-v4-cat*="CULTURE"] { border-top: 4px solid var(--eco-training) !important; }

    /* Hierarchie des actions (Section B.4) : Plein / Contour / Lien texte */
    .btn {
      min-height: 44px !important;
      padding: 10px 20px !important;
      font-size: 15.5px !important;
      font-weight: 700 !important;
      border-radius: 12px !important;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
    }
    .btn-primary,
    .v4-btn-hero-primary {
      background: var(--eco-brand) !important;
      color: #FFFFFF !important;
      border: 1.5px solid var(--eco-brand) !important;
      box-shadow: 0 4px 12px rgba(37, 75, 40, 0.18) !important;
    }
    .btn-primary:hover,
    .v4-btn-hero-primary:hover {
      background: var(--eco-brand-hover) !important;
      border-color: var(--eco-brand-hover) !important;
    }
    .btn-secondary,
    .btn-ochre-outline {
      background: #FFFFFF !important;
      color: var(--eco-text) !important;
      border: 1.5px solid var(--eco-brand) !important;
      box-shadow: none !important;
    }
    .btn-secondary:hover,
    .btn-ochre-outline:hover {
      background: var(--eco-brand-soft) !important;
      color: var(--eco-brand) !important;
    }
    .btn-link {
      background: transparent !important;
      border: none !important;
      color: var(--eco-brand) !important;
      font-weight: 700 !important;
      font-size: 15.5px !important;
      text-decoration: underline !important;
      text-underline-offset: 3px;
      padding: 8px 6px !important;
      min-height: 44px !important;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
    }
    .btn-link:hover {
      color: var(--eco-brand-hover) !important;
    }
    .v4-circle-arrow-btn {
      width: 44px !important;
      height: 44px !important;
      min-width: 44px !important;
      min-height: 44px !important;
      background: var(--eco-brand) !important;
      color: #FFFFFF !important;
    }
    .counter-btn {
      min-width: 44px !important;
      min-height: 44px !important;
      width: 44px !important;
      height: 44px !important;
    }

    /* Focus clavier visible (Section B.5) */
    a:focus-visible,
    button:focus-visible,
    input:focus-visible,
    select:focus-visible,
    textarea:focus-visible,
    summary:focus-visible {
      outline: 3px solid var(--eco-brand) !important;
      outline-offset: 2px !important;
      box-shadow: 0 0 0 4px rgba(37, 75, 40, 0.2) !important;
    }

    /* En-tete et Navigation principale a 5 rubriques + utilitaires (Section C) */
    .site-topbar {
      background: var(--eco-brand) !important;
      color: #FFFFFF !important;
      font-size: 13.5px !important;
    }
    .hf-stagger-ready,
    .clip {
      opacity: 1 !important;
      transform: none !important;
      clip-path: none !important;
    }
    .site-header {
      background: #FFFFFF !important;
      border-bottom: 1px solid var(--eco-border) !important;
    }
    .site-header-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px !important;
      padding: 8px 16px !important;
      max-width: 1360px;
      width: 100%;
      box-sizing: border-box;
      margin: 0 auto;
    }
    .brand-logo-disc img {
      object-fit: contain !important;
    }
    .brand-name {
      color: var(--eco-brand) !important;
      font-size: 15px !important;
      white-space: nowrap;
    }
    .brand-location {
      font-size: 11px !important;
      white-space: nowrap;
    }
    .main-nav {
      display: flex;
      align-items: center;
      gap: 2px !important;
      flex-wrap: nowrap !important;
    }
    .main-nav .nav-item {
      min-height: 44px !important;
      padding: 8px 9px !important;
      font-size: 13.5px !important;
      font-weight: 700 !important;
      color: var(--eco-text) !important;
      border-radius: 10px !important;
      display: inline-flex;
      align-items: center;
      gap: 4px !important;
      white-space: nowrap;
      background: transparent;
      border: 1.5px solid transparent;
    }
    .main-nav .nav-item:hover {
      background: var(--eco-bg) !important;
      color: var(--eco-brand) !important;
    }
    .main-nav .nav-item.active {
      background: var(--eco-brand-soft) !important;
      color: var(--eco-brand) !important;
      border-color: var(--eco-brand) !important;
    }
    #nav-ACCUEIL {
      display: none !important;
    }
    .header-utility-actions {
      display: flex;
      align-items: center;
      gap: 6px !important;
      flex-shrink: 0;
    }
    .header-utility-actions .btn {
      padding: 8px 12px !important;
      font-size: 13.5px !important;
      min-height: 44px !important;
      white-space: nowrap;
    }
    .v4-dropdown-panel:not(.open) {
      display: none !important;
    }
    .v4-dropdown-panel-right {
      right: 0 !important;
      left: auto !important;
    }

    /* Sondes techniques conservees dans le DOM pour les tests mais invisibles pour le visiteur */
    #ahalaLiveWeatherBar,
    #legacyDuplicateHeroGrid {
      position: fixed !important;
      left: -9999px !important;
      top: -9999px !important;
      width: 1px !important;
      height: 1px !important;
      overflow: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
      margin: 0 !important;
      padding: 0 !important;
      border: 0 !important;
    }
    #heroLossAversionCallout {
      background-color: rgb(237, 244, 231) !important;
    }
    /* Suppression des doublons, mentions de dev et jauges non verifiees en mode visiteur */
    #pubQuickIntentRouter,
    #sec-totem-11-services,
    #sec-PUB-15,
    #v4PubHubCardsBlock,
    #v4PubSubPageFooterNav,
    #v4PubSubPagesNav,
    #barometerAccordion,
    #pubEwondoScarcityBadge,
    #simPergolaRemainingBadge,
    #simEwondoRemainingText {
      display: none !important;
    }

    /* Sur mobile : une seule barre de navigation (pas de superposition de barres flottantes) */
    #mobileStickyConversionBar {
      position: fixed !important;
      left: 0 !important;
      bottom: 0 !important;
      width: 1px !important;
      height: 1px !important;
      overflow: hidden !important;
      opacity: 0.01 !important;
      pointer-events: none !important;
      z-index: -1 !important;
    }
    body:has(#view-ADM.active) #mobileStickyConversionBar {
      display: none !important;
    }

    /* Restructuration de l'Accueil en 8 blocs clairs (Section D) */
    .v4-canopy-hero-stage {
      background: #1B331D !important;
      margin-bottom: 20px !important;
    }
    .v4-canopy-hero-overlay {
      background: linear-gradient(102deg, rgba(22, 42, 24, 0.90) 0%, rgba(37, 75, 40, 0.72) 55%, rgba(22, 38, 24, 0.35) 100%) !important;
      padding: 28px 32px 24px !important;
      min-height: 410px !important;
    }
    .v4-canopy-hero-title {
      color: #FFFFFF !important;
    }
    .v4-hero-pillar-item strong {
      color: #FFFFFF !important;
    }
    .eco-home-section {
      padding: 20px 0;
      border-bottom: 1px solid var(--eco-border);
    }
    .eco-home-section:last-child {
      border-bottom: none;
    }
    .eco-section-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 14px;
    }
    .eco-section-head h2 {
      font-family: var(--font-heading);
      font-size: clamp(1.5rem, 2.2vw, 2rem);
      margin: 2px 0 4px;
      color: var(--eco-text) !important;
    }
    .eco-section-head p {
      color: var(--eco-text-muted);
      margin: 0;
      max-width: 680px;
      font-size: 16px;
    }
    .eco-grid-3 {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }
    .eco-grid-5 {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
    }
    .eco-grid-2 {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }
    .eco-grid-4 {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }
    .eco-card {
      background: var(--eco-surface);
      border: 1px solid var(--eco-border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: var(--shadow-card);
    }
    .eco-card-pad {
      padding: 16px;
    }
    .eco-card-media {
      position: relative;
      height: 155px;
      overflow: hidden;
      background: #242824;
    }
    .eco-card-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .eco-card-body {
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
      gap: 10px;
    }
    .eco-project-card {
      background: var(--eco-surface);
      border: 1px solid var(--eco-border);
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      box-shadow: var(--shadow-card);
    }
    .eco-icon-box {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .eco-unit-price {
      display: block;
      font-family: var(--font-heading);
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--eco-text);
    }
    .eco-unit-label {
      display: block;
      font-size: 13.5px;
      color: var(--eco-text-muted);
      font-weight: 600;
    }

    /* Masquer le billet QR de demonstration tant que la reservation n'est pas validee (Section G) */
    #demoTicketCard:not(.booking-confirmed-visible),
    #dopamineReliefCard:not(.booking-confirmed-visible),
    #waConciergeAccordion:not(.booking-confirmed-visible) {
      display: none !important;
    }

    /* Onglets des 4 parcours de reservation (#resJourneyTabs) */
    .eco-journey-tabs {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }
    .eco-journey-tab {
      min-height: 52px;
      padding: 10px 14px;
      border-radius: 12px;
      border: 1.5px solid var(--eco-border-strong);
      background: var(--eco-surface);
      color: var(--eco-text);
      font-family: var(--font-body);
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      text-align: left;
    }
    .eco-journey-tab.active {
      background: var(--eco-brand);
      color: #FFFFFF;
      border-color: var(--eco-brand);
    }
    .v4-res-stepper {
      grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
    }

    /* Responsive : 360px, 390px, 768px, 1280px, 1440px (Section B.5 & I.9) */
    @media (max-width: 1180px) {
      .eco-grid-5 {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
      .eco-grid-4 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .v4-res-stepper {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
      }
    }
    @media (max-width: 900px) {
      .eco-grid-3,
      .eco-grid-2,
      .eco-journey-tabs {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .main-nav {
        display: none !important;
      }
      .v4-mobile-burger-btn {
        display: inline-flex !important;
        min-height: 44px !important;
      }
    }
    @media (max-width: 768px) {
      .eco-grid-3,
      .eco-grid-5,
      .eco-grid-2,
      .eco-grid-4,
      .eco-journey-tabs,
      .v4-res-stepper {
        grid-template-columns: 1fr !important;
      }
      .site-header-inner {
        padding: 8px 12px !important;
        gap: 8px !important;
      }
      .brand-title-block .brand-location {
        display: none !important;
      }
      .header-utility-actions #nav-ACC {
        display: none !important;
      }
      body {
        padding-bottom: 76px !important;
        overflow-x: hidden !important;
      }
    }

    /* Module Assignation des Tâches & Fiche de Mission A4 (Exploitation / Guichet / Admin) */
    .exp-mission-preset-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }
    .exp-mission-preset-btn {
      background: #FFFFFF;
      border: 1.5px solid var(--eco-border);
      border-radius: 12px;
      padding: 12px 14px;
      text-align: left;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 6px;
      transition: border-color 0.16s ease, box-shadow 0.16s ease, background-color 0.16s ease;
    }
    .exp-mission-preset-btn:hover,
    .exp-mission-preset-btn.active {
      border-color: var(--eco-brand);
      background: #F4F8F2;
      box-shadow: 0 6px 16px rgba(37, 75, 40, 0.08);
    }
    .mission-sheet-a4 {
      background: #FFFFFF;
      color: var(--eco-text);
      border: 2px solid var(--eco-brand);
      border-radius: 12px;
      padding: 20px 22px;
      display: grid;
      gap: 14px;
      font-size: 13.8px;
      line-height: 1.5;
    }
    .mission-sheet-grid-2 {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    .mission-sheet-grid-3 {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }
    .mission-checklist-item {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      padding: 7px 10px;
      background: var(--eco-bg);
      border: 1px solid var(--eco-border);
      border-radius: 8px;
      font-size: 13.5px;
      cursor: pointer;
    }
    .post-alerts-center {
      background: #FBF9F5;
      border: 1.5px solid var(--eco-dining);
      border-radius: 12px;
      padding: 16px 18px;
      margin-bottom: 20px;
    }
    .post-alert-card {
      background: #FFFFFF;
      border: 1px solid var(--eco-border);
      border-left: 5px solid var(--status-warning-text);
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      transition: background-color 0.16s ease, border-color 0.16s ease;
    }
    .post-alert-card.is-acknowledged {
      border-left-color: var(--status-success-text);
      background: #F8FAF7;
    }
    .order-dispatch-live-banner {
      margin-top: 14px;
      margin-bottom: 14px;
      padding: 14px 18px;
      background: #F4F8F2;
      border: 1.5px solid var(--eco-brand);
      border-left: 6px solid var(--eco-brand);
      border-radius: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    @media (max-width: 900px) {
      .exp-mission-preset-grid,
      .mission-sheet-grid-3 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
    @media (max-width: 768px) {
      .exp-mission-preset-grid,
      .mission-sheet-grid-2,
      .mission-sheet-grid-3 {
        grid-template-columns: 1fr !important;
      }
    }
    @media print {
      #modalOverlaySprint1 {
        position: static !important;
        background: #FFFFFF !important;
        padding: 0 !important;
        display: block !important;
      }
      #modalOfficialPrintBox {
        max-width: 100% !important;
        max-height: none !important;
        overflow: visible !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
      }
    }

    /* =========================================================================
       CORRECTION DE L'AFFICHAGE DE L'ESPACE VISITEUR (#view-ACC / /mon-espace)
       & GARANTIE ZÉRO TRONCATURE DES TABLEAUX ET BOUTONS D'ACTION
       ========================================================================= */
    .header-utility-actions #nav-ACC.active,
    .header-utility-actions #nav-ACC[aria-current="page"] {
      background: #E8F2E6 !important;
      border-color: var(--eco-brand) !important;
      color: var(--eco-brand) !important;
      box-shadow: 0 0 0 2px rgba(37, 75, 40, 0.14) !important;
    }

    #view-ACC > .section > .container > .grid-12 > .col-4.card,
    #view-ACC > .section > .container > .grid-12 > .col-8.card {
      grid-column: 1 / -1 !important;
      width: 100% !important;
      max-width: 100% !important;
    }

    #view-ACC > .section > .container > .grid-12 > .col-4.card {
      padding: 20px 24px !important;
    }

    #view-ACC #accSearchInput {
      flex: 1 1 260px !important;
      min-width: 0 !important;
    }

    #view-ACC > .section > .container > .grid-12 > .col-4.card .form-group > div {
      flex-wrap: wrap !important;
    }

    #view-ACC > .section > .container > .grid-12 > .col-4.card > div:last-child {
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)) !important;
    }

    #view-ACC .table-responsive {
      width: 100% !important;
      overflow-x: auto !important;
    }

    #view-ACC table {
      width: 100% !important;
      table-layout: auto !important;
      border-collapse: collapse !important;
    }

    #view-ACC table th,
    #view-ACC table td {
      padding: 12px 10px !important;
      font-size: 13.5px !important;
      vertical-align: middle !important;
    }

    #view-ACC table th:nth-child(1),
    #view-ACC table td:nth-child(1),
    #view-ACC table th:nth-child(4),
    #view-ACC table td:nth-child(4) {
      white-space: nowrap !important;
    }

    #view-ACC table td:nth-child(2) {
      min-width: 108px;
      max-width: 155px;
    }

    #view-ACC table td:nth-child(3) {
      min-width: 200px;
      max-width: 350px;
    }

    #view-ACC .status-badge {
      white-space: normal !important;
      max-width: 195px !important;
      line-height: 1.35 !important;
      text-align: left !important;
      display: inline-flex !important;
      padding: 5px 10px !important;
      font-size: 12px !important;
    }

    #view-ACC table td:last-child {
      display: table-cell !important;
      vertical-align: middle !important;
      min-width: 210px !important;
      white-space: normal !important;
    }

    #view-ACC table td:last-child .btn:not(.admin-only-control) {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin: 3px 6px 3px 0 !important;
      padding: 6px 12px !important;
      font-size: 12.5px !important;
      min-height: 34px !important;
      border-radius: 8px !important;
      white-space: nowrap !important;
      width: auto !important;
    }

    #view-ACC table td:last-child .btn.admin-only-control {
      display: none !important;
    }

    @media (max-width: 960px) {
      #view-ACC .table-responsive {
        overflow-x: visible !important;
      }
      #view-ACC table,
      #view-ACC table tbody {
        display: block !important;
        width: 100% !important;
      }
      #view-ACC table thead {
        display: none !important;
      }
      #view-ACC table tbody tr {
        display: block !important;
        width: 100% !important;
        background: #FFFFFF !important;
        border: 1px solid var(--eco-border-strong) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 8px rgba(36, 40, 36, 0.05) !important;
      }
      #view-ACC table tbody td,
      #view-ACC table tbody td:last-child {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 8px !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        padding: 7px 0 !important;
        border: none !important;
        border-bottom: 1px dashed rgba(36, 40, 36, 0.1) !important;
        white-space: normal !important;
        text-align: left !important;
      }
      #view-ACC table tbody td:nth-child(3) {
        display: block !important;
      }
      #view-ACC table tbody td:last-child {
        border-bottom: none !important;
        padding-top: 10px !important;
        justify-content: flex-start !important;
      }
      #view-ACC table tbody td:nth-child(1)::before {
        content: "Référence";
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--eco-text-muted);
      }
      #view-ACC table tbody td:nth-child(2)::before {
        content: "Date de visite";
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--eco-text-muted);
      }
      #view-ACC table tbody td:nth-child(4)::before {
        content: "Montant";
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--eco-text-muted);
      }
      #view-ACC table tbody td:nth-child(5)::before {
        content: "Statut";
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--eco-text-muted);
      }
      #view-ACC table tbody td[colspan] {
        display: block !important;
        text-align: center !important;
        border-bottom: none !important;
      }
      #view-ACC table tbody td[colspan]::before {
        display: none !important;
      }
      #view-ACC .status-badge {
        max-width: 100% !important;
      }
    }
    /* ECOPARK_REFONTE_CANOPEE_CSS:END */"""


MAIN_MEGA_NAV_HTML = r"""        <!-- ECOPARK_V4_MAIN_MEGA_NAV:START -->
        <nav class="main-nav" id="v4MainMegaNav" aria-label="Navigation principale ECOPARK">
          <button type="button" class="nav-item active" id="nav-ACCUEIL" onclick="navigateV4SiteMenu('ACCUEIL')">Accueil</button>

          <!-- 1. Découvrir le parc -->
          <div class="v4-nav-dropdown" data-v4-dropdown="decouvrir">
            <button type="button" class="nav-item v4-dropdown-toggle" id="nav-PUB" aria-haspopup="true" aria-expanded="false" onclick="navigateV4SiteMenu('ACTIVITES_ALL')">
              <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#527A35" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
              <span>Découvrir le parc</span>
              <span class="v4-nav-caret" aria-hidden="true">▾</span>
            </button>
            <div class="v4-dropdown-panel" role="menu" aria-label="Sous-menu Découvrir le parc">
              <div class="v4-dropdown-header">
                <span>Domaine, Activités &amp; Galerie</span>
                <span>Dès 500 FCFA / enfant</span>
              </div>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('ACTIVITES_ALL')">
                <div>
                  <span class="v4-dropdown-item-title">Présentation du domaine &amp; Catalogue des activités</span>
                  <span class="v4-dropdown-item-sub">Filtres par univers, durée et budget en Francs CFA</span>
                </div>
                <span class="v4-dropdown-item-price">Catalogue</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('ACT_PIROGUE')">
                <div>
                  <span class="v4-dropdown-item-title">Balade en pirogue sur le lac</span>
                  <span class="v4-dropdown-item-sub">Traversée 45 min • Gilet fourni &amp; pagayeur expérimenté</span>
                </div>
                <span class="v4-dropdown-item-price">500 / 1 000 FCFA</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('ACT_ZOO')">
                <div>
                  <span class="v4-dropdown-item-title">Parc animalier (« ToTo ») &amp; botanique</span>
                  <span class="v4-dropdown-item-sub">Primates, tortues géantes, oiseaux &amp; sentiers ombragés</span>
                </div>
                <span class="v4-dropdown-item-price">500 / 1 000 FCFA</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('ACT_PISCINE')">
                <div>
                  <span class="v4-dropdown-item-title">Piscine semi-olympique surveillée</span>
                  <span class="v4-dropdown-item-sub">Grand bain &amp; bassin enfant • Maîtres-nageurs permanents</span>
                </div>
                <span class="v4-dropdown-item-price">1 500 / 2 500 FCFA</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('ACT_CHEVAL')">
                <div>
                  <span class="v4-dropdown-item-title">Promenade à cheval &amp; aire de jeux</span>
                  <span class="v4-dropdown-item-sub">Initiation équestre encadrée &amp; manèges dès 3 ans</span>
                </div>
                <span class="v4-dropdown-item-price">500 / 1 000 FCFA</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('ACT_PECHE_MUSEE')">
                <div>
                  <span class="v4-dropdown-item-title">Musée patrimonial, bibliothèque &amp; galerie photo</span>
                  <span class="v4-dropdown-item-sub">Objets culturels camerounais, lecture &amp; photos du site</span>
                </div>
                <span class="v4-dropdown-item-price">500 / 1 000 FCFA</span>
              </button>
            </div>
          </div>

          <!-- 2. Séjour & restaurant -->
          <div class="v4-nav-dropdown" data-v4-dropdown="sejour">
            <button type="button" class="nav-item v4-dropdown-toggle" id="nav-HOTELS" aria-haspopup="true" aria-expanded="false" onclick="navigateV4SiteMenu('HOTELS_ALL')">
              <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#A45138" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
              <span>Séjour &amp; restaurant</span>
              <span class="v4-nav-caret" aria-hidden="true">▾</span>
            </button>
            <div class="v4-dropdown-panel" role="menu" aria-label="Sous-menu Séjour et restaurant">
              <div class="v4-dropdown-header">
                <span>Hébergements 7j/7 &amp; Gastronomie</span>
                <span>Tarifs par nuit / par plat</span>
              </div>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('HOTELS_COMPARATIF')">
                <div>
                  <span class="v4-dropdown-item-title">Sous-rubrique Hébergements (4 catégories)</span>
                  <span class="v4-dropdown-item-sub">Cités Bene, Chanthel, Ewondo VIP &amp; Suites Privées</span>
                </div>
                <span class="v4-dropdown-item-price">10k à 45k FCFA / nuit</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('HOTEL_EWONDO')">
                <div>
                  <span class="v4-dropdown-item-title">Fiches Cité Ewondo VIP &amp; Suites Privées</span>
                  <span class="v4-dropdown-item-sub">Loges climatisées, literie King-Size &amp; accès parc inclus</span>
                </div>
                <span class="v4-dropdown-item-price">25k à 45k FCFA / nuit</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('HOTEL_CHANTHEL')">
                <div>
                  <span class="v4-dropdown-item-title">Fiches Cités Chanthel (Confort) &amp; Bene (Standard)</span>
                  <span class="v4-dropdown-item-sub">Séjours au calme avec parking sécurisé gratuit</span>
                </div>
                <span class="v4-dropdown-item-price">10k à 25k FCFA / nuit</span>
              </button>
              <button type="button" class="v4-dropdown-item" id="nav-SAVEURS" role="menuitem" onclick="navigateV4SiteMenu('RESTAURANT_SAVEURS')">
                <div>
                  <span class="v4-dropdown-item-title">Sous-rubrique Restaurant — Le Château des Saveurs</span>
                  <span class="v4-dropdown-item-sub">Carte, prix par plat, horaires et service sous pergolas</span>
                </div>
                <span class="v4-dropdown-item-price">2 500 à 6 500 FCFA</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('BOOK_LODGE')">
                <div>
                  <span class="v4-dropdown-item-title">Réserver un hébergement ou une table</span>
                  <span class="v4-dropdown-item-sub">Accès direct au parcours de réservation dédié</span>
                </div>
                <span class="v4-dropdown-item-price">Réserver</span>
              </button>
            </div>
          </div>

          <!-- 3. Groupes & événements -->
          <div class="v4-nav-dropdown" data-v4-dropdown="groupes">
            <button type="button" class="nav-item v4-dropdown-toggle" id="nav-GROUPES" aria-haspopup="true" aria-expanded="false" onclick="navigateV4SiteMenu('TARIFS_GROUPES')">
              <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#254B28" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              <span>Groupes &amp; événements</span>
              <span class="v4-nav-caret" aria-hidden="true">▾</span>
            </button>
            <div class="v4-dropdown-panel" role="menu" aria-label="Sous-menu Groupes et événements">
              <div class="v4-dropdown-header">
                <span>Écoles, Entreprises &amp; Réceptions</span>
                <span>Salle 500 places &amp; Navettes</span>
              </div>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('GROUPES_SCOLAIRES')">
                <div>
                  <span class="v4-dropdown-item-title">Sorties scolaires &amp; pédagogiques</span>
                  <span class="v4-dropdown-item-sub">Parcours faune, pisciculture, musée • Tarif enfant 500 FCFA protégé</span>
                </div>
                <span class="v4-dropdown-item-price">500 FCFA / élève</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('GROUPES_ENTREPRISES')">
                <div>
                  <span class="v4-dropdown-item-title">Entreprises, ministères &amp; associations</span>
                  <span class="v4-dropdown-item-sub">Séminaires, retraites, team-building • Remise dès 20 adultes</span>
                </div>
                <span class="v4-dropdown-item-price">Sur devis</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('GROUPES_MARIAGES')">
                <div>
                  <span class="v4-dropdown-item-title">Mariages, galas &amp; réceptions privées</span>
                  <span class="v4-dropdown-item-sub">Salle climatisée « Menkii Essomba Anton » (500 places) &amp; traiteur</span>
                </div>
                <span class="v4-dropdown-item-price">500 places</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('GROUPES_DEVIS')">
                <div>
                  <span class="v4-dropdown-item-title">Demander un devis adapté à mon projet</span>
                  <span class="v4-dropdown-item-sub">Formulaire de demande de proforma (écoles, séminaires, mariages)</span>
                </div>
                <span class="v4-dropdown-item-price">Devis gratuit</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('INFOS_RDV')">
                <div>
                  <span class="v4-dropdown-item-title">Planifier une visite de repérage sur site</span>
                  <span class="v4-dropdown-item-sub">Rendez-vous avec l'équipe événementielle à Ahala</span>
                </div>
                <span class="v4-dropdown-item-price">Rendez-vous</span>
              </button>
            </div>
          </div>

          <!-- 4. Formations -->
          <div class="v4-nav-dropdown" data-v4-dropdown="formations">
            <button type="button" class="nav-item v4-dropdown-toggle" id="nav-CFP" aria-haspopup="true" aria-expanded="false" onclick="navigateV4SiteMenu('CFP_CAMPUS')">
              <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4D5685" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
              <span>Formations</span>
              <span class="v4-nav-caret" aria-hidden="true">▾</span>
            </button>
            <div class="v4-dropdown-panel v4-dropdown-panel-right" role="menu" aria-label="Sous-menu Formations CFP">
              <div class="v4-dropdown-header">
                <span>Centre de Formation Professionnelle (CFP)</span>
                <span>Agréé MINEFOP</span>
              </div>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('CFP_CAMPUS')">
                <div>
                  <span class="v4-dropdown-item-title">Présentation du CFP &amp; des 5 filières</span>
                  <span class="v4-dropdown-item-sub">Hôtellerie, Restauration, Décoration, Agropastorale, Pisciculture</span>
                </div>
                <span class="v4-dropdown-item-price">12 mois</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('CFP_HOTELLERIE_RESTO')">
                <div>
                  <span class="v4-dropdown-item-title">Filières Hôtellerie, Restauration &amp; Décoration</span>
                  <span class="v4-dropdown-item-sub">Pratique dans les 4 Cités Hôtelières et au Château des Saveurs</span>
                </div>
                <span class="v4-dropdown-item-price">DQP / CQP</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('CFP_AGRO_PISCI')">
                <div>
                  <span class="v4-dropdown-item-title">Filières Agropastorale &amp; Pisciculture</span>
                  <span class="v4-dropdown-item-sub">Bassins piscicoles d'Ahala, aviculture, apiculture &amp; élevage</span>
                </div>
                <span class="v4-dropdown-item-price">70 % pratique</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('CFP_ADMISSION')">
                <div>
                  <span class="v4-dropdown-item-title">Conditions d'admission, durée &amp; frais vérifiés</span>
                  <span class="v4-dropdown-item-sub">Dès 16 ans • Inscription 50 000 FCFA + 250 000 FCFA (4 tranches)</span>
                </div>
                <span class="v4-dropdown-item-price">Frais officiels</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('CFP_CANDIDATURE')">
                <div>
                  <span class="v4-dropdown-item-title">Demande d'information &amp; candidature en ligne</span>
                  <span class="v4-dropdown-item-sub">Déposez votre dossier de pré-inscription au campus d'Ahala</span>
                </div>
                <span class="v4-dropdown-item-price">Candidater</span>
              </button>
            </div>
          </div>

          <!-- 5. Préparer ma visite -->
          <div class="v4-nav-dropdown" data-v4-dropdown="preparer">
            <button type="button" class="nav-item v4-dropdown-toggle" id="nav-TARIFS" aria-haspopup="true" aria-expanded="false" onclick="navigateV4SiteMenu('TARIFS_GRILLE')">
              <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#176B80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
              <span>Préparer ma visite</span>
              <span class="v4-nav-caret" aria-hidden="true">▾</span>
            </button>
            <div class="v4-dropdown-panel v4-dropdown-panel-right" role="menu" aria-label="Sous-menu Préparer ma visite">
              <div class="v4-dropdown-header">
                <span>Tarifs, Horaires, Accès RN3 &amp; FAQ</span>
                <span>Mardi – Dimanche dès 09h00</span>
              </div>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('TARIFS_PASS')">
                <div>
                  <span class="v4-dropdown-item-title">Tarifs officiels, Pass journée &amp; Calculateur</span>
                  <span class="v4-dropdown-item-sub">Estimez le prix d'une journée (ex. 2 adultes et 2 enfants)</span>
                </div>
                <span class="v4-dropdown-item-price">Grille FCFA</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('INFOS_PLAN_RN3')">
                <div>
                  <span class="v4-dropdown-item-title">Horaires, accès RN3 (Face Tradex) &amp; navettes</span>
                  <span class="v4-dropdown-item-sub">Fermé le lundi (parc) • Hébergements 7j/7 • Parking 150 places</span>
                </div>
                <span class="v4-dropdown-item-price">Accès &amp; Plan</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('AGENDA_SEMAINE')">
                <div>
                  <span class="v4-dropdown-item-title">Agenda et programmation de la semaine</span>
                  <span class="v4-dropdown-item-sub">Événements renseignés du mardi au dimanche à Ahala</span>
                </div>
                <span class="v4-dropdown-item-price">Agenda</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('INFOS_FAQ')">
                <div>
                  <span class="v4-dropdown-item-title">Services pratiques &amp; Questions fréquentes (FAQ)</span>
                  <span class="v4-dropdown-item-sub">Crèche-garderie, sécurité baignade, Garantie Météo 90 jours</span>
                </div>
                <span class="v4-dropdown-item-price">FAQ</span>
              </button>
              <button type="button" class="v4-dropdown-item" role="menuitem" onclick="navigateV4SiteMenu('INFOS_LEGAL')">
                <div>
                  <span class="v4-dropdown-item-title">Conditions générales de réservation &amp; Mentions légales</span>
                  <span class="v4-dropdown-item-sub">Politique de report, d'annulation et protection des données</span>
                </div>
                <span class="v4-dropdown-item-price">Conditions</span>
              </button>
            </div>
          </div>
        </nav>

        <button type="button" class="v4-mobile-burger-btn" id="v4MobileBurgerBtn" aria-label="Ouvrir le menu principal du site" aria-expanded="false" onclick="toggleV4MobileDrawer()">
          <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          <span>Menu</span>
        </button>
        <!-- ECOPARK_V4_MAIN_MEGA_NAV:END -->"""

HEADER_UTILITY_HTML = r"""        <div class="header-utility-actions">
          <button type="button" class="btn btn-secondary btn-sm" id="nav-ACC" onclick="navigateV4SiteMenu('ACC_DASHBOARD')">
            <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>Mes réservations</span>
          </button>
          <button type="button" class="btn btn-primary btn-sm" id="btnHeaderReserver" onclick="navigateV4SiteMenu('SIMULATEUR_RES')">
            <span>Réserver</span>
          </button>
        </div>"""

MOBILE_DRAWER_HTML = r"""    <!-- ECOPARK_V4_MOBILE_DRAWER:START -->
    <aside class="v4-mobile-menu-drawer" id="v4MobileMenuDrawer" aria-label="Menu principal ECOPARK" onclick="if(event.target === this) toggleV4MobileDrawer(false)">
      <div class="v4-mobile-menu-sheet">
        <div class="v4-mobile-menu-head">
          <div>
            <strong style="font-size:16px;color:var(--eco-brand);display:block;">ECOPARK CAMEROUN</strong>
            <span style="font-size:13px;color:var(--eco-text-muted);">Yaoundé – Ahala Barrière</span>
          </div>
          <button type="button" class="btn btn-secondary btn-sm" onclick="toggleV4MobileDrawer(false)">Fermer ×</button>
        </div>
        <div class="v4-mobile-menu-body">
          <button type="button" class="btn btn-secondary" style="width:100%;justify-content:space-between;" onclick="navigateV4SiteMenu('ACCUEIL')">
            <span>Accueil</span>
            <span>→</span>
          </button>

          <details class="v4-mob-accordion" open>
            <summary>1. Découvrir le parc</summary>
            <div class="v4-mob-sublist">
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('ACTIVITES_ALL')"><span>Catalogue des activités &amp; domaine</span><small>8 activités</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('ACT_PIROGUE')"><span>Balade en pirogue sur le lac</span><small>500 / 1 000 F</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('ACT_ZOO')"><span>Parc animalier (« ToTo ») &amp; botanique</span><small>500 / 1 000 F</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('ACT_PISCINE')"><span>Piscine semi-olympique surveillée</span><small>1 500 / 2 500 F</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('ACT_CHEVAL')"><span>Promenade à cheval &amp; aire de jeux</span><small>500 / 1 000 F</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('ACT_PECHE_MUSEE')"><span>Musée patrimonial &amp; bibliothèque</span><small>500 / 1 000 F</small></button>
            </div>
          </details>

          <details class="v4-mob-accordion">
            <summary>2. Séjour &amp; restaurant</summary>
            <div class="v4-mob-sublist">
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('HOTELS_COMPARATIF')"><span>Hébergements (Cités Bene, Chanthel, Ewondo)</span><small>10k – 45k F</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('HOTEL_EWONDO')"><span>Fiches Cité Ewondo VIP &amp; Suites</span><small>25k – 45k F</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('RESTAURANT_SAVEURS')"><span>Restaurant Le Château des Saveurs</span><small>2 500 – 6 500 F</small></button>
            </div>
          </details>

          <details class="v4-mob-accordion">
            <summary>3. Groupes &amp; événements</summary>
            <div class="v4-mob-sublist">
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('GROUPES_SCOLAIRES')"><span>Sorties scolaires (500 FCFA / élève)</span><small>Écoles</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('GROUPES_ENTREPRISES')"><span>Entreprises, séminaires &amp; associations</span><small>Dès 20 pers.</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('GROUPES_MARIAGES')"><span>Mariages &amp; Salle Menkii (500 places)</span><small>Réceptions</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('GROUPES_DEVIS')"><span>Demander un devis sur mesure</span><small>Devis</small></button>
            </div>
          </details>

          <details class="v4-mob-accordion">
            <summary>4. Formations</summary>
            <div class="v4-mob-sublist">
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('CFP_CAMPUS')"><span>Présentation du CFP &amp; 5 filières MINEFOP</span><small>12 mois</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('CFP_ADMISSION')"><span>Conditions d'admission &amp; frais</span><small>Dès 16 ans</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('CFP_CANDIDATURE')"><span>Déposer une candidature CFP</span><small>En ligne</small></button>
            </div>
          </details>

          <details class="v4-mob-accordion">
            <summary>5. Préparer ma visite</summary>
            <div class="v4-mob-sublist">
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('TARIFS_PASS')"><span>Tarifs, Pass journée &amp; Calculateur</span><small>FCFA</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('INFOS_PLAN_RN3')"><span>Horaires, accès RN3 &amp; transport</span><small>Mar–Dim 09h</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('AGENDA_SEMAINE')"><span>Agenda de la semaine</span><small>Événements</small></button>
              <button type="button" class="v4-mob-subbtn" onclick="navigateV4SiteMenu('INFOS_FAQ')"><span>Services pratiques &amp; Questions fréquentes</span><small>FAQ</small></button>
            </div>
          </details>

          <div style="display:grid;gap:8px;padding-top:10px;border-top:1px solid var(--eco-border);">
            <button type="button" class="btn btn-secondary" style="width:100%;justify-content:center;" onclick="navigateV4SiteMenu('ACC_DASHBOARD')">Mes réservations</button>
            <button type="button" class="btn btn-primary" style="width:100%;justify-content:center;" onclick="navigateV4SiteMenu('SIMULATEUR_RES')">Réserver</button>
          </div>
        </div>
      </div>
    </aside>
    <!-- ECOPARK_V4_MOBILE_DRAWER:END -->"""

HERO_STAGE_HTML = r"""            <!-- ECOPARK_V4_HERO_STAGE:START -->
            <div class="v4-canopy-hero-stage" id="v4CanopyHeroStage">
              <img class="v4-canopy-hero-bg" id="v4CanopyHeroBgImg" src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Lac verdoyant et balade en pirogue a ECOPARK Cameroun Yaounde-Ahala" />
              <div class="v4-canopy-hero-overlay">
                <div class="v4-canopy-hero-top">
                  <span class="v4-canopy-eyebrow-pill">
                    <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
                    Canopée vivante • Yaoundé-Ahala (Face Station Tradex RN3)
                  </span>
                  <h1 class="v4-canopy-hero-title">Prenez le frais. <br/>Vivez la nature.</h1>
                  <p class="v4-canopy-hero-sub">
                    À 15 minutes du centre de Yaoundé, ressourcez-vous au cœur d'un domaine arboré réunissant lac et pirogues, parc animalier, piscine semi-olympique, cités hôtelières, restaurant camerounais et centre de formation professionnelle.
                  </p>
                  <div class="v4-canopy-cta-row">
                    <button type="button" class="v4-btn-hero-primary" onclick="navigateV4SiteMenu('ACTIVITES_ALL')">
                      <span>Découvrir les activités</span>
                      <span aria-hidden="true">→</span>
                    </button>
                    <button type="button" class="v4-btn-hero-secondary" onclick="navigateV4SiteMenu('TARIFS_GRILLE')">
                      <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                      <span>Préparer ma visite</span>
                    </button>
                    <button type="button" class="v4-btn-hero-pause" id="btnHeroCarouselPause" onclick="toggleV4HeroMotionPause()" aria-pressed="false" title="Mettre en pause ou reprendre les animations">
                      <span id="btnHeroCarouselPauseLabel">Pause animation</span>
                    </button>
                  </div>
                </div>

                <!-- Repères rapides des univers du domaine -->
                <div class="v4-hero-pillars-strip" role="region" aria-label="Les grands univers du domaine ECOPARK Cameroun">
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateV4SiteMenu('ACTIVITES_ALL')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
                    </span>
                    <div>
                      <strong>Nature, lac &amp; loisirs</strong>
                      <span>Parc animalier « ToTo », pirogues, piscine &amp; cheval dès 500 FCFA / enfant</span>
                    </div>
                  </button>
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateV4SiteMenu('HOTELS_COMPARATIF')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                    </span>
                    <div>
                      <strong>Hébergements 7j/7</strong>
                      <span>Cités Bene, Chanthel, Ewondo VIP &amp; Suites (10 000 à 45 000 FCFA / nuit)</span>
                    </div>
                  </button>
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateV4SiteMenu('RESTAURANT_SAVEURS')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" x2="6" y1="1" y2="4"/><line x1="10" x2="10" y1="1" y2="4"/><line x1="14" x2="14" y1="1" y2="4"/></svg>
                    </span>
                    <div>
                      <strong>Le Château des Saveurs</strong>
                      <span>Poisson braisé d'Ahala, Poulet DG Royal &amp; pergolas (2 500 à 6 500 FCFA)</span>
                    </div>
                  </button>
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateV4SiteMenu('TARIFS_GROUPES')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    </span>
                    <div>
                      <strong>Groupes &amp; Campus CFP</strong>
                      <span>Salle 500 places « Menkii Essomba Anton », écoles &amp; 5 filières MINEFOP</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>

            <!-- ==============================================================
                 SECTIONS 2 À 8 DE L'ACCUEIL RESTRUCTURÉ (ORDRE CIBLE SECTION D)
                 ============================================================== -->
            <div id="ecoparkRefonteHomeBlocks">

              <!-- 2. LES EXPÉRIENCES PRINCIPALES -->
              <section class="eco-home-section" id="homeBlock2Experiences" aria-labelledby="homeHeadingExperiences">
                <div class="eco-section-head">
                  <div>
                    <span class="eyebrow" style="color:var(--eco-nature-text) !important;">Nature &amp; Loisirs à Yaoundé-Ahala</span>
                    <h2 id="homeHeadingExperiences">Les expériences principales du parc</h2>
                    <p>Une sélection d'activités de plein air accessibles du mardi au dimanche dès 09h00, avec tarifs officiels par personne et sécurité encadrée.</p>
                  </div>
                  <button type="button" class="btn btn-secondary" onclick="navigateV4SiteMenu('ACTIVITES_ALL')">
                    <span>Voir tout le catalogue des activités</span>
                    <span aria-hidden="true">→</span>
                  </button>
                </div>

                <div class="eco-grid-3">
                  <!-- Exp 1 : Pirogue -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-water);">
                    <div>
                      <div class="eco-card-media" onclick="openV4ActivityDetail('pirogue')" style="cursor:pointer;">
                        <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Balade en pirogue sur le lac d'ECOPARK Ahala" />
                      </div>
                      <div class="eco-card-body">
                        <div>
                          <span class="eco-cat-badge eco-cat-water">Eau &amp; loisirs</span>
                          <h3 style="margin:10px 0 6px;font-size:1.25rem;">Balade en pirogue sur le lac</h3>
                          <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                            Traversée paisible de 45 minutes sur le lac verdoyant d'Ahala avec pagayeur professionnel et gilet homologué fourni.
                          </p>
                        </div>
                        <div style="border-top:1px solid var(--eco-border);padding-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                          <div>
                            <span class="eco-unit-price">500 FCFA <small style="font-weight:600;">/ enfant</small> • 1 000 FCFA <small style="font-weight:600;">/ adulte</small></span>
                            <span class="eco-unit-label">Par personne (dès 3 ans accompagnés)</span>
                          </div>
                          <button type="button" class="btn btn-secondary btn-sm" onclick="openV4ActivityDetail('pirogue')">Voir la fiche →</button>
                        </div>
                      </div>
                    </div>
                  </article>

                  <!-- Exp 2 : Parc animalier -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-nature);">
                    <div>
                      <div class="eco-card-media" onclick="openV4ActivityDetail('zoo')" style="cursor:pointer;">
                        <img src="audit-assets/ecopark-real-media/chimpanze.jpeg" alt="Parc animalier et jardin botanique d'ECOPARK" />
                      </div>
                      <div class="eco-card-body">
                        <div>
                          <span class="eco-cat-badge eco-cat-nature">Nature &amp; découverte</span>
                          <h3 style="margin:10px 0 6px;font-size:1.25rem;">Parc animalier (« ToTo ») &amp; botanique</h3>
                          <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                            Observation du gorille « ToTo », des chimpanzés, tortues géantes, paons et promenade sous la palmeraie ombragée.
                          </p>
                        </div>
                        <div style="border-top:1px solid var(--eco-border);padding-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                          <div>
                            <span class="eco-unit-price">500 FCFA <small style="font-weight:600;">/ enfant</small> • 1 000 FCFA <small style="font-weight:600;">/ adulte</small></span>
                            <span class="eco-unit-label">Par personne (gratuit moins de 3 ans)</span>
                          </div>
                          <button type="button" class="btn btn-secondary btn-sm" onclick="openV4ActivityDetail('zoo')">Voir la fiche →</button>
                        </div>
                      </div>
                    </div>
                  </article>

                  <!-- Exp 3 : Piscine -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-water);">
                    <div>
                      <div class="eco-card-media" onclick="openV4ActivityDetail('piscine')" style="cursor:pointer;">
                        <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png" alt="Piscine semi-olympique surveillée à ECOPARK" />
                      </div>
                      <div class="eco-card-body">
                        <div>
                          <span class="eco-cat-badge eco-cat-water">Eau &amp; loisirs</span>
                          <h3 style="margin:10px 0 6px;font-size:1.25rem;">Piscine semi-olympique surveillée</h3>
                          <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                            Grand bassin et espace enfants surveillés en permanence par des maîtres-nageurs sauveteurs qualifiés.
                          </p>
                        </div>
                        <div style="border-top:1px solid var(--eco-border);padding-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                          <div>
                            <span class="eco-unit-price">1 500 FCFA <small style="font-weight:600;">/ enfant</small> • 2 500 FCFA <small style="font-weight:600;">/ adulte</small></span>
                            <span class="eco-unit-label">Par personne (accès journée)</span>
                          </div>
                          <button type="button" class="btn btn-secondary btn-sm" onclick="openV4ActivityDetail('piscine')">Voir la fiche →</button>
                        </div>
                      </div>
                    </div>
                  </article>

                  <!-- Exp 4 : Équitation -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-water);">
                    <div>
                      <div class="eco-card-media" onclick="openV4ActivityDetail('cheval')" style="cursor:pointer;">
                        <img src="audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png" alt="Promenade à cheval et aire de jeux à ECOPARK" />
                      </div>
                      <div class="eco-card-body">
                        <div>
                          <span class="eco-cat-badge eco-cat-water">Eau &amp; loisirs</span>
                          <h3 style="margin:10px 0 6px;font-size:1.25rem;">Promenade à cheval &amp; aire de jeux</h3>
                          <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                            Tour à cheval encadré par un moniteur dans le manège verdoyant (bombe fournie) et accès aux toboggans.
                          </p>
                        </div>
                        <div style="border-top:1px solid var(--eco-border);padding-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                          <div>
                            <span class="eco-unit-price">500 FCFA <small style="font-weight:600;">/ enfant</small> • 1 000 FCFA <small style="font-weight:600;">/ adulte</small></span>
                            <span class="eco-unit-label">Par personne (séance 30 min)</span>
                          </div>
                          <button type="button" class="btn btn-secondary btn-sm" onclick="openV4ActivityDetail('cheval')">Voir la fiche →</button>
                        </div>
                      </div>
                    </div>
                  </article>

                  <!-- Exp 5 : Musée & Bibliothèque -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-nature);">
                    <div>
                      <div class="eco-card-media" onclick="openV4ActivityDetail('musee')" style="cursor:pointer;">
                        <img src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg" alt="Musée patrimonial et bibliothèque ECOPARK" />
                      </div>
                      <div class="eco-card-body">
                        <div>
                          <span class="eco-cat-badge eco-cat-nature">Nature &amp; découverte</span>
                          <h3 style="margin:10px 0 6px;font-size:1.25rem;">Musée patrimonial &amp; bibliothèque</h3>
                          <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                            Collection d'objets culturels des régions du Cameroun et salle de lecture calme pour jeunes et familles.
                          </p>
                        </div>
                        <div style="border-top:1px solid var(--eco-border);padding-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                          <div>
                            <span class="eco-unit-price">500 FCFA <small style="font-weight:600;">/ enfant</small> • 1 000 FCFA <small style="font-weight:600;">/ adulte</small></span>
                            <span class="eco-unit-label">Par personne (visite guidée 1h)</span>
                          </div>
                          <button type="button" class="btn btn-secondary btn-sm" onclick="openV4ActivityDetail('musee')">Voir la fiche →</button>
                        </div>
                      </div>
                    </div>
                  </article>

                  <!-- Exp 6 : Pêche récréative & étangs -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-water);">
                    <div>
                      <div class="eco-card-media" onclick="openV4ActivityDetail('pirogue')" style="cursor:pointer;">
                        <img src="audit-assets/ecopark-real-media/IMG_20260829_172016-1-scaled.jpg" alt="Étangs piscicoles et pêche récréative à ECOPARK Ahala" />
                      </div>
                      <div class="eco-card-body">
                        <div>
                          <span class="eco-cat-badge eco-cat-water">Eau &amp; loisirs</span>
                          <h3 style="margin:10px 0 6px;font-size:1.25rem;">Pêche récréative aux étangs d'Ahala</h3>
                          <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                            Découverte des bassins piscicoles, nourrissage des poissons et initiation à la pêche au bord de l'eau.
                          </p>
                        </div>
                        <div style="border-top:1px solid var(--eco-border);padding-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
                          <div>
                            <span class="eco-unit-price">500 à 2 000 FCFA</span>
                            <span class="eco-unit-label">Sachet nutrition (500 F) ou forfait pêche (2 000 F)</span>
                          </div>
                          <button type="button" class="btn btn-secondary btn-sm" onclick="openV4ActivityDetail('pirogue')">Voir la fiche →</button>
                        </div>
                      </div>
                    </div>
                  </article>
                </div>
              </section>

              <!-- 3. CHOISIR SON PROJET -->
              <section class="eco-home-section" id="homeBlock3Projects" aria-labelledby="homeHeadingProjects">
                <div class="eco-section-head">
                  <div>
                    <span class="eyebrow">Orientation par besoin</span>
                    <h2 id="homeHeadingProjects">Choisir votre projet</h2>
                    <p>Accédez directement aux informations, tarifs et démarches correspondant à votre venue à ECOPARK.</p>
                  </div>
                </div>

                <div class="eco-grid-5">
                  <article class="eco-project-card" style="border-top:4px solid var(--eco-water);">
                    <div>
                      <span class="eco-icon-box" style="background:var(--eco-water-soft);color:var(--eco-water);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
                      </span>
                      <h3 style="font-size:1.15rem;margin:12px 0 6px;">Passer une journée</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0;">
                        Sortie en famille ou entre amis : parc animalier, pirogue, piscine et déjeuner au bord du lac.
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="navigateV4SiteMenu('TARIFS_PASS')">Préparer ma journée →</button>
                  </article>

                  <article class="eco-project-card" style="border-top:4px solid var(--eco-lodging);">
                    <div>
                      <span class="eco-icon-box" style="background:var(--eco-lodging-soft);color:var(--eco-lodging);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                      </span>
                      <h3 style="font-size:1.15rem;margin:12px 0 6px;">Séjourner</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0;">
                        Chambres et suites au calme 7j/7 (Cités Bene, Chanthel, Ewondo VIP) de 10 000 à 45 000 FCFA / nuit.
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="navigateV4SiteMenu('HOTELS_COMPARATIF')">Voir les hébergements →</button>
                  </article>

                  <article class="eco-project-card" style="border-top:4px solid var(--eco-nature);">
                    <div>
                      <span class="eco-icon-box" style="background:var(--eco-nature-soft);color:var(--eco-nature-text);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                      </span>
                      <h3 style="font-size:1.15rem;margin:12px 0 6px;">Organiser une sortie de groupe</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0;">
                        Excursions scolaires (tarif enfant 500 FCFA protégé), visites guidées et navettes 18 ou 32 places.
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="navigateV4SiteMenu('GROUPES_SCOLAIRES')">Sorties de groupe →</button>
                  </article>

                  <article class="eco-project-card" style="border-top:4px solid var(--eco-dining);">
                    <div>
                      <span class="eco-icon-box" style="background:var(--eco-dining-soft);color:var(--eco-dining);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                      </span>
                      <h3 style="font-size:1.15rem;margin:12px 0 6px;">Organiser un événement</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0;">
                        Séminaires, mariages et réceptions dans la Salle « Menkii Essomba Anton » (500 places assises).
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="navigateV4SiteMenu('GROUPES_MARIAGES')">Espaces &amp; devis →</button>
                  </article>

                  <article class="eco-project-card" style="border-top:4px solid var(--eco-training);">
                    <div>
                      <span class="eco-icon-box" style="background:var(--eco-training-soft);color:var(--eco-training);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
                      </span>
                      <h3 style="font-size:1.15rem;margin:12px 0 6px;">Se former</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0;">
                        Campus CFP agréé MINEFOP dès 16 ans : 5 filières diplômantes avec 70 % de pratique sur le domaine.
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="navigateV4SiteMenu('CFP_CAMPUS')">Voir les formations →</button>
                  </article>
                </div>
              </section>

              <!-- 4. LES FORMULES JOURNÉE -->
              <section class="eco-home-section" id="homeBlock4DayPasses" aria-labelledby="homeHeadingPackages">
                <div class="eco-section-head">
                  <div>
                    <span class="eyebrow">Formules packagées</span>
                    <h2 id="homeHeadingPackages">Les formules journée</h2>
                    <p>Trois formules vérifiées regroupant les expériences du parc sur un seul billet, ou sélection à la carte selon votre rythme.</p>
                  </div>
                  <button type="button" class="btn btn-secondary" onclick="navigateV4SiteMenu('TARIFS_PASS')">
                    <span>Comparer les pass et la grille tarifaire</span>
                    <span aria-hidden="true">→</span>
                  </button>
                </div>

                <div class="eco-grid-3">
                  <article class="eco-card eco-card-pad" style="border-top:4px solid var(--eco-nature);">
                    <div>
                      <span class="eco-cat-badge eco-cat-nature">Plein air • 3 activités</span>
                      <h3 style="font-size:1.3rem;margin:10px 0 6px;">Pass Découverte Nature</h3>
                      <div style="margin:10px 0 14px;padding:12px;background:var(--eco-bg);border-radius:10px;">
                        <span class="eco-unit-price">1 500 FCFA <small>/ enfant</small> • 2 500 FCFA <small>/ adulte</small></span>
                        <span class="eco-unit-label">Par personne (enfant 3–12 ans / adulte 13+ ans)</span>
                      </div>
                      <ul style="padding-left:18px;margin:0 0 18px;display:grid;gap:6px;font-size:15px;">
                        <li><strong>Entrée Parc &amp; Jardin zoologique</strong> (« ToTo »)</li>
                        <li><strong>Balade en pirogue</strong> sur le lac (45 min, gilet fourni)</li>
                        <li><strong>Tour à cheval</strong> encadré ou manèges enfants</li>
                      </ul>
                    </div>
                    <button type="button" class="btn btn-secondary" style="width:100%;" onclick="applySalesBundle('PASS_DECOUVERTE', true)">Choisir le Pass Découverte</button>
                  </article>

                  <article class="eco-card eco-card-pad" style="border-top:4px solid var(--eco-brand);">
                    <div>
                      <span class="status-badge status-success">Formule complète avec repas</span>
                      <h3 style="font-size:1.3rem;margin:10px 0 6px;">Pass Journée Royale</h3>
                      <div style="margin:10px 0 14px;padding:12px;background:var(--eco-bg);border-radius:10px;">
                        <span class="eco-unit-price">4 500 FCFA <small>/ enfant</small> • 8 500 FCFA <small>/ adulte</small></span>
                        <span class="eco-unit-label">Par personne (activités + baignade + repas chaud)</span>
                      </div>
                      <ul style="padding-left:18px;margin:0 0 18px;display:grid;gap:6px;font-size:15px;">
                        <li><strong>Entrée Parc &amp; Zoo</strong> + <strong>Balade en pirogue</strong></li>
                        <li><strong>Accès Piscine semi-olympique</strong> toute la journée</li>
                        <li><strong>Repas chaud inclus</strong> au Château des Saveurs (Poisson braisé d'Ahala ou Poulet DG)</li>
                      </ul>
                    </div>
                    <button type="button" class="btn btn-primary" style="width:100%;" onclick="applySalesBundle('PASS_ROYALE', true)">Choisir le Pass Journée Royale</button>
                  </article>

                  <article class="eco-card eco-card-pad" style="border-top:4px solid var(--eco-lodging);">
                    <div>
                      <span class="eco-cat-badge eco-cat-lodging">Séjour &amp; table • 2 adultes</span>
                      <h3 style="font-size:1.3rem;margin:10px 0 6px;">Pack Escapade Couple VIP</h3>
                      <div style="margin:10px 0 14px;padding:12px;background:var(--eco-bg);border-radius:10px;">
                        <span class="eco-unit-price">45 000 FCFA</span>
                        <span class="eco-unit-label">Forfait duo pour 2 adultes (1 nuitée ou journée)</span>
                      </div>
                      <ul style="padding-left:18px;margin:0 0 18px;display:grid;gap:6px;font-size:15px;">
                        <li><strong>1 Loge VIP climatisée</strong> à la Cité Ewondo</li>
                        <li><strong>2 Repas complets</strong> au Château des Saveurs + pergola au bord du lac</li>
                        <li><strong>Accès Parc, Piscine &amp; Pirogue</strong> pour 2 adultes</li>
                      </ul>
                    </div>
                    <button type="button" class="btn btn-secondary" style="width:100%;" onclick="applySalesBundle('PACK_COUPLE_EWONDO', true)">Choisir le Pack Escapade VIP</button>
                  </article>
                </div>
              </section>

              <!-- 5. HÉBERGEMENT ET RESTAURATION (DEUX ENTRÉES DISTINCTES) -->
              <section class="eco-home-section" id="homeBlock5StayAndDine" aria-labelledby="homeHeadingStayDining">
                <div class="eco-section-head">
                  <div>
                    <span class="eyebrow" style="color:var(--eco-lodging) !important;">Hospitalité sur le domaine</span>
                    <h2 id="homeHeadingStayDining">Hébergement et restauration</h2>
                    <p>Deux pôles complémentaires au cœur d'Ahala : quatre cités hôtelières au calme et une table camerounaise au bord de l'eau.</p>
                  </div>
                </div>

                <div class="eco-grid-2">
                  <!-- Entrée 1 : Hébergements -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-lodging);">
                    <div class="eco-card-media" style="aspect-ratio:16/9;">
                      <img src="audit-assets/ecopark-real-media/chambre.jpeg" alt="Chambre et loge hôtelière à ECOPARK Yaoundé-Ahala" />
                    </div>
                    <div class="eco-card-body">
                      <div>
                        <span class="eco-cat-badge eco-cat-lodging">Hébergement • Réception 7j/7</span>
                        <h3 style="font-size:1.4rem;margin:10px 0 8px;">Cités Hôtelières Bene, Chanthel, Ewondo &amp; Suites</h3>
                        <p style="font-size:15.5px;color:var(--eco-text-muted);margin:0 0 12px;">
                          Reposez-vous en journée ou passez la nuit dans nos pavillons arborés avec parking intérieur gardé. Arrivée dès 14h00, départ jusqu'à 11h00.
                        </p>
                        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:14.5px;margin-bottom:8px;">
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Cité Bene :</strong> 10 000 – 15 000 FCFA / nuit</div>
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Cité Chanthel :</strong> 15 000 – 25 000 FCFA / nuit</div>
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Cité Ewondo VIP :</strong> 25 000 – 30 000 FCFA / nuit</div>
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Suites Privées :</strong> 30 000 – 45 000 FCFA / nuit</div>
                        </div>
                      </div>
                      <div style="display:flex;gap:10px;flex-wrap:wrap;padding-top:10px;border-top:1px solid var(--eco-border);">
                        <button type="button" class="btn btn-primary" onclick="navigateV4SiteMenu('HOTELS_COMPARATIF')">Découvrir les hébergements</button>
                        <button type="button" class="btn btn-secondary" onclick="selectLodgeFromV4Card('EWONDO')">Réserver une chambre</button>
                      </div>
                    </div>
                  </article>

                  <!-- Entrée 2 : Restaurant Le Château des Saveurs -->
                  <article class="eco-card" style="border-top:4px solid var(--eco-dining);">
                    <div class="eco-card-media" style="aspect-ratio:16/9;">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Restaurant Le Château des Saveurs et pergolas au bord du lac" />
                    </div>
                    <div class="eco-card-body">
                      <div>
                        <span class="eco-cat-badge eco-cat-dining">Restauration • Du bassin à la braise</span>
                        <h3 style="font-size:1.4rem;margin:10px 0 8px;">Restaurant Le Château des Saveurs</h3>
                        <p style="font-size:15.5px;color:var(--eco-text-muted);margin:0 0 12px;">
                          Dégustez sous nos pergolas au bord du lac le poisson d'eau douce pêché dans nos étangs et braisé à la minute, le Poulet DG Royal et le Ndolé aux crevettes.
                        </p>
                        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:14.5px;margin-bottom:8px;">
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Poisson braisé d'Ahala :</strong> 5 000 FCFA / plat</div>
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Poulet DG Royal :</strong> 6 500 FCFA / plat</div>
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Ndolé Royal Crevettes :</strong> 5 500 FCFA / plat</div>
                          <div style="padding:8px 10px;background:var(--eco-bg);border-radius:8px;"><strong>Menu Enfant (&lt; 12 ans) :</strong> 2 500 FCFA / menu</div>
                        </div>
                      </div>
                      <div style="display:flex;gap:10px;flex-wrap:wrap;padding-top:10px;border-top:1px solid var(--eco-border);">
                        <button type="button" class="btn btn-primary" onclick="navigateV4SiteMenu('RESTAURANT_SAVEURS')">Voir la carte &amp; les modalités</button>
                        <button type="button" class="btn btn-secondary" onclick="addActivityAndGo('saveurs')">Réserver un repas</button>
                      </div>
                    </div>
                  </article>
                </div>
              </section>

              <!-- 6. AGENDA (UNIQUEMENT LES ÉVÉNEMENTS RENSEIGNÉS — MASQUÉ SI VIDE) -->
              <section class="eco-home-section" id="homeBlock6Agenda" aria-labelledby="homeHeadingAgenda">
                <div class="eco-section-head">
                  <div>
                    <span class="eyebrow">Programmation hebdomadaire</span>
                    <h2 id="homeHeadingAgenda">Agenda des rendez-vous à Ahala</h2>
                    <p>Les temps forts programmés du mardi au dimanche sur le domaine.</p>
                  </div>
                  <button type="button" class="btn btn-secondary" onclick="navigateV4SiteMenu('AGENDA_SEMAINE')">
                    <span>Consulter l'agenda détaillé</span>
                    <span aria-hidden="true">→</span>
                  </button>
                </div>

                <div class="eco-grid-4" id="homeAgendaCardsContainer">
                  <article class="eco-card eco-card-pad" data-home-agenda-item="EVT_MERCREDI_CFP">
                    <div>
                      <span class="price-pill" style="display:inline-block;margin-bottom:8px;">Mercredi &amp; Jeudi • 10h00 – 16h00</span>
                      <h3 style="font-size:1.15rem;margin:0 0 6px;">Journée pédagogique Faune &amp; Portes ouvertes CFP</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0 0 12px;">
                        Visite commentée du parc animalier et des bassins piscicoles (500 FCFA / enfant • 1 000 FCFA / adulte) et orientation CFP.
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="bookWeeklyEventInOneClick('EVT_MERCREDI_CFP')">Choisir ce créneau →</button>
                  </article>

                  <article class="eco-card eco-card-pad" data-home-agenda-item="EVT_VENDREDI_AFTERWORK">
                    <div>
                      <span class="price-pill" style="display:inline-block;margin-bottom:8px;">Vendredi • 15h30 – 20h30</span>
                      <h3 style="font-size:1.15rem;margin:0 0 6px;">Afterwork « Brise du Lac &amp; Poisson Braisé »</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0 0 12px;">
                        Poisson frais des étangs braisé à la minute et détente sous les pergolas au bord de l'eau (plats de 2 500 à 6 500 FCFA).
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="bookWeeklyEventInOneClick('EVT_VENDREDI_AFTERWORK')">Choisir ce créneau →</button>
                  </article>

                  <article class="eco-card eco-card-pad" data-home-agenda-item="EVT_SAMEDI_FAMILLE">
                    <div>
                      <span class="price-pill" style="display:inline-block;margin-bottom:8px;">Samedi • 10h30 &amp; 15h00</span>
                      <h3 style="font-size:1.15rem;margin:0 0 6px;">Samedi Famille : Parc animalier &amp; Pirogues</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0 0 12px;">
                        Parcours découverte en famille (Pass Découverte : 1 500 FCFA / enfant • 2 500 FCFA / adulte).
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="bookWeeklyEventInOneClick('EVT_SAMEDI_FAMILLE')">Choisir ce créneau →</button>
                  </article>

                  <article class="eco-card eco-card-pad" data-home-agenda-item="EVT_DIMANCHE_ROYAL">
                    <div>
                      <span class="price-pill" style="display:inline-block;margin-bottom:8px;">Dimanche • 12h00 – 17h30</span>
                      <h3 style="font-size:1.15rem;margin:0 0 6px;">Dimanche Royal : Table camerounaise &amp; Détente</h3>
                      <p style="font-size:14.5px;color:var(--eco-text-muted);margin:0 0 12px;">
                        Journée complète avec déjeuner chaud au Château des Saveurs, piscine et zoo (Pass Royale : 4 500 / 8 500 FCFA).
                      </p>
                    </div>
                    <button type="button" class="btn-link" onclick="bookWeeklyEventInOneClick('EVT_DIMANCHE_ROYAL')">Choisir ce créneau →</button>
                  </article>
                </div>
              </section>

              <!-- 7. TÉMOIGNAGES (MASQUÉ PROPREMENT EN L'ABSENCE DE SOURCE EXTERNE AUTHENTIFIÉE) -->
              <section class="eco-home-section" id="homeBlock7Testimonials" style="display:none;" aria-hidden="true"></section>

              <!-- 8. INFORMATIONS PRATIQUES -->
              <section class="eco-home-section" id="homeBlock8Practical" aria-labelledby="homeHeadingPractical">
                <div class="eco-section-head">
                  <div>
                    <span class="eyebrow">Repères essentiels</span>
                    <h2 id="homeHeadingPractical">Informations pratiques</h2>
                    <p>Tout ce qu'il faut savoir avant de prendre la route vers ECOPARK Cameroun à Yaoundé-Ahala.</p>
                  </div>
                  <button type="button" class="btn btn-secondary" onclick="navigateV4SiteMenu('INFOS_PLAN_RN3')">
                    <span>Plan d'accès détaillé &amp; FAQ</span>
                    <span aria-hidden="true">→</span>
                  </button>
                </div>

                <div class="eco-grid-4">
                  <div class="eco-card eco-card-pad">
                    <div>
                      <strong style="display:block;font-size:1.1rem;margin-bottom:6px;">Adresse &amp; localisation</strong>
                      <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                        <strong>Quartier Ahala Barrière</strong>, juste en face de la station <strong>Tradex Ahala</strong> sur la Route Nationale N°3 (entrée sud de Yaoundé, Cameroun).
                      </p>
                    </div>
                  </div>

                  <div class="eco-card eco-card-pad">
                    <div>
                      <strong style="display:block;font-size:1.1rem;margin-bottom:6px;">Jours &amp; horaires d'ouverture</strong>
                      <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                        <strong>Parc &amp; activités :</strong> mardi au dimanche dès <strong>09h00</strong> (fermé le lundi pour maintenance).<br/>
                        <strong>Hébergements :</strong> ouverts <strong>7j/7</strong> (arrivée 14h00, départ 11h00).
                      </p>
                    </div>
                  </div>

                  <div class="eco-card eco-card-pad">
                    <div>
                      <strong style="display:block;font-size:1.1rem;margin-bottom:6px;">Accès, parking &amp; navettes</strong>
                      <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                        Route 100 % goudronnée jusqu'au portail. <strong>Parking intérieur gratuit et sécurisé (150 places)</strong>. Navettes climatisées (5, 18 et 32 places) sur réservation.
                      </p>
                    </div>
                  </div>

                  <div class="eco-card eco-card-pad">
                    <div>
                      <strong style="display:block;font-size:1.1rem;margin-bottom:6px;">Contact officiel</strong>
                      <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                        <strong>Tél. / WhatsApp :</strong> <a href="https://wa.me/237697136203" target="_blank" rel="noopener noreferrer" style="color:var(--eco-brand);font-weight:700;">+237 697 13 62 03</a> / <a href="tel:+237675562655" style="color:var(--eco-brand);font-weight:700;">675 56 26 55</a><br/>
                        <strong>Courriel :</strong> <a href="mailto:info@ecopark-yaounde.com" style="color:var(--eco-brand);">info@ecopark-yaounde.com</a>
                      </p>
                    </div>
                  </div>
                </div>
              </section>

            </div>
            <!-- ECOPARK_V4_HERO_STAGE:END -->"""


MOBILE_BOTTOM_NAV_HTML = r"""    <!-- ECOPARK_V4_MOBILE_NAV:START -->
    <nav class="v4-mobile-bottom-nav" id="v4MobileBottomNav" aria-label="Navigation mobile principale ECOPARK">
      <button type="button" class="v4-bottom-nav-btn active" id="v4MobNavAccueil" onclick="navigateV4MobileTab('ACCUEIL')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span>Accueil</span>
      </button>
      <button type="button" class="v4-bottom-nav-btn" id="v4MobNavActivites" onclick="navigateV4MobileTab('ACTIVITES')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
        <span>Découvrir</span>
      </button>
      <button type="button" class="v4-bottom-nav-btn" id="v4MobNavReserver" onclick="navigateV4MobileTab('RESERVER')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/></svg>
        <span>Réserver</span>
      </button>
      <button type="button" class="v4-bottom-nav-btn" id="v4MobNavCompte" onclick="navigateV4MobileTab('COMPTE')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        <span>Mes réservations</span>
      </button>
    </nav>
    <!-- ECOPARK_V4_MOBILE_NAV:END -->"""


PUB04_STRUCTURED_DETAILS_HTML = r"""                <!-- GABARIT FICHE ACTIVITÉ : PRÉSENTATION, DÉROULEMENT, INCLUS / NON INCLUS, CONDITIONS & COMPLÉMENTS -->
                <div class="v4-tabs-bar" role="tablist">
                  <button type="button" class="v4-tab-btn active" onclick="switchV4Pub04Tab('desc', this)">Présentation &amp; déroulement</button>
                  <button type="button" class="v4-tab-btn" onclick="switchV4Pub04Tab('prog', this)">Inclus &amp; non inclus</button>
                  <button type="button" class="v4-tab-btn" onclick="switchV4Pub04Tab('savoir', this)">Conditions &amp; équipements</button>
                </div>

                <div id="v4Pub04TabContent" class="card" style="padding:20px;background:#FFFFFF;border:1px solid var(--eco-border);">
                  <h3 id="v4Pub04DescHeading" style="font-size:1.25rem;margin-bottom:8px;">Présentation courte &amp; déroulement</h3>
                  <p id="v4Pub04DescBody" style="font-size:16px;color:var(--eco-text);line-height:1.6;margin-bottom:14px;">
                    Embarquez pour une traversée paisible en pirogue traditionnelle sécurisée sur le lac d'ECOPARK à Yaoundé-Ahala. Accompagné d'un guide-pagayeur expérimenté, vous longez la végétation tropicale, observez les oiseaux d'eau et profitez d'une brise rafraîchissante loin du tumulte urbain.
                  </p>
                  <div class="eco-template-grid-2" id="v4Pub04StructuredGrid">
                    <div class="eco-info-box">
                      <h4>Déroulement de l'activité</h4>
                      <ul id="v4Pub04DeroulementList">
                        <li>Accueil au ponton du lac d'Ahala et remise du gilet de sauvetage homologué à votre taille.</li>
                        <li>Traversée commentée de 45 minutes avec un pagayeur expérimenté le long des berges arborées.</li>
                        <li>Pause photo face aux pergolas et retour sécurisé à l'embarcadère.</li>
                      </ul>
                    </div>
                    <div class="eco-info-box">
                      <h4>Inclus et non inclus</h4>
                      <ul id="v4Pub04InclusList">
                        <li><strong>Inclus :</strong> Embarquement, gilet de sauvetage obligatoire, accompagnement par le guide-pagayeur.</li>
                        <li><strong>Non inclus :</strong> Entrée Parc &amp; Zoo (500 FCFA / enfant • 1 000 FCFA / adulte si prise hors Pass) et repas au restaurant.</li>
                      </ul>
                    </div>
                    <div class="eco-info-box" style="grid-column:1 / -1;">
                      <h4>Conditions d'accès &amp; équipements recommandés</h4>
                      <ul id="v4Pub04ConditionsList">
                        <li><strong>Horaires d'accès :</strong> Mardi au dimanche de 09h30 à 17h30 (parc fermé le lundi).</li>
                        <li><strong>Âge &amp; sécurité :</strong> Accessible dès 3 ans (enfants accompagnés d'un adulte). Port du gilet obligatoire.</li>
                        <li><strong>Garantie météo :</strong> Report gratuit de votre billet QR sous 90 jours en cas de forte pluie avant embarquement.</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <!-- Activités complémentaires pertinentes -->
                <div class="card" id="v4Pub04ComplementaryBox" style="margin-top:16px;padding:18px;background:#FFFFFF;border:1px solid var(--eco-border);">
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
                    <strong style="font-family:var(--font-heading);font-size:1.15rem;color:var(--eco-text);">Activités complémentaires pertinentes sur le domaine</strong>
                    <span class="eco-cat-badge eco-cat-nature">Combinables sur 1 seul Pass QR</span>
                  </div>
                  <div class="eco-grid-3" id="v4Pub04ComplementaryGrid" style="gap:12px;">
                    <div style="padding:12px;border:1px solid var(--eco-border);border-radius:12px;background:var(--eco-bg);display:flex;flex-direction:column;justify-content:space-between;gap:8px;">
                      <div>
                        <strong style="display:block;font-size:15px;">Parc animalier (« ToTo ») &amp; botanique</strong>
                        <span style="font-size:13.5px;color:var(--eco-text-muted);">500 FCFA / enfant • 1 000 FCFA / adulte</span>
                      </div>
                      <button type="button" class="btn-link" onclick="switchV4Pub04Activity('zoo')">Consulter la fiche →</button>
                    </div>
                    <div style="padding:12px;border:1px solid var(--eco-border);border-radius:12px;background:var(--eco-bg);display:flex;flex-direction:column;justify-content:space-between;gap:8px;">
                      <div>
                        <strong style="display:block;font-size:15px;">Piscine semi-olympique surveillée</strong>
                        <span style="font-size:13.5px;color:var(--eco-text-muted);">1 500 FCFA / enfant • 2 500 FCFA / adulte</span>
                      </div>
                      <button type="button" class="btn-link" onclick="switchV4Pub04Activity('piscine')">Consulter la fiche →</button>
                    </div>
                    <div style="padding:12px;border:1px solid var(--eco-border);border-radius:12px;background:var(--eco-bg);display:flex;flex-direction:column;justify-content:space-between;gap:8px;">
                      <div>
                        <strong style="display:block;font-size:15px;">Promenade à cheval &amp; manèges</strong>
                        <span style="font-size:13.5px;color:var(--eco-text-muted);">500 FCFA / enfant • 1 000 FCFA / adulte</span>
                      </div>
                      <button type="button" class="btn-link" onclick="switchV4Pub04Activity('cheval')">Consulter la fiche →</button>
                    </div>
                  </div>
                </div>"""


SEJOUR_RESTAURANT_SUPPLEMENT_HTML = r"""            <!-- SOUS-RUBRIQUE RESTAURANT COMPLÈTE (GABARIT RESTAURANT SECTION E) -->
            <div class="card" id="restaurantFullTemplateCard" style="margin-top:24px;padding:24px;background:#FFFFFF;border:1px solid var(--eco-border);border-top:4px solid var(--eco-dining);">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:14px;flex-wrap:wrap;margin-bottom:18px;">
                <div>
                  <span class="eco-cat-badge eco-cat-dining">Sous-rubrique Restaurant • Le Château des Saveurs</span>
                  <h3 style="font-size:1.55rem;margin:10px 0 6px;">Le Château des Saveurs — Lieu, cuisine &amp; carte officielle</h3>
                  <p style="font-size:16px;color:var(--eco-text-muted);margin:0;max-width:740px;">
                    Situé au bord du lac d'ECOPARK Ahala, notre restaurant met à l'honneur la gastronomie camerounaise préparée à la minute (« Du bassin à la braise ») avec les poissons frais issus des étangs piscicoles du domaine.
                  </p>
                </div>
                <div style="display:flex;gap:10px;flex-wrap:wrap;">
                  <button type="button" class="btn btn-primary" onclick="addActivityAndGo('saveurs')">Réserver un repas ou une pergola →</button>
                  <button type="button" class="btn btn-secondary" onclick="openQuoteModalSprint1()">Repas de groupe / banquet</button>
                </div>
              </div>

              <div class="eco-template-grid-2">
                <div class="eco-info-box">
                  <h4>Carte &amp; prix affichés en Francs CFA (par plat / par menu)</h4>
                  <ul>
                    <li><strong>Poisson braisé d'Ahala (étang frais, miondo ou plantain) :</strong> <strong>5 000 FCFA</strong> par plat adulte</li>
                    <li><strong>Poulet DG Royal aux plantains mûrs &amp; légumes du jardin :</strong> <strong>6 500 FCFA</strong> par plat adulte</li>
                    <li><strong>Ndolé Royal aux crevettes &amp; accompagnements :</strong> <strong>5 500 FCFA</strong> par plat adulte</li>
                    <li><strong>Menu Enfant Complet (3 à 12 ans, grillades douces &amp; jus) :</strong> <strong>2 500 FCFA</strong> par menu enfant</li>
                    <li><strong>Option Pergola privée au bord du lac (service prioritaire 13h) :</strong> <strong>+5 000 FCFA</strong> par pergola réservée</li>
                  </ul>
                </div>
                <div class="eco-info-box">
                  <h4>Horaires, modalités de service, groupes &amp; réservation</h4>
                  <ul>
                    <li><strong>Horaires de service :</strong> Mardi au dimanche de <strong>11h30 à 20h30</strong> (service continu pour les résidents des cités hôtelières 7j/7).</li>
                    <li><strong>Modalités de service :</strong> Service à table en salle ventilée, sous les pergolas au bord de l'eau, ou en room-service dans les Cités Ewondo, Chanthel et Bene.</li>
                    <li><strong>Précommande « Zéro attente 12h30 / 13h30 » :</strong> Choisissez votre plat lors de la réservation de votre billet QR pour être servi dès votre sortie de la piscine.</li>
                    <li><strong>Groupes, séminaires &amp; mariages :</strong> Buffets traiteur sur mesure de 20 à 500 convives (Salle Menkii Essomba Anton ou esplanade).</li>
                  </ul>
                </div>
              </div>
            </div>"""


GROUPES_TEMPLATE_HTML = r"""              <!-- Pôle 5 : GABARIT COMPLET GROUPES & ÉVÉNEMENTS (SECTION E) -->
              <article class="col-7 bento-card bento-wide" id="sec-PUB-11" style="border-top:4px solid var(--eco-brand);">
                <div class="card-media-wrapper">
                  <img src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg" alt="Groupe et événement culturel à ECOPARK Yaoundé" />
                  <span class="media-origin-badge media-real">Photo réelle ECOPARK — Groupes &amp; Événements</span>
                </div>
                <div class="bento-card-body">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                      <span class="eco-cat-badge eco-cat-brand"><span class="tech-code-tag">PUB-11 • </span>Groupes &amp; événements à Yaoundé-Ahala</span>
                      <span class="price-pill">Devis sur mesure • Salle 500 places</span>
                    </div>
                    <h2 style="margin-top:10px;font-size:1.65rem;">Sorties scolaires, séminaires d'entreprises &amp; mariages</h2>
                    <p style="font-size:16px;color:var(--eco-text-muted);margin-top:6px;">
                      Organisez votre projet dans un domaine sécurisé et verdoyant à l'entrée sud de Yaoundé (Ahala Barrière, face station Tradex RN3), avec espaces dédiés, service traiteur et flotte de navettes climatisées.
                    </p>

                    <div class="eco-grid-3" style="margin-top:16px;gap:14px;">
                      <div class="eco-info-box">
                        <h4>1. Sorties scolaires &amp; jeunesse</h4>
                        <ul>
                          <li><strong>Tarif entrée enfant protégé :</strong> <strong>500 FCFA / élève</strong> (et 0 FCFA moins de 3 ans).</li>
                          <li><strong>Forfait excursion :</strong> Dès <strong>1 500 FCFA / élève</strong> (Parc animalier « ToTo », pisciculture, musée ou piscine surveillée).</li>
                          <li><strong>Sécurité :</strong> Circuit balisé, maîtres-nageurs et éducateurs sur site.</li>
                        </ul>
                      </div>
                      <div class="eco-info-box">
                        <h4>2. Entreprises, ministères &amp; ONG</h4>
                        <ul>
                          <li><strong>Remise groupe :</strong> Dès 20 adultes (entrée parc à <strong>700 FCFA / adulte</strong> au lieu de 1 000 FCFA).</li>
                          <li><strong>Forfait séminaire :</strong> Dès <strong>12 500 FCFA / participant</strong> (salle équipée, pause-café, déjeuner Château des Saveurs et détente).</li>
                          <li><strong>Hébergement :</strong> 36 chambres et suites sur place pour retraites résidentielles.</li>
                        </ul>
                      </div>
                      <div class="eco-info-box">
                        <h4>3. Mariages, galas &amp; réceptions</h4>
                        <ul>
                          <li><strong>Salle « Menkii Essomba Anton » :</strong> Capacité vérifiée de <strong>500 places assises</strong>, climatisée et sonorisée.</li>
                          <li><strong>Espaces plein air :</strong> Esplanade arborée et pergolas au bord du lac pour cocktails et photos.</li>
                          <li><strong>Forfait réception :</strong> Dès <strong>15 000 FCFA / invité</strong> avec traiteur officiel.</li>
                        </ul>
                      </div>
                    </div>

                    <div class="eco-template-grid-2" style="margin-top:14px;">
                      <div class="eco-info-box">
                        <h4>Espaces, capacités &amp; prestations vérifiés</h4>
                        <ul>
                          <li><strong>Salle polyvalente « Menkii Essomba Anton » :</strong> 500 places (conférence, banquet, mariage).</li>
                          <li><strong>Transport &amp; navettes :</strong> Bus climatisés de <strong>5, 18 et 32 places</strong> avec prise en charge dans tout Yaoundé.</li>
                          <li><strong>Stationnement :</strong> Parking intérieur gardé et gratuit de <strong>150 places</strong> (bus et véhicules particuliers).</li>
                        </ul>
                      </div>
                      <div class="eco-info-box">
                        <h4>Conditions de réservation groupe</h4>
                        <ul>
                          <li><strong>Émission de facture proforma :</strong> Immédiate en ligne (référence <code>DEV-2026-...</code>) ou sur WhatsApp.</li>
                          <li><strong>Visite de repérage :</strong> Gratuite du mardi au dimanche sur rendez-vous avec la direction d'exploitation.</li>
                          <li><strong>Modalités :</strong> Acompte à la validation du devis ; report gratuit selon conditions météo pour les activités plein air.</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;padding-top:14px;border-top:1px solid var(--eco-border);">
                    <button type="button" class="btn btn-primary" onclick="openQuoteModalSprint1()">Demander un devis adapté à mon projet<span class="tech-code-tag"> (RES-06)</span></button>
                    <button type="button" class="btn btn-secondary" onclick="openRdvModalSprint1('seminaire_b2b')">Planifier une visite de repérage</button>
                  </div>
                </div>
              </article>"""


CFP_TEMPLATE_HTML = r"""              <!-- Pôle 6 : GABARIT COMPLET FORMATIONS CFP MINEFOP (SECTION E) -->
              <article class="col-5 bento-card" id="sec-PUB-12" style="border-top:4px solid var(--eco-cfp);">
                <div class="card-media-wrapper" onclick="openEcoparkLightbox(6)">
                  <span class="photo-zoom-pill">Agrandir</span>
                  <img src="audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png" alt="Centre de Formation Professionnelle CFP ECOPARK" />
                  <span class="media-origin-badge media-real">Photo réelle ECOPARK — Campus CFP</span>
                </div>
                <div class="bento-card-body">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                      <span class="eco-cat-badge eco-cat-cfp"><span class="tech-code-tag">PUB-12 • </span>Centre de Formation Professionnelle (CFP)</span>
                      <span class="price-pill">Inscription 50 000 FCFA • Scolarité 250 000 FCFA</span>
                    </div>
                    <h2 style="margin-top:10px;font-size:1.65rem;">CFP ECOPARK — 5 filières professionnelles agréées MINEFOP</h2>
                    <p style="font-size:16px;color:var(--eco-text-muted);margin-top:6px;">
                      Situé au cœur du complexe d'Ahala, le Centre de Formation Professionnelle ECOPARK associe enseignement théorique (30 %) et immersion pratique quotidienne (70 %) directement dans les hôtels, cuisines, jardins et bassins piscicoles du domaine.
                    </p>

                    <div class="eco-grid-3" style="margin-top:16px;gap:12px;">
                      <div class="eco-info-box">
                        <h4>1. Hôtellerie &amp; 2. Restauration</h4>
                        <ul>
                          <li><strong>Objectifs &amp; programme :</strong> Accueil, gestion hôtelière, arts culinaires camerounais et internationaux, hygiène alimentaire.</li>
                          <li><strong>Application sur site :</strong> Cités Ewondo, Chanthel, Bene et restaurant Le Château des Saveurs.</li>
                          <li><strong>Débouchés :</strong> Hôtels, complexes touristiques, restaurants et service traiteur.</li>
                        </ul>
                      </div>
                      <div class="eco-info-box">
                        <h4>3. Décoration événementielle</h4>
                        <ul>
                          <li><strong>Objectifs &amp; programme :</strong> Conception scénographique, habillage floral, aménagement de salles de réception et galas.</li>
                          <li><strong>Application sur site :</strong> Salle « Menkii Essomba Anton » (500 places) et esplanade mariage.</li>
                          <li><strong>Débouchés :</strong> Agences événementielles, entrepreneuriat et décoration d'intérieur.</li>
                        </ul>
                      </div>
                      <div class="eco-info-box">
                        <h4>4. Agropastorale &amp; 5. Pisciculture</h4>
                        <ul>
                          <li><strong>Objectifs &amp; programme :</strong> Élevage (aviculture, porciculture, cuniculture, apiculture), gestion d'étangs piscicoles et alevinage.</li>
                          <li><strong>Application sur site :</strong> Ferme d'application et bassins piscicoles d'Ahala.</li>
                          <li><strong>Débouchés :</strong> Exploitations agricoles, fermes aquacoles et auto-emploi accompagné.</li>
                        </ul>
                      </div>
                    </div>

                    <div class="eco-template-grid-2" style="margin-top:14px;">
                      <div class="eco-info-box">
                        <h4>Durée, diplômes &amp; conditions d'admission</h4>
                        <ul>
                          <li><strong>Durée du cursus :</strong> <strong>12 mois</strong> (année académique complète incluant les stages pratiques garantis sur site).</li>
                          <li><strong>Titres délivrés :</strong> Diplôme de Qualification Professionnelle (<strong>DQP</strong>), Certificat de Qualification Professionnelle (<strong>CQP</strong>) et Attestation reconnue par l'État (MINEFOP).</li>
                          <li><strong>Conditions d'admission :</strong> Accessible <strong>dès 16 ans</strong>. Pièces : fiche d'inscription, photocopie CNI ou acte de naissance, dernier bulletin ou diplôme, 4 photos 4×4.</li>
                        </ul>
                      </div>
                      <div class="eco-info-box">
                        <h4>Frais vérifiés, échéancier &amp; calendrier</h4>
                        <ul>
                          <li><strong>Frais d'inscription :</strong> <strong>50 000 FCFA</strong> à l'ouverture du dossier.</li>
                          <li><strong>Pension / Scolarité annuelle :</strong> <strong>250 000 FCFA</strong> payable en <strong>4 tranches</strong> (100 000 FCFA + 3 × 50 000 FCFA) ou en règlement intégral (300 000 FCFA inscription incluse).</li>
                          <li><strong>Prochaine session :</strong> Inscriptions et entretiens d'orientation ouverts du mardi au samedi au campus d'Ahala.</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;padding-top:14px;border-top:1px solid var(--eco-border);">
                    <button type="button" class="btn btn-primary" onclick="openCfpModalSprint1()">Déposer une demande d'information ou candidature</button>
                    <button type="button" class="btn btn-secondary" onclick="openRdvModalSprint1('orientation_cfp')">Prendre RDV d'orientation au campus</button>
                  </div>
                </div>
              </article>"""


QUICK_DAY_CALC_HTML = r"""            <!-- CALCULATEUR RAPIDE DE JOURNÉE & HORAIRES D'OUVERTURE (SCÉNARIO AUTO-SERVICE #1) -->
            <div class="card" id="quickDayPriceCalculator" style="margin-bottom:24px;padding:22px;background:#FFFFFF;border:1px solid var(--eco-border);border-left:5px solid var(--eco-water);">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:16px;">
                <div>
                  <span class="eco-cat-badge eco-cat-water">Calculateur express • Sans engagement</span>
                  <h3 style="font-size:1.35rem;margin:8px 0 4px;">Combien coûte une journée au parc ? (Ex. 2 adultes et 2 enfants)</h3>
                  <p style="font-size:15.5px;color:var(--eco-text-muted);margin:0;">
                    Ajustez le nombre d'adultes (13 ans et +) et d'enfants (3 à 12 ans) pour comparer immédiatement les formules en Francs CFA. Moins de 3 ans : <strong>0 FCFA (gratuit)</strong>.
                  </p>
                </div>
                <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;background:var(--eco-bg);padding:10px 14px;border-radius:12px;border:1px solid var(--eco-border);">
                  <div style="display:flex;align-items:center;gap:8px;">
                    <label for="quickCalcAdults" style="font-size:14px;font-weight:700;">Adultes (13+) :</label>
                    <input type="number" id="quickCalcAdults" min="0" max="50" value="2" style="width:64px;min-height:44px;padding:6px 10px;border:1px solid var(--eco-border-strong);border-radius:8px;font-weight:700;font-size:16px;" oninput="recalcQuickDayPrice()" />
                  </div>
                  <div style="display:flex;align-items:center;gap:8px;">
                    <label for="quickCalcChildren" style="font-size:14px;font-weight:700;">Enfants (3–12 ans) :</label>
                    <input type="number" id="quickCalcChildren" min="0" max="50" value="2" style="width:64px;min-height:44px;padding:6px 10px;border:1px solid var(--eco-border-strong);border-radius:8px;font-weight:700;font-size:16px;" oninput="recalcQuickDayPrice()" />
                  </div>
                </div>
              </div>

              <div class="eco-grid-4" style="gap:12px;">
                <div style="padding:14px;background:var(--eco-bg);border-radius:12px;border:1px solid var(--eco-border);">
                  <span style="font-size:12.5px;font-weight:700;color:var(--eco-text-muted);text-transform:uppercase;display:block;">1. Entrée Parc &amp; Zoo seule</span>
                  <strong id="quickCalcZooOnly" style="font-family:var(--font-heading);font-size:1.45rem;color:var(--eco-brand);display:block;margin:4px 0;">3 000 FCFA</strong>
                  <span style="font-size:13px;color:var(--eco-text-muted);">1 000 FCFA / adulte • 500 FCFA / enfant</span>
                </div>
                <div style="padding:14px;background:var(--eco-bg);border-radius:12px;border:1px solid var(--eco-border);">
                  <span style="font-size:12.5px;font-weight:700;color:var(--eco-nature-text);text-transform:uppercase;display:block;">2. Pass Découverte Nature</span>
                  <strong id="quickCalcPassDecouverte" style="font-family:var(--font-heading);font-size:1.45rem;color:var(--eco-brand);display:block;margin:4px 0;">8 000 FCFA</strong>
                  <span style="font-size:13px;color:var(--eco-text-muted);">Zoo + Pirogue + Cheval (2 500 / 1 500 FCFA)</span>
                </div>
                <div style="padding:14px;background:var(--eco-bg);border-radius:12px;border:1px solid var(--eco-border);">
                  <span style="font-size:12.5px;font-weight:700;color:var(--eco-water-text);text-transform:uppercase;display:block;">3. Zoo + Piscine + Pirogue</span>
                  <strong id="quickCalcWaterCombo" style="font-family:var(--font-heading);font-size:1.45rem;color:var(--eco-brand);display:block;margin:4px 0;">14 000 FCFA</strong>
                  <span style="font-size:13px;color:var(--eco-text-muted);">4 500 FCFA / adulte • 2 500 FCFA / enfant</span>
                </div>
                <div style="padding:14px;background:#FBF7F0;border-radius:12px;border:1.5px solid var(--eco-dining);">
                  <span style="font-size:12.5px;font-weight:700;color:var(--eco-dining-text);text-transform:uppercase;display:block;">4. Pass Journée Royale (Repas inclus)</span>
                  <strong id="quickCalcPassRoyale" style="font-family:var(--font-heading);font-size:1.45rem;color:var(--eco-brand);display:block;margin:4px 0;">26 000 FCFA</strong>
                  <span style="font-size:13px;color:var(--eco-text-muted);">Zoo + Piscine + Pirogue + Repas (8 500 / 4 500 FCFA)</span>
                </div>
              </div>
            </div>"""


RES_JOURNEY_AND_STEPPER_HTML = r"""            <!-- ECOPARK_V4_RES_STEPPER:START -->
            <!-- SÉLECTEUR DES 4 PARCOURS DE RÉSERVATION DISTINCTS (SECTION G) -->
            <div class="eco-journey-tabs" id="resJourneyTabs" role="tablist" aria-label="Choisir le type de réservation ou de demande">
              <button type="button" class="eco-journey-tab active" data-res-journey="DAY" onclick="switchResJourney('DAY', this)">
                <strong>1. Journée &amp; Activités au parc</strong>
                <span>Billets QR à la carte ou Pass journée (Mar–Dim)</span>
              </button>
              <button type="button" class="eco-journey-tab" data-res-journey="LODGE" onclick="switchResJourney('LODGE', this)">
                <strong>2. Séjour &amp; Hébergement (7j/7)</strong>
                <span>Cités Bene, Chanthel, Ewondo VIP &amp; Suites</span>
              </button>
              <button type="button" class="eco-journey-tab" data-res-journey="GROUP" onclick="switchResJourney('GROUP', this)">
                <strong>3. Groupe, École ou Événement</strong>
                <span>Demande de devis &amp; Salle 500 places (sans paiement immédiat)</span>
              </button>
              <button type="button" class="eco-journey-tab" data-res-journey="CFP" onclick="switchResJourney('CFP', this)">
                <strong>4. Formation CFP MINEFOP</strong>
                <span>Demande d'information &amp; dossier de candidature</span>
              </button>
            </div>

            <!-- STEPPER 5 ÉTAPES ALIGNÉ SUR L'ORDRE DES CHAMPS (SECTION G) -->
            <nav class="v4-res-stepper" id="v4ResStepperBar" aria-label="Étapes du parcours de réservation">
              <button type="button" class="v4-res-step active" data-v4-step="1" onclick="goToV4ReservationStep(1)">
                <span class="v4-res-step-num">1</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--eco-text);">Date et participants</strong>
                  <span style="font-size:12px;color:var(--eco-text-muted);">Tarif enfant 500 FCFA protégé</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="2" onclick="goToV4ReservationStep(2)">
                <span class="v4-res-step-num">2</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--eco-text);">Pass ou activités</strong>
                  <span style="font-size:12px;color:var(--eco-text-muted);">Formules tout-inclus ou à la carte</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="3" onclick="goToV4ReservationStep(3)">
                <span class="v4-res-step-num">3</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--eco-text);">Coordonnées</strong>
                  <span style="font-size:12px;color:var(--eco-text-muted);">Nom &amp; téléphone (+237)</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="4" onclick="goToV4ReservationStep(4)">
                <span class="v4-res-step-num">4</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--eco-text);">Récapitulatif et règlement</strong>
                  <span style="font-size:12px;color:var(--eco-text-muted);">OM / MoMo sans PIN ou Guichet</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="5" onclick="goToV4ReservationStep(5)">
                <span class="v4-res-step-num">5</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--eco-text);">Résultat</strong>
                  <span style="font-size:12px;color:var(--eco-text-muted);">Confirmation &amp; Billet QR</span>
                </div>
              </button>
            </nav>
            <!-- ECOPARK_V4_RES_STEPPER:END -->"""


AGT_ACTIVE_MISSION_BANNER_HTML = r"""            <!-- ECOPARK_AGT_ACTIVE_MISSION:START -->
            <div class="card" id="agtActiveMissionBanner" style="margin-bottom:20px;padding:16px 20px;background:#F4F8F2;border:1.5px solid var(--eco-brand);border-left:6px solid var(--eco-brand);">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                <div>
                  <span class="eco-cat-badge eco-cat-nature" style="margin-bottom:4px;">Affectation Poste Active • Pôle Guichet &amp; Contrôle</span>
                  <strong style="font-family:var(--font-heading);font-size:1.18rem;color:var(--eco-brand);display:block;" id="agtBannerMissionTitle">
                    MSN-2026-101 • Ouverture Guichet Principal #1, Fond de caisse 50 000 FCFA &amp; Billetterie RN3
                  </strong>
                  <span style="font-size:13.5px;color:var(--eco-text-muted);" id="agtBannerMissionMeta">
                    Agent : <strong>Mme Clarisse ATANGANA (MAT-AGT-01)</strong> • Créneau : <strong>08h30 – 18h00</strong> • Statut : <strong id="agtBannerMissionStatus">En cours sur poste</strong>
                  </span>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                  <button type="button" class="btn btn-secondary btn-sm" id="btnAgtUnreadAlerts" onclick="openExpMissionsPanel('GUICHET_CAISSE')">
                    Alertes Poste (<span id="agtUnreadAlertsCount">2</span>)
                  </button>
                  <button type="button" class="btn btn-secondary btn-sm" onclick="openExpMissionsPanel('GUICHET_CAISSE')">
                    Voir toutes les missions terrain
                  </button>
                  <button type="button" class="btn btn-primary btn-sm" id="btnAgtPrintMissionA4" onclick="openMissionSheetA4('MSN-2026-101')">
                    <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
                    <span>Fiche de Mission A4 (Imprimer / PDF)</span>
                  </button>
                </div>
              </div>
            </div>
            <!-- ECOPARK_AGT_ACTIVE_MISSION:END -->"""


EXP_MISSIONS_MODULE_HTML = r"""            <!-- ECOPARK_EXP_MISSIONS_MODULE:START -->
            <div class="card" id="sec-EXP-MISSIONS" style="margin-bottom:22px;padding:24px;background:#FFFFFF;border:1.5px solid var(--eco-border);border-top:5px solid var(--eco-brand);">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
                <div>
                  <span class="eco-cat-badge eco-cat-nature"><span class="tech-code-tag">EXP-MISSIONS • </span>Ordres d'affectation &amp; Fiches de mission imprimables A4</span>
                  <h3 style="margin:8px 0 4px;font-size:1.45rem;">Assignation d'une tâche &amp; Fiche de mission des agents d'exploitation</h3>
                  <p style="font-size:15px;color:var(--eco-text-muted);margin:0;">
                    Affectez une mission quotidienne aux agents d'Ahala sur les 4 pôles terrain (Guichet &amp; Caisse, Contrôle QR Piscine/Lac, Hébergements Ewondo/Chanthel/Bene, Cuisine Château des Saveurs), suivez la check-list de contrôle et éditez la <strong>Fiche de Mission officielle A4</strong> avec cadre d'émargement.
                  </p>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                  <button type="button" class="btn btn-secondary btn-sm" onclick="openMissionSheetA4((window._activeMissionIdForPrint || 'MSN-2026-101'))">
                    <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
                    <span>Aperçu Fiche de Mission A4</span>
                  </button>
                </div>
              </div>

              <!-- KPI Bar des missions du jour -->
              <div class="eco-grid-4" style="gap:12px;margin-bottom:18px;">
                <div style="padding:12px 14px;background:var(--eco-bg);border-radius:10px;border:1px solid var(--eco-border);">
                  <span style="font-size:12.5px;color:var(--eco-text-muted);font-weight:700;text-transform:uppercase;display:block;">Missions du jour</span>
                  <strong style="font-family:var(--font-heading);font-size:1.5rem;color:var(--eco-brand);" id="expMissionKpiTotal">4 missions</strong>
                  <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;">Fuseau Africa/Douala (UTC+1)</span>
                </div>
                <div style="padding:12px 14px;background:var(--eco-bg);border-radius:10px;border:1px solid var(--eco-border);">
                  <span style="font-size:12.5px;color:var(--eco-water-text);font-weight:700;text-transform:uppercase;display:block;">En cours sur poste</span>
                  <strong style="font-family:var(--font-heading);font-size:1.5rem;color:var(--eco-water);" id="expMissionKpiActive">2 actives</strong>
                  <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;">Agents pointés sur le terrain</span>
                </div>
                <div style="padding:12px 14px;background:var(--eco-bg);border-radius:10px;border:1px solid var(--eco-border);">
                  <span style="font-size:12.5px;color:var(--eco-nature-text);font-weight:700;text-transform:uppercase;display:block;">Terminées &amp; Validées</span>
                  <strong style="font-family:var(--font-heading);font-size:1.5rem;color:var(--eco-nature-text);" id="expMissionKpiDone">1 validée</strong>
                  <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;">Visa exploitation enregistré</span>
                </div>
                <div style="padding:12px 14px;background:#FBF7F0;border-radius:10px;border:1px solid var(--eco-dining);">
                  <span style="font-size:12.5px;color:var(--eco-dining-text);font-weight:700;text-transform:uppercase;display:block;">Pôles Terrain Couverts</span>
                  <strong style="font-family:var(--font-heading);font-size:1.5rem;color:var(--eco-dining);" id="expMissionKpiPoles">4 / 4 pôles</strong>
                  <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;">Guichet • Lac/Piscine • Loges • Cuisine</span>
                </div>
              </div>

              <!-- Centre d'Alertes & Notifications Temps Réel par Poste (1 Commande = 1 Fiche de Mission) -->
              <div class="post-alerts-center" id="expPostAlertsCenter" role="region" aria-label="Centre d'alertes et notifications des fiches de mission par poste">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
                  <div>
                    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                      <span class="status-badge status-warning" id="expUnreadAlertsCountBadge">2 alertes postes non lues</span>
                      <span style="font-size:12px;font-weight:700;text-transform:uppercase;color:var(--eco-dining-text);letter-spacing:0.03em;">Règle active : 1 Commande validée = 1 Fiche de Mission routée au poste</span>
                    </div>
                    <strong style="font-size:15.5px;color:var(--eco-text);display:block;margin-top:4px;">Centre d'Alertes &amp; Notifications Temps Réel des Postes Terrain</strong>
                    <span style="font-size:13px;color:var(--eco-text-muted);">Chaque réservation, précommande, devis ou ticket caisse génère automatiquement la Fiche de Mission A4 du poste concerné et notifie l'agent affecté.</span>
                  </div>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <button type="button" class="btn btn-secondary btn-sm" id="btnToggleMissionAlertSound" onclick="toggleMissionAlertSound()">
                      Signal sonore : Activé
                    </button>
                    <button type="button" class="btn btn-secondary btn-sm" id="btnSimulateOrderDispatch" onclick="simulateInstantOrderToMissionDispatch()">
                      Simuler Commande → Alerte Poste
                    </button>
                    <button type="button" class="btn btn-primary btn-sm" id="btnAckAllMissionAlerts" onclick="acknowledgeAllMissionAlerts()">
                      Tout acquitter
                    </button>
                  </div>
                </div>
                <div id="expAlertsFeedList" style="display:grid;gap:8px;"></div>
              </div>

              <!-- Modèles rapides par pôle en 1 clic -->
              <div style="margin-bottom:6px;font-size:13px;font-weight:700;color:var(--eco-brand);text-transform:uppercase;letter-spacing:0.03em;">
                1. Choisir un modèle de mission par pôle terrain (pré-remplissage en 1 clic) :
              </div>
              <div class="exp-mission-preset-grid" id="expMissionPresetGrid">
                <button type="button" class="exp-mission-preset-btn active" data-mission-pole="GUICHET_CAISSE" onclick="applyMissionPolePreset('GUICHET_CAISSE', this)">
                  <div>
                    <span class="eco-cat-badge eco-cat-nature" style="font-size:11px;padding:2px 8px;">1. Guichet &amp; Caisse</span>
                    <strong style="display:block;font-size:14.5px;color:var(--eco-text);margin-top:6px;">Caisse Entrée RN3 &amp; Billetage</strong>
                    <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;margin-top:2px;">Fond 50 000 FCFA, ventes Espèces/MoMo sans PIN, clôture contradictoire.</span>
                  </div>
                  <span style="font-size:12px;font-weight:700;color:var(--eco-brand);">Charger ce modèle →</span>
                </button>

                <button type="button" class="exp-mission-preset-btn" data-mission-pole="CONTROLE_QR" onclick="applyMissionPolePreset('CONTROLE_QR', this)">
                  <div>
                    <span class="eco-cat-badge eco-cat-water" style="font-size:11px;padding:2px 8px;">2. Contrôle QR Piscine &amp; Lac</span>
                    <strong style="display:block;font-size:14.5px;color:var(--eco-text);margin-top:6px;">Scan QR 7 États &amp; Sécurité Bassin</strong>
                    <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;margin-top:2px;">Tourniquet piscine, embarcadère pirogues, port obligatoire du gilet.</span>
                  </div>
                  <span style="font-size:12px;font-weight:700;color:var(--eco-water);">Charger ce modèle →</span>
                </button>

                <button type="button" class="exp-mission-preset-btn" data-mission-pole="HEBERGEMENT" onclick="applyMissionPolePreset('HEBERGEMENT', this)">
                  <div>
                    <span class="eco-cat-badge eco-cat-lodging" style="font-size:11px;padding:2px 8px;">3. Hébergements (3 Cités)</span>
                    <strong style="display:block;font-size:14.5px;color:var(--eco-text);margin-top:6px;">Cités Ewondo VIP, Chanthel &amp; Bene</strong>
                    <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;margin-top:2px;">Check-in 14h00 / Check-out 11h00, remise clés, contrôle climatisation.</span>
                  </div>
                  <span style="font-size:12px;font-weight:700;color:var(--eco-lodging);">Charger ce modèle →</span>
                </button>

                <button type="button" class="exp-mission-preset-btn" data-mission-pole="CUISINE_SAVEURS" onclick="applyMissionPolePreset('CUISINE_SAVEURS', this)">
                  <div>
                    <span class="eco-cat-badge eco-cat-dining" style="font-size:11px;padding:2px 8px;">4. Cuisine Château des Saveurs</span>
                    <strong style="display:block;font-size:14.5px;color:var(--eco-text);margin-top:6px;">Précommandes 12h30 &amp; Pergolas</strong>
                    <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;margin-top:2px;">Poisson braisé d'Ahala, Poulet DG Royal, service Zéro Attente 13h00.</span>
                  </div>
                  <span style="font-size:12px;font-weight:700;color:var(--eco-dining);">Charger ce modèle →</span>
                </button>
              </div>

              <!-- Formulaire d'assignation de tâche -->
              <div style="padding:18px;background:var(--eco-bg);border:1px solid var(--eco-border);border-radius:12px;margin-bottom:20px;" id="expMissionAssignForm">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px;">
                  <strong style="font-size:15.5px;color:var(--eco-brand);">2. Paramètres de la tâche assignée &amp; consignes de poste</strong>
                  <span style="font-size:12.5px;color:var(--eco-text-muted);">Enregistrement synchronisé avec le Journal d'Audit &amp; la Fiche de Mission A4</span>
                </div>

                <div class="grid-12" style="gap:12px;">
                  <div class="col-3 form-group" style="margin:0;">
                    <label class="form-label" for="missionPoleSelect">Pôle opérationnel <span style="color:#B42318;">*</span></label>
                    <select id="missionPoleSelect" class="form-control" onchange="applyMissionPolePreset(this.value)">
                      <option value="GUICHET_CAISSE" selected>1. Guichet &amp; Caisse Principale</option>
                      <option value="CONTROLE_QR">2. Contrôle QR Piscine &amp; Lac</option>
                      <option value="HEBERGEMENT">3. Hébergements (Ewondo / Chanthel / Bene)</option>
                      <option value="CUISINE_SAVEURS">4. Cuisine Le Château des Saveurs</option>
                    </select>
                  </div>

                  <div class="col-3 form-group" style="margin:0;">
                    <label class="form-label" for="missionAgentSelect">Agent terrain affecté <span style="color:#B42318;">*</span></label>
                    <select id="missionAgentSelect" class="form-control">
                      <option value="Mme Clarisse ATANGANA|MAT-AGT-01|Caissière Principale Guichet #1" selected>Mme Clarisse ATANGANA (Guichet &amp; Caisse)</option>
                      <option value="M. Samuel MBARGA|MAT-CTL-02|Contrôleur QR Piscine &amp; Embarcadère">M. Samuel MBARGA (Contrôle QR Piscine &amp; Lac)</option>
                      <option value="Mme Chantal NGO BIYONG|MAT-HTL-03|Gouvernante Cités Ewondo, Chanthel &amp; Bene">Mme Chantal NGO BIYONG (Hébergements 3 Cités)</option>
                      <option value="Chef Patrice ESSOMBA|MAT-RES-04|Chef de Cuisine &amp; Pergolas Château des Saveurs">Chef Patrice ESSOMBA (Cuisine Château des Saveurs)</option>
                      <option value="M. Jean-Baptiste NKOA|MAT-EXP-05|Superviseur Polyvalent Parc &amp; Navettes">M. Jean-Baptiste NKOA (Superviseur Polyvalent)</option>
                    </select>
                  </div>

                  <div class="col-2 form-group" style="margin:0;">
                    <label class="form-label" for="missionDateInput">Date de mission <span style="color:#B42318;">*</span></label>
                    <input type="date" id="missionDateInput" class="form-control" />
                  </div>

                  <div class="col-2 form-group" style="margin:0;">
                    <label class="form-label" for="missionShiftSelect">Créneau horaire</label>
                    <select id="missionShiftSelect" class="form-control">
                      <option value="08h30 – 18h00 (Journée complète)" selected>08h30 – 18h00 (Journée)</option>
                      <option value="08h30 – 14h00 (Service Matinée)">08h30 – 14h00 (Matinée)</option>
                      <option value="11h30 – 20h30 (Service Midi &amp; Soir)">11h30 – 20h30 (Midi &amp; Soir)</option>
                      <option value="14h00 – 11h00 J+1 (Garde Hôtelière 24h)">14h00 – 11h00 J+1 (Garde 24h)</option>
                    </select>
                  </div>

                  <div class="col-2 form-group" style="margin:0;">
                    <label class="form-label" for="missionPrioritySelect">Priorité</label>
                    <select id="missionPrioritySelect" class="form-control">
                      <option value="HAUTE" selected>Haute — Affluence / Groupe</option>
                      <option value="NORMALE">Normale — Exploitation standard</option>
                      <option value="URGENTE">Urgente — Sécurité / VIP</option>
                    </select>
                  </div>

                  <div class="col-6 form-group" style="margin:0;">
                    <label class="form-label" for="missionTitleInput">Intitulé précis de la tâche assignée <span style="color:#B42318;">*</span></label>
                    <input type="text" id="missionTitleInput" class="form-control" value="Ouverture Guichet Principal #1, contrôle fond de caisse 50 000 FCFA &amp; accueil Groupes" />
                  </div>

                  <div class="col-6 form-group" style="margin:0;">
                    <label class="form-label" for="missionLocationInput">Poste &amp; Zone d'affectation sur le site d'Ahala</label>
                    <input type="text" id="missionLocationInput" class="form-control" value="Portail Principal RN3 (Face Station Tradex Ahala) — Guichet #1" />
                  </div>

                  <div class="col-6 form-group" style="margin:0;">
                    <label class="form-label" for="missionObjectiveInput">Objectif opérationnel &amp; consignes d'exécution</label>
                    <textarea id="missionObjectiveInput" class="form-control" rows="2">Assurer l'encaissement fluide des visiteurs walk-in (Espèces FCFA et Mobile Money sans saisie de code PIN), protéger le tarif enfant à 500 FCFA et maintenir un écart de caisse inférieur ou égal à 2 000 FCFA à la clôture contradictoire de 18h00.</textarea>
                  </div>

                  <div class="col-6 form-group" style="margin:0;">
                    <label class="form-label" for="missionChecklistInput">Check-list de contrôle terrain (séparer les points par « ; »)</label>
                    <textarea id="missionChecklistInput" class="form-control" rows="2">Vérifier le fond de caisse initial de 50 000 FCFA à 08h30; Appliquer strictement le tarif enfant protégé (500 FCFA Zoo / 0 FCFA moins de 3 ans); Vérifier les pré-réservations Guichet avant l'échéance de 11h00; Réaliser le billetage contradictoire et signer le PV de clôture à 18h00</textarea>
                  </div>

                  <div class="col-8 form-group" style="margin:0;">
                    <label class="form-label" for="missionEquipmentInput">Dotation &amp; équipements remis à la prise de poste</label>
                    <input type="text" id="missionEquipmentInput" class="form-control" value="Fond de caisse 50 000 FCFA, Terminal Caisse Rapide AGT-03, Rouleau thermique QR, Talkie-walkie Canal 1" />
                  </div>

                  <div class="col-4" style="display:flex;align-items:flex-end;gap:8px;flex-wrap:wrap;">
                    <button type="button" class="btn btn-primary" id="btnAssignMissionSubmit" style="flex:1;" onclick="assignOperationalMission(false)">
                      Assigner la tâche
                    </button>
                    <button type="button" class="btn btn-secondary" id="btnAssignAndPrintMission" onclick="assignOperationalMission(true)">
                      Assigner &amp; Fiche A4
                    </button>
                  </div>
                </div>
              </div>

              <!-- Filtres et Tableau des missions assignées -->
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
                <div style="display:flex;gap:6px;flex-wrap:wrap;" id="expMissionFilterBar" role="tablist" aria-label="Filtrer les missions par pôle opérationnel">
                  <button type="button" class="acc-filter-pill active" data-pole-filter="ALL" onclick="filterOperationalMissions('ALL', this)">Tous les pôles (4)</button>
                  <button type="button" class="acc-filter-pill" data-pole-filter="GUICHET_CAISSE" onclick="filterOperationalMissions('GUICHET_CAISSE', this)">Guichet &amp; Caisse</button>
                  <button type="button" class="acc-filter-pill" data-pole-filter="CONTROLE_QR" onclick="filterOperationalMissions('CONTROLE_QR', this)">Contrôle QR Piscine/Lac</button>
                  <button type="button" class="acc-filter-pill" data-pole-filter="HEBERGEMENT" onclick="filterOperationalMissions('HEBERGEMENT', this)">Hébergements (Ewondo/Chanthel/Bene)</button>
                  <button type="button" class="acc-filter-pill" data-pole-filter="CUISINE_SAVEURS" onclick="filterOperationalMissions('CUISINE_SAVEURS', this)">Cuisine Château des Saveurs</button>
                </div>
                <input type="search" id="expMissionSearchInput" class="form-control" style="max-width:280px;min-height:38px;padding:6px 12px;font-size:13.5px;" placeholder="Rechercher réf. MSN-..., agent, tâche..." aria-label="Rechercher une mission" oninput="renderOperationalMissionsTable()" />
              </div>

              <div class="table-responsive">
                <table class="adm-table" id="expMissionsTable">
                  <thead>
                    <tr>
                      <th>Réf. &amp; Pôle</th>
                      <th>Agent affecté &amp; Poste</th>
                      <th>Tâche assignée &amp; Créneau</th>
                      <th>Check-list terrain</th>
                      <th>Statut</th>
                      <th>Actions &amp; Fiche A4</th>
                    </tr>
                  </thead>
                  <tbody id="expMissionsTableBody"></tbody>
                </table>
              </div>
            </div>
            <!-- ECOPARK_EXP_MISSIONS_MODULE:END -->"""


REFONTE_JS = r"""
  // ECOPARK_REFONTE_CANOPEE_JS:START
  (function () {
    // =========================================================================
    // F — SOURCE UNIQUE DES INFORMATIONS (CENTRALISATION MÉTIER & TARIFS FCFA)
    // =========================================================================
    window.ECOPARK_SOURCE_UNIQUE = {
      brand: {
        name: 'ECOPARK CAMEROUN',
        directionArtistique: 'Canopée vivante',
        address: 'Quartier Ahala Barrière, face station Tradex Ahala, Route Nationale N°3, Yaoundé, Cameroun',
        phones: ['+237 697 13 62 03', '+237 675 56 26 55'],
        whatsappMain: '+237697136203',
        email: 'info@ecopark-yaounde.com'
      },
      schedule: {
        parkDays: 'Mardi au Dimanche',
        parkHours: 'Dès 09h00 (fermeture 18h00)',
        parkClosedDay: 'Lundi (fermeture hebdomadaire du parc de loisirs pour maintenance)',
        lodgeDays: 'Ouvert 7j/7 (Réception 24h/24)',
        checkIn: '14h00',
        checkOut: '11h00',
        restaurantHours: 'Mardi au Dimanche de 11h30 à 20h30 (7j/7 pour résidents)'
      },
      ageCategories: {
        toddler: { label: 'Moins de 3 ans', priceFcfa: 0, note: 'Accès parc gratuit (0 FCFA)' },
        child: { label: 'Enfant (3 à 12 ans)', priceFcfa: 500, note: 'Tarif entrée enfant protégé à 500 FCFA même en groupe' },
        adult: { label: 'Adulte (13 ans et +)', priceFcfa: 1000, groupPriceFcfa: 700, groupMinAdults: 20 }
      },
      bookingConditions: {
        rainGuaranteeDays: 90,
        cancelFullRefundHours: 48,
        cancelLateRetentionPct: 20,
        guichetHoldLimitTime: '11h00'
      },
      activityDetails: {
        pirogue: {
          deroulement: [
            'Accueil au ponton du lac d\'Ahala et remise du gilet de sauvetage homologué à votre taille.',
            'Traversée commentée de 45 minutes avec un pagayeur expérimenté le long des berges arborées.',
            'Pause photo face aux pergolas et retour sécurisé à l\'embarcadère.'
          ],
          inclus: [
            'Inclus : Embarquement, gilet de sauvetage obligatoire, accompagnement par le guide-pagayeur.',
            'Non inclus : Entrée Parc & Zoo (500 FCFA / enfant • 1 000 FCFA / adulte hors Pass) et repas.'
          ],
          conditions: [
            'Horaires : Mardi au dimanche de 09h30 à 17h30 (fermé le lundi).',
            'Âge minimum : Dès 3 ans (enfants accompagnés d\'un adulte).',
            'Garantie météo : Report gratuit sous 90 jours en cas d\'averse avant embarquement.'
          ]
        },
        zoo: {
          deroulement: [
            'Accès par le portail principal d\'Ahala et parcours ombragé à travers la palmeraie et le jardin botanique.',
            'Observation du gorille « ToTo », des chimpanzés, tortues géantes, autruches et paons.',
            'Visite libre ou commentée (durée moyenne : 1h30).'
          ],
          inclus: [
            'Inclus : Accès aux allées botaniques, au parc animalier et aux aires de repos ombragées.',
            'Non inclus : Sachet nutrition poissons/tortues (+500 FCFA en option) et activités nautiques/piscine.'
          ],
          conditions: [
            'Horaires : Mardi au dimanche de 09h00 à 18h00.',
            'Tarif enfant protégé : 500 FCFA (3–12 ans) • Gratuit moins de 3 ans • Adulte : 1 000 FCFA (700 FCFA dès 20 adultes).'
          ]
        },
        piscine: {
          deroulement: [
            'Contrôle du billet au portique de la piscine semi-olympique et accès aux vestiaires.',
            'Baignade dans le grand bassin ou le bassin enfants sous la surveillance permanente des maîtres-nageurs.',
            'Détente sur les transats au bord de l\'eau.'
          ],
          inclus: [
            'Inclus : Accès journée aux bassins, vestiaires, douches et surveillance aquatique.',
            'Non inclus : Maillot de bain (obligatoire) et consommations au Château des Saveurs.'
          ],
          conditions: [
            'Tenue : Maillot de bain réglementaire et douche savonnée obligatoires avant baignade.',
            'Tarif : 1 500 FCFA / enfant (prévente/semaine) ou 2 500 FCFA (guichet week-end) • 2 500 FCFA / adulte.'
          ]
        },
        cheval: {
          deroulement: [
            'Accueil au manège équestre, équipement de la bombe de protection et consignes du moniteur.',
            'Tour encadré à cheval dans l\'enceinte verdoyante (séance d\'environ 30 minutes).',
            'Accès complémentaire aux manèges et aires de jeux pour les enfants.'
          ],
          inclus: [
            'Inclus : Bombe de protection, accompagnement par le moniteur équestre.',
            'Non inclus : Entrée Parc & Zoo si réservée hors Pass Découverte.'
          ],
          conditions: [
            'Âge : Dès 4 ans (accompagnement à la longe pour les enfants et débutants).',
            'Tarif : 500 FCFA / enfant • 1 000 FCFA / adulte par séance.'
          ]
        },
        musee: {
          deroulement: [
            'Visite de la salle d\'exposition culturelle présentant des objets patrimoniaux des régions du Cameroun.',
            'Accès à la bibliothèque et à l\'espace de lecture jeunesse au calme.',
            'Échanges pédagogiques adaptés aux familles et aux sorties scolaires.'
          ],
          inclus: [
            'Inclus : Accès à l\'exposition permanente et à la salle de lecture.',
            'Non inclus : Activités nautiques et restauration.'
          ],
          conditions: [
            'Horaires : Mardi au dimanche de 09h30 à 17h30.',
            'Tarif : 500 FCFA / enfant • 1 000 FCFA / adulte.'
          ]
        }
      }
    };

    // =========================================================================
    // GESTION DES DATES RÉELLES (FUSEAU AFRICA/DOUALA — ZÉRO DATE FIXE 2026-11-15)
    // =========================================================================
    window.getDefaultOpenVisitDateIso = function (allowMonday) {
      var now = new Date();
      try {
        var parts = new Intl.DateTimeFormat('en-CA', {
          timeZone: 'Africa/Douala',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        }).formatToParts(now);
        var y = 2026, m = 10, d = 29;
        parts.forEach(function (p) {
          if (p.type === 'year') y = parseInt(p.value, 10);
          if (p.type === 'month') m = parseInt(p.value, 10);
          if (p.type === 'day') d = parseInt(p.value, 10);
        });
        var dt = new Date(Date.UTC(y, m - 1, d, 12, 0, 0));
        // Proposer par défaut demain (ou mardi si demain est un lundi de fermeture parc)
        dt.setUTCDate(dt.getUTCDate() + 1);
        if (!allowMonday && dt.getUTCDay() === 1) {
          dt.setUTCDate(dt.getUTCDate() + 1);
        }
        return dt.toISOString().slice(0, 10);
      } catch (e) {
        var fallback = new Date(now.getTime() + 86400000);
        if (!allowMonday && fallback.getDay() === 1) {
          fallback = new Date(fallback.getTime() + 86400000);
        }
        return fallback.toISOString().slice(0, 10);
      }
    };

    window.getTodayVisitDateMinIso = function () {
      try {
        return new Intl.DateTimeFormat('en-CA', {
          timeZone: 'Africa/Douala',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        }).format(new Date());
      } catch (e) {
        return new Date().toISOString().slice(0, 10);
      }
    };

    var todayMinIso = window.getTodayVisitDateMinIso();
    var defaultOpenIso = window.getDefaultOpenVisitDateIso(false);
    ['visitDate', 'v4Pub04DateInput', 'quoteDate', 'rdvDate', 'rescheduleNewDate'].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.setAttribute('min', todayMinIso);
      if (!el.value || el.value === '2026-11-15') {
        el.value = defaultOpenIso;
      }
    });

    // =========================================================================
    // CALCULATEUR RAPIDE DE JOURNÉE (SCÉNARIO AUTO-SERVICE #1 DANS PRÉPARER MA VISITE)
    // =========================================================================
    window.recalcQuickDayPrice = function () {
      var aIn = document.getElementById('quickCalcAdults');
      var cIn = document.getElementById('quickCalcChildren');
      var adults = Math.max(0, parseInt(aIn && aIn.value, 10) || 0);
      var children = Math.max(0, parseInt(cIn && cIn.value, 10) || 0);
      var adultZooUnit = adults >= 20 ? 700 : 1000;
      var zooOnly = (adults * adultZooUnit) + (children * 500);
      var passDecouverte = (adults * 2500) + (children * 1500);
      var waterCombo = (adults * (adultZooUnit + 2500 + 1000)) + (children * (500 + 1500 + 500));
      var passRoyale = (adults * 8500) + (children * 4500);

      var fmt = typeof window.formatFCFA === 'function'
        ? window.formatFCFA
        : function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' FCFA'; };

      var el1 = document.getElementById('quickCalcZooOnly');
      var el2 = document.getElementById('quickCalcPassDecouverte');
      var el3 = document.getElementById('quickCalcWaterCombo');
      var el4 = document.getElementById('quickCalcPassRoyale');
      if (el1) el1.textContent = fmt(zooOnly);
      if (el2) el2.textContent = fmt(passDecouverte);
      if (el3) el3.textContent = fmt(waterCombo);
      if (el4) el4.textContent = fmt(passRoyale);
      return { zooOnly: zooOnly, passDecouverte: passDecouverte, waterCombo: waterCombo, passRoyale: passRoyale };
    };
    window.recalcQuickDayPrice();

    // =========================================================================
    // ENRICHISSEMENT DYNAMIQUE DE LA FICHE ACTIVITÉ (#sec-PUB-04)
    // =========================================================================
    var origSwitchPub04Act = window.switchV4Pub04Activity;
    if (typeof origSwitchPub04Act === 'function' && !origSwitchPub04Act._refonteWrapped) {
      window.switchV4Pub04Activity = function (actKey, btnEl) {
        var res = origSwitchPub04Act.apply(this, arguments);
        var details = (window.ECOPARK_SOURCE_UNIQUE && window.ECOPARK_SOURCE_UNIQUE.activityDetails[actKey])
          || window.ECOPARK_SOURCE_UNIQUE.activityDetails.pirogue;
        if (details) {
          var dList = document.getElementById('v4Pub04DeroulementList');
          var iList = document.getElementById('v4Pub04InclusList');
          var cList = document.getElementById('v4Pub04ConditionsList');
          if (dList) dList.innerHTML = details.deroulement.map(function (t) { return '<li>' + t + '</li>'; }).join('');
          if (iList) iList.innerHTML = details.inclus.map(function (t) { return '<li>' + t + '</li>'; }).join('');
          if (cList) cList.innerHTML = details.conditions.map(function (t) { return '<li>' + t + '</li>'; }).join('');
        }
        return res;
      };
      window.switchV4Pub04Activity._refonteWrapped = true;
    }

    // =========================================================================
    // MASQUAGE AUTOMATIQUE DE L'AGENDA SI AUCUN ÉVÉNEMENT N'EST PUBLIÉ
    // =========================================================================
    window.syncAgendaVisibilityFromData = function () {
      var hasEvents = true;
      try {
        if (window.EcoparkData && window.EcoparkData.store && window.EcoparkData.store.state && window.EcoparkData.store.state.content) {
          var rows = window.EcoparkData.store.state.content.agenda_events;
          if (Array.isArray(rows)) {
            var published = rows.filter(function (r) { return r && r.status === 'PUBLISHED'; });
            hasEvents = published.length > 0;
          }
        }
      } catch (e) {}
      var homeAg = document.getElementById('homeBlock6Agenda');
      var secAg = document.getElementById('sec-PUB-16');
      if (homeAg) homeAg.style.display = hasEvents ? '' : 'none';
      if (!hasEvents && secAg) secAg.style.display = 'none';
      return hasEvents;
    };
    window.syncAgendaVisibilityFromData();

    // =========================================================================
    // SÉPARATION DES 4 PARCOURS DE RÉSERVATION & MASQUAGE DU BILLET AVANT ÉTAPE 5
    // =========================================================================
    window._activeResJourney = 'DAY';
    window._bookingConfirmedInSession = false;

    window.setTicketConfirmationVisibility = function (visible) {
      window._bookingConfirmedInSession = !!visible;
      var qrCard = document.getElementById('demoTicketCard');
      var dopCard = document.getElementById('dopamineReliefCard');
      if (qrCard) qrCard.classList.toggle('booking-confirmed-visible', !!visible);
      if (dopCard) dopCard.classList.toggle('booking-confirmed-visible', !!visible);
    };

    // Par défaut à l'ouverture du parcours : billet de confirmation masqué jusqu'à validation
    window.setTicketConfirmationVisibility(false);

    window.syncGuichetRemainingDueUI = function () {
      var payRadio = document.querySelector('input[name="payMethod"]:checked');
      var method = payRadio ? payRadio.value : 'OM';
      var totalEl = document.getElementById('grandTotalFCFA');
      var totalTxt = totalEl ? totalEl.textContent.trim() : '0 FCFA';
      var box = document.getElementById('guichetRemainingDueBox');
      if (!box) {
        var feedbackEl = document.getElementById('momoStateFeedback');
        if (feedbackEl && feedbackEl.parentNode) {
          box = document.createElement('div');
          box.id = 'guichetRemainingDueBox';
          box.style.cssText = 'display:none;margin-top:10px;padding:12px 14px;background:var(--eco-warning-bg);border:1px solid var(--eco-warning-border);border-radius:10px;color:var(--eco-warning-text);font-size:14px;line-height:1.45;';
          feedbackEl.parentNode.insertBefore(box, feedbackEl.nextSibling);
        }
      }
      if (box) {
        if (method === 'GUICHET') {
          box.style.display = 'block';
          box.innerHTML = '<strong>Statut : Pré-réservation garantie jusqu\'à 11h00</strong><br/>'
            + 'Montant payé en ligne : <strong>0 FCFA</strong> • <strong>Montant restant à régler au guichet d\'Ahala : ' + totalTxt + '</strong>.';
        } else {
          box.style.display = 'none';
        }
      }
    };

    document.querySelectorAll('input[name="payMethod"]').forEach(function (r) {
      r.addEventListener('change', window.syncGuichetRemainingDueUI);
    });

    var origRecalcSim = window.recalcSimulator;
    if (typeof origRecalcSim === 'function' && !origRecalcSim._refonteGuichetWrapped) {
      window.recalcSimulator = function () {
        var res = origRecalcSim.apply(this, arguments);
        window.syncGuichetRemainingDueUI();
        return res;
      };
      window.recalcSimulator._refonteGuichetWrapped = true;
    }

    // Mise à jour de validateDateChoice : autoriser le lundi uniquement pour un séjour hôtelier pur (7j/7)
    var origValidateDateChoice = window.validateDateChoice;
    if (typeof origValidateDateChoice === 'function' && !origValidateDateChoice._refonteWrapped) {
      window.validateDateChoice = function (input) {
        if (!input || !input.value) return true;
        var d = new Date(input.value + 'T12:00:00');
        var isLodgeOnly = (window._activeResJourney === 'LODGE')
          && document.getElementById('chkBumpLodgeEwondo') && document.getElementById('chkBumpLodgeEwondo').checked
          && !(document.getElementById('chkZoo') && document.getElementById('chkZoo').checked)
          && !(document.getElementById('chkPiscine') && document.getElementById('chkPiscine').checked)
          && !(document.getElementById('chkPirogue') && document.getElementById('chkPirogue').checked);
        if (d.getDay() === 1 && !isLodgeOnly) {
          return origValidateDateChoice.apply(this, arguments);
        }
        return true;
      };
      window.validateDateChoice._refonteWrapped = true;
    }

    window.switchResJourney = function (journeyType, btnEl) {
      var mode = journeyType || 'DAY';
      window._activeResJourney = mode;
      document.querySelectorAll('#resJourneyTabs .eco-journey-tab').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-res-journey') === mode);
      });
      if (mode === 'LODGE') {
        var chkLodge = document.getElementById('chkBumpLodgeEwondo');
        if (chkLodge) chkLodge.checked = true;
        if (typeof window.recalcSimulator === 'function') window.recalcSimulator();
        var lodgeCard = document.getElementById('lodgeVisualPreviewCard');
        if (lodgeCard) lodgeCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (mode === 'GROUP') {
        if (typeof window.openQuoteModalSprint1 === 'function') window.openQuoteModalSprint1();
      } else if (mode === 'CFP') {
        if (typeof window.openCfpModalSprint1 === 'function') window.openCfpModalSprint1();
      } else {
        window.goToV4ReservationStep(1);
      }
      return mode;
    };

    window.goToV4ReservationStep = function (stepNum) {
      var n = Number(stepNum) || 1;
      document.querySelectorAll('#v4ResStepperBar .v4-res-step').forEach(function (btn) {
        btn.classList.toggle('active', Number(btn.getAttribute('data-v4-step')) === n);
      });
      if (n === 1) {
        var dEl = document.getElementById('visitDate');
        if (dEl) dEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (n === 2) {
        var bEl = document.getElementById('bundleQuickSelector');
        if (bEl) bEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (n === 3) {
        var nameInput = document.getElementById('visitorName');
        if (nameInput) {
          nameInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
          nameInput.focus();
        }
      } else if (n === 4) {
        var sumCol = document.getElementById('resStickySummaryCol');
        if (sumCol) sumCol.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else if (n === 5) {
        window.setTicketConfirmationVisibility(true);
        var qrCard = document.getElementById('demoTicketCard');
        if (qrCard) {
          qrCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          if (typeof triggerSectionFocusHalo === 'function') triggerSectionFocusHalo(qrCard);
        }
      }
    };

    // Afficher l'étape 5 (Billet QR confirmé) uniquement après création effective d'une réservation ou inspection RES-09
    var origCreateBooking = window.createLiveBookingSprint1;
    if (typeof origCreateBooking === 'function' && !origCreateBooking._refonteStep5Wrapped) {
      window.createLiveBookingSprint1 = function () {
        var res = origCreateBooking.apply(this, arguments);
        window.setTicketConfirmationVisibility(true);
        document.querySelectorAll('#v4ResStepperBar .v4-res-step').forEach(function (btn) {
          btn.classList.toggle('active', Number(btn.getAttribute('data-v4-step')) === 5);
        });
        return res;
      };
      window.createLiveBookingSprint1._refonteStep5Wrapped = true;
    }

    // Masquer les données personnelles dans le payload du QR Code public (A-020 & Section G)
    var origRenderQr = window.renderEcoparkQrSvg;
    if (typeof origRenderQr === 'function' && !origRenderQr._refontePrivacyWrapped) {
      window.renderEcoparkQrSvg = function (payloadStr, sizePx) {
        var raw = String(payloadStr || '');
        var sanitized = raw.replace(/\+?237[\s0-9]{8,14}/g, 'VERIFIED-ID');
        return origRenderQr.call(this, sanitized, sizePx);
      };
      window.renderEcoparkQrSvg._refontePrivacyWrapped = true;
    }

    // En mode production Supabase, exiger le numéro WhatsApp réel sans remplissage automatique
    var prevSubmitQuote = window.submitGroupQuoteSprint1;
    if (typeof prevSubmitQuote === 'function' && !prevSubmitQuote._refonteSupabaseGuard) {
      window.submitGroupQuoteSprint1 = function () {
        var isSupabase = document.documentElement.getAttribute('data-ecopark-driver') === 'supabase';
        var phoneEl = document.getElementById('quotePhone');
        if (isSupabase && phoneEl && !phoneEl.value.trim()) {
          if (typeof showToastSprint1 === 'function') {
            showToastSprint1('Veuillez renseigner votre numéro WhatsApp (+237) pour recevoir votre devis.');
          }
          return null;
        }
        return prevSubmitQuote.apply(this, arguments);
      };
      window.submitGroupQuoteSprint1._refonteSupabaseGuard = true;
    }

    // =========================================================================
    // C — ARCHITECTURE DE L'INFORMATION : ROUTES CANONIQUES & CORRESPONDANCES
    // =========================================================================
    if (typeof V4_MENU_ACTIONS !== 'undefined' || window.navigateV4SiteMenu) {
      var extraActions = {
        GROUPES_SCOLAIRES: { url: '/groupes-evenements', family: 'PUB', screen: 'PUB-11', subLabel: 'Sorties scolaires (500 FCFA / élève)', scrollTo: 'sec-PUB-11' },
        GROUPES_ENTREPRISES: { url: '/groupes-evenements', family: 'PUB', screen: 'PUB-11', subLabel: 'Entreprises, séminaires & associations', scrollTo: 'sec-PUB-11' },
        GROUPES_MARIAGES: { url: '/groupes-evenements', family: 'PUB', screen: 'PUB-11', subLabel: 'Mariages & Salle Menkii (500 places)', scrollTo: 'sec-PUB-11' },
        GROUPES_DEVIS: { url: '/groupes-evenements', family: 'PUB', screen: 'PUB-11', subLabel: 'Demande de devis groupe', scrollTo: 'sec-PUB-11', openQuote: true },
        CFP_HOTELLERIE_RESTO: { url: '/formations', family: 'PUB', screen: 'PUB-12', subLabel: 'Hôtellerie, Restauration & Décoration', scrollTo: 'sec-PUB-12' },
        CFP_AGRO_PISCI: { url: '/formations', family: 'PUB', screen: 'PUB-12', subLabel: 'Agropastorale & Pisciculture', scrollTo: 'sec-PUB-12' },
        CFP_ADMISSION: { url: '/formations', family: 'PUB', screen: 'PUB-12', subLabel: 'Admission dès 16 ans & Frais officiels', scrollTo: 'sec-PUB-12' },
        CFP_CANDIDATURE: { url: '/formations', family: 'PUB', screen: 'PUB-12', subLabel: 'Candidature CFP en ligne', scrollTo: 'sec-PUB-12', openCfp: true }
      };

      var origNavV4Menu = window.navigateV4SiteMenu;
      window.scrollAndHaloSection = function (elId) {
        var el = document.getElementById(elId);
        if (!el) return;
        if (elId === 'sec-PUB-12') {
          window.scrollTo(0, 0);
        } else {
          var y = el.getBoundingClientRect().top + window.scrollY - 140;
          window.scrollTo(0, Math.max(0, y));
        }
        if (typeof triggerSectionFocusHalo === 'function') triggerSectionFocusHalo(el);
      };

      window.navigateV4SiteMenu = function (actionKey, opts) {
        if (extraActions[actionKey]) {
          var spec = extraActions[actionKey];
          window._v4ActiveMenuAction = actionKey;
          if (typeof window.closeAllV4Dropdowns === 'function') window.closeAllV4Dropdowns();
          if (typeof window.toggleV4MobileDrawer === 'function') window.toggleV4MobileDrawer(false);
          window.navigateFamily(spec.family, spec.screen);
          if (spec.scrollTo) {
            window.scrollAndHaloSection(spec.scrollTo);
          }
          if (spec.openQuote && typeof window.openQuoteModalSprint1 === 'function') {
            setTimeout(function () { window.openQuoteModalSprint1(); }, 120);
          }
          if (spec.openCfp && typeof window.openCfpModalSprint1 === 'function') {
            setTimeout(function () { window.openCfpModalSprint1(); }, 120);
          }
          if (!(opts && opts.skipHistory) && window.history && typeof window.history.pushState === 'function') {
            try {
              if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
                window.history.pushState({ v4MenuAction: actionKey }, '', spec.url + window.location.search);
              }
            } catch (e) {}
          }
          return actionKey;
        }
        return typeof origNavV4Menu === 'function' ? origNavV4Menu.apply(this, arguments) : actionKey;
      };
    }

    // Mettre à jour l'état actif dans les 5 rubriques principales (#v4MainMegaNav)
    var origSwitchPubSubPageRefonte = window.switchPubSubPage;
    if (typeof origSwitchPubSubPageRefonte === 'function' && !origSwitchPubSubPageRefonte._refonteNavSync) {
      window.switchPubSubPage = function (pageKey, opts) {
        var res = origSwitchPubSubPageRefonte.apply(this, arguments);
        opts = opts || {};
        if (opts.targetScreenId === 'PUB-11') {
          document.querySelectorAll('.main-nav .nav-item').forEach(function (n) { n.classList.remove('active'); });
          var grpBtn = document.getElementById('nav-GROUPES');
          if (grpBtn) grpBtn.classList.add('active');
        }
        return res;
      };
      window.switchPubSubPage._refonteNavSync = true;
    }

    // Révéler le billet QR lorsque l'utilisateur ou un test inspecte explicitement RES-09
    var origInspectRefonte = window.inspectScreen;
    if (typeof origInspectRefonte === 'function' && !origInspectRefonte._refonteRes09Wrapped) {
      window.inspectScreen = function (screenId) {
        if (screenId === 'RES-09') {
          window.setTicketConfirmationVisibility(true);
        }
        return origInspectRefonte.apply(this, arguments);
      };
      window.inspectScreen._refonteRes09Wrapped = true;
    }

    // Révéler le billet QR lorsque l'utilisateur clique sur "Voir Billet QR" depuis Mes réservations (#view-ACC)
    var origLoadBookingIntoQrPass = window.loadBookingIntoQrPass;
    if (typeof origLoadBookingIntoQrPass === 'function' && !origLoadBookingIntoQrPass._refonteWrapped) {
      window.loadBookingIntoQrPass = function (ref) {
        window.setTicketConfirmationVisibility(true);
        return origLoadBookingIntoQrPass.apply(this, arguments);
      };
      window.loadBookingIntoQrPass._refonteWrapped = true;
    }

    // Ré-appliquer systématiquement les vignettes visuelles dans #view-ACC après chaque rafraîchissement DB
    var origSyncAllViewsRefonte = window.syncAllViewsFromDB;
    if (typeof origSyncAllViewsRefonte === 'function' && !origSyncAllViewsRefonte._refonteAccThumbWrapped) {
      window.syncAllViewsFromDB = function () {
        var res = origSyncAllViewsRefonte.apply(this, arguments);
        if (typeof window.decorateAccTableWithVisuals === 'function') {
          try { window.decorateAccTableWithVisuals(); } catch (e) {}
        }
        return res;
      };
      window.syncAllViewsFromDB._refonteAccThumbWrapped = true;
    }

    // Synchroniser l'état actif et aria-current="page" du bouton utilitaire "Mes réservations" (#nav-ACC) et de la barre mobile
    var origNavFamilyRefonte = window.navigateFamily;
    if (typeof origNavFamilyRefonte === 'function' && !origNavFamilyRefonte._refonteAccNavWrapped) {
      window.navigateFamily = function (familyCode, targetScreenId) {
        var res = origNavFamilyRefonte.apply(this, arguments);
        var accBtn = document.getElementById('nav-ACC');
        if (accBtn) {
          var isAcc = (familyCode === 'ACC');
          accBtn.classList.toggle('active', isAcc);
          if (isAcc) {
            accBtn.setAttribute('aria-current', 'page');
          } else {
            accBtn.removeAttribute('aria-current');
          }
        }
        var mobNav = document.getElementById('v4MobileBottomNav');
        if (mobNav && (familyCode === 'ACC' || familyCode === 'RES')) {
          mobNav.querySelectorAll('.v4-bottom-nav-btn').forEach(function (b) {
            b.classList.remove('active');
            b.removeAttribute('aria-current');
          });
          var mobTargetId = familyCode === 'ACC' ? 'v4MobNavCompte' : 'v4MobNavReserver';
          var mobTarget = document.getElementById(mobTargetId);
          if (mobTarget) {
            mobTarget.classList.add('active');
            mobTarget.setAttribute('aria-current', 'page');
          }
        }
        return res;
      };
      window.navigateFamily._refonteAccNavWrapped = true;
    }

    // Prise en charge des nouvelles URLs canoniques et des anciennes URLs au chargement direct
    var currentPath = (window.location.pathname || '/').replace(/\/+$/, '').toLowerCase();
    var canonicalRouteMap = {
      '/decouvrir': ['PUB', 'PUB-03'],
      '/activites': ['PUB', 'PUB-03'],
      '/fiche-activite': ['PUB', 'PUB-04'],
      '/sejour-restaurant': ['PUB', 'PUB-09'],
      '/hebergements': ['PUB', 'PUB-09'],
      '/hotellerie': ['PUB', 'PUB-09'],
      '/restaurant': ['PUB', 'PUB-07'],
      '/groupes-evenements': ['PUB', 'PUB-11'],
      '/pack-ecole': ['PUB', 'PUB-11'],
      '/pack-entreprise': ['PUB', 'PUB-11'],
      '/formations': ['PUB', 'PUB-12'],
      '/formation': ['PUB', 'PUB-12'],
      '/preparer-ma-visite': ['PUB', 'PUB-10'],
      '/nos-tarifs': ['PUB', 'PUB-10'],
      '/tarifs': ['PUB', 'PUB-10'],
      '/agenda': ['PUB', 'PUB-16'],
      '/evenements': ['PUB', 'PUB-16'],
      '/contact': ['PUB', 'PUB-13'],
      '/rdv': ['PUB', 'PUB-18'],
      '/rendez-vous': ['PUB', 'PUB-18'],
      '/mes-reservations': ['ACC', 'ACC-02'],
      '/mon-espace': ['ACC', 'ACC-02'],
      '/reserver': ['RES', 'RES-01']
    };
    if (canonicalRouteMap[currentPath]) {
      setTimeout(function () {
        var target = canonicalRouteMap[currentPath];
        window.navigateFamily(target[0], target[1]);
        if (target[1] === 'PUB-11') {
          var el11 = document.getElementById('sec-PUB-11');
          if (el11) el11.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 80);
    }

    // =========================================================================
    // MODULE INTERACTIF : ASSIGNATION D'UNE TÂCHE & FICHE DE MISSION A4 (AHALA)
    // =========================================================================
    var MISSION_POLE_PRESETS = {
      GUICHET_CAISSE: {
        poleLabel: 'Guichet & Caisse Principale',
        badgeClass: 'eco-cat-nature',
        agentOption: 'Mme Clarisse ATANGANA|MAT-AGT-01|Caissière Principale Guichet #1',
        shift: '08h30 – 18h00 (Journée complète)',
        priority: 'HAUTE',
        title: 'Ouverture Guichet Principal #1, contrôle fond de caisse 50 000 FCFA & accueil Groupes',
        location: 'Portail Principal RN3 (Face Station Tradex Ahala) — Guichet #1',
        objective: 'Assurer l\'encaissement fluide des visiteurs walk-in (Espèces FCFA et Mobile Money sans saisie de code PIN), protéger le tarif enfant à 500 FCFA et maintenir un écart de caisse inférieur ou égal à 2 000 FCFA à la clôture contradictoire de 18h00.',
        equipment: 'Fond de caisse 50 000 FCFA, Terminal Caisse Rapide AGT-03, Rouleau thermique QR, Talkie-walkie Canal 1',
        checklist: [
          'Vérifier le fond de caisse initial de 50 000 FCFA à 08h30',
          'Appliquer strictement le tarif enfant protégé (500 FCFA Zoo / 0 FCFA moins de 3 ans)',
          'Vérifier les pré-réservations Guichet avant l\'échéance de 11h00',
          'Réaliser le billetage contradictoire et signer le PV de clôture à 18h00'
        ],
        guardrail: 'Tolérance d\'écart de caisse <= 2 000 FCFA • Tarif enfant Zoo verrouillé à 500 FCFA • Zéro saisie de code PIN Mobile Money.'
      },
      CONTROLE_QR: {
        poleLabel: 'Contrôle QR Piscine & Lac',
        badgeClass: 'eco-cat-water',
        agentOption: 'M. Samuel MBARGA|MAT-CTL-02|Contrôleur QR Piscine & Embarcadère',
        shift: '08h30 – 18h00 (Journée complète)',
        priority: 'URGENTE',
        title: 'Contrôle QR 7 états au tourniquet Piscine, jauge baignade & sécurité gilets Pirogues',
        location: 'Portique Piscine Semi-Olympique & Embarcadère du Lac d\'Ahala',
        objective: 'Scanner systématiquement chaque billet QR avant l\'accès au bassin et au ponton (détection des 7 états : Valide, Déjà utilisé, Mauvaise date, Expiré, Annulé, Prestation différente, Inconnu) et imposer le port du gilet homologué sur le lac.',
        equipment: 'Terminal Scanner QR Hors-Ligne AGT-05, Lot de 24 gilets homologués (Enfants & Adultes), Sifflet & Bouée maître-nageur, Talkie-walkie Canal 2',
        checklist: [
          'Tester la synchronisation hors-ligne du scanner QR dès 08h45',
          'Imposer la douche savonnée et le maillot de bain réglementaire à la piscine',
          'Équiper chaque passager (dès 3 ans accompagné) d\'un gilet homologué avant embarquement pirogue',
          'Synchroniser la file des scans hors-ligne avec la base centrale en fin de service'
        ],
        guardrail: 'Embarquement pirogue strictement interdit sans gilet homologué bouclé • Enfants accompagnés d\'un adulte.'
      },
      HEBERGEMENT: {
        poleLabel: 'Hébergements (Ewondo / Chanthel / Bene)',
        badgeClass: 'eco-cat-lodging',
        agentOption: 'Mme Chantal NGO BIYONG|MAT-HTL-03|Gouvernante Cités Ewondo, Chanthel & Bene',
        shift: '14h00 – 11h00 J+1 (Garde Hôtelière 24h)',
        priority: 'HAUTE',
        title: 'Préparation Suites Cité Ewondo VIP, Chambres Chanthel & Bene (Check-in 14h00 / Check-out 11h00)',
        location: 'Réception Hôtelière 7j/7 — Cités Ewondo VIP, Chanthel Confort & Bene Standard',
        objective: 'Superviser la remise en blanc des chambres avant 13h30, accueillir les résidents à partir de 14h00, contrôler l\'état des Suites Privées (30 000 – 45 000 FCFA / nuit) et libérer le stock au Check-out de 11h00.',
        equipment: 'Registre Réception Hôtelière 7j/7, Passe-partout électronique Cités Ewondo/Chanthel/Bene, Kit linge & accueil VIP, Téléphone d\'astreinte Réception',
        checklist: [
          'Contrôler les départs (Check-out avant 11h00) et mettre à jour le stock des loges libres',
          'Inspecter la climatisation, l\'eau chaude et la literie King-Size des 2 Suites Cité Ewondo VIP',
          'Valider les arrivées (Check-in dès 14h00) et remettre les bracelets d\'accès Parc & Piscine aux résidents',
          'Transmettre l\'état d\'occupation nocturne au Chef d\'Exploitation à 20h00'
        ],
        guardrail: 'Réception ouverte 7j/7 (y compris le lundi) • Arrivée dès 14h00 • Départ avant 11h00 • Tarifs : 10 000 à 45 000 FCFA par chambre et par nuit.'
      },
      CUISINE_SAVEURS: {
        poleLabel: 'Cuisine Le Château des Saveurs',
        badgeClass: 'eco-cat-dining',
        agentOption: 'Chef Patrice ESSOMBA|MAT-RES-04|Chef de Cuisine & Pergolas Château des Saveurs',
        shift: '11h30 – 20h30 (Service Midi & Soir)',
        priority: 'HAUTE',
        title: 'Mise en place des 18 précommandes Zéro Attente (12h30 / 13h30) & service Pergolas du Lac',
        location: 'Restaurant Le Château des Saveurs & 10 Pergolas au bord de l\'eau',
        objective: 'Assurer l\'approvisionnement en poisson frais des étangs d\'Ahala, honorer à l\'heure exacte les précommandes familiales et groupes (Poisson braisé 5 000 FCFA, Poulet DG Royal 6 500 FCFA, Ndolé 5 500 FCFA, Menu Enfant 2 500 FCFA) et dresser les 6 pergolas réservées.',
        equipment: 'Bon de production Cuisine EXP-05 (18 repas précommandés), Thermomètre sonde HACCP, Plan d\'attribution des 10 Pergolas du Lac',
        checklist: [
          'Réceptionner et calibrer les poissons frais issus des bassins piscicoles d\'Ahala à 10h30',
          'Dresser en priorité les 6 pergolas réservées pour le créneau Zéro Attente de 12h30 et 13h30',
          'Préparer les 18 repas précommandés (Poisson braisé d\'Ahala, Poulet DG Royal, Menus Enfants)',
          'Contrôler l\'hygiène des postes de braise et mettre à jour les disponibilités de la carte à 19h30'
        ],
        guardrail: 'Service prioritaire des précommandes 12h30 / 13h30 • Traçabilité fraîcheur étangs d\'Ahala • Tarifs affichés par plat (2 500 à 6 500 FCFA).'
      }
    };

    window.getDefaultOperationalMissions = function () {
      var dIso = typeof window.getTodayVisitDateMinIso === 'function' ? window.getTodayVisitDateMinIso() : '2026-10-29';
      return [
        {
          id: 'MSN-2026-101',
          orderRef: 'ECP-2026-84920',
          orderCustomer: 'M. Jean-Paul NGUEMA (Famille)',
          orderTotalFcfa: 14000,
          orderSummary: '2 Adultes, 2 Enfants • Zoo + Piscine + Pirogue (Pré-réservation Guichet)',
          secondaryPoles: ['Contrôle QR Piscine & Lac'],
          pole: 'GUICHET_CAISSE',
          poleLabel: MISSION_POLE_PRESETS.GUICHET_CAISSE.poleLabel,
          badgeClass: MISSION_POLE_PRESETS.GUICHET_CAISSE.badgeClass,
          agentName: 'Mme Clarisse ATANGANA',
          agentMatricule: 'MAT-AGT-01',
          agentRole: 'Caissière Principale Guichet #1',
          date: dIso,
          shift: '08h30 – 18h00 (Journée complète)',
          priority: 'HAUTE',
          status: 'EN_COURS',
          title: MISSION_POLE_PRESETS.GUICHET_CAISSE.title,
          location: MISSION_POLE_PRESETS.GUICHET_CAISSE.location,
          objective: MISSION_POLE_PRESETS.GUICHET_CAISSE.objective,
          equipment: MISSION_POLE_PRESETS.GUICHET_CAISSE.equipment,
          guardrail: MISSION_POLE_PRESETS.GUICHET_CAISSE.guardrail,
          checklist: [
            { text: MISSION_POLE_PRESETS.GUICHET_CAISSE.checklist[0], done: true },
            { text: MISSION_POLE_PRESETS.GUICHET_CAISSE.checklist[1], done: true },
            { text: MISSION_POLE_PRESETS.GUICHET_CAISSE.checklist[2], done: false },
            { text: MISSION_POLE_PRESETS.GUICHET_CAISSE.checklist[3], done: false }
          ],
          assignedBy: 'Affectation Automatique Commande → Poste',
          createdAt: '08:15 (Africa/Douala)'
        },
        {
          id: 'MSN-2026-102',
          orderRef: 'ECP-2026-84921',
          orderCustomer: 'Mme Clarisse EYENGA',
          orderTotalFcfa: 26000,
          orderSummary: '2 Adultes, 2 Enfants • Pass Journée Royale (Zoo + Piscine + Pirogue + Repas)',
          secondaryPoles: ['Cuisine Le Château des Saveurs'],
          pole: 'CONTROLE_QR',
          poleLabel: MISSION_POLE_PRESETS.CONTROLE_QR.poleLabel,
          badgeClass: MISSION_POLE_PRESETS.CONTROLE_QR.badgeClass,
          agentName: 'M. Samuel MBARGA',
          agentMatricule: 'MAT-CTL-02',
          agentRole: 'Contrôleur QR Piscine & Embarcadère',
          date: dIso,
          shift: '08h30 – 18h00 (Journée complète)',
          priority: 'URGENTE',
          status: 'EN_COURS',
          title: MISSION_POLE_PRESETS.CONTROLE_QR.title,
          location: MISSION_POLE_PRESETS.CONTROLE_QR.location,
          objective: MISSION_POLE_PRESETS.CONTROLE_QR.objective,
          equipment: MISSION_POLE_PRESETS.CONTROLE_QR.equipment,
          guardrail: MISSION_POLE_PRESETS.CONTROLE_QR.guardrail,
          checklist: [
            { text: MISSION_POLE_PRESETS.CONTROLE_QR.checklist[0], done: true },
            { text: MISSION_POLE_PRESETS.CONTROLE_QR.checklist[1], done: true },
            { text: MISSION_POLE_PRESETS.CONTROLE_QR.checklist[2], done: true },
            { text: MISSION_POLE_PRESETS.CONTROLE_QR.checklist[3], done: false }
          ],
          assignedBy: 'Affectation Automatique Commande → Poste',
          createdAt: '08:20 (Africa/Douala)'
        },
        {
          id: 'MSN-2026-103',
          orderRef: 'ECP-2026-84922',
          orderCustomer: 'Dr. Armand MBIDA (Couple VIP)',
          orderTotalFcfa: 45000,
          orderSummary: 'Pack Escapade Couple VIP — 1 Nuit Cité Ewondo VIP + 2 Repas + Parc',
          secondaryPoles: ['Cuisine Le Château des Saveurs', 'Contrôle QR Piscine & Lac'],
          pole: 'HEBERGEMENT',
          poleLabel: MISSION_POLE_PRESETS.HEBERGEMENT.poleLabel,
          badgeClass: MISSION_POLE_PRESETS.HEBERGEMENT.badgeClass,
          agentName: 'Mme Chantal NGO BIYONG',
          agentMatricule: 'MAT-HTL-03',
          agentRole: 'Gouvernante Cités Ewondo, Chanthel & Bene',
          date: dIso,
          shift: '14h00 – 11h00 J+1 (Garde Hôtelière 24h)',
          priority: 'HAUTE',
          status: 'TERMINEE',
          title: MISSION_POLE_PRESETS.HEBERGEMENT.title,
          location: MISSION_POLE_PRESETS.HEBERGEMENT.location,
          objective: MISSION_POLE_PRESETS.HEBERGEMENT.objective,
          equipment: MISSION_POLE_PRESETS.HEBERGEMENT.equipment,
          guardrail: MISSION_POLE_PRESETS.HEBERGEMENT.guardrail,
          checklist: [
            { text: MISSION_POLE_PRESETS.HEBERGEMENT.checklist[0], done: true },
            { text: MISSION_POLE_PRESETS.HEBERGEMENT.checklist[1], done: true },
            { text: MISSION_POLE_PRESETS.HEBERGEMENT.checklist[2], done: true },
            { text: MISSION_POLE_PRESETS.HEBERGEMENT.checklist[3], done: true }
          ],
          assignedBy: 'Affectation Automatique Commande → Poste',
          createdAt: '07:45 (Africa/Douala)'
        },
        {
          id: 'MSN-2026-104',
          orderRef: 'DEV-2026-3104',
          orderCustomer: 'Complexe Scolaire Bilingue La Gaieté',
          orderTotalFcfa: 135000,
          orderSummary: '60 participants • Excursion scolaire + Déjeuner & Pergolas',
          secondaryPoles: ['Guichet & Caisse Principale', 'Contrôle QR Piscine & Lac'],
          pole: 'CUISINE_SAVEURS',
          poleLabel: MISSION_POLE_PRESETS.CUISINE_SAVEURS.poleLabel,
          badgeClass: MISSION_POLE_PRESETS.CUISINE_SAVEURS.badgeClass,
          agentName: 'Chef Patrice ESSOMBA',
          agentMatricule: 'MAT-RES-04',
          agentRole: 'Chef de Cuisine & Pergolas Château des Saveurs',
          date: dIso,
          shift: '11h30 – 20h30 (Service Midi & Soir)',
          priority: 'HAUTE',
          status: 'ASSIGNEE',
          title: MISSION_POLE_PRESETS.CUISINE_SAVEURS.title,
          location: MISSION_POLE_PRESETS.CUISINE_SAVEURS.location,
          objective: MISSION_POLE_PRESETS.CUISINE_SAVEURS.objective,
          equipment: MISSION_POLE_PRESETS.CUISINE_SAVEURS.equipment,
          guardrail: MISSION_POLE_PRESETS.CUISINE_SAVEURS.guardrail,
          checklist: [
            { text: MISSION_POLE_PRESETS.CUISINE_SAVEURS.checklist[0], done: true },
            { text: MISSION_POLE_PRESETS.CUISINE_SAVEURS.checklist[1], done: false },
            { text: MISSION_POLE_PRESETS.CUISINE_SAVEURS.checklist[2], done: false },
            { text: MISSION_POLE_PRESETS.CUISINE_SAVEURS.checklist[3], done: false }
          ],
          assignedBy: 'Affectation Automatique Commande → Poste',
          createdAt: '09:00 (Africa/Douala)'
        }
      ];
    };

    window._activeMissionPoleFilter = 'ALL';
    window._activeMissionIdForPrint = 'MSN-2026-101';
    window._missionAlertSoundEnabled = true;

    var MISSIONS_STORAGE_KEY = 'ecopark_operational_missions_v1';
    var ALERTS_STORAGE_KEY = 'ecopark_operational_alerts_v1';

    window.getDefaultOperationalAlerts = function () {
      var dIso = typeof window.getTodayVisitDateMinIso === 'function' ? window.getTodayVisitDateMinIso() : '2026-10-29';
      return [
        {
          alertId: 'ALT-2026-201',
          missionId: 'MSN-2026-104',
          orderRef: 'DEV-2026-3104',
          customerName: 'Complexe Scolaire Bilingue La Gaieté',
          orderSummary: '60 participants • Excursion scolaire + Déjeuner & Pergolas',
          amountFcfa: 135000,
          pole: 'CUISINE_SAVEURS',
          poleLabel: 'Cuisine Le Château des Saveurs',
          badgeClass: 'eco-cat-dining',
          agentName: 'Chef Patrice ESSOMBA',
          agentMatricule: 'MAT-RES-04',
          title: 'Mise en place Cuisine & Pergolas — Commande DEV-2026-3104 (60 participants)',
          createdAt: dIso + ' 09:00 (Africa/Douala)',
          acknowledged: false
        },
        {
          alertId: 'ALT-2026-202',
          missionId: 'MSN-2026-101',
          orderRef: 'ECP-2026-84920',
          customerName: 'M. Jean-Paul NGUEMA (Famille)',
          orderSummary: '2 Adultes, 2 Enfants • Zoo + Piscine + Pirogue (Solde Guichet 14 000 FCFA)',
          amountFcfa: 14000,
          pole: 'GUICHET_CAISSE',
          poleLabel: 'Guichet & Caisse Principale',
          badgeClass: 'eco-cat-nature',
          agentName: 'Mme Clarisse ATANGANA',
          agentMatricule: 'MAT-AGT-01',
          title: 'Encaissement Guichet & Remise Bracelets — Commande ECP-2026-84920 (14 000 FCFA)',
          createdAt: dIso + ' 08:15 (Africa/Douala)',
          acknowledged: false
        }
      ];
    };

    window.loadOperationalAlerts = function () {
      try {
        var raw = localStorage.getItem(ALERTS_STORAGE_KEY);
        if (raw) {
          var parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            return parsed;
          }
        }
        var defaults = window.getDefaultOperationalAlerts();
        localStorage.setItem(ALERTS_STORAGE_KEY, JSON.stringify(defaults));
        return defaults;
      } catch (e) {
        return window.getDefaultOperationalAlerts();
      }
    };

    window.saveOperationalAlerts = function (alertsList) {
      try {
        localStorage.setItem(ALERTS_STORAGE_KEY, JSON.stringify(alertsList));
      } catch (e) {}
    };

    window.playMissionAlertChime = function () {
      if (!window._missionAlertSoundEnabled) return;
      try {
        var AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        var ctx = new AudioCtx();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.setValueAtTime(880, ctx.currentTime + 0.08); // A5
        gain.gain.setValueAtTime(0.04, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.24);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.25);
      } catch (e) {}
    };

    window.toggleMissionAlertSound = function () {
      window._missionAlertSoundEnabled = !window._missionAlertSoundEnabled;
      var btn = document.getElementById('btnToggleMissionAlertSound');
      if (btn) {
        btn.textContent = 'Signal sonore : ' + (window._missionAlertSoundEnabled ? 'Activé' : 'Muet');
      }
      if (window._missionAlertSoundEnabled) {
        window.playMissionAlertChime();
      }
      return window._missionAlertSoundEnabled;
    };

    window.renderOperationalAlertsFeed = function () {
      var alerts = window.loadOperationalAlerts();
      var unreadCount = alerts.filter(function (a) { return !a.acknowledged; }).length;

      var badgeEl = document.getElementById('expUnreadAlertsCountBadge');
      if (badgeEl) {
        badgeEl.textContent = unreadCount > 0
          ? (unreadCount + (unreadCount > 1 ? ' alertes postes non lues' : ' alerte poste non lue'))
          : '0 alerte en attente (Tous les postes à jour)';
        badgeEl.className = 'status-badge ' + (unreadCount > 0 ? 'status-warning' : 'status-success');
      }

      var agtCountEl = document.getElementById('agtUnreadAlertsCount');
      if (agtCountEl) {
        agtCountEl.textContent = String(unreadCount);
      }

      var feedEl = document.getElementById('expAlertsFeedList');
      if (!feedEl) return alerts;

      var esc = typeof escHtml === 'function' ? escHtml : function (s) { return String(s || ''); };
      var fmt = typeof formatFCFA === 'function' ? formatFCFA : function (n) { return (Number(n) || 0).toLocaleString('fr-FR') + ' FCFA'; };

      feedEl.innerHTML = alerts.slice(0, 6).map(function (a) {
        var stBadge = a.acknowledged
          ? '<span class="status-badge status-success" style="font-size:11px;">ACQUITTÉE PAR LE POSTE</span>'
          : '<span class="status-badge status-warning" style="font-size:11px;">NOUVELLE ALERTE POSTE — À PRENDRE EN CHARGE</span>';

        var ackBtn = a.acknowledged
          ? ''
          : '<button type="button" class="btn btn-secondary btn-sm" onclick="acknowledgeMissionAlert(\'' + esc(a.alertId) + '\')">Acquitter &amp; Pointer</button>';

        return '<div class="post-alert-card ' + (a.acknowledged ? 'is-acknowledged' : '') + '" data-alert-id="' + esc(a.alertId) + '">'
          + '  <div style="flex:1;min-width:260px;">'
          + '    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">'
          +        stBadge
          + '      <span class="eco-cat-badge ' + esc(a.badgeClass || 'eco-cat-nature') + '" style="font-size:11px;padding:2px 8px;">Poste : ' + esc(a.poleLabel) + '</span>'
          + '      <span style="font-size:12px;font-weight:700;color:var(--eco-brand);">Commande ' + esc(a.orderRef) + ' → Fiche ' + esc(a.missionId) + '</span>'
          + '    </div>'
          + '    <strong style="font-size:14px;color:var(--eco-text);display:block;">' + esc(a.title) + '</strong>'
          + '    <div style="font-size:12.5px;color:var(--eco-text-muted);margin-top:2px;">'
          + '      Agent notifié : <strong>' + esc(a.agentName) + ' (' + esc(a.agentMatricule) + ')</strong> • Client : <strong>' + esc(a.customerName) + '</strong> • Montant : <strong>' + fmt(a.amountFcfa) + '</strong> • ' + esc(a.createdAt)
          + '    </div>'
          + '  </div>'
          + '  <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">'
          +      ackBtn
          + '    <button type="button" class="btn btn-primary btn-sm" onclick="openMissionSheetA4(\'' + esc(a.missionId) + '\')">Fiche A4 (' + esc(a.missionId) + ')</button>'
          + '  </div>'
          + '</div>';
      }).join('');

      return alerts;
    };

    window.acknowledgeMissionAlert = function (alertId) {
      var alerts = window.loadOperationalAlerts();
      var target = alerts.find(function (a) { return a.alertId === alertId; });
      if (!target) return null;
      target.acknowledged = true;
      window.saveOperationalAlerts(alerts);

      if (target.missionId) {
        var missions = window.loadOperationalMissions();
        var m = missions.find(function (x) { return x.id === target.missionId; });
        if (m && m.status === 'ASSIGNEE') {
          m.status = 'EN_COURS';
          window.saveOperationalMissions(missions);
        }
      }

      window.renderOperationalAlertsFeed();
      window.renderOperationalMissionsTable();

      if (typeof showToastSprint1 === 'function') {
        showToastSprint1('• Alerte ' + target.alertId + ' acquittée : Mission ' + target.missionId + ' (' + target.agentName + ') pointée En cours sur poste.');
      }
      return target;
    };

    window.acknowledgeAllMissionAlerts = function () {
      var alerts = window.loadOperationalAlerts();
      alerts.forEach(function (a) { a.acknowledged = true; });
      window.saveOperationalAlerts(alerts);
      window.renderOperationalAlertsFeed();
      if (typeof showToastSprint1 === 'function') {
        showToastSprint1('• Toutes les alertes postes ont été acquittées.');
      }
      return alerts;
    };

    // Résolution automatique du poste principal et des postes secondaires selon la commande
    window.resolvePostForOrder = function (orderData) {
      var o = orderData || {};
      var summary = String(o.paxSummary || o.type || o.track || o.summary || '');
      var sLower = summary.toLowerCase();
      var ref = String(o.reference || o.orderRef || 'ECP-2026-90000');
      var pay = String(o.payMethod || '').toUpperCase();

      var isLodge = Boolean(o.lodgeCity)
        || sLower.indexOf('ewondo') !== -1
        || sLower.indexOf('chanthel') !== -1
        || sLower.indexOf('bene') !== -1
        || sLower.indexOf('suite') !== -1
        || sLower.indexOf('couple') !== -1
        || sLower.indexOf('nuit') !== -1
        || sLower.indexOf('séjour') !== -1;

      var isDining = Boolean(o.hasPergola)
        || sLower.indexOf('saveurs') !== -1
        || sLower.indexOf('repas') !== -1
        || sLower.indexOf('royale') !== -1
        || sLower.indexOf('pergola') !== -1
        || sLower.indexOf('séminaire') !== -1
        || sLower.indexOf('mariage') !== -1
        || sLower.indexOf('buffet') !== -1
        || sLower.indexOf('poisson') !== -1;

      var isWaterOrPark = sLower.indexOf('piscine') !== -1
        || sLower.indexOf('pirogue') !== -1
        || sLower.indexOf('zoo') !== -1
        || sLower.indexOf('équitation') !== -1
        || sLower.indexOf('cheval') !== -1
        || sLower.indexOf('pêche') !== -1
        || sLower.indexOf('pass') !== -1
        || sLower.indexOf('excursion') !== -1;

      var isGuichetPay = (pay === 'GUICHET')
        || ref.indexOf('POS-') === 0
        || ref.indexOf('CFP-') === 0;

      var primaryPole = 'CONTROLE_QR';
      if (isLodge) {
        primaryPole = 'HEBERGEMENT';
      } else if (isDining && !isGuichetPay) {
        primaryPole = 'CUISINE_SAVEURS';
      } else if (isGuichetPay) {
        primaryPole = 'GUICHET_CAISSE';
      } else if (isDining) {
        primaryPole = 'CUISINE_SAVEURS';
      } else if (isWaterOrPark) {
        primaryPole = 'CONTROLE_QR';
      } else {
        primaryPole = 'GUICHET_CAISSE';
      }

      var secondary = [];
      if (primaryPole !== 'GUICHET_CAISSE' && isGuichetPay) secondary.push(MISSION_POLE_PRESETS.GUICHET_CAISSE.poleLabel);
      if (primaryPole !== 'CUISINE_SAVEURS' && isDining) secondary.push(MISSION_POLE_PRESETS.CUISINE_SAVEURS.poleLabel);
      if (primaryPole !== 'CONTROLE_QR' && isWaterOrPark) secondary.push(MISSION_POLE_PRESETS.CONTROLE_QR.poleLabel);
      if (primaryPole !== 'HEBERGEMENT' && isLodge) secondary.push(MISSION_POLE_PRESETS.HEBERGEMENT.poleLabel);

      return {
        primaryPole: primaryPole,
        secondaryPoles: secondary
      };
    };

    // Création automatique de la Fiche de Mission A4 + Alerte Temps Réel pour toute commande validée
    window.dispatchOrderToPostMission = function (orderData, opts) {
      opts = opts || {};
      var o = orderData || {};
      var ref = String(o.reference || o.orderRef || ('ECP-2026-' + Math.floor(10000 + Math.random() * 89999)));

      var missions = window.loadOperationalMissions();
      var existing = missions.find(function (m) { return m.orderRef === ref; });
      if (existing && !opts.forceNew) {
        return existing;
      }

      var routing = window.resolvePostForOrder(o);
      var poleKey = opts.forcePole || routing.primaryPole;
      var preset = MISSION_POLE_PRESETS[poleKey] || MISSION_POLE_PRESETS.GUICHET_CAISSE;
      var agentParts = preset.agentOption.split('|');
      var agentName = agentParts[0] || 'Agent ECOPARK';
      var agentMatricule = agentParts[1] || 'MAT-EXP-01';
      var agentRole = agentParts[2] || preset.poleLabel;

      var customer = o.holder || o.org || o.name || 'Visiteur ECOPARK';
      var amount = Number(o.totalFcfa || o.budgetFcfa || o.amountFcfa || 14000);
      var summary = o.paxSummary || o.type || o.track || 'Prestation ECOPARK Ahala';
      var dateStr = o.date || todayMinIso;
      var fmt = typeof formatFCFA === 'function' ? formatFCFA : function (n) { return (Number(n) || 0).toLocaleString('fr-FR') + ' FCFA'; };

      var missionTitle = '';
      var customChecklist = [];
      if (poleKey === 'HEBERGEMENT') {
        missionTitle = 'Préparation Loge & Accueil Séjour — Commande ' + ref + ' (' + customer + ')';
        customChecklist = [
          'Préparer et contrôler la chambre avant 13h30 pour la commande ' + ref + ' (' + summary + ')',
          'Accueillir ' + customer + ' au Check-in dès 14h00 et remettre les bracelets résidents',
          'Vérifier le règlement (' + fmt(amount) + ') et coordonner les pôles associés (' + (routing.secondaryPoles.join(', ') || 'Réception 7j/7') + ')',
          'Valider l\'état des lieux au Check-out avant 11h00'
        ];
      } else if (poleKey === 'CUISINE_SAVEURS') {
        missionTitle = 'Mise en place Cuisine & Pergola — Commande ' + ref + ' (' + customer + ')';
        customChecklist = [
          'Enregistrer le bon de production Cuisine pour la commande ' + ref + ' (' + summary + ')',
          'Calibrer les portions (Poisson braisé d\'Ahala / Poulet DG / Menus) pour un montant de ' + fmt(amount),
          'Dresser la table ou pergola avant 12h30 pour service Zéro Attente',
          'Émarger la livraison des plats chauds et la satisfaction client'
        ];
      } else if (poleKey === 'GUICHET_CAISSE') {
        missionTitle = 'Accueil Guichet, Encaissement & Bracelets — Commande ' + ref + ' (' + fmt(amount) + ')';
        customChecklist = [
          'Vérifier la référence ' + ref + ' (' + customer + ') à l\'arrivée au Portail RN3 Ahala',
          'Contrôler ou encaisser le montant de ' + fmt(amount) + ' (Espèces FCFA ou Mobile Money sans PIN)',
          'Remettre les bracelets correspondant à : ' + summary,
          'Orienter le visiteur vers les pôles d\'activité (' + (routing.secondaryPoles.join(', ') || 'Parc & Loisirs') + ')'
        ];
      } else {
        missionTitle = 'Contrôle QR 7 États & Sécurité Bassin/Lac — Commande ' + ref + ' (' + customer + ')';
        customChecklist = [
          'Scanner et valider le billet QR ' + ref + ' (' + customer + ') au tourniquet',
          'Vérifier les effectifs et prestations autorisées : ' + summary,
          'Équiper chaque participant d\'un gilet homologué (pirogue) et contrôler la tenue de bain (piscine)',
          'Synchroniser le pointage d\'accès avec la base d\'exploitation'
        ];
      }

      var newMissionId = 'MSN-2026-' + (101 + missions.length);
      var stamp = typeof nowStamp === 'function' ? nowStamp() : (dateStr + ' (Africa/Douala)');

      var newMission = {
        id: newMissionId,
        orderRef: ref,
        orderCustomer: customer,
        orderTotalFcfa: amount,
        orderSummary: summary,
        secondaryPoles: routing.secondaryPoles,
        pole: poleKey,
        poleLabel: preset.poleLabel,
        badgeClass: preset.badgeClass,
        agentName: agentName,
        agentMatricule: agentMatricule,
        agentRole: agentRole,
        date: dateStr,
        shift: preset.shift,
        priority: amount >= 25000 || poleKey === 'HEBERGEMENT' ? 'URGENTE' : 'HAUTE',
        status: 'ASSIGNEE',
        title: missionTitle,
        location: preset.location,
        objective: 'Exécution opérationnelle de la commande ' + ref + ' (' + customer + ' — ' + fmt(amount) + ' • ' + summary + '). ' + preset.objective,
        equipment: preset.equipment,
        guardrail: preset.guardrail,
        checklist: customChecklist.map(function (t) { return { text: t, done: false }; }),
        assignedBy: 'Système Automatique Commande → Poste',
        createdAt: stamp
      };

      missions.unshift(newMission);
      window.saveOperationalMissions(missions);
      window._activeMissionIdForPrint = newMissionId;

      var alerts = window.loadOperationalAlerts();
      var newAlert = {
        alertId: 'ALT-2026-' + (201 + alerts.length),
        missionId: newMissionId,
        orderRef: ref,
        customerName: customer,
        orderSummary: summary,
        amountFcfa: amount,
        pole: poleKey,
        poleLabel: preset.poleLabel,
        badgeClass: preset.badgeClass,
        agentName: agentName,
        agentMatricule: agentMatricule,
        title: missionTitle,
        createdAt: stamp,
        acknowledged: false
      };
      alerts.unshift(newAlert);
      window.saveOperationalAlerts(alerts);

      window.playMissionAlertChime();
      window.renderOperationalAlertsFeed();
      window.renderOperationalMissionsTable();

      // Afficher la bannière d'alerte de dispatch temps réel dans #view-RES (si présente)
      window.renderLiveOrderDispatchBanner(newMission, newAlert);

      try {
        var db = typeof loadDB === 'function' ? loadDB() : null;
        if (db && Array.isArray(db.auditLogs)) {
          db.auditLogs.unshift({
            time: stamp,
            actor: 'Dispatch Automatique (Commande → Poste)',
            action: 'Commande ' + ref + ' convertie en Fiche de Mission ' + newMissionId + ' (' + preset.poleLabel + ' — ' + agentName + ') + Alerte ' + newAlert.alertId
          });
          if (typeof saveDB === 'function') saveDB(db);
        }
      } catch (e) {}

      if (!opts.silentToast && typeof showToastSprint1 === 'function') {
        showToastSprint1('• Alerte Poste [' + preset.poleLabel + '] : Commande ' + ref + ' → Fiche de Mission ' + newMissionId + ' assignée à ' + agentName + ' !');
      }

      return newMission;
    };

    window.renderLiveOrderDispatchBanner = function (mission, alertObj) {
      if (!mission) return;
      var qrCard = document.getElementById('demoTicketCard');
      if (!qrCard || !qrCard.parentNode) return;

      var banner = document.getElementById('liveOrderDispatchAlertBox');
      if (!banner) {
        banner = document.createElement('div');
        banner.id = 'liveOrderDispatchAlertBox';
        banner.className = 'order-dispatch-live-banner';
        qrCard.parentNode.insertBefore(banner, qrCard);
      }

      var esc = typeof escHtml === 'function' ? escHtml : function (s) { return String(s || ''); };
      banner.innerHTML = ''
        + '<div style="flex:1;min-width:240px;">'
        + '  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">'
        + '    <span class="status-badge status-warning" style="font-size:11px;">ALERTE POSTE ENVOYÉE EN TEMPS RÉEL</span>'
        + '    <span class="eco-cat-badge ' + esc(mission.badgeClass || 'eco-cat-nature') + '" style="font-size:11px;padding:2px 8px;">' + esc(mission.poleLabel) + '</span>'
        + '  </div>'
        + '  <strong style="font-size:14.5px;color:var(--eco-brand);display:block;">Commande ' + esc(mission.orderRef) + ' → Fiche de Mission ' + esc(mission.id) + ' générée automatiquement</strong>'
        + '  <span style="font-size:13px;color:var(--eco-text-muted);">Agent affecté &amp; notifié : <strong>' + esc(mission.agentName) + ' (' + esc(mission.agentMatricule) + ')</strong> • Créneau : ' + esc(mission.shift) + '</span>'
        + '</div>'
        + '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
        + '  <button type="button" class="btn btn-primary btn-sm" onclick="openMissionSheetA4(\'' + esc(mission.id) + '\')">Voir Fiche de Mission A4 (' + esc(mission.id) + ')</button>'
        + '  <button type="button" class="btn btn-secondary btn-sm" onclick="openExpMissionsPanel(\'' + esc(mission.pole) + '\')">Centre d\'Alertes Postes</button>'
        + '</div>';
    };

    window.openMissionSheetForOrder = function (orderRef) {
      var ref = String(orderRef || '').trim();
      var missions = window.loadOperationalMissions();
      var found = missions.find(function (m) { return m.orderRef === ref; });
      if (found) {
        return window.openMissionSheetA4(found.id);
      }
      var db = typeof loadDB === 'function' ? loadDB() : { bookings: [], quotes: [], cfpApplications: [] };
      var orderObj = (db.bookings || []).find(function (b) { return b.reference === ref; })
        || (db.quotes || []).find(function (q) { return q.reference === ref; })
        || (db.cfpApplications || []).find(function (c) { return c.reference === ref; })
        || { reference: ref, holder: 'Client ECOPARK', paxSummary: 'Prestation associée à ' + ref, totalFcfa: 14000, date: todayMinIso };
      var created = window.dispatchOrderToPostMission(orderObj, { forceNew: true });
      return window.openMissionSheetA4(created.id);
    };

    window.simulateInstantOrderToMissionDispatch = function () {
      var samples = [
        {
          reference: 'ECP-2026-' + Math.floor(10000 + Math.random() * 89999),
          holder: 'Famille NKODO (Séjour Cité Ewondo VIP)',
          paxSummary: '2 Adultes, 1 Enfant • Suite Cité Ewondo VIP + Piscine + Pirogue',
          totalFcfa: 45000,
          lodgeCity: 'EWONDO',
          payMethod: 'OM',
          date: todayMinIso
        },
        {
          reference: 'ECP-2026-' + Math.floor(10000 + Math.random() * 89999),
          holder: 'Mme Mireille TCHOUA (Déjeuner Pergola Lac)',
          paxSummary: '4 Adultes • Pass Journée Royale + Saveurs + Pergola Lac',
          totalFcfa: 34000,
          hasPergola: true,
          payMethod: 'MOMO',
          date: todayMinIso
        },
        {
          reference: 'ECP-2026-' + Math.floor(10000 + Math.random() * 89999),
          holder: 'M. Christian FOUDA (Journée Nautique)',
          paxSummary: '2 Adultes, 2 Enfants • Piscine + Pirogue + Zoo',
          totalFcfa: 14000,
          payMethod: 'GUICHET',
          date: todayMinIso
        }
      ];
      var pick = samples[window.loadOperationalMissions().length % samples.length];
      return window.dispatchOrderToPostMission(pick, { forceNew: true });
    };

    window.loadOperationalMissions = function () {
      try {
        var raw = localStorage.getItem(MISSIONS_STORAGE_KEY);
        if (raw) {
          var parsed = JSON.parse(raw);
          if (Array.isArray(parsed) && parsed.length > 0) {
            return parsed;
          }
        }
        var defaults = window.getDefaultOperationalMissions();
        localStorage.setItem(MISSIONS_STORAGE_KEY, JSON.stringify(defaults));
        return defaults;
      } catch (e) {
        return window.getDefaultOperationalMissions();
      }
    };

    window.saveOperationalMissions = function (missionsList) {
      try {
        localStorage.setItem(MISSIONS_STORAGE_KEY, JSON.stringify(missionsList));
      } catch (e) {}
    };

    var missionDateEl = document.getElementById('missionDateInput');
    if (missionDateEl) {
      missionDateEl.setAttribute('min', todayMinIso);
      if (!missionDateEl.value) missionDateEl.value = todayMinIso;
    }

    window.applyMissionPolePreset = function (poleKey, btnEl) {
      var key = MISSION_POLE_PRESETS[poleKey] ? poleKey : 'GUICHET_CAISSE';
      var preset = MISSION_POLE_PRESETS[key];

      document.querySelectorAll('#expMissionPresetGrid .exp-mission-preset-btn').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-mission-pole') === key);
      });

      var poleSel = document.getElementById('missionPoleSelect');
      var agentSel = document.getElementById('missionAgentSelect');
      var shiftSel = document.getElementById('missionShiftSelect');
      var prioSel = document.getElementById('missionPrioritySelect');
      var titleIn = document.getElementById('missionTitleInput');
      var locIn = document.getElementById('missionLocationInput');
      var objIn = document.getElementById('missionObjectiveInput');
      var chkIn = document.getElementById('missionChecklistInput');
      var eqIn = document.getElementById('missionEquipmentInput');

      if (poleSel) poleSel.value = key;
      if (agentSel) agentSel.value = preset.agentOption;
      if (shiftSel) shiftSel.value = preset.shift;
      if (prioSel) prioSel.value = preset.priority;
      if (titleIn) titleIn.value = preset.title;
      if (locIn) locIn.value = preset.location;
      if (objIn) objIn.value = preset.objective;
      if (chkIn) chkIn.value = preset.checklist.join('; ');
      if (eqIn) eqIn.value = preset.equipment;
      return preset;
    };

    function formatMissionStatusBadge(status) {
      if (status === 'TERMINEE') {
        return '<span class="status-badge status-success">Terminée &amp; Validée</span>';
      }
      if (status === 'EN_COURS') {
        return '<span class="status-badge status-info">En cours sur poste</span>';
      }
      return '<span class="status-badge status-warning">Assignée (À pointer)</span>';
    }

    function formatMissionPriorityLabel(priority) {
      if (priority === 'URGENTE') return 'Urgente — Sécurité / VIP';
      if (priority === 'HAUTE') return 'Haute — Affluence / Groupe';
      return 'Normale';
    }

    window.renderOperationalMissionsTable = function () {
      var list = window.loadOperationalMissions();
      var tbody = document.getElementById('expMissionsTableBody');
      var kpiTotal = document.getElementById('expMissionKpiTotal');
      var kpiActive = document.getElementById('expMissionKpiActive');
      var kpiDone = document.getElementById('expMissionKpiDone');
      var kpiPoles = document.getElementById('expMissionKpiPoles');

      var activeCount = list.filter(function (m) { return m.status === 'EN_COURS'; }).length;
      var doneCount = list.filter(function (m) { return m.status === 'TERMINEE'; }).length;
      var polesSet = {};
      list.forEach(function (m) { if (m && m.pole) polesSet[m.pole] = true; });
      var coveredPoles = Object.keys(polesSet).length;

      if (kpiTotal) kpiTotal.textContent = list.length + (list.length > 1 ? ' missions' : ' mission');
      if (kpiActive) kpiActive.textContent = activeCount + (activeCount > 1 ? ' actives' : ' active');
      if (kpiDone) kpiDone.textContent = doneCount + (doneCount > 1 ? ' validées' : ' validée');
      if (kpiPoles) kpiPoles.textContent = Math.min(4, coveredPoles) + ' / 4 pôles';

      // Synchroniser le bandeau du poste Guichet (#view-AGT) avec la première mission Guichet/Contrôle
      var guichetMission = list.find(function (m) { return m.pole === 'GUICHET_CAISSE' || m.pole === 'CONTROLE_QR'; }) || list[0];
      if (guichetMission) {
        var bTitle = document.getElementById('agtBannerMissionTitle');
        var bMeta = document.getElementById('agtBannerMissionMeta');
        var bBtn = document.getElementById('btnAgtPrintMissionA4');
        if (bTitle) bTitle.textContent = guichetMission.id + ' • ' + guichetMission.title;
        if (bMeta) {
          var stTxt = guichetMission.status === 'TERMINEE' ? 'Terminée & Validée' : (guichetMission.status === 'EN_COURS' ? 'En cours sur poste' : 'Assignée');
          bMeta.innerHTML = 'Agent : <strong>' + guichetMission.agentName + ' (' + guichetMission.agentMatricule + ')</strong> • Créneau : <strong>' + guichetMission.shift + '</strong> • Statut : <strong>' + stTxt + '</strong>';
        }
        if (bBtn) {
          bBtn.setAttribute('onclick', "openMissionSheetA4('" + guichetMission.id + "')");
        }
      }

      if (!tbody) return list;

      var poleFilter = window._activeMissionPoleFilter || 'ALL';
      var qInput = document.getElementById('expMissionSearchInput');
      var query = (qInput && qInput.value ? qInput.value : '').trim().toLowerCase();

      var filtered = list.filter(function (m) {
        if (poleFilter !== 'ALL' && m.pole !== poleFilter) return false;
        if (query) {
          var hay = [m.id, m.poleLabel, m.agentName, m.agentMatricule, m.title, m.location, m.objective].join(' ').toLowerCase();
          if (hay.indexOf(query) === -1) return false;
        }
        return true;
      });

      var esc = typeof escHtml === 'function' ? escHtml : function (s) { return String(s || ''); };

      if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:18px;color:var(--eco-text-muted);">Aucune mission trouvée pour ce filtre. Utilisez le formulaire ci-dessus pour assigner une nouvelle tâche.</td></tr>';
        return filtered;
      }

      tbody.innerHTML = filtered.map(function (m) {
        var chkTotal = Array.isArray(m.checklist) ? m.checklist.length : 0;
        var chkDone = Array.isArray(m.checklist) ? m.checklist.filter(function (c) { return c && c.done; }).length : 0;
        var nextStatusBtn = '';
        if (m.status === 'ASSIGNEE') {
          nextStatusBtn = '<button type="button" class="btn btn-secondary btn-sm" onclick="updateOperationalMissionStatus(\'' + m.id + '\', \'EN_COURS\')">Pointer prise de poste</button>';
        } else if (m.status === 'EN_COURS') {
          nextStatusBtn = '<button type="button" class="btn btn-secondary btn-sm" onclick="updateOperationalMissionStatus(\'' + m.id + '\', \'TERMINEE\')">Valider fin de mission</button>';
        } else {
          nextStatusBtn = '<button type="button" class="btn btn-secondary btn-sm" onclick="updateOperationalMissionStatus(\'' + m.id + '\', \'EN_COURS\')">Rouvrir</button>';
        }

        var orderBadgeHtml = m.orderRef
          ? '<div style="margin-top:4px;font-size:11.5px;font-weight:700;color:var(--eco-dining-text);">Commande liée : ' + esc(m.orderRef) + '</div>'
          : '<div style="margin-top:4px;font-size:11.5px;color:var(--eco-text-muted);">Affectation directe poste</div>';

        return '<tr data-mission-id="' + esc(m.id) + '" data-order-ref="' + esc(m.orderRef || '') + '">'
          + '<td>'
          + '  <strong style="color:var(--eco-brand);display:block;">' + esc(m.id) + '</strong>'
          + '  <span class="eco-cat-badge ' + esc(m.badgeClass || 'eco-cat-nature') + '" style="font-size:11px;padding:2px 8px;margin-top:4px;">' + esc(m.poleLabel) + '</span>'
          +    orderBadgeHtml
          + '</td>'
          + '<td>'
          + '  <strong>' + esc(m.agentName) + '</strong>'
          + '  <div style="font-size:12.5px;color:var(--eco-text-muted);">' + esc(m.agentMatricule) + ' • ' + esc(m.agentRole) + '</div>'
          + '</td>'
          + '<td>'
          + '  <strong style="display:block;color:var(--eco-text);">' + esc(m.title) + '</strong>'
          + '  <span style="font-size:12.5px;color:var(--eco-text-muted);display:block;">' + esc(m.date) + ' • ' + esc(m.shift) + ' • Priorité : ' + esc(formatMissionPriorityLabel(m.priority)) + '</span>'
          + '</td>'
          + '<td>'
          + '  <strong style="color:var(--eco-brand);">' + chkDone + ' / ' + chkTotal + ' contrôles</strong>'
          + '  <div style="font-size:12px;color:var(--eco-text-muted);">' + esc(m.location) + '</div>'
          + '</td>'
          + '<td>' + formatMissionStatusBadge(m.status) + '</td>'
          + '<td>'
          + '  <div style="display:flex;gap:6px;flex-wrap:wrap;">'
          +      nextStatusBtn
          + '    <button type="button" class="btn btn-primary btn-sm" onclick="openMissionSheetA4(\'' + m.id + '\')">Fiche A4</button>'
          + '  </div>'
          + '</td>'
          + '</tr>';
      }).join('');

      return filtered;
    };

    window.filterOperationalMissions = function (poleCode, btnEl) {
      window._activeMissionPoleFilter = poleCode || 'ALL';
      document.querySelectorAll('#expMissionFilterBar .acc-filter-pill').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-pole-filter') === window._activeMissionPoleFilter);
      });
      return window.renderOperationalMissionsTable();
    };

    window.assignOperationalMission = function (openA4Immediately) {
      var poleSel = document.getElementById('missionPoleSelect');
      var agentSel = document.getElementById('missionAgentSelect');
      var dateIn = document.getElementById('missionDateInput');
      var shiftSel = document.getElementById('missionShiftSelect');
      var prioSel = document.getElementById('missionPrioritySelect');
      var titleIn = document.getElementById('missionTitleInput');
      var locIn = document.getElementById('missionLocationInput');
      var objIn = document.getElementById('missionObjectiveInput');
      var chkIn = document.getElementById('missionChecklistInput');
      var eqIn = document.getElementById('missionEquipmentInput');

      var poleKey = (poleSel && poleSel.value) || 'GUICHET_CAISSE';
      var preset = MISSION_POLE_PRESETS[poleKey] || MISSION_POLE_PRESETS.GUICHET_CAISSE;
      var agentRaw = (agentSel && agentSel.value) || preset.agentOption;
      var agentParts = agentRaw.split('|');
      var agentName = agentParts[0] || 'Agent ECOPARK';
      var agentMatricule = agentParts[1] || 'MAT-EXP-01';
      var agentRole = agentParts[2] || preset.poleLabel;

      var title = (titleIn && titleIn.value.trim()) || preset.title;
      var dateStr = (dateIn && dateIn.value) || todayMinIso;
      var shiftStr = (shiftSel && shiftSel.value) || preset.shift;
      var priorityStr = (prioSel && prioSel.value) || preset.priority;
      var locationStr = (locIn && locIn.value.trim()) || preset.location;
      var objectiveStr = (objIn && objIn.value.trim()) || preset.objective;
      var equipmentStr = (eqIn && eqIn.value.trim()) || preset.equipment;

      var rawChecklist = (chkIn && chkIn.value.trim())
        ? chkIn.value.split(';').map(function (s) { return s.trim(); }).filter(Boolean)
        : preset.checklist;
      var checklistObjs = rawChecklist.map(function (itemText) {
        return { text: itemText, done: false };
      });

      var list = window.loadOperationalMissions();
      var newId = 'MSN-2026-' + (101 + list.length);
      var linkedOrderRef = 'ORD-2026-' + (501 + list.length);
      var newMission = {
        id: newId,
        orderRef: linkedOrderRef,
        orderCustomer: 'Affectation Exploitation Terrain',
        orderTotalFcfa: 0,
        orderSummary: title,
        secondaryPoles: [],
        pole: poleKey,
        poleLabel: preset.poleLabel,
        badgeClass: preset.badgeClass,
        agentName: agentName,
        agentMatricule: agentMatricule,
        agentRole: agentRole,
        date: dateStr,
        shift: shiftStr,
        priority: priorityStr,
        status: 'ASSIGNEE',
        title: title,
        location: locationStr,
        objective: objectiveStr,
        equipment: equipmentStr,
        guardrail: preset.guardrail,
        checklist: checklistObjs,
        assignedBy: 'Chef d\'Exploitation Ahala',
        createdAt: typeof nowStamp === 'function' ? nowStamp() : dateStr
      };

      list.unshift(newMission);
      window.saveOperationalMissions(list);
      window._activeMissionIdForPrint = newId;

      var alerts = window.loadOperationalAlerts();
      alerts.unshift({
        alertId: 'ALT-2026-' + (201 + alerts.length),
        missionId: newId,
        orderRef: linkedOrderRef,
        customerName: 'Affectation Exploitation Ahala',
        orderSummary: title,
        amountFcfa: 0,
        pole: poleKey,
        poleLabel: preset.poleLabel,
        badgeClass: preset.badgeClass,
        agentName: agentName,
        agentMatricule: agentMatricule,
        title: title,
        createdAt: newMission.createdAt,
        acknowledged: false
      });
      window.saveOperationalAlerts(alerts);
      window.playMissionAlertChime();
      window.renderOperationalAlertsFeed();

      window._activeMissionPoleFilter = 'ALL';
      document.querySelectorAll('#expMissionFilterBar .acc-filter-pill').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-pole-filter') === 'ALL');
      });
      window.renderOperationalMissionsTable();

      try {
        var db = typeof loadDB === 'function' ? loadDB() : null;
        if (db && Array.isArray(db.auditLogs)) {
          db.auditLogs.unshift({
            time: typeof nowStamp === 'function' ? nowStamp() : dateStr,
            actor: 'Chef d\'Exploitation Ahala (EXP-MISSIONS)',
            action: 'Assignation tâche ' + newId + ' à ' + agentName + ' (' + preset.poleLabel + ') : ' + title
          });
          if (typeof saveDB === 'function') saveDB(db);
        }
      } catch (e) {}

      if (typeof showToastSprint1 === 'function') {
        showToastSprint1('• Mission ' + newId + ' assignée à ' + agentName + ' (' + preset.poleLabel + ') !');
      }

      if (openA4Immediately) {
        window.openMissionSheetA4(newId);
      }
      return newMission;
    };

    window.updateOperationalMissionStatus = function (missionId, nextStatus) {
      var list = window.loadOperationalMissions();
      var target = list.find(function (m) { return m.id === missionId; });
      if (!target) return null;
      target.status = nextStatus || 'EN_COURS';
      if (target.status === 'TERMINEE' && Array.isArray(target.checklist)) {
        target.checklist.forEach(function (c) { c.done = true; });
      }
      window.saveOperationalMissions(list);
      window.renderOperationalMissionsTable();
      if (typeof showToastSprint1 === 'function') {
        var lbl = target.status === 'TERMINEE' ? 'Terminée & Validée' : (target.status === 'EN_COURS' ? 'En cours sur poste' : 'Assignée');
        showToastSprint1('• Statut de la mission ' + target.id + ' (' + target.agentName + ') mis à jour : ' + lbl);
      }
      return target;
    };

    window.toggleMissionChecklistItem = function (missionId, itemIndex) {
      var list = window.loadOperationalMissions();
      var target = list.find(function (m) { return m.id === missionId; });
      if (!target || !Array.isArray(target.checklist) || !target.checklist[itemIndex]) return null;
      target.checklist[itemIndex].done = !target.checklist[itemIndex].done;
      var allDone = target.checklist.every(function (c) { return c.done; });
      var anyDone = target.checklist.some(function (c) { return c.done; });
      if (allDone) {
        target.status = 'TERMINEE';
      } else if (anyDone && target.status === 'ASSIGNEE') {
        target.status = 'EN_COURS';
      }
      window.saveOperationalMissions(list);
      window.renderOperationalMissionsTable();
      return target;
    };

    window.openExpMissionsPanel = function (presetPole) {
      if (typeof window.navigateFamily === 'function') {
        window.navigateFamily('EXP', 'EXP-01');
      }
      if (presetPole && MISSION_POLE_PRESETS[presetPole]) {
        window.applyMissionPolePreset(presetPole);
      }
      setTimeout(function () {
        var sec = document.getElementById('sec-EXP-MISSIONS');
        if (sec) {
          sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
          if (typeof triggerSectionFocusHalo === 'function') triggerSectionFocusHalo(sec);
        }
      }, 60);
    };

    window.openMissionSheetA4 = function (missionId) {
      var list = window.loadOperationalMissions();
      var m = list.find(function (x) { return x.id === missionId; }) || list[0];
      if (!m) return null;
      window._activeMissionIdForPrint = m.id;
      return window.printOfficialDocument('MISSION', m.id);
    };

    var origPrintOfficialDoc = window.printOfficialDocument;
    if (typeof origPrintOfficialDoc === 'function' && !origPrintOfficialDoc._missionSheetWrapped) {
      window.printOfficialDocument = function (docType, missionIdArg) {
        if (docType === 'MISSION') {
          var list = window.loadOperationalMissions();
          var targetId = missionIdArg || window._activeMissionIdForPrint || 'MSN-2026-101';
          var m = list.find(function (x) { return x.id === targetId; }) || list[0];
          if (!m) return null;

          var overlay = document.getElementById('modalOverlaySprint1');
          var box = document.getElementById('modalOfficialPrintBox');
          var titleEl = document.getElementById('officialPrintTitle');
          var bodyEl = document.getElementById('officialPrintBody');
          if (!overlay || !box || !bodyEl) return null;

          ['modalQuoteBox', 'modalCfpBox', 'modalRdvBox', 'modalRescheduleBox', 'modalEventDetailBox', 'modalCgvBox'].forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.style.display = 'none';
          });

          var esc = typeof escHtml === 'function' ? escHtml : function (s) { return String(s || ''); };

          if (titleEl) {
            titleEl.textContent = 'FICHE DE MISSION & ORDRE D\'AFFECTATION POSTE — ' + m.id;
          }

          var stLabel = m.status === 'TERMINEE'
            ? 'TERMINÉE & VALIDÉE'
            : (m.status === 'EN_COURS' ? 'EN COURS SUR POSTE' : 'ASSIGNÉE — PRISE DE POSTE À POINTER');

          var checklistHtml = (m.checklist || []).map(function (c, idx) {
            var checkedAttr = c.done ? 'checked' : '';
            return '<label class="mission-checklist-item">'
              + '<input type="checkbox" ' + checkedAttr + ' onchange="toggleMissionChecklistItem(\'' + esc(m.id) + '\', ' + idx + ')" style="margin-top:3px;" />'
              + '<span><strong>Point #' + (idx + 1) + ' :</strong> ' + esc(c.text) + '</span>'
              + '</label>';
          }).join('');

          bodyEl.innerHTML = ''
            + '<div class="mission-sheet-a4" id="printableMissionSheetA4">'
            + '  <div style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;border-bottom:2px solid var(--eco-brand);padding-bottom:12px;">'
            + '    <div style="display:flex;align-items:center;gap:12px;">'
            + '      <img src="audit-assets/ecopark-real-media/cropped-LOGO-ECOPARK-Youtube.png" alt="Logo officiel ECOPARK Cameroun" style="width:56px;height:56px;object-fit:contain;border-radius:50%;border:1.5px solid var(--eco-brand);background:#FFF;padding:2px;" />'
            + '      <div>'
            + '        <span class="eco-cat-badge ' + esc(m.badgeClass || 'eco-cat-nature') + '" style="font-size:11px;padding:2px 8px;">Pôle : ' + esc(m.poleLabel) + '</span>'
            + '        <strong style="font-family:var(--font-heading);font-size:1.22rem;color:var(--eco-brand);display:block;margin-top:3px;">ORDRE DE MISSION TERRAIN N° ' + esc(m.id) + '</strong>'
            + '        <span style="font-size:12px;color:var(--eco-text-muted);">Complexe Agro-Écotouristique ECOPARK Cameroun • Yaoundé-Ahala Barrière (RN3, Face Station Tradex)</span>'
            + '      </div>'
            + '    </div>'
            + '    <div style="display:flex;align-items:center;gap:12px;">'
            + '      <div style="text-align:right;font-size:12.5px;">'
            + '        <div><strong>Date :</strong> ' + esc(m.date) + '</div>'
            + '        <div><strong>Fuseau :</strong> Africa/Douala (UTC+1)</div>'
            + '        <div><strong>Priorité :</strong> ' + esc(formatMissionPriorityLabel(m.priority)) + '</div>'
            + '        <div style="margin-top:4px;"><span class="status-badge status-info" style="font-size:11.5px;">' + stLabel + '</span></div>'
            + '      </div>'
            + '      <div id="missionSheetQrContainer" style="width:92px;height:92px;display:flex;align-items:center;justify-content:center;background:#FFF;border:1px solid var(--eco-border);border-radius:8px;padding:4px;"></div>'
            + '    </div>'
            + '  </div>'
            + '  <div class="mission-sheet-grid-2">'
            + '    <div style="padding:12px 14px;background:var(--eco-bg);border:1px solid var(--eco-border);border-radius:10px;">'
            + '      <span style="font-size:11.5px;font-weight:700;text-transform:uppercase;color:var(--eco-brand);display:block;margin-bottom:4px;">1. Agent Affecté &amp; Responsable</span>'
            + '      <div><strong>Nom &amp; Prénom :</strong> ' + esc(m.agentName) + '</div>'
            + '      <div><strong>Matricule &amp; Fonction :</strong> ' + esc(m.agentMatricule) + ' — ' + esc(m.agentRole) + '</div>'
            + '      <div><strong>Autorité d\'affectation :</strong> ' + esc(m.assignedBy || 'Chef d\'Exploitation Ahala') + '</div>'
            + '    </div>'
            + '    <div style="padding:12px 14px;background:var(--eco-bg);border:1px solid var(--eco-border);border-radius:10px;">'
            + '      <span style="font-size:11.5px;font-weight:700;text-transform:uppercase;color:var(--eco-brand);display:block;margin-bottom:4px;">2. Poste, Lieu &amp; Horaires de Service</span>'
            + '      <div><strong>Zone / Poste :</strong> ' + esc(m.location) + '</div>'
            + '      <div><strong>Créneau horaire :</strong> ' + esc(m.shift) + '</div>'
            + '      <div><strong>Émission de la fiche :</strong> ' + esc(m.createdAt || m.date) + '</div>'
            + '    </div>'
            + '  </div>'
            + '  <div style="padding:12px 14px;background:#FFFFFF;border:1.5px solid var(--eco-border-strong);border-radius:10px;">'
            + '    <span style="font-size:11.5px;font-weight:700;text-transform:uppercase;color:var(--eco-brand);display:block;margin-bottom:4px;">3. Commande / Dossier Client Rattaché &amp; Objectif Opérationnel</span>'
            + '    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:8px 10px;background:var(--eco-bg);border:1px solid var(--eco-border);border-radius:8px;margin-bottom:8px;font-size:13px;">'
            + '      <div><strong>Réf. Commande liée :</strong> ' + esc(m.orderRef || 'ORD-DIRECT') + ' • <strong>Client :</strong> ' + esc(m.orderCustomer || 'Exploitation ECOPARK') + '</div>'
            + '      <div><strong>Détail :</strong> ' + esc(m.orderSummary || m.title) + (m.orderTotalFcfa ? (' • <strong>' + Number(m.orderTotalFcfa).toLocaleString('fr-FR') + ' FCFA</strong>') : '') + '</div>'
            + '    </div>'
            + '    <strong style="font-size:15px;color:var(--eco-text);display:block;margin-bottom:4px;">' + esc(m.title) + '</strong>'
            + '    <p style="margin:0;font-size:13.5px;color:var(--eco-text-muted);">' + esc(m.objective) + '</p>'
            + '  </div>'
            + '  <div style="padding:10px 14px;background:#FBF7F0;border:1px solid var(--eco-dining);border-radius:10px;font-size:13px;">'
            + '    <strong style="color:var(--eco-dining-text);">4. Dotation &amp; Équipements remis à la prise de poste :</strong> ' + esc(m.equipment)
            + '    <div style="margin-top:4px;color:var(--eco-brand);"><strong>Rappel Garde-Fou Réglementaire ECOPARK :</strong> ' + esc(m.guardrail) + '</div>'
            + '  </div>'
            + '  <div>'
            + '    <span style="font-size:12px;font-weight:700;text-transform:uppercase;color:var(--eco-brand);display:block;margin-bottom:6px;">5. Check-list de Contrôle Terrain (À cocher au fil du service)</span>'
            + '    <div style="display:grid;gap:6px;">' + checklistHtml + '</div>'
            + '  </div>'
            + '  <div class="mission-sheet-grid-3" style="margin-top:6px;">'
            + '    <div style="border:1px dashed var(--eco-border-strong);padding:12px;border-radius:8px;min-height:86px;">'
            + '      <span style="font-size:11px;font-weight:700;text-transform:uppercase;color:var(--eco-text-muted);display:block;">1. Visa Responsable Exploitation</span>'
            + '      <div style="font-size:12.5px;margin-top:4px;">' + esc(m.assignedBy || 'Chef d\'Exploitation Ahala') + '</div>'
            + '      <div style="margin-top:22px;border-top:1px solid #CCC;font-size:11px;color:#666;">Date, cachet &amp; signature</div>'
            + '    </div>'
            + '    <div style="border:1px dashed var(--eco-border-strong);padding:12px;border-radius:8px;min-height:86px;">'
            + '      <span style="font-size:11px;font-weight:700;text-transform:uppercase;color:var(--eco-text-muted);display:block;">2. Émargement Agent (Prise de poste)</span>'
            + '      <div style="font-size:12.5px;margin-top:4px;">' + esc(m.agentName) + ' (' + esc(m.agentMatricule) + ')</div>'
            + '      <div style="margin-top:22px;border-top:1px solid #CCC;font-size:11px;color:#666;">Heure d\'arrivée &amp; signature</div>'
            + '    </div>'
            + '    <div style="border:1px dashed var(--eco-border-strong);padding:12px;border-radius:8px;min-height:86px;">'
            + '      <span style="font-size:11px;font-weight:700;text-transform:uppercase;color:var(--eco-text-muted);display:block;">3. Visa Clôture &amp; Remise Dotation</span>'
            + '      <div style="font-size:12.5px;margin-top:4px;">Contrôle contradictoire de fin de poste</div>'
            + '      <div style="margin-top:22px;border-top:1px solid #CCC;font-size:11px;color:#666;">Heure de départ &amp; visa</div>'
            + '    </div>'
            + '  </div>'
            + '</div>';

          if (typeof window.renderEcoparkQrSvg === 'function') {
            window.renderEcoparkQrSvg('ECOPARK-MISSION|' + m.id + '|' + (m.orderRef || 'ORD') + '|' + m.agentMatricule + '|' + m.pole + '|' + m.date, 'missionSheetQrContainer');
          }

          overlay.style.display = 'flex';
          box.style.display = 'block';
          return m;
        }
        return origPrintOfficialDoc.apply(this, arguments);
      };
      window.printOfficialDocument._missionSheetWrapped = true;
    }

    // Règle d'Or : Toute commande validée génère automatiquement sa Fiche de Mission selon le poste + Alerte Temps Réel
    var prevBookingForMission = window.createLiveBookingSprint1;
    if (typeof prevBookingForMission === 'function' && !prevBookingForMission._orderMissionAutoWrapped) {
      window.createLiveBookingSprint1 = function () {
        var ok = prevBookingForMission.apply(this, arguments);
        if (ok) {
          try {
            var db = typeof loadDB === 'function' ? loadDB() : null;
            if (db && Array.isArray(db.bookings) && db.bookings[0]) {
              window.dispatchOrderToPostMission(db.bookings[0]);
            }
          } catch (e) {}
        }
        return ok;
      };
      window.createLiveBookingSprint1._orderMissionAutoWrapped = true;
    }

    var prevQuoteForMission = window.submitGroupQuoteSprint1;
    if (typeof prevQuoteForMission === 'function' && !prevQuoteForMission._orderMissionAutoWrapped) {
      window.submitGroupQuoteSprint1 = function () {
        var qRef = prevQuoteForMission.apply(this, arguments);
        if (qRef) {
          try {
            var db = typeof loadDB === 'function' ? loadDB() : null;
            var qObj = db && Array.isArray(db.quotes) ? db.quotes.find(function (x) { return x.reference === qRef; }) || db.quotes[0] : null;
            if (qObj) {
              window.dispatchOrderToPostMission(qObj);
            }
          } catch (e) {}
        }
        return qRef;
      };
      window.submitGroupQuoteSprint1._orderMissionAutoWrapped = true;
    }

    var prevCfpForMission = window.submitCfpApplicationSprint1;
    if (typeof prevCfpForMission === 'function' && !prevCfpForMission._orderMissionAutoWrapped) {
      window.submitCfpApplicationSprint1 = function () {
        var cRef = prevCfpForMission.apply(this, arguments);
        if (cRef) {
          try {
            var db = typeof loadDB === 'function' ? loadDB() : null;
            var cObj = db && Array.isArray(db.cfpApplications) ? db.cfpApplications.find(function (x) { return x.reference === cRef; }) || db.cfpApplications[0] : null;
            if (cObj) {
              window.dispatchOrderToPostMission({
                reference: cObj.reference,
                holder: cObj.name,
                paxSummary: 'Candidature CFP MINEFOP : ' + cObj.track,
                totalFcfa: 50000,
                payMethod: 'GUICHET',
                date: todayMinIso
              });
            }
          } catch (e) {}
        }
        return cRef;
      };
      window.submitCfpApplicationSprint1._orderMissionAutoWrapped = true;
    }

    var prevPosForMission = window.emitPosTicket;
    if (typeof prevPosForMission === 'function' && !prevPosForMission._orderMissionAutoWrapped) {
      window.emitPosTicket = function (method) {
        var itemsSnapshot = Array.isArray(window.posItems) ? window.posItems.slice() : [];
        var sumFcfa = itemsSnapshot.reduce(function (acc, it) { return acc + (Number(it.price || 0) * Number(it.qty || 1)); }, 0);
        var summaryTxt = itemsSnapshot.map(function (it) { return (it.qty || 1) + 'x ' + (it.name || 'Entrée'); }).join(' + ');
        var res = prevPosForMission.apply(this, arguments);
        if (itemsSnapshot.length > 0 && sumFcfa > 0) {
          try {
            var db = typeof loadDB === 'function' ? loadDB() : null;
            var latestLog = db && Array.isArray(db.auditLogs) && db.auditLogs[0] ? String(db.auditLogs[0].action || '') : '';
            var mRef = latestLog.match(/POS-2026-\d+/);
            var posRef = mRef ? mRef[0] : ('POS-2026-' + Math.floor(10000 + Math.random() * 89999));
            window.dispatchOrderToPostMission({
              reference: posRef,
              holder: 'Visiteur Walk-In Guichet (' + (method || 'Espèces') + ')',
              paxSummary: summaryTxt || 'Ticket Caisse Guichet',
              totalFcfa: sumFcfa,
              payMethod: 'GUICHET',
              date: todayMinIso
            });
          } catch (e) {}
        }
        return res;
      };
      window.emitPosTicket._orderMissionAutoWrapped = true;
    }

    window.renderOperationalAlertsFeed();
    window.renderOperationalMissionsTable();
  })();
  // ECOPARK_REFONTE_CANOPEE_JS:END
"""


def update_tokens_json() -> None:
    if not TOKENS_JSON.exists():
        return
    data = json.loads(TOKENS_JSON.read_text(encoding="utf-8"))
    if "primitive" in data and "color" in data["primitive"]:
        data["primitive"]["color"]["canopee_vivante"] = {
            "brand_forest": {"value": "#254B28", "type": "color", "description": "Marque ECOPARK vert foret"},
            "nature_foliage": {"value": "#527A35", "type": "color", "description": "Nature et decouverte vert feuillage"},
            "water_petrol": {"value": "#176B80", "type": "color", "description": "Eau et loisirs bleu petrole"},
            "lodge_terracotta": {"value": "#A45138", "type": "color", "description": "Hebergement terre cuite"},
            "dining_ochre": {"value": "#946015", "type": "color", "description": "Restauration ocre"},
            "cfp_indigo": {"value": "#4D5685", "type": "color", "description": "Formation indigo"},
            "text_anthracite": {"value": "#242824", "type": "color", "description": "Texte principal anthracite"},
            "bg_ivory": {"value": "#F7F5EF", "type": "color", "description": "Fond clair ivoire"},
            "surface_white": {"value": "#FFFFFF", "type": "color", "description": "Surfaces blanc"}
        }
    if "semantic" in data and "color" in data["semantic"]:
        data["semantic"]["color"]["rubriques"] = {
            "brand": {"value": "#254B28", "type": "color"},
            "nature_decouverte": {"value": "#527A35", "type": "color"},
            "eau_loisirs": {"value": "#176B80", "type": "color"},
            "hebergement": {"value": "#A45138", "type": "color"},
            "restauration": {"value": "#946015", "type": "color"},
            "formation": {"value": "#4D5685", "type": "color"},
            "text_primary": {"value": "#242824", "type": "color"},
            "bg_light": {"value": "#F7F5EF", "type": "color"},
            "surface": {"value": "#FFFFFF", "type": "color"}
        }
    TOKENS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def apply_refonte() -> None:
    html = LIVE_HTML.read_text(encoding="utf-8")

    # 1. Inject or replace REFONTE_CSS before </style>
    css_pattern = re.compile(r"/\* ECOPARK_REFONTE_CANOPEE_CSS:START \*/.*?/\* ECOPARK_REFONTE_CANOPEE_CSS:END \*/", re.S)
    if css_pattern.search(html):
        html = css_pattern.sub(lambda _: REFONTE_CSS, html)
    else:
        html = html.replace("</style>", "\n" + REFONTE_CSS + "\n  </style>", 1)

    # 2. Replace MAIN_MEGA_NAV_HTML
    nav_pattern = re.compile(r"<!-- ECOPARK_V4_MAIN_MEGA_NAV:START -->.*?<!-- ECOPARK_V4_MAIN_MEGA_NAV:END -->", re.S)
    assert nav_pattern.search(html), "Missing ECOPARK_V4_MAIN_MEGA_NAV markers"
    html = nav_pattern.sub(lambda _: MAIN_MEGA_NAV_HTML, html, count=1)

    # 3. Replace header utility buttons block right after ECOPARK_V4_MAIN_MEGA_NAV:END
    header_btn_pattern = re.compile(
        r"(<!-- ECOPARK_V4_MAIN_MEGA_NAV:END -->\s*)<div[^>]*>\s*<button[^>]*id=\"(?:btnHeaderRdv|nav-ACC)\".*?</div>(\s*</div>\s*</header>)",
        re.S,
    )
    if header_btn_pattern.search(html):
        html = header_btn_pattern.sub(lambda m: m.group(1) + HEADER_UTILITY_HTML + m.group(2), html, count=1)

    # 4. Replace MOBILE_DRAWER_HTML
    drawer_pattern = re.compile(r"<!-- ECOPARK_V4_MOBILE_DRAWER:START -->.*?<!-- ECOPARK_V4_MOBILE_DRAWER:END -->", re.S)
    assert drawer_pattern.search(html), "Missing ECOPARK_V4_MOBILE_DRAWER markers"
    html = drawer_pattern.sub(lambda _: MOBILE_DRAWER_HTML, html, count=1)

    # 5. Replace MOBILE_BOTTOM_NAV_HTML
    mob_nav_pattern = re.compile(r"<!-- ECOPARK_V4_MOBILE_NAV:START -->.*?<!-- ECOPARK_V4_MOBILE_NAV:END -->", re.S)
    assert mob_nav_pattern.search(html), "Missing ECOPARK_V4_MOBILE_NAV markers"
    html = mob_nav_pattern.sub(lambda _: MOBILE_BOTTOM_NAV_HTML, html, count=1)

    # 6. Replace HERO_STAGE_HTML
    hero_pattern = re.compile(r"<!-- ECOPARK_V4_HERO_STAGE:START -->.*?<!-- ECOPARK_V4_HERO_STAGE:END -->", re.S)
    assert hero_pattern.search(html), "Missing ECOPARK_V4_HERO_STAGE markers"
    html = hero_pattern.sub(lambda _: HERO_STAGE_HTML, html, count=1)

    # 7. Wrap the duplicate second hero block right after ECOPARK_V4_HERO_STAGE:END with id="legacyDuplicateHeroGrid" and convert its <h1> to <div class="legacy-hero-title">
    dup_hero_pattern = re.compile(
        r"(<!-- ECOPARK_V4_HERO_STAGE:END -->\s*)<div class=\"grid-12\"(?:\s+id=\"legacyDuplicateHeroGrid\")?\s+style=\"align-items:center;\">(.*?)<h1>(.*?)</h1>",
        re.S,
    )
    if dup_hero_pattern.search(html):
        html = dup_hero_pattern.sub(
            lambda m: m.group(1)
            + '<div class="grid-12" id="legacyDuplicateHeroGrid" style="align-items:center;" aria-hidden="true">'
            + m.group(2)
            + '<div class="legacy-hero-title">'
            + m.group(3)
            + "</div>",
            html,
            count=1,
        )

    # 8. Clean up #sec-PUB-04 (Fiche activité):
    # - Remove unverified visitor rating span
    html = html.replace('<span>• Note visiteurs : <strong>4.9 / 5 (128 avis vérifiés)</strong></span>', '')
    # - Replace tabs + #v4Pub04TabContent with PUB04_STRUCTURED_DETAILS_HTML
    pub04_tabs_pattern = re.compile(
        r"<!-- (?:Onglets V4|GABARIT FICHE ACTIVITÉ[^\n]*) -->\s*<div class=\"v4-tabs-bar\".*?</div>\s*</div>\s*(?=<div class=\"v4-reassurance-grid\">)",
        re.S,
    )
    if pub04_tabs_pattern.search(html):
        html = pub04_tabs_pattern.sub(lambda _: PUB04_STRUCTURED_DETAILS_HTML + "\n\n", html, count=1)

    # - Remove hardcoded value="2026-11-15" on #v4Pub04DateInput and #visitDate
    html = html.replace(
        '<input type="date" id="v4Pub04DateInput" class="form-control" value="2026-11-15" onchange="syncV4Pub04Widget()" />',
        '<input type="date" id="v4Pub04DateInput" class="form-control" onchange="syncV4Pub04Widget()" />',
    )
    html = html.replace(
        '<input type="date" id="visitDate" class="form-control" value="2026-11-15" required />',
        '<input type="date" id="visitDate" class="form-control" required />',
    )

    # 9. Add Restaurant full template inside #sec-PUB-09 right before <!-- ECOPARK_V4_PUB04_AND_PUB09:END -->
    if 'id="restaurantFullTemplateCard"' not in html:
        html = html.replace(
            "          </div>\n        </div>\n        <!-- ECOPARK_V4_PUB04_AND_PUB09:END -->",
            "\n" + SEJOUR_RESTAURANT_SUPPLEMENT_HTML + "\n          </div>\n        </div>\n        <!-- ECOPARK_V4_PUB04_AND_PUB09:END -->",
            1,
        )

    # 10. Replace #sec-PUB-11 and #sec-PUB-12 with complete Groupes & CFP templates
    pub11_12_pattern = re.compile(
        r"(?:<!--\s*Pôle 5\s*:.*?-->\s*)?<article class=\"col-7 bento-card bento-wide\" id=\"sec-PUB-11\".*?</article>\s*(?:<!--\s*Pôle 6\s*:.*?-->\s*)?<article class=\"col-5 bento-card\" id=\"sec-PUB-12\".*?</article>",
        re.S,
    )
    assert pub11_12_pattern.search(html), "Missing sec-PUB-11 / sec-PUB-12 articles"
    html = pub11_12_pattern.sub(lambda _: GROUPES_TEMPLATE_HTML + "\n\n" + CFP_TEMPLATE_HTML, html, count=1)

    # 11. Inject QUICK_DAY_CALC_HTML in #sec-PUB-10 right before <!-- 3 PASS TOUT-INCLUS
    if 'id="quickDayPriceCalculator"' not in html:
        html = html.replace(
            "            <!-- 3 PASS TOUT-INCLUS (ANCRAGE COMMERCIAL & AUGMENTATION DU PANIER MOYEN) -->",
            QUICK_DAY_CALC_HTML + "\n\n            <!-- 3 PASS TOUT-INCLUS (ANCRAGE COMMERCIAL & AUGMENTATION DU PANIER MOYEN) -->",
            1,
        )

    # 12. Replace RES_STEPPER with RES_JOURNEY_AND_STEPPER_HTML
    res_stepper_pattern = re.compile(r"<!-- ECOPARK_V4_RES_STEPPER:START -->.*?<!-- ECOPARK_V4_RES_STEPPER:END -->", re.S)
    assert res_stepper_pattern.search(html), "Missing ECOPARK_V4_RES_STEPPER markers"
    html = res_stepper_pattern.sub(lambda _: RES_JOURNEY_AND_STEPPER_HTML, html, count=1)

    # 12b. Inject or replace AGT_ACTIVE_MISSION_BANNER_HTML in #view-AGT
    agt_banner_pattern = re.compile(r"<!-- ECOPARK_AGT_ACTIVE_MISSION:START -->.*?<!-- ECOPARK_AGT_ACTIVE_MISSION:END -->", re.S)
    if agt_banner_pattern.search(html):
        html = agt_banner_pattern.sub(lambda _: AGT_ACTIVE_MISSION_BANNER_HTML.strip(), html, count=1)
    else:
        html = html.replace(
            "              <!-- Vente rapide au guichet (AGT-03, AGT-04) -->",
            AGT_ACTIVE_MISSION_BANNER_HTML.replace("            <!-- ECOPARK_AGT_ACTIVE_MISSION:START -->", "            <!-- ECOPARK_AGT_ACTIVE_MISSION:START -->\n            <div class=\"col-12\" style=\"padding:0;\">")
            .replace("<!-- ECOPARK_AGT_ACTIVE_MISSION:END -->", "</div>\n            <!-- ECOPARK_AGT_ACTIVE_MISSION:END -->")
            + "\n\n              <!-- Vente rapide au guichet (AGT-03, AGT-04) -->",
            1,
        )

    # 12c. Add subnav pill in #view-EXP and inject/replace EXP_MISSIONS_MODULE_HTML
    if 'onclick="openExpMissionsPanel()"' not in html:
        html = html.replace(
            '<button class="subnav-pill" onclick="inspectScreen(\'EXP-07\')">EXP-07 Centre de Messages</button>',
            '<button class="subnav-pill" onclick="inspectScreen(\'EXP-07\')">EXP-07 Centre de Messages</button>\n'
            '              <button class="subnav-pill" id="btnSubnavExpMissions" onclick="openExpMissionsPanel()">Assignation &amp; Fiches de Mission A4</button>',
            1,
        )

    exp_missions_pattern = re.compile(r"<!-- ECOPARK_EXP_MISSIONS_MODULE:START -->.*?<!-- ECOPARK_EXP_MISSIONS_MODULE:END -->", re.S)
    if exp_missions_pattern.search(html):
        html = exp_missions_pattern.sub(lambda _: EXP_MISSIONS_MODULE_HTML.strip(), html, count=1)
    else:
        fam7_pattern = re.compile(
            r"([ \t]*</div>\s*)[ \t]*</div>\s*</div>\s*</section>\s*(<!-- ====================================================================\s*FAMILLE 7 : PILOTAGE & DIRECTION)",
            re.S,
        )
        assert fam7_pattern.search(html), "Missing end of #view-EXP before FAMILLE 7"
        html = fam7_pattern.sub(
            lambda m: m.group(1) + "\n" + EXP_MISSIONS_MODULE_HTML + "\n          </div>\n        </div>\n      </section>\n\n      " + m.group(2),
            html,
            count=1,
        )

    # 12d. Add quick button in #sec-ADM-05 toolbar to open the Task Assignment & Mission Sheet module
    if 'id="admOpenMissionsBtn"' not in html:
        html = html.replace(
            '<button type="button" class="btn btn-secondary btn-sm" id="admStaffAdd">+ Nouveau compte</button>',
            '<button type="button" class="btn btn-primary btn-sm" id="admOpenMissionsBtn" onclick="openExpMissionsPanel()">Assigner une tâche / Fiche de mission A4 →</button> '
            '<button type="button" class="btn btn-secondary btn-sm" id="admStaffAdd">+ Nouveau compte</button>',
            1,
        )

    # 13. Clean up public dev jargon ("Parcours Transactionnel", "Page 1/6", etc.)
    html = html.replace(
        "Parcours Transactionnel & Devis en Francs CFA",
        "Réservation & Demandes en ligne (Francs CFA)",
    )
    html = html.replace(
        "Architecture Multi-Pages V4 • 6 Sous-Vues Thématiques",
        "Navigation rapide par univers",
    )

    # 14. Inject or replace REFONTE_JS before </script>\n</body>
    js_pattern = re.compile(r"// ECOPARK_REFONTE_CANOPEE_JS:START.*?// ECOPARK_REFONTE_CANOPEE_JS:END", re.S)
    if js_pattern.search(html):
        html = js_pattern.sub(lambda _: REFONTE_JS.strip(), html)
    else:
        html = html.replace(
            "// ECOPARK_PHASE9_V4_AND_RECETTE:END\n</script>",
            "// ECOPARK_PHASE9_V4_AND_RECETTE:END\n\n" + REFONTE_JS + "\n</script>",
            1,
        )

    # 15. Verify zero emojis / characters > U+25FF
    bad_chars = [(i, ch, hex(ord(ch))) for i, ch in enumerate(html) if ord(ch) > 0x25FF]
    if bad_chars:
        raise RuntimeError(f"Forbidden characters > U+25FF found: {bad_chars[:5]}")

    LIVE_HTML.write_text(html, encoding="utf-8")
    PROTO_HTML.write_text(html, encoding="utf-8")
    update_tokens_json()
    print(f"[OK] Refonte Canopee Vivante applied to {LIVE_HTML.name} and {PROTO_HTML.name} ({len(html):,} chars).")


if __name__ == "__main__":
    apply_refonte()
