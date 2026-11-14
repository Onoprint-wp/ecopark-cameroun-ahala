# 06 - Rapport QA Visuel & Métriques Avant / Après (Phase 3 - Passe Unifiée Finale)

- **Branche** : `audit/typography-accessibility-v3` (après Lots 1, 2, 3, correctifs ARIA/clavier/inert/CLS/zoom 200% et re-build final ; aucune fusion ni déploiement)
- **Date de vérification unifiée** : 2026-11-14
- **Environnement mesuré (run unique final post-retouches)** :
  - **Bundle production `dist/` via `vite preview` (`http://127.0.0.1:4173`)** : **346 contextes** en passe unifiée Playwright Chromium headless (`308` contextes publics sur `14` routes x `11` viewports x `2` thèmes Light/Dark + `12` contextes zoom `200%` + `15` états interactifs + `11` contextes Cockpit Pro `/exploitation` RBAC/modale).
  - **Atelier Chromatique DEV via `vite dev` (`http://127.0.0.1:5177`)** : **14 contextes** (`ColorAtlasDrawer` onglets `#pillars`, `#scales` x5 familles Light & Dark, `#tester`, plus test clavier `Escape`).
  - **Total passe unifiée finale** : **`360` contextes**, `9` tests clavier automatisés, `3` simulations daltonisme (`deuteranopia`, `protanopia`, `tritanopia`), `4` sondes `<option value="domaine">` sur `SpeciesAtlas`, `5` mesures CLS (`PerformanceObserver layout-shift`), et **`59` PNG** régénérés dans `docs/ux-audit/screenshots/after/`.
  - **Outillage sans pollution `package.json`** : Python Playwright Chromium headless, conversions couleur `oklch`/Canvas RGBA pour contraste W3C WACG 2.1, animations CSS figées après stabilisation des View Transitions (`650ms` après bascule thème) lors des captures et mesures DOM.
- **Référentiel Phase 1** : [03_TYPOGRAPHY_FINDINGS.md](./03_TYPOGRAPHY_FINDINGS.md), [04_RESPONSIVE_AND_REFLOW_MATRIX.md](./04_RESPONSIVE_AND_REFLOW_MATRIX.md), [05_COMPONENT_REMEDIATION_PLAN.md](./05_COMPONENT_REMEDIATION_PLAN.md), [ECOPARK_TYPOGRAPHY_TOKENS_V3.md](../design/ECOPARK_TYPOGRAPHY_TOKENS_V3.md).

---

## 1. Synthèse Quantitative Avant / Après (Passe Unifiée `360` Contextes)

