# -*- coding: utf-8 -*-
"""
Simulation utilisateur de la console d'administration CRUD (préversion).
Clique les vrais boutons de Preview_Administration_ECOPARK.html avec Playwright et
vérifie l'effet de chaque action (tableau, journal d'audit, persistance, erreurs).

Lancement : python scripts/simulate_admin_preview_ui.py
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / "Preview_Administration_ECOPARK.html"
OUT_DIR = ROOT / "audit-assets" / "qa-etape0-live"
OUT_DIR.mkdir(parents=True, exist_ok=True)

results = []


def check(cond, label, detail=""):
    results.append((bool(cond), label))
    print(f"  [{'OK' if cond else 'FAIL'}] {label}{(' — ' + detail) if detail else ''}")


def open_admin(context):
    page = context.new_page()
    page.goto(PREVIEW.as_uri(), wait_until="networkidle")
    page.wait_for_timeout(300)
    page.evaluate("navigateFamily('ADM', 'ADM-01'); window.scrollTo(0, 0);")
    page.wait_for_timeout(300)
    return page


def counts(page):
    return page.evaluate("""() => ({
        catalog: document.querySelectorAll('#admCatalogTbody tr').length,
        audit: document.querySelectorAll('#admAuditLogTbody tr').length,
        cms: document.querySelectorAll('#admCmsListContainer .adm-cms-item').length,
        staff: document.querySelectorAll('#admStaffTbody tr').length,
    })""")


def audit_text(page):
    return page.inner_text("#admAuditLogTbody")


def row_inputs(row):
    return [i.input_value() for i in row.locator("input").all()]


def main():
    console_errors, page_errors = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 940})
        page = open_admin(ctx)
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("dialog", lambda d: d.accept())

        c0 = counts(page)
        print(f"\nÉtat initial : {c0}")

        print("\n1. Catalogue (ADM-01/02) — Dupliquer")
        zoo = page.locator("#admCatalogTbody tr", has_text="Zoologique").first
        zoo.locator("button.duplicate").click()
        page.wait_for_timeout(200)
        c = counts(page)
        copy_row = page.locator("#admCatalogTbody tr", has_text="(Copie").first
        check(c["catalog"] == c0["catalog"] + 1, "Une ligne de plus dans le catalogue", f"{c0['catalog']} -> {c['catalog']}")
        check(copy_row.count() == 1, "La copie porte le suffixe « (Copie »")
        check("brouillon" in copy_row.inner_text().lower(), "La copie est en brouillon")
        check("DUPLICATION" in audit_text(page), "Entrée « DUPLICATION » dans le journal d'audit")

        print("\n2. Catalogue — Ajouter (avec saisie interdite du tarif enfant groupe)")
        page.locator("button[onclick=\"openAdmCrudModal('CREATE', null)\"]:visible").first.click()
        page.wait_for_timeout(200)
        check(page.locator("#modalAdmCrudBox.open").count() == 1, "La modale d'ajout s'ouvre")
        title = "Simulation Pack Paques Famille"
        page.fill("#admCrudTitleInput", title)
        page.fill("#admCrudChildPrice", "1000")
        page.fill("#admCrudAdultPrice", "4000")
        page.fill("#admCrudGrpAdultPrice", "3500")
        page.fill("#admCrudGrpChildPrice", "1500")  # > tarif enfant individuel : doit être bloqué
        page.click("#modalAdmCrudBox button[onclick='saveAdmCrudModal()']")
        page.wait_for_timeout(250)
        new_row = page.locator("#admCatalogTbody tr", has_text=title).first
        vals = row_inputs(new_row) if new_row.count() else []
        check(new_row.count() == 1, "La nouvelle offre apparaît dans le tableau")
        check(vals[:4] == ["1000", "4000", "3500", "1000"], "Garde-fou : enfant groupe ramené à 1 000 FCFA (= enfant individuel)", f"valeurs {vals[:4]}")
        check("rejected" in (page.get_attribute("#admChildGuardBanner", "class") or ""), "Bandeau d'alerte du garde-fou affiché")
        check("AJOUT" in audit_text(page), "Entrée « AJOUT » dans le journal")
        check("Actif en ligne" in new_row.inner_text(),
              "LIMITE CONSTATÉE : la préversion publie directement la nouvelle offre (la base exigera brouillon + Direction)")

        print("\n3. Catalogue — Modifier via la modale")
        new_row.locator("button[onclick^='openAdmCrudModal']").click()
        page.wait_for_timeout(200)
        check(page.input_value("#admCrudTitleInput") == title, "La modale est préremplie avec la fiche")
        page.fill("#admCrudAdultPrice", "4500")
        page.click("#modalAdmCrudBox button[onclick='saveAdmCrudModal()']")
        page.wait_for_timeout(250)
        vals = row_inputs(page.locator("#admCatalogTbody tr", has_text=title).first)
        check(vals[1] == "4500", "Nouveau prix adulte 4 500 FCFA enregistré", f"valeurs {vals[:4]}")
        check("MODIFICATION" in audit_text(page), "Entrée « MODIFICATION » dans le journal")

        print("\n4. Catalogue — Rechercher")
        total_before = counts(page)["catalog"]
        page.fill("#admCatalogSearchInput", "Piscine")
        page.dispatch_event("#admCatalogSearchInput", "input")
        page.wait_for_timeout(200)
        visible = page.evaluate("""() => Array.from(document.querySelectorAll('#admCatalogTbody tr')).map(r => r.innerText)""")
        check(0 < len(visible) < total_before and all("iscine" in t for t in visible),
              "La recherche « Piscine » ne garde que les lignes correspondantes", f"{len(visible)}/{total_before} lignes affichées")
        page.fill("#admCatalogSearchInput", "")
        page.dispatch_event("#admCatalogSearchInput", "input")
        page.wait_for_timeout(150)

        print("\n5. Catalogue — Supprimer")
        before = counts(page)["catalog"]
        page.locator("#admCatalogTbody tr", has_text=title).first.locator("button.danger").click()
        page.wait_for_timeout(200)
        check(counts(page)["catalog"] == before - 1, "L'offre de simulation est supprimée")
        check("SUPPRESSION" in audit_text(page), "Entrée « SUPPRESSION » dans le journal")
        before = counts(page)["catalog"]
        page.locator("#admCatalogTbody tr", has_text="Zoologique").first.locator("button.danger").click()
        page.wait_for_timeout(200)
        check(counts(page)["catalog"] == before, "Supprimer le Zoo (billets actifs) est refusé")
        check("refusée" in audit_text(page), "Le refus est tracé dans le journal")

        print("\n6. Agenda & carte (ADM-04)")
        n = counts(page)["cms"]
        page.locator("#admCmsListContainer .adm-cms-item").first.locator("button.duplicate").click()
        page.wait_for_timeout(200)
        check(counts(page)["cms"] == n + 1, "Dupliquer un événement : +1 carte")
        page.locator("#admCmsListContainer .adm-cms-item", has_text="(Copie").first.locator("button.danger").click()
        page.wait_for_timeout(200)
        check(counts(page)["cms"] == n, "Supprimer la copie : retour au nombre initial")
        page.fill("#admQuickEventTitle", "Simulation Lundi de Paques en famille")
        page.click("button[onclick='admPublishQuickAgendaUpdate()']")
        page.wait_for_timeout(200)
        check(counts(page)["cms"] == n + 1 and page.locator("#admCmsListContainer", has_text="Lundi de Paques").count() == 1,
              "Ajout rapide d'un événement")

        print("\n7. Comptes équipe (ADM-05)")
        n = counts(page)["staff"]
        page.locator("#admStaffTbody tr").first.locator("button.duplicate").click()
        page.wait_for_timeout(200)
        check(counts(page)["staff"] == n + 1, "Dupliquer un poste : +1 compte")
        clarisse = page.locator("#admStaffTbody tr", has_text="ATANGANA").first
        clarisse.locator("button", has_text="Suspendre").click()
        page.wait_for_timeout(200)
        clarisse = page.locator("#admStaffTbody tr", has_text="ATANGANA").first
        check("Suspendu" in clarisse.inner_text(), "Suspendre l'agent guichet")
        clarisse.locator("button", has_text="Activer").click()
        page.wait_for_timeout(200)
        check("Suspendu" not in page.locator("#admStaffTbody tr", has_text="ATANGANA").first.inner_text(), "Réactiver l'agent")

        print("\n8. Journal d'audit (ADM-08) — filtres")
        kpi = lambda: int(page.inner_text("#admAuditCountKpi").split()[0])
        total = counts(page)["audit"]
        page.click("button[onclick=\"admFilterAuditLogs('CRUD')\"]")
        page.wait_for_timeout(150)
        crud = counts(page)["audit"]
        page.click("button[onclick=\"admFilterAuditLogs('ALL')\"]")
        page.wait_for_timeout(150)
        check(0 < crud <= total and counts(page)["audit"] == total, "Filtre « Actions CRUD » puis « Tout afficher »", f"{crud}/{total} lignes affichées")
        check(kpi() >= c0["audit"] + 10, "Chaque action a laissé une trace (compteur du journal)", f"{c0['audit']} -> {kpi()} événements")
        check(total == 8 and kpi() > 8, "LIMITE CONSTATÉE : le tableau n'affiche que les 8 dernières entrées (pas de pagination)",
              f"{total} lignes affichées sur {kpi()}")

        page.evaluate("document.getElementById('admAuditLogTable').scrollIntoView({block: 'start'})")
        page.wait_for_timeout(200)
        shot = OUT_DIR / "simulation_ui_journal_audit_apres_parcours.png"
        page.screenshot(path=str(shot))

        print("\n9. Persistance & partage entre appareils")
        snapshot = counts(page)
        page.reload(wait_until="networkidle")
        page.evaluate("navigateFamily('ADM', 'ADM-01');")
        page.wait_for_timeout(300)
        after = counts(page)
        check(after["catalog"] == snapshot["catalog"] and after["staff"] == snapshot["staff"],
              "Après rechargement, les modifications sont conservées (même navigateur)")
        other = browser.new_context(viewport={"width": 1440, "height": 940})
        other_page = open_admin(other)
        seen = counts(other_page)
        same_device_only = seen["catalog"] == c0["catalog"] and seen["staff"] == c0["staff"]
        check(same_device_only,
              "LIMITE ATTENDUE : un autre appareil ne voit PAS ces modifications (stockage local, pas encore Supabase)",
              f"autre appareil : {seen['catalog']} offres / {seen['staff']} comptes")
        other.close()

        print("\n10. Qualité")
        high = page.evaluate("""() => Array.from(document.body.innerText).filter(ch => ch.codePointAt(0) > 0x25FF).length""")
        check(high == 0, "Aucun emoji / caractère interdit après toutes les actions")
        check(not console_errors and not page_errors, "Aucune erreur JavaScript", f"{console_errors + page_errors}")
        browser.close()

    ok = sum(1 for r in results if r[0])
    print(f"\n{ok}/{len(results)} vérifications réussies. Capture : {shot}")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
