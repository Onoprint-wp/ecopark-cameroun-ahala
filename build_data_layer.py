# -*- coding: utf-8 -*-
"""
Phase 3 — Intégration de la couche d'accès aux données (EcoparkData) dans le site.

Met à jour etape0-site-live/index.html ET Prototype_Interactif_ECOPARK_NEW_LOOK.html
(de façon identique, comme les autres scripts build_*.py) :

  1. Configuration du pilote (window.ECOPARK_CONFIG), intégrée au HTML par environnement
  2. Copie de secours du contenu public (content-snapshot.json) intégrée au HTML
  3. Module etape0-site-live/js/ecopark-data.js intégré au HTML (site autonome, sans requête en plus)
  4. supabase-js (vendor/) chargé UNIQUEMENT pour un build Supabase
  5. loadDB() / saveDB() rebranchés sur le magasin EcoparkData (comportement démo inchangé)
  6. Pilotes de bout en bout : bandeau météo (lecture temps réel) et dépôt de devis (écriture anonyme)

Ré-exécutable : chaque bloc est délimité par des marqueurs et remplacé à l'identique.

Usage :
  python build_data_layer.py                         # build démo / local (comportement actuel)
  python build_data_layer.py --env staging --supabase-url https://xxx.supabase.co --anon-key eyJ...
"""
import argparse
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = [ROOT / "etape0-site-live" / "index.html", ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"]
DATA_LAYER_JS = ROOT / "etape0-site-live" / "js" / "ecopark-data.js"
SNAPSHOT_JSON = ROOT / "etape0-site-live" / "content-snapshot.json"
SUPABASE_JS_VERSION = "2.118.0"

HEAD_START, HEAD_END = "<!-- ECOPARK_DATA_LAYER:START -->", "<!-- ECOPARK_DATA_LAYER:END -->"
JS_START, JS_END = "// ECOPARK_DATA_BRIDGE:START", "// ECOPARK_DATA_BRIDGE:END"
QUOTE_START, QUOTE_END = "// ECOPARK_QUOTE_PILOT:START", "// ECOPARK_QUOTE_PILOT:END"
PHONE_START, PHONE_END = "// ECOPARK_QUOTE_PHONE:START", "// ECOPARK_QUOTE_PHONE:END"


def jwt_role(token: str) -> str:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("role", "")
    except Exception:
        return ""


def script_safe(text: str) -> str:
    """Empêche la fermeture prématurée d'une balise <script> par le contenu intégré."""
    return text.replace("</", "<\\/")


def minify_js(src: str) -> str:
    """
    Allègement prudent pour l'intégration au HTML (la source lisible reste dans js/) :
    retire les lignes de commentaire complètes (// ... et blocs /* ... */ en début de ligne),
    l'indentation et les lignes vides. Ne touche jamais au contenu d'une ligne de code.
    Hypothèse vérifiée : les modules n'utilisent pas de gabarits `...` multilignes.
    """
    out, in_block = [], False
    for line in src.splitlines():
        s = line.strip()
        if in_block:
            if "*/" in s:
                in_block = False
            continue
        if s.startswith("/*"):
            if "*/" not in s[2:]:
                in_block = True
            continue
        if not s or s.startswith("//"):
            continue
        out.append(s)
    return "\n".join(out)


def build_head_block(config: dict) -> str:
    snapshot = json.loads(SNAPSHOT_JSON.read_text(encoding="utf-8"))
    data_layer = minify_js(DATA_LAYER_JS.read_text(encoding="utf-8"))
    parts = [
        HEAD_START,
        '  <script id="ecoparkConfig">window.ECOPARK_CONFIG = ' + json.dumps(config, ensure_ascii=False) + ";</script>",
        '  <script type="application/json" id="ecoparkContentSnapshot">' + script_safe(json.dumps(snapshot, ensure_ascii=False, separators=(",", ":"))) + "</script>",
    ]
    if config.get("dataDriver") == "supabase":
        parts.append(f'  <script src="/vendor/supabase.min.js" data-version="{SUPABASE_JS_VERSION}"></script>')
    parts.append('  <script id="ecoparkDataLayer">\n' + script_safe(data_layer) + "\n  </script>")
    parts.append("  " + HEAD_END)
    return "\n".join(parts)


BRIDGE_JS = r"""
    // ECOPARK_DATA_BRIDGE:START
    // Couche d'accès aux données (Phase 3) : loadDB()/saveDB() lisent et écrivent le magasin
    // EcoparkData. En démo, comportement strictement identique (localStorage).
    (function bootEcoparkData() {
      var snapEl = document.getElementById('ecoparkContentSnapshot');
      var snapshot = null;
      try { snapshot = snapEl ? JSON.parse(snapEl.textContent) : null; } catch (e) { snapshot = null; }
      if (!window.EcoparkData) return;
      EcoparkData.configureLegacy({ storageKey: STORAGE_KEY_SPRINT1, defaults: DEFAULT_DB_STATE, snapshot: snapshot });
      EcoparkData.init({
        onStatus: function (status) { document.documentElement.setAttribute('data-ecopark-sync', status); }
      });
      document.documentElement.setAttribute('data-ecopark-driver', EcoparkData.driverName);
      EcoparkData.onChange(function (meta) {
        if (!meta) return;
        if (meta.source === 'rollback' || meta.source === 'realtime') {
          if (typeof syncAllViewsFromDB === 'function') syncAllViewsFromDB();
        }
        if (meta.op === 'refreshContent' || meta.source === 'rollback' || meta.entity === 'site_settings') {
          renderWeatherBannerFromData();
        }
      });
      if (EcoparkData.driverName === 'local' && new URLSearchParams(window.location.search).get('demo') === '77') {
        document.documentElement.setAttribute('data-ecopark-demo', '1');
      }
    })();

    function renderWeatherBannerFromData() {
      if (!window.EcoparkData || !EcoparkData.store) return;
      var wb = EcoparkData.setting('weather_banner');
      var el = document.getElementById('ahalaLiveWeatherText');
      if (!wb || !el) return;
      var text = wb.custom_message || (wb.presets && wb.presets[wb.active_preset]);
      if (text && el.textContent !== text) el.textContent = text;
    }

    function loadDB() {
      if (window.EcoparkData && EcoparkData.store) return EcoparkData.legacyLoad();
      try {
        const raw = localStorage.getItem(STORAGE_KEY_SPRINT1);
        if (!raw) return JSON.parse(JSON.stringify(DEFAULT_DB_STATE));
        return Object.assign(JSON.parse(JSON.stringify(DEFAULT_DB_STATE)), JSON.parse(raw));
      } catch (e) {
        return JSON.parse(JSON.stringify(DEFAULT_DB_STATE));
      }
    }

    function saveDB(db) {
      try {
        if (window.EcoparkData && EcoparkData.store) {
          var caller = ((new Error().stack || '').split('\n')[2] || '').replace(/^\s*at\s+/, '').split(' ')[0];
          EcoparkData.legacySave(db, caller);
        } else {
          localStorage.setItem(STORAGE_KEY_SPRINT1, JSON.stringify(db));
        }
        if (syncChannel) syncChannel.postMessage({ type: 'DB_UPDATED' });
      } catch (e) {}
      syncAllViewsFromDB();
    }
    // ECOPARK_DATA_BRIDGE:END
"""

QUOTE_PHONE_JS = r"""      // ECOPARK_QUOTE_PHONE:START
      // En production, un devis sans numéro serait inexploitable (le numéro par défaut est celui d'ECOPARK)
      if (window.EcoparkData && EcoparkData.driverName === 'supabase' && !(phoneEl && phoneEl.value.trim())) {
        if (phoneEl) phoneEl.focus();
        showToastSprint1('• Indiquez votre numéro WhatsApp (+237) pour recevoir la proforma.');
        return false;
      }
      // ECOPARK_QUOTE_PHONE:END
"""

QUOTE_PILOT_JS = r"""      // ECOPARK_QUOTE_PILOT:START
      // Production : le devis est enregistré en base (dépôt anonyme autorisé par la RLS).
      // En cas d'échec, le magasin est restauré et le visiteur est prévenu.
      if (window.EcoparkData && EcoparkData.driverName === 'supabase') {
        const submitted = loadDB().quotes.find(q => q.reference === ref);
        if (submitted) {
          submitted.phone = phone;
          EcoparkData.create('group_quotes', submitted, { legacy: true, anonymous: true }).then(function (res) {
            if (!res.ok) {
              EcoparkData.revertLegacy('quotes', function (q) { return q.reference === ref; }, ref);
              showToastSprint1('• ' + res.error.message + ' Votre demande ' + ref + " n'a pas été transmise.");
            }
          });
        }
      }
      // ECOPARK_QUOTE_PILOT:END
"""


def replace_between(text: str, start: str, end: str, block: str) -> tuple[str, bool]:
    """Remplace le bloc existant [start ... end] par la version à jour (ré-exécution du script)."""
    inner = block[block.index(start): block.index(end) + len(end)]
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: inner, text, count=1), True
    return text, False


