# -*- coding: utf-8 -*-
"""
Générateur des visuels de validation pour la 3e Couleur :
Triade Chromatique 60-30-10 :
- 60 % : Blanc Lumière (#FFFFFF) & Neutres (#1E281B)
- 30 % : Vert Canopée (#1D490D / #EDF4E7) — Nature, Faune, Eau, Confiance
- 10 % : Ocre Bronze / Terre d'Ahala (#C47D2B / texte #9A5B13 / surface douce #FBF5EC) — Valeur FCFA, Hospitalité, Gastronomie
"""

import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "etape0-site-live" / "index.html"
OCRE_HTML = ROOT / "Preview_Troisieme_Couleur_Ocre_Bronze.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\a7ec3e06-7022-4aad-b64e-501927169ab1")
LOCAL_QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"

OCRE_BRONZE_CSS = """
    /* ==========================================================================
       TRIADE CHROMATIQUE 60-30-10 AVEC LA 3e COULEUR : OCRE BRONZE / TERRE D'AHALA
       - 60 % : Blanc Lumière (#FFFFFF)
       - 30 % : Vert Canopée (#1D490D / #EDF4E7)
       - 10 % : Ocre Bronze / Terre d'Ahala (#C47D2B / #9A5B13 / #FBF5EC)
       ========================================================================== */
    :root {
      --color-accent-ochre: #C47D2B;
      --color-accent-ochre-deep: #9A5B13;
      --color-accent-ochre-soft: #FBF5EC;
      --color-accent-ochre-border: rgba(196, 125, 43, 0.32);
    }

    /* 1. Pilules de prix en FCFA (.price-pill) mises en valeur par l'Ocre Bronze */
    .price-pill {
      background-color: var(--color-accent-ochre-soft) !important;
      color: var(--color-accent-ochre-deep) !important;
      border: 1px solid var(--color-accent-ochre-border) !important;
      border-radius: var(--radius-pill) !important;
      padding: 5px 14px !important;
      font-weight: 600 !important;
      box-shadow: 0 2px 6px rgba(196, 125, 43, 0.08);
    }

    /* 2. Bouton "Devis École / Groupe" dans l'en-tête distingué en Ocre Bronze */
    .btn-ochre-outline {
      background-color: var(--color-accent-ochre-soft) !important;
      color: var(--color-accent-ochre-deep) !important;
      border: 1px solid var(--color-accent-ochre-border) !important;
    }
    .btn-ochre-outline:hover {
      background-color: var(--color-accent-ochre) !important;
      color: #FFFFFF !important;
      border-color: var(--color-accent-ochre) !important;
    }

    /* 3. Filet d'onglet actif réchauffé d'une touche Ocre Bronze */
    .nav-item.active {
      background: var(--color-surface-soft) !important;
      color: var(--color-brand-deep) !important;
      box-shadow: inset 0 -2.5px 0 var(--color-accent-ochre) !important;
    }

    /* 4. Sur-titres (eyebrows) et médaillons des univers Hospitalité, Saveurs & Événements */
    .eyebrow-hospitality {
      color: var(--color-accent-ochre-deep) !important;
    }
    .medallion-hospitality {
      background-color: var(--color-accent-ochre-soft) !important;
      color: var(--color-accent-ochre-deep) !important;
      border: 1px solid var(--color-accent-ochre-border) !important;
    }

    /* 5. Carte KPI Hôtellerie dans le Hero & Badge Billet QR Prestige */
    .kpi-card-hospitality {
      background-color: var(--color-accent-ochre-soft) !important;
      border: 1px solid rgba(196, 125, 43, 0.22) !important;
    }
    .kpi-card-hospitality strong {
      color: var(--color-accent-ochre-deep) !important;
    }

    .badge-qr-prestige {
      background-color: var(--color-accent-ochre-soft) !important;
      color: var(--color-accent-ochre-deep) !important;
      border: 1px solid var(--color-accent-ochre-border) !important;
    }
"""

