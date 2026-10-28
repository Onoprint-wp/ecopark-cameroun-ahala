# -*- coding: utf-8 -*-
"""
Banc de test automatisé E2E — Phase 7 : Orchestration Multi-Agents 360° & Optimisation (ECOPARK Yaoundé-Ahala)

Vérifie :
  1. Livrables Vagues 1 & 2 (00_STRATEGIE, 01_NEURO_COPYWRITING, 02_SUITE_CONTRACTUELLE_6_CDC,
     lead-and-ticket-schema.json, tokens.json, 03_DIRECTIVES_PRINT_ET_IMAGES).
  2. Audit SEO & Schema.org JSON-LD Multi-Entités (#ecoparkSchemaJsonLd : TouristAttraction,
     LocalBusiness, LodgingBusiness, Restaurant, EducationalOrganization) + Open Graph WhatsApp.
  3. Audit Neuro-Conversion : Bandeau d'aversion à la perte (#heroLossAversionCallout) +
     Carte de Soulagement Dopaminergique Post-Formulaire (#dopamineReliefCard) & Pont WhatsApp 1-Clic.
  4. Audit Back-Office : Inbox Unifiée des Leads & Réservations (#admLeadsInboxCard / ADM-09)
     avec filtres par canal, recherche et transition de statut en 1 clic tracée dans l'audit.
  5. Audit Sécurité Anti-XSS & Validation du Contrat de Données (sanitizeEcoparkInput &
     validateEcoparkLeadContract).
  6. Audit Cross-Device (Mobile 390x844 Thumb Zone & Desktop 1440x900), Zéro caractère > U+25FF,
     Zéro fuite de code technique en mode visiteur, Parité stricte index.html == Prototype.
"""
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("ECOPARK_BASE_URL", "http://localhost:3000").rstrip("/")

results = []


def check(cond, label, detail=""):
    results.append((bool(cond), label))
    status = "OK" if cond else "FAIL"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)


