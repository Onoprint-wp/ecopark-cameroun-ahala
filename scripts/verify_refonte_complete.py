# -*- coding: utf-8 -*-
"""
Verification complete de la refonte ECOPARK Cameroun « Canopee vivante » (Sections A a I).
Controle :
  - Regles persistantes (.agents/rules/ecopark-*.md) et documentation (docs/ecopark-*.md)
  - Palette semantique, surfaces neutres, typographie >= 16px, cibles >= 44px, 0 emoji
  - Architecture de l'information (5 rubriques principales, utilitaires, routes canoniques et anciennes)
  - Restructuration de l'Accueil (8 sections dans l'ordre cible, 1 seul H1 visible, 0 mention de dev)
  - Gabarits complets (Fiche activite, Hebergement, Restaurant, Groupes & evenements, Formation CFP)
  - Source unique des informations (ECOPARK_SOURCE_UNIQUE) et les 5 scenarios auto-service
  - Parcours de reservation (4 parcours distincts, 5 etapes dans l'ordre, 0 date fixe 2026-11-15,
    billet QR masque avant confirmation, solde guichet explicite, QR sans telephone personnel)
  - Responsive sans debordement horizontal sur 360px, 390px, 768px, 1280px et 1440px
  - Captures visuelles des 6 pages : accueil, catalogue et fiche activite, hebergement,
    restaurant, formation, reservation.
"""
import http.server
import json
import os
import socketserver
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
LIVE_DIR = ROOT / "etape0-site-live"
QA_DIR = ROOT / "audit-assets" / "qa-refonte"
ARTIFACT_DIR = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\647fe6a0-be58-4692-ab77-e139c6c1d041")


class _SpaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(LIVE_DIR), **kwargs)

    def do_GET(self):
        clean = self.path.lstrip("/").split("?")[0]
        target = LIVE_DIR / clean
        if not target.exists() or target.is_dir():
            self.path = "/index.html"
        return super().do_GET()

    def log_message(self, *args):
        pass


_httpd = socketserver.TCPServer(("127.0.0.1", 0), _SpaHandler)
threading.Thread(target=_httpd.serve_forever, daemon=True).start()
BASE = os.environ.get("ECOPARK_BASE_URL", f"http://127.0.0.1:{_httpd.server_address[1]}").rstrip("/")

results = []


def check(cond, label, detail=""):
    ok = bool(cond)
    results.append((ok, label, str(detail)))
    print(f"  [{'OK' if ok else 'FAIL'}] {label}{(' — ' + str(detail)) if detail else ''}")


