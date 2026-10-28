# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

for filename in ['etape0-site-live/index.html', 'Prototype_Interactif_ECOPARK_NEW_LOOK.html']:
    target = ROOT / filename
    with open(target, 'r', encoding='utf-8') as f:
        c = f.read()

    # Extract modalCgvBox block
    match = re.search(r'(<!-- MODALE CGV OFFICIELLES.*?<!-- ECOPARK_CGV_MODAL:END -->)', c, re.DOTALL)
    if not match:
        print(f'Error: modal not found in {filename}')
        continue
    modal_block = match.group(1).replace('<!-- ECOPARK_CGV_MODAL:END -->', '').strip()

    # Clean sprint1Toast
    c = re.sub(
        r'<div id="sprint1Toast"[^>]*><!-- ECOPARK_CGV_MODAL:START -->.*?<!-- ECOPARK_CGV_MODAL:END -->\s*</div>',
        '<div id="sprint1Toast" style="display:none;position:fixed;bottom:72px;right:18px;z-index:3500;max-width:420px;background:#1D490D;color:#FFFFFF;padding:14px 20px;border-radius:18px;box-shadow:0 16px 40px rgba(0,0,0,0.25);font-size:14.5px;font-weight:600;"></div>',
        c,
        flags=re.DOTALL
    )

    # Place modal inside modalOverlaySprint1
    target_overlay_close = "<!-- LEVIER 3 : BARRE D'ACTION RAPIDE MOBILE (ZONE DU POUCE) -->"
    insert_point = c.rfind('  </div>\n\n  ' + target_overlay_close)
    if insert_point == -1:
        insert_point = c.rfind('  </div>\r\n\r\n  ' + target_overlay_close)

    if insert_point == -1:
        print(f'Error: insert point not found in {filename}')
        continue

    new_c = c[:insert_point] + '\n\n    <!-- ECOPARK_CGV_MODAL:START -->\n    ' + modal_block + '\n    <!-- ECOPARK_CGV_MODAL:END -->\n' + c[insert_point:]

    # Also update openOfficialCgvModal to cleanly hide sibling modals
    new_c = new_c.replace(
        "window.openOfficialCgvModal = function () {\n    closeSprint1Modals();\n    var overlay = document.getElementById('modalOverlaySprint1');\n    var box = document.getElementById('modalCgvBox');\n    if (overlay) overlay.style.display = 'flex';\n    if (box) box.style.display = 'block';\n  };",
        "window.openOfficialCgvModal = function () {\n    closeSprint1Modals();\n    var overlay = document.getElementById('modalOverlaySprint1');\n    var box = document.getElementById('modalCgvBox');\n    var siblings = ['modalQuoteBox', 'modalCfpBox', 'modalRdvBox', 'modalWeeklyEventBox', 'modalOfficialPrintBox'];\n    siblings.forEach(function (id) { var el = document.getElementById(id); if (el) el.style.display = 'none'; });\n    if (overlay) overlay.style.display = 'flex';\n    if (box) box.style.display = 'block';\n  };"
    )

    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_c)

    print(f'Successfully updated {filename}')
