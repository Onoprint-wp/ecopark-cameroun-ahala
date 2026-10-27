# -*- coding: utf-8 -*-
"""
Script d'intégration des 4 Optimisations de Positionnement de l'Information :
1. Barre d'Aiguillage Express par Profil (#pubQuickIntentRouter) entre le Hero (PUB-01) et les 6 Univers (PUB-03).
2. Colonne Droite Sticky (#resStickySummaryCol) dans le Simulateur & Réservation (#view-RES) pour garder le Total FCFA et le Billet QR toujours visibles au scroll.
3. Barre de Conversion Flottante Mobile / Zone du Pouce (#mobileStickyConversionBar) synchronisée en temps réel avec l'odomètre FCFA.
4. Navigation Intelligente avec Halo Visuel d'Atterrissage (.section-focus-halo) sur les sections cibles (Tarifs PUB-10, Hébergement PUB-08, Restauration PUB-07, CFP PUB-12, RDV PUB-18).

Respect strict des invariants :
- Zéro caractère Unicode > 0x25FF
- Hauteur Hero = 455px, Hauteur Bento = 340px, 12 Stagger clips
- Odomètre initial = 14 000 FCFA -> +1 adulte = 18 500 FCFA
- Zéro code technique visible dans h1, h2, h3, .eyebrow hors .tech-code-tag
"""

import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "etape0-site-live" / "index.html"
PROTO_PATH = ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html"


