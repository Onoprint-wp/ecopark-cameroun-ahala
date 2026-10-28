# -*- coding: utf-8 -*-
"""
Phase 4 — Test navigateur de la console d'administration (mode démo, vrais clics).
Prérequis : `npm run dev` (http://localhost:3000).
Lancement : python scripts/test_admin_console.py   (captures dans audit-assets/qa-etape0-live/)
"""
import json
import shutil
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"
SHOTS = ROOT / "audit-assets" / "qa-etape0-live"
SHOTS.mkdir(parents=True, exist_ok=True)
SNAP = json.loads((ROOT / "etape0-site-live" / "content-snapshot.json").read_text(encoding="utf-8"))
RAIN = SNAP["content"]["site_settings"]["weather_banner"]["presets"]["RAIN_GUARANTEE"]

results = []
shots = []


def check(cond, label, detail=""):
    results.append(bool(cond))
    print(f"  [{'OK' if cond else 'FAIL'}] {label}{(' — ' + str(detail)) if detail else ''}")


def shot(page, name, selector=None):
    path = SHOTS / name
    if selector:
        page.locator(selector).scroll_into_view_if_needed()
        page.wait_for_timeout(250)
    page.screenshot(path=str(path))
    shots.append(path)


def set_role(page, role):
    page.select_option("#admDemoRole", role)
    page.wait_for_timeout(150)


def row(page, text):
    return page.locator("#admCatalogBody tr", has_text=text).first


def confirm(page, label):
    page.locator("#admConfirm.open button", has_text=label).click()
    page.wait_for_timeout(300)


