# -*- coding: utf-8 -*-
"""
Générateur de l'aperçu visuel « Apple-Grade × Canopée Vivante » (Version v3 — Finition chirurgicale)
Corrections v3 :
1. En-tête Liquid Glass strictement sur 1 seule ligne horizontale sur Desktop (@media min-width: 1080px).
2. Masquage global en mode visiteur normal de toutes les barres techniques .subnav-bar et de tous les codes (RES-01, PUB-05, etc.) entourés ou non de backticks.
3. Cadrage parfait des 4 captures haute définition pour l'artefact de validation.
"""

import pathlib
import re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "etape0-site-live" / "index.html"
PREVIEW_HTML = ROOT / "Preview_Apple_Grade_ECOPARK.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\a7ec3e06-7022-4aad-b64e-501927169ab1")
LOCAL_QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"

APPLE_GRADE_CSS_OVERRIDES = """
    /* ==========================================================================
       RAFFINEMENT VISUEL « APPLE-GRADE × CANOPÉE VIVANTE » (V3 FINITION)
       Respect strict de la palette #FFFFFF / #1D490D / #1F880B / #EDF4E7 / #1E281B
       et des polices Barlow Semi Condensed + Source Sans 3
       ========================================================================== */
    :root {
      --radius-sm: 14px;
      --radius-md: 24px;
      --radius-lg: 28px;
      --radius-pill: 980px;
      --shadow-card: 0 14px 40px rgba(29, 73, 13, 0.06);
      --shadow-elevated: 0 24px 60px rgba(29, 73, 13, 0.12);
    }

    /* 1. Typographie Monumentale Semibold (600) & Contraste Tonal façon Apple */
    h1, h2, h3, .heading-font {
      font-weight: 600 !important;
      letter-spacing: -0.02em;
    }
    h1 {
      font-size: clamp(2.75rem, 4.8vw, 4.15rem) !important;
      line-height: 1.04 !important;
      letter-spacing: -0.024em !important;
    }
    h2 {
      font-size: clamp(2.1rem, 3.6vw, 3.1rem) !important;
      line-height: 1.07 !important;
      letter-spacing: -0.018em !important;
    }
    h3 {
      font-size: clamp(1.32rem, 2.0vw, 1.62rem) !important;
      line-height: 1.15 !important;
      letter-spacing: -0.01em !important;
    }
    .tonal-muted {
      color: rgba(29, 73, 13, 0.50);
      font-weight: 600;
    }
    .lead-editorial {
      font-size: 1.2rem !important;
      font-weight: 600 !important;
      line-height: 1.42 !important;
      color: rgba(30, 40, 27, 0.62) !important;
      letter-spacing: -0.01em;
    }
    .lead-editorial strong {
      color: var(--color-text) !important;
      font-weight: 600 !important;
    }

    /* 2. En-tête « Liquid Glass » Canopée sur 1 seule ligne horizontale */
    .site-header {
      background-color: rgba(255, 255, 255, 0.82) !important;
      backdrop-filter: saturate(180%) blur(20px) !important;
      -webkit-backdrop-filter: saturate(180%) blur(20px) !important;
      border-bottom: 1px solid rgba(29, 73, 13, 0.08) !important;
    }
    .site-header-inner {
      padding: 10px 20px !important;
      gap: 10px !important;
    }
    @media (min-width: 1080px) {
      .site-header-inner {
        flex-wrap: nowrap !important;
      }
      .main-nav {
        flex-wrap: nowrap !important;
        gap: 2px !important;
      }
    }
    .brand-logo-disc {
      width: 50px !important;
      height: 50px !important;
    }
    .brand-name {
      font-size: 1.3rem !important;
    }
    .brand-location {
      font-size: 12px !important;
      white-space: nowrap;
    }
    .nav-item {
      border-radius: var(--radius-pill) !important;
      padding: 6px 11px !important;
      font-size: 14px !important;
      white-space: nowrap;
    }

    /* En mode visiteur normal, masquer toutes les barres techniques .subnav-bar et les codes d'audit */
    body:not(.admin-mode-enabled) .subnav-bar {
      display: none !important;
    }
    body:not(.admin-mode-enabled) .tech-code-tag {
      display: none !important;
    }

    /* 3. Boutons Pilules (980px) sans bordures lourdes */
    .btn {
      border-radius: var(--radius-pill) !important;
      padding: 11px 22px !important;
      font-weight: 600 !important;
      letter-spacing: -0.01em;
    }
    .btn-primary {
      background-color: var(--color-brand-deep) !important;
      color: var(--color-white) !important;
      border: 1px solid transparent !important;
      box-shadow: 0 6px 20px rgba(29, 73, 13, 0.18);
    }
    .btn-secondary {
      background-color: rgba(237, 244, 231, 0.88) !important;
      color: var(--color-brand-deep) !important;
      border: 1px solid rgba(29, 73, 13, 0.16) !important;
    }
    .btn-secondary:hover {
      background-color: var(--color-brand-deep) !important;
      color: var(--color-white) !important;
    }
    .btn-sm {
      padding: 6px 14px !important;
      min-height: 36px !important;
      font-size: 13.5px !important;
      white-space: nowrap;
    }

    /* 4. Cartes Bento Sans Bordures (Borderless Plans de Lumière + 28px) */
    .card {
      border: none !important;
      border-radius: var(--radius-lg) !important;
      box-shadow: var(--shadow-card) !important;
      padding: 26px !important;
    }
    /* Cartes Bento Média Plein Bord (Full-Bleed Image) */
    .bento-card {
      padding: 0 !important;
      overflow: hidden;
      border: none !important;
      border-radius: var(--radius-lg) !important;
      background: var(--color-white);
      box-shadow: var(--shadow-card) !important;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .bento-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-elevated) !important;
    }
    .bento-card .card-media-wrapper {
      border-radius: 0 !important;
      aspect-ratio: auto !important;
      height: 260px !important;
      width: 100%;
    }
    .bento-card.bento-wide .card-media-wrapper {
      height: 260px !important;
    }
    .bento-card-body {
      padding: 22px 26px 24px !important;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex: 1;
      gap: 12px;
    }
    .price-pill {
      border-radius: var(--radius-pill) !important;
      border: none !important;
      background: var(--color-surface-soft) !important;
      padding: 5px 14px !important;
      font-weight: 600 !important;
    }
    .leaf-photo-frame {
      border-radius: 32px !important;
      border: none !important;
      box-shadow: var(--shadow-elevated) !important;
    }
"""

