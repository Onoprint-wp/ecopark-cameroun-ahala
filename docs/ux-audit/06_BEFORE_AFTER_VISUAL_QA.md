# 06 - Rapport QA Visuel & Métriques Avant / Après (Phase 3 - Passe Unifiée Finale)

- **Branche** : `audit/typography-accessibility-v3` (sur base `5f43b08` / Phase 1 `e7aaa03` + Lot 1-3 + correctifs finaux ARIA/clavier/`inert`/CLS/SVG/zoom `200%` et re-build final ; aucune fusion vers `feat/react-adobe-color-ahala` ni déploiement)
- **Date de vérification unifiée** : 2026-11-14
- **Environnement mesuré (run unique final post-retouches)** :
  - **Bundle production `dist/` via `vite preview` (`http://127.0.0.1:4179`)** : **`224` contextes** en passe unifiée Playwright Chromium headless (`55` matrice principale `5` routes x `11` viewports + `115` matrice étendue `14` routes publiques x `5` viewports x `2` thèmes hors doublons déjà couverts + `19` contextes zoom `200%` `font-size: 32px` et `zoom: 2` + `32` états interactifs & Cockpit Pro `/exploitation` RBAC/modale + `3` simulations daltonisme).
  - **Atelier Chromatique DEV via `vite dev` (`http://127.0.0.1:5179`)** : **`14` contextes** (`ColorAtlasDrawer` onglets `#pillars`, `#scales` x5 familles Light & Dark, `#tester`, plus test clavier complet entrée/`Tab`/`Shift+Tab`/`Escape`/retour focus).
  - **Total passe unifiée finale** : **`238` contextes DOM**, **`6` suites automatisées de navigation clavier**, **`3` modes daltonisme** (`deuteranopia`, `protanopia`, `tritanopia`), **`4` sondes `<option value="domaine">`** sur `SpeciesAtlas`, **`5` mesures CLS** (`PerformanceObserver layout-shift`), **`8` sondes SVG `<text>`** (`35` nœuds contrôlés Light & Dark sur `/activites`), et **`59` PNG** régénérés dans `docs/ux-audit/screenshots/after/`.
  - **Outillage sans pollution `package.json`** : Playwright Python Chromium headless, moteur JS intégré sRGB/Canvas RGBA pour contraste WCAG 2.1, sans modification de `package.json`, `src/utils/` ni des données métier.
- **Référentiel Phase 1** : [03_TYPOGRAPHY_FINDINGS.md](./03_TYPOGRAPHY_FINDINGS.md), [04_RESPONSIVE_AND_REFLOW_MATRIX.md](./04_RESPONSIVE_AND_REFLOW_MATRIX.md), [05_COMPONENT_REMEDIATION_PLAN.md](./05_COMPONENT_REMEDIATION_PLAN.md), [ECOPARK_TYPOGRAPHY_TOKENS_V3.md](../design/ECOPARK_TYPOGRAPHY_TOKENS_V3.md).

---

## 1. Synthèse Quantitative Avant / Après (Passe Unifiée `238` Contextes)

