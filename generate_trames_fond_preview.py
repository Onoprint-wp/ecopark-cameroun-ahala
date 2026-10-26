# -*- coding: utf-8 -*-
"""
Générateur des visuels de validation pour la Gestion des Trames de Fond (Architecture en 3 Plans de Lumière) :
1. Trame 1 — Blanc Lumière (#FFFFFF) + Filigrane Vectoriel « Le Cercle du Vivant » (opacité 4.5 %) sur le Hero (#sec-PUB-01)
2. Trame 2 — Sauge Tendre (#EDF4E7) + Cartes Bento Blanc Pur (#FFFFFF) sans bordures (#sec-PUB-03)
3. Trame 3 (Option A — Approche Keynote Apple) — « Canopée Profonde » (#142E0B / #1D490D + halo radial émeraude) sur #sec-PUB-10
4. Trame 3 (Option B — Approche Hospitalité Organique) — « Sable Raphia / Pierre Chaude » (#F6F4EE) sur #sec-PUB-10
"""

import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "etape0-site-live" / "index.html"
TRAME_HTML = ROOT / "Preview_Trames_De_Fond_ECOPARK.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\a7ec3e06-7022-4aad-b64e-501927169ab1")
LOCAL_QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"

# Filigrane vectoriel SVG « Le Cercle du Vivant » (Rosace géométrique à 8 feuilles inspirée du logo ECOPARK)
BOTANICAL_ROSETTE_SVG = """
<div class="cercle-vivant-watermark" aria-hidden="true">
  <svg viewBox="0 0 400 400" fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="200" cy="200" r="185" stroke-dasharray="4 6" />
    <circle cx="200" cy="200" r="140" />
    <circle cx="200" cy="200" r="85" />
    <g transform="translate(200,200)">
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(45)" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(90)" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(135)" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(180)" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(225)" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(270)" />
      <path d="M0,0 C-28,-55 -28,-125 0,-175 C28,-125 28,-55 0,0 Z" transform="rotate(315)" />
    </g>
  </svg>
</div>
"""

TRAMES_CSS = """
    /* ==========================================================================
       ARCHITECTURE DES TRAMES DE FOND EN 3 PLANS DE LUMIÈRE
       1. Blanc Lumière (#FFFFFF) + Filigrane « Le Cercle du Vivant » (4.5%)
       2. Sauge Tendre (#EDF4E7) + Cartes Bento Blanc Pur (#FFFFFF)
       3. Troisième Trame :
          - Option A (Keynote Apple) : Canopée Profonde (#142E0B)
          - Option B (Hospitalité Organique) : Sable Raphia (#F6F4EE)
       ========================================================================== */
    :root {
      --color-surface-canopy-dark: #142E0B;
      --color-surface-warm-sand: #F6F4EE;
    }

    .section {
      position: relative;
      overflow: hidden;
      padding: 68px 0;
    }

    /* Filigrane vectoriel « Le Cercle du Vivant » */
    .cercle-vivant-watermark {
      position: absolute;
      right: -90px;
      top: -70px;
      width: 560px;
      height: 560px;
      color: var(--color-brand-deep);
      opacity: 0.055;
      pointer-events: none;
      z-index: 0;
    }
    .section > .container {
      position: relative;
      z-index: 1;
    }

    /* Trame 2 : Sauge Tendre (#EDF4E7) avec halo radial subtil */
    .section-soft {
      background: radial-gradient(circle at 12% 10%, rgba(255, 255, 255, 0.65) 0%, rgba(237, 244, 231, 1) 65%);
      background-color: var(--color-surface-soft);
    }

    /* Trame 3 — OPTION A : « Canopée Profonde » (#142E0B — Effet Keynote Apple) */
    .section-canopy-dark {
      background:
        radial-gradient(circle at 85% 18%, rgba(31, 136, 11, 0.28) 0%, transparent 55%),
        radial-gradient(circle at 10% 85%, rgba(29, 73, 13, 0.45) 0%, transparent 60%),
        #142E0B !important;
      color: #FFFFFF !important;
    }
    .section-canopy-dark .cercle-vivant-watermark {
      color: #FFFFFF;
      opacity: 0.06;
      left: -120px;
      right: auto;
      bottom: -120px;
      top: auto;
    }
    .section-canopy-dark .eyebrow {
      color: #82D672 !important;
    }
    .section-canopy-dark h2,
    .section-canopy-dark h3 {
      color: #FFFFFF !important;
    }
    .section-canopy-dark .tonal-muted {
      color: rgba(207, 224, 197, 0.58) !important;
    }
    .section-canopy-dark .section-header p {
      color: rgba(237, 244, 231, 0.82) !important;
    }
    .section-canopy-dark .table-responsive {
      background: #FFFFFF !important;
      border-radius: 24px !important;
      border: 1px solid rgba(255, 255, 255, 0.16) !important;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28) !important;
      overflow: hidden;
    }
    .section-canopy-dark table td {
      color: var(--color-text) !important;
    }

    /* Trame 3 — OPTION B : « Sable Raphia / Pierre Chaude » (#F6F4EE — Hospitalité Organique) */
    .section-warm-sand {
      background:
        radial-gradient(circle at 80% 15%, rgba(255, 255, 255, 0.85) 0%, rgba(246, 244, 238, 1) 70%) !important;
      background-color: var(--color-surface-warm-sand) !important;
      border-top: 1px solid rgba(29, 73, 13, 0.06);
      border-bottom: 1px solid rgba(29, 73, 13, 0.06);
    }
    .section-warm-sand .cercle-vivant-watermark {
      color: #1D490D;
      opacity: 0.045;
      left: -100px;
      right: auto;
      top: -80px;
    }
    .section-warm-sand .table-responsive {
      background: #FFFFFF !important;
      border-radius: 24px !important;
      border: none !important;
      box-shadow: 0 18px 48px rgba(29, 73, 13, 0.07) !important;
      overflow: hidden;
    }
    .section-warm-sand th {
      background: #EFECE3 !important;
      color: var(--color-brand-deep) !important;
    }
"""

