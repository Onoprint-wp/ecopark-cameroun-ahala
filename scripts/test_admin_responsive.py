# -*- coding: utf-8 -*-
"""
Contrôle de mise en page responsive de la console /admin (5 largeurs).
Vérifie qu'aucun bloc ne déborde de sa carte et que les boutons des jauges restent visibles.
Prérequis : npm run dev. Lancement : python scripts/test_admin_responsive.py
"""
import shutil
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "audit-assets" / "qa-etape0-live"
ART = Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\7ee4ce6d-03a1-4262-8080-a7fbda05ab9a")
WIDTHS = [1440, 1280, 1024, 768, 390]
results = []


def check(cond, label, detail=""):
    results.append(bool(cond))
    print(f"  [{'OK' if cond else 'FAIL'}] {label}{(' — ' + str(detail)) if detail else ''}")


MEASURE = """() => {
  const out = { overflowingCards: [], escaping: [], quotaScroll: 0, hiddenButtons: 0 };
  document.querySelectorAll('#view-ADM .adm-card').forEach(card => {
    const cr = card.getBoundingClientRect();
    if (card.scrollWidth > card.clientWidth + 1) out.overflowingCards.push(card.id);
    card.querySelectorAll('select, textarea, input, button, .adm-weather-preview').forEach(el => {
      if (el.closest('.table-responsive')) return;
      const r = el.getBoundingClientRect();
      if (r.width && (r.right > cr.right + 1 || r.left < cr.left - 1)) out.escaping.push(card.id + ' > ' + (el.id || el.tagName));
    });
  });
  const tr = document.querySelector('#sec-ADM-03 .table-responsive');
  out.quotaScroll = tr ? tr.scrollWidth - tr.clientWidth : 0;
  document.querySelectorAll('#admQuotaBody [data-act="quota-save"]').forEach(b => {
    const r = b.getBoundingClientRect(), t = tr.getBoundingClientRect();
    if (r.right > t.right + 1) out.hiddenButtons++;
  });
  out.pageScroll = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  // Débord propre à la console (le menu horizontal du site défile volontairement sur mobile)
  const vw = document.documentElement.clientWidth;
  out.consoleOverflow = Array.from(document.querySelectorAll('#view-ADM .adm-console > *'))
    .filter(el => el.getBoundingClientRect().right > vw + 1).map(el => el.id || el.className);
  return out;
}"""


def main():
    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in WIDTHS:
            print(f"\nLargeur {w}px")
            page = browser.new_page(viewport={"width": w, "height": 900})
            page.goto("http://localhost:3000/admin", wait_until="networkidle")
            page.wait_for_function("() => window.EcoparkAdmin && EcoparkAdmin.state.loaded", timeout=8000)
            m = page.evaluate(MEASURE)
            check(not m["overflowingCards"], "Aucune carte ne déborde", m["overflowingCards"])
            check(not m["escaping"], "Aucun champ ne sort de sa carte", m["escaping"][:4])
            check(not m["consoleOverflow"], "La console tient dans la largeur de l'écran", m["consoleOverflow"][:4])
            check(m["quotaScroll"] <= 1 and m["hiddenButtons"] == 0, "Tableau des jauges entier, boutons visibles",
                  f"débord {m['quotaScroll']} px, {m['hiddenButtons']} bouton(s) masqué(s)")
            if w in (1440, 1024, 390):
                page.locator("#sec-ADM-03").scroll_into_view_if_needed()
                page.wait_for_timeout(250)
                path = SHOTS / f"phase4_responsive_jauges_{w}px.png"
                page.locator("#sec-ADM-03").screenshot(path=str(path))
                shots.append(path)
            page.close()
        browser.close()
    for s in shots:
        if ART.exists():
            shutil.copy(s, ART / s.name)
    ok = sum(results)
    print(f"\n{ok}/{len(results)} vérifications réussies.")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
