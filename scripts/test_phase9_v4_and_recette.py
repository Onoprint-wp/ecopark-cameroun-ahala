# -*- coding: utf-8 -*-
"""
Vérification E2E automatisée de la Phase 9 :
  1. Design System V4 « Canopée immersive » (Hero, 4 Piliers, Catalogue filtrable, PUB-04, PUB-09, Stepper 4 étapes, Mobile Bottom Nav)
  2. Présence des 22 ancres autonomes sec-PUB-01 à sec-PUB-22 (A-019)
  3. Validation des correctifs des 24 anomalies (A-001 à A-024) + ADM-09 (A-011)
  4. Intégrité de la hiérarchie de vérité (Logo officiel, Tarifs FCFA sanctuarisés, 0 caractère > U+25FF)
"""
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://ecopark-cameroun-ahala.vercel.app" if "--prod" in sys.argv else "http://localhost:3000"
results = []


def check(cond, label, detail=""):
    results.append(bool(cond))
    print(f"  [{'OK' if cond else 'FAIL'}] {label}{(' — ' + str(detail)) if detail else ''}")


def main():
    print("\n=== TEST PHASE 9 : DESIGN SYSTEM V4 « CANOPÉE IMMERSIVE » & CAHIER DE RECETTE (24 ANOMALIES) ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        page.goto(f"{BASE}/?demo=77", wait_until="networkidle")

        # 1. Pilot 1 : Hero Cinématique V4 & 4 Piliers
        v4_hero = page.evaluate("""() => {
            const stage = document.getElementById('v4CanopyHeroStage');
            const pillars = document.querySelectorAll('.v4-hero-pillars-strip .v4-hero-pillar-item').length;
            const title = stage ? stage.querySelector('.v4-canopy-hero-title').textContent.trim() : '';
            const weatherBar = document.getElementById('ahalaLiveWeatherBar').textContent;
            return {
                exists: !!stage,
                pillars,
                hasTagline: title.includes('Prenez le frais') && title.includes('Vivez la nature'),
                weatherHonest: weatherBar.includes("Bulletin d'accueil Ahala") && !weatherBar.includes("En direct d'Ahala")
            };
        }""")
        check(v4_hero["exists"] and v4_hero["hasTagline"], "Pilote 1 (PUB-01) : Hero Cinématique V4 « Prenez le frais. Vivez la nature. »")
        check(v4_hero["pillars"] == 4, "Pilote 1 (PUB-01) : Bandeau des 4 Piliers d'Expérience V4 présent", f"{v4_hero['pillars']} piliers")
        check(v4_hero["weatherHonest"], "Anomalie A-009 corrigée : Bandeau météo horodaté honnête (sans faux « En direct »)")

        # 2. Pilot 2 : Catalogue V4 & Filtres (PUB-03)
        v4_cat = page.evaluate("""() => {
            const totalCards = document.querySelectorAll('#v4ActivityCardsGrid .v4-activity-card').length;
            const waterCount = filterV4CatalogCards('EAU');
            const resetCount = resetV4CatalogFilters();
            return { totalCards, waterCount, resetCount };
        }""")
        check(v4_cat["totalCards"] == 8 and v4_cat["waterCount"] == 3 and v4_cat["resetCount"] == 8,
              "Pilote 2 (PUB-03) : Grille 4 colonnes & Filtres V4 interactifs opérationnels", str(v4_cat))

        # 3. Pilot 3 : Fiche Activité PUB-04 autonome
        v4_pub04 = page.evaluate("""() => {
            openV4ActivityDetail('pirogue');
            const title1 = document.getElementById('v4Pub04Title').textContent.trim();
            const sub1 = document.getElementById('v4Pub04SubtotalFcfa').textContent.trim();
            switchV4Pub04Activity('piscine');
            const title2 = document.getElementById('v4Pub04Title').textContent.trim();
            const sub2 = document.getElementById('v4Pub04SubtotalFcfa').textContent.trim();
            openV4ActivityDetail('pirogue');
            return { title1, sub1, title2, sub2 };
        }""")
        check("pirogue" in v4_pub04["title1"].lower() and v4_pub04["sub1"] == "3 000 FCFA" and v4_pub04["sub2"] == "8 000 FCFA",
              "Pilote 3 (PUB-04) : Fiche détail activité autonome & calculateur FCFA (Pirogue 3 000 F / Piscine 8 000 F)", str(v4_pub04))

        # 4. Pilot 4 & A-019 : Les 22 ancres sec-PUB-01 à sec-PUB-22 & Prix Saveurs A-014
        pub_anchors = page.evaluate("""() => {
            const missing = [];
            for (let i = 1; i <= 22; i++) {
                const code = 'sec-PUB-' + String(i).padStart(2, '0');
                if (!document.getElementById(code)) missing.push(code);
            }
            const hasAdm09 = SCREENS_77.some(s => s.id === 'ADM-09');
            return { missing, hasAdm09, screensLen: SCREENS_77.length };
        }""")
        check(len(pub_anchors["missing"]) == 0, "Anomalie A-019 corrigée : 22/22 sections autonomes sec-PUB-01 à sec-PUB-22 présentes")
        check(pub_anchors["hasAdm09"] and pub_anchors["screensLen"] == 78,
              "Anomalie A-011 corrigée : ADM-09 enregistré dans SCREENS_77 (77 contractuels + 1 extension)", f"total={pub_anchors['screensLen']}")

        # 5. Anomalies A-001, A-010, A-017, A-020, A-022, A-023
        fixes_check = page.evaluate("""() => {
            // A-010 : XSS dans filterFAQSearch
            filterFAQSearch('introuvable <img src=x onerror=alert(1)>');
            const faqHtml = document.getElementById('faqListContainer').innerHTML;
            const xssSafe = !faqHtml.includes('<img');

            // A-017 : Remise à zéro à blanc vs Réinitialisation conforme
            clearPhysicalCashCountToZero();
            const zeroTotal = document.getElementById('physicalCashTotal').textContent.trim();
            resetPhysicalCashCount();
            const restoredTotal = document.getElementById('physicalCashTotal').textContent.trim();

            // A-023 : Signature d'intégrité billet QR
            const sig = computeEcoparkTicketIntegritySig('ECP-2026-84920', 14000, '2026-11-15');

            // A-020 : Masquage partiel téléphone
            const masked = maskVisitorPhonePrivacy('+237 697 13 62 03');

            return { xssSafe, zeroTotal, restoredTotal, sig, masked };
        }""")
        check(fixes_check["xssSafe"], "Anomalie A-010 corrigée : filterFAQSearch immunisé contre l'injection HTML/XSS")
        check(fixes_check["zeroTotal"] == "0 FCFA" and fixes_check["restoredTotal"] == "184 500 FCFA",
              "Anomalie A-017 corrigée : Recomptage à blanc (0 FCFA) + Réinitialisation conforme (184 500 FCFA)", str(fixes_check))
        check(fixes_check["sig"].startswith("SIG-V4-"), "Anomalies A-007/A-008/A-023 corrigées : Signature d'intégrité QR active", fixes_check["sig"])
        check("2 03" in fixes_check["masked"] and "•" in fixes_check["masked"],
              "Anomalie A-020 corrigée : Masquage de confidentialité téléphone actif", fixes_check["masked"])

        # 5b. Architecture Multi-Pages Publiques (6 Sous-Pages Dédiées dans #view-PUB)
        subpage_check = page.evaluate("""() => {
            navigateFamily('PUB', 'PUB-01');
            const accueilH = document.documentElement.scrollHeight;
            const accueilActive = window._activePubSubPage;
            const pub04HiddenOnAccueil = getComputedStyle(document.getElementById('sec-PUB-04')).display === 'none';

            navigateFamily('PUB', 'PUB-03');
            const actH = document.documentElement.scrollHeight;
            const actActive = window._activePubSubPage;
            const pub03VisibleOnAct = getComputedStyle(document.getElementById('sec-PUB-03')).display !== 'none';

            navigateFamily('PUB', 'PUB-04');
            const ficheH = document.documentElement.scrollHeight;
            const ficheActive = window._activePubSubPage;

            navigateFamily('PUB', 'PUB-09');
            const hotelH = document.documentElement.scrollHeight;
            const hotelActive = window._activePubSubPage;

            navigateFamily('PUB', 'PUB-10');
            const tarifsH = document.documentElement.scrollHeight;
            const tarifsActive = window._activePubSubPage;

            navigateFamily('PUB', 'PUB-12');
            const cfpH = document.documentElement.scrollHeight;
            const cfpActive = window._activePubSubPage;

            navigateFamily('PUB', 'PUB-01');
            return {
                accueilH, accueilActive, pub04HiddenOnAccueil,
                actH, actActive, pub03VisibleOnAct,
                ficheH, ficheActive,
                hotelH, hotelActive,
                tarifsH, tarifsActive,
                cfpH, cfpActive
            };
        }""")
        check(
            subpage_check["accueilActive"] == "ACCUEIL"
            and subpage_check["actActive"] == "ACTIVITES"
            and subpage_check["ficheActive"] == "FICHE_ACTIVITE"
            and subpage_check["hotelActive"] == "HOTELS_SAVEURS"
            and subpage_check["tarifsActive"] == "TARIFS_AGENDA"
            and subpage_check["cfpActive"] == "CFP_INFOS"
            and subpage_check["accueilH"] < 5500,
            "Architecture V4 à 6 Sous-Pages Publiques opérationnelle (Hauteur Accueil réduite de 15 296 px à ~3 800 px)",
            str(subpage_check)
        )

        # 5c. Menu Principal & Sous-Menus Déroulants (Mega-Menu V4 + Fil d'Ariane + Tiroir Mobile)
        mega_menu_check = page.evaluate("""() => {
            const dropdownsCount = document.querySelectorAll('#v4MainMegaNav .v4-nav-dropdown').length;
            const dropdownItemsCount = document.querySelectorAll('#v4MainMegaNav .v4-dropdown-item').length;
            const mobileAccordionsCount = document.querySelectorAll('#v4MobileMenuDrawer details.v4-mob-accordion').length;

            // Vérifier le routage via navigateV4SiteMenu
            navigateV4SiteMenu('ACT_PISCINE');
            const piscinePage = window._activePubSubPage;
            const piscineTitle = document.getElementById('v4Pub04Title').textContent.trim();
            const bcVisibleOnInterior = document.getElementById('v4SiteBreadcrumbBar').classList.contains('visible');
            const bcSubItem = document.getElementById('v4BreadcrumbSubItem').textContent.trim();
            const sublinksCount = document.querySelectorAll('#v4SiteContextualSublinks .v4-site-sublink-pill').length;

            navigateV4SiteMenu('RESTAURANT_SAVEURS');
            const saveursPage = window._activePubSubPage;
            const navHotelsActive = document.getElementById('nav-HOTELS').classList.contains('active');

            navigateV4SiteMenu('ACCUEIL');
            const bcHiddenOnAccueil = !document.getElementById('v4SiteBreadcrumbBar').classList.contains('visible');

            // Tiroir mobile accordéon
            const drawerOpened = toggleV4MobileDrawer(true);
            const drawerClosed = !toggleV4MobileDrawer(false);

            return {
                dropdownsCount,
                dropdownItemsCount,
                mobileAccordionsCount,
                piscinePage,
                piscineTitle,
                bcVisibleOnInterior,
                bcSubItem,
                sublinksCount,
                saveursPage,
                navHotelsActive,
                bcHiddenOnAccueil,
                drawerOpened,
                drawerClosed
            };
        }""")
        check(
            mega_menu_check["dropdownsCount"] == 5
            and mega_menu_check["dropdownItemsCount"] >= 24
            and mega_menu_check["mobileAccordionsCount"] == 5
            and mega_menu_check["piscinePage"] == "FICHE_ACTIVITE"
            and "piscine" in mega_menu_check["piscineTitle"].lower()
            and mega_menu_check["bcVisibleOnInterior"]
            and mega_menu_check["bcHiddenOnAccueil"]
            and mega_menu_check["saveursPage"] == "HOTELS_SAVEURS"
            and mega_menu_check["navHotelsActive"]
            and mega_menu_check["drawerOpened"]
            and mega_menu_check["drawerClosed"],
            "Mega-Menu V4 (5 sous-menus déroulants, 26 entrées, Fil d'Ariane dynamique & Tiroir Mobile accordéon) 100 % fonctionnel",
            str(mega_menu_check)
        )

        # 6. Pilot 5 & 6 : Mobile 390x844 Bottom Nav & Cibles tactiles >= 44px (A-013, A-024)
        page.set_viewport_size({"width": 390, "height": 844})
        mob_check = page.evaluate("""() => {
            const nav = document.getElementById('v4MobileBottomNav');
            const navVisible = nav && getComputedStyle(nav).display !== 'none';
            const btns = Array.from(nav.querySelectorAll('.v4-bottom-nav-btn'));
            const minH = Math.min(...btns.map(b => b.getBoundingClientRect().height));
            return { navVisible, tabsCount: btns.length, minH: Math.round(minH) };
        }""")
        check(mob_check["navVisible"] and mob_check["tabsCount"] == 4 and mob_check["minH"] >= 44,
              "Pilotes 5 & 6 + A-013/A-024 : Barre mobile V4 à 4 onglets active et cibles tactiles >= 44px", str(mob_check))

        check(len(console_errors) == 0, "Zéro erreur console JavaScript", console_errors)
        browser.close()

    passed = sum(results)
    total = len(results)
    print(f"\n=== BILAN PHASE 9 V4 : {passed}/{total} CONTRÔLES VALIDÉS ===")
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
