# -*- coding: utf-8 -*-
"""
Étape 0 (Corrigée après vérification HTTP) — Construction et vérification du bundle « Site Normal » (etape0-site-live/)
Corrections intégrées :
1. Routage SPA complet dans vercel.json (sans conflit cleanUrls) pour que toutes les URLs historiques (/nos-tarifs, /restaurant, /hotellerie, /formation, /pack-ecole, /pack-entreprise, /contact, /reserver) répondent en HTTP 200 OK.
2. Détection automatique du pathname dans index.html pour ouvrir directement la bonne section métier lorsque le client visite une sous-URL.
"""

import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"
DIST_DIR = ROOT / "etape0-site-live"

def build_etape0():
    # Préserver le dossier .vercel s'il existe déjà dans DIST_DIR
    vercel_dot_dir = DIST_DIR / ".vercel"
    saved_project_json = None
    if (vercel_dot_dir / "project.json").exists():
        saved_project_json = (vercel_dot_dir / "project.json").read_text(encoding="utf-8")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    if saved_project_json:
        vercel_dot_dir.mkdir(parents=True, exist_ok=True)
        (vercel_dot_dir / "project.json").write_text(saved_project_json, encoding="utf-8")

    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Masquer par défaut la barre d'inspection technique (.review-inspector-shell) et l'indicateur d'ID (.active-screen-indicator)
    old_css_target = ".review-inspector-shell {\n      background: #142211;"
    new_css_replacement = """.review-inspector-shell {
      display: none;
      background: #142211;"""
    assert old_css_target in html, "Cible CSS .review-inspector-shell introuvable"
    html = html.replace(old_css_target, new_css_replacement, 1)

    old_indicator_css = ".active-screen-indicator {\n      background: var(--color-surface-soft);"
    new_indicator_css = """.active-screen-indicator {
      display: none;
      background: var(--color-surface-soft);"""
    assert old_indicator_css in html, "Cible CSS .active-screen-indicator introuvable"
    html = html.replace(old_indicator_css, new_indicator_css, 1)

    extra_css = """
    .site-header {
      top: 0 !important;
    }
    body.admin-mode-enabled .review-inspector-shell {
      display: block !important;
    }
    body.admin-mode-enabled .active-screen-indicator {
      display: block !important;
    }
    body.admin-mode-enabled .site-header {
      top: 45px !important;
    }
    body:not(.admin-mode-enabled) .media-origin-badge {
      display: none !important;
    }
    .floating-demo-pill {
      position: fixed;
      bottom: 18px;
      right: 18px;
      z-index: 2500;
      background: var(--color-brand-deep);
      color: var(--color-white);
      border: 2px solid var(--color-white);
      border-radius: 999px;
      padding: 8px 16px;
      font-size: 13.5px;
      font-weight: 600;
      box-shadow: 0 8px 24px rgba(0,0,0,0.22);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .floating-demo-pill:hover {
      background: var(--color-brand-hover);
    }
"""
    html = html.replace("</style>", extra_css + "\n  </style>", 1)

    # 2. Bouton WhatsApp réel dans le récapitulatif du panier
    whatsapp_btn_html = """                  <div style="display:flex;gap:10px;flex-wrap:wrap;">
                    <button type="button" class="btn btn-primary" style="flex:1;" onclick="sendWhatsAppBooking()">📲 Confirmer via WhatsApp ECOPARK (+237 697 13 62 03)</button>
                    <button type="button" class="btn btn-secondary" onclick="inspectScreen('RES-09')">Voir Billet QR (RES-09)</button>
                  </div>"""

    old_buttons_block = """                  <div style="display:flex;gap:10px;flex-wrap:wrap;">
                    <button type="button" class="btn btn-primary" style="flex:1;" onclick="inspectScreen('RES-09')">Générer le Billet QR Démo (RES-09)</button>
                    <button type="button" class="btn btn-secondary" onclick="inspectScreen('RES-10')">Générer Devis Groupe (RES-10)</button>
                  </div>"""
    assert old_buttons_block in html, "Bloc boutons panier introuvable"
    html = html.replace(old_buttons_block, whatsapp_btn_html, 1)

    # 3. Bouton flottant discret pour activer/désactiver le Mode Back-Office & Inspecteur des 77 Écrans
    floating_btn = """
  <button type="button" class="floating-demo-pill" id="btnFloatingAdminToggle" onclick="toggleAdminMode()" title="Activer/Désactiver l'inspecteur des 77 écrans, des 7 rôles et du back-office (Raccourci : Alt+D)">
    ⚙️ <span id="floatingAdminLabel">Mode Démo & Back-Office (77 Écrans)</span>
  </button>
"""
    html = html.replace("  <script>", floating_btn + "\n  <script>", 1)

    # 4. Fonctions JS toggleAdminMode(), sendWhatsAppBooking() et routage par pathname
    extra_js = """
    function toggleAdminMode(forceState) {
      const enabled = typeof forceState === 'boolean'
        ? forceState
        : !document.body.classList.contains('admin-mode-enabled');
      document.body.classList.toggle('admin-mode-enabled', enabled);
      const lbl = document.getElementById('floatingAdminLabel');
      if (lbl) {
        lbl.textContent = enabled
          ? 'Quitter le Mode Inspecteur (Retour Site Client)'
          : 'Mode Démo & Back-Office (77 Écrans)';
      }
    }

    function sendWhatsAppBooking() {
      const name = (document.getElementById('visitorName') || {}).value || 'Visiteur ECOPARK';
      const phone = (document.getElementById('visitorPhone') || {}).value || '';
      const date = (document.getElementById('visitDate') || {}).value || '';
      const total = (document.getElementById('grandTotalFCFA') || {}).textContent || '';
      const pax = `${counts.adults} Adulte(s), ${counts.children} Enfant(s) (3-12 ans), ${counts.toddlers} Tout-petit(s)`;
      const msg = [
        `Bonjour ECOPARK CAMEROUN (Yaoundé-Ahala),`,
        `Je souhaite confirmer ma réservation / demande de visite :`,
        `- Référence : ECP-2026-84920`,
        `- Nom : ${name} (${phone})`,
        `- Date souhaitée : ${date}`,
        `- Participants : ${pax}`,
        `- Budget estimé : ${total}`,
        `Merci de m'indiquer la marche à suivre.`
      ].join('\\n');
      const url = 'https://wa.me/237697136203?text=' + encodeURIComponent(msg);
      window.open(url, '_blank', 'noopener,noreferrer');
    }

    window.addEventListener('keydown', (e) => {
      if (e.altKey && (e.key === 'd' || e.key === 'D')) {
        e.preventDefault();
        toggleAdminMode();
      }
    });

    function initRouteAndParams() {
      const params = new URLSearchParams(window.location.search);
      if (params.get('mode') === 'admin' || params.get('demo') === '77') {
        toggleAdminMode(true);
      }
      const path = (window.location.pathname || '/').replace(/\\/+$/, '').toLowerCase();
      const routeMap = {
        '/nos-tarifs': ['PUB', 'PUB-10'],
        '/tarifs': ['PUB', 'PUB-10'],
        '/restaurant': ['PUB', 'PUB-07'],
        '/hotellerie': ['PUB', 'PUB-08'],
        '/formation': ['PUB', 'PUB-12'],
        '/pack-ecole': ['PUB', 'PUB-11'],
        '/pack-entreprise': ['PUB', 'PUB-11'],
        '/contact': ['PUB', 'PUB-13'],
        '/reserver': ['RES', 'RES-03'],
        '/guichet': ['AGT', 'AGT-03'],
        '/direction': ['DIR', 'DIR-01'],
        '/admin': ['ADM', 'ADM-01']
      };
      if (routeMap[path]) {
        const [fam, scr] = routeMap[path];
        setTimeout(() => navigateFamily(fam, scr), 60);
      }
    }
"""
    html = html.replace(
        "// Initialisation au chargement\n    renderInspectorPills();\n    recalcSimulator();\n    renderPos();",
        extra_js + "\n    // Initialisation au chargement\n    renderInspectorPills();\n    recalcSimulator();\n    renderPos();\n    initRouteAndParams();",
        1
    )

    (DIST_DIR / "index.html").write_text(html, encoding="utf-8")

    # 5. Copier les images référencées dans index.html
    img_paths = sorted(set(re.findall(r'src="([^"]+)"', html)))
    copied_count = 0
    for rel_path in img_paths:
        src_file = ROOT / rel_path
        dst_file = DIST_DIR / rel_path
        if not src_file.exists():
            raise FileNotFoundError(f"Image référencée introuvable : {src_file}")
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)
        copied_count += 1

    # 6. Configuration vercel.json corrigée (sans cleanUrls:true qui cassait la destination /index.html)
    vercel_config = {
        "version": 2,
        "rewrites": [
            {"source": "/nos-tarifs", "destination": "/index.html"},
            {"source": "/nos-tarifs/", "destination": "/index.html"},
            {"source": "/tarifs", "destination": "/index.html"},
            {"source": "/restaurant", "destination": "/index.html"},
            {"source": "/restaurant/", "destination": "/index.html"},
            {"source": "/hotellerie", "destination": "/index.html"},
            {"source": "/hotellerie/", "destination": "/index.html"},
            {"source": "/formation", "destination": "/index.html"},
            {"source": "/formation/", "destination": "/index.html"},
            {"source": "/pack-ecole", "destination": "/index.html"},
            {"source": "/pack-ecole/", "destination": "/index.html"},
            {"source": "/pack-entreprise", "destination": "/index.html"},
            {"source": "/pack-entreprise/", "destination": "/index.html"},
            {"source": "/contact", "destination": "/index.html"},
            {"source": "/contact/", "destination": "/index.html"},
            {"source": "/reserver", "destination": "/index.html"},
            {"source": "/guichet", "destination": "/index.html"},
            {"source": "/direction", "destination": "/index.html"},
            {"source": "/admin", "destination": "/index.html"}
        ],
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}
                ]
            }
        ]
    }
    (DIST_DIR / "vercel.json").write_text(json.dumps(vercel_config, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[OK] Bundle Etape 0 (corrige) genere dans : {DIST_DIR}")
    print(f"[OK] index.html : {(DIST_DIR / 'index.html').stat().st_size} octets | Images : {copied_count}")

if __name__ == "__main__":
    build_etape0()
