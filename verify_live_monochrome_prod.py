# -*- coding: utf-8 -*-
"""
Audit automatisé de la version en production : https://ecopark-cameroun-ahala.vercel.app
Vérifie :
1. Routes HTTP 200
2. Zéro erreur console / réseau / image cassée
3. Zéro emoji OS coloré dans le DOM visible + présence des icônes SVG linéaires monochromes (.svg-mono, .icon-medallion)
4. Pureté chromatique 60-30-10 (#childPriceProtectionAlert en #EDF4E7, zéro boîte bleue/jaune au repos)
5. Zéro préfixe technique (PUB-xx, RES-xx...) visible en mode visiteur
6. Parcours E2E Sprint 1 (Devis Groupe, Candidature CFP, Billet QR & Anti-fraude double scan au Guichet)
"""

import urllib.request
from playwright.sync_api import sync_playwright

BASE_URL = "https://ecopark-cameroun-ahala.vercel.app"

ROUTES = [
    "/",
    "/nos-tarifs",
    "/restaurant",
    "/hotellerie",
    "/formation",
    "/reserver",
    "/rdv",
    "/guichet",
    "/direction",
    "/admin",
    "/favicon.ico",
]

def run_live_audit():
    print("=== 1. VERIFICATION DES ROUTES HTTP EN PRODUCTION ===")
    for r in ROUTES:
        req = urllib.request.Request(BASE_URL + r, headers={"User-Agent": "ECOPARK-QA/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.getcode()
            print(f"  [HTTP {status}] {BASE_URL}{r}")
            assert status == 200, f"Route {r} returned {status}"

    print("\n=== 2. AUDIT PLAYWRIGHT DOM, SVG MONOCHROME, COULEURS 60-30-10 & E2E ===")
    console_errors = []
    page_errors = []
    failed_requests = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))
        page.on("response", lambda res: failed_requests.append((res.status, res.url)) if res.status >= 400 else None)

        page.goto(BASE_URL + "/?cb=" + str(int(__import__("time").time())), wait_until="networkidle")
        page.wait_for_timeout(500)

        # A. Images chargées
        img_stats = page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            const broken = imgs.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
            return { total: imgs.length, broken };
        }""")
        print(f"  [IMAGES] Total: {img_stats['total']} | Cassees: {len(img_stats['broken'])}")
        assert len(img_stats["broken"]) == 0, f"Images cassees: {img_stats['broken']}"

        # B. Icônes SVG Monochromes & Zéro Emoji OS
        svg_stats = page.evaluate("""() => {
            const svgs = document.querySelectorAll('svg.svg-mono');
            const medallions = document.querySelectorAll('.icon-medallion');
            const html = document.documentElement.innerHTML;
            const highChars = [];
            for (const ch of html) {
                if (ch.codePointAt(0) > 0x25FF) highChars.push(ch);
            }
            return {
                svgCount: svgs.length,
                medallionCount: medallions.length,
                highCharsCount: highChars.length,
                sampleStrokeWidth: svgs.length ? svgs[0].getAttribute('stroke-width') : null,
                sampleStroke: svgs.length ? svgs[0].getAttribute('stroke') : null
            };
        }""")
        print(f"  [SVG MONOCHROME] .svg-mono: {svg_stats['svgCount']} | .icon-medallion: {svg_stats['medallionCount']} | Emojis restants: {svg_stats['highCharsCount']} | stroke={svg_stats['sampleStroke']} ({svg_stats['sampleStrokeWidth']}px)")
        assert svg_stats["svgCount"] >= 20, "Nombre d'icones SVG insuffisant"
        assert svg_stats["medallionCount"] >= 8, "Nombre de medaillons SVG insuffisant"
        assert svg_stats["highCharsCount"] == 0, f"Emojis restants detectes: {svg_stats['highCharsCount']}"

        # C. Pureté Chromatique 60-30-10 & 3e Couleur Ocre Bronze (#C47D2B / #FBF5EC)
        color_check = page.evaluate("""() => {
            const pill = document.querySelector('.price-pill');
            const pillCs = window.getComputedStyle(pill);
            const ochreBtn = document.querySelector('.btn-ochre-outline');
            const ochreBtnCs = window.getComputedStyle(ochreBtn);
            navigateFamily('RES', 'RES-03');
            const alertEl = document.getElementById('childPriceProtectionAlert');
            const cs = window.getComputedStyle(alertEl);
            return {
                className: alertEl.className,
                bg: cs.backgroundColor,
                color: cs.color,
                pillBg: pillCs.backgroundColor,
                pillColor: pillCs.color,
                ochreBtnBg: ochreBtnCs.backgroundColor
            };
        }""")
        print(f"  [60-30-10 + OCRE BRONZE] #childPriceProtectionAlert bg={color_check['bg']} | .price-pill bg={color_check['pillBg']} text={color_check['pillColor']} | .btn-ochre-outline bg={color_check['ochreBtnBg']}")
        assert "monochrome-callout" in color_check["className"]
        assert color_check["bg"] == "rgb(237, 244, 231)", f"Fond inattendu: {color_check['bg']}"
        assert color_check["pillBg"] == "rgb(251, 245, 236)", f"Fond .price-pill Ocre Bronze inattendu: {color_check['pillBg']}"
        # C2. Verification de la Mise en Exergue Photographique (Hero 455px, Bento 340px, Mosaique Galerie PUB-14 & Lightbox)
        photo_check = page.evaluate("""() => {
            navigateFamily('PUB', 'PUB-01');
            const heroFrame = document.getElementById('heroShowcaseFrame');
            const heroH = heroFrame ? heroFrame.getBoundingClientRect().height : 0;
            const heroThumbs = document.querySelectorAll('.hero-thumb-btn').length;
            window.setHeroShowcase(2, document.querySelectorAll('.hero-thumb-btn')[2]);
            const switchedHeroSrc = document.getElementById('heroShowcaseImg').getAttribute('src');

            const bentoMedia = document.querySelector('.bento-card .card-media-wrapper');
            const bentoH = bentoMedia ? bentoMedia.offsetHeight : 0;
            const zoomPills = document.querySelectorAll('.photo-zoom-pill').length;
            const mosaicItems = document.querySelectorAll('.gallery-mosaic-item').length;

            // Test Lightbox plein ecran
            window.openEcoparkLightbox(1);
            const lbOpen = document.getElementById('ecoparkLightbox').classList.contains('open');
            const lbTitle1 = document.getElementById('lightboxTitle').textContent.trim();
            window.stepEcoparkLightbox(1);
            const lbTitle2 = document.getElementById('lightboxTitle').textContent.trim();
            window.closeEcoparkLightbox();
            const lbClosed = !document.getElementById('ecoparkLightbox').classList.contains('open');

            return {
                heroH: Math.round(heroH),
                heroThumbs,
                switchedHeroSrc,
                bentoH: Math.round(bentoH),
                zoomPills,
                mosaicItems,
                lbOpen,
                lbTitle1,
                lbTitle2,
                lbClosed
            };
        }""")
        print(f"  [PHOTO SPOTLIGHT] Hero: {photo_check['heroH']}px ({photo_check['heroThumbs']} vues) | Bento: {photo_check['bentoH']}px | Loupes: {photo_check['zoomPills']} | Mosaique: {photo_check['mosaicItems']} | Lightbox: open={photo_check['lbOpen']} -> '{photo_check['lbTitle1']}' -> '{photo_check['lbTitle2']}' -> closed={photo_check['lbClosed']}")
        assert photo_check["heroH"] == 455, f"Hauteur Hero inattendue: {photo_check['heroH']}"
        assert photo_check["heroThumbs"] == 4, f"Nombre de miniatures Hero inattendu: {photo_check['heroThumbs']}"
        assert photo_check["bentoH"] == 340, f"Hauteur Bento inattendue: {photo_check['bentoH']}"
        assert photo_check["mosaicItems"] == 6, f"Nombre d'elements mosaique inattendu: {photo_check['mosaicItems']}"
        assert photo_check["lbOpen"] and photo_check["lbClosed"] and photo_check["lbTitle1"] != photo_check["lbTitle2"], "Erreur cycle Lightbox"

        # C3. Verification des 3 Animations HyperFrames (heygen-com/hyperframes)
        hf_check = page.evaluate("""() => {
            navigateFamily('PUB', 'PUB-01');
            const tlKeys = Object.keys(window.__timelines || {});
            // Test Animation 1 : Hero Scene Reel + Sync KPI
            window.setHeroShowcase(1, document.querySelectorAll('.hero-thumb-btn')[1]);
            const kpi1Active = document.getElementById('heroKpiCard1').classList.contains('kpi-active-sync');
            const captionText = document.getElementById('heroSceneCaptionText').textContent.trim();
            const playheadBars = document.querySelectorAll('.hero-playhead-bar').length;

            // Test Animation 2 : Carte Vectorielle SVG du Parc Ahala (Zones A -> E) & Staggered Bento
            const svgExists = !!document.getElementById('ahalaTrailSvg');
            const activePathExists = !!document.getElementById('ahalaActivePath');
            window.selectAhalaZone(3);
            const zone3Text = document.getElementById('ahalaZoneDetailText').textContent.trim();
            const staggerClips = document.querySelectorAll('.bento-card.clip, .gallery-mosaic-item.clip').length;

            // Test Animation 3 : Kinetic FCFA Odometer & Apple Wallet QR Pass 3D Reveal
            navigateFamily('RES', 'RES-03');
            window.changeCount('adults', 1);
            const updatedTotalText = document.getElementById('grandTotalFCFA').textContent.trim();
            const updatedTargetAttr = document.getElementById('grandTotalFCFA').getAttribute('data-target-fcfa');
            window.changeCount('adults', -1);
            const sheenExists = !!document.getElementById('qrPassSheen');
            window.__timelines['ecopark-qr-pass'].play();

            return {
                tlKeys,
                kpi1Active,
                captionText,
                playheadBars,
                svgExists,
                activePathExists,
                zone3Text,
                staggerClips,
                updatedTotalText,
                updatedTargetAttr,
                sheenExists
            };
        }""")
        print(f"  [HYPERFRAMES TIMELINES] Registre: {hf_check['tlKeys']} | Playheads: {hf_check['playheadBars']} | Clips Bento/Mosaique: {hf_check['staggerClips']}")
        print(f"  [HYPERFRAMES ANIM 1]    KPI Piscine Sync: {hf_check['kpi1Active']} | Caption: '{hf_check['captionText']}'")
        print(f"  [HYPERFRAMES ANIM 2]    SVG Trail: {hf_check['svgExists']} | Zone D Detail: '{hf_check['zone3Text'][:65]}...'")
        print(f"  [HYPERFRAMES ANIM 3]    Odometre FCFA (+1 adulte): {hf_check['updatedTotalText']} (target={hf_check['updatedTargetAttr']}) | QR Sheen 3D: {hf_check['sheenExists']}")
        assert "ecopark-hero-reel" in hf_check["tlKeys"], "Timeline ecopark-hero-reel manquante"
        assert "ecopark-ahala-map" in hf_check["tlKeys"], "Timeline ecopark-ahala-map manquante"
        assert "ecopark-qr-pass" in hf_check["tlKeys"], "Timeline ecopark-qr-pass manquante"
        assert hf_check["kpi1Active"], "La carte KPI Piscine n'est pas synchronisee avec la scene 2 du Hero"
        assert hf_check["playheadBars"] == 4, "Les 4 barres de progression .hero-playhead-bar sont manquantes"
        assert hf_check["svgExists"] and hf_check["activePathExists"], "La carte vectorielle SVG #ahalaTrailSvg est manquante"
        assert hf_check["staggerClips"] == 12, f"Attendu 12 clips Stagger Bento/Mosaique, obtenu {hf_check['staggerClips']}"
        assert hf_check["updatedTargetAttr"] == "18500", f"Odometre FCFA inattendu: {hf_check['updatedTargetAttr']}"
        assert hf_check["sheenExists"], "Le reflet speculaire #qrPassSheen est manquant sur #demoTicketCard"

        # Capture des 3 visuels de validation HyperFrames en production
        art_dir = r"C:\Users\PcGamerCm\.gemini\antigravity\brain\a7ec3e06-7022-4aad-b64e-501927169ab1"
        page.evaluate("navigateFamily('PUB', 'PUB-01'); setHeroShowcase(1, document.querySelectorAll('.hero-thumb-btn')[1]);")
        page.wait_for_timeout(450)
        page.screenshot(path=art_dir + r"\hf_live_1_hero_reel_sync.png")

        page.locator("#ahalaMapContainer").scroll_into_view_if_needed()
        page.evaluate("selectAhalaZone(3);")
        page.wait_for_timeout(450)
        page.screenshot(path=art_dir + r"\hf_live_2_ahala_svg_map.png")

        page.evaluate("navigateFamily('RES', 'RES-03'); changeCount('adults', 1); createLiveBookingSprint1();")
        page.locator("#demoTicketCard").scroll_into_view_if_needed()
        page.wait_for_timeout(450)
        page.screenshot(path=art_dir + r"\hf_live_3_odometer_qr_pass_3d.png")

        page.evaluate("navigateFamily('PUB', 'PUB-18');")
        page.locator("#sec-PUB-18").scroll_into_view_if_needed()
        page.wait_for_timeout(450)
        page.screenshot(path=art_dir + r"\hf_live_5_prise_de_rdv_section.png")

        page.evaluate("openRdvModalSprint1('reperage_mariage'); selectRdvSlot('11h00 – 12h00'); submitRdvSprint1();")
        page.wait_for_timeout(450)
        page.screenshot(path=art_dir + r"\hf_live_4_prise_de_rdv_modal.png")
        page.evaluate("closeSprint1Modals();")

        # D. Vérification qu'aucun code technique (PUB-xx, RES-xx) n'est visible en mode visiteur
        leaked_codes = page.evaluate("""() => {
            document.body.classList.remove('inspector-active');
            const familias = ['PUB', 'RES', 'ACC', 'AGT', 'EXP', 'DIR', 'ADM'];
            const leaks = [];
            for (const f of familias) {
                navigateFamily(f);
                const visibleHeadings = Array.from(document.querySelectorAll('h1, h2, h3, .eyebrow'))
                    .filter(el => el.offsetParent !== null)
                    .map(el => el.innerText.trim());
                for (const txt of visibleHeadings) {
                    if (/(PUB|RES|ACC|AGT|EXP|DIR|ADM|DS)-\\d{2}/.test(txt)) {
                        leaks.push({ family: f, text: txt });
                    }
                }
            }
            navigateFamily('PUB', 'PUB-01');
            return leaks;
        }""")
        print(f"  [VISITOR CLEANLINESS] Codes techniques visibles dans les titres en mode visiteur: {len(leaked_codes)}")
        if leaked_codes:
            for lk in leaked_codes:
                print(f"    -> Fuite detectee [{lk['family']}]: {lk['text']}")
        assert len(leaked_codes) == 0, f"Codes techniques visibles en mode visiteur: {leaked_codes}"

        # E. Test E2E Sprint 1 : Devis Groupe -> Candidature CFP -> Billet QR -> Double Scan Guichet
        e2e_result = page.evaluate("""() => {
            // 1. Devis Groupe
            window.openQuoteModalSprint1();
            document.getElementById('quoteOrgName').value = 'Collège Bilingue Ahala';
            document.getElementById('quotePhone').value = '+237 697 13 62 03';
            document.getElementById('quotePax').value = '35';
            window.submitGroupQuoteSprint1();
            const quotes = window.loadDB().quotes;

            // 1b. Candidature CFP
            window.openCfpModalSprint1();
            document.getElementById('cfpCandidateName').value = 'M. Jean-Paul MBARGA';
            window.submitCfpApplicationSprint1();
            const cfpApps = window.loadDB().cfpApplications;

            // 1c. Prise de RDV (Repérage / B2B / Écoles / CFP)
            window.openRdvModalSprint1('seminaire_b2b');
            window.selectRdvSlot('14h00 – 15h00');
            document.getElementById('rdvVisitorName').value = 'Dr Christophe FOE NDI';
            document.getElementById('rdvOrgName').value = 'Direction Générale & Séminaire';
            const rdvRef = window.submitRdvSprint1();
            window.closeSprint1Modals();
            const rdvList = window.loadDB().appointments || [];

            // 2. Generation Billet QR
            navigateFamily('RES', 'RES-03');
            const refBefore = document.getElementById('qrScanInput').value.trim();
            window.createLiveBookingSprint1();
            const refAfter = document.getElementById('qrScanInput').value.trim();

            // 3. Premier scan au Guichet (VALIDE)
            navigateFamily('AGT', 'AGT-05');
            document.getElementById('qrScanInput').value = refAfter;
            window.verifyLiveQrCode();
            const firstScanTitle = document.getElementById('scanResultTitle').textContent.trim();

            // 4. Second scan immediat du meme billet (DEJA UTILISE)
            window.verifyLiveQrCode();
            const secondScanTitle = document.getElementById('scanResultTitle').textContent.trim();

            // 5. Septieme verdict (UNKNOWN) : verifier l'absence de balises HTML brutes dans textContent
            window.triggerScanVerdict('UNKNOWN');
            const unknownScanTitle = document.getElementById('scanResultTitle').textContent.trim();

            return {
                latestQuoteId: quotes[0] ? quotes[0].reference : null,
                latestCfpId: cfpApps[0] ? cfpApps[0].reference : null,
                latestRdvId: rdvList[0] ? rdvList[0].reference : rdvRef,
                refBefore,
                refAfter,
                firstScanTitle,
                secondScanTitle,
                unknownScanTitle
            };
        }""")
        print(f"  [E2E SPRINT 1] Devis: {e2e_result['latestQuoteId']} | CFP: {e2e_result['latestCfpId']} | RDV: {e2e_result['latestRdvId']} | Billet: {e2e_result['refAfter']}")
        assert e2e_result["latestRdvId"] and e2e_result["latestRdvId"].startswith("RDV-2026-"), f"RDV non cree: {e2e_result['latestRdvId']}"
        print(f"  [E2E SCAN 1]   {e2e_result['firstScanTitle']}")
        print(f"  [E2E SCAN 2]   {e2e_result['secondScanTitle']}")
        print(f"  [E2E SCAN 7]   {e2e_result['unknownScanTitle']}")
        assert e2e_result["refAfter"] != e2e_result["refBefore"], "Le billet QR n'a pas ete regenere"
        assert "BILLET VALIDE" in e2e_result["firstScanTitle"], f"1er scan invalide: {e2e_result['firstScanTitle']}"
        assert "DÉJÀ UTILISÉ" in e2e_result["secondScanTitle"], f"2nd scan non rejete: {e2e_result['secondScanTitle']}"
        assert "<svg" not in e2e_result["unknownScanTitle"] and "<span" not in e2e_result["unknownScanTitle"], f"Balises HTML brutes dans scanResultTitle: {e2e_result['unknownScanTitle']}"

        browser.close()

    print(f"\n=== 3. BILAN DES ERREURS CONSOLE & RESEAU ===")
    print(f"  Console errors : {len(console_errors)}")
    print(f"  Page errors    : {len(page_errors)}")
    print(f"  Failed HTTP req: {len(failed_requests)}")
    assert len(console_errors) == 0, f"Console errors: {console_errors}"
    assert len(page_errors) == 0, f"Page errors: {page_errors}"
    assert len(failed_requests) == 0, f"Failed requests: {failed_requests}"
    print("\n[SUCCES TOTAL] La version en production https://ecopark-cameroun-ahala.vercel.app est 100 % conforme et sans aucune erreur.")

if __name__ == "__main__":
    run_live_audit()
