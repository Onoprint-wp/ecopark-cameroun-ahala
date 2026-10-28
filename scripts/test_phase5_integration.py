# -*- coding: utf-8 -*-
"""
Vérification automatisée de la Phase 5 & Viabilité Terrain :
  1. Micro-générateur de vrai QR Code matriciel autonome (SVG & Canvas)
  2. Styles d'impression dédiés @media print
  3. Verrouillage du Lundi et des dates passées
  4. Validation stricte des numéros camerounais (+237 6XXXXXXXX) & case CGV obligatoire
  5. Raccordement dynamique de la grille /nos-tarifs (PUB-10) sur catalog_activities
  6. Raccordement dynamique du simulateur /reserver sur les prix administrés
  7. Activation du flux caméra pour le scanner d'entrée AGT-05
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"

results = []


def check(cond, label, detail=""):
    results.append(bool(cond))
    print(f"  [{'OK' if cond else 'FAIL'}] {label}{(' — ' + str(detail)) if detail else ''}")


def main():
    print("\n=== TEST PHASE 5 & VIABILITÉ TERRAIN ECOPARK ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        # 1. Chargement de la page d'accueil
        page.goto(f"{BASE}/?demo=77", wait_until="networkidle")

        print("\n1. Bibliothèque & Génération de vrai QR Code (Task 1)")
        qr_lib_present = page.evaluate("typeof window.qrcode === 'function'")
        check(qr_lib_present, "Bibliothèque QR Code matricielle autonome chargée (window.qrcode)")

        svg_has_real_qr = page.evaluate("""() => {
            renderEcoparkQrSvg('ECP-2026-TEST', 'demoTicketQrWrapper');
            const path = document.querySelector('#demoTicketQrWrapper svg path');
            return path && path.getAttribute('d') && path.getAttribute('d').length > 500;
        }""")
        check(svg_has_real_qr, "QR Code SVG généré avec de vrais modules matriciels (path d > 500 car.)")

        offline_png_ok = page.evaluate("""() => {
            try {
                const ref = downloadOfflineQrTicketPng();
                return typeof ref === 'string' && ref.startsWith('ECP-');
            } catch (e) {
                return false;
            }
        }""")
        check(offline_png_ok, "Génération et téléchargement du PNG de billet hors-ligne fonctionnels")

        print("\n2. Impression dédiée @media print (Task 2)")
        print_css_present = page.evaluate("""() => {
            const sheets = Array.from(document.styleSheets);
            let hasPrint = false;
            for (const s of sheets) {
                try {
                    const rules = Array.from(s.cssRules || []);
                    for (const r of rules) {
                        if (r.media && r.media.mediaText.includes('print')) hasPrint = true;
                    }
                } catch (e) {}
            }
            return hasPrint;
        }""")
        check(print_css_present, "Feuille de style @media print active")

        print("\n3. Verrouillage du Lundi et des dates passées (Task 3)")
        visit_date_min = page.evaluate("document.getElementById('visitDate').getAttribute('min')")
        check(bool(visit_date_min), "Attribut min posé sur la date de visite", visit_date_min)

        monday_blocked = page.evaluate("""() => {
            const input = document.getElementById('visitDate');
            input.value = '2026-11-16'; // 16 novembre 2026 est un Lundi
            const valid = validateDateChoice(input);
            return valid === false && input.value === '2026-11-17'; // Doit être repoussé au Mardi
        }""")
        check(monday_blocked, "Choix du Lundi bloqué et automatiquement décalé au Mardi (repos du parc)")

        print("\n4. Téléphone camerounais & CGV obligatoires (Task 4)")
        phone_validations = page.evaluate("""() => {
            return {
                bad1: isValidCameroonPhone('01234567'),
                bad2: isValidCameroonPhone('0612345678'),
                good1: isValidCameroonPhone('+237697136203'),
                good2: isValidCameroonPhone('670000000'),
                good3: isValidCameroonPhone('+237 697 13 62 03')
            };
        }""")
        phone_ok = (
            not phone_validations["bad1"]
            and not phone_validations["bad2"]
            and phone_validations["good1"]
            and phone_validations["good2"]
            and phone_validations["good3"]
        )
        check(phone_ok, "Validation stricte des numéros camerounais (+237 6XXXXXXXX)")

        cgv_checkbox_exists = page.locator("#agreeTermsBooking").count() > 0
        check(cgv_checkbox_exists, "Case à cocher CGV & report 90j présente dans le formulaire")

        # Tenter de réserver sans cocher la case CGV
        booking_blocked_without_cgv = page.evaluate("""() => {
            document.getElementById('agreeTermsBooking').checked = false;
            return createLiveBookingSprint1() === false;
        }""")
        check(booking_blocked_without_cgv, "Réservation bloquée si les CGV ne sont pas acceptées")

        print("\n5. Raccordement dynamique de la grille tarifaire PUB-10 (Task 5)")
        page.goto(f"{BASE}/nos-tarifs?demo=77", wait_until="networkidle")
        catalog_rows_count = page.locator("#pubCatalogTableBody tr").count()
        check(catalog_rows_count >= 8, f"Grille /nos-tarifs alimentée dynamiquement ({catalog_rows_count} lignes)")

        # Vérifier que les tarifs sont lus dynamiquement
        first_row_text = page.locator("#pubCatalogTableBody tr:first-child").inner_text()
        check(len(first_row_text) > 10, "Contenu de ligne tarifaire dynamique lisible", first_row_text[:60])

        print("\n6. Prix dynamiques du simulateur /reserver (Task 6)")
        sim_dyn_prices = page.evaluate("""() => {
            return {
                zooIndivAdult: getCatalogPriceDynamic('zoo', false, false),
                zooGroupAdult: getCatalogPriceDynamic('zoo', true, false),
                zooChildProtected: getCatalogPriceDynamic('zoo', true, true),
                piscineIndivAdult: getCatalogPriceDynamic('piscine', false, false),
                piscineGroupChild: getCatalogPriceDynamic('piscine', true, true)
            };
        }""")
        check(sim_dyn_prices["zooIndivAdult"] == 1000, "Zoo adulte individuel : 1 000 FCFA")
        check(sim_dyn_prices["zooGroupAdult"] == 700, "Zoo adulte groupe : 700 FCFA")
        check(sim_dyn_prices["zooChildProtected"] == 500, "Garde-fou enfant groupe Zoo strictement protégé à 500 FCFA")
        check(sim_dyn_prices["piscineGroupChild"] == 1500, "Plafond enfant groupe Piscine à 1 500 FCFA")

        print("\n7. Scanner caméra d'entrée AGT-05 (Task 8)")
        page.goto(f"{BASE}/guichet?demo=77", wait_until="networkidle")
        camera_btn_exists = page.locator("#btnToggleCameraScan").count() > 0
        camera_box_exists = page.locator("#qrCameraScanContainer").count() > 0
        check(camera_btn_exists and camera_box_exists, "Bouton et conteneur de caméra présents dans le scanner AGT-05")

        camera_toggle_fn = page.evaluate("typeof window.toggleQrCameraScan === 'function'")
        check(camera_toggle_fn, "Fonction de pilotage de flux caméra disponible (window.toggleQrCameraScan)")

        print("\n8. Intégrité globale & Erreurs console")
        check(len(console_errors) == 0, "Zéro erreur console JavaScript", console_errors)

        browser.close()

    total = len(results)
    passed = sum(results)
    print(f"\n{passed}/{total} vérifications réussies.")
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