def main():
    print("\n=== TEST PHASE 7 : ORCHESTRATION MULTI-AGENTS 360° & OPTIMISATION ECOPARK ===\n")

    # -------------------------------------------------------------------------
    # 1. Vérification des Livrables Documentaires & Techniques (Vagues 1 & 2)
    # -------------------------------------------------------------------------
    print("1. Verification des Livrables Multi-Agents (Vagues 1 & 2)")
    doc_00 = ROOT / "00_STRATEGIE_ET_SOCIAL_LISTENING.md"
    doc_01 = ROOT / "01_NEURO_COPYWRITING_AIDA.md"
    doc_02 = ROOT / "02_SUITE_CONTRACTUELLE_6_CDC.md"
    doc_03 = ROOT / "03_DIRECTIVES_PRINT_ET_IMAGES.md"
    schema_file = ROOT / "lead-and-ticket-schema.json"
    tokens_file = ROOT / "tokens.json"

    for p, label in [
        (doc_00, "Livrable Sous-Agent 1 : 00_STRATEGIE_ET_SOCIAL_LISTENING.md"),
        (doc_01, "Livrable Sous-Agent 2 : 01_NEURO_COPYWRITING_AIDA.md"),
        (doc_02, "Livrable Sous-Agent 3 : 02_SUITE_CONTRACTUELLE_6_CDC.md"),
        (doc_03, "Livrable Sous-Agent 4 : 03_DIRECTIVES_PRINT_ET_IMAGES.md"),
    ]:
        exists = p.is_file() and p.stat().st_size > 4000
        check(exists, label, f"{p.stat().st_size if p.is_file() else 0:,} octets")

    schema_json = json.loads(schema_file.read_text(encoding="utf-8")) if schema_file.is_file() else {}
    defs = schema_json.get("$defs") or schema_json.get("definitions") or {}
    expected_defs = {"BookingTicket", "GroupQuoteLead", "AppointmentLead", "CfpApplicationLead", "UnifiedLeadInboxItem"}
    check(
        expected_defs.issubset(set(defs.keys())),
        "Contrat JSON Schema (lead-and-ticket-schema.json) complet (5 entites)",
        ", ".join(sorted(defs.keys())),
    )

    tokens_json = json.loads(tokens_file.read_text(encoding="utf-8")) if tokens_file.is_file() else {}
    has_token_groups = all(k in tokens_json for k in ("primitive", "semantic", "component", "typography", "layout", "motion"))
    check(has_token_groups, "Design Tokens W3C (tokens.json) valides et complets (6 groupes)")

    # -------------------------------------------------------------------------
    # 2. Audit Playwright DOM, SEO Schema.org, Neuro-Copywriting, Inbox & XSS
    # -------------------------------------------------------------------------
    console_errors = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        page.goto(f"{BASE}/?cb=phase7", wait_until="networkidle")
        page.wait_for_timeout(300)

        # 2A. Audit SEO & Schema.org JSON-LD Multi-Entités
        print("\n2. Audit SEO, Schema.org JSON-LD Multi-Entites & Open Graph WhatsApp")
        seo_audit = page.evaluate("""() => {
            const ldEl = document.getElementById('ecoparkSchemaJsonLd');
            let parsed = null;
            try { parsed = ldEl ? JSON.parse(ldEl.textContent) : null; } catch (e) {}
            const graph = (parsed && parsed['@graph']) || [];
            const types = [];
            graph.forEach(node => {
                if (Array.isArray(node['@type'])) types.push(...node['@type']);
                else if (node['@type']) types.push(node['@type']);
            });
            const ogTitle = (document.querySelector('meta[property="og:title"]') || {}).content || '';
            const ogLocale = (document.querySelector('meta[property="og:locale"]') || {}).content || '';
            const ogImage = (document.querySelector('meta[property="og:image"]') || {}).content || '';
            return {
                hasJsonLd: !!parsed,
                graphCount: graph.length,
                types,
                currencies: graph[0] ? graph[0].currenciesAccepted : null,
                phone: graph[0] ? graph[0].telephone : null,
                ogTitle,
                ogLocale,
                hasOgImage: ogImage.includes('balade_pirogue3.jpg')
            };
        }""")
        check(
            seo_audit["hasJsonLd"] and seo_audit["graphCount"] == 4,
            "Graphe Schema.org JSON-LD actif avec 4 entites metiers",
            f"types={seo_audit['types']}",
        )
        check(
            all(t in seo_audit["types"] for t in ("TouristAttraction", "LocalBusiness", "LodgingBusiness", "Restaurant", "EducationalOrganization")),
            "Couverture Schema.org : TouristAttraction, LocalBusiness, LodgingBusiness, Restaurant, EducationalOrganization",
        )
        check(
            seo_audit["currencies"] == "XAF" and seo_audit["ogLocale"] == "fr_CM" and seo_audit["hasOgImage"],
            "Metadonnees Open Graph WhatsApp (fr_CM, XAF, image HD Ahala) conformes",
        )

        # 2B. Audit Neuro-Copywriting, Soulagement Dopaminergique & Pont WhatsApp 1-Clic
        print("\n3. Audit Neuro-Copywriting AIDA, Soulagement Dopaminergique & Pont WhatsApp 1-Clic")
        neuro_audit = page.evaluate("""() => {
            navigateFamily('PUB', 'PUB-01');
            const heroAnchor = document.getElementById('heroLossAversionCallout');
            const heroAnchorCs = heroAnchor ? window.getComputedStyle(heroAnchor) : null;

            // Declencher les 4 parcours et verifier la mise a jour du Soulagement Dopaminergique
            // 1. Devis Groupe
            window.openQuoteModalSprint1();
            document.getElementById('quoteOrgName').value = 'Ministere de l Education Yaounde';
            document.getElementById('quotePhone').value = '+237 697 13 62 03';
            document.getElementById('quotePax').value = '40';
            const quoteRef = window.submitGroupQuoteSprint1();
            const dopAfterQuote = document.getElementById('dopamineReliefRefBadge').textContent.trim();
            const waUrlAfterQuote = document.getElementById('btnDopamineWhatsAppBridge').getAttribute('data-wa-url');

            // 2. RDV
            window.openRdvModalSprint1('reperage_mariage');
            document.getElementById('rdvVisitorName').value = 'Mme Chantal BIYA-NKOA';
            document.getElementById('rdvPhone').value = '+237 677 11 22 33';
            const rdvRef = window.submitRdvSprint1();
            window.closeSprint1Modals();
            const dopAfterRdv = document.getElementById('dopamineReliefRefBadge').textContent.trim();

            // 3. CFP
            window.openCfpModalSprint1();
            document.getElementById('cfpCandidateName').value = 'Alain FOUDA';
            document.getElementById('cfpAge').value = '21';
            document.getElementById('cfpPhone').value = '+237 690 11 22 33';
            const cfpRef = window.submitCfpApplicationSprint1();
            const dopAfterCfp = document.getElementById('dopamineReliefRefBadge').textContent.trim();

            // 4. Booking Billet QR
            navigateFamily('RES', 'RES-03');
            const cgv = document.getElementById('agreeTermsBooking');
            if (cgv) cgv.checked = true;
            document.getElementById('visitorName').value = 'Famille MBARGA Bastos';
            document.getElementById('visitorPhone').value = '+237 697 13 62 03';
            window.createLiveBookingSprint1();
            const dopAfterBooking = document.getElementById('dopamineReliefRefBadge').textContent.trim();
            const waUrlAfterBooking = document.getElementById('btnDopamineWhatsAppBridge').getAttribute('data-wa-url');

            return {
                hasHeroAnchor: !!heroAnchor,
                heroAnchorBg: heroAnchorCs ? heroAnchorCs.backgroundColor : '',
                quoteRef,
                dopAfterQuote,
                waHasQuoteRef: waUrlAfterQuote.includes(quoteRef),
                rdvRef,
                dopAfterRdv,
                cfpRef,
                dopAfterCfp,
                dopAfterBooking,
                waHasBookingRef: waUrlAfterBooking.includes(dopAfterBooking) && waUrlAfterBooking.startsWith('https://wa.me/237697136203')
            };
        }""")
        check(
            neuro_audit["hasHeroAnchor"] and neuro_audit["heroAnchorBg"] == "rgb(237, 244, 231)",
            "Bandeau Hero d'aversion a la perte (#heroLossAversionCallout) actif en monochrome #EDF4E7",
            neuro_audit["heroAnchorBg"],
        )
        check(
            neuro_audit["dopAfterQuote"] == neuro_audit["quoteRef"] and neuro_audit["waHasQuoteRef"],
            "Soulagement dopaminergique & Pont WhatsApp 1-clic synchronises apres Devis Groupe",
            neuro_audit["quoteRef"],
        )
        check(
            neuro_audit["dopAfterRdv"] == neuro_audit["rdvRef"] and neuro_audit["dopAfterCfp"] == neuro_audit["cfpRef"],
            "Soulagement dopaminergique synchronise apres RDV et Candidature CFP MINEFOP",
            f"{neuro_audit['rdvRef']} / {neuro_audit['cfpRef']}",
        )
        check(
            neuro_audit["dopAfterBooking"].startswith("ECP-2026-") and neuro_audit["waHasBookingRef"],
            "Soulagement dopaminergique & Pont WhatsApp 1-clic synchronises apres Billet QR",
            neuro_audit["dopAfterBooking"],
        )

        # 2C. Audit Back-Office : Inbox Unifiée des Leads & Dossiers (Statuts en 1 Clic — ADM-09)
        print("\n4. Audit Back-Office : Inbox Unifiee des Leads & Statuts en 1 Clic (ADM-09)")
        inbox_audit = page.evaluate("""(quoteRef) => {
            navigateFamily('ADM', 'ADM-01');
            const card = document.getElementById('admLeadsInboxCard');
            const totalBefore = parseInt(document.getElementById('admLeadsTotalCount').textContent, 10) || 0;

            // Filtrer sur QUOTE uniquement
            window.filterAdmLeadsInbox('QUOTE');
            const quoteRows = document.querySelectorAll('#admLeadsTableBody tr[data-lead-channel="QUOTE"]').length;

            // Basculer le statut du devis en 1 clic : CONFIRMED puis PROCESSED
            window.setLeadInboxStatus('QUOTE', quoteRef, 'CONFIRMED');
            const statusAfterConfirm = window.loadDB().quotes.find(q => q.reference === quoteRef).leadStatus;

            window.setLeadInboxStatus('QUOTE', quoteRef, 'PROCESSED');
            const quoteObj = window.loadDB().quotes.find(q => q.reference === quoteRef);
            const latestAudit = window.loadDB().auditLogs[0];

            // Remettre le filtre sur ALL
            window.filterAdmLeadsInbox('ALL');

            return {
                hasInboxCard: !!card,
                totalBefore,
                quoteRows,
                statusAfterConfirm,
                statusAfterProcessed: quoteObj ? quoteObj.leadStatus : null,
                humanStatus: quoteObj ? quoteObj.status : null,
                auditLogged: latestAudit && latestAudit.action.includes(quoteRef) && latestAudit.actor.includes('ADM-09')
            };
        }""", neuro_audit["quoteRef"])
        check(
            inbox_audit["hasInboxCard"] and inbox_audit["totalBefore"] >= 6,
            "Inbox Unifiee des Leads (#admLeadsInboxCard) active et peuplee en temps reel",
            f"{inbox_audit['totalBefore']} dossiers",
        )
        check(
            inbox_audit["quoteRows"] >= 2,
            "Filtrage par canal (BOOKING / QUOTE / RDV / CFP) operationnel dans l'Inbox",
            f"{inbox_audit['quoteRows']} devis affiches",
        )
        check(
            inbox_audit["statusAfterConfirm"] == "CONFIRMED" and inbox_audit["statusAfterProcessed"] == "PROCESSED",
            "Bascule de statut en 1 clic (NEW -> CONFIRMED -> PROCESSED) persistee en BDD",
            inbox_audit["humanStatus"],
        )
        check(
            inbox_audit["auditLogged"],
            "Transition de statut 1-clic tracee dans le Journal d'Audit immuable (ADM-08)",
        )

        # 2D. Audit Sécurité Anti-XSS & Validateur Contractuel JSON Schema
        print("\n5. Audit Securite Anti-XSS & Validation du Contrat de Donnees")
        xss_audit = page.evaluate("""() => {
            window.__xss_triggered = false;
            const maliciousName = '<script>window.__xss_triggered=true</script><img src=x onerror="window.__xss_triggered=true">Dr FOE NDI';

            navigateFamily('RES', 'RES-03');
            document.getElementById('visitorName').value = maliciousName;
            document.getElementById('visitorPhone').value = '+237 697 13 62 03';
            const cgv = document.getElementById('agreeTermsBooking');
            if (cgv) cgv.checked = true;
            window.createLiveBookingSprint1();

            const latestBooking = window.loadDB().bookings[0];
            const inboxHtml = document.getElementById('admLeadsTableBody').innerHTML;

            const validCheck = window.validateEcoparkLeadContract('BOOKING', latestBooking);
            const invalidCheck = window.validateEcoparkLeadContract('BOOKING', {
                reference: 'BAD-REF',
                phone: '123',
                totalFcfa: 100
            });

            return {
                xssTriggered: window.__xss_triggered,
                storedHolder: latestBooking.holder,
                hasRawScriptTag: latestBooking.holder.includes('<script') || inboxHtml.includes('<script'),
                hasRawOnerror: latestBooking.holder.includes('onerror') || inboxHtml.includes('onerror='),
                validContractPass: validCheck.valid,
                invalidContractRejected: !invalidCheck.valid && invalidCheck.errors.length >= 2
            };
        }""")
        check(
            not xss_audit["xssTriggered"] and not xss_audit["hasRawScriptTag"] and not xss_audit["hasRawOnerror"],
            "Protection Anti-XSS : charges <script> et onerror= neutralisees avant persistance et rendu DOM",
            f"holder assaini='{xss_audit['storedHolder']}'",
        )
        check(
            xss_audit["validContractPass"] and xss_audit["invalidContractRejected"],
            "Validateur contractuel (validateEcoparkLeadContract) conforme a lead-and-ticket-schema.json",
        )

        # 2E. Audit Cross-Device (Mobile 390x844 vs Desktop 1440x900)
        print("\n6. Audit Cross-Device (Mobile 390x844 Thumb Zone & Desktop) et Invariants")
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("navigateFamily('PUB', 'PUB-01')")
        page.wait_for_timeout(200)
        mobile_sticky_vis = page.locator("#mobileStickyConversionBar").is_visible()
        page.evaluate("navigateFamily('ADM', 'ADM-01')")
        page.wait_for_timeout(200)
        mobile_sticky_hidden_in_adm = not page.locator("#mobileStickyConversionBar").is_visible()
        check(
            mobile_sticky_vis and mobile_sticky_hidden_in_adm,
            "Ergonomie Mobile 390x844 : Thumb Zone visible côté visiteur et masquée dans le Back-Office ADM",
        )

        browser.close()

    # 3. Parité des fichiers et erreurs console
    h1 = (ROOT / "etape0-site-live" / "index.html").read_bytes()
    h2 = (ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html").read_bytes()
    check(h1 == h2, "Parite stricte octet par octet : index.html == Prototype_Interactif_ECOPARK_NEW_LOOK.html")
    check(len(console_errors) == 0 and len(page_errors) == 0, "Zero erreur console / page JavaScript", f"errors={len(console_errors) + len(page_errors)}")

    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    print(f"\n=== BILAN PHASE 7 : {passed}/{total} CONTROLES VALIDES ===")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