def build_apple_grade_html():
    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Injecter les styles Apple-Grade
    html = html.replace("</style>", APPLE_GRADE_CSS_OVERRIDES + "\n  </style>", 1)

    # 2. Transformer le Hero H1 et le paragraphe d'accroche avec le Contraste Tonal Apple
    old_hero_h1 = "<h1>Respirez, explorez et partagez une journée grandeur nature à ECOPARK</h1>"
    new_hero_h1 = """<h1><span class="tonal-muted">Respirez. Explorez.</span><br/>La nature en grand à Yaoundé-Ahala.</h1>"""
    html = html.replace(old_hero_h1, new_hero_h1, 1)

    old_hero_p = """<p style="font-size:1.15rem;color:var(--color-text-muted);margin:18px 0 26px;max-width:640px;">
                  À 15 minutes du centre de Yaoundé sur la Nationale N°3 (Ahala Barrière), découvrez notre jardin zoologique et botanique, le lac de pirogues, la piscine semi-olympique, la gastronomie camerounaise du <em>Château des Saveurs</em>, nos cités hôtelières et notre Centre de Formation Professionnelle.
                </p>"""
    new_hero_p = """<p class="lead-editorial" style="margin:18px 0 26px;max-width:640px;">
                  À 15 minutes du centre de Yaoundé (Ahala Barrière), vivez <strong>le jardin zoologique et botanique</strong>, <strong>le lac de pirogues</strong>, <strong>la piscine semi-olympique</strong>, la gastronomie camerounaise du <strong>Château des Saveurs</strong>, nos <strong>cités hôtelières</strong> et notre <strong>Centre de Formation Professionnelle</strong>.
                </p>"""
    html = html.replace(old_hero_p, new_hero_p, 1)

    # 3. Transformer les titres de sections avec le Contraste Tonal Apple et encapsuler tous les codes techniques dans .tech-code-tag
    old_sec_h2 = "<h2>Six univers complémentaires au cœur de la verdure d'Ahala</h2>"
    new_sec_h2 = """<h2><span class="tonal-muted">Six univers complémentaires.</span> Au cœur de la verdure d'Ahala.</h2>"""
    html = html.replace(old_sec_h2, new_sec_h2, 1)

    old_res_h2 = "<h2>Préparer ma visite, estimer mon budget et réserver</h2>"
    new_res_h2 = """<h2><span class="tonal-muted">Préparez votre visite.</span> Estimez votre budget en FCFA.</h2>"""
    html = html.replace(old_res_h2, new_res_h2, 1)

    # Encapsuler les préfixes et parenthèses techniques uniquement dans le balisage HTML (avant <script>)
    parts = html.split("<script>", 1)
    parts[0] = re.sub(r'((?:PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\d{2}(?:\s*à\s*(?:PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\d{2}|/\d{2})?\s*•\s*)', r'<span class="tech-code-tag">\1</span>', parts[0])
    parts[0] = re.sub(r'\s*\(`?(?:PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\d{2}`?(?:\s*/\s*`?(?:PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\d{2}`?)*\)', r'<span class="tech-code-tag">\g<0></span>', parts[0])
    html = "<script>".join(parts)

    # 4. Transformer les 6 cartes symétriques (col-4) en Grille Bento Asymétrique (col-8/col-4, col-5/col-7, col-7/col-5) plein bord
    bento_replacements = [
        ('<article class="col-4 card">\n                <div>\n                  <div class="card-media-wrapper">\n                    <img src="audit-assets/ecopark-real-media/chimpanze.jpeg"',
         '<article class="col-8 bento-card bento-wide">\n                <div class="card-media-wrapper">\n                  <img src="audit-assets/ecopark-real-media/chimpanze.jpeg"'),
        ('<article class="col-4 card">\n                <div>\n                  <div class="card-media-wrapper">\n                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png"',
         '<article class="col-4 bento-card">\n                <div class="card-media-wrapper">\n                  <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png"'),
        ('<article class="col-4 card" id="sec-PUB-07">\n                <div>\n                  <div class="card-media-wrapper">\n                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png"',
         '<article class="col-5 bento-card" id="sec-PUB-07">\n                <div class="card-media-wrapper">\n                  <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png"'),
        ('<article class="col-4 card" id="sec-PUB-08">\n                <div>\n                  <div class="card-media-wrapper">\n                    <img src="audit-assets/ecopark-real-media/chambre.jpeg"',
         '<article class="col-7 bento-card bento-wide" id="sec-PUB-08">\n                <div class="card-media-wrapper">\n                  <img src="audit-assets/ecopark-real-media/chambre.jpeg"'),
        ('<article class="col-4 card" id="sec-PUB-11">\n                <div>\n                  <div class="card-media-wrapper">\n                    <img src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg"',
         '<article class="col-7 bento-card bento-wide" id="sec-PUB-11">\n                <div class="card-media-wrapper">\n                  <img src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg"'),
        ('<article class="col-4 card" id="sec-PUB-12">\n                <div>\n                  <div class="card-media-wrapper">\n                    <img src="audit-assets/ecopark-real-media/1786968889976.jpg"',
         '<article class="col-5 bento-card" id="sec-PUB-12">\n                <div class="card-media-wrapper">\n                  <img src="audit-assets/ecopark-real-media/1786968889976.jpg"'),
    ]

    for old_s, new_s in bento_replacements:
        assert old_s in html, f"Bloc Bento introuvable : {old_s[:60]}"
        html = html.replace(old_s, new_s, 1)

    html = html.replace(
        '</div>\n                  <div style="margin-top:14px;display:flex;justify-content:space-between;align-items:center;">',
        '</div>\n                <div class="bento-card-body">\n                  <div>\n                    <div style="display:flex;justify-content:space-between;align-items:center;">'
    )
    html = html.replace(
        '</div>\n                <div style="display:flex;gap:8px;flex-wrap:wrap;">',
        '  </div>\n                  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">'
    )
    html = html.replace(
        '</div>\n              </article>',
        '  </div>\n                </div>\n              </article>'
    )

    PREVIEW_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Apercu Apple-Grade (v3) ecrit : {PREVIEW_HTML}")

