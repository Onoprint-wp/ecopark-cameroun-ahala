# 03 — Synthèse Diagnostique Typographique, Contrastes & Accessibilité (Audit Playwright + Statique)

- **Branche** : `audit/typography-accessibility-v3` (`6157dd7` / parent `0f677f8`, bundle compilé `vite preview` + vérification DEV ciblée `ColorAtlasDrawer`)
- **Date d'audit** : 2026-11-14
- **Sources de preuves** :
  - Inventaire mesuré : [02_TYPOGRAPHY_INVENTORY.csv](./02_TYPOGRAPHY_INVENTORY.csv) (**47 640 lignes** dédupliquées par scan sur **40 routes/états**, **211 scans** `route × viewport`, généré par Playwright Chromium headless avec résolution CSS Color 4 sur canvas 2px et transitions désactivées en régime permanent)
  - Matrice responsive/zoom : [04_RESPONSIVE_AND_REFLOW_MATRIX.md](./04_RESPONSIVE_AND_REFLOW_MATRIX.md)
  - Captures visuelles avant correction : `docs/ux-audit/screenshots/before/` (**54 PNG**, inspectées sur vues critiques Light, Dark, Zoom 200%, Modales, RBAC et États)
  - Lecture statique & moteur WCAG : `src/index.css` (1–1013), `src/utils/wcagContrast.ts`, `src/utils/ecosystemE2E.test.ts` et composants TSX

---

## 1. Synthèse Quantitative & Niveau de Criticité

| Indicateur (`02_TYPOGRAPHY_INVENTORY.csv`) | Valeur mesurée | Répartition / Précision |
| :--- | :---: | :--- |
| **Total d'observations CSV (`40` routes/états)** | **47 640** | 14 routes publiques + `/exploitation` Light & Dark (`5 à 10` viewports, couvrant les **9 viewports obligatoires** dont `430x932` + `1280x800`), 5 onglets Showcase actifs, `/exploitation` (`unauth`, `admin`, `agent_guichet`, `comptable`, `client_403`, modale fermeture), états interactifs complets et 7 scénarios zoom 200%/reflow |
| **Anomalies `P0` (bloquantes / contrastes < AA / coupures vitales / débordements)** | **1 627** | `855` Light / `772` Dark : **587** contrastes WCAG `< AA` + **858** troncatures critiques (`395` `line-clamp-2`, `390` `ellipsis`, `64` `line-clamp-3`, `8` `line-clamp-1`, `1` `ancestor-clip:+113px`) + **183** débordements hors boîte/viewport (`127` `parent-out`, `56` `vp-right` ; 1 nœud combiné) |
| **Anomalies `P0` par composant** | **1 627** | `AppShell (Accueil)` : `511`, `RangerDashboard` : `380`, `Navbar` : `190`, `TrailCatalog` : `158`, `SpeciesAtlas` : `150`, `HeroCanopy` : `91`, `AhalaShowcase` : `46`, `BookingWizard` : `32`, `Footer` : `23`, `DigitalEcoPass` : `18`, `LegalNoticeView` : `15`, `AuthPortal` : `9`, `ColorAtlasDrawer` (`dev`) : `4` |
| **Anomalies `P1` (paliers taille, cibles < 44px, zoom 200%)** | **16 107** | **6 665** micro-textes publics `< 12px`, **5 140** corps `< 16px`, **2 733** cibles tactiles `< 44px`, **711** liens nav `< 14px`, **452** occurrences zoom 200% (`fixed-px`/`zoom-clip`), **438** micro-textes cockpit `< 11px`, **368** troncatures non-P0 *(multi-critères possibles par nœud)* |
| **Anomalies `P2` (tracking/interlignage, micro-notes, RBAC désactivé)** | **12 008** | Tracking corps `-0.022em` (`-0.374px`), footnotes/labels `< 13px`, plus `60` observations de contrôles RBAC désactivés (`30` par rôle sur `agent_guichet` & `comptable`, `opacity-50`/`pointer-events-none`, exemptés WCAG 1.4.3) |
| **Observations `OK`** | **17 898** | Conformes à leur rôle et contexte mesuré |
| **Exclusions automatisées** | **231 + 35** | **231** nœuds sur fond dégradé ou photo (`N/A (gradient/photo)`) + **35** nœuds `<text>` SVG internes max (hors ratio DOM HTML ; mesurés statiquement à `9px`–`10px`) |

