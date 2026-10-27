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

        # F. Verification des 7 Remediations (Manquements Obligatoire vs Facultatif)
        remediation_check = page.evaluate("""() => {
            // 1. CFP : 5 filieres + rejet age < 16 ans + validation age >= 16 ans + 4 tranches
            window.openCfpModalSprint1();
            const cfpTrackCount = document.querySelectorAll('#cfpTrack option').length;
            const cfpPlanCount = document.querySelectorAll('#cfpPaymentPlan option').length;
            document.getElementById('cfpAge').value = '14';
            const cfpUnderageRejected = (window.submitCfpApplicationSprint1() === false);
            document.getElementById('cfpAge').value = '20';
            document.getElementById('cfpTrack').value = 'Pisciculture';
            const cfpValidRef = window.submitCfpApplicationSprint1();

            // 2 & 4. Devis Proforma B2B / Ecole / Mariage + Navette
            window.openQuoteModalSprint1();
            document.getElementById('quoteType').value = 'Séminaire Ministère / ONG / Entreprise';
            document.getElementById('quotePax').value = '50';
            document.getElementById('quoteOptShuttle').checked = true;
            window.recalcQuoteProformaPreview();
            const proformaSeminarText = document.getElementById('quoteProformaTotalText').textContent.trim();
            const quoteRef = window.submitGroupQuoteSprint1();

            // 3, 5 & 6. Simulateur : 3 Cites Hotelieres + Nuitees + Navette + Peche + Tarif Piscine Week-end
            navigateFamily('RES', 'RES-03');
            window.applySalesBundle('CUSTOM', false);
            // Remettre 2 adultes, 2 enfants
            counts.adults = 2; counts.children = 2; counts.toddlers = 1;
            document.getElementById('countAdults').textContent = '2';
            document.getElementById('countChildren').textContent = '2';
            document.getElementById('chkZoo').checked = true;
            document.getElementById('chkPiscine').checked = true;
            document.getElementById('chkPirogue').checked = true;
            document.getElementById('chkCheval').checked = false;
            document.getElementById('chkRepas').checked = false;

            // Tester bascule Tarif Piscine Week-end (Enfant 2 500 FCFA au lieu de 1 500 FCFA -> +2 000 FCFA pour 2 enfants)
            document.getElementById('poolRatePeriod').value = 'WEEKEND_PLEIN';
            window.recalcSimulator();
            const subPiscineWeekend = document.getElementById('subPiscine').textContent.trim();
            document.getElementById('poolRatePeriod').value = 'SEMAINE_PROMO';

            // Tester Cite Chanthel (15 000 FCFA) x 2 nuitees = 30 000 FCFA + Navette A/R (2x1500 + 2x1000 = 5 000 FCFA) + Peche (2 000 FCFA)
            document.getElementById('chkBumpLodgeEwondo').checked = true;
            document.getElementById('lodgeCitySelect').value = 'CHANTHEL';
            document.getElementById('lodgeNightsSelect').value = '2';
            document.getElementById('chkBumpNavette').checked = true;
            document.getElementById('chkBumpPeche').checked = true;
            window.recalcSimulator();

            const subLodgeChanthel2N = document.getElementById('subBumpLodge').textContent.trim();
            const subNavette = document.getElementById('subBumpNavette').textContent.trim();
            const subPeche = document.getElementById('subBumpPeche').textContent.trim();
            const waSummary = document.getElementById('waBubbleBodyText').textContent.trim();

            // 7. Validation stricte des champs (Telephone invalide rejete)
            const savedPhone = document.getElementById('visitorPhone').value;
            document.getElementById('visitorPhone').value = '123';
            const emptyNameRejected = (window.createLiveBookingSprint1() === false);
            document.getElementById('visitorPhone').value = savedPhone;

            return {
                cfpTrackCount,
                cfpPlanCount,
                cfpUnderageRejected,
                cfpValidRef,
                proformaSeminarText,
                quoteRef,
                subPiscineWeekend,
                subLodgeChanthel2N,
                subNavette,
                subPeche,
                waHasChanthel: waSummary.includes('Chanthel') && waSummary.includes('Navette'),
                emptyNameRejected
            };
        }""")
        print(f"  [REMEDIATION #1 CFP]     Filieres={remediation_check['cfpTrackCount']} | Plans={remediation_check['cfpPlanCount']} | <16ans rejete={remediation_check['cfpUnderageRejected']} | Ref={remediation_check['cfpValidRef']}")
        print(f"  [REMEDIATION #4 DEVIS]   Seminaire 50 pax + Navette = {remediation_check['proformaSeminarText']} ({remediation_check['quoteRef']})")
        print(f"  [REMEDIATION #3/5/6 SIM] Piscine WE={remediation_check['subPiscineWeekend']} | Chanthel 2N={remediation_check['subLodgeChanthel2N']} | Navette={remediation_check['subNavette']} | Peche={remediation_check['subPeche']}")
        print(f"  [REMEDIATION #2/7 WA/VAL] Sync WhatsApp={remediation_check['waHasChanthel']} | Champ vide bloque={remediation_check['emptyNameRejected']}")

        assert remediation_check["cfpTrackCount"] == 5, "Les 5 filieres CFP sont requises"
        assert remediation_check["cfpPlanCount"] == 2, "Les 2 plans de paiement CFP sont requis"
        assert remediation_check["cfpUnderageRejected"], "L'age < 16 ans doit etre bloque au CFP"
        assert remediation_check["proformaSeminarText"] == "670 000 FCFA", f"Calcul proforma Seminaire inattendu: {remediation_check['proformaSeminarText']}"
        assert remediation_check["subPiscineWeekend"] == "10 000 FCFA", f"Tarif Piscine Week-end inattendu: {remediation_check['subPiscineWeekend']}"
        assert remediation_check["subLodgeChanthel2N"] == "30 000 FCFA", f"Tarif Chanthel 2 nuits inattendu: {remediation_check['subLodgeChanthel2N']}"
        assert remediation_check["subNavette"] == "5 000 FCFA", f"Tarif Navette inattendu: {remediation_check['subNavette']}"
        assert remediation_check["subPeche"] == "2 000 FCFA", f"Tarif Peche inattendu: {remediation_check['subPeche']}"
        assert remediation_check["waHasChanthel"], "La Vue WhatsApp ne synchronise pas les nouvelles options"
        assert remediation_check["emptyNameRejected"], "La validation du champ obligatoire Nom Visiteur n'a pas bloque un champ vide"

        # G. Verification des 4 Optimisations de Positionnement de l'Information
        pos_check = page.evaluate("""() => {
            navigateFamily('PUB', 'PUB-01');
            const routerCards = document.querySelectorAll('#pubQuickIntentRouter .quick-intent-card').length;
            window.routeVisitorByProfile('HOTEL');
            const navHotelsActive = document.getElementById('nav-HOTELS').classList.contains('active');
            const hotelHaloActive = document.getElementById('sec-PUB-08').classList.contains('section-focus-halo');

            navigateFamily('RES', 'RES-03');
            const stickyCol = document.getElementById('resStickySummaryCol');
            const stickyPosition = stickyCol ? window.getComputedStyle(stickyCol).position : '';
            const stickyBarTotal = document.getElementById('stickyBarTotalFcfa') ? document.getElementById('stickyBarTotalFcfa').textContent.trim() : '';
            const mainTotal = document.getElementById('grandTotalFCFA').textContent.trim();

            return {
                routerCards,
                navHotelsActive,
                hotelHaloActive,
                stickyPosition,
                stickyBarSynced: stickyBarTotal === mainTotal && stickyBarTotal.length > 0
            };
        }""")
        print(f"  [POSITIONING #1-4]      Cartes Aiguillage={pos_check['routerCards']} | Nav Hotel Active={pos_check['navHotelsActive']} | Halo Focus={pos_check['hotelHaloActive']} | Col Droite={pos_check['stickyPosition']} | Sticky Bar Sync={pos_check['stickyBarSynced']}")
        assert pos_check["routerCards"] == 4, "Les 4 cartes d'aiguillage #pubQuickIntentRouter sont requises"
        assert pos_check["navHotelsActive"], "Le bouton #nav-HOTELS doit etre actif lors de la navigation vers PUB-08"
        assert pos_check["hotelHaloActive"], "Le halo visuel .section-focus-halo doit s'activer sur #sec-PUB-08"
        assert pos_check["stickyPosition"] == "sticky", f"Position attendue sticky sur #resStickySummaryCol, obtenu: {pos_check['stickyPosition']}"
        assert pos_check["stickyBarSynced"], "La barre mobile #mobileStickyConversionBar n'est pas synchronisee avec le total FCFA"

        # H. Verification du Pack des 7 Omissions (Recherche ACC-01/RES-12, PNG Hors-Ligne, Report Date ACC-05, Cuisine 13h & Navette, Mobile Nav, Meteo/Avis PUB-15, Export CSV DIR-05)
        omissions_check = page.evaluate("""() => {
            // 1. Bandeau Meteo & Avis Verifies PUB-15
            const hasLiveWeatherBar = !!document.getElementById('ahalaLiveWeatherBar');
            const testimonialCount = document.querySelectorAll('#sec-PUB-15 .testimonial-card').length;

            // 2. Selecteurs contextuels Cuisine 13h & Point de ramassage Navette Yaounde
            navigateFamily('RES', 'RES-03');
            document.getElementById('chkRepas').checked = true;
            document.getElementById('simDishSelect').value = "Poulet DG Royal Plantain Mûr";
            document.getElementById('simMealSlotSelect').value = "Service 13h30";
            document.getElementById('chkBumpNavette').checked = true;
            document.getElementById('simShuttlePickupSelect').value = "Départ Carrefour Bastos (09h15)";
            window.recalcSimulator();
            const itemsSummary = window.getActiveSimulatorItemsSummary();

            // 3. Telechargement PNG Hors-Ligne & Impression PDF Billet QR / Proforma
            const dlRef = window.downloadOfflineQrTicketPng();
            window.printOfficialDocument('PROFORMA');
            const printTitle = document.getElementById('officialPrintTitle').textContent.trim();
            window.closeSprint1Modals();

            // 4. Recherche ACC-01 / RES-12 + Filtre CFP + Report de date sans frais (ACC-05)
            navigateFamily('ACC', 'ACC-02');
            window.setAccCategoryFilter('CFP', document.querySelectorAll('#accCategoryFilterBar .acc-filter-pill')[4]);
            const cfpRowsCount = document.querySelectorAll('#view-ACC table tbody tr[data-dossier-kind="CFP"]').length;
            window.setAccCategoryFilter('ALL', document.querySelectorAll('#accCategoryFilterBar .acc-filter-pill')[0]);

            const firstBookingRef = window.loadDB().bookings[0].reference;
            window.openRescheduleModal(firstBookingRef, 'BOOKING');
            document.getElementById('rescheduleNewDate').value = '2026-12-28';
            window.confirmRescheduleSprint1();
            const updatedBookingDate = window.loadDB().bookings[0].date;

            // 5. Navigation tactile mobile (#mobileQuickNavPills) & Export CSV Comptable (DIR-05 / AGT-09)
            const mobilePillsCount = document.querySelectorAll('#mobileQuickNavPills .mobile-quick-pill').length;
            const exportedCsvCount = window.exportEcoparkDatabaseCSV();

            return {
                hasLiveWeatherBar,
                testimonialCount,
                hasKitchenAndShuttleInSummary: itemsSummary.includes('Poulet DG Royal') && itemsSummary.includes('Carrefour Bastos'),
                dlRefValid: dlRef && dlRef.startsWith('ECP-2026-'),
                printTitleHasProforma: printTitle.includes('FACTURE PROFORMA OFFICIELLE'),
                cfpRowsCount,
                updatedBookingDate,
                mobilePillsCount,
                exportedCsvCount
            };
        }""")
        print(f"  [OMISSIONS #1-7]        Meteo={omissions_check['hasLiveWeatherBar']} | Avis={omissions_check['testimonialCount']} | Cuisine+Navette={omissions_check['hasKitchenAndShuttleInSummary']} | PNG Offline={omissions_check['dlRefValid']} | Proforma PDF={omissions_check['printTitleHasProforma']} | CFP Rows={omissions_check['cfpRowsCount']} | Report Date={omissions_check['updatedBookingDate']} | Mobile Pills={omissions_check['mobilePillsCount']} | CSV Exported={omissions_check['exportedCsvCount']} lignes")
        assert omissions_check["hasLiveWeatherBar"], "Bandeau meteo #ahalaLiveWeatherBar manquant"
        assert omissions_check["testimonialCount"] == 4, f"Attendu 4 avis verifies, obtenu {omissions_check['testimonialCount']}"
        assert omissions_check["hasKitchenAndShuttleInSummary"], "Les selecteurs Cuisine 13h et Navette Yaounde ne remontent pas dans le recapitulatif"
        assert omissions_check["dlRefValid"], "Echec generation PNG hors-ligne du Billet QR"
        assert omissions_check["printTitleHasProforma"], "Echec generation Facture Proforma officielle imprimable"
        assert omissions_check["cfpRowsCount"] >= 1, "Les dossiers CFP ne s'affichent pas dans Mon Espace"
        assert omissions_check["updatedBookingDate"] == "2026-12-28", f"Le report de date ACC-05 n'a pas mis a jour la date: {omissions_check['updatedBookingDate']}"
        assert omissions_check["mobilePillsCount"] == 7, f"Attendu 7 raccourcis mobiles, obtenu {omissions_check['mobilePillsCount']}"
        assert omissions_check["exportedCsvCount"] >= 4, "Echec export CSV comptable DIR-05 / AGT-09"

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
