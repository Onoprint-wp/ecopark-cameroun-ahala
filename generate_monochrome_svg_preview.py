# -*- coding: utf-8 -*-
"""
Générateur de la version « 100 % Iconographie SVG Monochrome & Pureté Chromatique 60-30-10 » (v2 — Sans préfixes techniques en mode visiteur)
"""

import pathlib
import re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "etape0-site-live" / "index.html"
MONO_HTML = ROOT / "Preview_Monochrome_SVG_ECOPARK.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\a7ec3e06-7022-4aad-b64e-501927169ab1")
LOCAL_QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"

def svg_icon(paths_d, size=18, cls="svg-mono"):
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'{paths_d}</svg>'
    )

ICONS = {
    "pin": svg_icon('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>', 16),
    "phone": svg_icon('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.58 2.81.7A2 2 0 0 1 22 16.92z"/>', 16),
    "mail": svg_icon('<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>', 16),
    "leaf": svg_icon('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>', 16),
    "map": svg_icon('<polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/>', 18),
    "help": svg_icon('<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>', 18),
    "camera": svg_icon('<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>', 18),
    "shield": svg_icon('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>', 20),
    "lock": svg_icon('<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>', 16),
    "send": svg_icon('<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>', 17),
    "qr": svg_icon('<rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M21 21v.01"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M3 12h.01"/><path d="M12 3h.01"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/><path d="M12 21v-1"/>', 17),
    "zap": svg_icon('<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>', 18),
    "scan": svg_icon('<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" x2="17" y1="12" y2="12"/>', 18),
    "receipt": svg_icon('<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/>', 18),
    "home": svg_icon('<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>', 18),
    "grad": svg_icon('<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>', 18),
    "sliders": svg_icon('<line x1="4" x2="20" y1="21" y2="14"/><line x1="4" x2="20" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><circle cx="12" cy="10" r="2"/>', 16),
    "users": svg_icon('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', 16),
    "check": svg_icon('<path d="M20 6 9 17l-5-5"/>', 16),
    "smartphone": svg_icon('<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>', 15),
    "compass": svg_icon('<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>', 15),
    "wifi_off": svg_icon('<line x1="2" x2="22" y1="2" y2="22"/><path d="M8.5 16.5a5 5 0 0 1 7 0"/><path d="M2 8.82a15 15 0 0 1 4.17-2.65"/><path d="M10.66 5c4.01-.36 8.14.9 11.34 3.76"/><path d="M16.85 11.25a10 10 0 0 1 2.22 1.68"/><path d="M5 12.86a10 10 0 0 1 5.17-2.89"/><line x1="12" x2="12.01" y1="20" y2="20"/>', 16),
    "close": svg_icon('<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', 15),
}

def medallion(icon_key):
    return f'<span class="icon-medallion">{ICONS[icon_key]}</span>'

MONOCHROME_CSS_ADDITIONS = """
    /* ==========================================================================
       PURETÉ CHROMATIQUE 60-30-10 & ICONOGRAPHIE 100 % SVG MONOCHROME
       Zéro bleu / jaune au repos • Uniquement #FFFFFF, #EDF4E7, #1D490D, #1E281B
       ========================================================================== */
    :root {
      --color-info-bg: #EDF4E7 !important;
      --color-info-text: #1D490D !important;
      --color-info-border: rgba(29, 73, 13, 0.18) !important;
    }

    .svg-mono {
      display: inline-block;
      vertical-align: -0.18em;
      flex-shrink: 0;
    }

    .icon-medallion {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background-color: var(--color-surface-soft);
      color: var(--color-brand-deep);
      margin-right: 10px;
      vertical-align: middle;
      flex-shrink: 0;
    }

    .monochrome-callout {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      background-color: var(--color-surface-soft);
      color: var(--color-text);
      border: 1px solid rgba(29, 73, 13, 0.16);
      border-radius: 18px;
      padding: 16px 18px;
      font-size: 14.5px;
      line-height: 1.5;
    }
    .monochrome-callout-icon {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background-color: var(--color-white);
      color: var(--color-brand-deep);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: 0 2px 8px rgba(29, 73, 13, 0.08);
    }

    .status-badge.status-success,
    .status-badge.status-info,
    .status-badge.status-neutral {
      background-color: var(--color-surface-soft) !important;
      color: var(--color-brand-deep) !important;
      border: 1px solid rgba(29, 73, 13, 0.20) !important;
    }
"""