---

## 2. Vérification des Polices Web (`document.fonts`) & Cascade CSS

**Chargement effectif des 3 familles Google Fonts (Mesuré)** :
Sur `vite preview`, `Array.from(document.fonts)` recense **75 instances `FontFace`**, dont **10 chargées (`status === "loaded"`)** :
- **`Barlow Semi Condensed`** : graisses `600` (`normal`), `700` (`normal`) chargées (`800` et `italic` restent `unloaded`).
- **`Source Sans 3`** : graisses `400`, `500`, `600`, `700` chargées.
- **`JetBrains Mono`** : graisses `400`, `500`, `600` chargées.

**Défaillance de cascade détectée sur `.font-mono` (Mesuré sur `/hebergements` & `/`)** :
Bien que `JetBrains Mono` soit chargée, les fourchettes tarifaires `.type-footnote.font-mono` (ex. `10 000 à 15 000 FCFA` sur `/hebergements` en `1440x900` Light et Dark) rendent en **`"Source Sans 3"` (`12px`)** au lieu de `JetBrains Mono` !
- **Cause racine (`src/index.css:374-572`)** : `.type-*` et `.cta-*` sont déclarées **hors de tout `@layer`** (`@layer components`). En Tailwind CSS v4, une règle non-layered écrase `@layer utilities` où vit `.font-mono` (et explique le recours aux **38 `!important`** dans les TSX).
- **Anomalie connexe (`TrailCatalog.tsx:375`)** : les sous-titres de sentiers utilisent `italic font-serif text-xs` (`12px`), où `--font-serif` pointe vers `'Barlow Semi Condensed'` (police display sans italique dédié chargé, utilisée sous le seuil `< 20px`).

---

## 3. Constats `P0` — Bloquants Accessibilité, Contrastes, Troncatures & Débordements

### P0-1 — Rupture du Mode Sombre Tailwind (`dark:*` inactif lorsque l'OS préfère Light) [Mesuré]
- **Preuves mesurées** :
  - `/decouvrir` (`dark`) : alerte `Respecter la distance de sécurité...` / `Consigne de quiétude éco-garde` = **`1.40:1`** (`bg-emerald-50/80` resté clair sous texte `#E9F5ED`).
  - `/activites` (`dark`) : badge `1 obs. terrain` = **`1.68:1`**, `Avis Éco-Garde` = **`1.87:1`–`2.64:1`**.
  - `/exploitation (admin)` (`dark`, capture [cockpit_admin_1440x900_dark.png](./screenshots/before/cockpit_admin_1440x900_dark.png)) : cartes sentiers fermées/balisées (`Pôle Hôtelier 24h/24...`) = **`1.12:1`**, `Très Bon` / KPIs = **`1.78:1`–`2.52:1`**, `Heure actuelle` = **`2.69:1`**, `ADMINISTRATEUR PLATEFORME` = **`3.13:1`**.
- **Cause racine (`src/index.css:1`)** : Tailwind v4 (`@import "tailwindcss";`) n'a pas de `@custom-variant dark (&:where(.dark, .dark *, [data-theme="dark"], [data-theme="dark"] *));` (`tailwind.config.js` n'est pas lu). Les variables CSS `[data-theme="dark"]` basculent, mais aucune classe utilitaire `dark:bg-*` / `dark:text-*` ne s'active.

### P0-2 — `text-white` codé en dur sur `bg-[var(--brand-primary)]` en Mode Sombre (`2.47:1`) [Mesuré]
- **Preuves mesurées (`2.47:1` < `4.5:1`)** : onglets actifs (`/activites`, `/decouvrir`, `/mentions-legales`, `/cgv`, `/confidentialite`), pastille étape `1` et CTA (`/reserver`), boutons `Réserver un Pass QR` (`/mon-espace`), `Se connecter à mon Espace Cliente` (`/connexion`), et bouton palier `1500 places` (`/exploitation` admin Dark).
- **Cause racine** : en Dark (`src/index.css:153-155`), `--brand-primary` vaut `#52B788` (vert clair prévu pour `--on-primary: #121614`), mais ces éléments forcent `text-white`.