def patch(html: str, config: dict) -> str:
    nl = "\r\n" if "\r\n" in html else "\n"
    to_nl = lambda s: s.replace("\r\n", "\n").replace("\n", nl)

    # 1-4. Bloc de tête : configuration, copie de secours, supabase-js, module EcoparkData
    head = to_nl(build_head_block(config))
    if HEAD_START in html:
        html = re.sub(re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END), lambda _: head.strip(), html, count=1, flags=re.S)
    else:
        anchor = "  <script>" + nl + "    // Inventaire contractuel complet des 77"
        assert html.count(anchor) == 1, "Ancre du script principal introuvable"
        html = html.replace(anchor, "  " + head.strip() + nl + nl + anchor, 1)

    # 5. Pont loadDB / saveDB
    bridge = to_nl(BRIDGE_JS)
    if JS_START in html:
        html, _ = replace_between(html, JS_START, JS_END, bridge)
    else:
        legacy = re.compile(
            r"    function loadDB\(\) \{\r?\n.*?\r?\n    \}\r?\n\r?\n    function saveDB\(db\) \{\r?\n.*?\r?\n    \}\r?\n", re.S)
        m = legacy.search(html)
        assert m, "Fonctions loadDB/saveDB d'origine introuvables"
        html = html[: m.start()] + bridge.lstrip(nl).rstrip() + nl + html[m.end():]

    # 6a. Bandeau météo : cible explicite (le 1er <span> est le point animé)
    if 'id="ahalaLiveWeatherText"' not in html:
        old = "<strong>En direct d'Ahala :</strong>" + nl + "                <span>"
        assert html.count(old) == 1, "Bandeau météo introuvable"
        html = html.replace(old, "<strong>En direct d'Ahala :</strong>" + nl + '                <span id="ahalaLiveWeatherText">', 1)

    # 6b. Dépôt de devis : numéro obligatoire en production
    phone_block = to_nl(QUOTE_PHONE_JS)
    if PHONE_START in html:
        html, _ = replace_between(html, PHONE_START, PHONE_END, phone_block)
    else:
        anchor = ("        showToastSprint1('• Veuillez indiquer un numéro WhatsApp valide (+237).');" + nl +
                  "        return false;" + nl + "      }" + nl)
        fn_start = html.index("function submitGroupQuoteSprint1() {")
        pos = html.find(anchor, fn_start)
        assert pos != -1 and pos - fn_start < 1500, "Validation du téléphone du devis introuvable"
        cut = pos + len(anchor)
        html = html[:cut] + phone_block.lstrip(nl) + html[cut:]

    # 6c. Dépôt de devis : écriture en base
    pilot = to_nl(QUOTE_PILOT_JS)
    if QUOTE_START in html:
        html, _ = replace_between(html, QUOTE_START, QUOTE_END, pilot)
    else:
        anchor = "      saveDB(db);" + nl + "      closeSprint1Modals();" + nl + "      showToastSprint1(`Devis Proforma ${ref}"
        assert html.count(anchor) == 1, "Fin de submitGroupQuoteSprint1 introuvable"
        html = html.replace(anchor, "      saveDB(db);" + nl + pilot.lstrip(nl) + "      closeSprint1Modals();" + nl +
                            "      showToastSprint1(`Devis Proforma ${ref}", 1)
    return html