def build_and_capture():
    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Injecter les styles de trames de fond
    if "ARCHITECTURE DES TRAMES DE FOND" not in html:
        html = html.replace("</style>", TRAMES_CSS + "\n  </style>", 1)

    # 2. Ajouter le filigrane « Le Cercle du Vivant » dans le Hero (#sec-PUB-01) et dans #sec-PUB-10
    html = html.replace(
        '<div class="section" id="sec-PUB-01">\n          <div class="container">',
        f'<div class="section" id="sec-PUB-01">\n          {BOTANICAL_ROSETTE_SVG}\n          <div class="container">',
        1
    )
    html = html.replace(
        '<div class="section" id="sec-PUB-10">\n          <div class="container">',
        f'<div class="section section-canopy-dark" id="sec-PUB-10">\n          {BOTANICAL_ROSETTE_SVG}\n          <div class="container">',
        1
    )
    # Ajouter le contraste tonal sur le titre H2 de #sec-PUB-10
    html = html.replace(
        "<h2>Grille Tarifaire Officielle ECOPARK Yaoundé-Ahala</h2>",
        '<h2><span class="tonal-muted">Tous nos tarifs en toute clarté.</span> Grille Officielle en Francs CFA.</h2>',
        1
    )

    TRAME_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Preview Trames de Fond ecrite : {TRAME_HTML}")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_QA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        page.goto(TRAME_HTML.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)

        # Capture 1 : Trame 1 — Blanc Lumière (#FFFFFF) + Filigrane Vectoriel « Le Cercle du Vivant » + Cartes KPI Sauge (#EDF4E7)
        s1 = ARTIFACT_DIR / "trame_validation_1_hero_filigrane_botanique.png"
        page.screenshot(path=str(s1), full_page=False)
        (LOCAL_QA_DIR / s1.name).write_bytes(s1.read_bytes())

        # Capture 2 : Trame 2 — Sauge Tendre (#EDF4E7) + Cartes Bento Blanc Pur (#FFFFFF) en inversion Figure/Fond
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-03').offsetTop - 75);")
        page.wait_for_timeout(350)
        s2 = ARTIFACT_DIR / "trame_validation_2_sauge_bento_inversion.png"
        page.screenshot(path=str(s2), full_page=False)
        (LOCAL_QA_DIR / s2.name).write_bytes(s2.read_bytes())

        # Capture 3 : Trame 3 (Option A — Approche Keynote Apple) — « Canopée Profonde » (#142E0B) sur #sec-PUB-10
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-10').offsetTop - 75);")
        page.wait_for_timeout(350)
        s3 = ARTIFACT_DIR / "trame_validation_3_optionA_canopee_profonde.png"
        page.screenshot(path=str(s3), full_page=False)
        (LOCAL_QA_DIR / s3.name).write_bytes(s3.read_bytes())

        # Capture 4 : Trame 3 (Option B — Approche Hospitalité Organique) — « Sable Raphia / Pierre Chaude » (#F6F4EE) sur #sec-PUB-10
        page.evaluate("""() => {
            const sec = document.getElementById('sec-PUB-10');
            sec.classList.remove('section-canopy-dark');
            sec.classList.add('section-warm-sand');
            window.scrollTo(0, sec.offsetTop - 75);
        }""")
        page.wait_for_timeout(350)
        s4 = ARTIFACT_DIR / "trame_validation_4_optionB_sable_raphia.png"
        page.screenshot(path=str(s4), full_page=False)
        (LOCAL_QA_DIR / s4.name).write_bytes(s4.read_bytes())

        browser.close()
    print("[OK] 4 captures de validation des Trames de Fond generees avec succes.")

if __name__ == "__main__":
    build_and_capture()