def apply_positioning():
    raw_bytes = INDEX_PATH.read_bytes()
    has_crlf = b"\r\n" in raw_bytes
    text = raw_bytes.decode("utf-8").replace("\r\n", "\n")

    # -------------------------------------------------------------------------
    # 1. CSS : Styles pour #pubQuickIntentRouter, #resStickySummaryCol,
    #    .section-focus-halo et #mobileStickyConversionBar
    # -------------------------------------------------------------------------
    css_target = """    .rdv-confirm-pass.open {
      display: flex;
    }

  </style>"""

    css_replacement = """    .rdv-confirm-pass.open {
      display: flex;
    }

    /* ==========================================================================
       POSITIONNEMENT STRATÉGIQUE DE L'INFORMATION (4 LEVIERS UX / CRO)
       ========================================================================== */
    /* Levier 1 : Barre d'Aiguillage Express par Profil (4 Portes d'Entrée sous le Hero) */
    .quick-intent-shell {
      padding: 0 0 28px 0;
      background: linear-gradient(180deg, #FFFFFF 0%, var(--color-surface-soft) 100%);
      border-bottom: 1px solid rgba(29, 73, 13, 0.08);
    }
    .quick-intent-bar {
      background: #FFFFFF;
      border: 1.5px solid rgba(29, 73, 13, 0.14);
      border-radius: 22px;
      padding: 18px 20px;
      box-shadow: 0 14px 36px rgba(20, 34, 17, 0.06);
    }
    .quick-intent-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }
    .quick-intent-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }
    @media (max-width: 1024px) {
      .quick-intent-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    @media (max-width: 600px) {
      .quick-intent-grid {
        grid-template-columns: 1fr;
      }
    }
    .quick-intent-card {
      text-align: left;
      padding: 14px 16px;
      border-radius: 16px;
      border: 1.5px solid rgba(29, 73, 13, 0.12);
      background: var(--color-surface-soft);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.28s ease, box-shadow 0.28s ease, background 0.28s ease;
    }
    .quick-intent-card:hover {
      transform: translate3d(0, -3px, 0);
      border-color: #C47D2B;
      background: #FBF5EC;
      box-shadow: 0 12px 28px rgba(196, 125, 43, 0.14);
    }
    .quick-intent-card-ochre {
      background: #FBF5EC;
      border-color: rgba(196, 125, 43, 0.38);
    }
    .quick-intent-cta {
      font-size: 12.8px;
      font-weight: 700;
      color: var(--color-brand-deep);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    /* Levier 2 : Colonne Droite Sticky dans le Simulateur (#view-RES) */
    @media (min-width: 1024px) {
      #resMainGrid {
        align-items: start;
      }
      #resStickySummaryCol {
        position: sticky;
        top: 86px;
        align-self: start;
      }
    }

    /* Levier 3 : Barre d'Action Rapide Flottante Mobile (Zone du Pouce <= 960px) */
    .mobile-sticky-conversion-bar {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 2950;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(14px);
      border-top: 2px solid #C47D2B;
      padding: 10px 16px;
      box-shadow: 0 -10px 30px rgba(20, 34, 17, 0.14);
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    @media (max-width: 960px) {
      .mobile-sticky-conversion-bar {
        display: flex;
      }
      body {
        padding-bottom: 72px;
      }
    }
    body.viewport-mobile .mobile-sticky-conversion-bar {
      display: flex;
    }

    /* Levier 4 : Halo Visuel d'Atterrissage lors d'une navigation ciblée */
    @keyframes sectionHaloPulse {
      0% {
        box-shadow: 0 0 0 0 rgba(196, 125, 43, 0.55), 0 18px 42px rgba(196, 125, 43, 0.22);
      }
      70% {
        box-shadow: 0 0 0 10px rgba(196, 125, 43, 0), 0 18px 42px rgba(29, 73, 13, 0.12);
      }
      100% {
        box-shadow: none;
      }
    }
    .section-focus-halo {
      outline: 2.5px solid #C47D2B !important;
      outline-offset: 4px;
      border-radius: 20px;
      animation: sectionHaloPulse 1.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

  </style>"""

    assert css_target in text, "css_target introuvable"
    text = text.replace(css_target, css_replacement, 1)

    # -------------------------------------------------------------------------
    # 2. HTML Levier 1 : Insérer #pubQuickIntentRouter entre #sec-PUB-01 et #sec-PUB-03
    # -------------------------------------------------------------------------
    hero_end_target = """        <!-- CATALOGUE DES 6 PÔLES D'EXPÉRIENCES (PUB-02 à PUB-09, PUB-11, PUB-12) -->
        <div class="section section-soft" id="sec-PUB-03">"""

    hero_end_replacement = """        <!-- LEVIER 1 : BARRE D'AIGUILLAGE EXPRESS PAR PROFIL (RÈGLE DES 3 SECONDES SOUS LE HERO) -->
        <div class="quick-intent-shell" id="pubQuickIntentRouter">
          <div class="container">
            <div class="quick-intent-bar">
              <div class="quick-intent-header">
                <div style="display:flex;align-items:center;gap:8px;">
                  <span class="icon-medallion" style="width:30px;height:30px;"><svg class="svg-mono" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg></span>
                  <strong style="font-family:var(--font-heading);font-size:1.12rem;color:var(--color-brand-deep);">Accès Direct par Profil — Que souhaitez-vous organiser aujourd'hui ?</strong>
                </div>
                <span style="font-size:12.5px;color:var(--color-text-muted);font-weight:600;">Orientation en 1 clic • Tarifs 100 % transparents en FCFA</span>
              </div>
              <div class="quick-intent-grid">
                <button type="button" class="quick-intent-card quick-intent-card-ochre" onclick="routeVisitorByProfile('FAMILLE')">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:4px;">
                      <strong style="font-family:var(--font-heading);font-size:1.04rem;color:var(--color-brand-deep);">1. Sortie Famille &amp; Week-end</strong>
                      <span class="price-pill" style="font-size:11px;padding:2px 7px;">Dès 500 FCFA</span>
                    </div>
                    <span style="font-size:13px;color:var(--color-text-muted);display:block;">Pass Tout-Inclus Coupe-File (Zoo « ToTo », Piscine, Pirogue &amp; Repas).</span>
                  </div>
                  <span class="quick-intent-cta" style="color:#8E5617;">Voir les 3 Pass Tout-Inclus →</span>
                </button>

                <button type="button" class="quick-intent-card" onclick="routeVisitorByProfile('HOTEL')">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:4px;">
                      <strong style="font-family:var(--font-heading);font-size:1.04rem;color:var(--color-brand-deep);">2. Séjour &amp; Loges Hôtelières</strong>
                      <span class="price-pill" style="font-size:11px;padding:2px 7px;">10k – 30k FCFA</span>
                    </div>
                    <span style="font-size:13px;color:var(--color-text-muted);display:block;">Repos en journée ou nuitée au calme : Cités Bene, Chanthel &amp; Ewondo VIP.</span>
                  </div>
                  <span class="quick-intent-cta">Choisir ma Cité Hôtelière →</span>
                </button>

                <button type="button" class="quick-intent-card" onclick="routeVisitorByProfile('B2B_ECOLE')">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:4px;">
                      <strong style="font-family:var(--font-heading);font-size:1.04rem;color:var(--color-brand-deep);">3. Écoles, Séminaires &amp; Galas</strong>
                      <span class="price-pill" style="font-size:11px;padding:2px 7px;">Proforma 2 min</span>
                    </div>
                    <span style="font-size:13px;color:var(--color-text-muted);display:block;">Salle « Menkii Essomba Anton », Traiteur &amp; Navettes 18/32 places.</span>
                  </div>
                  <span class="quick-intent-cta">Calculer ma Proforma Groupe →</span>
                </button>

                <button type="button" class="quick-intent-card" onclick="routeVisitorByProfile('CFP')">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;margin-bottom:4px;">
                      <strong style="font-family:var(--font-heading);font-size:1.04rem;color:var(--color-brand-deep);">4. Formation CFP MINEFOP</strong>
                      <span class="price-pill" style="font-size:11px;padding:2px 7px;">50k + 4 tranches</span>
                    </div>
                    <span style="font-size:13px;color:var(--color-text-muted);display:block;">5 filières dès 16 ans (Hôtellerie, Cuisine, Déco, Agro, Pisciculture).</span>
                  </div>
                  <span class="quick-intent-cta">Déposer ma candidature CFP →</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- CATALOGUE DES 6 PÔLES D'EXPÉRIENCES (PUB-02 à PUB-09, PUB-11, PUB-12) -->
        <div class="section section-soft" id="sec-PUB-03">"""

    assert hero_end_target in text, "hero_end_target introuvable"
    text = text.replace(hero_end_target, hero_end_replacement, 1)

    # -------------------------------------------------------------------------
    # 3. HTML Levier 2 : Ajouter id="resMainGrid" et id="resStickySummaryCol" dans #view-RES
    # -------------------------------------------------------------------------
    res_grid_target = """            <div class="grid-12">
              <!-- Colonne gauche : Configurateur & Simulateur (RES-01, RES-02, RES-03, RES-05) -->"""
    res_grid_replacement = """            <div class="grid-12" id="resMainGrid">
              <!-- Colonne gauche : Configurateur & Simulateur (RES-01, RES-02, RES-03, RES-05) -->"""
    assert res_grid_target in text, "res_grid_target introuvable"
    text = text.replace(res_grid_target, res_grid_replacement, 1)

    res_right_col_target = """              <!-- Colonne droite : Panier, Paiement Mobile Money sans PIN & Billet QR Démo (RES-04, RES-07 à RES-12) -->
              <div class="col-5" style="display:flex;flex-direction:column;gap:20px;">"""
    res_right_col_replacement = """              <!-- Colonne droite Sticky : Panier, Paiement Mobile Money sans PIN & Billet QR Démo (RES-04, RES-07 à RES-12) -->
              <div class="col-5" id="resStickySummaryCol" style="display:flex;flex-direction:column;gap:20px;">"""
    assert res_right_col_target in text, "res_right_col_target introuvable"
    text = text.replace(res_right_col_target, res_right_col_replacement, 1)

    # -------------------------------------------------------------------------
    # 4. HTML Levier 3 : Barre d'action rapide mobile (#mobileStickyConversionBar)
    # -------------------------------------------------------------------------
    toast_target = """  <!-- Notification Toast Apple-Grade -->
  <div id="sprint1Toast" """
    toast_replacement = """  <!-- LEVIER 3 : BARRE D'ACTION RAPIDE MOBILE (ZONE DU POUCE) -->
  <div class="mobile-sticky-conversion-bar" id="mobileStickyConversionBar" aria-label="Accès rapide réservation et WhatsApp">
    <div>
      <span style="font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--color-text-muted);display:block;font-weight:700;" id="stickyBarPaxText">2 Adultes, 2 Enfants • Pass QR</span>
      <strong style="font-family:var(--font-heading);font-size:1.25rem;color:var(--color-brand-deep);" id="stickyBarTotalFcfa">14 000 FCFA</strong>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="padding:8px 12px;font-size:12.5px;" onclick="openStickyWhatsAppQuick()">
        <svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> WhatsApp
      </button>
      <button type="button" class="btn btn-primary btn-sm" style="padding:8px 14px;font-size:12.5px;" onclick="navigateFamily('RES', 'RES-03')">
        Réserver mon Pass
      </button>
    </div>
  </div>

  <!-- Notification Toast Apple-Grade -->
  <div id="sprint1Toast" """
    assert toast_target in text, "toast_target introuvable"
    text = text.replace(toast_target, toast_replacement, 1)

    # -------------------------------------------------------------------------
    # 5. JS Levier 4 & Synchronisation Sticky Bar + Aiguillage par Profil
    # -------------------------------------------------------------------------
    old_nav_js = """    function navigateFamily(family, screenId) {
      document.querySelectorAll('.family-view').forEach(el => el.classList.remove('active'));
      const targetView = document.getElementById('view-' + family);
      if (targetView) targetView.classList.add('active');

      document.querySelectorAll('.main-nav .nav-item').forEach(el => el.classList.remove('active'));
      const navBtn = document.getElementById('nav-' + family);
      if (navBtn) navBtn.classList.add('active');

      inspectScreen(screenId || (family + '-01'));
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function inspectScreen(screenId) {
      currentScreenId = screenId;
      const found = SCREENS_77.find(s => s.id === screenId) || SCREENS_77[8];
      document.getElementById('currentScreenCode').textContent = found.id;
      document.getElementById('currentScreenTitle').textContent = found.title;
      document.getElementById('currentScreenFamilyLabel').textContent = `(Famille : ${found.family} • 77/77 écrans couverts)`;
      renderInspectorPills();

      const anchorSection = document.getElementById('sec-' + screenId);
      if (anchorSection) {
        anchorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }"""

    new_nav_js = """    function triggerSectionFocusHalo(el) {
      if (!el) return;
      document.querySelectorAll('.section-focus-halo').forEach(n => n.classList.remove('section-focus-halo'));
      void el.offsetWidth;
      el.classList.add('section-focus-halo');
      clearTimeout(window._haloTimer);
      window._haloTimer = setTimeout(() => {
        el.classList.remove('section-focus-halo');
      }, 1850);
    }

    function navigateFamily(family, screenId) {
      document.querySelectorAll('.family-view').forEach(el => el.classList.remove('active'));
      const targetView = document.getElementById('view-' + family);
      if (targetView) targetView.classList.add('active');

      document.querySelectorAll('.main-nav .nav-item').forEach(el => el.classList.remove('active'));
      const navMap = {
        'PUB-10': 'nav-TARIFS',
        'PUB-08': 'nav-HOTELS',
        'PUB-09': 'nav-HOTELS',
        'PUB-07': 'nav-SAVEURS',
        'PUB-12': 'nav-CFP'
      };
      const mappedId = (screenId && navMap[screenId]) ? navMap[screenId] : ('nav-' + family);
      const navBtn = document.getElementById(mappedId) || document.getElementById('nav-' + family);
      if (navBtn) navBtn.classList.add('active');

      const targetScreen = screenId || (family + '-01');
      const anchorSection = document.getElementById('sec-' + targetScreen);
      if (!anchorSection || targetScreen === 'PUB-01' || targetScreen === 'RES-01') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      inspectScreen(targetScreen);
    }

    function inspectScreen(screenId) {
      currentScreenId = screenId;
      const found = SCREENS_77.find(s => s.id === screenId) || SCREENS_77[8];
      document.getElementById('currentScreenCode').textContent = found.id;
      document.getElementById('currentScreenTitle').textContent = found.title;
      document.getElementById('currentScreenFamilyLabel').textContent = `(Famille : ${found.family} • 77/77 écrans couverts)`;
      renderInspectorPills();

      const anchorSection = document.getElementById('sec-' + screenId);
      if (anchorSection && screenId !== 'PUB-01') {
        anchorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        triggerSectionFocusHalo(anchorSection);
      }
    }

    function routeVisitorByProfile(profileKey) {
      if (profileKey === 'FAMILLE') {
        navigateFamily('PUB', 'PUB-10');
        const grid = document.getElementById('pubSalesBundlesGrid');
        if (grid) triggerSectionFocusHalo(grid);
        showToastSprint1('• Parcours Famille & Week-end : Choisissez un Pass Tout-Inclus en 1 clic ou simulez à la carte.');
      } else if (profileKey === 'HOTEL') {
        navigateFamily('PUB', 'PUB-08');
        showToastSprint1('• Hébergement au calme : Cités Bene (10k), Chanthel (15k) et Ewondo VIP (25k FCFA).');
      } else if (profileKey === 'B2B_ECOLE') {
        navigateFamily('PUB', 'PUB-11');
        openQuoteModalSprint1();
      } else if (profileKey === 'CFP') {
        navigateFamily('PUB', 'PUB-12');
        openCfpModalSprint1();
      }
    }

    function openStickyWhatsAppQuick() {
      navigateFamily('RES', 'RES-04');
      const waCard = document.getElementById('whatsappConciergeCard');
      if (waCard) {
        setTimeout(() => {
          waCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          triggerSectionFocusHalo(waCard);
        }, 80);
      }
    }"""

    assert old_nav_js in text, "old_nav_js introuvable"
    text = text.replace(old_nav_js, new_nav_js, 1)

    # Synchroniser #stickyBarTotalFcfa et #stickyBarPaxText dans syncWhatsAppConciergeView()
    old_wa_sync_end = """      const delivTitle = document.getElementById('waDeliveryTitle');
      if (delivTitle) delivTitle.textContent = `E-Billet QR Actif : ${ref} (${total})`;"""

    new_wa_sync_end = """      const delivTitle = document.getElementById('waDeliveryTitle');
      if (delivTitle) delivTitle.textContent = `E-Billet QR Actif : ${ref} (${total})`;

      const stickyTot = document.getElementById('stickyBarTotalFcfa');
      const stickyPax = document.getElementById('stickyBarPaxText');
      if (stickyTot) stickyTot.textContent = total;
      if (stickyPax) stickyPax.textContent = `${counts.adults} Adulte(s), ${counts.children} Enfant(s) • Pass QR`;"""

    assert old_wa_sync_end in text, "old_wa_sync_end introuvable"
    text = text.replace(old_wa_sync_end, new_wa_sync_end, 1)

    # -------------------------------------------------------------------------
    # VÉRIFICATION : ZÉRO CARACTÈRE UNICODE > 0x25FF + NODE --CHECK
    # -------------------------------------------------------------------------
    bad_chars = [(i, ch, hex(ord(ch))) for i, ch in enumerate(text) if ord(ch) > 0x25FF]
    if bad_chars:
        raise ValueError(f"Caractères > 0x25FF détectés : {bad_chars[:10]}")

    out_bytes = (text.replace("\n", "\r\n") if has_crlf else text).encode("utf-8")
    INDEX_PATH.write_bytes(out_bytes)
    shutil.copyfile(INDEX_PATH, PROTO_PATH)

    # Vérifier la syntaxe JS avec node --check
    s_idx = text.rfind("<script>") + len("<script>")
    e_idx = text.rfind("</script>")
    scratch_js = ROOT / "scratch_check.js"
    scratch_js.write_text(text[s_idx:e_idx], encoding="utf-8")
    res = subprocess.run(["node", "--check", str(scratch_js)], capture_output=True, text=True)
    scratch_js.unlink(missing_ok=True)
    if res.returncode != 0:
        raise RuntimeError(f"Erreur de syntaxe JS :\n{res.stderr}")

    print(f"SUCCÈS : 4 optimisations de positionnement appliquées et validées ({len(text.splitlines())} lignes, node --check OK, 0 emoji OS).")


if __name__ == "__main__":
    apply_positioning()
