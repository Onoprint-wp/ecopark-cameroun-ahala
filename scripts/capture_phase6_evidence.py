# -*- coding: utf-8 -*-
"""
Script de capture visuelle des réalisations de la Phase 6 ECOPARK Ahala.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"
ARTIFACTS_DIR = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\7ee4ce6d-03a1-4262-8080-a7fbda05ab9a")


def main():
    print("\nCapture des preuves visuelles de la Phase 6...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Capture de la grille de billetage physique conforme
        page.goto(f"{BASE}/guichet?demo=77", wait_until="networkidle")
        page.evaluate("inspectScreen('AGT-08'); window.scrollTo(0, document.getElementById('cardCashClosureAgt08').offsetTop - 60);")
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase6_1_grille_billetage_physique.png"))
        print("  [OK] phase6_1_grille_billetage_physique.png")

        # 2. Capture avec écart critique (> 2 000 FCFA)
        page.locator("#cashQty10k").fill("16")
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase6_2_alerte_ecart_critique_caisse.png"))
        print("  [OK] phase6_2_alerte_ecart_critique_caisse.png")

        # 3. Capture du Procès-Verbal de clôture imprimable
        page.evaluate("resetPhysicalCashCount(); validateCashClosure();")
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase6_3_proces_verbal_cloture_imprimable.png"))
        print("  [OK] phase6_3_proces_verbal_cloture_imprimable.png")

        # Fermer la modale
        page.evaluate("closeSprint1Modals()")
        page.wait_for_timeout(200)

        # 4. Capture du scanner en mode hors-ligne
        page.evaluate("inspectScreen('AGT-05'); window.scrollTo(0, 0);")
        context.set_offline(True)
        page.evaluate("""
            window._ecoparkOfflineScansQueue = [{ reference: 'ECP-2026-84920', scannedAt: '28/10/2026 08:00', holder: 'M. Jean-Paul MBARGA', offline: true }];
            updateScannerNetworkStatus();
        """)
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase6_4_scanner_mode_horsligne_rn3.png"))
        print("  [OK] phase6_4_scanner_mode_horsligne_rn3.png")

        browser.close()
    print("Captures Phase 6 terminees avec succes !\n")


if __name__ == "__main__":
    main()