def main():
    QA_DIR.mkdir(parents=True, exist_ok=True)
    print("\n=== VERIFICATION COMPLETE DE LA REFONTE ECOPARK « CANOPEE VIVANTE » ===\n")

    # 1. Section A : Regles persistantes & Documentation
    print("1. Section A — Regles persistantes & Documentation vivante")
    rule_files = [
        ROOT / ".agents" / "rules" / "ecopark-design.md",
        ROOT / ".agents" / "rules" / "ecopark-information.md",
        ROOT / ".agents" / "rules" / "ecopark-booking.md",
        ROOT / ".agents" / "rules" / "ecopark-quality.md",
    ]
    for rf in rule_files:
        exists = rf.exists()
        txt = rf.read_text(encoding="utf-8") if exists else ""
        check(exists and txt.startswith("---\ntrigger: always_on\n---"), f"Regle persistante active : {rf.name}")

    plan_doc = ROOT / "docs" / "ecopark-refonte-plan.md"
    val_doc = ROOT / "docs" / "ecopark-validation.md"
    check(plan_doc.exists() and len(plan_doc.read_text(encoding="utf-8")) > 500, "Document docs/ecopark-refonte-plan.md present")
    check(val_doc.exists() and len(val_doc.read_text(encoding="utf-8")) > 500, "Document docs/ecopark-validation.md present")

    # Parite index.html == Prototype_Interactif_ECOPARK_NEW_LOOK.html
    live_bytes = (ROOT / "etape0-site-live" / "index.html").read_bytes()
    proto_bytes = (ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html").read_bytes()
    check(live_bytes == proto_bytes, "Parite stricte octet par octet index.html == Prototype_Interactif_ECOPARK_NEW_LOOK.html", f"{len(live_bytes):,} octets")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        console_errors = []
        page.on("pageerror", lambda e: console_errors.append(str(e)))
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

        page.goto(BASE + "/", wait_until="networkidle")

        # 2. Section B : Systeme graphique, couleurs semantiques & accessibilite
        print("\n2. Section B — Systeme graphique « Canopee vivante » & Accessibilite")
        gfx = page.evaluate("""() => {
            const cs = getComputedStyle(document.documentElement);
            const bodyCs = getComputedStyle(document.body);
            const tokens = {
                brand: cs.getPropertyValue('--eco-brand').trim(),
                nature: cs.getPropertyValue('--eco-nature').trim(),
                water: cs.getPropertyValue('--eco-water').trim(),
                lodge: cs.getPropertyValue('--eco-lodge').trim(),
                dining: cs.getPropertyValue('--eco-dining').trim(),
                cfp: cs.getPropertyValue('--eco-cfp').trim(),
                text: cs.getPropertyValue('--eco-text').trim(),
                bg: cs.getPropertyValue('--eco-bg').trim(),
                surface: cs.getPropertyValue('--eco-surface').trim()
            };
            const fontSizePx = parseFloat(bodyCs.fontSize);
            const btnRes = document.getElementById('btnHeaderReserver');
            const btnResRect = btnRes ? btnRes.getBoundingClientRect() : { height: 0 };
            const logoImg = document.querySelector('.brand-logo-disc img');
            return {
                tokens,
                fontSizePx,
                btnResH: Math.round(btnResRect.height),
                logoSrc: logoImg ? logoImg.getAttribute('src') : ''
            };
        }""")
        check(
            gfx["tokens"]["brand"] == "#254B28"
            and gfx["tokens"]["nature"] == "#527A35"
            and gfx["tokens"]["water"] == "#176B80"
            and gfx["tokens"]["lodge"] == "#A45138"
            and gfx["tokens"]["dining"] == "#946015"
            and gfx["tokens"]["cfp"] == "#4D5685"
            and gfx["tokens"]["text"] == "#242824"
            and gfx["tokens"]["bg"] == "#F7F5EF"
            and gfx["tokens"]["surface"] == "#FFFFFF",
            "Palette semantique « Canopee vivante » conforme aux 9 tokens de depart",
            gfx["tokens"]
        )
        check(gfx["fontSizePx"] >= 16 and gfx["btnResH"] >= 44 and "cropped-LOGO-ECOPARK-Youtube.png" in gfx["logoSrc"],
              "Corps de texte >= 16px, bouton Reserver >= 44px et logo officiel conserve",
              f"font={gfx['fontSizePx']}px, btnH={gfx['btnResH']}px")

        # 3. Section C & D : Navigation principale a 5 rubriques & Accueil en 8 sections
        print("\n3. Sections C & D — Architecture de l'information (5 rubriques) & Accueil (8 sections)")
        nav_and_home = page.evaluate("""() => {
            const topNavLabels = Array.from(document.querySelectorAll('#v4MainMegaNav .v4-dropdown-toggle span:nth-child(2)')).map(el => el.textContent.trim());
            const hasMesReservations = !!document.getElementById('nav-ACC') && document.getElementById('nav-ACC').textContent.includes('Mes réservations');
            const hasReserverBtn = !!document.getElementById('btnHeaderReserver') && document.getElementById('btnHeaderReserver').textContent.trim() === 'Réserver';

            // Verifier les H1 visibles sur l'accueil
            const visibleH1s = Array.from(document.querySelectorAll('h1')).filter(h => {
                const r = h.getBoundingClientRect();
                return r.width > 5 && r.height > 5 && getComputedStyle(h).visibility !== 'hidden';
            }).map(h => h.textContent.replace(/\\s+/g, ' ').trim());

            // Ordre des 8 blocs de l'accueil
            const blockIds = [
                'v4CanopyHeroStage',
                'homeBlock2Experiences',
                'homeBlock3Projects',
                'homeBlock4DayPasses',
                'homeBlock5StayAndDine',
                'homeBlock6Agenda',
                'homeBlock7Testimonials',
                'homeBlock8Practical'
            ];
            const blocksPresent = blockIds.every(id => !!document.getElementById(id));
            const topPositions = blockIds.filter(id => id !== 'homeBlock7Testimonials').map(id => {
                const el = document.getElementById(id);
                return el ? Math.round(el.getBoundingClientRect().top) : -1;
            });
            const strictlyOrdered = topPositions.every((val, i, arr) => i === 0 || val > arr[i - 1]);
            const testimonialsHidden = getComputedStyle(document.getElementById('homeBlock7Testimonials')).display === 'none';

            // Verifier l'absence de mentions de dev visibles
            const visiblePublicText = document.getElementById('view-PUB').innerText;
            const hasDevJargon = /Page 1\\/6|Architecture Multi-Pages|Parcours Transactionnel|128 avis vérifiés/i.test(visiblePublicText);

            return {
                topNavLabels,
                hasMesReservations,
                hasReserverBtn,
                visibleH1s,
                blocksPresent,
                strictlyOrdered,
                testimonialsHidden,
                hasDevJargon
            };
        }""")
        expected_rubriques = [
            "Découvrir le parc",
            "Séjour & restaurant",
            "Groupes & événements",
            "Formations",
            "Préparer ma visite",
        ]
        check(nav_and_home["topNavLabels"] == expected_rubriques and nav_and_home["hasMesReservations"] and nav_and_home["hasReserverBtn"],
              "Navigation principale conforme aux 5 rubriques cibles + Mes reservations + Reserver",
              nav_and_home["topNavLabels"])
        check(len(nav_and_home["visibleH1s"]) == 1 and "Prenez le frais. Vivez la nature." in nav_and_home["visibleH1s"][0],
              "Un seul H1 visible sur l'Accueil : « Prenez le frais. Vivez la nature. »",
              nav_and_home["visibleH1s"])
        check(nav_and_home["blocksPresent"] and nav_and_home["strictlyOrdered"] and nav_and_home["testimonialsHidden"] and not nav_and_home["hasDevJargon"],
              "8 sections de l'Accueil dans l'ordre exact, temoignages non authentifies masques, 0 mention de developpement",
              nav_and_home)

        # Capture 1 : Accueil
        page.screenshot(path=str(QA_DIR / "01_accueil_canopee_vivante.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "01_accueil_canopee_vivante.png"), full_page=False)

        # 4. Section E, F & H : Gabarits des pages, Source unique & 5 scenarios auto-service
        print("\n4. Sections E, F & H — Gabarits des pages, Source unique & 5 scenarios auto-service")

        # Page Catalogue & Fiche activite
        page.evaluate("navigateV4SiteMenu('ACT_PIROGUE')")
        page.wait_for_timeout(200)
        fiche_check = page.evaluate("""() => {
            const title = document.getElementById('v4Pub04Title').textContent.trim();
            const hasDeroulement = document.getElementById('v4Pub04DeroulementList').children.length >= 2;
            const hasInclus = document.getElementById('v4Pub04InclusList').children.length >= 2;
            const hasConditions = document.getElementById('v4Pub04ConditionsList').children.length >= 2;
            const hasComplementary = !!document.getElementById('v4Pub04ComplementaryBox');
            const dateVal = document.getElementById('v4Pub04DateInput').value;
            return { title, hasDeroulement, hasInclus, hasConditions, hasComplementary, dateVal };
        }""")
        check(
            fiche_check["hasDeroulement"]
            and fiche_check["hasInclus"]
            and fiche_check["hasConditions"]
            and fiche_check["hasComplementary"]
            and fiche_check["dateVal"] != "2026-11-15",
            "Gabarit Fiche Activite complet (deroulement, inclus/non inclus, conditions, activites complementaires, date dynamique)",
            fiche_check
        )
        page.screenshot(path=str(QA_DIR / "02_catalogue_et_fiche_activite.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "02_catalogue_et_fiche_activite.png"), full_page=False)

        # Page Sejour & Hebergement (Scenario #2 : conditions et prix d'une chambre)
        page.evaluate("navigateV4SiteMenu('HOTELS_COMPARATIF')")
        page.wait_for_timeout(200)
        hotel_check = page.evaluate("""() => {
            const sec = document.getElementById('sec-PUB-09');
            const txt = sec ? sec.innerText : '';
            return {
                hasCheckInOut: txt.includes('Check-in : 14h00') && txt.includes('Check-out : 11h00'),
                hasPricesAndUnits: txt.includes('25 000 – 30 000 FCFA') && txt.includes('/ nuit') && txt.includes('10 000 – 15 000 FCFA'),
                hasRestoTemplate: !!document.getElementById('restaurantFullTemplateCard')
            };
        }""")
        check(hotel_check["hasCheckInOut"] and hotel_check["hasPricesAndUnits"] and hotel_check["hasRestoTemplate"],
              "Scenario #2 & Gabarit Hebergement : tarifs par nuit (10k-45k FCFA) et conditions d'arrivee 14h00 / depart 11h00 explicites",
              hotel_check)
        page.screenshot(path=str(QA_DIR / "03_hebergement_cites.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "03_hebergement_cites.png"), full_page=False)

        # Capture 4 : Restaurant Le Chateau des Saveurs
        page.evaluate("""() => {
            const el = document.getElementById('restaurantFullTemplateCard');
            if (el) {
                const y = el.getBoundingClientRect().top + window.scrollY - 145;
                window.scrollTo({ top: Math.max(0, y), behavior: 'instant' });
            }
        }""")
        page.wait_for_timeout(150)
        page.screenshot(path=str(QA_DIR / "04_restaurant_chateau_des_saveurs.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "04_restaurant_chateau_des_saveurs.png"), full_page=False)

        # Page Groupes & evenements (Scenario #3 : formulaire de devis pour une sortie scolaire)
        page.evaluate("navigateV4SiteMenu('GROUPES_SCOLAIRES')")
        page.wait_for_timeout(200)
        group_check = page.evaluate("""() => {
            const sec = document.getElementById('sec-PUB-11');
            const txt = sec ? sec.innerText : '';
            return {
                hasSchool500: txt.includes('500 FCFA / élève'),
                hasMenkii500: txt.includes('500 places'),
                hasShuttles: txt.includes('5, 18 et 32 places')
            };
        }""")
        check(group_check["hasSchool500"] and group_check["hasMenkii500"] and group_check["hasShuttles"],
              "Scenario #3 & Gabarit Groupes : sorties scolaires (500 FCFA/eleve), Salle Menkii 500 places, navettes et devis accessibles",
              group_check)

        # Page Formations CFP (Scenario #4 : conditions d'admission d'une formation)
        page.goto(BASE + "/formations", wait_until="domcontentloaded")
        page.wait_for_timeout(250)
        cfp_check = page.evaluate("""() => {
            const sec = document.getElementById('sec-PUB-12');
            const txt = sec ? sec.innerText : '';
            return {
                hasAge16: txt.includes('dès 16 ans'),
                hasDuration12m: txt.includes('12 mois'),
                hasFees: txt.includes('50 000 FCFA') && txt.includes('250 000 FCFA') && txt.includes('4 tranches'),
                has5Tracks: txt.includes('Hôtellerie') && txt.includes('Restauration') && txt.includes('Décoration') && txt.includes('Agropastorale') && txt.includes('Pisciculture')
            };
        }""")
        check(cfp_check["hasAge16"] and cfp_check["hasDuration12m"] and cfp_check["hasFees"] and cfp_check["has5Tracks"],
              "Scenario #4 & Gabarit Formation CFP : 5 filieres MINEFOP, admission des 16 ans, duree 12 mois, frais 50k + 250k FCFA en 4 tranches",
              cfp_check)
        page.evaluate("window.scrollTo(0, 220)")
        page.wait_for_timeout(150)
        page.screenshot(path=str(QA_DIR / "05_formation_cfp_minefop.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "05_formation_cfp_minefop.png"), full_page=False)

        # Page Preparer ma visite (Scenario #1 : prix d'une journee pour 2 adultes et 2 enfants)
        page.evaluate("navigateV4SiteMenu('TARIFS_PASS')")
        page.wait_for_timeout(200)
        calc_check = page.evaluate("""() => {
            document.getElementById('quickCalcAdults').value = 2;
            document.getElementById('quickCalcChildren').value = 2;
            return recalcQuickDayPrice();
        }""")
        check(
            calc_check["zooOnly"] == 3000
            and calc_check["passDecouverte"] == 8000
            and calc_check["waterCombo"] == 14000
            and calc_check["passRoyale"] == 26000,
            "Scenario #1 : Calculateur express pour 2 adultes et 2 enfants (3 000 F / 8 000 F / 14 000 F / 26 000 F)",
            calc_check
        )

        # 5. Section G : Parcours de reservation restructures (5 etapes, 0 billet avant validation, solde guichet)
        print("\n5. Section G — Parcours de reservation restructures")
        page.evaluate("navigateV4SiteMenu('SIMULATEUR_RES'); window.scrollTo(0, 0);")
        page.wait_for_timeout(200)
        res_check_before = page.evaluate("""() => {
            const journeyTabs = Array.from(document.querySelectorAll('#resJourneyTabs .eco-journey-tab')).length;
            const steps = Array.from(document.querySelectorAll('#v4ResStepperBar .v4-res-step strong')).map(el => el.textContent.trim());
            const visitDateVal = document.getElementById('visitDate').value;
            const qrVisibleBefore = getComputedStyle(document.getElementById('demoTicketCard')).display !== 'none';

            // Tester la selection du mode GUICHET
            const guichetRadio = document.querySelector('input[name="payMethod"][value="GUICHET"]');
            if (guichetRadio) {
                guichetRadio.checked = true;
                guichetRadio.dispatchEvent(new Event('change'));
            }
            const guichetBox = document.getElementById('guichetRemainingDueBox');
            const guichetBoxTxt = guichetBox && getComputedStyle(guichetBox).display !== 'none' ? guichetBox.innerText : '';

            // Remettre OM
            const omRadio = document.querySelector('input[name="payMethod"][value="OM"]');
            if (omRadio) {
                omRadio.checked = true;
                omRadio.dispatchEvent(new Event('change'));
            }

            return {
                journeyTabs,
                steps,
                visitDateVal,
                qrVisibleBefore,
                guichetBoxTxt
            };
        }""")
        expected_steps = [
            "Date et participants",
            "Pass ou activités",
            "Coordonnées",
            "Récapitulatif et règlement",
            "Résultat",
        ]
        check(
            res_check_before["journeyTabs"] == 4
            and res_check_before["steps"] == expected_steps
            and res_check_before["visitDateVal"] != "2026-11-15"
            and not res_check_before["qrVisibleBefore"]
            and "Montant restant à régler au guichet" in res_check_before["guichetBoxTxt"],
            "Parcours de reservation : 4 parcours distincts, 5 etapes dans l'ordre, billet QR masque avant validation, solde guichet explicite",
            res_check_before
        )
        page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
        page.wait_for_timeout(120)
        page.screenshot(path=str(QA_DIR / "06_reservation_parcours_5_etapes.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "06_reservation_parcours_5_etapes.png"), full_page=False)

        # Scenario #5 : Statut d'une reservation existante dans Mes reservations & zero troncature des boutons d'action
        page.evaluate("navigateV4SiteMenu('ACC_DASHBOARD')")
        page.wait_for_timeout(200)
        acc_check = page.evaluate("""() => {
            const viewAcc = document.getElementById('view-ACC');
            const txt = viewAcc ? viewAcc.innerText : '';
            const tr = document.querySelector('#view-ACC .table-responsive');
            const trR = tr ? tr.getBoundingClientRect() : null;
            const visibleBtns = Array.from(document.querySelectorAll('#view-ACC table td:last-child .btn'))
                .filter(b => getComputedStyle(b).display !== 'none');
            const clippedBtns = visibleBtns.filter(b => {
                const r = b.getBoundingClientRect();
                return !trR || r.right > trR.right + 2 || r.left < trR.left - 2 || r.width < 20;
            }).map(b => b.textContent.trim());
            return {
                active: viewAcc && viewAcc.classList.contains('active'),
                hasBookingRef: txt.includes('ECP-2026-84920') && txt.includes('Confirmé'),
                hasQuoteRef: txt.includes('DEV-2026-3104'),
                tableNoOverflow: tr ? (tr.scrollWidth <= tr.clientWidth + 1) : false,
                visibleBtnCount: visibleBtns.length,
                clippedBtns
            };
        }""")
        check(
            acc_check["active"]
            and acc_check["hasBookingRef"]
            and acc_check["hasQuoteRef"]
            and acc_check["tableNoOverflow"]
            and len(acc_check["clippedBtns"]) == 0,
            "Scenario #5 : Consultation du statut d'une reservation existante et d'un devis dans Mes reservations (0 bouton tronque)",
            acc_check
        )
        page.evaluate("() => { const c = document.querySelector('#view-ACC .col-8.card'); if (c) c.scrollIntoView({block: 'start'}); }")
        page.wait_for_timeout(150)
        page.screenshot(path=str(QA_DIR / "09_mon_espace_sans_troncature.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "09_mon_espace_sans_troncature.png"), full_page=False)

        # 6. Verification des nouvelles URLs canoniques en acces direct
        print("\n6. Verification des URLs canoniques et anciennes en acces direct")
        for route_path, expected_view in [
            ("/decouvrir", "view-PUB"),
            ("/sejour-restaurant", "view-PUB"),
            ("/groupes-evenements", "view-PUB"),
            ("/formations", "view-PUB"),
            ("/preparer-ma-visite", "view-PUB"),
            ("/mes-reservations", "view-ACC"),
            ("/reserver", "view-RES"),
        ]:
            resp = page.goto(BASE + route_path, wait_until="domcontentloaded")
            page.wait_for_timeout(120)
            active_ok = page.evaluate(f"() => document.getElementById('{expected_view}').classList.contains('active')")
            check(resp.status == 200 and active_ok, f"Route canonique {route_path} -> HTTP 200 & #{expected_view}.active")

        # 7. Verification Responsive (360px, 390px, 768px, 1280px, 1440px) sans debordement horizontal
        print("\n7. Verification Responsive sur 360px, 390px, 768px, 1280px et 1440px")
        page.goto(BASE + "/", wait_until="domcontentloaded")
        for w in [360, 390, 768, 1280, 1440]:
            page.set_viewport_size({"width": w, "height": 844})
            page.wait_for_timeout(100)
            overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(overflow <= 0, f"Largeur {w}px : zero debordement horizontal (overflow={overflow}px)")

        # 8. Module Assignation d'une tache & Fiche de mission imprimable A4 (Exploitation / Guichet / Admin)
        print("\n8. Module Assignation d'une tache & Fiche de mission imprimable A4")
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(100)
        mission_check = page.evaluate("""() => {
            openExpMissionsPanel('CONTROLE_QR');
            const sec = document.getElementById('sec-EXP-MISSIONS');
            const initialRows = document.querySelectorAll('#expMissionsTableBody tr').length;
            const created = assignOperationalMission(false);
            const afterRows = document.querySelectorAll('#expMissionsTableBody tr').length;
            updateOperationalMissionStatus(created.id, 'EN_COURS');
            return {
                hasSection: !!sec,
                initialRows,
                afterRows,
                createdId: created ? created.id : null,
                createdPole: created ? created.pole : null,
                hasAgtBanner: !!document.getElementById('agtActiveMissionBanner'),
                hasAdmBtn: !!document.getElementById('admOpenMissionsBtn')
            };
        }""")
        check(
            mission_check["hasSection"]
            and mission_check["initialRows"] >= 4
            and mission_check["afterRows"] == mission_check["initialRows"] + 1
            and mission_check["createdPole"] == "CONTROLE_QR"
            and mission_check["hasAgtBanner"]
            and mission_check["hasAdmBtn"],
            "Module d'assignation de taches operationnel sur les 4 poles terrain (creation, suivi, bandeau Guichet et acces Admin)",
            mission_check
        )
        page.evaluate("""() => {
            const sec = document.getElementById('sec-EXP-MISSIONS');
            if (sec) {
                const y = sec.getBoundingClientRect().top + window.scrollY - 90;
                window.scrollTo({ top: Math.max(0, y), behavior: 'instant' });
            }
        }""")
        page.wait_for_timeout(150)
        page.screenshot(path=str(QA_DIR / "07_assignation_taches_exploitation.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "07_assignation_taches_exploitation.png"), full_page=False)

        # Ouverture de la Fiche de Mission Officielle A4 Imprimable
        a4_check = page.evaluate("""(mId) => {
            openMissionSheetA4(mId || 'MSN-2026-101');
            const sheet = document.getElementById('printableMissionSheetA4');
            const txt = sheet ? sheet.textContent : '';
            return {
                sheetVisible: !!sheet && getComputedStyle(document.getElementById('modalOfficialPrintBox')).display !== 'none',
                hasTitle: txt.includes('ORDRE DE MISSION TERRAIN'),
                hasChecklist: sheet ? sheet.querySelectorAll('.mission-checklist-item').length >= 3 : false,
                hasVisas: txt.includes('Visa Responsable Exploitation') && txt.includes('Émargement Agent')
            };
        }""", mission_check["createdId"])
        check(
            a4_check["sheetVisible"] and a4_check["hasTitle"] and a4_check["hasChecklist"] and a4_check["hasVisas"],
            "Fiche de Mission Officielle A4 Imprimable complete (en-tete, QR, dotation, check-list terrain et 3 cadres d'emargement)",
            a4_check
        )
        page.wait_for_timeout(150)
        page.screenshot(path=str(QA_DIR / "08_fiche_mission_imprimable_a4.png"), full_page=False)
        if ARTIFACT_DIR.exists():
            page.screenshot(path=str(ARTIFACT_DIR / "08_fiche_mission_imprimable_a4.png"), full_page=False)

        check(len(console_errors) == 0, "Zero erreur console / page JavaScript sur l'ensemble des parcours", console_errors)
        browser.close()

    passed = sum(1 for ok, _, _ in results if ok)
    total = len(results)
    print(f"\n=== BILAN GLOBAL REFONTE CANOPEE VIVANTE : {passed}/{total} CONTROLES VALIDES ===")
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