### P0-3 — Contrastes insuffisants en Mode Clair (`emerald-600`, `amber-600/700`, `red-600`, Atelier DEV) [Mesuré]
- `/reserver` (Étape 1 & Étape 3, Light) : `858 places disponibles`, `-0 FCFA`, `+8,4 kg CO₂` (`text-emerald-600` sur `#E9F5ED`) = **`3.26:1`** ; checkbox `on` Étape 3 = **`3.49:1`**.
- `/reserver` (Étape 2 erreurs validation, Light) : `Le nom du visiteur...`, `Une adresse email valide...`, `Veuillez saisir votre numéro...` (`text-red-600`) = **`4.26:1`**.
- `/mon-espace` (Pass déverrouillé, Confirmation, `Plein Soleil` & `OLED` Light) : `+8,4 kg CO₂` (`text-emerald-600` sur `--bg-elevated`) = **`3.65:1`** (en mode `OLED`, le conteneur externe passe en `bg-black`, mais les tuiles internes `bg-[var(--bg-elevated)]` restent blanches hors thème sombre global : voir [state_ecopass_oled_1440x900.png](./screenshots/before/state_ecopass_oled_1440x900.png)).
- `/decouvrir` (Light) : `Jardin Zoologique, Bassins Piscicoles & Flore Tropicale` = **`3.60:1`**.
- `/activites` (Light) : `Avis Éco-Garde :` = **`4.16:1`**.
- `/connexion#staff`, `/exploitation#unauth`, `/exploitation#403-client`, `/exploitation` (`admin`, `agent_guichet`, `comptable`, Light) :
  - `text-amber-700` sur `#E9F5ED` (`ADMINISTRATEUR PLATEFORME`, `Agent Guichet RN3`, `Comptable SYSCOHADA`, `Cockpit Pro`, `Accès Réservé...`) = **`4.49:1`** (< `4.50:1`),
  - `Balisé` / `Ouvrir le Cockpit Pro` (`bg-amber-600 text-white`) = **`3.20:1`**, `Fluide` / `Check-In` (`bg-emerald-600 text-white`) = **`3.65:1`**, `Résoudre & Commenter` = **`4.02:1`**, `Annuler` = **`4.26:1`**, `Fermé / Protection` = **`2.70–2.89:1`**.
- `ColorAtlasDrawer` (`vite dev`, onglet `#scales`) : **`4` P0** (`600` = `3.04:1`, `#40916C` = `3.83:1`, `Lum: 22%` = `2.87:1`, `Lum: 11%` = `4.40:1`).

### P0-4 — Troncatures critiques d'informations tarifaires, identitaires & opérationnelles [Mesuré]
- **Temps 1 (`Navbar.tsx:248`)** : `• Garantie Météo RN3 (report gratuit 90j)...` coupé avec `ellipsis:+418px` à `320x700`, `+351px` à `390x844` et **`+312px` à `430x932`** sur toutes les routes publiques (`320–430px`).
- **Marque `ECOPARK CAMEROUN` & `POSTE EXPLOITATION RN3` (`Navbar.tsx:304,307`)** :
  - Coupés à `320x700` (`ellipsis:+12px` et `+33px`, capture [home_320x700_light.png](./screenshots/before/home_320x700_light.png)).
  - **Coupés même en Desktop `1280px`–`1440px` sur `/exploitation` (Admin)** : `ellipsis:+107px` / `+76px` à `1366x768`, **`ellipsis:+39px` / `+8px` à `1440x900`** (prouvé visuellement dans [cockpit_admin_1440x900_dark.png](./screenshots/before/cockpit_admin_1440x900_dark.png) et [cockpit_modal_closure_1440x900.png](./screenshots/before/cockpit_modal_closure_1440x900.png)), car tous les items `<nav>` et badges de droite portent `shrink-0`.
- **Collage Hero (`HeroCanopy.tsx:186,199,212`)** : `Pirogue · 500 FCFA enf.` et `Hôtels dès 10 000 FCFA` coupés (`ellipsis:+21px` à `390px`, `+8px` à `430x932`, `+12px` à `1024px`).
- **Pôles & Sentiers (`App.tsx:173,179`, `AhalaShowcase.tsx:601`)** : `Jardin Zoologique & Canopée d Ahala...` (`ellipsis:+39px` à `430x932`) et `Pôle Hôtelier 24h/24 & Complexe Évé...` coupés jusqu'à `1366–1440px`, `line-clamp-2`/`3` sur descriptions sentiers (`395` + `64` P0), `line-clamp-1` sur la file check-in (`8` P0), `truncate` sur `hotel.priceRange` (`10 000 à 15 000 FCFA` coupé sous zoom 200%).

