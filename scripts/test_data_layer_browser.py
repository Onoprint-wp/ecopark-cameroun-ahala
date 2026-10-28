# -*- coding: utf-8 -*-
"""
Phase 3 — Test navigateur de la couche EcoparkData (Playwright).

A. Build démo réel (http://localhost:3000, `npm run dev` doit tourner) :
   pilote local, bandeau inchangé, mode ?demo=77, synchronisation entre onglets.
B. Build Supabase généré à la volée (build_data_layer.py --out), servi par interception,
   avec un faux serveur Supabase (REST) piloté par le test :
   - le bandeau météo est mis à jour depuis la base (au-dessus de la copie de secours)
   - un devis est converti au format de la base et envoyé
   - un refus de la base restaure l'écran et affiche un message français
   - réseau coupé : affichage immédiat depuis la copie de secours, aucune erreur JavaScript
   - numéro WhatsApp obligatoire en production

Lancement : python scripts/test_data_layer_browser.py
"""
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:3000"
SB_URL = "https://demo-ecopark.supabase.co"
SNAPSHOT = json.loads((ROOT / "etape0-site-live" / "content-snapshot.json").read_text(encoding="utf-8"))
RAIN = SNAPSHOT["content"]["site_settings"]["weather_banner"]["presets"]["RAIN_GUARANTEE"]
SUNNY = SNAPSHOT["content"]["site_settings"]["weather_banner"]["presets"]["SUNNY"]

results = []


def check(cond, label, detail=""):
    results.append(bool(cond))
    print(f"  [{'OK' if cond else 'FAIL'}] {label}{(' — ' + str(detail)) if detail else ''}")


def fake_anon_key():
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256", "typ": "JWT"}) + "." + enc({"role": "anon", "iss": "supabase-demo"}) + ".signature"


def build_supabase_html():
    out = Path(tempfile.gettempdir()) / "ecopark_supabase_build.html"
    subprocess.run([sys.executable, str(ROOT / "build_data_layer.py"), "--env", "staging",
                    "--supabase-url", SB_URL, "--anon-key", fake_anon_key(), "--out", str(out)],
                   check=True, capture_output=True)
    return out.read_text(encoding="utf-8")


def table_rows(table, weather_preset="RAIN_GUARANTEE"):
    content = SNAPSHOT["content"]
    if table == "site_settings":
        rows = []
        for k, v in content["site_settings"].items():
            v = json.loads(json.dumps(v))
            if k == "weather_banner":
                v["active_preset"] = weather_preset
            rows.append({"key": k, "value": v, "is_public": True})
        return rows
    return content.get(table, [])


def part_a(browser):
    print("\nA. Build démo (site réel sur localhost:3000)")
    ctx = browser.new_context()
    errors = []
    p1 = ctx.new_page()
    p1.on("pageerror", lambda e: errors.append(str(e)))
    p1.goto(BASE + "/", wait_until="networkidle")
    check(p1.get_attribute("html", "data-ecopark-driver") == "local", "Pilote démo actif par défaut")
    check(p1.inner_text("#ahalaLiveWeatherText").strip() == SUNNY, "Bandeau météo identique au site actuel", p1.inner_text("#ahalaLiveWeatherText").strip())
    info = p1.evaluate("() => ({ v: EcoparkData.version, cat: EcoparkData.content('catalog_activities').length, hasBookings: Array.isArray(loadDB().bookings) })")
    check(info["v"] == "3.0.0" and info["cat"] == 12 and info["hasBookings"], "Magasin hydraté depuis la copie de secours, loadDB() au format historique", info)

    p2 = ctx.new_page()
    p2.goto(BASE + "/guichet", wait_until="networkidle")
    p1.evaluate("""() => { const db = loadDB(); db.quotes.unshift({ reference: 'DEV-ONGLET-1', org: 'Test onglets', type: 'x', pax: 12, date: '2026-12-01', budgetFcfa: 18000, status: 'Proforma générée' }); saveDB(db); }""")
    p2.wait_for_timeout(300)
    seen = p2.evaluate("() => loadDB().quotes[0].reference")
    check(seen == "DEV-ONGLET-1", "Synchronisation entre onglets conservée (BroadcastChannel + localStorage)")

    p3 = ctx.new_page()
    p3.goto(BASE + "/?demo=77", wait_until="networkidle")
    check(p3.get_attribute("html", "data-ecopark-demo") == "1", "Mode ?demo=77 reconnu")
    check(not errors, "Aucune erreur JavaScript", errors)
    ctx.close()


