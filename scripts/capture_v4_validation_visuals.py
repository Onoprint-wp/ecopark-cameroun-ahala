# -*- coding: utf-8 -*-
"""
Capture des visuels de validation V4 « Canopée immersive » (Desktop 1440x900 & Mobile 390x844)
pour les 6 écrans pilotes et copie dans le dossier d'artefacts de la session.
"""
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
RELOOK_DIR = ROOT / "relooking"
ARTIFACT_DIR = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\b7524df8-7e88-4d15-bffe-671da338b621")
BASE = "http://localhost:3000"


def main():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    RELOOK_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copier les 3 planches de référence V4 dans le dossier d'artefacts pour l'intégration Markdown
    for ref_img in [
        "ecopark_nature_design_system_board.png",
        "ecopark_desktop_interfaces_nature_inspired_touris.png",
        "ecopark_interfaces_mobiles_immersives.png",
    ]:
        src = RELOOK_DIR / ref_img
        if src.exists():
            shutil.copy2(src, ARTIFACT_DIR / ref_img)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # --- VUES DESKTOP (1440 x 900) ---
        desk = browser.new_page(viewport={"width": 1440, "height": 900})
        desk.goto(f"{BASE}/", wait_until="networkidle")
        desk.wait_for_timeout(400)

        # Pilote 1 : PUB-01 Accueil Desktop (Hero Cinématique V4 + 4 Piliers)
        desk.locator("#v4CanopyHeroStage").scroll_into_view_if_needed()
        desk.evaluate("window.scrollTo(0, 0)")
        desk.wait_for_timeout(300)
        p1 = ARTIFACT_DIR / "v4_pilot1_accueil_desktop.png"
        desk.screenshot(path=str(p1))
        shutil.copy2(p1, RELOOK_DIR / p1.name)

        # Pilote 2 : PUB-03 Catalogue des Activités Desktop (Filtres + Grille 4 colonnes V4)
        desk.evaluate("document.getElementById('sec-PUB-03').scrollIntoView({behavior:'instant', block:'start'})")
        desk.wait_for_timeout(300)
        p2 = ARTIFACT_DIR / "v4_pilot2_catalogue_desktop.png"
        desk.screenshot(path=str(p2))
        shutil.copy2(p2, RELOOK_DIR / p2.name)

        # Pilote 3 : PUB-04 Fiche Détail d'une Activité Desktop (Balade en pirogue + Sidebar Réservation)
        desk.evaluate("openV4ActivityDetail('pirogue'); document.getElementById('sec-PUB-04').scrollIntoView({behavior:'instant', block:'start'})")
        desk.wait_for_timeout(350)
        p3 = ARTIFACT_DIR / "v4_pilot3_fiche_activite_pub04_desktop.png"
        desk.screenshot(path=str(p3))
        shutil.copy2(p3, RELOOK_DIR / p3.name)

        # Pilote 4 : PUB-09 Hébergement (Cités Ewondo, Chanthel, Bene & Suites) + Carte Saveurs FCFA
        desk.evaluate("document.getElementById('sec-PUB-09').scrollIntoView({behavior:'instant', block:'start'})")
        desk.wait_for_timeout(350)
        p4 = ARTIFACT_DIR / "v4_pilot4_hebergement_saveurs_pub09_desktop.png"
        desk.screenshot(path=str(p4))
        shutil.copy2(p4, RELOOK_DIR / p4.name)

        # Pilote 6A : RES Parcours de Réservation 4 Étapes & Billet QR Desktop
        desk.evaluate("navigateFamily('RES', 'RES-01'); window.scrollTo(0, 0)")
        desk.wait_for_timeout(350)
        p6d = ARTIFACT_DIR / "v4_pilot6_reservation_stepper_desktop.png"
        desk.screenshot(path=str(p6d))
        shutil.copy2(p6d, RELOOK_DIR / p6d.name)

        desk.close()

        # --- VUES MOBILES (390 x 844) ---
        mob = browser.new_page(viewport={"width": 390, "height": 844})
        mob.goto(f"{BASE}/", wait_until="networkidle")
        mob.wait_for_timeout(400)

        # Pilote 5A : Accueil Mobile V4 + Bottom Nav 4 Onglets
        mob.evaluate("document.getElementById('v4CanopyHeroStage').scrollIntoView({behavior:'instant', block:'start'})")
        mob.wait_for_timeout(300)
        p5a = ARTIFACT_DIR / "v4_pilot5_accueil_mobile.png"
        mob.screenshot(path=str(p5a))
        shutil.copy2(p5a, RELOOK_DIR / p5a.name)

        # Pilote 5B : Fiche Activité Mobile V4 (PUB-04) + Bottom Nav
        mob.evaluate("openV4ActivityDetail('pirogue'); document.getElementById('sec-PUB-04').scrollIntoView({behavior:'instant', block:'start'})")
        mob.wait_for_timeout(350)
        p5b = ARTIFACT_DIR / "v4_pilot5_fiche_activite_mobile.png"
        mob.screenshot(path=str(p5b))
        shutil.copy2(p5b, RELOOK_DIR / p5b.name)

        # Pilote 6B : Billet QR Coupe-File Mobile (RES-09) + Bottom Nav
        mob.evaluate("navigateV4MobileTab('RESERVER'); document.getElementById('demoTicketCard').scrollIntoView({behavior:'instant', block:'center'})")
        mob.wait_for_timeout(350)
        p6m = ARTIFACT_DIR / "v4_pilot6_billet_qr_mobile.png"
        mob.screenshot(path=str(p6m))
        shutil.copy2(p6m, RELOOK_DIR / p6m.name)

        # Pilote 6C : Mon Compte Mobile (ACC-02) + Bottom Nav
        mob.evaluate("navigateV4MobileTab('COMPTE'); window.scrollTo(0, 0)")
        mob.wait_for_timeout(350)
        p6acc = ARTIFACT_DIR / "v4_pilot6_mon_compte_mobile.png"
        mob.screenshot(path=str(p6acc))
        shutil.copy2(p6acc, RELOOK_DIR / p6acc.name)

        mob.close()
        browser.close()

    print("[OK] 8 captures haute définition V4 générées dans les dossiers artifact et relooking/.")


if __name__ == "__main__":
    main()