def capture_screenshots():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_QA_DIR.mkdir(parents=True, exist_ok=True)
    file_url = PREVIEW_HTML.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(500)

        # Capture 1 : Hero Apple-Grade (En-tête 1 ligne Liquid Glass + Typo monumentale bicolore + CTA pilules)
        s1 = ARTIFACT_DIR / "validation_1_hero_apple_grade.png"
        page.screenshot(path=str(s1), full_page=False)
        (LOCAL_QA_DIR / s1.name).write_bytes(s1.read_bytes())

        # Capture 2 : Grille Bento Asymétrique (Cadrée avec marge de respiration sous le header Liquid Glass)
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-03').offsetTop - 95)")
        page.wait_for_timeout(400)
        s2 = ARTIFACT_DIR / "validation_2_bento_grid_6_univers.png"
        page.screenshot(path=str(s2), full_page=False)
        (LOCAL_QA_DIR / s2.name).write_bytes(s2.read_bytes())

        # Capture 3 : Simulateur de Budget FCFA & Billet QR en style Apple-Grade
        page.evaluate("navigateFamily('RES', 'RES-03'); window.scrollTo(0, 0);")
        page.wait_for_timeout(400)
        s3 = ARTIFACT_DIR / "validation_3_simulateur_fcfa_apple_grade.png"
        page.screenshot(path=str(s3), full_page=False)
        (LOCAL_QA_DIR / s3.name).write_bytes(s3.read_bytes())

        # Capture 4 : Mobile 412x915
        mobile_page = browser.new_page(viewport={"width": 412, "height": 915})
        mobile_page.goto(file_url, wait_until="networkidle")
        mobile_page.wait_for_timeout(400)
        s4 = ARTIFACT_DIR / "validation_4_mobile_apple_grade.png"
        mobile_page.screenshot(path=str(s4), full_page=False)
        (LOCAL_QA_DIR / s4.name).write_bytes(s4.read_bytes())

        browser.close()
    print("[OK] 4 captures de validation (v3) generees avec succes.")

if __name__ == "__main__":
    build_apple_grade_html()
    capture_screenshots()
