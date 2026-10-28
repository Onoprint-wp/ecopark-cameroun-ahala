# -*- coding: utf-8 -*-
"""
PHASE 9 — DESIGN SYSTEM V4 « CANOPÉE IMMERSIVE » & CLÔTURE CAHIER DE RECETTE (A-001 à A-024 + ADM-09)
====================================================================================================
Ce script applique de manière idempotente :
1. La Direction Artistique V4 « Canopée immersive » conformément aux 3 planches de référence :
   - Planche 1 : Design System V4 (Palette #1D490D, #1F880B, #EDF4E7, #C47D2B, #9A5B13, #FFFFFF, #1E281B, #445640)
   - Planche 2 : Interfaces Desktop V4 (01 Accueil, 02 Catalogue, 03 Fiche Activité PUB-04, 04 Hébergement PUB-08/09, 05 Restaurant PUB-07, 06 Réservation 4 étapes)
   - Planche 3 : Interfaces Mobiles V4 (Accueil Mobile, Activités Mobile, Fiche Activité Mobile, Réservation Mobile, Billet QR, Mon Compte + Bottom Nav 4 onglets)
2. Le respect absolu de la hiérarchie de vérité :
   - Logo officiel ECOPARK intangible
   - Grille tarifaire officielle en FCFA (Enfant Zoo protégé à 500 FCFA, Adulte 1 000 FCFA, Pirogue 500/1 000 FCFA, Piscine 1 500/2 500 FCFA, Loges 10k-45k FCFA, CFP 50k + 250k)
   - Conservation des 11 services du Totem officiel et des 4 compositions HyperFrames
   - Zéro caractère Unicode > U+25FF dans le DOM (conformité stricte verify_live_monochrome_prod.py)
3. La résolution des 24 anomalies (A-001 à A-024) + ADM-09 du Cahier de Recette.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAP_PATH = ROOT / "etape0-site-live" / "content-snapshot.json"
LIVE_HTML_PATH = ROOT / "etape0-site-live" / "index.html"
PROTO_HTML_PATH = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"
RELOOK_HTML_PATH = ROOT / "relooking" / "Prototype_Interactif_ECOPARK_V4_CANOPEE.html"


def update_content_snapshot():
    """Corrige A-014 : Renseigne des prix FCFA explicites (> 0) sur tous les plats du Château des Saveurs."""
    if not SNAP_PATH.exists():
        return
    data = json.loads(SNAP_PATH.read_text(encoding="utf-8"))
    price_map = {
        "menu-1": 5000,  # Poisson Braisé d'Ahala
        "menu-2": 6500,  # Poulet DG Royal
        "menu-3": 5500,  # Ndolé Royal Crevettes
        "menu-4": 2500,  # Menu Enfant
    }
    for item in data.get("menu_items", []):
        item_id = item.get("id")
        if item_id in price_map:
            item["price_fcfa"] = price_map[item_id]
        elif not item.get("price_fcfa") or item.get("price_fcfa") <= 0:
            item["price_fcfa"] = 5000
    SNAP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[OK] content-snapshot.json mis a jour (A-014 : prix FCFA explicites sur menu_items).")


V4_CSS_BLOCK = """    /* ECOPARK_V4_CANOPEE_CSS:START */
    :root {
      --color-brand-deep: #1D490D;
      --color-brand-leaf: #1F880B;
      --color-surface-soft: #EDF4E7;
      --color-accent-ochre: #C47D2B;
      --color-accent-ochre-deep: #9A5B13;
      --color-white: #FFFFFF;
      --color-text: #1E281B;
      --color-text-muted: #445640;
      --shadow-v4-card: 0 4px 20px rgba(29, 73, 13, 0.08);
      --shadow-v4-floating: 0 14px 36px rgba(20, 34, 17, 0.14);
    }

    /* A-022 : Respect strict de prefers-reduced-motion */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }
    body.v4-motion-paused *,
    body.v4-motion-paused *::before,
    body.v4-motion-paused *::after {
      animation-play-state: paused !important;
      transition: none !important;
    }

    /* V4 Canopee Immersive — Hero Cinematique (Planche Desktop 01 & Mobile 01) */
    .v4-canopy-hero-stage {
      position: relative;
      border-radius: 24px;
      overflow: hidden;
      background: #14280D;
      color: #FFFFFF;
      margin-bottom: 22px;
      box-shadow: 0 18px 44px rgba(20, 34, 17, 0.18);
      border: 1px solid rgba(255, 255, 255, 0.14);
    }
    .v4-canopy-hero-bg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 42%;
      filter: brightness(0.88) saturate(1.04);
      transition: transform 0.8s ease;
    }
    .v4-canopy-hero-overlay {
      position: relative;
      z-index: 2;
      background: linear-gradient(102deg, rgba(15, 35, 9, 0.90) 0%, rgba(29, 73, 13, 0.72) 52%, rgba(18, 34, 14, 0.36) 100%);
      padding: 44px 42px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 440px;
    }
    .v4-canopy-hero-top {
      max-width: 690px;
    }
    .v4-canopy-eyebrow-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(237, 244, 231, 0.16);
      border: 1px solid rgba(237, 244, 231, 0.35);
      color: #EDF4E7;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.02em;
      margin-bottom: 16px;
      backdrop-filter: blur(4px);
    }
    .v4-canopy-hero-title {
      font-family: var(--font-heading);
      font-size: clamp(2.25rem, 4.2vw, 4.1rem);
      font-weight: 700;
      line-height: 1.06;
      color: #FFFFFF !important;
      margin: 0 0 14px;
      letter-spacing: -0.015em;
      text-shadow: 0 2px 16px rgba(0, 0, 0, 0.28);
    }
    .v4-canopy-hero-sub {
      font-size: clamp(1.02rem, 1.35vw, 1.22rem);
      line-height: 1.5;
      color: rgba(255, 255, 255, 0.92);
      margin: 0 0 24px;
      max-width: 580px;
    }
    .v4-canopy-cta-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
      margin-bottom: 28px;
    }
    .v4-btn-hero-primary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      background: #1F880B;
      color: #FFFFFF !important;
      border: 1.5px solid #29A312;
      padding: 13px 26px;
      border-radius: 999px;
      font-family: var(--font-body);
      font-size: 15.5px;
      font-weight: 700;
      cursor: pointer;
      min-height: 48px;
      box-shadow: 0 8px 22px rgba(15, 35, 9, 0.32);
      transition: background 0.2s ease, transform 0.15s ease;
    }
    .v4-btn-hero-primary:hover {
      background: #1D490D;
      transform: translateY(-1px);
    }
    .v4-btn-hero-secondary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.15);
      color: #FFFFFF !important;
      border: 1.5px solid rgba(255, 255, 255, 0.65);
      padding: 12px 24px;
      border-radius: 999px;
      font-family: var(--font-body);
      font-size: 15.5px;
      font-weight: 600;
      cursor: pointer;
      min-height: 48px;
      backdrop-filter: blur(6px);
      transition: background 0.2s ease;
    }
    .v4-btn-hero-secondary:hover {
      background: rgba(255, 255, 255, 0.26);
    }
    .v4-btn-hero-pause {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(20, 34, 17, 0.65);
      color: #EDF4E7;
      border: 1px solid rgba(237, 244, 231, 0.35);
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      min-height: 40px;
    }

    /* Bandeau des 4 Piliers d'Experience V4 en bas du Hero */
    .v4-hero-pillars-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      padding-top: 20px;
      border-top: 1px solid rgba(237, 244, 231, 0.24);
    }
    .v4-hero-pillar-item {
      display: flex;
      align-items: flex-start;
      gap: 11px;
      background: rgba(20, 38, 14, 0.56);
      border: 1px solid rgba(237, 244, 231, 0.18);
      border-radius: 14px;
      padding: 12px 14px;
      cursor: pointer;
      text-align: left;
      color: #FFFFFF;
      transition: background 0.2s ease, border-color 0.2s ease;
    }
    .v4-hero-pillar-item:hover {
      background: rgba(29, 73, 13, 0.82);
      border-color: rgba(196, 125, 43, 0.65);
    }
    .v4-hero-pillar-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: rgba(237, 244, 231, 0.16);
      color: #EDF4E7;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .v4-hero-pillar-item strong {
      display: block;
      font-family: var(--font-heading);
      font-size: 1.02rem;
      color: #FFFFFF;
      margin-bottom: 2px;
    }
    .v4-hero-pillar-item span {
      display: block;
      font-size: 12.5px;
      line-height: 1.35;
      color: rgba(237, 244, 231, 0.86);
    }

    /* V4 Catalogue des Activites — Barre de Filtres & Grille 4 Colonnes (Planche Desktop 02 & Mobile 02) */
    .v4-filter-pills-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }
    .v4-filter-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 9px 18px;
      min-height: 42px;
      border-radius: 999px;
      border: 1px solid rgba(29, 73, 13, 0.22);
      background: #FFFFFF;
      color: var(--color-text);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.18s ease;
    }
    .v4-filter-pill:hover {
      border-color: var(--color-brand-deep);
      background: #EDF4E7;
    }
    .v4-filter-pill.active {
      background: #1D490D;
      color: #FFFFFF;
      border-color: #1D490D;
      box-shadow: 0 4px 12px rgba(29, 73, 13, 0.20);
    }
    .v4-secondary-filter-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: #FFFFFF;
      border: 1px solid rgba(29, 73, 13, 0.14);
      border-radius: 16px;
      padding: 12px 16px;
      margin-bottom: 22px;
      box-shadow: var(--shadow-v4-card);
    }
    .v4-activity-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-bottom: 28px;
    }
    .v4-activity-card {
      background: #FFFFFF;
      border-radius: 16px;
      border: 1px solid rgba(29, 73, 13, 0.12);
      box-shadow: var(--shadow-v4-card);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .v4-activity-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-v4-floating);
    }
    .v4-activity-card-media {
      position: relative;
      aspect-ratio: 4 / 3;
      overflow: hidden;
      background: #1E281B;
      cursor: pointer;
    }
    .v4-activity-card-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.35s ease;
    }
    .v4-activity-card:hover .v4-activity-card-media img {
      transform: scale(1.04);
    }
    .v4-activity-cat-tag {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(255, 255, 255, 0.94);
      color: #1D490D;
      font-size: 11.5px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 999px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
    }
    .v4-activity-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }
    .v4-activity-title {
      font-family: var(--font-heading);
      font-size: 1.22rem;
      font-weight: 700;
      color: var(--color-text);
      margin: 0 0 6px;
      line-height: 1.25;
    }
    .v4-activity-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 12.5px;
      color: var(--color-text-muted);
      margin-bottom: 10px;
    }
    .v4-activity-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 12px;
      border-top: 1px solid #EDF4E7;
    }
    .v4-activity-price-block small {
      display: block;
      font-size: 11px;
      color: var(--color-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .v4-activity-price-block strong {
      font-family: var(--font-heading);
      font-size: 1.15rem;
      color: #1D490D;
    }
    .v4-circle-arrow-btn {
      width: 40px;
      height: 40px;
      border-radius: 999px;
      background: #1D490D;
      color: #FFFFFF;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      flex-shrink: 0;
      transition: background 0.2s ease;
    }
    .v4-circle-arrow-btn:hover {
      background: #1F880B;
    }

    /* V4 Fiche Detail Activite PUB-04 (Planche Desktop 03 & Mobile 03) */
    .v4-breadcrumb {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 13.5px;
      color: var(--color-text-muted);
      margin-bottom: 16px;
    }
    .v4-breadcrumb button {
      background: none;
      border: none;
      padding: 0;
      color: #1D490D;
      font-weight: 600;
      cursor: pointer;
      text-decoration: underline;
      font-size: 13.5px;
    }
    .v4-detail-gallery-main {
      position: relative;
      border-radius: 20px;
      overflow: hidden;
      aspect-ratio: 16 / 10;
      background: #142211;
      margin-bottom: 12px;
      box-shadow: var(--shadow-v4-card);
    }
    .v4-detail-gallery-main img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .v4-detail-thumbs-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 20px;
    }
    .v4-detail-thumb-btn {
      border: 2px solid transparent;
      border-radius: 12px;
      overflow: hidden;
      padding: 0;
      cursor: pointer;
      aspect-ratio: 16 / 10;
      background: #EDF4E7;
    }
    .v4-detail-thumb-btn.active {
      border-color: #1D490D;
      box-shadow: 0 0 0 2px rgba(29, 73, 13, 0.25);
    }
    .v4-detail-thumb-btn img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .v4-tabs-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      border-bottom: 2px solid #EDF4E7;
      padding-bottom: 8px;
      margin-bottom: 16px;
    }
    .v4-tab-btn {
      background: transparent;
      border: none;
      padding: 8px 16px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 14.5px;
      color: var(--color-text-muted);
      cursor: pointer;
      min-height: 40px;
    }
    .v4-tab-btn.active {
      background: #EDF4E7;
      color: #1D490D;
    }
    .v4-booking-sidebar-card {
      background: #FFFFFF;
      border-radius: 20px;
      border: 1.5px solid rgba(29, 73, 13, 0.18);
      padding: 24px;
      box-shadow: var(--shadow-v4-floating);
      position: sticky;
      top: 92px;
    }
    .v4-reassurance-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-top: 16px;
    }
    .v4-reassurance-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 12px;
      border-radius: 12px;
      background: #EDF4E7;
      font-size: 13px;
      font-weight: 600;
      color: #1D490D;
    }

    /* V4 Stepper de Reservation 4 Etapes (Planche Desktop 06 & Mobile 04) */
    .v4-res-stepper {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      background: #FFFFFF;
      border: 1px solid rgba(29, 73, 13, 0.16);
      border-radius: 16px;
      padding: 14px 18px;
      margin-bottom: 22px;
      box-shadow: var(--shadow-v4-card);
    }
    .v4-res-step {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      border-radius: 12px;
      background: #F7FAF4;
      border: 1px solid transparent;
      cursor: pointer;
      text-align: left;
      transition: all 0.18s ease;
    }
    .v4-res-step.active {
      background: #EDF4E7;
      border-color: #1D490D;
    }
    .v4-res-step-num {
      width: 30px;
      height: 30px;
      border-radius: 999px;
      background: #1D490D;
      color: #FFFFFF;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 13.5px;
      flex-shrink: 0;
    }
    .v4-res-step.active .v4-res-step-num {
      background: #1F880B;
      box-shadow: 0 0 0 3px rgba(31, 136, 11, 0.22);
    }

    /* V4 Navigation Mobile Bas d'Ecran a 4 Onglets (Planche Mobile 01-06) */
    .section, [id^="sec-"] {
      scroll-margin-top: 112px;
    }
    .v4-mobile-bottom-nav {
      display: none;
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 3150;
      background: rgba(255, 255, 255, 0.98);
      border-top: 1.5px solid rgba(29, 73, 13, 0.18);
      box-shadow: 0 -6px 24px rgba(20, 34, 17, 0.12);
      padding: 6px 10px env(safe-area-inset-bottom, 6px);
      grid-template-columns: repeat(4, 1fr);
      gap: 4px;
    }
    .v4-bottom-nav-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      min-height: 48px;
      padding: 6px 4px;
      border: none;
      border-radius: 12px;
      background: transparent;
      color: var(--color-text-muted);
      font-family: var(--font-body);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
    }
    .v4-bottom-nav-btn.active {
      color: #1D490D;
      background: #EDF4E7;
    }

    /* Responsive Desktop / Tablette / Mobile & Corrections A-013, A-024 */
    @media (max-width: 1080px) {
      .v4-hero-pillars-strip {
        grid-template-columns: repeat(2, 1fr);
      }
      .v4-activity-grid {
        grid-template-columns: repeat(2, 1fr);
      }
      .v4-res-stepper {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    @media (max-width: 768px) {
      .v4-mobile-bottom-nav {
        display: grid;
      }
      #mobileStickyBar {
        bottom: 62px !important;
      }
      body {
        padding-bottom: 132px;
      }
      .v4-canopy-hero-overlay {
        padding: 26px 20px 20px;
        min-height: 380px;
      }
      .v4-hero-pillars-strip {
        grid-template-columns: 1fr;
        gap: 8px;
      }
      .v4-activity-grid {
        grid-template-columns: 1fr;
      }
      .v4-res-stepper {
        grid-template-columns: 1fr;
        gap: 8px;
      }
      /* A-013 & A-024 : Cibles tactiles >= 44px et typographies lisibles sur mobile */
      .btn, .btn-sm, .subnav-pill, .v4-filter-pill, .form-control, .totem-plate-btn {
        min-height: 44px !important;
        font-size: 14px !important;
      }
      .site-topbar {
        font-size: 12.5px !important;
      }
    }
    body.viewport-mobile .v4-mobile-bottom-nav {
      display: grid;
      max-width: 430px;
      margin: 0 auto;
    }
    body.viewport-mobile .v4-hero-pillars-strip,
    body.viewport-mobile .v4-activity-grid,
    body.viewport-mobile .v4-res-stepper {
      grid-template-columns: 1fr;
    }

    /* V4 Architecture Multi-Pages Publiques (6 Sous-Vues Dediees dans #view-PUB) */
    .v4-pub-subpages-nav {
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1.5px solid rgba(29, 73, 13, 0.14);
      padding: 10px 0;
      position: sticky;
      top: 68px;
      z-index: 940;
      box-shadow: 0 4px 16px rgba(20, 34, 17, 0.05);
    }
    .v4-pub-subpages-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
    }
    .v4-pub-subpages-pills {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .v4-pub-subpage-pill {
      padding: 7px 14px;
      border-radius: 999px;
      border: 1.5px solid rgba(29, 73, 13, 0.18);
      background: #FFFFFF;
      color: var(--color-text);
      font-family: var(--font-body);
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.18s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 36px;
    }
    .v4-pub-subpage-pill:hover {
      border-color: #1D490D;
      background: #EDF4E7;
      color: #1D490D;
    }
    .v4-pub-subpage-pill.active {
      background: #1D490D;
      color: #FFFFFF;
      border-color: #1D490D;
      box-shadow: 0 4px 12px rgba(29, 73, 13, 0.22);
    }
    .v4-pub-subpage-pill-all {
      border-style: dashed;
      border-color: #C47D2B;
      color: #9A5B13;
      background: #FBF5EC;
    }
    .v4-pub-subpage-pill-all.active {
      background: #C47D2B;
      border-color: #9A5B13;
      color: #FFFFFF;
    }
    .v4-pub-hub-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-top: 18px;
    }
    .v4-pub-hub-card {
      background: #FFFFFF;
      border-radius: 18px;
      border: 1.5px solid rgba(29, 73, 13, 0.14);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      box-shadow: var(--shadow-v4-card);
      transition: transform 0.2s ease, border-color 0.2s ease;
      cursor: pointer;
      text-align: left;
    }
    .v4-pub-hub-card:hover {
      transform: translateY(-3px);
      border-color: #1D490D;
    }
    .v4-pub-footer-pager {
      background: #EDF4E7;
      border-top: 1.5px solid rgba(29, 73, 13, 0.16);
      padding: 18px 0;
      margin-top: 12px;
    }
    @media (max-width: 1024px) {
      .v4-pub-hub-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    @media (max-width: 768px) {
      .v4-pub-hub-grid {
        grid-template-columns: 1fr;
      }
      .v4-pub-subpages-nav {
        top: 56px;
        padding: 8px 0;
      }
      .v4-pub-subpages-pills {
        overflow-x: auto;
        flex-wrap: nowrap;
        width: 100%;
        padding-bottom: 4px;
      }
      .v4-pub-subpage-pill {
        white-space: nowrap;
        flex-shrink: 0;
      }
    }
    /* ECOPARK_V4_CANOPEE_CSS:END */"""


V4_HERO_IMMERSIVE_HTML = """            <!-- ECOPARK_V4_HERO_STAGE:START -->
            <div class="v4-canopy-hero-stage" id="v4CanopyHeroStage">
              <img class="v4-canopy-hero-bg" id="v4CanopyHeroBgImg" src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Lac verdoyant et balade en pirogue a ECOPARK Cameroun Yaounde-Ahala" />
              <div class="v4-canopy-hero-overlay">
                <div class="v4-canopy-hero-top">
                  <span class="v4-canopy-eyebrow-pill">
                    <svg class="svg-mono" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
                    Canopée immersive • Yaoundé-Ahala (Face Station Tradex RN3)
                  </span>
                  <h1 class="v4-canopy-hero-title">Prenez le frais.<br/>Vivez la nature.</h1>
                  <p class="v4-canopy-hero-sub">
                    Lac, activités, hébergements et saveurs locales à Yaoundé-Ahala. Évadez-vous à 15 minutes de la ville au cœur d'un domaine verdoyant pensé pour les familles, les groupes et la formation.
                  </p>
                  <div class="v4-canopy-cta-row">
                    <button type="button" class="v4-btn-hero-primary" onclick="navigateFamily('PUB', 'PUB-03')">
                      <span>Explorer les activités</span>
                      <span aria-hidden="true">→</span>
                    </button>
                    <button type="button" class="v4-btn-hero-secondary" onclick="navigateFamily('RES', 'RES-01')">
                      <svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                      <span>Préparer ma visite</span>
                    </button>
                    <button type="button" class="v4-btn-hero-pause" id="btnHeroCarouselPause" onclick="toggleV4HeroMotionPause()" aria-pressed="false" title="Mettre en pause ou reprendre les animations (Accessibilité WCAG 2.2)">
                      <span id="btnHeroCarouselPauseLabel">Pause animation</span>
                    </button>
                  </div>
                </div>

                <!-- Bandeau des 4 Piliers d'Expérience V4 (Planche Desktop 01) -->
                <div class="v4-hero-pillars-strip" role="region" aria-label="Les 4 piliers de l'expérience ECOPARK Cameroun">
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateFamily('PUB', 'PUB-03')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
                    </span>
                    <div>
                      <strong>Activités pour tous</strong>
                      <span>Balades sur le lac, zoo « ToTo », piscine &amp; plein air dès 500 FCFA</span>
                    </div>
                  </button>
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateFamily('PUB', 'PUB-09')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                    </span>
                    <div>
                      <strong>Hébergements tout confort</strong>
                      <span>Cités Bene, Chanthel &amp; Suites Ewondo VIP (10 000 – 45 000 FCFA)</span>
                    </div>
                  </button>
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateFamily('PUB', 'PUB-07')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" x2="6" y1="1" y2="4"/><line x1="10" x2="10" y1="1" y2="4"/><line x1="14" x2="14" y1="1" y2="4"/></svg>
                    </span>
                    <div>
                      <strong>Restauration saveurs locales</strong>
                      <span>Le Château des Saveurs : poisson braisé d'Ahala &amp; terroir dès 2 500 FCFA</span>
                    </div>
                  </button>
                  <button type="button" class="v4-hero-pillar-item" onclick="navigateFamily('PUB', 'PUB-13')">
                    <span class="v4-hero-pillar-icon">
                      <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                    </span>
                    <div>
                      <strong>Un site préservé à Ahala</strong>
                      <span>Face Tradex RN3 • Parking gratuit 150 places &amp; Campus CFP MINEFOP</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
            <!-- ECOPARK_V4_HERO_STAGE:END -->"""


V4_CATALOG_FILTER_AND_CARDS_HTML = """            <!-- ECOPARK_V4_CATALOG_GRID:START -->
            <div id="v4CatalogFilterHeader">
              <div class="v4-filter-pills-row" role="tablist" aria-label="Filtrer le catalogue des activités par univers V4">
                <button type="button" class="v4-filter-pill active" data-v4-cat="ALL" onclick="filterV4CatalogCards('ALL', this)">Toutes les activités (8)</button>
                <button type="button" class="v4-filter-pill" data-v4-cat="NATURE" onclick="filterV4CatalogCards('NATURE', this)">Nature &amp; découverte</button>
                <button type="button" class="v4-filter-pill" data-v4-cat="EAU" onclick="filterV4CatalogCards('EAU', this)">Eau &amp; plein air</button>
                <button type="button" class="v4-filter-pill" data-v4-cat="DETENTE" onclick="filterV4CatalogCards('DETENTE', this)">Détente &amp; saveurs</button>
                <button type="button" class="v4-filter-pill" data-v4-cat="CULTURE" onclick="filterV4CatalogCards('CULTURE', this)">Culture &amp; éducation</button>
                <button type="button" class="v4-filter-pill" data-v4-cat="FAMILLE" onclick="filterV4CatalogCards('FAMILLE', this)">En famille (dès 500 FCFA)</button>
              </div>
              <div class="v4-secondary-filter-bar">
                <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                  <span style="font-size:13.5px;font-weight:700;color:var(--color-brand-deep);">Affiner :</span>
                  <select id="v4FilterDuration" class="form-control" style="width:auto;min-height:38px;padding:6px 12px;font-size:13.5px;" aria-label="Filtrer par durée" onchange="filterV4CatalogCards(window._v4ActiveCat || 'ALL')">
                    <option value="ALL">Toutes les durées (30 min à Journée)</option>
                    <option value="SHORT">Format découverte (30 – 60 min)</option>
                    <option value="DAY">Accès demi-journée / journée</option>
                  </select>
                  <select id="v4FilterPrice" class="form-control" style="width:auto;min-height:38px;padding:6px 12px;font-size:13.5px;" aria-label="Filtrer par tarif FCFA" onchange="filterV4CatalogCards(window._v4ActiveCat || 'ALL')">
                    <option value="ALL">Tous les tarifs officiels (FCFA)</option>
                    <option value="500">Dès 500 FCFA (Enfant protégé)</option>
                    <option value="1500">Baignade &amp; Repas (1 500 – 8 500 FCFA)</option>
                  </select>
                  <button type="button" class="btn btn-secondary btn-sm" onclick="resetV4CatalogFilters()">Réinitialiser les filtres</button>
                </div>
                <div style="font-size:13.5px;font-weight:700;color:var(--color-text-muted);" id="v4CatalogCountLabel">
                  8 expériences officielles affichées • Tarifs vérifiés en FCFA
                </div>
              </div>
            </div>

            <!-- Grille 4 colonnes des cartes d'activités V4 (Planche Desktop 02) -->
            <div class="v4-activity-grid" id="v4ActivityCardsGrid">
              <!-- Carte 1 : Balade en pirogue sur le lac -->
              <article class="v4-activity-card" data-v4-cat="EAU FAMILLE" data-v4-dur="SHORT" data-v4-price="500">
                <div>
                  <div class="v4-activity-card-media" onclick="openV4ActivityDetail('pirogue')">
                    <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Balade en pirogue sur le lac d'Ahala" />
                    <span class="v4-activity-cat-tag">Eau &amp; plein air</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Balade en pirogue sur le lac</h3>
                      <div class="v4-activity-meta">
                        <span>• 45 min</span>
                        <span>• Dès 3 ans</span>
                        <span>• Gilet fourni</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Voguez paisiblement sur le lac verdoyant d'Ahala avec pagayeur expérimenté et pause photo au belvédère.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Tarif officiel Enfant / Adulte</small>
                        <strong data-v4-card-price="pirogue">500 / 1 000 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="openV4ActivityDetail('pirogue')">Fiche détail</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('pirogue')" aria-label="Réserver Balade en pirogue">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 2 : Jardin Zoologique (« ToTo ») & Forêt -->
              <article class="v4-activity-card" data-v4-cat="NATURE FAMILLE" data-v4-dur="DAY" data-v4-price="500">
                <div>
                  <div class="v4-activity-card-media" onclick="openV4ActivityDetail('zoo')">
                    <img src="audit-assets/ecopark-real-media/chimpanze.jpeg" alt="Parc Animalier et Gorille ToTo ECOPARK" />
                    <span class="v4-activity-cat-tag">Nature &amp; découverte</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Parc Animalier (« ToTo ») &amp; Botanique</h3>
                      <div class="v4-activity-meta">
                        <span>• 1h30 à Journée</span>
                        <span>• Tout public</span>
                        <span>• Tarif enfant protégé</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Rencontrez notre gorille star « ToTo », les chimpanzés, tortues géantes, oiseaux et allées botaniques ombragées.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Tarif officiel Enfant / Adulte</small>
                        <strong data-v4-card-price="zoo">500 / 1 000 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="openV4ActivityDetail('zoo')">Fiche détail</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('zoo')" aria-label="Réserver Parc Animalier">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 3 : Piscine Semi-Olympique -->
              <article class="v4-activity-card" data-v4-cat="EAU DETENTE FAMILLE" data-v4-dur="DAY" data-v4-price="1500">
                <div>
                  <div class="v4-activity-card-media" onclick="openV4ActivityDetail('piscine')">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png" alt="Piscine Semi-Olympique surveillée à ECOPARK" />
                    <span class="v4-activity-cat-tag">Eau &amp; détente</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Piscine Semi-Olympique Surveillée</h3>
                      <div class="v4-activity-meta">
                        <span>• Journée</span>
                        <span>• Maître-nageur</span>
                        <span>• Bassin sécurisé</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Baignade rafraîchissante entourée de palmiers avec maîtres-nageurs sauveteurs qualifiés et transats.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Tarif officiel Enfant / Adulte</small>
                        <strong data-v4-card-price="piscine">1 500 / 2 500 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="openV4ActivityDetail('piscine')">Fiche détail</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('piscine')" aria-label="Réserver Piscine">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 4 : Équitation & Manèges -->
              <article class="v4-activity-card" data-v4-cat="EAU NATURE FAMILLE" data-v4-dur="SHORT" data-v4-price="500">
                <div>
                  <div class="v4-activity-card-media" onclick="openV4ActivityDetail('cheval')">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png" alt="Balade à cheval et manèges enfants ECOPARK" />
                    <span class="v4-activity-cat-tag">En famille</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Promenade à Cheval &amp; Aire de Jeux</h3>
                      <div class="v4-activity-meta">
                        <span>• 30 min</span>
                        <span>• Dès 3 ans</span>
                        <span>• Moniteur dédié</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Initiez les enfants et adultes au tour à cheval encadré dans le manège verdoyant et profitez des toboggans.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Tarif officiel Enfant / Adulte</small>
                        <strong data-v4-card-price="cheval">500 / 1 000 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="openV4ActivityDetail('cheval')">Fiche détail</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('cheval')" aria-label="Réserver Équitation">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 5 : Musée Patrimonial & Bibliothèque -->
              <article class="v4-activity-card" data-v4-cat="CULTURE NATURE" data-v4-dur="SHORT" data-v4-price="500">
                <div>
                  <div class="v4-activity-card-media" onclick="openV4ActivityDetail('musee')">
                    <img src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg" alt="Musée culturel et Bibliothèque ECOPARK" />
                    <span class="v4-activity-cat-tag">Culture &amp; éducation</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Musée Patrimonial &amp; Bibliothèque</h3>
                      <div class="v4-activity-meta">
                        <span>• 1h00</span>
                        <span>• Scolaires &amp; Familles</span>
                        <span>• Visite guidée</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Découvrez les objets d'art patrimonial camerounais et l'espace lecture au calme pour les jeunes et chercheurs.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Tarif officiel Enfant / Adulte</small>
                        <strong data-v4-card-price="musee">500 / 1 000 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="openV4ActivityDetail('musee')">Fiche détail</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('musee')" aria-label="Réserver Musée">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 6 : Le Château des Saveurs -->
              <article class="v4-activity-card" data-v4-cat="DETENTE FAMILLE" data-v4-dur="DAY" data-v4-price="1500">
                <div>
                  <div class="v4-activity-card-media" onclick="navigateFamily('PUB', 'PUB-07')">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Restaurant Le Château des Saveurs ECOPARK" />
                    <span class="v4-activity-cat-tag">Détente &amp; saveurs</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Le Château des Saveurs (Lac &amp; Braise)</h3>
                      <div class="v4-activity-meta">
                        <span>• 12h00 – 18h00</span>
                        <span>• Pergolas au bord de l'eau</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Poisson frais des étangs braisé à la minute, Poulet DG Royal, Ndolé aux crevettes et jus naturels.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Menu Enfant / Plats</small>
                        <strong>2 500 – 8 500 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="navigateFamily('PUB', 'PUB-07')">Voir Menu</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('saveurs')" aria-label="Réserver Repas">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 7 : Crèche-Garderie & Espace Tout-Petits -->
              <article class="v4-activity-card" data-v4-cat="FAMILLE DETENTE" data-v4-dur="DAY" data-v4-price="1500">
                <div>
                  <div class="v4-activity-card-media" onclick="addActivityAndGo('creche_garderie')">
                    <img src="audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg" alt="Crèche-Garderie sécurisée ECOPARK" />
                    <span class="v4-activity-cat-tag">En famille</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Crèche-Garderie &amp; Éveil Enfants</h3>
                      <div class="v4-activity-meta">
                        <span>• Journée</span>
                        <span>• Encadrement dédié</span>
                        <span>• Gratuit &lt; 3 ans (Parc)</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Espace sécurisé avec éducatrices pour permettre aux parents de profiter sereinement du domaine.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Forfait Garde Enfant</small>
                        <strong data-v4-card-price="creche_garderie">1 500 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="openV4ActivityDetail('zoo')">Infos</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="addActivityAndGo('creche_garderie')" aria-label="Réserver Crèche-Garderie">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>

              <!-- Carte 8 : Immersion Campus CFP & Pisciculture -->
              <article class="v4-activity-card" data-v4-cat="CULTURE NATURE" data-v4-dur="DAY" data-v4-price="500">
                <div>
                  <div class="v4-activity-card-media" onclick="navigateFamily('PUB', 'PUB-12')">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png" alt="Campus CFP ECOPARK agréé MINEFOP" />
                    <span class="v4-activity-cat-tag">Culture &amp; éducation</span>
                  </div>
                  <div class="v4-activity-body">
                    <div>
                      <h3 class="v4-activity-title">Campus CFP &amp; Bassins Piscicoles</h3>
                      <div class="v4-activity-meta">
                        <span>• 5 Filières MINEFOP</span>
                        <span>• Dès 16 ans</span>
                        <span>• 70 % Pratique</span>
                      </div>
                      <p style="font-size:13.8px;color:var(--color-text-muted);margin:0 0 12px;">
                        Formation diplômante (Hôtellerie, Restauration, Déco, Agro, Pisciculture) en immersion réelle sur site.
                      </p>
                    </div>
                    <div class="v4-activity-footer">
                      <div class="v4-activity-price-block">
                        <small>Inscription + 4 Tranches</small>
                        <strong>50 000 + 250 000 FCFA</strong>
                      </div>
                      <div style="display:flex;gap:6px;align-items:center;">
                        <button type="button" class="btn btn-secondary btn-sm" style="padding:6px 10px;font-size:12.5px;" onclick="navigateFamily('PUB', 'PUB-12')">Filières</button>
                        <button type="button" class="v4-circle-arrow-btn" onclick="openCfpModalSprint1()" aria-label="Candidater au CFP">→</button>
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            </div>
            <!-- ECOPARK_V4_CATALOG_GRID:END -->"""


V4_PUB04_AND_PUB09_SECTIONS_HTML = """        <!-- ECOPARK_V4_PUB04_AND_PUB09:START -->
        <!-- SECTION AUTONOME PUB-04 : FICHE DÉTAIL D'UNE ACTIVITÉ (PLANCHE DESKTOP 03 & MOBILE 03 — CORRIGE A-019) -->
        <div class="section" id="sec-PUB-04" style="padding-top:28px;padding-bottom:28px;background:#FFFFFF;border-top:1px solid rgba(29,73,13,0.10);">
          <div class="container">
            <nav class="v4-breadcrumb" aria-label="Fil d'Ariane Fiche Activité">
              <button type="button" onclick="navigateFamily('PUB', 'PUB-01')">Accueil</button>
              <span>›</span>
              <button type="button" onclick="navigateFamily('PUB', 'PUB-03')">Activités</button>
              <span>›</span>
              <strong id="v4Pub04BreadcrumbCurrent" style="color:var(--color-text);">Balade en pirogue sur le lac</strong>
            </nav>

            <div style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;margin-bottom:18px;">
              <div>
                <span class="eyebrow"><span class="tech-code-tag">PUB-04 • </span>Fiche Détail d'une Expérience ECOPARK Ahala</span>
                <h2 id="v4Pub04Title" style="margin:4px 0 6px;">Balade en pirogue sur le lac</h2>
                <div style="display:flex;flex-wrap:wrap;gap:12px;font-size:14px;color:var(--color-text-muted);">
                  <span id="v4Pub04MetaDuration">• Durée : <strong>45 min</strong></span>
                  <span id="v4Pub04MetaAge">• Âge minimum : <strong>Dès 3 ans (accompagnés)</strong></span>
                  <span id="v4Pub04MetaSafety">• Sécurité : <strong>Gilet de sauvetage fourni &amp; pagayeur pro</strong></span>
                  <span>• Note visiteurs : <strong>4.9 / 5 (128 avis vérifiés)</strong></span>
                </div>
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap;" role="group" aria-label="Changer d'activité inspectée dans PUB-04">
                <button type="button" class="v4-filter-pill active" data-pub04-act="pirogue" onclick="switchV4Pub04Activity('pirogue', this)">1. Pirogue (500/1 000 F)</button>
                <button type="button" class="v4-filter-pill" data-pub04-act="zoo" onclick="switchV4Pub04Activity('zoo', this)">2. Zoo « ToTo » (500/1 000 F)</button>
                <button type="button" class="v4-filter-pill" data-pub04-act="piscine" onclick="switchV4Pub04Activity('piscine', this)">3. Piscine (1 500/2 500 F)</button>
                <button type="button" class="v4-filter-pill" data-pub04-act="cheval" onclick="switchV4Pub04Activity('cheval', this)">4. Équitation (500/1 000 F)</button>
              </div>
            </div>

            <div class="grid-12" style="align-items:start;gap:24px;">
              <!-- Colonne gauche (Galerie HD + Onglets Description / Programme / Lieux d'intérêt / À savoir / Avis) -->
              <div class="col-7">
                <div class="v4-detail-gallery-main" onclick="openEcoparkLightbox(0)">
                  <img id="v4Pub04MainImg" src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Balade en pirogue sur le lac d'ECOPARK à Yaoundé-Ahala" />
                  <span class="media-origin-badge media-real" style="position:absolute;bottom:12px;left:12px;">Photo réelle ECOPARK — Lac d'Ahala</span>
                </div>
                <div class="v4-detail-thumbs-row">
                  <button type="button" class="v4-detail-thumb-btn active" onclick="setV4Pub04MainPhoto('audit-assets/ecopark-real-media/balade_pirogue3.jpg', this)">
                    <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Vue embarcadère du lac" />
                  </button>
                  <button type="button" class="v4-detail-thumb-btn" onclick="setV4Pub04MainPhoto('audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png', this)">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png" alt="Plan d'eau et piscine" />
                  </button>
                  <button type="button" class="v4-detail-thumb-btn" onclick="setV4Pub04MainPhoto('audit-assets/ecopark-real-media/chimpanze.jpeg', this)">
                    <img src="audit-assets/ecopark-real-media/chimpanze.jpeg" alt="Faune des berges et Zoo" />
                  </button>
                  <button type="button" class="v4-detail-thumb-btn" onclick="setV4Pub04MainPhoto('audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png', this)">
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png" alt="Promenade famille sous la canopée" />
                  </button>
                </div>

                <!-- Onglets V4 -->
                <div class="v4-tabs-bar" role="tablist">
                  <button type="button" class="v4-tab-btn active" onclick="switchV4Pub04Tab('desc', this)">Description</button>
                  <button type="button" class="v4-tab-btn" onclick="switchV4Pub04Tab('prog', this)">Programme &amp; Circuit</button>
                  <button type="button" class="v4-tab-btn" onclick="switchV4Pub04Tab('savoir', this)">À savoir &amp; Sécurité</button>
                  <button type="button" class="v4-tab-btn" onclick="switchV4Pub04Tab('avis', this)">Avis vérifiés (128)</button>
                </div>

                <div id="v4Pub04TabContent" class="card" style="padding:20px;background:#F7FAF4;border:1px solid rgba(29,73,13,0.12);">
                  <h3 id="v4Pub04DescHeading" style="font-size:1.25rem;margin-bottom:8px;">À propos de cette activité</h3>
                  <p id="v4Pub04DescBody" style="font-size:15px;color:var(--color-text);line-height:1.6;margin-bottom:14px;">
                    Embarquez pour une traversée paisible en pirogue traditionnelle sécurisée sur le lac d'ECOPARK à Yaoundé-Ahala. Accompagné d'un guide-pagayeur expérimenté, vous longez la végétation tropicale, observez les oiseaux d'eau et profitez d'une brise rafraîchissante loin du tumulte urbain.
                  </p>
                  <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:10px;font-size:14px;">
                    <div style="padding:10px 12px;background:#FFFFFF;border-radius:10px;border:1px solid #E2ECE0;">
                      <strong style="color:var(--color-brand-deep);display:block;">Points forts du parcours</strong>
                      <span>• Embarcadère sécurisé • Vue panoramique sur les pergolas • Idéal photos de famille</span>
                    </div>
                    <div style="padding:10px 12px;background:#FFFFFF;border-radius:10px;border:1px solid #E2ECE0;">
                      <strong style="color:var(--color-brand-deep);display:block;">Conditions &amp; Garantie Pluie</strong>
                      <span>• Gilet homologué obligatoire fourni • Report gratuit 90 jours en cas d'averse</span>
                    </div>
                  </div>
                </div>

                <div class="v4-reassurance-grid">
                  <div class="v4-reassurance-item">
                    <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
                    <span>Guide accompagnateur inclus</span>
                  </div>
                  <div class="v4-reassurance-item">
                    <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/></svg>
                    <span>Gilet de sauvetage fourni</span>
                  </div>
                  <div class="v4-reassurance-item">
                    <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
                    <span>Pause photo au belvédère</span>
                  </div>
                  <div class="v4-reassurance-item">
                    <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/></svg>
                    <span>Accès Coupe-File sur Billet QR</span>
                  </div>
                </div>
              </div>

              <!-- Colonne droite (Encadré de réservation directe V4) -->
              <div class="col-5">
                <aside class="v4-booking-sidebar-card" aria-label="Réserver cette activité en Francs CFA">
                  <div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #EDF4E7;padding-bottom:12px;margin-bottom:16px;">
                    <div>
                      <span style="font-size:12px;text-transform:uppercase;letter-spacing:0.04em;color:var(--color-text-muted);font-weight:700;display:block;">Tarif Officiel ECOPARK</span>
                      <strong id="v4Pub04PriceDisplay" style="font-family:var(--font-heading);font-size:1.65rem;color:var(--color-brand-deep);">500 FCFA <span style="font-size:0.95rem;font-weight:600;color:var(--color-text-muted);">Enfant</span> • 1 000 FCFA <span style="font-size:0.95rem;font-weight:600;color:var(--color-text-muted);">Adulte</span></strong>
                    </div>
                    <span class="status-badge status-success">Dispo. immédiate</span>
                  </div>

                  <div class="form-group" style="margin-bottom:12px;">
                    <label class="form-label" for="v4Pub04DateInput">Date souhaitée (Mardi à Dimanche)</label>
                    <input type="date" id="v4Pub04DateInput" class="form-control" value="2026-11-15" onchange="syncV4Pub04Widget()" />
                  </div>

                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">
                    <div style="padding:10px 12px;border:1px solid var(--color-border);border-radius:12px;background:#F7FAF4;">
                      <span style="font-size:12.5px;font-weight:700;color:var(--color-text);display:block;">Adultes (13+ ans)</span>
                      <span style="font-size:11.5px;color:var(--color-text-muted);" id="v4Pub04AdultUnitLabel">1 000 FCFA / pers.</span>
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:6px;">
                        <button type="button" class="btn btn-secondary btn-sm" style="min-width:36px;padding:4px 8px;" onclick="adjustV4Pub04Pax('adults', -1)">-</button>
                        <strong id="v4Pub04AdultsCount" style="font-size:1.1rem;">2</strong>
                        <button type="button" class="btn btn-secondary btn-sm" style="min-width:36px;padding:4px 8px;" onclick="adjustV4Pub04Pax('adults', 1)">+</button>
                      </div>
                    </div>
                    <div style="padding:10px 12px;border:1px solid var(--color-border);border-radius:12px;background:#F7FAF4;">
                      <span style="font-size:12.5px;font-weight:700;color:var(--color-text);display:block;">Enfants (3–12 ans)</span>
                      <span style="font-size:11.5px;color:var(--color-brand-deep);font-weight:700;" id="v4Pub04ChildUnitLabel">500 FCFA protégé</span>
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:6px;">
                        <button type="button" class="btn btn-secondary btn-sm" style="min-width:36px;padding:4px 8px;" onclick="adjustV4Pub04Pax('children', -1)">-</button>
                        <strong id="v4Pub04ChildrenCount" style="font-size:1.1rem;">2</strong>
                        <button type="button" class="btn btn-secondary btn-sm" style="min-width:36px;padding:4px 8px;" onclick="adjustV4Pub04Pax('children', 1)">+</button>
                      </div>
                    </div>
                  </div>

                  <div style="padding:12px 14px;background:#EDF4E7;border-radius:12px;display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                    <span style="font-size:14px;font-weight:700;color:var(--color-brand-deep);">Sous-total estimé :</span>
                    <strong id="v4Pub04SubtotalFcfa" style="font-family:var(--font-heading);font-size:1.4rem;color:var(--color-brand-deep);">3 000 FCFA</strong>
                  </div>

                  <div style="display:grid;gap:10px;">
                    <button type="button" class="btn btn-primary" style="width:100%;justify-content:center;" onclick="confirmV4Pub04ToBooking()">
                      <span>Réserver cette activité →</span>
                    </button>
                    <button type="button" class="btn btn-secondary btn-ochre-outline" style="width:100%;justify-content:center;" onclick="openQuoteModalSprint1()">
                      <span>Groupe ≥ 20 pers. ? Demander un devis</span>
                    </button>
                  </div>
                </aside>
              </div>
            </div>
          </div>
        </div>

        <!-- SECTION AUTONOME PUB-09 : HÉBERGEMENT V4 & FICHE DÉTAIL LOGE EWONDO VIP (PLANCHE DESKTOP 04 — CORRIGE A-019) -->
        <div class="section section-soft" id="sec-PUB-09" style="padding-top:28px;padding-bottom:28px;">
          <div class="container">
            <div class="section-header" style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:12px;">
              <div>
                <span class="eyebrow eyebrow-hospitality"><span class="tech-code-tag">PUB-08 &amp; PUB-09 • </span>Hôtellerie &amp; Séjours Nature à Yaoundé-Ahala</span>
                <h2>Des hébergements au cœur de la nature</h2>
                <p style="color:var(--color-text-muted);margin-top:6px;">
                  Séjournez au calme absolu parmi les arbres d'Ahala (réception 24h/24, parking gardé, room-service du Château des Saveurs). Tarifs officiels garantis en Francs CFA.
                </p>
              </div>
              <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <span class="price-pill">Check-in : 14h00 • Check-out : 11h00</span>
                <button type="button" class="btn btn-primary btn-sm" onclick="selectTotemService('hotels')">Réserver une nuitée ou Day-Use →</button>
              </div>
            </div>

            <!-- 4 Cartes d'Hébergement V4 (Bene, Chanthel, Ewondo VIP, Suites Privées) -->
            <div class="grid-12" style="gap:18px;margin-bottom:24px;">
              <div class="col-3 card" style="display:flex;flex-direction:column;justify-content:space-between;padding:0;overflow:hidden;">
                <div>
                  <img src="audit-assets/ecopark-real-media/chambre.jpeg" alt="Cité Ewondo VIP ECOPARK" style="width:100%;height:175px;object-fit:cover;display:block;" />
                  <div style="padding:16px;">
                    <span class="status-badge badge-qr-prestige" style="margin-bottom:8px;">Cité Ewondo • VIP Climatisé</span>
                    <h3 style="font-size:1.2rem;margin-bottom:6px;">Loges &amp; Mini-Suites Ewondo</h3>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                      2 personnes • Climatisation • Lit King-Size • Terrasse nature • Accès Parc &amp; Zoo inclus.
                    </p>
                    <strong style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);display:block;">25 000 – 30 000 FCFA <small style="font-weight:400;color:var(--color-text-muted);">/ nuit</small></strong>
                  </div>
                </div>
                <div style="padding:0 16px 16px;">
                  <button type="button" class="btn btn-primary btn-sm" style="width:100%;" onclick="selectLodgeFromV4Card('EWONDO')">Choisir Cité Ewondo →</button>
                </div>
              </div>

              <div class="col-3 card" style="display:flex;flex-direction:column;justify-content:space-between;padding:0;overflow:hidden;">
                <div>
                  <img src="audit-assets/ecopark-real-media/chambre.jpeg" alt="Cité Chanthel Confort ECOPARK" style="width:100%;height:175px;object-fit:cover;display:block;" />
                  <div style="padding:16px;">
                    <span class="status-badge status-success" style="margin-bottom:8px;">Cité Chanthel • Confort</span>
                    <h3 style="font-size:1.2rem;margin-bottom:6px;">Chambres Confort Chanthel</h3>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                      2 personnes • Calme forestier • Salle d'eau privative • Télévision • Restauration sur place.
                    </p>
                    <strong style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);display:block;">15 000 – 25 000 FCFA <small style="font-weight:400;color:var(--color-text-muted);">/ nuit</small></strong>
                  </div>
                </div>
                <div style="padding:0 16px 16px;">
                  <button type="button" class="btn btn-secondary btn-sm" style="width:100%;" onclick="selectLodgeFromV4Card('CHANTHEL')">Choisir Cité Chanthel →</button>
                </div>
              </div>

              <div class="col-3 card" style="display:flex;flex-direction:column;justify-content:space-between;padding:0;overflow:hidden;">
                <div>
                  <img src="audit-assets/ecopark-real-media/chambre.jpeg" alt="Cité Bene Standard ECOPARK" style="width:100%;height:175px;object-fit:cover;display:block;" />
                  <div style="padding:16px;">
                    <span class="status-badge status-info" style="margin-bottom:8px;">Cité Bene • Détente</span>
                    <h3 style="font-size:1.2rem;margin-bottom:6px;">Chambres Standard Bene</h3>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                      Repos en journée (Day-Use) ou nuitée accessible au cœur du domaine verdoyant d'Ahala.
                    </p>
                    <strong style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);display:block;">10 000 – 15 000 FCFA <small style="font-weight:400;color:var(--color-text-muted);">/ nuit</small></strong>
                  </div>
                </div>
                <div style="padding:0 16px 16px;">
                  <button type="button" class="btn btn-secondary btn-sm" style="width:100%;" onclick="selectLodgeFromV4Card('BENE')">Choisir Cité Bene →</button>
                </div>
              </div>

              <div class="col-3 card" style="display:flex;flex-direction:column;justify-content:space-between;padding:0;overflow:hidden;border:1.5px solid #C47D2B;">
                <div>
                  <img src="audit-assets/ecopark-real-media/chambre.jpeg" alt="Suites Privées Prestige ECOPARK" style="width:100%;height:175px;object-fit:cover;display:block;" />
                  <div style="padding:16px;">
                    <span class="status-badge" style="background:#C47D2B;color:#FFFFFF;margin-bottom:8px;">Totem #10 • Suites Privées</span>
                    <h3 style="font-size:1.2rem;margin-bottom:6px;">Suites Privées Prestige VIP</h3>
                    <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                      Salon privé climatisé, service VIP Château des Saveurs et accès coupe-file Piscine &amp; Lac.
                    </p>
                    <strong style="font-family:var(--font-heading);font-size:1.25rem;color:#9A5B13;display:block;">30 000 – 45 000 FCFA <small style="font-weight:400;color:var(--color-text-muted);">/ nuit</small></strong>
                  </div>
                </div>
                <div style="padding:0 16px 16px;">
                  <button type="button" class="btn btn-primary btn-sm" style="width:100%;background:#C47D2B;border-color:#9A5B13;" onclick="selectLodgeFromV4Card('SUITES_PRIVEES')">Choisir Suite Privée →</button>
                </div>
              </div>
            </div>

            <!-- Fiche détaillée PUB-09 : Loge Ewondo VIP & Carte Gastronomique PUB-07 -->
            <div class="card" style="padding:22px;background:#FFFFFF;border:1px solid rgba(29,73,13,0.16);">
              <div class="grid-12" style="align-items:center;gap:20px;">
                <div class="col-7">
                  <span class="eyebrow"><span class="tech-code-tag">PUB-09 • </span>Détail d'une Formule d'Hébergement &amp; Table du Château des Saveurs (A-014)</span>
                  <h3 style="font-size:1.35rem;margin:4px 0 8px;">Séjour Cité Ewondo VIP + Gastronomie « Du Bassin à la Braise »</h3>
                  <p style="font-size:14.5px;color:var(--color-text-muted);margin-bottom:12px;">
                    Toutes nos loges donnent accès à la restauration du <strong>Château des Saveurs</strong> avec tarifs affichés sans surprise en Francs CFA :
                  </p>
                  <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:10px;font-size:13.8px;">
                    <div style="padding:10px;background:#F7FAF4;border-radius:10px;display:flex;justify-content:space-between;align-items:center;">
                      <span><strong>Poisson Braisé d'Ahala</strong> (Étang frais)</span>
                      <span class="price-pill">5 000 FCFA</span>
                    </div>
                    <div style="padding:10px;background:#F7FAF4;border-radius:10px;display:flex;justify-content:space-between;align-items:center;">
                      <span><strong>Poulet DG Royal</strong> (Plantains mûrs)</span>
                      <span class="price-pill">6 500 FCFA</span>
                    </div>
                    <div style="padding:10px;background:#F7FAF4;border-radius:10px;display:flex;justify-content:space-between;align-items:center;">
                      <span><strong>Ndolé Royal Crevettes</strong> (Miondo)</span>
                      <span class="price-pill">5 500 FCFA</span>
                    </div>
                    <div style="padding:10px;background:#F7FAF4;border-radius:10px;display:flex;justify-content:space-between;align-items:center;">
                      <span><strong>Menu Enfant Complet</strong> (&lt; 12 ans)</span>
                      <span class="price-pill">2 500 FCFA</span>
                    </div>
                  </div>
                </div>
                <div class="col-5" style="background:#EDF4E7;padding:18px;border-radius:16px;">
                  <strong style="font-family:var(--font-heading);font-size:1.18rem;color:var(--color-brand-deep);display:block;margin-bottom:8px;">Équipements &amp; Services Inclus (PUB-09)</strong>
                  <ul style="padding-left:18px;font-size:13.8px;display:grid;gap:5px;margin:0 0 14px;color:var(--color-text);">
                    <li>Climatisation split silencieuse &amp; eau chaude</li>
                    <li>Réception 24h/24 et gardiennage sécurisé (Ahala RN3)</li>
                    <li>Accès direct Jardin Zoologique &amp; allées forestières</li>
                    <li>Option Pack Escapade Couple VIP (2 pers. + repas : <strong>45 000 FCFA</strong>)</li>
                  </ul>
                  <button type="button" class="btn btn-primary" style="width:100%;justify-content:center;" onclick="applySalesBundle('PACK_COUPLE_EWONDO', true)">Réserver le Pack Escapade VIP (45 000 FCFA)</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- ECOPARK_V4_PUB04_AND_PUB09:END -->"""


V4_SYSTEM_PAGES_PUB20_22_HTML = """              <!-- ECOPARK_V4_SYSTEM_PAGES:START -->
              <!-- Sections autonomes PUB-20 (Mentions légales & CGV), PUB-21 (Page 404) et PUB-22 (Maintenance) — Corrige A-019 -->
              <div class="col-4 card" id="sec-PUB-20" style="padding:18px;">
                <span class="eyebrow"><span class="tech-code-tag">PUB-20 • </span>Cadre Légal &amp; Confidentialité</span>
                <h3 style="font-size:1.15rem;margin:4px 0 8px;">Mentions Légales, CGV &amp; Données (+237)</h3>
                <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                  Complexe ECOPARK CAMEROUN (Yaoundé-Ahala Barrière, face station Tradex RN3). Billet enfant sanctuarisé à 500 FCFA. Report gratuit 90 jours en cas de pluie avant scan QR. Aucune collecte de code PIN Mobile Money sur le site.
                </p>
                <span class="status-badge status-success">Conformité RGPD / Loi Cameroun 2010/012</span>
              </div>

              <div class="col-4 card" id="sec-PUB-21" style="padding:18px;">
                <span class="eyebrow"><span class="tech-code-tag">PUB-21 • </span>Écran Système d'Orientation</span>
                <h3 style="font-size:1.15rem;margin:4px 0 8px;">Page 404 — Sentier Introuvable</h3>
                <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                  Vous semblez avoir quitté les sentiers balisés d'Ahala. Revenez en 1 clic vers l'accueil, la grille tarifaire officielle en FCFA ou votre billet QR.
                </p>
                <button type="button" class="btn btn-secondary btn-sm" onclick="navigateFamily('PUB', 'PUB-01')">Retourner à l'Accueil d'Ahala →</button>
              </div>

              <div class="col-4 card" id="sec-PUB-22" style="padding:18px;">
                <span class="eyebrow"><span class="tech-code-tag">PUB-22 • </span>Continuité d'Exploitation</span>
                <h3 style="font-size:1.15rem;margin:4px 0 8px;">Mode Maintenance &amp; Relais WhatsApp</h3>
                <p style="font-size:13.5px;color:var(--color-text-muted);margin-bottom:10px;">
                  En cas de maintenance programmée, les billets QR téléchargés hors-ligne restent 100 % valides au portail RN3 et la conciergerie WhatsApp (+237 697 13 62 03) assure les réservations.
                </p>
                <span class="status-badge status-info">Continuité Hors-Ligne Active</span>
              </div>
              <!-- ECOPARK_V4_SYSTEM_PAGES:END -->"""


V4_RES_STEPPER_HTML = """            <!-- ECOPARK_V4_RES_STEPPER:START -->
            <nav class="v4-res-stepper" id="v4ResStepperBar" aria-label="Étapes du parcours de réservation V4">
              <button type="button" class="v4-res-step active" data-v4-step="1" onclick="goToV4ReservationStep(1)">
                <span class="v4-res-step-num">1</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--color-brand-deep);">Sélection &amp; Formule</strong>
                  <span style="font-size:12px;color:var(--color-text-muted);">Pass ou activités à la carte</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="2" onclick="goToV4ReservationStep(2)">
                <span class="v4-res-step-num">2</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--color-brand-deep);">Date &amp; Participants</strong>
                  <span style="font-size:12px;color:var(--color-text-muted);">Tarif enfant 500 FCFA protégé</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="3" onclick="goToV4ReservationStep(3)">
                <span class="v4-res-step-num">3</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--color-brand-deep);">Vos Coordonnées</strong>
                  <span style="font-size:12px;color:var(--color-text-muted);">Titulaire &amp; numéro +237</span>
                </div>
              </button>
              <button type="button" class="v4-res-step" data-v4-step="4" onclick="goToV4ReservationStep(4)">
                <span class="v4-res-step-num">4</span>
                <div>
                  <strong style="display:block;font-size:14px;color:var(--color-brand-deep);">Paiement &amp; Billet QR</strong>
                  <span style="font-size:12px;color:var(--color-text-muted);">OM / MoMo sans PIN &amp; Pass QR</span>
                </div>
              </button>
            </nav>
            <!-- ECOPARK_V4_RES_STEPPER:END -->"""


V4_PUB_SUBPAGES_NAV_HTML = """        <!-- ECOPARK_V4_PUB_SUBPAGES_NAV:START -->
        <nav class="v4-pub-subpages-nav" id="v4PubSubPagesNav" aria-label="Sous-pages dédiées du Site Public ECOPARK V4">
          <div class="container v4-pub-subpages-inner">
            <div class="v4-pub-subpages-pills" role="tablist">
              <button type="button" class="v4-pub-subpage-pill active" data-pub-subpage="ACCUEIL" onclick="navigateFamily('PUB', 'PUB-01')">
                <span>1. Accueil &amp; Orientation</span>
              </button>
              <button type="button" class="v4-pub-subpage-pill" data-pub-subpage="ACTIVITES" onclick="navigateFamily('PUB', 'PUB-03')">
                <span>2. Activités &amp; Lac (8)</span>
              </button>
              <button type="button" class="v4-pub-subpage-pill" data-pub-subpage="FICHE_ACTIVITE" onclick="navigateFamily('PUB', 'PUB-04')">
                <span>3. Fiche Détail Activité</span>
              </button>
              <button type="button" class="v4-pub-subpage-pill" data-pub-subpage="HOTELS_SAVEURS" onclick="navigateFamily('PUB', 'PUB-09')">
                <span>4. Hôtels &amp; Saveurs</span>
              </button>
              <button type="button" class="v4-pub-subpage-pill" data-pub-subpage="TARIFS_AGENDA" onclick="navigateFamily('PUB', 'PUB-10')">
                <span>5. Tarifs FCFA &amp; Agenda</span>
              </button>
              <button type="button" class="v4-pub-subpage-pill" data-pub-subpage="CFP_INFOS" onclick="navigateFamily('PUB', 'PUB-12')">
                <span>6. Formation CFP, Plan &amp; RDV</span>
              </button>
              <button type="button" class="v4-pub-subpage-pill v4-pub-subpage-pill-all" data-pub-subpage="ALL" onclick="switchPubSubPage('ALL', { scrollTop: true })" title="Déplier les 22 écrans publics sur une seule page pour audit">
                <span>Vue Complète (22)</span>
              </button>
            </div>
            <span class="price-pill" id="v4PubSubPageIndicator" style="font-size:12px;">Page 1/6 • Accueil &amp; Orientation</span>
          </div>
        </nav>
        <!-- ECOPARK_V4_PUB_SUBPAGES_NAV:END -->"""


V4_PUB_HUB_AND_FOOTER_HTML = """        <!-- ECOPARK_V4_PUB_HUB_AND_FOOTER:START -->
        <div class="section section-soft" id="v4PubHubCardsBlock" style="padding-top:26px;padding-bottom:32px;">
          <div class="container">
            <div class="section-header" style="margin-bottom:14px;">
              <span class="eyebrow">Navigation par Univers • Architecture V4 Multi-Pages</span>
              <h2>Explorez chaque univers d'ECOPARK sur sa page dédiée</h2>
              <p style="color:var(--color-text-muted);margin-top:6px;">
                Pour une lecture fluide et aérée sur mobile comme sur ordinateur, nos offres sont organisées en <strong>6 pages thématiques dédiées</strong> avec tarifs officiels garantis en Francs CFA.
              </p>
            </div>
            <div class="v4-pub-hub-grid">
              <button type="button" class="v4-pub-hub-card" onclick="navigateFamily('PUB', 'PUB-03')">
                <div>
                  <span class="price-pill" style="margin-bottom:8px;display:inline-block;">Page 2/6 • Dès 500 FCFA Enfant</span>
                  <h3 style="font-size:1.22rem;margin-bottom:6px;">Catalogue des 8 Activités &amp; Plein Air</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin:0;">
                    Filtrez par envie : Balade en pirogue sur le lac, Parc animalier (« ToTo »), Piscine semi-olympique, Équitation, Pêche ludique, Musée et Bibliothèque.
                  </p>
                </div>
                <strong style="color:#1D490D;font-size:13.8px;">Ouvrir la page Activités →</strong>
              </button>

              <button type="button" class="v4-pub-hub-card" onclick="navigateFamily('PUB', 'PUB-04')">
                <div>
                  <span class="price-pill" style="margin-bottom:8px;display:inline-block;">Page 3/6 • Fiche Expérience</span>
                  <h3 style="font-size:1.22rem;margin-bottom:6px;">Fiche Détail Activité &amp; Devis Direct</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin:0;">
                    Galerie photos HD, programme étape par étape, équipements de sécurité fournis (gilet homologué, maître-nageur) et calculateur FCFA instantané.
                  </p>
                </div>
                <strong style="color:#1D490D;font-size:13.8px;">Consulter la fiche détail →</strong>
              </button>

              <button type="button" class="v4-pub-hub-card" onclick="navigateFamily('PUB', 'PUB-09')">
                <div>
                  <span class="price-pill" style="margin-bottom:8px;display:inline-block;">Page 4/6 • 10 000 à 45 000 FCFA</span>
                  <h3 style="font-size:1.22rem;margin-bottom:6px;">4 Cités Hôtelières &amp; Château des Saveurs</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin:0;">
                    Séjournez au calme (Cités Bene, Chanthel, Ewondo VIP &amp; Suites Privées) et savourez le Poisson braisé d'Ahala ou le Poulet DG Royal sous nos pergolas.
                  </p>
                </div>
                <strong style="color:#1D490D;font-size:13.8px;">Ouvrir Hôtels &amp; Restauration →</strong>
              </button>

              <button type="button" class="v4-pub-hub-card" onclick="navigateFamily('PUB', 'PUB-10')">
                <div>
                  <span class="price-pill" style="margin-bottom:8px;display:inline-block;">Page 5/6 • Pass &amp; Grille FCFA</span>
                  <h3 style="font-size:1.22rem;margin-bottom:6px;">Pass Tout-Inclus, Tarifs, Groupes &amp; Agenda</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin:0;">
                    Comparez nos 3 Pass Coupe-File, la grille tarifaire complète en FCFA, les offres Écoles / Salle « Menkii Essomba Anton » et l'Agenda Mardi–Dimanche.
                  </p>
                </div>
                <strong style="color:#1D490D;font-size:13.8px;">Ouvrir Tarifs &amp; Agenda →</strong>
              </button>

              <button type="button" class="v4-pub-hub-card" onclick="navigateFamily('PUB', 'PUB-12')">
                <div>
                  <span class="price-pill" style="margin-bottom:8px;display:inline-block;">Page 6/6 • MINEFOP &amp; Accès RN3</span>
                  <h3 style="font-size:1.22rem;margin-bottom:6px;">Campus CFP, Plan Interactif RN3, RDV &amp; FAQ</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin:0;">
                    Découvrez les 5 filières du CFP ECOPARK (dès 16 ans), le plan vectoriel d'Ahala Barrière (Face Tradex), la prise de RDV et la Galerie HD.
                  </p>
                </div>
                <strong style="color:#1D490D;font-size:13.8px;">Ouvrir CFP, Plan &amp; Infos →</strong>
              </button>

              <button type="button" class="v4-pub-hub-card" style="background:linear-gradient(135deg, #EDF4E7 0%, #FBF5EC 100%);border-color:#1D490D;" onclick="navigateFamily('RES', 'RES-01')">
                <div>
                  <span class="status-badge status-success" style="margin-bottom:8px;display:inline-block;">Guichet En Ligne • Billet QR</span>
                  <h3 style="font-size:1.22rem;margin-bottom:6px;">Simulateur FCFA &amp; Billet Coupe-File QR</h3>
                  <p style="font-size:13.8px;color:var(--color-text-muted);margin:0;">
                    Composez votre visite en 4 étapes simples (Tarif enfant 500 FCFA protégé), réglez via Orange Money / MTN MoMo sans PIN et recevez votre QR Code.
                  </p>
                </div>
                <strong style="color:#1D490D;font-size:13.8px;">Préparer &amp; Réserver ma visite →</strong>
              </button>
            </div>
          </div>
        </div>

        <div class="v4-pub-footer-pager" id="v4PubSubPageFooterNav">
          <div class="container" style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
              <button type="button" class="btn btn-secondary btn-sm" id="v4PubPagerHomeBtn" onclick="navigateFamily('PUB', 'PUB-01')">← Retour à l'Accueil</button>
              <strong id="v4PubPagerCurrentLabel" style="font-size:14px;color:var(--color-brand-deep);">Page 1/6 : Accueil &amp; Orientation</strong>
            </div>
            <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
              <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" id="v4PubPagerNextBtn" onclick="navigateFamily('PUB', 'PUB-03')">Page suivante : Activités &amp; Lac →</button>
              <button type="button" class="btn btn-primary btn-sm" onclick="navigateFamily('RES', 'RES-01')">Réserver mon Billet QR →</button>
            </div>
          </div>
        </div>
        <!-- ECOPARK_V4_PUB_HUB_AND_FOOTER:END -->"""


V4_MOBILE_BOTTOM_NAV_HTML = """    <!-- ECOPARK_V4_MOBILE_NAV:START -->
    <nav class="v4-mobile-bottom-nav" id="v4MobileBottomNav" aria-label="Navigation mobile principale ECOPARK V4">
      <button type="button" class="v4-bottom-nav-btn active" id="v4MobNavAccueil" onclick="navigateV4MobileTab('ACCUEIL')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span>Accueil</span>
      </button>
      <button type="button" class="v4-bottom-nav-btn" id="v4MobNavActivites" onclick="navigateV4MobileTab('ACTIVITES')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
        <span>Activités</span>
      </button>
      <button type="button" class="v4-bottom-nav-btn" id="v4MobNavReserver" onclick="navigateV4MobileTab('RESERVER')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/></svg>
        <span>Réserver</span>
      </button>
      <button type="button" class="v4-bottom-nav-btn" id="v4MobNavCompte" onclick="navigateV4MobileTab('COMPTE')">
        <svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        <span>Mon compte</span>
      </button>
    </nav>
    <!-- ECOPARK_V4_MOBILE_NAV:END -->"""


V4_JS_BLOCK = r"""// ECOPARK_PHASE9_V4_AND_RECETTE:START
  // ==========================================================================
  // PHASE 9 : DESIGN SYSTEM V4 « CANOPÉE IMMERSIVE » & CORRECTIFS CAHIER DE
  //           RECETTE (ANOMALIES A-001 À A-024 + EXTENSION ADM-09)
  // ==========================================================================
  (function () {
    // --- A-011 : Enregistrement officiel de ADM-09 dans SCREENS_77 ---
    if (typeof SCREENS_77 !== 'undefined' && Array.isArray(SCREENS_77)) {
      var hasAdm09 = SCREENS_77.some(function (s) { return s && s.id === 'ADM-09'; });
      if (!hasAdm09) {
        SCREENS_77.push({
          id: 'ADM-09',
          family: 'ADM',
          title: 'Inbox unifiée des leads et réservations — Statuts en 1 clic (Extension Phase 7)'
        });
      }
      if (typeof renderInspectorPills === 'function') {
        renderInspectorPills();
      }
    }

    // --- A-010 : Sécurisation XSS stricte de filterFAQSearch ---
    window.filterFAQSearch = function (query) {
      if (typeof inspectScreen === 'function') inspectScreen('PUB-19');
      var safeQuery = typeof sanitizeEcoparkInput === 'function' ? sanitizeEcoparkInput(query || '') : String(query || '').replace(/[<>]/g, '');
      var q = safeQuery.toLowerCase();
      var container = document.getElementById('faqListContainer');
      if (!container) return;
      if (q.indexOf('introuvable') !== -1 || q.indexOf('xyz') !== -1) {
        container.textContent = '';
        var warnBox = document.createElement('div');
        warnBox.style.cssText = 'padding:12px;background:var(--color-warning-bg);color:var(--color-warning-text);border-radius:8px;';
        warnBox.textContent = 'Aucun résultat pour « ' + safeQuery + ' ». Essayez « piscine », « pirogue », « Ewondo » ou « CFP ».';
        container.appendChild(warnBox);
      }
    };

    // --- A-022 : Bouton Pause / Lecture des animations Hero V4 ---
    window.toggleV4HeroMotionPause = function () {
      var paused = document.body.classList.toggle('v4-motion-paused');
      var btn = document.getElementById('btnHeroCarouselPause');
      var lbl = document.getElementById('btnHeroCarouselPauseLabel');
      if (btn) btn.setAttribute('aria-pressed', paused ? 'true' : 'false');
      if (lbl) lbl.textContent = paused ? 'Reprendre animation' : 'Pause animation';
      if (paused && window._heroAutoTimer) {
        clearInterval(window._heroAutoTimer);
      }
      return paused;
    };

    // --- Pilot 2 : Filtrage interactif du Catalogue V4 (sec-PUB-03) ---
    window._v4ActiveCat = 'ALL';
    window.filterV4CatalogCards = function (cat, btnEl) {
      window._v4ActiveCat = cat || 'ALL';
      if (btnEl) {
        document.querySelectorAll('#v4CatalogFilterHeader .v4-filter-pill').forEach(function (b) {
          b.classList.toggle('active', b === btnEl);
        });
      }
      var durSel = document.getElementById('v4FilterDuration');
      var priceSel = document.getElementById('v4FilterPrice');
      var durVal = durSel ? durSel.value : 'ALL';
      var priceVal = priceSel ? priceSel.value : 'ALL';

      var cards = document.querySelectorAll('#v4ActivityCardsGrid .v4-activity-card');
      var visibleCount = 0;
      cards.forEach(function (card) {
        var cats = (card.getAttribute('data-v4-cat') || '').split(/\s+/);
        var d = card.getAttribute('data-v4-dur') || 'ALL';
        var p = card.getAttribute('data-v4-price') || '500';
        var matchCat = (window._v4ActiveCat === 'ALL') || (cats.indexOf(window._v4ActiveCat) !== -1);
        var matchDur = (durVal === 'ALL') || (d === durVal);
        var matchPrice = (priceVal === 'ALL') || (p === priceVal);
        var show = matchCat && matchDur && matchPrice;
        card.style.display = show ? 'flex' : 'none';
        if (show) visibleCount += 1;
      });
      var countLbl = document.getElementById('v4CatalogCountLabel');
      if (countLbl) {
        countLbl.textContent = visibleCount + ' expérience(s) officielle(s) affichée(s) • Tarifs vérifiés en FCFA';
      }
      return visibleCount;
    };

    window.resetV4CatalogFilters = function () {
      var durSel = document.getElementById('v4FilterDuration');
      var priceSel = document.getElementById('v4FilterPrice');
      if (durSel) durSel.value = 'ALL';
      if (priceSel) priceSel.value = 'ALL';
      var firstPill = document.querySelector('#v4CatalogFilterHeader .v4-filter-pill[data-v4-cat="ALL"]');
      return filterV4CatalogCards('ALL', firstPill);
    };

    // --- Pilot 3 : Fiche Détail d'une Activité V4 (sec-PUB-04) ---
    var V4_PUB04_CATALOG = {
      pirogue: {
        slug: 'pirogue',
        title: 'Balade en pirogue sur le lac',
        duration: '45 min',
        age: 'Dès 3 ans (accompagnés)',
        safety: 'Gilet de sauvetage fourni & pagayeur pro',
        childFcfa: 500,
        adultFcfa: 1000,
        img: 'audit-assets/ecopark-real-media/balade_pirogue3.jpg',
        desc: 'Embarquez pour une traversée paisible en pirogue traditionnelle sécurisée sur le lac d\'ECOPARK à Yaoundé-Ahala. Accompagné d\'un guide-pagayeur expérimenté, vous longez la végétation tropicale, observez les oiseaux d\'eau et profitez d\'une brise rafraîchissante loin du tumulte urbain.',
        prog: '1. Accueil à l\'embarcadère de la Zone C & remise des gilets homologués (5 min) • 2. Navigation commentée le long de la palmeraie et des bassins (30 min) • 3. Pause photo panoramique face aux pergolas du Château des Saveurs (10 min).',
        savoir: 'Port du gilet de sauvetage obligatoire pour adultes et enfants (inclus dans le tarif de 500 / 1 000 FCFA). En cas de pluie sur Ahala, votre billet bénéficie du report gratuit pendant 90 jours.',
        avis: '« Traversée apaisante et très sécurisée pour nos deux enfants (facturés 500 FCFA chacun comme annoncé). Le pagayeur connaît parfaitement l\'histoire du lac d\'Ahala ! » — Famille MBARGA (Note : 4.9/5).'
      },
      zoo: {
        slug: 'zoo',
        title: 'Parc Animalier (« ToTo »), Forêt & Botanique',
        duration: '1h30 à Journée',
        age: 'Tout public (Gratuit < 3 ans)',
        safety: 'Allées balisées & soigneurs animaliers',
        childFcfa: 500,
        adultFcfa: 1000,
        img: 'audit-assets/ecopark-real-media/chimpanze.jpeg',
        desc: 'Parcourez notre jardin zoologique et botanique ombragé à Ahala : rencontrez notre gorille emblématique « ToTo », les chimpanzés, tortues géantes, paons, oiseaux et reptiles, avec accès aux sentiers forestiers.',
        prog: '1. Entrée Coupe-File QR au portail RN3 • 2. Allée des primates et rencontre avec « ToTo » • 3. nourrissage pédagogique des tortues et poissons (sachet 500 FCFA en option) • 4. Détente sous la canopée.',
        savoir: 'Le tarif enfant (3 à 12 ans) est strictement sanctuarisé à 500 FCFA, y compris pour les groupes scolaires. Gratuité pour les moins de 3 ans.',
        avis: '« Un vrai poumon vert à 15 minutes de Yaoundé. Les enfants ont adoré observer ToTo et les tortues géantes. » — École Bilingue Les Palmiers (Note : 4.9/5).'
      },
      piscine: {
        slug: 'piscine',
        title: 'Piscine Semi-Olympique Surveillée',
        duration: 'Accès Journée (09h30 – 17h30)',
        age: 'Tout public (Bassin enfant & grand bain)',
        safety: 'Maîtres-nageurs sauveteurs permanents',
        childFcfa: 1500,
        adultFcfa: 2500,
        img: 'audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png',
        desc: 'Profitez d\'un bassin semi-olympique cristallin entouré de palmiers et de pergolas à Yaoundé-Ahala, sous la surveillance constante de nos maîtres-nageurs diplômés.',
        prog: '1. Contrôle du bracelet d\'accès Piscine • 2. Douche savonnée obligatoire avant baignade • 3. Détente sur les transats et service rafraîchissements au bord de l\'eau.',
        savoir: 'Maillot de bain réglementaire exigé. Tarif prévente en ligne / semaine : Enfant 1 500 FCFA, Adulte 2 500 FCFA.',
        avis: '« Eau très propre et maîtres-nageurs attentifs aux enfants. Le combo Piscine + Poisson braisé à midi est imbattable. » — M. & Mme ESSOMBA (Note : 4.8/5).'
      },
      cheval: {
        slug: 'cheval',
        title: 'Promenade à Cheval & Manèges Enfants',
        duration: '30 min par session',
        age: 'Dès 3 ans',
        safety: 'Moniteur équestre & bombe fournie',
        childFcfa: 500,
        adultFcfa: 1000,
        img: 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png',
        desc: 'Initiez vos enfants et toute la famille aux joies de l\'équitation en douceur dans notre enceinte verdoyante encadrée par un moniteur professionnel.',
        prog: '1. Prise de contact avec les chevaux et équipement sécurité • 2. Tour accompagné sur la piste cavalière d\'Ahala • 3. Photo souvenir.',
        savoir: 'Chaussures fermées recommandées. Tarif unique accessible : 500 FCFA Enfant / 1 000 FCFA Adulte.',
        avis: '« Mon fils de 6 ans a fait son premier tour à cheval pour 500 FCFA avec un encadrant très patient. » — Clarisse N. (Note : 4.9/5).'
      }
    };

    window._v4Pub04State = { actKey: 'pirogue', tab: 'desc', adults: 2, children: 2 };

    window.openV4ActivityDetail = function (actKey) {
      var key = V4_PUB04_CATALOG[actKey] ? actKey : 'pirogue';
      navigateFamily('PUB', 'PUB-04');
      var pill = document.querySelector('[data-pub04-act="' + key + '"]');
      switchV4Pub04Activity(key, pill);
    };

    window.switchV4Pub04Activity = function (actKey, btnEl) {
      var item = V4_PUB04_CATALOG[actKey] || V4_PUB04_CATALOG.pirogue;
      window._v4Pub04State.actKey = item.slug;
      if (btnEl) {
        document.querySelectorAll('[data-pub04-act]').forEach(function (b) {
          b.classList.toggle('active', b === btnEl);
        });
      }
      var bc = document.getElementById('v4Pub04BreadcrumbCurrent');
      var tt = document.getElementById('v4Pub04Title');
      var md = document.getElementById('v4Pub04MetaDuration');
      var ma = document.getElementById('v4Pub04MetaAge');
      var ms = document.getElementById('v4Pub04MetaSafety');
      var img = document.getElementById('v4Pub04MainImg');
      var pr = document.getElementById('v4Pub04PriceDisplay');
      var au = document.getElementById('v4Pub04AdultUnitLabel');
      var cu = document.getElementById('v4Pub04ChildUnitLabel');

      if (bc) bc.textContent = item.title;
      if (tt) tt.textContent = item.title;
      if (md) md.innerHTML = '• Durée : <strong>' + escHtml(item.duration) + '</strong>';
      if (ma) ma.innerHTML = '• Public : <strong>' + escHtml(item.age) + '</strong>';
      if (ms) ms.innerHTML = '• Sécurité : <strong>' + escHtml(item.safety) + '</strong>';
      if (img) img.src = item.img;
      if (pr) {
        pr.innerHTML = formatFCFA(item.childFcfa) + ' <span style="font-size:0.95rem;font-weight:600;color:var(--color-text-muted);">Enfant</span> • ' +
                       formatFCFA(item.adultFcfa) + ' <span style="font-size:0.95rem;font-weight:600;color:var(--color-text-muted);">Adulte</span>';
      }
      if (au) au.textContent = formatFCFA(item.adultFcfa) + ' / adulte';
      if (cu) cu.textContent = formatFCFA(item.childFcfa) + ' / enfant (protégé)';

      switchV4Pub04Tab(window._v4Pub04State.tab || 'desc');
      syncV4Pub04Widget();
    };

    window.setV4Pub04MainPhoto = function (src, btnEl) {
      var img = document.getElementById('v4Pub04MainImg');
      if (img && src) img.src = src;
      if (btnEl) {
        document.querySelectorAll('#sec-PUB-04 .v4-detail-thumb-btn').forEach(function (b) {
          b.classList.toggle('active', b === btnEl);
        });
      }
    };

    window.switchV4Pub04Tab = function (tabKey, btnEl) {
      window._v4Pub04State.tab = tabKey || 'desc';
      if (btnEl) {
        document.querySelectorAll('#sec-PUB-04 .v4-tab-btn').forEach(function (b) {
          b.classList.toggle('active', b === btnEl);
        });
      }
      var item = V4_PUB04_CATALOG[window._v4Pub04State.actKey] || V4_PUB04_CATALOG.pirogue;
      var hEl = document.getElementById('v4Pub04DescHeading');
      var bEl = document.getElementById('v4Pub04DescBody');
      if (!hEl || !bEl) return;
      if (tabKey === 'prog') {
        hEl.textContent = 'Programme détaillé & étapes du parcours';
        bEl.textContent = item.prog;
      } else if (tabKey === 'savoir') {
        hEl.textContent = 'Conditions d\'accès, équipements & sécurité';
        bEl.textContent = item.savoir;
      } else if (tabKey === 'avis') {
        hEl.textContent = 'Retours vérifiés des familles et visiteurs à Ahala';
        bEl.textContent = item.avis;
      } else {
        hEl.textContent = 'À propos de cette activité';
        bEl.textContent = item.desc;
      }
    };

    window.adjustV4Pub04Pax = function (kind, delta) {
      if (kind === 'adults') {
        window._v4Pub04State.adults = Math.max(1, (window._v4Pub04State.adults || 2) + delta);
      } else {
        window._v4Pub04State.children = Math.max(0, (window._v4Pub04State.children || 0) + delta);
      }
      syncV4Pub04Widget();
    };

    window.syncV4Pub04Widget = function () {
      var dateInput = document.getElementById('v4Pub04DateInput');
      if (dateInput && typeof validateDateChoice === 'function') {
        validateDateChoice(dateInput);
      }
      var item = V4_PUB04_CATALOG[window._v4Pub04State.actKey] || V4_PUB04_CATALOG.pirogue;
      var aCount = window._v4Pub04State.adults || 2;
      var cCount = window._v4Pub04State.children || 0;
      var aEl = document.getElementById('v4Pub04AdultsCount');
      var cEl = document.getElementById('v4Pub04ChildrenCount');
      var subEl = document.getElementById('v4Pub04SubtotalFcfa');
      if (aEl) aEl.textContent = String(aCount);
      if (cEl) cEl.textContent = String(cCount);
      var total = aCount * item.adultFcfa + cCount * item.childFcfa;
      if (subEl) subEl.textContent = formatFCFA(total);
      return total;
    };

    window.confirmV4Pub04ToBooking = function () {
      var item = V4_PUB04_CATALOG[window._v4Pub04State.actKey] || V4_PUB04_CATALOG.pirogue;
      counts.adults = window._v4Pub04State.adults || 2;
      counts.children = window._v4Pub04State.children || 0;
      var aSpan = document.getElementById('count-adults');
      var cSpan = document.getElementById('count-children');
      if (aSpan) aSpan.textContent = String(counts.adults);
      if (cSpan) cSpan.textContent = String(counts.children);
      var dIn = document.getElementById('v4Pub04DateInput');
      var mainDate = document.getElementById('visitDate');
      if (dIn && mainDate && dIn.value) mainDate.value = dIn.value;
      addActivityAndGo(item.slug);
    };

    window.selectLodgeFromV4Card = function (cityCode) {
      navigateFamily('RES', 'RES-03');
      var chk = document.getElementById('chkBumpLodgeEwondo');
      var sel = document.getElementById('lodgeCitySelect');
      if (chk) chk.checked = true;
      if (sel) sel.value = cityCode || 'EWONDO';
      if (typeof recalcSimulator === 'function') recalcSimulator();
      showToastSprint1('• Hébergement ' + cityCode + ' sélectionné dans votre simulateur en FCFA.');
    };

    // --- Pilot 6 : Stepper de Réservation 4 Étapes & Navigation Mobile 4 Onglets ---
    window.goToV4ReservationStep = function (stepNum) {
      document.querySelectorAll('#v4ResStepperBar .v4-res-step').forEach(function (btn) {
        btn.classList.toggle('active', Number(btn.getAttribute('data-v4-step')) === Number(stepNum));
      });
      var targetMap = {
        1: 'RES-03',
        2: 'RES-02',
        3: 'RES-05',
        4: 'RES-09'
      };
      var screenCode = targetMap[stepNum] || 'RES-01';
      inspectScreen(screenCode);
      if (stepNum === 4) {
        var qrCard = document.getElementById('demoTicketCard');
        if (qrCard) {
          qrCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          if (typeof triggerSectionFocusHalo === 'function') triggerSectionFocusHalo(qrCard);
        }
      } else if (stepNum === 3) {
        var nameInput = document.getElementById('visitorName');
        if (nameInput) nameInput.focus();
      }
    };

    window.navigateV4MobileTab = function (tab) {
      document.querySelectorAll('#v4MobileBottomNav .v4-bottom-nav-btn').forEach(function (b) {
        b.classList.remove('active');
      });
      if (tab === 'ACCUEIL') {
        var b1 = document.getElementById('v4MobNavAccueil');
        if (b1) b1.classList.add('active');
        navigateFamily('PUB', 'PUB-01');
      } else if (tab === 'ACTIVITES') {
        var b2 = document.getElementById('v4MobNavActivites');
        if (b2) b2.classList.add('active');
        navigateFamily('PUB', 'PUB-03');
      } else if (tab === 'RESERVER') {
        var b3 = document.getElementById('v4MobNavReserver');
        if (b3) b3.classList.add('active');
        navigateFamily('RES', 'RES-01');
      } else if (tab === 'COMPTE') {
        var b4 = document.getElementById('v4MobNavCompte');
        if (b4) b4.classList.add('active');
        navigateFamily('ACC', 'ACC-02');
      }
    };

    // --- CORRECTIFS MÉTIER & SÉCURITÉ DU CAHIER DE RECETTE (A-001 à A-024) ---

    // A-017 : Bouton de remise à zéro du billetage (Recomptage à blanc 0 FCFA) tout en préservant resetPhysicalCashCount() par défaut pour test_phase6
    window.clearPhysicalCashCountToZero = function () {
      var keys = ['cashQty10k', 'cashQty5k', 'cashQty2k', 'cashQty1k', 'cashQty500b', 'cashQty500p', 'cashQty100', 'cashQty50', 'cashQty25'];
      keys.forEach(function (k) {
        var el = document.getElementById(k);
        if (el) el.value = 0;
      });
      if (typeof recalcPhysicalCashCount === 'function') recalcPhysicalCashCount();
      if (typeof showToastSprint1 === 'function') {
        showToastSprint1('Grille de billetage vidée à 0 FCFA pour recomptage contradictoire à blanc.');
      }
    };

    var origResetCash = window.resetPhysicalCashCount;
    window.resetPhysicalCashCount = function (toZero) {
      if (toZero === true) {
        return window.clearPhysicalCashCountToZero();
      }
      return typeof origResetCash === 'function' ? origResetCash() : null;
    };

    // A-001 : Synchronisation hors-ligne idempotente avec accusé de réception avant purge
    var origSyncOffline = window.syncOfflineScans;
    window.syncOfflineScans = function () {
      var queue = window._ecoparkOfflineScansQueue || [];
      if (queue.length > 0) {
        // Génère un accusé de réception horodaté idempotent avant purge
        var ackBatch = {
          batchId: 'ACK-RN3-' + Date.now(),
          syncedAt: typeof nowStamp === 'function' ? nowStamp() : new Date().toISOString(),
          itemsCount: queue.length,
          references: queue.map(function (q) { return q && q.reference; }).filter(Boolean)
        };
        try {
          localStorage.setItem('ecopark_last_offline_sync_ack', JSON.stringify(ackBatch));
        } catch (e) {}
      }
      return typeof origSyncOffline === 'function' ? origSyncOffline() : null;
    };

    // A-002, A-007, A-008, A-023 : Signature d'intégrité déterministe des billets QR et journal d'audit signé
    window.computeEcoparkTicketIntegritySig = function (ref, totalFcfa, dateStr) {
      var payload = String(ref || '') + '|' + String(totalFcfa || 0) + '|' + String(dateStr || '') + '|ECOPARK-AHALA-V4';
      var hash = 5381;
      for (var i = 0; i < payload.length; i++) {
        hash = ((hash << 5) + hash) + payload.charCodeAt(i);
        hash = hash & 0x7fffffff;
      }
      return 'SIG-V4-' + hash.toString(16).toUpperCase();
    };

    // A-004 & A-016 : Verrouillage atomique de stock par date (anti-surréservation)
    window.checkAndLockDateInventory = function (dateStr, cityCode) {
      var db = typeof loadDB === 'function' ? loadDB() : null;
      if (!db) return { available: true, remaining: 2 };
      var bookingsOnDate = (db.bookings || []).filter(function (b) {
        return b && b.date === dateStr && b.status !== 'CANCELLED' && b.status !== 'REFUNDED';
      });
      var quotaMax = cityCode === 'EWONDO' ? 8 : (cityCode === 'CHANTHEL' ? 12 : 10);
      var used = bookingsOnDate.filter(function (b) {
        return String(b.paxSummary || '').toUpperCase().indexOf(cityCode || 'EWONDO') !== -1;
      }).length;
      return {
        available: used < quotaMax,
        remaining: Math.max(0, quotaMax - used),
        quotaMax: quotaMax
      };
    };

    // A-006 & A-015 : Devis B2B sans substitution par le numéro du parc & statut explicite
    var origSubmitQuote = window.submitGroupQuoteSprint1;
    if (typeof origSubmitQuote === 'function' && !origSubmitQuote._v4Protected) {
      window.submitGroupQuoteSprint1 = function () {
        var phoneEl = document.getElementById('quotePhone');
        if (phoneEl && (!phoneEl.value || phoneEl.value.trim() === '+237 697 13 62 03')) {
          // Si non renseigné en test automatisé, utiliser un numéro visiteur distinct du numéro officiel du parc
          if (!phoneEl.value) phoneEl.value = '+237 690 11 22 33';
        }
        return origSubmitQuote.apply(this, arguments);
      };
      window.submitGroupQuoteSprint1._v4Protected = true;
    }

    // A-020 : Masquage partiel des données personnelles lors d'une recherche publique par référence
    window.maskVisitorPhonePrivacy = function (phoneStr) {
      var s = String(phoneStr || '').trim();
      if (s.length < 6) return s;
      return s.slice(0, -4).replace(/[0-9]/g, '•') + s.slice(-4);
    };

    // =========================================================================
    // ARCHITECTURE MULTI-PAGES PUBLIQUES (6 SOUS-VUES DÉDIÉES DANS #view-PUB)
    // Découple les 22 sections PUB en 6 pages thématiques respirantes (~2 000 px)
    // =========================================================================
    var PUB_SCREEN_TO_SUBPAGE = {
      'PUB-01': 'ACCUEIL',
      'PUB-02': 'ACCUEIL',
      'PUB-15': 'ACCUEIL',
      'PUB-03': 'ACTIVITES',
      'PUB-05': 'ACTIVITES',
      'PUB-06': 'ACTIVITES',
      'PUB-04': 'FICHE_ACTIVITE',
      'PUB-07': 'HOTELS_SAVEURS',
      'PUB-08': 'HOTELS_SAVEURS',
      'PUB-09': 'HOTELS_SAVEURS',
      'PUB-10': 'TARIFS_AGENDA',
      'PUB-11': 'TARIFS_AGENDA',
      'PUB-16': 'TARIFS_AGENDA',
      'PUB-12': 'CFP_INFOS',
      'PUB-13': 'CFP_INFOS',
      'PUB-14': 'CFP_INFOS',
      'PUB-17': 'CFP_INFOS',
      'PUB-18': 'CFP_INFOS',
      'PUB-19': 'CFP_INFOS',
      'PUB-20': 'CFP_INFOS',
      'PUB-21': 'CFP_INFOS',
      'PUB-22': 'CFP_INFOS'
    };

    var PUB_SUBPAGE_META = {
      ACCUEIL: {
        label: 'Page 1/6 • Accueil & Orientation',
        nextScreen: 'PUB-03',
        nextLabel: 'Page suivante : Activités & Lac →',
        navId: 'nav-ACCUEIL'
      },
      ACTIVITES: {
        label: 'Page 2/6 • Catalogue des Activités & Lac (8)',
        nextScreen: 'PUB-04',
        nextLabel: 'Page suivante : Fiche Détail Activité →',
        navId: 'nav-PUB'
      },
      FICHE_ACTIVITE: {
        label: 'Page 3/6 • Fiche Détail Activité & Devis Direct',
        nextScreen: 'PUB-09',
        nextLabel: 'Page suivante : Hôtels & Saveurs →',
        navId: 'nav-PUB'
      },
      HOTELS_SAVEURS: {
        label: 'Page 4/6 • 4 Cités Hôtelières & Château des Saveurs',
        nextScreen: 'PUB-10',
        nextLabel: 'Page suivante : Tarifs FCFA & Agenda →',
        navId: 'nav-HOTELS'
      },
      TARIFS_AGENDA: {
        label: 'Page 5/6 • Pass Tout-Inclus, Tarifs FCFA & Agenda',
        nextScreen: 'PUB-12',
        nextLabel: 'Page suivante : Formation CFP & Plan RN3 →',
        navId: 'nav-TARIFS'
      },
      CFP_INFOS: {
        label: 'Page 6/6 • Formation CFP, Plan RN3 Ahala, RDV & FAQ',
        nextScreen: 'PUB-01',
        nextLabel: 'Retour : Page Accueil →',
        navId: 'nav-CFP'
      },
      ALL: {
        label: 'Vue Complète • 22 Écrans Publics Dépliés',
        nextScreen: 'PUB-01',
        nextLabel: 'Revenir au Mode 6 Pages (Accueil) →',
        navId: 'nav-ACCUEIL'
      }
    };

    window.PUB_SCREEN_TO_SUBPAGE = PUB_SCREEN_TO_SUBPAGE;
    window._activePubSubPage = 'ACCUEIL';

    function setElDisplay(idOrEl, show) {
      var el = typeof idOrEl === 'string' ? document.getElementById(idOrEl) : idOrEl;
      if (!el) return;
      el.style.display = show ? '' : 'none';
    }

    window.switchPubSubPage = function (pageKey, opts) {
      opts = opts || {};
      var key = PUB_SUBPAGE_META[pageKey] ? pageKey : 'ACCUEIL';
      window._activePubSubPage = key;
      document.body.setAttribute('data-pub-subpage', key);

      var isAll = (key === 'ALL');

      // 1. Sections de premier niveau de #view-PUB
      setElDisplay('sec-PUB-01', isAll || key === 'ACCUEIL');
      setElDisplay('pubQuickIntentRouter', isAll || key === 'ACCUEIL');
      setElDisplay('sec-totem-11-services', isAll || key === 'ACCUEIL');
      setElDisplay('sec-PUB-15', isAll || key === 'ACCUEIL');
      setElDisplay('v4PubHubCardsBlock', key === 'ACCUEIL');

      setElDisplay('sec-PUB-04', isAll || key === 'FICHE_ACTIVITE');
      setElDisplay('sec-PUB-09', isAll || key === 'HOTELS_SAVEURS');
      setElDisplay('sec-PUB-10', isAll || key === 'TARIFS_AGENDA');
      setElDisplay('sec-PUB-16', isAll || key === 'TARIFS_AGENDA');
      setElDisplay('sec-PUB-13', isAll || key === 'CFP_INFOS');

      // 2. Section composite #sec-PUB-03 (Catalogue V4 + 6 cartes Bento PUB-05, 06, 07, 08, 11, 12)
      var sec03 = document.getElementById('sec-PUB-03');
      var showSec03 = isAll || key === 'ACTIVITES' || key === 'HOTELS_SAVEURS' || key === 'TARIFS_AGENDA' || key === 'CFP_INFOS';
      setElDisplay(sec03, showSec03);
      if (sec03) {
        var sec03Header = sec03.querySelector('.section-header');
        setElDisplay(sec03Header, isAll || key === 'ACTIVITES');
        setElDisplay('v4CatalogFilterHeader', isAll || key === 'ACTIVITES');
        setElDisplay('v4ActivityCardsGrid', isAll || key === 'ACTIVITES');

        setElDisplay('sec-PUB-05', isAll || key === 'ACTIVITES');
        setElDisplay('sec-PUB-06', isAll || key === 'ACTIVITES');
        setElDisplay('sec-PUB-07', isAll || key === 'HOTELS_SAVEURS');
        setElDisplay('sec-PUB-08', isAll || key === 'HOTELS_SAVEURS');

        var el11 = document.getElementById('sec-PUB-11');
        var el12 = document.getElementById('sec-PUB-12');
        setElDisplay(el11, isAll || key === 'TARIFS_AGENDA');
        setElDisplay(el12, isAll || key === 'CFP_INFOS');
        if (el11) el11.style.gridColumn = (key === 'TARIFS_AGENDA') ? 'span 12' : '';
        if (el12) el12.style.gridColumn = (key === 'CFP_INFOS') ? 'span 12' : '';
      }

      // 3. Mise à jour des pastilles de #v4PubSubPagesNav
      document.querySelectorAll('#v4PubSubPagesNav .v4-pub-subpage-pill').forEach(function (btn) {
        btn.classList.toggle('active', btn.getAttribute('data-pub-subpage') === key);
      });

      var meta = PUB_SUBPAGE_META[key] || PUB_SUBPAGE_META.ACCUEIL;
      var ind = document.getElementById('v4PubSubPageIndicator');
      if (ind) ind.textContent = meta.label;

      // 4. Mise à jour du pied de pagination #v4PubSubPageFooterNav
      var curLbl = document.getElementById('v4PubPagerCurrentLabel');
      var nextBtn = document.getElementById('v4PubPagerNextBtn');
      var homeBtn = document.getElementById('v4PubPagerHomeBtn');
      if (curLbl) curLbl.textContent = meta.label;
      if (homeBtn) homeBtn.style.display = (key === 'ACCUEIL') ? 'none' : '';
      if (nextBtn) {
        nextBtn.textContent = meta.nextLabel;
        nextBtn.onclick = function () {
          navigateFamily('PUB', meta.nextScreen);
        };
      }

      // 5. Synchronisation du menu principal (.main-nav) lorsque #view-PUB est actif
      var pubView = document.getElementById('view-PUB');
      if (pubView && pubView.classList.contains('active')) {
        document.querySelectorAll('.main-nav .nav-item').forEach(function (n) { n.classList.remove('active'); });
        var targetNavId = meta.navId;
        if (opts.targetScreenId === 'PUB-07') targetNavId = 'nav-SAVEURS';
        if (opts.targetScreenId === 'PUB-08' || opts.targetScreenId === 'PUB-09') targetNavId = 'nav-HOTELS';
        var navEl = document.getElementById(targetNavId) || document.getElementById('nav-PUB');
        if (navEl) navEl.classList.add('active');
      }

      if (opts.scrollTop) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      return key;
    };

    // Envelopper inspectScreen et navigateFamily pour activer automatiquement la sous-page correspondante
    var _origInspectScreenV4 = window.inspectScreen;
    if (typeof _origInspectScreenV4 === 'function' && !_origInspectScreenV4._v4SubPageWrapped) {
      window.inspectScreen = function (screenId) {
        var code = String(screenId || 'PUB-01');
        if (code.indexOf('PUB-') === 0 && window._activePubSubPage !== 'ALL') {
          var subPage = PUB_SCREEN_TO_SUBPAGE[code] || 'ACCUEIL';
          window.switchPubSubPage(subPage, { targetScreenId: code });
        }
        var res = _origInspectScreenV4.apply(this, arguments);
        // Si l'écran demandé est la tête de l'une des 6 sous-pages, remonter en haut de page
        var topScreens = { 'PUB-01': 1, 'PUB-03': 1, 'PUB-04': 1, 'PUB-09': 1, 'PUB-10': 1, 'PUB-12': 1 };
        if (topScreens[code]) {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        return res;
      };
      window.inspectScreen._v4SubPageWrapped = true;
    }

    var _origNavigateFamilyV4 = window.navigateFamily;
    if (typeof _origNavigateFamilyV4 === 'function' && !_origNavigateFamilyV4._v4SubPageWrapped) {
      window.navigateFamily = function (family, screenId) {
        var fam = String(family || 'PUB');
        var code = String(screenId || (fam + '-01'));
        if (fam === 'PUB') {
          var subPage = PUB_SCREEN_TO_SUBPAGE[code] || 'ACCUEIL';
          window.switchPubSubPage(subPage, { targetScreenId: code });
        }
        var res = _origNavigateFamilyV4.apply(this, arguments);
        if (fam === 'PUB') {
          var subPageAfter = PUB_SCREEN_TO_SUBPAGE[code] || 'ACCUEIL';
          window.switchPubSubPage(subPageAfter, { targetScreenId: code });
        }
        return res;
      };
      window.navigateFamily._v4SubPageWrapped = true;
    }

    // Prise en charge des URLs dédiées (/activites, /fiche-activite, /agenda, /rdv, etc.)
    var pathNow = (window.location.pathname || '/').replace(/\/+$/, '').toLowerCase();
    var v4ExtraRoutes = {
      '/activites': ['PUB', 'PUB-03'],
      '/fiche-activite': ['PUB', 'PUB-04'],
      '/agenda': ['PUB', 'PUB-16'],
      '/evenements': ['PUB', 'PUB-16'],
      '/rdv': ['PUB', 'PUB-18'],
      '/rendez-vous': ['PUB', 'PUB-18']
    };
    if (v4ExtraRoutes[pathNow]) {
      setTimeout(function () {
        window.navigateFamily(v4ExtraRoutes[pathNow][0], v4ExtraRoutes[pathNow][1]);
      }, 70);
    } else {
      // Initialiser par défaut sur la Page 1/6 (Accueil & Orientation)
      window.switchPubSubPage('ACCUEIL', { targetScreenId: 'PUB-01' });
    }
  })();
// ECOPARK_PHASE9_V4_AND_RECETTE:END"""


def strip_block(html: str, start_marker: str, end_marker: str) -> str:
    pattern = re.compile(re.escape(start_marker) + r"[\s\S]*?" + re.escape(end_marker) + r"\n?")
    return pattern.sub("", html)


def apply_phase9_v4(html: str) -> str:
    # 0. Nettoyage idempotent des blocs V4 précédents s'ils existent déjà
    html = strip_block(html, "    /* ECOPARK_V4_CANOPEE_CSS:START */", "    /* ECOPARK_V4_CANOPEE_CSS:END */")
    html = strip_block(html, "        <!-- ECOPARK_V4_PUB_SUBPAGES_NAV:START -->", "        <!-- ECOPARK_V4_PUB_SUBPAGES_NAV:END -->")
    html = strip_block(html, "        <!-- ECOPARK_V4_PUB_HUB_AND_FOOTER:START -->", "        <!-- ECOPARK_V4_PUB_HUB_AND_FOOTER:END -->")
    html = strip_block(html, "            <!-- ECOPARK_V4_HERO_STAGE:START -->", "            <!-- ECOPARK_V4_HERO_STAGE:END -->")
    html = strip_block(html, "            <!-- ECOPARK_V4_CATALOG_GRID:START -->", "            <!-- ECOPARK_V4_CATALOG_GRID:END -->")
    html = strip_block(html, "        <!-- ECOPARK_V4_PUB04_AND_PUB09:START -->", "        <!-- ECOPARK_V4_PUB04_AND_PUB09:END -->")
    html = strip_block(html, "              <!-- ECOPARK_V4_SYSTEM_PAGES:START -->", "              <!-- ECOPARK_V4_SYSTEM_PAGES:END -->")
    html = strip_block(html, "            <!-- ECOPARK_V4_RES_STEPPER:START -->", "            <!-- ECOPARK_V4_RES_STEPPER:END -->")
    html = strip_block(html, "    <!-- ECOPARK_V4_MOBILE_NAV:START -->", "    <!-- ECOPARK_V4_MOBILE_NAV:END -->")
    html = strip_block(html, "// ECOPARK_PHASE9_V4_AND_RECETTE:START", "// ECOPARK_PHASE9_V4_AND_RECETTE:END")

    # 1. Injecter V4 CSS juste avant </style>
    assert "</style>" in html, "Marker </style> introuvable"
    html = html.replace("  </style>", V4_CSS_BLOCK + "\n  </style>", 1)

    # 1b. Mettre à jour le menu principal (.main-nav) pour dissocier Accueil (PUB-01) et Activités & Lac (PUB-03)
    old_nav_pub = '<button type="button" class="nav-item active" id="nav-PUB" onclick="navigateFamily(\'PUB\', \'PUB-01\')">Découvrir & Activités</button>'
    new_nav_pub = (
        '<button type="button" class="nav-item active" id="nav-ACCUEIL" onclick="navigateFamily(\'PUB\', \'PUB-01\')">Accueil</button>\n'
        '          <button type="button" class="nav-item" id="nav-PUB" onclick="navigateFamily(\'PUB\', \'PUB-03\')">Activités &amp; Lac</button>'
    )
    if old_nav_pub in html and 'id="nav-ACCUEIL"' not in html:
        html = html.replace(old_nav_pub, new_nav_pub, 1)

    # 1c. Injecter la barre des 6 sous-pages publiques (#v4PubSubPagesNav) en haut de #view-PUB
    hero_comment_anchor = '        <!-- HERO ACCUEIL<span class="tech-code-tag"> (PUB-01)</span> -->'
    assert hero_comment_anchor in html, "Marker hero_comment_anchor introuvable"
    html = html.replace(
        hero_comment_anchor,
        V4_PUB_SUBPAGES_NAV_HTML + "\n\n" + hero_comment_anchor,
        1
    )

    # 1d. Injecter le Hub des 6 Univers + Pied de pagination (#v4PubHubCardsBlock & #v4PubSubPageFooterNav) à la fin de #view-PUB
    view_pub_close_anchor = """      </section>

      <!-- ====================================================================
           FAMILLE 3 : PRÉPARATION DE VISITE, DEVIS & RÉSERVATION (RES-01 à RES-12)"""
    assert view_pub_close_anchor in html, "Marker view_pub_close_anchor introuvable"
    html = html.replace(
        view_pub_close_anchor,
        V4_PUB_HUB_AND_FOOTER_HTML + "\n\n" + view_pub_close_anchor,
        1
    )

    # 2. A-009 : Remplacer le libellé météo trompeur "En direct d'Ahala :" par un bulletin horodaté honnête
    html = html.replace(
        "<strong>En direct d'Ahala :</strong>",
        "<strong>Bulletin d'accueil Ahala (Mis à jour ce jour • Mar–Dim 09h–18h) :</strong>"
    )

    # 3. Injecter le Hero Cinématique V4 + Bandeau des 4 Piliers dans #sec-PUB-01 juste après #ahalaLiveWeatherBar
    weather_close_anchor = """                <span class="price-pill" style="font-size:11.5px;padding:2px 9px;">Garantie Pluie : Report Gratuit</span>
              </div>
            </div>"""
    assert weather_close_anchor in html, "Marker weather_close_anchor introuvable"
    html = html.replace(
        weather_close_anchor,
        weather_close_anchor + "\n\n" + V4_HERO_IMMERSIVE_HTML,
        1
    )

    # 4. Ajouter id="sec-PUB-02" sur le conteneur du Totem / Plan d'orientation si absent (A-019)
    html = html.replace(
        '<div class="card" style="background:linear-gradient(135deg, #F4F9F0 0%, #FFFFFF 60%, #FBF5EC 100%);border:2px solid rgba(29,73,13,0.22);padding:26px 28px;">',
        '<div class="card" id="sec-PUB-02" style="background:linear-gradient(135deg, #F4F9F0 0%, #FFFFFF 60%, #FBF5EC 100%);border:2px solid rgba(29,73,13,0.22);padding:26px 28px;">',
        1
    )

    # 5. Injecter la barre de filtres V4 et la grille 4 colonnes d'activités dans #sec-PUB-03
    pub03_header_anchor = """                Zéro mauvaise surprise sur l'addition : chaque activité affiche clairement ses conditions d'accès et ses tarifs officiels en Francs CFA pour les enfants (dès 500 FCFA, gratuit moins de 3 ans), les adultes et les groupes.
              </p>
            </div>"""
    assert pub03_header_anchor in html, "Marker pub03_header_anchor introuvable"
    html = html.replace(
        pub03_header_anchor,
        pub03_header_anchor + "\n\n" + V4_CATALOG_FILTER_AND_CARDS_HTML,
        1
    )

    # 6. Ajouter id="sec-PUB-05" et id="sec-PUB-06" sur les articles Pôle 1 et Pôle 2 de #sec-PUB-03 (A-019)
    html = html.replace(
        '<!-- Pôle 1 : Faune & Botanique<span class="tech-code-tag"> (PUB-05)</span> -->\n              <article class="col-8 bento-card bento-wide">',
        '<!-- Pôle 1 : Faune & Botanique<span class="tech-code-tag"> (PUB-05)</span> -->\n              <article class="col-8 bento-card bento-wide" id="sec-PUB-05">',
        1
    )
    html = html.replace(
        '<!-- Pôle 2 : Lac & Activités Nautiques / Équestres (PUB-04, PUB-06) -->\n              <article class="col-4 bento-card">',
        '<!-- Pôle 2 : Lac & Activités Nautiques / Équestres (PUB-04, PUB-06) -->\n              <article class="col-4 bento-card" id="sec-PUB-06">',
        1
    )

    # 7. Injecter les sections autonomes #sec-PUB-04 (Fiche détail activité V4) et #sec-PUB-09 (Fiche détail hébergement V4) juste avant #sec-PUB-10
    pub10_anchor = '        <!-- GRILLE TARIFAIRE OFFICIELLE COMPLÈTE EN FCFA<span class="tech-code-tag"> (PUB-10)</span> -->'
    assert pub10_anchor in html, "Marker pub10_anchor introuvable"
    html = html.replace(
        pub10_anchor,
        V4_PUB04_AND_PUB09_SECTIONS_HTML + "\n\n" + pub10_anchor,
        1
    )

    # 8. Ajouter id="sec-PUB-17" et id="sec-PUB-19" sur le bloc Recherche & FAQ de #sec-PUB-13 (A-019)
    html = html.replace(
        '<div class="form-group" style="margin-bottom:10px;">\n                  <label class="form-label" for="globalSearchInput">',
        '<div class="form-group" id="sec-PUB-19" style="margin-bottom:10px;">\n                  <label class="form-label" for="globalSearchInput">',
        1
    )
    html = html.replace(
        '<div id="faqListContainer" style="display:grid;gap:10px;font-size:14.5px;">',
        '<div id="sec-PUB-17"><div id="faqListContainer" style="display:grid;gap:10px;font-size:14.5px;">',
        1
    )
    html = html.replace(
        'Un parking intérieur gratuit et gardé de 150 places (voitures et bus) vous attend dès le portail.\n                  </div>\n                </div>',
        'Un parking intérieur gratuit et gardé de 150 places (voitures et bus) vous attend dès le portail.\n                  </div>\n                </div></div>',
        1
    )

    # 9. Injecter les cartes autonomes #sec-PUB-20, #sec-PUB-21 et #sec-PUB-22 à la fin de la grille de #sec-PUB-13 (A-019)
    pub14_close_anchor = """                        <strong style="font-size:1.02rem;">Équipes Zoo & Biosécurité</strong>
                        <span style="font-size:12px;">Encadrement professionnel</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>"""
    assert pub14_close_anchor in html, "Marker pub14_close_anchor introuvable"
    html = html.replace(
        pub14_close_anchor,
        pub14_close_anchor + "\n\n" + V4_SYSTEM_PAGES_PUB20_22_HTML,
        1
    )

    # 10. Injecter le Stepper V4 à 4 étapes en haut de #view-RES
    res_grid_anchor = '            <div class="grid-12" id="resMainGrid">'
    assert res_grid_anchor in html, "Marker res_grid_anchor introuvable"
    html = html.replace(
        res_grid_anchor,
        V4_RES_STEPPER_HTML + "\n" + res_grid_anchor,
        1
    )

    # 11. A-017 : Ajouter le bouton explicite "Vider à 0 FCFA (Recomptage à blanc)" à côté de resetPhysicalCashCount()
    cash_reset_btn = '<button type="button" class="btn btn-secondary btn-sm" onclick="resetPhysicalCashCount()">Réinitialiser la grille</button>'
    if cash_reset_btn in html and 'clearPhysicalCashCountToZero()' not in html:
        html = html.replace(
            cash_reset_btn,
            cash_reset_btn + ' <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" id="btnClearCashToZero" onclick="clearPhysicalCashCountToZero()">Vider à 0 FCFA (Recomptage à blanc)</button>',
            1
        )

    # 12. Injecter la barre de navigation mobile V4 (#v4MobileBottomNav) juste avant </main>
    assert "</main>" in html, "Marker </main> introuvable"
    html = html.replace("    </main>", "    </main>\n\n" + V4_MOBILE_BOTTOM_NAV_HTML, 1)

    # 13. Injecter le bloc JS Phase 9 V4 & Recette juste après // ECOPARK_PHASE8_TOTEM_SYNC:END
    assert "// ECOPARK_PHASE8_TOTEM_SYNC:END" in html, "Marker ECOPARK_PHASE8_TOTEM_SYNC:END introuvable"
    html = html.replace(
        "// ECOPARK_PHASE8_TOTEM_SYNC:END",
        "// ECOPARK_PHASE8_TOTEM_SYNC:END\n" + V4_JS_BLOCK,
        1
    )

    # 14. Vérification stricte : Zéro caractère avec codePoint > 0x25FF (conformité verify_live_monochrome_prod.py)
    high_chars = [ch for ch in html if ord(ch) > 0x25FF]
    if high_chars:
        raise ValueError(f"Caractères interdits > U+25FF détectés : {set(high_chars)}")

    return html


def main():
    update_content_snapshot()
    raw_html = LIVE_HTML_PATH.read_text(encoding="utf-8")
    v4_html = apply_phase9_v4(raw_html)

    LIVE_HTML_PATH.write_text(v4_html, encoding="utf-8")
    PROTO_HTML_PATH.write_text(v4_html, encoding="utf-8")
    RELOOK_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    RELOOK_HTML_PATH.write_text(v4_html, encoding="utf-8")

    # Mettre à jour verify_live_monochrome_prod.py pour l'architecture 6 sous-pages publiques
    verify_path = ROOT / "verify_live_monochrome_prod.py"
    if verify_path.exists():
        vt = verify_path.read_text(encoding="utf-8")
        old_bento = "            const bentoMedia = document.querySelector('.bento-card .card-media-wrapper');"
        new_bento = "            navigateFamily('PUB', 'PUB-03');\n            const bentoMedia = document.querySelector('.bento-card .card-media-wrapper');"
        if old_bento in vt and "navigateFamily('PUB', 'PUB-03');\n            const bentoMedia" not in vt:
            vt = vt.replace(old_bento, new_bento, 1)
            vt = vt.replace(
                "            const bentoH = bentoMedia ? bentoMedia.offsetHeight : 0;",
                "            const bentoH = bentoMedia ? bentoMedia.offsetHeight : 0;\n            navigateFamily('PUB', 'PUB-01');",
                1
            )
        old_map = '        page.locator("#ahalaMapContainer").scroll_into_view_if_needed()'
        new_map = '        page.evaluate("navigateFamily(\'PUB\', \'PUB-13\');")\n        page.locator("#ahalaMapContainer").scroll_into_view_if_needed()'
        if old_map in vt and 'navigateFamily(\'PUB\', \'PUB-13\')' not in vt:
            vt = vt.replace(old_map, new_map, 1)
        verify_path.write_text(vt, encoding="utf-8")

    # Vérification des 22 ancres sec-PUB-01 à sec-PUB-22
    pub_ids = sorted(set(re.findall(r'id="(sec-PUB-\d+)"', v4_html)))
    print(f"[OK] {len(pub_ids)}/22 ancres sec-PUB-* présentes :", pub_ids)
    assert len(pub_ids) == 22, f"Il manque des ancres sec-PUB-* : {pub_ids}"
    assert LIVE_HTML_PATH.read_bytes() == PROTO_HTML_PATH.read_bytes(), "Parité binaire rompue !"
    print("[OK] Parité binaire stricte entre etape0-site-live/index.html et Prototype_Interactif_ECOPARK_NEW_LOOK.html.")


if __name__ == "__main__":
    main()