| Indicateur audité | Baseline Phase 1 (`before`) | Passe Unifiée Finale (`238` contextes, build final) | Statut |
| :--- | :---: | :--- | :---: |
| **Contextes DOM évalués** | `40` routes/états (`211` scans) | **`238` contextes** (`55` matrice 11-vp + `115` routes 14x5 L/D + `19` zoom `200%` + `32` états interactifs/cockpit + `3` daltonisme + `14` `ColorAtlasDrawer` DEV) | **PASS** |
| **Erreurs console / runtime JS** | - | **`0` `consoleErrors` / `0` `pageErrors`** sur `238 / 238` contextes | **PASS** |
| **Contrastes HTML actifs `< AA` (`4.5:1` / `3:1`)** | **588** | **`0 / 238`** (`ColorAtlasDrawer` `#scales` x5 familles L/D & `#tester` inclus ; `--text-muted` mesuré via `wcagContrast.ts` à **`10.29:1`** Light / **`11.71:1`** Dark ; `--on-primary` Dark `#081C15`/`#74C69D` **`8.68:1`**) | **PASS** |
| **Contrastes texte SVG (`InteractiveTopoMap` / `ElevationProfile`)** | non isolé | **`0 / 70` échec** (`35` `<text>` sur `/activites` Light + `35` Dark ; boussole `"N"` dotée d'un halo `#141816` `3px` -> **`17.92:1`** vs `2.47:1` sans halo) | **PASS** |
| **Contrôles RBAC désactivés** | `66` | Exemptés WCAG 2.2 (1.4.3 / 1.4.11 inactifs sur `guichet` / `comptable`) | **Exempté** |
| **Troncatures / clipping HTML (`clippedCount`)** | **858** | **`0 / 238`** | **PASS** |
| **Débordements documentaires racine (`docOverflowPx > 0`)** | `0` | **`0 / 238`** (`documentElement.scrollWidth === vw` de `320px` à `1920px`, `640x400`, zoom `200%` `font200` et `csszoom2`) | **PASS** |
| **Débordements horizontaux boîte HTML (`overflowingCount`)** | **183** | **`0 / 224` hors `<select>` natif à libellé sentier long** *(exception unique mesurée : `CitizenSentinel` `<select>` sur `sentinel_form` `scrollW 872 > clientW 290` à `390px` et `765 > 627` à `1440px`, libellé métier `trail.name` conservé, `docOverflowPx = 0`)* | **PASS (réserve `<select>`)** |
| **Micro-textes `< 12px` (`sub12pxCount`)** | **6 665** / **438** | **`0 / 238`** (`minFont = 12px`, `maxFont = 80px` public / `104px` sous zoom `200%`) | **PASS** |
| **Cockpit `Barlow` ou titres `>= 20px` hors zoom `200%`** | `16px` h1 / `24px` AuthPortal | **`0 / 16`** titres `>= 20px` en taille nominale (`100%`) ; seul le span marque `ECOPARK CAMEROUN` du header global est en `Barlow` (`0` composant métier cockpit en `Barlow`) | **PASS** |
| **Cibles tactiles HTML autonomes `< 44px` (`vw <= 1024px`)** | **2 731** | **`0 / 238`** (`smallTapCount = 0`, dont checkbox Charte `shrink-0` dans `<label> >= 44px`) | **PASS** |
| **Tests unitaires / E2E (`npm test`)** | `32/32` | **`37/37` sous-tests (`10` blocs `node:test`, `0` échec)** sans altération des tests | **PASS** |
| **TypeScript & build (`tsc` / `vite build`)** | `0` | **`0` erreur** (`npx tsc -p tsconfig.app.json --noEmit` et `tsc -b && vite build`) | **PASS** |
| **Loi 1 (`U+2013` / `U+2014`)** | `0` | **`0`** dans `index.html`, `tailwind.config.js`, `src/`, `styles/`, `tokens/`, `docs/ux-audit/06..08` | **PASS** |

---

## 2. Ventilation Exacte des `238` Contextes de la Passe Finale

1. **`matrix_11_viewports` (`55` contextes)** : `5` routes clés (`/`, `/activites`, `/decouvrir`, `/reserver`, `/tarifs`) x `11` viewports (`320x700`, `360x800`, `390x844`, `430x932`, `640x400`, `768x1024`, `1024x768`, `1280x800`, `1366x768`, `1440x900`, `1920x1080`) en Light (`fontRange [12px .. 80px]`, **`0` défaut**).
2. **`routes_14_light_dark` (`115` contextes)** : `14` routes publiques (`/`, `/hebergements`, `/restaurant`, `/tarifs`, `/pack-entreprise`, `/formation`, `/activites`, `/decouvrir`, `/reserver`, `/mon-espace`, `/connexion`, `/mentions-legales`, `/cgv`, `/confidentialite`) x `5` viewports (`320x700`, `390x844`, `430x932`, `768x1024`, `1440x900`) x `2` thèmes Light/Dark, hors `25` doublons déjà couverts au point 1 (`fontRange [12px .. 74.88px]`, **`0` défaut**).
3. **`zoom_200_and_reflow` (`19` contextes)** : `/`, `/decouvrir`, `/reserver`, `/tarifs`, `/activites` et `/exploitation` (`admin`) à `390x844` et `1440x900` sous `html { font-size: 32px }` (`font200`) et `html { zoom: 2 }` (`csszoom2`) (`fontRange [12px .. 104px]`, **`0` `docOverflowPx`**, **`0` `lowContrast`**, **`0` `clipped`**, **`0` `overflowing`** ; sous `font200` les titres cockpit s'agrandissent proportionnellement de `16-19px` à `32-38px`).
4. **`interactive_states` (`32` contextes)** :
   - Public / client : `mobile_drawer` (`320x700`, `390x844`), `bento_drawer` (`390x844`, `1440x900`), `booking_step2_errors` (`390x844`), `booking_step3` (`390x844`), `ecopass_recto` (`390x844`, `1440x900`), `ecopass_verso` (`390x844`, `1440x900`), `ecopass_sunlight` (`1440x900`), `ecopass_oled` (`1440x900`), `sentinel_form` (`390x844`, `1440x900`), `sentinel_feed` (`390x844`, `1440x900`).
   - Cockpit `/exploitation` (`16` contextes) : `cockpit_unauth` (`390x844`, `1440x900`), `cockpit_403` (`1440x900`), `cockpit_admin` (`320x700`, `390x844`, `430x932`, `1280x800`, `1440x900` en Light & Dark), `cockpit_modal_closure` (`1440x900`), `cockpit_guichet` (`1440x900`), `cockpit_comptable` (`1440x900`).
5. **`daltonism_modes` (`3` contextes)** : `deuteranopia`, `protanopia`, `tritanopia` (`1440x900`, `0` défaut).
6. **`color_atlas_dev` (`14` contextes DEV sur `vite dev` `5179`)** : `#pillars`, `#scales` (`forest`, `leaf`, `earth`, `mist`, `bark`) et `#tester` en **Light** & **Dark** (`2 x 7 = 14`, **`0` défaut**).

---

## 3. Mesure Réelle du `<select>` UICN `SpeciesAtlas` (`option[value="domaine"]`)

Libellé métier intact : `"Élevage, Bassins & Flore (LC / NT)"` (aucun raccourcissement). Ajustements appliqués : conteneur filtres `p-2.5 sm:p-5`, wrapper `relative min-w-0 max-w-full basis-[210px] grow w-full sm:w-auto sm:min-w-[260px] sm:flex-initial`, et `<select>` `appearance-none pl-[8px] pr-[22px] sm:pl-2.5 sm:pr-7` avec chevron `aria-hidden="true"`.

Mesures Playwright exactes relevées sur le build final (`vite preview`, Canvas `measuredTextW` vs `innerTextBoxW = selectClientW - padL - padR`) :

| Contexte (`/decouvrir`) | `fontSize` | `selectRectW` (`px`) | `clientW / scrollW` (`px`) | Padding L / R (`px`) | `innerTextBoxW` (`px`) | `measuredTextW` (`px`) | `textDeltaPx` (`measured - inner`) | `docOverflowPx` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `320x700` | `16px` | `253.19` | `251 / 251` | `8 / 22` | `221` | `219.45` | **`-1.55 px`** *(tient entier, `1.55px` libres)* | `0` |
| `390x844` | `16px` | `320.39` | `318 / 318` | `8 / 22` | `288` | `219.45` | **`-68.55 px`** *(tient entier, `68.55px` libres)* | `0` |
| `1440x900` | `14px` | `260.00` | `258 / 258` | `10 / 28` | `220` | `192.02` | **`-27.98 px`** *(tient entier, `27.98px` libres)* | `0` |
| `390x844` zoom `200%` (`32px`) | `32px` | `300.39` | `298 / 447` | `8 / 22` | `268` | `438.89` | **`+170.89 px`** *(contrainte native `<select>` mono-ligne à `32px` sur écran `390px`)* | `0` |

> **Constats factuels** : à `320x700`, `390x844` et `1440x900`, l'intitulé complet `"Élevage, Bassins & Flore (LC / NT)"` tient intégralement dans `<select>` sans troncature ni débordement (`scrollW === clientW`, marge libre `1.55px` à `68.55px`). Sous zoom texte `200%` (`32px`) à `390x844`, ce libellé métier de `34` caractères atteint `438.89px` sur une ligne (plus large que le viewport `390px`) ; un `<select>` HTML natif ne pouvant pas passer à la ligne, le texte fermé déborde en interne (`scrollW 447 > clientW 298`) sans jamais provoquer de débordement carte ni page (`docOverflowPx = 0`). Constat similaire relevé sur `CitizenSentinel` pour le nom officiel `"Circuit Jardin Zoologique & Sanctuaire du Gorille « ToTo »"` (`scrollW 872 > clientW 290` à `390px`, `765 > 627` à `1440px`, `docOverflowPx = 0`).

---

## 4. Tests Complémentaires Automatisables : Daltonisme, Clavier & CLS

### 4.1. Modes Daltonisme (`Navbar` -> `ThemeContext`)

| Mode activé | Attribut `data-vision` | `getComputedStyle(html).filter` actif | `docOverflowPx` | `lowContrastCount` | `consoleErrors` | Capture archivée |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `deuteranopia` | `deuteranopia` | `true` (`#filter-deuteranopia`) | `0` | **`0`** | `0` | `state_daltonism_deuteranopia_1440x900.png` |
| `protanopia` | `protanopia` | `true` (`#filter-protanopia`) | `0` | **`0`** | `0` | *(contrôlé DOM/CSS)* |
| `tritanopia` | `tritanopia` | `true` (`#filter-tritanopia`) | `0` | **`0`** | `0` | *(contrôlé DOM/CSS)* |

### 4.2. Navigation Clavier Automatisée (`6 / 6` Suites PASS)

| Suite testée en Playwright | Assertions exécutées et vérifiées | Résultat |
| :--- | :--- | :---: |
| `ahala_showcase_tabs` (`/`) | Flèches clavier sur `role="tablist"` : `showcase-tab-hebergements` -> `ArrowRight` -> `showcase-tab-saveurs` -> `End` -> `showcase-tab-formation` -> `Home` -> `showcase-tab-hebergements` -> `ArrowLeft` (wrap) -> `showcase-tab-formation` | **PASS** |
| `navbar_daltonism_escape` (`1440x900`) | Ouverture menu daltonisme (`aria-expanded="true"`), `Escape` ferme (`aria-expanded="false"`) et restaure le focus sur `"Sélecteur d'accessibilité daltonisme"` | **PASS** |
| `navbar_mobile_drawer_escape` (`390x844`) | Ouverture `#mobile-nav-drawer` (`open_visible=true`), `Escape` ferme (`closed_count=0`) et restaure le focus sur le déclencheur (`aria-controls="mobile-nav-drawer"`) | **PASS** |
| `ecopass_inert_and_flip` (`/mon-espace`) | État vide initial (`empty_visible=true`), puis après chargement pass `ECP-2026-8942` : `rectoInert=false` / `versoInert=true` (`aria-hidden="true"`), `12` pressions `Tab` -> `leaked_to_verso=false`, bascule `Enter` -> focus dans Verso (`activeInVerso=true`, `rectoInert=true`, `versoInert=false`), `12` pressions `Tab` -> `leaked_to_recto=false`, retour Recto -> `activeInRecto=true` | **PASS** |
| `ranger_modals` (`/exploitation`) | **M1 (Fermeture)** : `role="dialog"`/`aria-labelledby`, focus dans modale, `textarea#closure-reason-input` lié à `1` `<label>`, piège `Tab`, `Escape` ferme + focus rendu au bouton `"Fermer"`. **M2 (Résolution)** : `textarea#intervention-note-input` lié à `1` `<label>`, `Escape` restaure déclencheur, confirmation déplace proprement le focus vers `<h2>` `"File de Modération des Signalements Sentinelle"` (jamais `BODY`). **M3 (Reset DEV `5179`)** : dialogue ouvert, focus interne, `Escape` ferme + focus rendu au bouton `Reset` | **PASS** |
| `color_atlas_drawer` (`vite dev` `5179`) | `Enter` sur `"Ouvrir l'Atelier Chromatique"` entre dans `[role="dialog"]` (`focus_entered=true`), `18` `Tab` + `Shift+Tab` piégés (`trap_ok=true`, `shift_trap_ok=true`), `Escape` en phase capture ferme le tiroir sans collision avec `Navbar` et restaure le focus sur le bouton d'atelier | **PASS** |

### 4.3. Mesure CLS (`PerformanceObserver` `layout-shift` sans entrée utilisateur, `1440x900`)

| Route mesurée | CLS mesuré (build final) | Seuil Google CWV ("Bon" `<= 0.10`) |
| :--- | :---: | :---: |
| `/` | **`0.05446`** | **PASS** |
| `/activites` | **`0.00582`** | **PASS** |
| `/decouvrir` | **`0.00720`** | **PASS** |
| `/reserver` | **`0.00467`** | **PASS** |
| `/exploitation` | **`0.00034`** *(corrigé depuis `0.25775` via `key` distincts + `min-h-screen` sur toutes les branches `isAuthLoading` / `!isAuthenticated` / `!isStaff` dans `App.tsx`)* | **PASS** |

---

## 5. Inspection Visuelle des Captures `docs/ux-audit/screenshots/after/` & Réserves

Toutes les **`59` captures** de `docs/ux-audit/screenshots/after/` ont été régénérées lors de ce dernier run unifié sur le build final (`dist/` + `vite dev`) :
- Accueil & Hero (`12`) : `home_320x700_light.png`, `home_390x844_light.png`, `home_390x844_light_full.png`, `home_390x844_dark.png`, `home_430x932_light.png`, `home_430x932_dark.png`, `home_768x1024_light.png`, `home_1024x768_light.png`, `home_1440x900_light.png`, `home_1440x900_light_full.png`, `home_1440x900_dark.png`, `home_1920x1080_light.png`
- Routes publiques (`22`) : `route_activites_390x844_light.png`, `route_activites_430x932_light.png`, `route_activites_1024x768_light.png`, `route_activites_1440x900_light.png`, `route_decouvrir_390x844_light.png`, `route_decouvrir_430x932_light.png`, `route_decouvrir_1440x900_light.png`, `route_formation_1440x900_light.png`, `route_hebergements_390x844_light.png`, `route_hebergements_1440x900_light.png`, `route_hebergements_1440x900_dark.png`, `route_legal_cgv_390x844_light.png`, `route_mentions-legales_390x844_light.png`, `route_mon_espace_anon_390x844_light.png`, `route_mon_espace_anon_1440x900_light.png`, `route_pack_entreprise_1440x900_light.png`, `route_reserver_step1_390x844_light.png`, `route_reserver_step1_1440x900_light.png`, `route_restaurant_1440x900_light.png`, `route_tarifs_390x844_light.png`, `route_tarifs_1440x900_light.png`, `route_tarifs_1440x900_dark.png`
- Zoom `200%`, états interactifs, daltonisme & DEV (`18`) : `zoom_font200_390x844.png`, `zoom_font200_1440x900.png`, `state_mobile_drawer_320x700.png`, `state_mobile_drawer_390x844.png`, `state_bento_drawer_390x844.png`, `state_bento_drawer_1440x900.png`, `state_booking_step2_390x844.png`, `state_booking_step3_390x844.png`, `state_ecopass_recto_390x844.png`, `state_ecopass_verso_390x844.png`, `state_ecopass_sunlight_1440x900.png`, `state_ecopass_oled_1440x900.png`, `state_sentinel_feed_390x844.png`, `state_sentinel_feed_1440x900.png`, `state_daltonism_deuteranopia_1440x900.png`, `state_color_atlas_dev_1440x900.png`, `state_color_atlas_scales_1440x900.png`, `state_color_atlas_tester_1440x900.png`
- Cockpit `/exploitation` (`7`) : `cockpit_admin_390x844_light.png`, `cockpit_admin_430x932_light.png`, `cockpit_admin_1440x900_light.png`, `cockpit_admin_1440x900_dark.png`, `cockpit_guichet_1440x900_light.png`, `cockpit_comptable_1440x900_light.png`, `cockpit_modal_closure_1440x900.png`

### Inspection visuelle directe (`read_file`)
- **`home_320x700_light.png`** : bandeau Temps 1, en-tête `ECOPARK CAMEROUN` lisible (les boutons Compte & Menu passent proprement en seconde rangée `>= 48px` sans tronquer la marque), ruban chapternav scrollable et Hero nets à `320px`.
- **`zoom_font200_390x844.png` & `zoom_font200_1440x900.png`** : suite au retrait de `flex-1` / `overflow-x-clip` sur le bouton marque dans `Navbar.tsx`, `"ECOPARK CAMEROUN"` reste entièrement lisible à `390x844` sous `font-size: 32px` sans troncature sur le bord droit ; à `1440x900`, alignement complet de la barre, des pastilles et du Hero.
- **`route_decouvrir_390x844_light.png`** : Hero Biodiversité lisible, carte `"Visites Guidées & Écoles"` contrastée, barre de recherche et filtre `"Statut UICN :"` propres sans chevauchement à `390px`.
- **`route_activites_390x844_light.png`** : barre `Calques` en `flex-wrap`, contrôles zoom `>= 44px` et carte topographique parfaitement contenue à `390px`.
- **`cockpit_modal_closure_1440x900.png`** : modale `Fermeture d Urgence de Sentier` centrée sur fond assombri, notice lisible en `14px` et bouton sélectionné avec bordure nette à l'intérieur du `role="dialog"`.
- **`cockpit_admin_1440x900_dark.png`** : thème sombre intégral net (barre RBAC, Régulateur de capacité, `4` KPI, Histogramme et Part modale Éco-Mobilité) sans artefact visuel.
- **`state_color_atlas_scales_1440x900.png`** : les `11` échelons `50..950` de l'échelle `Forest` en DEV s'affichent avec un contraste texte conforme (`>= 4.5:1`).

### Réserves & limites transparentes
1. **Libellés longs dans `<select>` natif** : en HTML natif mono-ligne, `"Élevage, Bassins & Flore (LC / NT)"` sous `font-size: 32px` à `390x844` (`scrollW 447 > clientW 298`) et `"Circuit Jardin Zoologique & Sanctuaire du Gorille « ToTo »"` dans `CitizenSentinel` (`scrollW 872 > clientW 290` à `390px` ; `765 > 627` à `1440px`) dépassent la largeur intérieure du `<select>` fermé sans créer de débordement documentaire (`docOverflowPx = 0`).
2. **Paragraphes secondaires compacts `12px`** : certains avis/descriptions de fiches courtes (notices `BookingWizard`, descriptions `text-xs sm:text-sm` des signalements `RangerDashboard` sous `640px`, notice `2e` face `DigitalEcoPass`) restent à `12px` (`>=` plancher `12px`) tandis que les paragraphes éditoriaux principaux utilisent `.type-body` (`16-17px`) ou `.type-body-compact` (`>= 14px`).
3. **Contrôles RBAC désactivés & liens inline** : boutons désactivés `guichet`/`comptable` exemptés par WCAG 2.2 (1.4.3 / 1.4.11) ; liens `tel:`/`mailto:` dans le flux de paragraphes soumis à l'exception *Inline* de WCAG 2.5.8.
4. **Éléments restant non testés en Chromium headless** : matériel physique iOS Safari / Android Chrome, navigateurs Firefox Gecko et Safari WebKit, lecteurs d'écran réels (NVDA, JAWS, VoiceOver), modes OS `prefers-contrast: more` et `forced-colors: active`, popup `<option>` native OS ouverte et audit tiers `axe-core` *(détail dans [07_WCAG_MANUAL_CHECKLIST.md](./07_WCAG_MANUAL_CHECKLIST.md))*.
