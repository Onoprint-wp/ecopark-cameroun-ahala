# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"
ARTIFACTS_DIR = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\7ee4ce6d-03a1-4262-8080-a7fbda05ab9a")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        # 1. Capture Billet avec vrai QR code matriciel
        page.goto(f"{BASE}/reserver?demo=77", wait_until="networkidle")
        page.locator("#agreeTermsBooking").check()
        page.locator("button:has-text('Générer & Enregistrer mon Billet QR')").click()
        page.wait_for_timeout(400)
        page.locator("#demoTicketCard").scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase5_1_vrai_qr_code_matriciel.png"))
        print("  [OK] phase5_1_vrai_qr_code_matriciel.png")

        # 2. Capture de la grille dynamique /nos-tarifs
        page.goto(f"{BASE}/nos-tarifs?demo=77", wait_until="networkidle")
        page.locator("#sec-PUB-10").scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase5_2_grille_tarifs_dynamique.png"))
        print("  [OK] phase5_2_grille_tarifs_dynamique.png")

        # 3. Capture du document d'impression officiel (A4/PDF)
        page.goto(f"{BASE}/reserver?demo=77", wait_until="networkidle")
        page.locator("#btnPrintQrPassPdf").click()
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase5_3_impression_officielle_billet.png"))
        print("  [OK] phase5_3_impression_officielle_billet.png")

        # 4. Capture de la modale CGV et case à cocher
        page.goto(f"{BASE}/reserver?demo=77", wait_until="networkidle")
        page.evaluate("openOfficialCgvModal()")
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase5_4_modale_cgv_mentions_legales.png"))
        print("  [OK] phase5_4_modale_cgv_mentions_legales.png")

        # 5. Capture du scanner AGT-05 avec bouton Caméra
        page.goto(f"{BASE}/guichet?demo=77", wait_until="networkidle")
        page.locator(".col-6.card:has(#qrScanInput)").scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=str(ARTIFACTS_DIR / "phase5_5_scanner_camera_agt05.png"))
        print("  [OK] phase5_5_scanner_camera_agt05.png")

        browser.close()
    print("Captures Phase 5 terminees avec succes !")


if __name__ == "__main__":
    main()