| Indicateur audité | Baseline Phase 1 (`before`) | Passe Unifiée Finale (`360` contextes, build final) | Statut |
| :--- | :---: | :--- | :---: |
| **Contextes évalués** | `40` routes/états (`211` scans) | **`360` contextes** (`308` public + `12` zoom 200% + `15` interactifs + `11` cockpit + `14` ColorAtlas DEV) | **PASS** |
| **Erreurs console / runtime JS** | - | **`0` `console_errors` / `0` `page_errors`** sur `360` contextes | **PASS** |
| **Contrastes actifs `< AA` (`4.5:1` / `3:1`)** | **588** | **`0 / 360`** (`ColorAtlasDrawer` `#scales` x5 familles L/D & `#tester` inclus ; `--text-muted` mesuré entre **`10.29:1` et `11.71:1`**) | **PASS** |
| **Contrôles RBAC désactivés** | `66` | Exemptés WCAG 2.2 (1.4.3 / 1.4.11 inactifs sur `guichet` / `comptable`), isolés hors défauts actifs | **Exempté** |
| **Troncatures / clipping critique (`clippingIssues`)** | **858** | **`0 / 360`** (`splitWords = 0`, `ancestorClip = 0`) | **PASS** |
| **Débordements horizontaux boîte (`boxOverflows`)** | **183** | **`0 / 360`** (tableaux dotés d'`overflow-x-auto` et badges/KPI/jauges adaptatifs y compris `/exploitation` à `390x844` zoom `200%`) | **PASS** |
| **Débordement documentaire racine (`docOverflowX`)** | `0` | **`0 / 360`** (`documentElement.scrollWidth === vw` de `320px` à `1920px`, reflow `640x400` et zoom `200%`) | **PASS** |
| **Micro-textes publics `< 12px` (`tinyPublic`)** | **6 665** | **`0 / 360`** | **PASS** |
| **Micro-textes cockpit `< 12px` (`tinyCockpit`)** | **438** (`< 11px`) | **`0 / 360`** (plancher `12px` y compris 28 labels SVG de l'histogramme `RangerDashboard`) | **PASS** |
| **Corps éditorial `< 16px` (`bodyUnder16`)** | **5 112** | **`0 / 360`** (`.type-body` `16px` mobile / `17px` desktop, tracking `0em`) | **PASS** |
| **Navigation `< 14px` (`navUnder14`)** | **711** | **`0 / 360`** (`.type-nav` `14px` / `28px` sous zoom `200%`) | **PASS** |
| **Display `Barlow` `< 20px` (`displayUnder20`)** | présent | **`0 / 360`** | **PASS** |
| **Cockpit `>= 20px` ou `Barlow` (`cockpitOver20` / `cockpitBarlow`)** | `16px` h1 uniforme / `24px` AuthPortal | **`0 / 11`** (Profil C strict `< 20px` `Source Sans 3` / `Mono` y compris page login `/exploitation` `AuthPortal` `type-cockpit-h2` `17px`) | **PASS** |
| **Cibles tactiles HTML autonomes `< 44px` (`vw <= 1024px`)** | **2 731** | **`0 / 360`** (`touchUnder44 = 0`, dont checkbox Charte `shrink-0` `16x16` dans `<label>` `>= 44px` et contrôles `768-1024px`) | **PASS** |
| **Textes SVG `< 12px` (`svgTextIssues`)** | `35+` | **`0 / 360`** | **PASS** |
| **Polices web chargées (`fontsMissing`)** | - | **`0 / 360`** (`Barlow Semi Condensed`, `Source Sans 3`, `JetBrains Mono` chargées) | **PASS** |
| **Tests unitaires / E2E (`npm test`)** | `32/32` | **`37/37` sous-tests (`10` blocs `node:test`, `0` échec)** sans modification des tests | **PASS** |
| **TypeScript (`tsc -p tsconfig.app.json --noEmit` & `tsc -b`)** | `0` | **`0` erreur**, build Vite production vert (`dist/`) | **PASS** |
| **Loi 1 (`U+2013` / `U+2014`)** | `0` (`index.html`/`src/`) | **`0`** sur `index.html`, `tailwind.config.js`, `src/`, `styles/`, `tokens/`, `docs/ux-audit/06..08` | **PASS** |

---

## 2. Périmètre & Ventilation des `360` Contextes de la Passe Finale

1. **`public_matrix` (`308` contextes)** : `14` routes (`/`, `/hebergements`, `/restaurant`, `/tarifs`, `/pack-entreprise`, `/formation`, `/activites`, `/decouvrir`, `/reserver`, `/mon-espace`, `/connexion`, `/mentions-legales`, `/cgv`, `/confidentialite`) x `11` viewports (`320x700`, `360x800`, `390x844`, `430x932`, `640x400` reflow, `768x1024`, `1024x768`, `1280x800`, `1366x768`, `1440x900`, `1920x1080`) x `2` thèmes (`light`, `dark`). Résultat : **`0` erreur** sur tous indicateurs.
2. **`zoom200` (`12` contextes)** : simulation `html { font-size: 32px }` (`200%`) à `390x844` et `1440x900` sur `/`, `/decouvrir`, `/reserver`, `/tarifs`, `/activites` et `/exploitation` (session `admin` authentifiée). Résultat : **`0` `docOverflowX`**, **`0` `boxOverflows`**, **`0` `clippingIssues`**, **`0` `contrastErrors`**.
3. **`interactive_states` (`15` contextes)** :
   - `mobile_drawer` (`320x700`, `390x844`)
   - `bento_drawer` (`1440x900`, `390x844`)
   - `booking_step2_errors_390x844` (déclenchement et contraste `--status-danger-text` des erreurs) & `booking_step3_390x844`
   - `ecopass_recto_390x844`, `ecopass_verso_390x844`, `ecopass_sunlight_1440x900`, `ecopass_oled_in_light_1440x900`, `ecopass_oled_dark_1440x900`
   - `sentinel_form_1440x900`, `sentinel_feed_1440x900`, `sentinel_form_390x844`, `sentinel_feed_390x844` (après inscription client authentifiée)
   Résultat : **`0` erreur** sur les `15` états (`0` contraste, `0` boxOverflow, `0` touchUnder44).
4. **`cockpit` (`11` contextes `/exploitation`)** :
   - `unauth` (`1440x900` light) & `client_403` (`1440x900` light)
   - `admin` (`1440x900` light & dark, `390x844`, `430x932`, `320x700`, `1024x768`), `modal_closure` (`1440x900` light)
   - `guichet` (`1440x900` light) & `comptable` (`1440x900` light)
   Résultat : **`0` erreur** sur les `11` contextes (`cockpitOver20 = 0`, `cockpitBarlowCount = 0`, `contrastErrorsCount = 0`, `boxOverflowsCount = 0`, `touchUnder44Count = 0`).
5. **`color_atlas_dev` (`14` contextes DEV sur `vite dev` `5177`)** :
   - Ouverture du tiroir `ColorAtlasDrawer`, onglets `#pillars`, `#scales` sur les `5` familles (`forest`, `leaf`, `earth`, `mist`, `bark`) et `#tester`, en **Light** puis en **Dark** (`2 x 7 = 14` contextes). Résultat : **`0` erreur** sur tous indicateurs (`contrastErrorsCount = 0`, `boxOverflowsCount = 0`, `touchUnder44Count = 0`).

---

## 3. Mesure Réelle du `<select>` UICN `SpeciesAtlas` (`option[value="domaine"]`)

Libellé métier intact : `"Élevage, Bassins & Flore (LC / NT)"` (aucun raccourcissement). Pour éliminer le léger débordement interne mesuré initialement à `320x700` sans altérer le texte métier, le conteneur filtres de `SpeciesAtlas.tsx` passe à `p-2.5 sm:p-5` et le `<select>` adopte `appearance-none pl-[8px] pr-[22px] sm:pl-2.5 sm:pr-7` avec chevron décoratif `aria-hidden="true"`.

Mesures Playwright réelles sur le build final (`vite preview`, largeur Canvas `textWidth` vs largeur intérieure `innerAvail = rectW - pl - pr`) :

| Contexte (`/decouvrir`) | `fontSize` | `rectW` (`px`) | `clientW / scrollW` (`px`) | Padding L / R (`px`) | `innerAvail` (`px`) | `textWidth` (`px`) | Marge (`innerAvail - textWidth`) | `docScrollW / vw` | `cardOverflow` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `320x700` | `16px` | `253.19` | `251 / 251` | `8 / 22` | `221.19` | `219.45` | **`+1.74 px`** | `320 / 320` | `false` |
| `390x844` | `16px` | `320.39` | `318 / 318` | `8 / 22` | `288.39` | `219.45` | **`+68.94 px`** | `390 / 390` | `false` |
| `1440x900` | `14px` | `233.00` | `231 / 231` | `10 / 28` | `193.00` | `192.02` | **`+0.98 px`** | `1440 / 1440` | `false` |
| `390x844` zoom `200%` (`32px`) | `32px` | `300.39` | `298 / 447` | `8 / 22` | `268.39` | `438.89` | **`-170.50 px`** *(clipping natif boîte fermée sans débordement page/carte)* | `390 / 390` | `false` |

> **Constats factuels** : à `320x700`, `390x844` et `1440x900`, l'intitulé complet `"Élevage, Bassins & Flore (LC / NT)"` tient intégralement dans le `<select>` avec marge positive (`+1.74 px`, `+68.94 px`, `+0.98 px`). Sous zoom texte `200%` (`32px`) à `390px`, le libellé de `34` caractères mesure `438.89 px` (plus large que le viewport `390 px` lui-même), si bien que le `<select>` fermé tronque visuellement à `268.39 px` sans jamais provoquer de débordement carte ni page (`docScrollW = 390 === vw`, `cardOverflow = false`) ; l'ouverture du menu déroulant natif relève du rendu OS/navigateur.

---

## 4. Tests Complémentaires Automatisables : Daltonisme, Clavier & CLS

### 4.1. Modes Daltonisme (`Navbar` -> `ThemeContext`)

| Mode activé | Attribut `data-vision` | Filtre SVG appliqué | `docOverflowX` | `contrastErrorsCount` | Capture archivée |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `deuteranopia` | `deuteranopia` | `url("#filter-deuteranopia")` | `false` | **`0`** | `state_daltonism_deuteranopia_1440x900.png` |
| `protanopia` | `protanopia` | `url("#filter-protanopia")` | `false` | **`0`** | *(contrôlé DOM/CSS)* |
| `tritanopia` | `tritanopia` | `url("#filter-tritanopia")` | `false` | **`0`** | *(contrôlé DOM/CSS)* |

### 4.2. Navigation Clavier Automatisée (`9 / 9` PASS)

| # | Scénario testé en Playwright | Assertions vérifiées | Résultat |
| :---: | :--- | :--- | :---: |
| 1 | `Navbar_mobile_drawer_Escape` (`390x844`) | Ouverture `#mobile-nav-drawer` -> `Escape` ferme le tiroir et restaure le focus sur le bouton d'ouverture | **PASS** |
| 2 | `Tab_ShiftTab_focus_visible` (`/`) | `Tab` puis `Shift+Tab` valident `:focus-visible` avec anneau visible `3px solid` | **PASS** |
| 3 | `AhalaShowcase_ArrowRight_ArrowLeft` (`/`) | `ArrowRight` bascule vers `#showcase-tab-saveurs` (`aria-selected="true"`, panneau visible), `ArrowLeft` revient sur `#showcase-tab-hebergements` | **PASS** |
| 4 | `Navbar_daltonism_dropdown_Escape` (`1440x900`) | Ouverture menu daltonisme -> `Escape` ferme (`aria-expanded="false"`) et restaure le focus sur le déclencheur | **PASS** |
| 5 | `DigitalEcoPass_Recto_Verso_inert_Tab` (`/mon-espace`) | `0` fuite `Tab` sur `12` pressions vers la face masquée (`inert` + `aria-hidden`), bascule clavier `Enter` Recto <-> Verso transfère et restaure proprement le focus | **PASS** |
| 6 | `RangerDashboard_Modal1_closure_ARIA_trap_Escape` (`/exploitation`) | Modale 1 (`role="dialog"`, `aria-modal="true"`, `aria-labelledby="ranger-modal-closure-title"`), focus initial à l'intérieur, `12` `Tab` piégés (`trapEscaped: false`), `Escape` ferme et rend le focus au bouton `"Fermer"` | **PASS** |
| 7 | `RangerDashboard_Modal2_resolve_ARIA_Escape` (`/exploitation`) | Modale 2 (`ranger-modal-resolve-title`), focus intérieur et fermeture `Escape` | **PASS** |
| 8 | `ColorAtlasDrawer_Escape` (`vite dev` `5177`) | Ouverture du tiroir chromatique et fermeture propre via `Escape` | **PASS** |
| 9 | `RangerDashboard_Modal3_reset_ARIA_Escape` (`/exploitation`) | Modale 3 (`ranger-modal-reset-title`, Reset DEV), focus intérieur et fermeture `Escape` | **PASS** |

### 4.3. Mesure CLS (`PerformanceObserver` `layout-shift` sans entrée utilisateur)

| Route mesurée | CLS mesuré (build final) | Seuil Google CWV ("Bon" `<= 0.10`) |
| :--- | :---: | :---: |
| `/` | **`0.05446`** | **PASS** |
| `/activites` | **`0.00582`** | **PASS** |
| `/decouvrir` | **`0.00775`** | **PASS** |
| `/reserver` | **`0.00467`** | **PASS** |
| `/exploitation` | **`0`** *(corrigé depuis `0.65414` via `min-h-screen` sur le placeholder `isAuthLoading`)* | **PASS** |

---

## 5. Inspection Visuelle des `59` Captures `docs/ux-audit/screenshots/after/` & Réserves

Toutes les **`59` captures** de `docs/ux-audit/screenshots/after/` proviennent exclusivement de ce dernier run unifié (`0` PNG résiduel/périmé) :
- Accueil & Hero : `home_320x700_light.png`, `home_390x844_light.png`, `home_390x844_light_full.png`, `home_390x844_dark.png`, `home_430x932_light.png`, `home_430x932_dark.png`, `home_768x1024_light.png`, `home_1024x768_light.png`, `home_1440x900_light.png`, `home_1440x900_light_full.png`, `home_1440x900_dark.png`, `home_1920x1080_light.png`
- Routes publiques : `route_activites_390x844_light.png`, `route_activites_430x932_light.png`, `route_activites_1024x768_light.png`, `route_activites_1440x900_light.png`, `route_decouvrir_390x844_light.png`, `route_decouvrir_430x932_light.png`, `route_decouvrir_1440x900_light.png`, `route_formation_1440x900_light.png`, `route_hebergements_390x844_light.png`, `route_hebergements_1440x900_light.png`, `route_hebergements_1440x900_dark.png`, `route_legal_cgv_390x844_light.png`, `route_mentions-legales_390x844_light.png`, `route_mon_espace_anon_390x844_light.png`, `route_mon_espace_anon_1440x900_light.png`, `route_pack_entreprise_1440x900_light.png`, `route_reserver_step1_390x844_light.png`, `route_reserver_step1_1440x900_light.png`, `route_restaurant_1440x900_light.png`, `route_tarifs_390x844_light.png`, `route_tarifs_1440x900_light.png`, `route_tarifs_1440x900_dark.png`
- Zoom 200%, états interactifs, daltonisme & DEV : `zoom_font200_390x844.png`, `zoom_font200_1440x900.png`, `state_mobile_drawer_320x700.png`, `state_mobile_drawer_390x844.png`, `state_bento_drawer_390x844.png`, `state_bento_drawer_1440x900.png`, `state_booking_step2_390x844.png`, `state_booking_step3_390x844.png`, `state_ecopass_recto_390x844.png`, `state_ecopass_verso_390x844.png`, `state_ecopass_sunlight_1440x900.png`, `state_ecopass_oled_1440x900.png`, `state_sentinel_feed_390x844.png`, `state_sentinel_feed_1440x900.png`, `state_daltonism_deuteranopia_1440x900.png`, `state_color_atlas_dev_1440x900.png`, `state_color_atlas_scales_1440x900.png`, `state_color_atlas_tester_1440x900.png`
- Cockpit `/exploitation` : `cockpit_admin_390x844_light.png`, `cockpit_admin_430x932_light.png`, `cockpit_admin_1440x900_light.png`, `cockpit_admin_1440x900_dark.png`, `cockpit_guichet_1440x900_light.png`, `cockpit_comptable_1440x900_light.png`, `cockpit_modal_closure_1440x900.png`

### Inspection visuelle directe (`read_file`)
- **`home_320x700_light.png`** : bandeau Temps 1, en-tête, ruban chapternav scrollable sans débordement et Hero `"Complexe écologique et loisirs à Yaoundé, Ahala."` propres sans césure ni débordement à `320px`.
- **`zoom_font200_390x844.png` & `zoom_font200_1440x900.png`** : mise en page verticale fluide à `390px` et alignement complet utility bar + navbar + pastilles + Hero/vignettes à `1440px` sans troncature ni chevauchement.
- **`route_decouvrir_390x844_light.png`** : Hero Biodiversité lisible, carte `"Visites Guidées & Écoles"` contrastée, barre de recherche et filtre `"Statut UICN :"` propres à `390px`.
- **`cockpit_modal_closure_1440x900.png`** : modale `Fermeture d Urgence de Sentier` centrée sur fond assombri, anneau de focus net sur le bouton actif à l'intérieur du `role="dialog"`.
- **`cockpit_admin_1440x900_dark.png`** : thème sombre intégral net (barre RBAC, Régulateur de capacité, 4 KPI, Histogramme + Part modale Éco-Mobilité) sans artefact visuel après stabilisation complète (`650ms`) de la View Transition.
- **Contrôles additionnels (`state_ecopass_oled_1440x900.png`, `state_ecopass_verso_390x844.png`, `state_sentinel_feed_390x844.png`, `state_color_atlas_scales_1440x900.png`, `state_daltonism_deuteranopia_1440x900.png`, `state_booking_step2_390x844.png`)** : conformes et sans chevauchement.

### Réserves & limites transparentes
1. **Liens prose inline** : quelques liens `tel:` / `mailto:` insérés dans le flux de paragraphes/listes (`/mentions-legales`, `/confidentialite` mobile) relèvent de l'exception *Inline* de WCAG 2.5.8 (`21-22px` de hauteur de ligne).
2. **Contrôles RBAC désactivés** : `29` boutons sur `guichet` et sur `comptable` sont intentionnellement `disabled` et exemptés de contraste minimum par WCAG 2.2 SC 1.4.3 / 1.4.11.
3. **Éléments restant hors portée Chromium automatisé** : matériel physique iOS Safari / Android Chrome, navigateurs Firefox/WebKit, lecteurs d'écran réels (NVDA, VoiceOver), modes OS `prefers-contrast: more` / `forced-colors: active`, rendu natif OS de la popup `<option>` ouverte et audit tiers `axe-core` *(listés dans [07_WCAG_MANUAL_CHECKLIST.md](./07_WCAG_MANUAL_CHECKLIST.md))*.
