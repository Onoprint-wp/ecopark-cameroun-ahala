# -*- coding: utf-8 -*-
"""
Durcissement : échappement HTML des données saisies par les visiteurs dans les tableaux
historiques du site (Mon Espace, guichet, exploitation, rendez-vous, CFP, ticket de caisse).

Avant : `<td>${q.org}</td>` -> un nom d'organisation contenant du HTML était interprété
(injection). Après : `<td>${escHtml(q.org)}</td>`.

Ne touche pas aux valeurs placées entre apostrophes dans un attribut onclick (références
générées par le système, contexte JavaScript traité séparément).
Ré-exécutable. Met à jour index.html ET le prototype.
Usage : python build_escape_legacy.py
"""
import re

from build_data_layer import TARGETS

HELPER_MARK = "// ECOPARK_ESCAPE_HELPER"
HELPER = (
    "    function escHtml(v) { " + HELPER_MARK + "\n"
    "      return String(v == null ? '' : v).replace(/[&<>\"']/g, function (c) {\n"
    "        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', \"'\": '&#39;' }[c];\n"
    "      });\n"
    "    }\n\n"
)
OBJ = r"[A-Za-z_]\w*"  # b, q, latestQ, latestRdv, qt...
FIELDS = r"(?:reference|date|paxSummary|org|pax|type|status|holder|visitorName|purposeLabel|slot|name|track|phone|actor|action|mode|refundRef)"
PATTERN = re.compile(r"(?<!')\$\{(" + OBJ + r"\." + FIELDS + r")\}")
# Variables locales reprises telles quelles d'un formulaire (récapitulatifs, proforma, billet)
BARE = re.compile(r"(?<!')\$\{(visitorName|org|purposeLabel|name|phone|holder|type|date|slot)\}")
HTML_LINE = re.compile(r"<(td|strong|div|span|em|li|p|b)\b|</(td|strong|div|span|em|li|p|b)>")


def patch(html: str):
    nl = "\r\n" if "\r\n" in html else "\n"
    if HELPER_MARK not in html:
        anchor = "    function formatFCFA(num) {"
        assert html.count(anchor) == 1, "formatFCFA() introuvable"
        html = html.replace(anchor, HELPER.replace("\n", nl) + anchor, 1)
    lines = html.split(nl)
    changed = 0
    for i, line in enumerate(lines):
        if "${" not in line or not HTML_LINE.search(line):
            continue
        new, n = PATTERN.subn(lambda m: "${escHtml(" + m.group(1) + ")}", line)
        new, n2 = BARE.subn(lambda m: "${escHtml(" + m.group(1) + ")}", new)
        n += n2
        if n:
            lines[i] = new
            changed += n
    return nl.join(lines), changed


def main():
    for target in TARGETS:
        with open(target, "r", encoding="utf-8", newline="") as fh:
            html = fh.read()
        out, n = patch(html)
        with open(target, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)
        print(f"[OK] {target.name} : {n} insertion(s) échappée(s)")


if __name__ == "__main__":
    main()