def build_monochrome_html():
    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Injecter les styles monochromes (idempotent)
    if "PURETÉ CHROMATIQUE 60-30-10" not in html:
        html = html.replace("</style>", MONOCHROME_CSS_ADDITIONS + "\n  </style>", 1)

    # 2. Remplacer l'encadré #childPriceProtectionAlert
    old_alert_pattern = re.compile(
        r'<div id="childPriceProtectionAlert"[^>]*>[\s\S]*?</div>',
        re.MULTILINE
    )
    new_alert_html = f"""<div id="childPriceProtectionAlert" class="monochrome-callout">
                  <div class="monochrome-callout-icon">{ICONS['shield']}</div>
                  <div>
                    <strong style="color:var(--color-brand-deep);">Règle de protection tarifaire active :</strong> Même au-delà de 20 participants, le billet d'entrée enfant reste protégé à <strong>500 FCFA</strong> (il n'est jamais majoré à 700 FCFA). Seul le billet adulte bénéficie de la remise groupe à 700 FCFA (au lieu de 1 000 FCFA), ou fait l'objet d'un devis scolaire dédié.
                  </div>
                </div>"""
    if 'class="monochrome-callout"' not in html:
        html, n_alert = old_alert_pattern.subn(new_alert_html, html, count=1)
        assert n_alert == 1, "Encadré #childPriceProtectionAlert introuvable"

    # 3. Passer le badge "BILLET DÉMONSTRATION — PROTOTYPE" en monochrome végétal
    html = html.replace(
        '<span class="status-badge status-warning" style="font-weight:700;">BILLET DÉMONSTRATION — PROTOTYPE</span>',
        f'<span class="status-badge status-neutral" style="font-weight:600;">{ICONS["qr"]} Billet Électronique ECOPARK</span>'
    )

    # 4. Encapsuler tous les préfixes techniques restants dans les titres H3 / Eyebrows (avant <script>)
    parts = html.split("<script>", 1)
    parts[0] = parts[0].replace("(`RES-07` / `RES-08` — Mode Démonstration)", '<span class="tech-code-tag">(RES-07 / RES-08)</span>')
    if '<span class="tech-code-tag">PUB-02 & </span>' not in parts[0]:
        parts[0] = re.sub(
            r'((?:PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\d{2}(?:\s*(?:&|à|,)\s*(?:PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\d{2})*\s*(?:—|•)\s*)',
            r'<span class="tech-code-tag">\1</span>',
            parts[0]
        )
        parts[0] = parts[0].replace("PUB-02 & ORIENTATION,", "ORIENTATION,")
        parts[0] = parts[0].replace("PUB-02 & ", '<span class="tech-code-tag">PUB-02 & </span>')

    # 5. Remplacer tous les emojis du HTML (uniquement dans parts[0] avant <script>) par les icônes SVG monochromes ou médaillons
    emoji_map_html = [
        ("📍", ICONS["pin"]),
        ("📞", ICONS["phone"]),
        ("✉️", ICONS["mail"]),
        ("🌿", ICONS["leaf"]),
        ("🍃", ICONS["leaf"]),
        ("📡", ICONS["wifi_off"]),
        ("🔐", medallion("lock")),
        ("✕", ICONS["close"]),
        ("🗺️", medallion("map")),
        ("❓", medallion("help")),
        ("📸", medallion("camera")),
        ("🔒", ICONS["lock"]),
        ("📲", ICONS["send"]),
        ("🎟️", ICONS["qr"]),
        ("⚡", medallion("zap")),
        ("🔍", medallion("scan")),
        ("🧾", medallion("receipt")),
        ("🏨", medallion("home")),
        ("🎓", medallion("grad")),
        ("🛡️", medallion("shield")),
        ("⚙️", ICONS["sliders"]),
        ("📱", ICONS["smartphone"]),
        ("🧭", ICONS["compass"]),
        ("📷", ICONS["camera"]),
        ("🎨", ICONS["leaf"]),
    ]
    for emo, svg_rep in emoji_map_html:
        parts[0] = parts[0].replace(emo, svg_rep)

    # 6. Nettoyer les emojis et balises SVG résiduelles dans les chaînes JS (parts[1])
    parts[1] = re.sub(r'<span class="icon-medallion">[\s\S]*?</span>\s*', '', parts[1])
    js_emoji_clean = [
        ("👥 ", ""),
        ("✅ ", "• "),
        ("⏳ ", "• "),
        ("❌ ", "• "),
        ("⌛ ", "• "),
        ("🚫 ", "• "),
        ("⛔ ", "• "),
        ("📅 ", "• "),
        ("⚠️ ", "• "),
        ("❓ ", ""),
        ("🎓 ", "• "),
        ("🧾 ", "• "),
        ("📋 ", ""),
        ("• • ", "• "),
    ]
    for emo, rep in js_emoji_clean:
        parts[1] = parts[1].replace(emo, rep)

    html = "<script>".join(parts)

    MONO_HTML.write_text(html, encoding="utf-8")
    SRC_HTML.write_text(html, encoding="utf-8")
    (ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html").write_text(html, encoding="utf-8")
    print(f"[OK] Version 100% Monochrome SVG ecrite dans :\n  - {MONO_HTML}\n  - {SRC_HTML}\n  - {ROOT / 'Prototype_Interactif_ECOPARK_NEW_LOOK.html'}")

def capture_monochrome_screenshots():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_QA_DIR.mkdir(parents=True, exist_ok=True)
    file_url = MONO_HTML.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(400)

        # Capture 1 : Hero & Topbar avec icônes SVG monochromes (#FFFFFF dans le topbar, #1F880B dans l'eyebrow)
        s1 = ARTIFACT_DIR / "mono_validation_1_hero_svg.png"
        page.screenshot(path=str(s1), full_page=False)
        (LOCAL_QA_DIR / s1.name).write_bytes(s1.read_bytes())

        # Capture 2 : Simulateur de Budget FCFA & Billet QR 100 % Monochrome (Zéro boîte bleue ni badge jaune, médaillon bouclier SVG, boutons avec icônes SVG)
        page.evaluate("navigateFamily('RES', 'RES-03'); window.scrollTo(0, 290);")
        page.wait_for_timeout(400)
        s2 = ARTIFACT_DIR / "mono_validation_2_simulateur_sans_bleu_jaune.png"
        page.screenshot(path=str(s2), full_page=False)
        (LOCAL_QA_DIR / s2.name).write_bytes(s2.read_bytes())

        # Capture 3 : Cartes Plan d'Orientation, Recherche/FAQ & Galerie avec Médaillons SVG Monochromes (#EDF4E7 / #1D490D)
        page.evaluate("navigateFamily('PUB', 'PUB-01'); window.scrollTo(0, document.getElementById('sec-PUB-13').offsetTop - 95);")
        page.wait_for_timeout(400)
        s3 = ARTIFACT_DIR / "mono_validation_3_medaillons_svg.png"
        page.screenshot(path=str(s3), full_page=False)
        (LOCAL_QA_DIR / s3.name).write_bytes(s3.read_bytes())

        # Capture 4 : Espace Guichet & Scanner QR avec Médaillons SVG Monochromes
        page.evaluate("navigateFamily('AGT', 'AGT-03'); window.scrollTo(0, 0);")
        page.wait_for_timeout(400)
        s4 = ARTIFACT_DIR / "mono_validation_4_guichet_svg.png"
        page.screenshot(path=str(s4), full_page=False)
        (LOCAL_QA_DIR / s4.name).write_bytes(s4.read_bytes())

        browser.close()
    print("[OK] 4 captures Monochrome SVG (v2) generees avec succes.")

if __name__ == "__main__":
    build_monochrome_html()
    capture_monochrome_screenshots()