def build_and_capture():
    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Injecter le CSS de la 3e couleur Ocre Bronze
    if "TRIADE CHROMATIQUE 60-30-10 AVEC LA 3e COULEUR" not in html:
        html = html.replace("</style>", OCRE_BRONZE_CSS + "\n  </style>", 1)

    # 2. Appliquer la classe .btn-ochre-outline sur le bouton "Devis École / Groupe" du header
    html = html.replace(
        '<button type="button" class="btn btn-secondary btn-sm" onclick="openQuoteModalSprint1()">Devis École / Groupe</button>',
        '<button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openQuoteModalSprint1()">Devis École / Groupe</button>',
        1
    )

    # 3. Appliquer .kpi-card-hospitality sur la 3e carte KPI du Hero (Séjour Loges Bene, Chanthel & Ewondo)
    html = html.replace(
        '<div class="col-4 card" style="padding:14px;background:var(--color-surface-soft);">\n                    <strong style="color:var(--color-brand-deep);font-family:var(--font-heading);font-size:1.25rem;">10 000 – 30 000 FCFA</strong>\n                    <span style="font-size:14px;">Séjour Loges Bene, Chanthel & Ewondo</span>\n                  </div>',
        '<div class="col-4 card kpi-card-hospitality" style="padding:14px;">\n                    <strong style="font-family:var(--font-heading);font-size:1.25rem;">10 000 – 30 000 FCFA</strong>\n                    <span style="font-size:14px;">Séjour Loges Bene, Chanthel & Ewondo</span>\n                  </div>',
        1
    )

    # 4. Appliquer .eyebrow-hospitality sur les pôles Gastronomie (PUB-07), Hébergement (PUB-08/09) et Événements (PUB-11)
    html = html.replace(
        'Gastronomie & Événements</span>',
        'Gastronomie & Événements</span>'.replace('Gastronomie', '<span class="eyebrow-hospitality">Gastronomie') + '</span>',
        1
    )
    html = html.replace(
        'Hébergement & Séjour</span>',
        '<span class="eyebrow-hospitality">Hébergement & Séjour</span></span>',
        1
    )
    html = html.replace(
        'Groupes & Séminaires</span>',
        '<span class="eyebrow-hospitality">Groupes & Séminaires</span></span>',
        1
    )

    # 5. Appliquer .badge-qr-prestige sur le badge du Billet Électronique ECOPARK
    html = html.replace(
        'Billet Électronique ECOPARK</span>',
        'Billet Électronique ECOPARK</span>',
        1
    )
    html = html.replace(
        '<span class="status-badge status-neutral" style="font-weight:600;">',
        '<span class="status-badge badge-qr-prestige" style="font-weight:600;">',
        1
    )

    OCRE_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Preview 3e Couleur Ocre Bronze ecrite : {OCRE_HTML}")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_QA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        page.goto(OCRE_HTML.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)

        # Capture 1 : Hero & Header avec la Triade 60-30-10 (Blanc + Vert Canopée + Ocre Bronze sur le bouton Devis Groupe, le filet actif et la carte Séjour Loges)
        s1 = ARTIFACT_DIR / "ocre_validation_1_hero_triade.png"
        page.screenshot(path=str(s1), full_page=False)
        (LOCAL_QA_DIR / s1.name).write_bytes(s1.read_bytes())

        # Capture 2 : Bento Grid des Univers (Lignes 2 & 3 : Gastronomie Le Château des Saveurs, Loges Ewondo/Chanthel/Bene, Groupes & CFP avec Price Pills et Eyebrows en Ocre Bronze)
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-03').offsetTop + 460);")
        page.wait_for_timeout(350)
        s2 = ARTIFACT_DIR / "ocre_validation_2_bento_univers_hospitalite_prix.png"
        page.screenshot(path=str(s2), full_page=False)
        (LOCAL_QA_DIR / s2.name).write_bytes(s2.read_bytes())

        # Capture 3 : Grille Tarifaire Officielle en FCFA (#sec-PUB-10) avec Price Pills en Ocre Bronze
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-10').offsetTop - 85);")
        page.wait_for_timeout(350)
        s3 = ARTIFACT_DIR / "ocre_validation_3_grille_tarifaire_fcfa.png"
        page.screenshot(path=str(s3), full_page=False)
        (LOCAL_QA_DIR / s3.name).write_bytes(s3.read_bytes())

        # Capture 4 : Simulateur FCFA & Billet Électronique QR avec Badge Prestige Ocre Bronze
        page.evaluate("navigateFamily('RES', 'RES-03'); window.scrollTo(0, 620);")
        page.wait_for_timeout(350)
        s4 = ARTIFACT_DIR / "ocre_validation_4_simulateur_billet_qr_prestige.png"
        page.screenshot(path=str(s4), full_page=False)
        (LOCAL_QA_DIR / s4.name).write_bytes(s4.read_bytes())

        browser.close()
    print("[OK] 4 captures de validation de la 3e couleur (Ocre Bronze) generees avec succes.")

if __name__ == "__main__":
    build_and_capture()