def main():
    errors, console_errors = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 940}, accept_downloads=True)
        page = ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.goto(BASE + "/admin", wait_until="networkidle")
        page.wait_for_function("() => window.EcoparkAdmin && EcoparkAdmin.state.loaded", timeout=8000)

        print("\n1. Ouverture & rôles")
        check(page.locator("#admRoleBar", has_text="Mode démonstration").count() == 1, "Bandeau « mode démonstration » visible")
        check(page.locator("#admCatalogBody tr").count() == 8, "8 activités en ligne affichées", page.locator("#admCatalogBody tr").count())
        size = page.evaluate("() => document.documentElement.outerHTML.length")
        check(page.evaluate("() => !!document.querySelector('script[src*=\"ecopark-admin.js\"]')"), "Module admin chargé à la demande (absent du site public)")
        shot(page, "phase4_1_console_catalogue.png", "#sec-ADM-01")

        print("\n2. Exploitation : dupliquer, modifier un brouillon, prix en ligne verrouillé")
        set_role(page, "responsable_exploitation")
        row(page, "Jardin Zoologique").locator("[data-act=duplicate]").click()
        page.wait_for_selector("#admEditor.open", timeout=3000)
        check("(Copie)" in page.inner_text("#admEditorCard h4"), "La copie s'ouvre directement en édition")
        page.fill("#admF_adult_price_fcfa", "1200")
        check("1 000 FCFA → 1 200 FCFA" in page.inner_text("#admEdDiff"), "Différentiel avant → après affiché", page.inner_text("#admEdDiff")[:80])
        page.fill("#admF_group_child_price_fcfa", "700")
        check("Garde-fou" in page.inner_text("#admF_group_child_price_fcfa_err") and page.is_disabled("#admEdSave"),
              "Garde-fou : 700 FCFA enfant groupe bloqué avant envoi")
        shot(page, "phase4_2_modale_garde_fou.png")
        page.fill("#admF_group_child_price_fcfa", "500")
        page.click("#admEdSave")
        page.wait_for_timeout(300)
        draft = page.locator("#admCatalogBody tr.adm-row-new").first
        check(draft.count() == 1 and "Brouillon" in draft.inner_text() and "1 200 FCFA" in draft.inner_text(), "Brouillon enregistré à 1 200 FCFA et surligné")
        check(draft.locator("[data-act=publish]").is_disabled(), "Publier désactivé pour l'Exploitation (tarif)")
        row(page, "Entrée Parc & Jardin Zoologique").locator("[data-act=edit]").first.click()
        page.wait_for_selector("#admEditor.open")
        check(page.is_disabled("#admF_adult_price_fcfa") and page.locator("#admEditorCard .adm-note").count() == 1,
              "Offre en ligne : prix verrouillés avec explication")
        page.click("#admEdCancel")
        public_price = page.evaluate("() => EcoparkData.content('catalog_activities').find(r => r.slug === 'zoo').adult_price_fcfa")
        check(public_price == 1000, "Le site public affiche toujours 1 000 FCFA")

        print("\n3. Direction : publier la nouvelle version")
        set_role(page, "direction")
        page.locator("#admCatalogBody tr.adm-row-new [data-act=publish]").click()
        page.wait_for_selector("#admConfirm.open")
        shot(page, "phase4_3_confirmation_publication.png")
        confirm(page, "Remplacer l'offre en ligne")
        public_price = page.evaluate("() => EcoparkData.content('catalog_activities').find(r => r.slug === 'zoo').adult_price_fcfa")
        check(public_price == 1200, "Nouveau prix en ligne (1 200 FCFA) sous la même adresse")
        check(page.locator("#admCatalogBody tr", has_text="(Copie)").count() == 0, "La version de travail est archivée (masquée)")

        print("\n4. Archiver puis annuler (8 s)")
        row(page, "Pirogue").locator("[data-act=delete]").click()
        page.wait_for_selector("#admConfirm.open")
        check("Archiver" in page.inner_text("#admConfirm h4"), "Une offre publiée est archivée, pas effacée")
        confirm(page, "Archiver")
        check(page.locator("#admCatalogBody tr", has_text="Pirogue").count() == 0, "Pirogue retirée du catalogue actif")
        page.click("#admUndoBtn")
        page.wait_for_timeout(400)
        check(page.locator("#admCatalogBody tr", has_text="Pirogue").count() == 1 and
              page.evaluate("() => EcoparkData.content('catalog_activities').some(r => r.slug === 'pirogue')"), "« Annuler » la remet en ligne")

        print("\n5. Ajouter puis supprimer un brouillon")
        page.click("#admAddOffer")
        page.wait_for_selector("#admEditor.open")
        page.fill("#admF_title", "Tyrolienne au-dessus du lac")
        page.fill("#admF_slug", "Tyrolienne Lac")
        check("Format attendu" in page.inner_text("#admF_slug_err"), "Contrôle du format de l'adresse courte")
        page.fill("#admF_slug", "tyrolienne-lac")
        page.fill("#admF_sku", "CAT-TYRO")
        page.fill("#admF_description", "Parcours suspendu encadré, dès 10 ans.")
        page.click("#admEdSave")
        page.wait_for_timeout(300)
        new = row(page, "Tyrolienne")
        check(new.count() == 1 and "Brouillon" in new.inner_text(), "Nouvelle offre créée en brouillon")
        check(not page.evaluate("() => EcoparkData.content('catalog_activities').some(r => r.slug === 'tyrolienne-lac')"), "Invisible du public")
        new.locator("[data-act=delete]").click()
        page.wait_for_selector("#admConfirm.open")
        check("Supprimer" in page.inner_text("#admConfirm h4"), "Brouillon jamais publié : suppression définitive proposée")
        confirm(page, "Supprimer")
        check(row(page, "Tyrolienne").count() == 0, "Brouillon supprimé")

        print("\n5 bis. Une image pour chaque publication")
        check(page.locator("#admCatalogBody img.adm-thumb").count() == page.locator("#admCatalogBody tr").count(),
              "Chaque offre en ligne affiche sa vignette")
        page.click("#admAddOffer")
        page.wait_for_selector("#admEditor.open")
        page.fill("#admF_title", "Accrobranche Canopée")
        page.fill("#admF_slug", "accrobranche")
        page.fill("#admF_sku", "CAT-ACCRO")
        page.fill("#admF_description", "Parcours dans les arbres, encadré.")
        page.click("#admEdSave")
        page.wait_for_timeout(300)
        acc = row(page, "Accrobranche")
        pub_btn = acc.locator("[data-act=publish]")
        check(pub_btn.is_disabled() and "image" in (pub_btn.get_attribute("title") or ""), "Sans image : « Publier » bloqué avec explication",
              pub_btn.get_attribute("title"))
        check(acc.locator(".adm-thumb-missing").count() == 1, "Vignette « Sans image » signalée")
        acc.locator("[data-act=edit]").click()
        page.wait_for_selector("#admEditor.open")
        page.set_input_files("#admImgFile", str(ROOT / "etape0-site-live" / "audit-assets" / "ecopark-real-media" / "IMG_20260829_172016-1-scaled.jpg"))
        page.wait_for_function("() => document.querySelector('#admImgPreview img') !== null", timeout=8000)
        src = page.get_attribute("#admImgPreview img", "src") or ""
        kb = round(len(src) * 3 / 4 / 1024)
        check(src.startswith("data:image/") and kb < 450, "Photo de 679 Ko téléversée et optimisée", f"{kb} Ko après optimisation")
        check(page.input_value("#admF_image_alt") == "Accrobranche Canopée", "Texte alternatif proposé à partir du titre")
        shot(page, "phase4_8_modale_image.png")
        page.click("#admEdSave")
        page.wait_for_timeout(300)
        acc = row(page, "Accrobranche")
        check(acc.locator("img.adm-thumb").count() == 1 and not acc.locator("[data-act=publish]").is_disabled(), "Avec image : vignette affichée, « Publier » actif")
        acc.locator("[data-act=publish]").click()
        page.wait_for_selector("#admConfirm.open")
        confirm(page, "Publier")
        live = page.evaluate("() => { const r = EcoparkData.content('catalog_activities').find(x => x.slug === 'accrobranche'); return r && { img: !!r.image_src, alt: r.image_alt }; }")
        check(live and live["img"] and live["alt"] == "Accrobranche Canopée", "Offre publiée avec son image et sa description")
        row(page, "Accrobranche").locator("[data-act=edit]").click()
        page.wait_for_selector("#admEditor.open")
        page.click("#admImgRemove")
        check("garder une image" in page.inner_text("#admF_image_src_err") and page.is_disabled("#admEdSave"),
              "Impossible de retirer l'image d'une offre en ligne")
        page.click("#admEdCancel")

        print("\n6. Recherche, filtres & onglets")
        page.fill("#admCatalogSearch", "piscine")
        page.wait_for_timeout(150)
        n = page.locator("#admCatalogBody tr").count()
        check(n >= 1 and all("iscine" in t for t in page.locator("#admCatalogBody tr").all_inner_texts()), "Recherche « piscine »", f"{n} ligne(s)")
        page.fill("#admCatalogSearch", "")
        page.select_option("#admPoleFilter", "RESTAURATION")
        page.wait_for_timeout(150)
        check(page.locator("#admCatalogBody tr").count() == 2, "Filtre pôle Restauration (2 offres)", page.locator("#admCatalogBody tr").count())
        page.select_option("#admPoleFilter", "ALL")
        page.click("#admCatalogTabs [data-tab=sales_bundles]")
        check(page.locator("#admCatalogBody tr").count() == 3, "Onglet Formules : 3 pass")
        page.click("#admCatalogTabs [data-tab=lodge_cities]")
        check(page.locator("#admCatalogBody [data-act=duplicate]").count() == 0 and page.is_disabled("#admAddOffer"),
              "Cités hôtelières : ni duplication ni création (codes figés)")
        page.click("#admCatalogTabs [data-tab=catalog_activities]")

        print("\n7. Agenda & carte")
        page.locator("#admAgendaList .adm-cms-row", has_text="Grand Dimanche Royal").locator("[data-act=duplicate]").click()
        page.wait_for_selector("#admEditor.open")
        page.select_option("#admF_target_weekday", "1")
        page.select_option("#admF_day_filter", "LUNDI_FERIE")
        page.fill("#admF_short_label", "Lundi de Pâques Royal")
        page.fill("#admF_badge", "Lundi de Pâques • 12h00 – 17h30")
        page.click("#admEdSave")
        page.wait_for_timeout(300)
        page.locator("#admAgendaList .adm-cms-row", has_text="Lundi de Pâques Royal").locator("[data-act=publish]").click()
        page.wait_for_selector("#admConfirm.open")
        check("(Copie)" in page.inner_text("#admConfirm p"), "Avertissement : titre encore suffixé « (Copie) »")
        page.locator("#admConfirm.open button", has_text="Retour").click()
        page.locator("#admAgendaList .adm-cms-row", has_text="Lundi de Pâques Royal").locator("[data-act=edit]").click()
        page.wait_for_selector("#admEditor.open")
        page.fill("#admF_title", "Lundi de Pâques Royal : Buffet Camerounais & Ambiance Live")
        page.click("#admImgLibBtn")
        page.locator("#admImgLibrary .adm-lib-item", has_text="Balade en pirogue").click()
        check((page.get_attribute("#admImgPreview img", "src") or "").endswith("balade_pirogue3.jpg"), "Image choisie dans la photothèque")
        page.click("#admEdSave")
        page.wait_for_timeout(300)
        page.locator("#admAgendaList .adm-cms-row", has_text="Lundi de Pâques Royal").locator("[data-act=publish]").click()
        page.wait_for_selector("#admConfirm.open")
        confirm(page, "Publier comme nouvelle offre")
        check(page.evaluate("() => EcoparkData.content('agenda_events').length") == 5, "Événement du lundi férié publié (5 temps forts)")
        page.locator("#admMenuList .adm-cms-row", has_text="Poisson Braisé").locator("[data-act=stock]").click()
        page.wait_for_timeout(250)
        check("En rupture" in page.locator("#admMenuList .adm-cms-row", has_text="Poisson Braisé").inner_text(), "Plat marqué en rupture")
        shot(page, "phase4_4_agenda_carte.png", "#sec-ADM-04")

        print("\n8. Jauges & bandeau météo")
        page.locator("#admQuotaBody tr", has_text="Piscine").locator("input").fill("60")
        page.locator("#admQuotaBody tr", has_text="Piscine").locator("[data-act=quota-save]").click()
        page.wait_for_timeout(250)
        check(page.locator("#admQuotaBody tr", has_text="Piscine").locator("input").input_value() == "60", "Jauge piscine du jour : 60 places")
        page.select_option("#admWeatherPreset", "RAIN_GUARANTEE")
        check(page.inner_text("#admWeatherPreview") == RAIN, "Aperçu du bandeau avant publication")
        page.click("#admWeatherSave")
        page.wait_for_timeout(250)
        shot(page, "phase4_5_jauges_meteo.png", "#sec-ADM-03")

        print("\n9. Comptes équipe & passerelles")
        page.locator("#admStaffBody tr", has_text="ATANGANA").locator("[data-act=staff-toggle]").click()
        page.wait_for_selector("#admConfirm.open")
        confirm(page, "Suspendre")
        check("Suspendu" in page.locator("#admStaffBody tr", has_text="ATANGANA").inner_text(), "Agent guichet suspendu")
        roles = page.locator("#admStaffBody tr td:nth-child(2)").all_inner_texts()
        check(all("&" not in r for r in roles), "Uniquement des rôles valides (plus de « direction & exploitation »)", roles)
        check(page.locator("#admGatewayList .adm-gw").count() == 3, "3 passerelles affichées, sans clé secrète")
        page.locator("#admGatewayList [data-act=gw-test]").first.click()
        page.wait_for_timeout(250)
        shot(page, "phase4_6_equipe_passerelles.png", "#sec-ADM-05")

        print("\n10. Journal d'audit")
        page.select_option("#admAuditOp", "DUPLICATE")
        page.wait_for_timeout(200)
        ops = page.locator("#admAuditBody tr td:nth-child(2)").all_inner_texts()
        check(len(ops) >= 2 and all(o == "Duplication" for o in ops), "Filtre « Duplications »", f"{len(ops)} entrée(s)")
        page.select_option("#admAuditOp", "ALL")
        page.wait_for_timeout(200)
        total = page.inner_text("#admAuditCount")
        check(page.locator("#admAuditBody tr").count() <= 25, "Pagination (25 par page)", total)
        with page.expect_download() as dl:
            page.click("#admAuditExport")
        check(dl.value.suggested_filename.startswith("journal-audit-ecopark-"), "Export CSV téléchargé", dl.value.suggested_filename)
        page.click("#admAuditVerify")
        page.wait_for_timeout(200)
        check("indisponible en mode démonstration" in page.inner_text("#admChainResult"), "Vérification de chaîne : message clair en démo")
        shot(page, "phase4_7_journal_audit.png", "#sec-ADM-08")

        print("\n11. Sécurité & lecture seule")
        page.evaluate("""() => {
            document.getElementById('quoteOrgName').value = '<img src=x onerror="window.__xss=1">';
            document.getElementById('quotePhone').value = '+237 677 00 00 00';
            submitGroupQuoteSprint1();
            navigateFamily('ADM', 'ADM-08');
        }""")
        page.wait_for_timeout(500)
        check(page.evaluate("() => window.__xss") is None and page.locator("#admAuditBody img").count() == 0,
              "Texte saisi par un visiteur affiché sans être interprété (pas d'injection HTML)")
        set_role(page, "agent_guichet")
        edits = page.locator("#admCatalogBody [data-act=edit]")
        check(edits.count() > 0 and all(edits.nth(i).is_disabled() for i in range(edits.count())), "Agent guichet : consultation seule")
        hidden = page.evaluate("() => getComputedStyle(document.querySelector('#sec-ADM-01 h3 .tech-code-tag')).display")
        check(hidden == "none", "Codes techniques masqués en mode visiteur")

        print("\n12. Effet sur le site public")
        page.evaluate("navigateFamily('PUB', 'PUB-01')")
        page.wait_for_timeout(300)
        check(page.inner_text("#ahalaLiveWeatherText").strip() == RAIN, "Bandeau météo publié visible sur l'accueil")

        high = page.evaluate("() => Array.from(document.body.innerText).filter(c => c.codePointAt(0) > 0x25FF).length")
        check(high == 0, "Aucun emoji / caractère interdit")
        check(not errors and not console_errors, "Aucune erreur JavaScript ni console", (errors + console_errors)[:3])
        browser.close()

    ok = sum(results)
    print(f"\n{ok}/{len(results)} vérifications réussies.")
    art = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\7ee4ce6d-03a1-4262-8080-a7fbda05ab9a")
    if art.exists():
        for s in shots:
            shutil.copy(s, art / s.name)
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
