#!/usr/bin/env python3
"""
SIMULATIONS PROGRESSIVES 360° (DU SIMPLE AU COMPLEXE — NIVEAUX 1 À 6) — ECOPARK CAMEROUN
Exécute une batterie graduée de 20 scénarios réalistes, complexes et offensifs (chaos/sécurité)
pour détecter et prévenir la moindre anomalie fonctionnelle, mathématique, ergonomique ou sécuritaire.
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = os.environ.get("ECOPARK_BASE_URL", "http://localhost:3000").rstrip("/")


def run_simulations():
    print(f"=== LANCEMENT DES SIMULATIONS PROGRESSIVES (NIVEAUX 1 A 6) SUR : {BASE_URL} ===\n")
    passed = 0
    failed = 0
    issues = []

    def check(label: str, cond: bool, detail: str = ""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  [PASS] {label}" + (f" — {detail}" if detail else ""))
        else:
            failed += 1
            msg = f"{label}" + (f" — {detail}" if detail else "")
            issues.append(msg)
            print(f"  [FAIL] {msg}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900}, locale="fr-FR")
        page = context.new_page()

        console_errors = []
        page_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))

        page.goto(f"{BASE_URL}/?demo=77", wait_until="networkidle", timeout=45000)

        # =========================================================================
        # NIVEAU 1 : SIMPLE — Parcours Visiteur Express B2C & Cohérence Vitrine
        # =========================================================================
        print("1. NIVEAU 1 (SIMPLE) : Parcours Visiteur Express, Hero HyperFrames & Pass Nature")
        res_lvl1 = page.evaluate(
            """() => {
            navigateFamily('PUB', 'PUB-01');
            const lossBox = document.getElementById('heroLossAversionCallout');
            const thumbs = Array.from(document.querySelectorAll('#heroThumbStrip button, .hero-thumb-btn'));
            thumbs.forEach(btn => btn.click());

            navigateFamily('RES', 'RES-03');
            const btnNature = document.getElementById('btnBundleDecouverte');
            if (btnNature) btnNature.click();
            const totalText = (document.getElementById('grandTotalFCFA') || {}).textContent || '';
            const childAlert = document.getElementById('childPriceProtectionAlert');
            return {
                hasLossBox: !!lossBox && lossBox.textContent.includes('500 FCFA'),
                thumbsCount: thumbs.length,
                totalText: totalText.trim(),
                childProtected: !!childAlert && childAlert.textContent.includes('500 FCFA')
            };
        }"""
        )
        check(
            "N1.1 — Vitrine Hero (4 vues HyperFrames) & Encart Aversion à la Perte FCFA",
            res_lvl1["hasLossBox"] and res_lvl1["thumbsCount"] == 4,
            f"thumbs={res_lvl1['thumbsCount']}",
        )
        check(
            "N1.2 — Preset 'Pass Découverte Nature' & Protection Tarif Enfant 500 FCFA",
            res_lvl1["childProtected"] and "FCFA" in res_lvl1["totalText"],
            f"total={res_lvl1['totalText']}",
        )

        # =========================================================================
        # NIVEAU 2 : INTERMÉDIAIRE — Famille Royale + Cuisine + Navette + Loge + Report Pluie
        # =========================================================================
        print("\n2. NIVEAU 2 (INTERMÉDIAIRE) : Panier Complexe Multi-Pôles, Billet QR, Dopamine & Report Pluie")
        res_lvl2 = page.evaluate(
            """() => {
            navigateFamily('RES', 'RES-03');
            const btnRoyale = document.getElementById('btnBundleRoyale');
            if (btnRoyale) btnRoyale.click();

            // Sélection Hébergement Cité Chanthel (2 nuits), Cuisine Poulet DG 13h30, Navette Bastos, Pêche
            document.getElementById('chkRepas').checked = true;
            document.getElementById('simDishSelect').value = 'Poulet DG Royal Plantain Mûr';
            document.getElementById('simMealSlotSelect').value = 'Service 13h30';
            document.getElementById('chkBumpLodgeEwondo').checked = true;
            document.getElementById('lodgeCitySelect').value = 'CHANTHEL';
            document.getElementById('lodgeNightsSelect').value = '2';
            document.getElementById('chkBumpNavette').checked = true;
            document.getElementById('simShuttlePickupSelect').value = 'Départ Carrefour Bastos (09h15)';
            document.getElementById('chkBumpPeche').checked = true;
            window.recalcSimulator();

            const totalAfterOptions = (document.getElementById('grandTotalFCFA') || {}).textContent || '';

            // Remplissage titulaire + date Mardi prochain (non-lundi)
            document.getElementById('visitorName').value = 'Famille Mvondo Bastos';
            document.getElementById('visitorPhone').value = '+237 697 13 62 03';
            document.getElementById('visitDate').value = '2026-11-03'; // Mardi
            const cgv = document.getElementById('agreeTermsBooking');
            if (cgv) cgv.checked = true;

            window.createLiveBookingSprint1();

            const latestBooking = window.loadDB().bookings[0];
            const qrRef = latestBooking ? latestBooking.reference : '';
            const dopCard = document.getElementById('dopamineReliefCard');
            const dopVisible = dopCard && dopCard.style.display !== 'none';
            const waUrl = document.getElementById('btnDopamineWhatsAppBridge')
                ? document.getElementById('btnDopamineWhatsAppBridge').getAttribute('data-wa-url')
                : '';

            // Téléchargement du PNG Hors-Ligne
            const pngRef = typeof downloadOfflineQrTicketPng === 'function' ? downloadOfflineQrTicketPng() : '';

            // Garantie Pluie : report gratuit de date dans Mon Espace (ACC-05)
            // Test 1 : tenter de reporter sur un Lundi (2026-11-16) -> doit être automatiquement décalé au Mardi (2026-11-17) !
            navigateFamily('ACC', 'ACC-05');
            window.openRescheduleModal(qrRef, 'BOOKING');
            document.getElementById('rescheduleNewDate').value = '2026-11-16'; // Lundi
            window.confirmRescheduleSprint1();
            const dateAfterMondayAttempt = window.loadDB().bookings.find(b => b.reference === qrRef).date;

            // Test 2 : reporter sur un Dimanche valide (2026-12-20)
            window.openRescheduleModal(qrRef, 'BOOKING');
            document.getElementById('rescheduleNewDate').value = '2026-12-20';
            window.confirmRescheduleSprint1();
            const rescheduledDate = window.loadDB().bookings.find(b => b.reference === qrRef).date;

            return {
                totalAfterOptions: totalAfterOptions.trim(),
                qrRef,
                dopVisible,
                waHasRef: waUrl.includes(qrRef) && waUrl.startsWith('https://wa.me/237697136203'),
                pngOk: pngRef.startsWith('ECP-'),
                dateAfterMondayAttempt,
                rescheduledDate
            };
        }"""
        )
        check(
            "N2.1 — Calcul multi-options (Pass Royale + Cité Chanthel 2N + Cuisine 13h30 + Navette + Pêche)",
            "FCFA" in res_lvl2["totalAfterOptions"] and res_lvl2["qrRef"].startswith("ECP-2026-"),
            f"ref={res_lvl2['qrRef']} | total={res_lvl2['totalAfterOptions']}",
        )
        check(
            "N2.2 — Carte de Soulagement Dopaminergique, Pont WhatsApp 1-Clic & Export PNG Hors-Ligne",
            res_lvl2["dopVisible"] and res_lvl2["waHasRef"] and res_lvl2["pngOk"],
            res_lvl2["qrRef"],
        )
        check(
            "N2.3 — Garantie Pluie (ACC-05) : Verrou Lundi sur report (2026-11-16 -> 2026-11-17) & Report Dimanche (2026-12-20)",
            res_lvl2["dateAfterMondayAttempt"] == "2026-11-17" and res_lvl2["rescheduledDate"] == "2026-12-20",
            f"lundi->{res_lvl2['dateAfterMondayAttempt']} | dimanche->{res_lvl2['rescheduledDate']}",
        )

        # =========================================================================
        # NIVEAU 3 : INTERMÉDIAIRE B2B & INSTITUTIONNEL — Garde-fous Lundi, <16 ans CFP, Devis & RDV
        # =========================================================================
        print("\n3. NIVEAU 3 (B2B & GARDE-FOUS METIER) : Verrou Lundi, Devis Ministère 50 pax, RDV Mariage & CFP MINEFOP")
        res_lvl3 = page.evaluate(
            """() => {
            // 3.1 Test du verrouillage du Lundi sur le formulaire principal
            const dateInput = document.getElementById('visitDate');
            let mondayRejected = false;
            if (dateInput && typeof validateDateChoice === 'function') {
                dateInput.value = '2026-11-16'; // Lundi 16 novembre 2026
                const valid = validateDateChoice(dateInput);
                mondayRejected = (valid === false && dateInput.value === '2026-11-17');
            }

            // 3.2 Devis B2B Séminaire Ministère 50 pax + Navette
            window.openQuoteModalSprint1();
            document.getElementById('quoteOrgName').value = 'Ministère du Tourisme & des Loisirs (MINTOUL)';
            document.getElementById('quotePhone').value = '+237 677 88 99 00';
            document.getElementById('quoteType').value = 'Séminaire Ministère / ONG / Entreprise';
            document.getElementById('quotePax').value = '50';
            document.getElementById('quoteOptShuttle').checked = true;
            window.recalcQuoteProformaPreview();
            const proformaPreview = document.getElementById('quoteProformaTotalText').textContent.trim();
            const quoteRef = window.submitGroupQuoteSprint1();

            // 3.3 Prise de RDV Repérage Mariage Salle Menkii Essomba Anton
            window.openRdvModalSprint1('reperage_mariage');
            document.getElementById('rdvVisitorName').value = 'M. & Mme Abessolo';
            document.getElementById('rdvOrgName').value = 'Mariage Royal Ahala (350 invités)';
            document.getElementById('rdvPhone').value = '+237 699 11 22 33';
            const rdvRef = window.submitRdvSprint1();
            window.closeSprint1Modals();

            // 3.4 Candidature CFP MINEFOP : test rejet < 16 ans puis acceptation 20 ans
            const countBeforeCfp = window.loadDB().cfpApplications.length;
            window.openCfpModalSprint1();
            document.getElementById('cfpCandidateName').value = 'Junior Mineur';
            document.getElementById('cfpAge').value = '14';
            document.getElementById('cfpPhone').value = '+237 655 44 33 22';
            const underageRes = window.submitCfpApplicationSprint1();
            const countAfterUnderage = window.loadDB().cfpApplications.length;

            document.getElementById('cfpCandidateName').value = 'Ngo Biyiha Sandrine';
            document.getElementById('cfpAge').value = '20';
            document.getElementById('cfpPhone').value = '+237 655 44 33 22';
            const cfpRef = window.submitCfpApplicationSprint1();
            const countAfterValidCfp = window.loadDB().cfpApplications.length;

            return {
                mondayRejected,
                quoteRef: quoteRef || '',
                proformaPreview,
                rdvRef: rdvRef || '',
                underageBlocked: countAfterUnderage === countBeforeCfp && !underageRes,
                validCfpAdded: countAfterValidCfp === countBeforeCfp + 1,
                cfpRef: cfpRef || ''
            };
        }"""
        )
        check("N3.1 — Garde-fou fermeture hebdomadaire du Lundi actif (décalage automatique au Mardi)", res_lvl3["mondayRejected"])
        check(
            "N3.2 — Devis B2B Séminaire MINTOUL (50 pax + Navette = 670 000 FCFA) généré",
            res_lvl3["quoteRef"].startswith("DEV-2026-") and res_lvl3["proformaPreview"] == "670 000 FCFA",
            f"{res_lvl3['quoteRef']} ({res_lvl3['proformaPreview']})",
        )
        check(
            "N3.3 — RDV Repérage Mariage Salle Menkii Essomba Anton confirmé",
            res_lvl3["rdvRef"].startswith("RDV-2026-"),
            res_lvl3["rdvRef"],
        )
        check(
            "N3.4 — Garde-fou MINEFOP (< 16 ans rejeté, >= 16 ans accepté)",
            res_lvl3["underageBlocked"] and res_lvl3["validCfpAdded"] and res_lvl3["cfpRef"].startswith("CFP-2026-"),
            res_lvl3["cfpRef"],
        )

        # =========================================================================
        # NIVEAU 4 : COMPLEXE TERRAIN — Scanner 7 Verdicts, Coupure Réseau RN3 & Billetage FCFA
        # =========================================================================
        print("\n4. NIVEAU 4 (TERRAIN GUICHET) : Anti-Fraude 7 Verdicts, Coupure Réseau RN3 & Billetage FCFA")
        ticket_ref = res_lvl2["qrRef"]

        page.evaluate("navigateFamily('AGT', 'AGT-05')")
        page.locator("#qrScanInput").fill(ticket_ref)
        page.locator("button:has-text('dans la BDD')").click()
        v1 = page.locator("#scanResultTitle").text_content().strip()

        page.locator("button:has-text('dans la BDD')").click()
        v2 = page.locator("#scanResultTitle").text_content().strip()

        page.locator("#qrScanInput").fill("ECP-2026-FORGED99")
        page.locator("button:has-text('dans la BDD')").click()
        v7 = page.locator("#scanResultTitle").text_content().strip()

        # Simulation coupure réseau 3G/4G RN3
        context.set_offline(True)
        page.evaluate("window.dispatchEvent(new Event('offline'))")
        page.wait_for_timeout(150)
        badge_offline = page.locator("#scannerNetworkStatusBadge").text_content().strip()

        page.locator("#qrScanInput").fill("ECP-2026-84920")
        page.locator("button:has-text('dans la BDD')").click()
        q_offline = page.evaluate("window._ecoparkOfflineScansQueue.length")

        # Retour du réseau 4G RN3
        context.set_offline(False)
        page.evaluate("window.dispatchEvent(new Event('online'))")
        page.wait_for_timeout(200)
        q_online = page.evaluate("window._ecoparkOfflineScansQueue.length")
        badge_online = page.locator("#scannerNetworkStatusBadge").text_content().strip()

        # Grille de billetage contradictoire FCFA (AGT-08)
        page.evaluate("inspectScreen('AGT-08')")
        page.locator("#cashQty10k").fill("15")
        page.wait_for_timeout(100)
        diff_crit = page.locator("#physicalCashDiff").text_content().strip()
        alert_visible = page.locator("#closureIncidentAlert").is_visible()
        page.evaluate("resetPhysicalCashCount()")

        check(
            "N4.1 — Double Scan Anti-Fraude : 1er passage AUTORISÉ -> 2e passage REFUSÉ -> Forgé INCONNU",
            "BILLET VALIDE" in v1 and "DÉJÀ UTILISÉ" in v2 and "INCONNU" in v7,
            f"1er='{v1[:24]}' | 2e='{v2[:24]}' | 7e='{v7[:22]}'",
        )
        check(
            "N4.2 — Résilience Hors-Ligne RN3 : file d'attente locale puis synchronisation auto au retour 4G",
            "Mode Hors-Ligne RN3" in badge_offline and q_offline >= 1 and q_online == 0 and "Liaison RN3 Active" in badge_online,
            f"offline_queue={q_offline} -> online_queue={q_online}",
        )
        check(
            "N4.3 — Grille de Billetage FCFA (AGT-08) : Alerte critique sur écart > 2 000 FCFA & Reset conforme",
            "ALERTE CRITIQUE" in diff_crit and alert_visible,
            diff_crit,
        )

        # =========================================================================
        # NIVEAU 5 : COMPLEXE GOUVERNANCE — Inbox Unifiée ADM-09, Garde-Fou Enfant & Audit
        # =========================================================================
        print("\n5. NIVEAU 5 (GOUVERNANCE & BACK-OFFICE) : Inbox Leads 1-Clic ADM-09 & Garde-Fou Tarif Enfant")
        res_lvl5 = page.evaluate(
            """(refs) => {
            navigateFamily('ADM', 'ADM-01');
            window.filterAdmLeadsInbox('ALL');
            const rows = Array.from(document.querySelectorAll('#admLeadsTableBody tr'));
            const html = document.getElementById('admLeadsTableBody').innerHTML;

            const foundTicket = html.includes(refs.ticket);
            const foundQuote  = html.includes(refs.quote);
            const foundRdv    = html.includes(refs.rdv);
            const foundCfp    = html.includes(refs.cfp);

            // Changement de statut en 1 clic sur les 4 canaux (BOOKING, QUOTE, RDV, CFP)
            window.setLeadInboxStatus('BOOKING', refs.ticket, 'CONFIRMED');
            window.setLeadInboxStatus('QUOTE', refs.quote, 'CONFIRMED');
            window.setLeadInboxStatus('RDV', refs.rdv, 'PROCESSED');
            window.setLeadInboxStatus('CFP', refs.cfp, 'CONFIRMED');

            const db = window.loadDB();
            const bStatus = (db.bookings.find(b => b.reference === refs.ticket) || {}).leadStatus;
            const qStatus = (db.quotes.find(q => q.reference === refs.quote) || {}).leadStatus;
            const rStatus = (db.appointments.find(r => r.reference === refs.rdv) || {}).leadStatus;
            const cStatus = (db.cfpApplications.find(c => c.reference === refs.cfp) || {}).leadStatus;

            // Recherche textuelle dans l'Inbox
            const searchEl = document.getElementById('admLeadsSearchInput');
            let searchMatches = 0;
            if (searchEl) {
                searchEl.value = 'MINTOUL';
                window.renderAdmLeadsInbox();
                searchMatches = document.querySelectorAll('#admLeadsTableBody tr[data-lead-channel]').length;
                searchEl.value = '';
                window.renderAdmLeadsInbox();
            }

            // Vérification du garde-fou tarif enfant (500 FCFA)
            const zooChildProtected = typeof getCatalogPriceDynamic === 'function'
                ? getCatalogPriceDynamic('zoo', true, true)
                : 0;

            return {
                allFourPresent: foundTicket && foundQuote && foundRdv && foundCfp,
                statusesOk: bStatus === 'CONFIRMED' && qStatus === 'CONFIRMED' && rStatus === 'PROCESSED' && cStatus === 'CONFIRMED',
                searchMatches,
                zooChildProtected,
                totalRows: rows.length
            };
        }""",
            {
                "ticket": res_lvl2["qrRef"],
                "quote": res_lvl3["quoteRef"],
                "rdv": res_lvl3["rdvRef"],
                "cfp": res_lvl3["cfpRef"],
            },
        )
        check(
            "N5.1 — Convergence temps réel : les 4 flux (Billet, Devis, RDV, CFP) remontent dans l'Inbox ADM-09",
            res_lvl5["allFourPresent"],
            f"{res_lvl5['totalRows']} lignes dans l'Inbox",
        )
        check(
            "N5.2 — Traitement 1-Clic multi-canal (BOOKING, QUOTE, RDV, CFP) & Recherche instantanée ('MINTOUL')",
            res_lvl5["statusesOk"] and res_lvl5["searchMatches"] >= 1,
            f"searchMatches={res_lvl5['searchMatches']}",
        )
        check(
            "N5.3 — Sanctuarisation Tarif Enfant Parc/Zoo verrouillée à 500 FCFA",
            res_lvl5["zooChildProtected"] == 500,
            f"zooChild={res_lvl5['zooChildProtected']} FCFA",
        )

        # =========================================================================
        # NIVEAU 6 : STRESS, CHAOS & SÉCURITÉ OFFENSIVE — XSS Polymorphes & Formats Téléphone
        # =========================================================================
        print("\n6. NIVEAU 6 (STRESS & SÉCURITÉ OFFENSIVE) : Injections XSS Polymorphes & Validation Cameroun")
        res_lvl6 = page.evaluate(
            """() => {
            window.__xss_triggered = false;
            const payloads = [
                "<script>window.__xss_triggered=true</script>Jean",
                "<img src=x onerror='window.__xss_triggered=true'>Marie",
                "<svg/onload=window.__xss_triggered=true>Paul",
                "\\" autofocus onfocus=\\"window.__xss_triggered=true\\" x=\\"",
                "javascript:window.__xss_triggered=true"
            ];

            const sanitizedResults = payloads.map(p => window.sanitizeEcoparkInput(p));
            const anyAngleBracketLeft = sanitizedResults.some(s => s.includes('<') || s.includes('>'));
            const anyEventHandlerLeft = sanitizedResults.some(s => /onerror|onload|onfocus|javascript:/i.test(s));

            // Injection dans la recherche de l'Inbox Admin
            const searchEl = document.getElementById('admLeadsSearchInput');
            if (searchEl) {
                searchEl.value = payloads[1];
                window.renderAdmLeadsInbox();
                searchEl.value = '';
                window.renderAdmLeadsInbox();
            }

            // Validation stricte du contrat JSON Schema sur téléphones camerounais valides vs invalides (y compris vide)
            const validPhones = ['697136203', '+237 677 12 34 56', '222 23 45 67', '+237655001122'];
            const invalidPhones = ['', '12345', '0612345678', '+33612345678', 'abcde', '600000000'];

            const validCheck = validPhones.every(ph => window.validateEcoparkLeadContract('BOOKING', {
                reference: 'ECP-2026-10001', holder: 'Test', phone: ph, totalFcfa: 1000
            }).valid);
            const invalidCheck = invalidPhones.every(ph => !window.validateEcoparkLeadContract('BOOKING', {
                reference: 'ECP-2026-10001', holder: 'Test', phone: ph, totalFcfa: 1000
            }).valid);

            // Validation âge MINEFOP dans le validateur contractuel CFP
            const cfpUnderageRejected = !window.validateEcoparkLeadContract('CFP', {
                reference: 'CFP-2026-1001', name: 'Mineur', age: 14, phone: '697136203'
            }).valid;
            const cfpValidAccepted = window.validateEcoparkLeadContract('CFP', {
                reference: 'CFP-2026-1001', name: 'Majeur', age: 20, phone: '697136203'
            }).valid;

            return {
                xssTriggered: !!window.__xss_triggered,
                anyAngleBracketLeft,
                anyEventHandlerLeft,
                validCheck,
                invalidCheck,
                cfpContractOk: cfpUnderageRejected && cfpValidAccepted
            };
        }"""
        )
        check(
            "N6.1 — Résistance aux 5 vecteurs XSS polymorphes (<script>, <img onerror>, <svg onload>, attributs, javascript:)",
            not res_lvl6["xssTriggered"] and not res_lvl6["anyAngleBracketLeft"] and not res_lvl6["anyEventHandlerLeft"],
        )
        check(
            "N6.2 — Validation contractuelle Cameroun (+237 6XX/2XX acceptés, vide/étrangers/invalides & CFP <16 ans rejetés)",
            res_lvl6["validCheck"] and res_lvl6["invalidCheck"] and res_lvl6["cfpContractOk"],
        )
        check(
            "N6.3 — Stabilité globale après stress-test (0 erreur console / 0 exception JS)",
            len(console_errors) == 0 and len(page_errors) == 0,
            f"console_errors={len(console_errors)}, page_errors={len(page_errors)}",
        )

        browser.close()

    print(f"\n=== BILAN DES SIMULATIONS PROGRESSIVES (NIVEAUX 1 A 6) : {passed}/{passed + failed} PASS ===")
    if failed > 0:
        print("Anomalies détectées :")
        for iss in issues:
            print(f"  - {iss}")
        sys.exit(1)


if __name__ == "__main__":
    run_simulations()