def main():
    ap = argparse.ArgumentParser(description="Intégration de la couche EcoparkData")
    ap.add_argument("--env", default="local", choices=["local", "staging", "production"])
    ap.add_argument("--supabase-url", default="")
    ap.add_argument("--anon-key", default="")
    ap.add_argument("--out", default="", help="Écrit le résultat dans ce fichier au lieu de modifier le site (tests)")
    args = ap.parse_args()

    config = {"env": args.env, "dataDriver": "local", "snapshotVersion": None}
    if args.supabase_url or args.anon_key:
        if not (args.supabase_url and args.anon_key):
            sys.exit("--supabase-url et --anon-key doivent être fournis ensemble")
        if jwt_role(args.anon_key) == "service_role":
            sys.exit("REFUS : la clé fournie est une clé service_role. Seule la clé anon (publique) peut être intégrée au site.")
        config.update({"dataDriver": "supabase", "supabaseUrl": args.supabase_url.rstrip("/"), "supabaseAnonKey": args.anon_key})
    snapshot = json.loads(SNAPSHOT_JSON.read_text(encoding="utf-8"))
    config["snapshotVersion"] = snapshot.get("generatedAt")

    for target in (TARGETS[:1] if args.out else TARGETS):
        with open(target, "r", encoding="utf-8", newline="") as fh:
            html = fh.read()
        out = patch(html, config)
        high = [ch for ch in out if ord(ch) > 0x25FF]
        assert not high, f"Caractères interdits (> U+25FF) : {sorted(set(high))[:10]}"
        dest = Path(args.out) if args.out else target
        with open(dest, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)
        print(f"[OK] {dest.name} : pilote « {config['dataDriver']} » ({args.env}), {len(out)} octets")


if __name__ == "__main__":
    main()