def part_b(browser, html):
    print("\nB. Build Supabase (faux serveur Supabase piloté par le test)")
    state = {"quote_status": 201, "posted": [], "offline": False}

    def serve_page(route):
        route.fulfill(status=200, content_type="text/html; charset=utf-8", body=html)

    def serve_supabase(route):
        req = route.request
        if state["offline"]:
            return route.abort("internetdisconnected")
        path = req.url.split("/rest/v1/")[-1].split("?")[0] if "/rest/v1/" in req.url else ""
        if req.method == "GET" and path:
            return route.fulfill(status=200, content_type="application/json", body=json.dumps(table_rows(path)))
        if req.method == "POST" and path == "group_quotes":
            state["posted"].append(json.loads(req.post_data or "{}"))
            if state["quote_status"] == 201:
                return route.fulfill(status=201, body="")
            return route.fulfill(status=401, content_type="application/json",
                                 body=json.dumps({"code": "42501", "message": "new row violates row-level security policy for table \"group_quotes\""}))
        return route.fulfill(status=404, content_type="application/json", body="{}")

    def open_page(ctx):
        page = ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.route(BASE + "/__supabase-build", serve_page)
        page.route(SB_URL + "/**", serve_supabase)
        page.goto(BASE + "/__supabase-build", wait_until="domcontentloaded")
        return page, errs

    def submit_quote(page, phone, org):
        page.evaluate("""([phone, org]) => {
            document.getElementById('quoteOrgName').value = org;
            document.getElementById('quotePhone').value = phone;
            document.getElementById('quoteDate').value = '2026-12-10';
            return submitGroupQuoteSprint1();
        }""", [phone, org])
        page.wait_for_timeout(600)
        return page.inner_text("#sprint1Toast")

    ctx = browser.new_context()
    page, errs = open_page(ctx)
    page.wait_for_function("() => document.documentElement.getAttribute('data-ecopark-driver') === 'supabase'", timeout=5000)
    check(True, "Pilote Supabase actif (supabase-js chargé depuis /vendor)")
    page.wait_for_function(f"() => document.getElementById('ahalaLiveWeatherText').textContent === {json.dumps(RAIN)}", timeout=5000)
    check(True, "Bandeau météo mis à jour depuis la base (préréglage « pluie »)")
    cached = page.evaluate("() => JSON.parse(localStorage.getItem('ecopark_cache_v2_staging') || '{}')")
    check("content" in cached and "quotes" not in cached and "bookings" not in cached,
          "Cache navigateur : contenu public uniquement (aucune donnée d'équipe)")

    toast = submit_quote(page, "+237 677 11 22 33", "Collège Simulation Ahala")
    body = state["posted"][-1] if state["posted"] else {}
    check(body.get("group_type") == "ecole" and body.get("preferred_date") == "2026-12-10" and body.get("status") == "EN_ETUDE"
          and body.get("contact_phone") == "+237 677 11 22 33" and body.get("participants_count", 0) >= 10,
          "Devis envoyé au format de la base", {k: body.get(k) for k in ("quote_reference", "group_type", "preferred_date", "status")})
    check("enregistré" in toast, "Confirmation affichée au visiteur", toast[:80])

    state["quote_status"] = 401
    ref_count_before = page.evaluate("() => loadDB().quotes.length")
    toast = submit_quote(page, "+237 677 44 55 66", "Refus Simulation")
    page.wait_for_timeout(300)
    after = page.evaluate("() => ({ n: loadDB().quotes.length, refs: loadDB().quotes.map(q => q.org) })")
    check("Action non autorisée" in toast and "n'a pas été transmise" in toast, "Refus de la base : message français explicite", toast[:110])
    check(after["n"] == ref_count_before and "Refus Simulation" not in after["refs"], "Retour arrière : le devis refusé disparaît de l'écran")

    n_posted = len(state["posted"])
    toast = submit_quote(page, "", "Sans Numero")
    check(len(state["posted"]) == n_posted and "numéro WhatsApp" in toast, "Numéro obligatoire en production (rien n'est envoyé)", toast[:80])
    check(not errs, "Aucune erreur JavaScript", errs)
    ctx.close()

    print("\nC. Réseau coupé (Supabase injoignable)")
    state["offline"] = True
    ctx = browser.new_context()
    page, errs = open_page(ctx)
    page.wait_for_timeout(1500)
    txt = page.inner_text("#ahalaLiveWeatherText").strip()
    visible = page.evaluate("() => document.querySelectorAll('img').length > 20 && document.body.innerText.length > 5000")
    check(txt == SUNNY, "Bandeau affiché depuis la copie de secours", txt)
    check(visible, "Page complète affichée (pas d'écran vide)")
    check(page.evaluate("() => EcoparkData.content('agenda_events').length") == 4, "Agenda disponible hors ligne (4 événements)")
    check(not errs, "Aucune erreur JavaScript malgré la coupure", errs)
    ctx.close()


def main():
    html = build_supabase_html()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        part_a(browser)
        part_b(browser, html)
        browser.close()
    ok = sum(results)
    print(f"\n{ok}/{len(results)} vérifications réussies.")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
