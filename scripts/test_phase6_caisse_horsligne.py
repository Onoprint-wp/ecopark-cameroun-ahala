# -*- coding: utf-8 -*-
"""
Test automatisé d'intégration pour la Phase 6 ECOPARK Ahala :
1. Grille de billetage physique interactive (AGT-08/09)
2. Détection dynamique des écarts de caisse (Conforme, Tolérance <= 2 000 FCFA, Critique > 2 000 FCFA)
3. PV de clôture contradictoire imprimable avec décompte des coupures et visas
4. Contrôle au tourniquet en mode hors-ligne RN3 (AGT-05)
5. Synchronisation automatique des scans à la reconnexion
6. Zéro erreur console JavaScript
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"

results = []


def check(cond, label, detail=""):
    results.append((bool(cond), label))
    status = "OK" if cond else "FAIL"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)


def main():
    print("\n=== TEST PHASE 6 : CAISSE GUICHET, BILLETAGE & CONTROLE HORS-LIGNE ===\n")
    console_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        # ---------------------------------------------------------------------
        # 1. Grille de billetage physique interactive (Task 1)
        # ---------------------------------------------------------------------
        print("1. Grille de billetage physique interactive (Task 1)")
        page.goto(f"{BASE}/guichet?demo=77", wait_until="networkidle")
        page.evaluate("inspectScreen('AGT-08')")
        page.wait_for_timeout(300)

        has_grid = page.locator("#cardCashClosureAgt08").is_visible()
        check(has_grid, "Carte AGT-08/09 presente dans la vue guichet")

        # Vérifier le calcul par défaut (184 500 FCFA conforme)
        initial_phys = page.locator("#physicalCashTotal").text_content().strip()
        initial_theo = page.locator("#theoreticalCashTotal").text_content().strip()
        check(initial_phys == "184 500 FCFA", "Total physique initial conforme", initial_phys)
        check(initial_theo == "184 500 FCFA", "Total theorique initial conforme", initial_theo)

        # Modifier une coupure : 15 billets de 10 000 FCFA
        page.locator("#cashQty10k").fill("15")
        page.wait_for_timeout(100)
        sub10k = page.locator("#subtotal10k").text_content().strip()
        check(sub10k == "150 000 FCFA", "Sous-total 10 000 FCFA recalcule", sub10k)

        # ---------------------------------------------------------------------
        # 2. Gestion des seuils d'ecart de caisse (Task 2)
        # ---------------------------------------------------------------------
        print("\n2. Gestion des seuils d'ecart de caisse (Task 2)")
        # Avec 15 billets de 10k (au lieu de 12), total = 184 500 + 30 000 = 214 500 FCFA (Ecart +30 000 FCFA > 2 000 FCFA)
        diff_crit = page.locator("#physicalCashDiff").text_content().strip()
        is_crit_alert = page.locator("#closureIncidentAlert").is_visible()
        check("ALERTE CRITIQUE" in diff_crit and "+30 000 FCFA" in diff_crit, "Alerte critique declenchee si ecart > 2 000 FCFA", diff_crit)
        check(is_crit_alert, "Bandeau d'alerte gouvernance incident affiche")

        # Ajuster pour un ecart mineur de +500 FCFA : 12 billets 10k et 1 piece 500 FCFA
        page.locator("#cashQty10k").fill("12")
        page.locator("#cashQty500p").fill("1")
        page.wait_for_timeout(100)
        diff_min = page.locator("#physicalCashDiff").text_content().strip()
        check("Tolerance mineure" in diff_min and "+500 FCFA" in diff_min, "Tolerance mineure affichee si ecart <= 2 000 FCFA", diff_min)

        # Reinitialiser aux valeurs conformes
        page.evaluate("resetPhysicalCashCount()")
        page.wait_for_timeout(100)
        diff_reset = page.locator("#physicalCashDiff").text_content().strip()
        check("Caisse Conforme" in diff_reset, "Bouton Reinitialiser retablit la conformite a 0 FCFA", diff_reset)

        # ---------------------------------------------------------------------
        # 3. PV de cloture contradictoire imprimable (Task 3)
        # ---------------------------------------------------------------------
        print("\n3. PV de cloture contradictoire imprimable (Task 3)")
        page.evaluate("validateCashClosure()")
        page.wait_for_timeout(300)

        is_modal_print = page.locator("#modalOfficialPrintBox").is_visible()
        print_title = page.locator("#officialPrintTitle").text_content().strip()
        check(is_modal_print, "Modale d'impression officielle ouverte apres validation cloture")
        check("PROCES-VERBAL DE CLOTURE DE CAISSE" in print_title, "Titre du proces-verbal conforme", print_title)

        print_body = page.locator("#officialPrintBody").text_content()
        check("Billet 10 000 FCFA" in print_body, "Ventilation des billets de 10 000 FCFA presente dans le PV")
        check("TOTAL ESPECES COMPTE (PHYSIQUE)" in print_body, "Ligne de total physique presente dans le PV")
        check("Emargement Caissiere" in print_body and "Visa Direction" in print_body, "Encarts de signatures et visas contradictoires presents")

        # Fermer la modale d'impression
        page.evaluate("closeSprint1Modals()")
        page.wait_for_timeout(200)

        # ---------------------------------------------------------------------
        # 4. Scanner AGT-05 & Controle Hors-Ligne (Task 4)
        # ---------------------------------------------------------------------
        print("\n4. Scanner AGT-05 & Controle Hors-Ligne (Task 4)")
        page.evaluate("inspectScreen('AGT-05')")
        page.wait_for_timeout(200)

        status_text = page.locator("#scannerNetworkStatusBadge").text_content().strip()
        check("Liaison RN3 Active" in status_text, "Badge reseau en ligne par defaut", status_text)

        # Passer en mode Hors-Ligne simulé
        context.set_offline(True)
        page.evaluate("window.dispatchEvent(new Event('offline'))")
        page.wait_for_timeout(200)

        status_offline = page.locator("#scannerNetworkStatusBadge").text_content().strip()
        check("Mode Hors-Ligne RN3" in status_offline, "Bascule automatique sur le badge Mode Hors-Ligne RN3", status_offline)

        # Valider un billet en mode hors-ligne
        page.locator("#qrScanInput").fill("ECP-2026-84920")
        page.locator("button:has-text('dans la BDD')").click()
        page.wait_for_timeout(200)

        verdict_text = page.locator("#scanResultTitle").text_content().strip()
        check("BILLET VALIDE" in verdict_text, "Billet valide avec succes en mode hors-ligne", verdict_text)

        q_count = page.evaluate("window._ecoparkOfflineScansQueue.length")
        check(q_count >= 1, "Scan enregistre dans la file d'attente hors-ligne", f"{q_count} scan(s)")

        # ---------------------------------------------------------------------
        # 5. Synchronisation automatique a la reconnexion (Task 5)
        # ---------------------------------------------------------------------
        print("\n5. Synchronisation automatique a la reconnexion (Task 5)")
        # Rétablir la connexion
        context.set_offline(False)
        page.evaluate("window.dispatchEvent(new Event('online'))")
        page.wait_for_timeout(300)

        q_count_after = page.evaluate("window._ecoparkOfflineScansQueue.length")
        check(q_count_after == 0, "File d'attente hors-ligne automatiquement videe apres reconnexion", f"{q_count_after} restant(s)")

        status_back = page.locator("#scannerNetworkStatusBadge").text_content().strip()
        check("Liaison RN3 Active" in status_back, "Badge reseau repasse en statut actif", status_back)

        # ---------------------------------------------------------------------
        # 6. Integrite console JavaScript
        # ---------------------------------------------------------------------
        print("\n6. Integrite console JavaScript")
        check(len(console_errors) == 0, "Zero erreur console JavaScript", f"{len(console_errors)} erreur(s)")
        if console_errors:
            for err in console_errors[:5]:
                print(f"    [ERR] {err}")

        browser.close()

    successes = sum(1 for ok, _ in results if ok)
    total = len(results)
    print(f"\n{successes}/{total} verifications de la Phase 6 reussies.\n")
    if successes != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
