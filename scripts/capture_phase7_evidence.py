# -*- coding: utf-8 -*-
"""
Script de capture visuelle des réalisations de la Phase 7 (Orchestration Multi-Agents 360°) ECOPARK Ahala.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"
ARTIFACTS_DIR = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\4d80e3a5-f34e-4353-905e-d4119ec3cccc")
QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    print("\nCapture des preuves visuelles de la Phase 7 (Orchestration 360°)...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Capture du Hero avec Bandeau d'Aversion à la Perte (#heroLossAversionCallout)
        page.goto(f"{BASE}/?cb=phase7cap", wait_until="networkidle")
        page.wait_for_timeout(300)
        for dest in (ARTIFACTS_DIR / "phase7_1_hero_loss_aversion_aida.png", QA_DIR / "phase7_1_hero_loss_aversion_aida.png"):
            page.screenshot(path=str(dest))
        print("  [OK] phase7_1_hero_loss_aversion_aida.png")

        # 2. Capture de la Carte de Soulagement Dopaminergique Post-Formulaire & Pont WhatsApp 1-Clic
        page.evaluate("""() => {
            navigateFamily('RES', 'RES-03');
            const cgv = document.getElementById('agreeTermsBooking');
            if (cgv) cgv.checked = true;
            document.getElementById('visitorName').value = 'Dr Christophe FOE NDI (VIP Ahala)';
            document.getElementById('visitorPhone').value = '+237 697 13 62 03';
            window.createLiveBookingSprint1();
            const card = document.getElementById('dopamineReliefCard');
            if (card) card.scrollIntoView({ behavior: 'instant', block: 'center' });
        }""")
        page.wait_for_timeout(400)
        for dest in (ARTIFACTS_DIR / "phase7_2_dopamine_relief_whatsapp_bridge.png", QA_DIR / "phase7_2_dopamine_relief_whatsapp_bridge.png"):
            page.screenshot(path=str(dest))
        print("  [OK] phase7_2_dopamine_relief_whatsapp_bridge.png")

        # 3. Capture du Module Back-Office « Inbox Unifiée des Leads — Statuts en 1 Clic » (ADM-09)
        page.evaluate("""() => {
            navigateFamily('ADM', 'ADM-01');
            const inbox = document.getElementById('admLeadsInboxCard');
            if (inbox) inbox.scrollIntoView({ behavior: 'instant', block: 'start' });
        }""")
        page.wait_for_timeout(400)
        for dest in (ARTIFACTS_DIR / "phase7_3_admin_unified_leads_inbox_1click.png", QA_DIR / "phase7_3_admin_unified_leads_inbox_1click.png"):
            page.screenshot(path=str(dest))
        print("  [OK] phase7_3_admin_unified_leads_inbox_1click.png")

        # 4. Capture Mobile 390x844 (Thumb Zone & Ergonomie Smartphone Cameroun)
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("navigateFamily('PUB', 'PUB-01'); window.scrollTo(0, 0);")
        page.wait_for_timeout(350)
        for dest in (ARTIFACTS_DIR / "phase7_4_mobile_thumb_zone_390x844.png", QA_DIR / "phase7_4_mobile_thumb_zone_390x844.png"):
            page.screenshot(path=str(dest))
        print("  [OK] phase7_4_mobile_thumb_zone_390x844.png")

        browser.close()
    print("Captures Phase 7 terminees avec succes !\n")


if __name__ == "__main__":
    main()