### P0-5 — Débordements horizontaux hors boîte conteneur (`parent-out` / `vp-right`) [Mesuré]
- **`SpeciesAtlas.tsx` (`/decouvrir`)** : `<select>` (`Tous statuts (8)`) déborde de **`vp-right:+156px;parent-out:+199px;form-out:+140px`** à `320x700`, **`+116px/+161px`** à `360x800`, **`+87px/+132px`** à `390x844` (capture [route_decouvrir_390x844_light.png](./screenshots/before/route_decouvrir_390x844_light.png)) et **`+48px/+93px`** à `430x932` (capture [route_decouvrir_430x932_light.png](./screenshots/before/route_decouvrir_430x932_light.png)), provoqué par la cohabitation du garde-fou iOS `16px` (`src/index.css:338`) sans `min-w-0 max-w-full flex-wrap`.
- **`RangerDashboard.tsx` (`/exploitation`)** : `<select>` (`Tous les sentiers`) déborde de **`vp-right:+271px;parent-out:+293px`** à `320x700`, **`+232px/+255px`** à `360x800`, **`+202px/+226px`** à `390x844` et **`+163px`** à `430x932`.
- **`TrailCatalog.tsx` & `InteractiveTopoMap.tsx` (`/activites`)** : barre `Calques` (`Sentiers`, `POIs`) et pilules de filtres débordent à **`320x700`** (jusqu'à `vp-right:+112px;parent-out:+148px` sur `POIs`), **`360x800`** (`+73px/+109px`), **`390x844`** (`+44px/+81px`, capture [route_activites_390x844_light.png](./screenshots/before/route_activites_390x844_light.png)), **`430x932`** (`+5px/+42px` sur `POIs`, `+4px` sur `Sportif`, capture [route_activites_430x932_light.png](./screenshots/before/route_activites_430x932_light.png)), et légèrement en boîte interne à `768px` (`+14px`), `1024px` (`+24px`) et `1280px` (`+5px`).
- **`Footer.tsx` (`1024x768`)** : `24h/24 · 7j/7` déborde de sa colonne (`parent-out:+32px`).
- **`Navbar.tsx` (`/exploitation`, `1280x800`)** : badge `Administration` déborde (`parent-out:+7px`).

---

## 4. Constats `P1` & `P2` — Corps Mobile, Micro-Textes, Zoom 200%, Hiérarchie & Tactile

1. **Corps de texte `< 16px` & `!important` (`P1`)** : `.type-body` vaut **`15px / 22px`** sur mobile (`5 140` P1) avec tracking serré **`-0.022em` (`-0.374px`)** sur desktop (`P2`) et interlignage `1.47`. **38 `!text`/`!leading`** (`AhalaShowcase`: 23, `ImpactBanner`: 6, `HeroCanopy`: 5, `App`: 3, `DigitalEcoPass`: 1) abaissent des paragraphes à **`12px` mobile / `14px` desktop**. `LegalNoticeView` (`/mentions-legales`, `/cgv`, `/confidentialite`) rend tout son corps juridique à **`12px / 16px`**.
2. **Navigation `.type-nav` (`12px`) & `.type-chapternav` (`11px–12px`)** : `711` P1 sous le seuil `14px`.
3. **Micro-textes `9px–11px`** : **210 classes** `text-[Npx]` (`9px`: 11, `10px`: 65, `11px`: 117) et **383 `text-xs`** dans `18` fichiers `.tsx` -> `6 665` P1 publiques `< 12px` + `438` P1 cockpit `< 11px` + `83` sous-12px dans `ColorAtlasDrawer`. Sur `InteractiveTopoMap` (`viewBox="0 0 1000 700"`), les libellés SVG `9–10` unités tombent vers ~`3.5 CSS px` physiques sur mobile `390px`.
4. **Zoom 200% (`html { font-size: 32px }`)** :
   - Sur `/_390x844_font200` (capture [zoom_font200_390x844.png](./screenshots/before/zoom_font200_390x844.png)), **`53` nœuds** (`13` composants/rôles distincts en `px` fixes) restent figés, et `.type-hero` (`96px`) atteint `scrollWidth: 423px > clientWidth: 310px` -> **`ancestor-clip:+113px`** dans `ImmersiveSection` (`overflow-hidden`), tandis que la marque se réduit à `"E."` / `"YA..."`.
   - Sur `/exploitation_1440x900_font200`, **`339` nœuds** en `px` Tailwind/arbitraires ne doublent pas.
5. **Hiérarchie des `<h1>`** : 5 traitements publics disparates (`48–80px`, `.type-h2`, `30–48px`, `24–36px`), et sur `/exploitation` (`RangerDashboard.tsx:476`, `App.tsx:441,465`) un **`<h1>` à `16px`** identique aux `<h2>` et `<h3>` (`16px`).
6. **Cibles tactiles `< 44px`** : **`2 733`** occurrences P1 sur viewports `<= 1024px` (contrôles zoom carte `26px`, filtres `TrailCatalog`, steppers `w-8 h-8` `32px` de `BookingWizard`, boutons `DigitalEcoPass` et actions tableau `RangerDashboard`).
7. **Routage `/atelier-couleurs` & Accès `CitizenSentinel`** :
   - Contrairement à l'hypothèse statique initiale, la visite réelle de `/atelier-couleurs` sur `vite preview` prouve qu'**aucune route `/atelier-couleurs` n'existe** (`hasHero: true`, `hasAtelierBtn: false`, `hasDrawerDialog: false` -> fallback `'accueil'`). `ColorAtlasDrawer` ne s'ouvre que via `"Atelier"` en mode `DEV` (`181` nœuds mesurés sur `vite dev`).
   - `CitizenSentinel` (`App.tsx:408-415`) ne se monte que pour un utilisateur authentifié (`form` : `132` nœuds / `0` P0 ; `feed` : `178` nœuds / `0` P0).

---

## 5. Statut Épistémique Exhaustif (Mesuré vs Observé Statiquement vs Non Testé)

| Catégorie | Périmètre vérifié | Statut |
| :--- | :--- | :--- |
| **Fontes & cascade CSS** | `document.fonts` (`10/75` faces chargées), `.type-footnote.font-mono` en `Source Sans 3` | **Mesuré (Chromium Playwright)** |
| **14 routes Light/Dark, 10 VPs (`9 obligatoires + 1280x800`), Zoom 200%, 40 états** | `47 640` lignes CSV (`40` routes/états, `211` scans), tous onglets Showcase (`panel-hebergements`, `panel-saveurs`, `panel-tarifs`, `panel-entreprise`, `panel-formation`), `LegalNoticeView`, `BookingWizard` étapes 1–3 & confirm, `DigitalEcoPass` (`recto`, `verso`, `sunlight`, `oled`), `Daltonism` (`#filter-deuteranopia`), `MobileDrawer`, `AuthPortal` (4 modes), `CitizenSentinel` (`form`/`feed`), `ColorAtlasDrawer` (`dev` 3 onglets), `/exploitation` (`unauth`, `client_403`, `admin`, `agent_guichet`, `comptable`, modale fermeture) | **Mesuré (Chromium Playwright)** |
| **Ratios Dalto & `--text-muted`** | Contraste Light/Dark + simulation matricielle daltonisme | **Calculé via `src/utils/wcagContrast.ts`** |
| **Causes racines CSS/JSX & E2E** | `@custom-variant dark` absent, `@layer` absent, `shrink-0`, `<select>` sans `min-w-0`, assertions `ecosystemE2E.test.ts` | **Observé statiquement & corrélé aux mesures** |
| **Dégradés, photos & SVG internes** | `231` nœuds `gradient/photo` (Hero, `Pack VIP`, photos Bento) et `35` `<text>` SVG max | **Inspecté visuellement (`before/*.png`) / exclu du ratio auto** |
| **Environnements & outils non exécutés** | **iOS Safari physique** (`max(1rem, 16px)` matériel), **Android Chrome**, **Firefox/Gecko**, **WebKit natif**, **pinch-zoom tactile/trackpad**, et scan automatique **`axe-core`** (`node_modules/axe-core` absent du repo sans ajout npm autorisé) | **Non testé** |
