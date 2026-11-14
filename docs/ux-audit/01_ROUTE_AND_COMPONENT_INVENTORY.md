# 01 — Inventaire Exhaustif des Routes, Vues, Composants & Sources CSS/Tokens

- **Branche d'audit** : `audit/typography-accessibility-v3` (créée depuis `feat/react-adobe-color-ahala` @ `6157dd7`, parent `0f677f8`)
- **Date** : 2026-11-14
- **Méthodologie** : Analyse statique exhaustive du code source (`src/`, `index.html`, `vercel.json`, `tokens/`, `styles/`) préalablement aux mesures navigateur Playwright (Livrables `02` à `04`).
- **Distinction épistémique** : Tous les éléments ci-dessous sont **observés statiquement** dans les fichiers cités ; aucun ratio calculé en runtime DOM n'est affirmé ici sans renvoi à l'audit Playwright (`02`–`04`).

---

## 1. Architecture Applicative, Build & Tests

| Élément | Valeur observée | Source |
| :--- | :--- | :--- |
| Framework UI | React 19 + TypeScript strict (`tsc -b`) | `package.json`, `src/main.tsx` |
| Bundler & CSS | Vite 6 (`vite v6.4.6`) + `@tailwindcss/vite` v4.0.9 | `package.json` |
| Icônes | `lucide-react` | `package.json` |
| Routage | Sans routeur tiers : moteur History API bidirectionnel (`window.history.pushState` / `popstate`) + CustomEvent `ecopark:showcase-nav` | `src/utils/ecoRouting.ts`, `src/App.tsx` |
| Tests | `node --test --experimental-strip-types "src/utils/*.test.ts"` — **32/32 tests OK** sur `6157dd7` (parent `0f677f8`) | `package.json`, `src/utils/*.test.ts` |
| Build baseline | `npm run build` (`tsc -b && vite build`) — OK en 2.73s sur `audit/typography-accessibility-v3` | `package.json` |

---

## 2. Cartographie Complète des Routes, Vues & États UI

### 2.1. Vues principales (`ActiveView`) & Sous-vues

`ActiveView` (`src/types/ecosystem.ts`) comprend **9 identifiants** (`accueil`, `sentiers`, `biodiversite`, `billetterie`, `pass`, `ranger`, `connexion`, `legal`, `color_atlas`). Note : `color_atlas` n'est pas une page isolée mais l'ouverture du tiroir modale `ColorAtlasDrawer` par-dessus la vue active.

| `ActiveView` | Route canonique (`VIEW_PATH_MAP`) | Alias `resolveViewFromPath` & `vercel.json` | Composant(s) rendu(s) | État / Garde d'accès |
| :--- | :--- | :--- | :--- | :--- |
| `accueil` | `/` | `/`, `/contact`, `/whatsapp` (+ 13 deep paths Showcase) | `HeroCanopy`, `ImpactBanner`, `AhalaShowcase` (5 onglets), grilles Sentiers (6) & Biodiversité (8) dans `App.tsx` | Public |
| `sentiers` | `/activites` | `/activites`, `/fiche-activite` | Bannière canopy `App.tsx`, `InteractiveTopoMap`, `ElevationProfile`, `TrailCatalog` | Public |
| `biodiversite` | `/decouvrir` | `/decouvrir` | `SpeciesAtlas` | Public |
| `billetterie` | `/reserver` | `/reserver`, `/rdv`, `/rendez-vous`, `/preparer-ma-visite` | Bannière canopy `App.tsx`, `BookingWizard` (Étapes 1, 2, 3 + confirmation) | Public |
| `pass` | `/mon-espace` | `/mon-espace`, `/mes-reservations`, `/espace-cliente` | Bannière dark `App.tsx`, `DigitalEcoPass` (recherche anonyme `/mon-pass` ou pass connecté + 3D Recto/Verso + modale annulation), `CitizenSentinel` (onglets `form`/`feed`, monté uniquement si `isAuthenticated === true` dans `App.tsx:408-415`) | Public (lookup anonyme par Code + Email/Tél) ou Client connecté |
| `ranger` | `/exploitation` | `/exploitation`, `/cockpit-pro`, `/guichet`, `/direction`, `/admin` | 1) Si non authentifié : écran `App.tsx` + `AuthPortal embedded defaultStaffMode`; 2) Si client non staff : écran 403 `App.tsx`; 3) Si staff : `RangerDashboard` (Sections 1–6 + 3 modales) | Staff RBAC (6 postes provisionnés) |
| `connexion` | `/connexion` | `/connexion`, `/Connexion`, `/login`, `/inscription`, `/mon-compte` | `AuthPortal` (non connecté : 4 modes `client_login`, `client_register`, `staff_login`, `recover` ; connecté : profil + changement MDP + suppression Loi 2010/012) | Public / Authentifié |
| `legal` | `/mentions-legales` | `/mentions-legales`, `/cgv`, `/cgu`, `/confidentialite` | `LegalNoticeView` (3 onglets : `mentions`, `cgv`, `confidentialite`) | Public |
| `color_atlas` | *(aucune route URL — fallback `'accueil'` sur `/atelier-couleurs`)* | *(aucun alias dans `ecoRouting.ts` / `vercel.json` ; déclenchée uniquement par le bouton `"Atelier"` de `Navbar.tsx` lorsque `isDevEnvironment() === true` ou appel direct à `color_atlas`)* | `ColorAtlasDrawer` (3 onglets : Piliers Chrom., Échelles 50–950, Palettes Adobe / Testeur WCAG) | Overlay DEV (`vite dev` uniquement par défaut, absent en build `vite preview`) |

> **Remarques routage `vercel.json` / `ecoRouting.ts` / `EcoParkContext.tsx`** : `vercel.json` contient **78 règles** (`rewrites` lignes 7–84, soit **39 chemins de base** doublés avec et sans slash final). Note : `/espace-cliente` est listé dans `vercel.json` et `ecoRouting.ts` (`pass`) ; `/mon-pass` apparaît uniquement dans le libellé du test unitaire `ecosystemE2E.test.ts:470` pour désigner le flux fonctionnel de recherche anonyme sur `/mon-espace` (il n'existe pas de route HTTP `/mon-pass`). Tout chemin inconnu (`resolveViewFromPath` retournant `null`, par exemple `/atelier-couleurs` en production) bascule sur `'accueil'` via `EcoParkContext.tsx`.

### 2.1bis. Inventaire des Composants UI (`src/components/**` — 19 fichiers TSX + `src/App.tsx`)

| Domaine / Fichier | Lignes | Rôle principal | Spécificités typographiques observées |
| :--- | :---: | :--- | :--- |
| `src/App.tsx` | 518 | Routeur vues, bannières intérieures, grilles Accueil & garde RBAC | 3 `<h1>` (`sentiers`, `billetterie`, `pass`, + `ranger` unauth/403), 3 `!text`/`!leading`, 22 `text-xs`, 2 `text-[Npx]` |
| `src/components/layout/Navbar.tsx` | 652 | Temps 1 promo, Global Nav `.type-nav`, Chapternav, `MobileDrawer`, sélecteurs Thème/Daltonisme | `truncate` Temps 1 & marque, `shrink-0` nav/badges, 11 `text-xs`, 7 `text-[Npx]` |
| `src/components/layout/Footer.tsx` | 299 | Pied de page, contacts, accès rapides, mentions légales | `text-[21px]` figé (`footer-brand`), 10 `text-xs`, 1 `text-[Npx]` |
| `src/components/layout/ImmersiveSection.tsx` | 116 | Conteneur section plein écran avec `overflow-hidden` | Rognage latéral du `<h1>` Hero sous zoom 200% (`390px`) |
| `src/components/discovery/HeroCanopy.tsx` | 358 | Hero Accueil (`<h1>`), collage 3 vignettes, télémétrie | `<h1>` `.type-hero` (`ligne 70`), 5 `!text-*`, 13 `text-[11px]`, 3 `truncate` |
| `src/components/discovery/ImpactBanner.tsx` | 230 | 4 cartes Bento + tiroirs BLUF (`bento-plus-btn`) | 6 `!text`/`!leading`, 4 `text-[Npx]`, 3 `text-xs` |
| `src/components/discovery/AhalaShowcase.tsx` | 1039 | 5 onglets Showcase, comparateur Pass, table native `<table>` Tarifs | **23 `!text`/`!leading`**, `hotel.priceRange` `truncate`, 22 `text-xs`, 4 `text-[Npx]` |
| `src/components/map/InteractiveTopoMap.tsx` | 958 | Carte SVG topo `viewBox="0 0 1000 700"`, calques & zoom | 27 `text-[Npx]` (SVG `9–10px` & UI), 3 `text-xs`, barre Calques sans `flex-wrap` |
| `src/components/map/ElevationProfile.tsx` | 571 | Profil altimétrique SVG + simulateur marche | 14 `text-[Npx]` (`9–10px` SVG & UI), 5 `text-xs` |
| `src/components/trails/TrailCatalog.tsx` | 473 | Catalogue 6 sentiers, filtres difficulté/secteur/état | `font-serif italic`, `line-clamp-3`, 22 `text-xs`, 12 `text-[Npx]` |
| `src/components/biodiversity/SpeciesAtlas.tsx` | 487 | Atlas faune/flore, `<select>` UICN, filtres onglets | `<h1>` sans `.type-*`, `<select>` non contraint (`min-w-0`), 20 `text-xs`, 6 `text-[Npx]` |
| `src/components/booking/BookingWizard.tsx` | 1064 | Tunnel réservation 3 étapes + steppers & validation | 35 `text-xs`, 15 `text-[Npx]` (`text-[11px]` erreurs), steppers `w-8 h-8` |
| `src/components/booking/DigitalEcoPass.tsx` | 973 | Recherche anonyme, Pass 3D Recto/Verso, Plein Soleil / OLED | 39 `text-xs`, 16 `text-[Npx]` (`11px` Serment/champs), 1 `!text-white` |
| `src/components/booking/Co2BotanicalSprout.tsx` | 195 | Certificat / jauge végétale CO2 intégrée à l'Éco-Pass | 2 `text-xs`, 2 `text-[Npx]` (`text-[11px]`) |
| `src/components/booking/GerminatingQrCode.tsx` | 107 | Générateur visuel QR SVG ISO encapsulé dans l'Éco-Pass | `aria-label` QR SVG, 0 classe micro-texte HTML |
| `src/components/field/CitizenSentinel.tsx` | 787 | Signalement terrain (`form`) & flux communautaire (`feed`) | 27 `text-xs`, 17 `text-[Npx]` (`10px`/`11px` métadonnées photo) |
| `src/components/auth/AuthPortal.tsx` | 900 | 4 modes connexion/inscription/staff/récupération + profil | `<h1>` sans `.type-*`, 36 `text-xs`, 2 `text-[Npx]` |
| `src/components/legal/LegalNoticeView.tsx` | 183 | 3 onglets légaux (`mentions`, `cgv`, `confidentialite`) | `<h1>` sans `.type-*`, 10 `text-xs` en corps de texte |
| `src/components/admin/RangerDashboard.tsx` | 1897 | Cockpit Pro RBAC (Sections 1–6, SVG affluence, 3 modales) | Profil C `< 20px`, `<h1>`=`<h2>`=`<h3>`=`16px`, 83 `text-xs`, 50 `text-[Npx]`, `line-clamp-1` |
| `src/components/design-system/ColorAtlasDrawer.tsx` | 879 | Tiroir DEV palette Adobe, échelles 50–950, testeur WCAG | 30 `text-xs`, 18 `text-[Npx]` (`9px–11px`), `truncate` |

*(S'y ajoutent `src/context/AuthContext.tsx`, `src/context/EcoParkContext.tsx`, `src/context/ThemeContext.tsx` et `src/main.tsx`, portant le total à 24 fichiers `.tsx` dans `src/`.)*

### 2.2. Deep Paths Showcase & Onglets (`ShowcaseTab`)

| Onglet (`ShowcaseTab`) | Route canonique | Alias dans `ecoRouting.ts` & `vercel.json` | Contenu dans `AhalaShowcase.tsx` |
| :--- | :--- | :--- | :--- |
| `hebergements` | `/hebergements` | `/hebergements`, `/hotellerie` | 30 Hôtels & Suites (Ewondo, Chanthel, Bene) + 3 Pass comparator `#pass-comparateur` |
| `saveurs` | `/restaurant` | `/restaurant`, `/sejour-restaurant` | Château des Saveurs, Barbecue Royal, Glaciers, Bars & Lounges |
| `tarifs` | `/tarifs` | `/tarifs`, `/nos-tarifs` | Grille native `<table>` (`panel-tarifs`, maintenue dans le DOM via CSS `hidden` pour accessibilité/tests) |
| `entreprise` | `/pack-entreprise` | `/pack-entreprise`, `/pack-ecole`, `/groupes-evenements`, `/agenda`, `/evenements` | Team building, mariages 400 pl., sorties scolaires, événements |
| `formation` | `/formation` | `/formation`, `/formations` | CFP MINEFOP Yaoundé (5 filières + options additionnelles `#cross-sell-options`) |

### 2.3. Tiroirs, Modales & États Transverses

- **En-tête & Navigation (`src/components/layout/Navbar.tsx`)** :
  - *Temps 1* : Bandeau d'accueil sticky (`42px` / `44px`, masqué sur `/exploitation` via `isOperationalCockpit`).
  - *Niveau 1* : Global Nav (`.type-nav`, `44px` desktop / `48px` mobile, sélecteur de vue + boutons Thème `light`/`dark`/`auto` + menu déroulant Vision/Daltonisme + menu hamburger mobile `< lg`).
  - *Temps 2* : Chapternav (`.type-chapternav`, 5 ancres d'accès rapide vers `AhalaShowcase`, visible sur desktop uniquement quand `activeView === 'accueil'` ou `activeView === 'sentiers'`, masqué sur `ranger`).
- **Thèmes & Accessibilité visuelle (`src/context/ThemeContext.tsx`)** :
  - `themeMode` (`auto`, `light`, `dark` -> classe `.dark` + `[data-theme="dark"|"light"]`). Note : script anti-FOUC dans `index.html` force `'light'` par défaut si aucun choix stocké.
  - `daltonismMode` (`normal`, `deuteranopia`, `protanopia`, `tritanopia` -> attribut `[data-vision="..."]` + filtres SVG dans `index.html`).
  - `highContrastOutdoor` (`[data-outdoor-contrast="true"]`, activable depuis `DigitalEcoPass`).
- **Composants interactifs multi-états** :
  - `ImpactBanner` : 4 cartes Bento équipées chacune d'un tiroir BLUF permanent (`grid-rows-[0fr]` / `grid-rows-[1fr]`, `.bento-plus-btn`).
  - `DigitalEcoPass` : Vue recherche anonyme (formulaire code + téléphone/email), Vue Pass déverrouillé (Face Recto QR animé + Face Verso 3D certificat carbone + modale d'annulation + mode plein soleil).
  - `RangerDashboard` : Sections conditionnées par rôle RBAC (`Section 1` Jauge & 4 KPIs + histogramme SVG horaires ; `Section 2` Contrôle sentiers + modale fermeture urgente ; `Section 3` Check-In QR ; `Section 4` Modération Citizen Sentinel + modale résolution ; `Section 5` Journal & Audit SYSCOHADA FCFA ; `Section 6` Matrice RBAC 6 postes ; `Modal 3` Reset Seed).

---

## 3. Sources CSS, Polices & Design Tokens

### 3.1. Chargement des polices (`index.html:18-24`)
Google Fonts preconnect + stylesheet charge 3 familles :
1. **`Barlow Semi Condensed`** (weights `600;700;800`) : Display / Titres (`.type-hero`, `.type-h2`, `.type-h3`, `.type-eyebrow`, marque Navbar/Footer, et nombreuses classes ad-hoc `font-['Barlow_Semi_Condensed']`).
2. **`Source Sans 3`** (weights `400;500;600;700`) : Sans / Corps de texte (`--font-sans`).
3. **`JetBrains Mono`** (weights `400;500;600`) : Monospace / Télémétrie / Prix (`--font-mono`, `.type-footnote`).

### 3.2. Feuille active (`src/index.css`, 1013 lignes — importée par `src/main.tsx:4`)
- **Tokens couleur Light (`:root`)** : `--bg-canvas: #F6FBF8`, `--bg-surface: #E9F5ED`, `--bg-elevated: #FFFFFF`, `--text-primary: #1F2421`, `--text-muted: #36403A` (calibré >= 7:1 WCAG AAA, testé par `ecosystemE2E.test.ts`), `--brand-primary: #1B4332`, `--brand-accent: #84562D` (dark ochre pour texte).
- **Tokens couleur Dark (`.dark, [data-theme="dark"]`)** : `--bg-canvas: #121614`, `--bg-surface: #1F2421`, `--bg-elevated: #29302C`, `--text-primary: #E9F5ED`, `--text-muted: #C9D1CC` (calibré >= 7:1 WCAG AAA), `--brand-primary: #52B788`.
- **Échelle typographique optique (Fiche mémo n°4)** dans `src/index.css:374-572` :
  - `.type-nav` : `12px`, `line-height: 16px`, `letter-spacing: -0.010em`, `font-weight: 500`.
  - `.type-chapternav` : `11px` mobile / `12px` desktop (`>=1024px`), `line-height: 16px`, `letter-spacing: -0.010em`, `font-weight: 500`.
  - `.type-eyebrow` : `12px` / `14px` desktop (`>=1024px`), `var(--font-sans)` (`Source Sans 3`), `font-weight: 600`, `letter-spacing: -0.010em` / `-0.014em`.
  - `.type-hero` : `48px` (`3rem`) mobile (`line-height: 1.0833`, `tracking: -0.003em`) / `clamp(3.25rem, 5.2vw, 5rem)` (`52px..80px`) desktop (`line-height: 1.05`, `tracking: -0.015em`).
  - `.type-h2` : `32px` mobile (`line-height: 1.125`) / `clamp(2.25rem, 3.34vw, 3rem)` (`36px..48px`) desktop (`line-height: 1.0833`).
  - `.type-h3` : `21px` mobile (`line-height: 1.1905`) / `24px` desktop (`line-height: 1.1667`).
  - `.type-tagline` : `19px` mobile (`line-height: 1.2105`) / `24px` desktop (`line-height: 1.1667`).
  - `.type-body` : **`15px` mobile (`0.9375rem`, `line-height: 22px`, `letter-spacing: -0.016em`) / `17px` desktop (`1.0625rem`, `line-height: 25px`, `letter-spacing: -0.022em`)**. *Point critique : taille mobile < 16px et tracking négatif accentué sur Source Sans 3.*
  - `.cta-pill` / `.cta-chevron` : `14px`, `line-height: 18px`, `tracking: -0.014em`.
  - `.type-footnote` : `12px`, `line-height: 16px`, `tracking: -0.008em` / `-0.010em`.
- **Garde-fou iOS (`src/index.css:334-340`)** : Sur `@media (max-width: 1023px)`, force `font-size: max(1rem, 16px) !important` sur `input:not([type="checkbox"]):not([type="radio"]):not([type="range"])`, `select`, `textarea`.

### 3.3. Sources dormantes / divergentes (non importées par Vite)
| Fichier | Statut | Divergence constatée par rapport à `src/index.css` |
| :--- | :--- | :--- |
| `styles/theme.css` | **Dormant** (jamais importé dans `src/`) | Déclare `--text-muted: #46534B` (Light) et `#A3B0A8` (Dark), inférieurs au calibrage AAA `#36403A` / `#C9D1CC` de `src/index.css`. Pas de tokens typographiques. |
| `tailwind.config.js` | **Dormant** (Tailwind v4 utilise `@theme` dans CSS, aucun `@config` dans `src/index.css`) | Héritage Tailwind v3, aucune échelle `fontSize` / `fontFamily` personnalisée. |
| `tokens/color-tokens.json` | Documentation/source W3C couleur uniquement | Couleurs seules (`--text-muted` aligné sur `#46534B`/`#A3B0A8`), aucun token typographique. |
| `public/color-atlas-standalone.html` | Asset statique autonome | Hors bundle React (`App.tsx`), lien externe depuis `ColorAtlasDrawer`. |

---

## 4. Audit Statique des Anomalies Typographiques par Catégorie

### 4.1. Hiérarchie des `<h1>` (11 occurrences `<h1` dans `src/`)

| Fichier & Ligne | Vue / État | Classes actuelles | Constat statique |
| :--- | :--- | :--- | :--- |
| `HeroCanopy.tsx:70` | `accueil` | `type-hero text-white` (`48px` -> `52–80px`) | Conforme au Profil A éditorial, ~10 mots finissant par `.` (tagline en `HeroCanopy.tsx:76`). |
| `App.tsx:266` | `sentiers` | `type-h2 text-white mt-1` (`32px` -> `36–48px`) | Utilise la classe `type-h2` pour un `<h1>` de vue intérieure. |
| `App.tsx:315` | `billetterie` | `type-h2 text-white mt-1` | Utilise la classe `type-h2` pour un `<h1>` de vue intérieure. |
| `App.tsx:343` | `pass` | `font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1` | Contourne `.type-*` (`24px` -> `36px`). |
| `SpeciesAtlas.tsx:180` | `biodiversite` | `font-['Barlow_Semi_Condensed'] text-3xl sm:text-4xl lg:text-5xl font-bold text-white tracking-tight leading-tight` | Contourne `.type-*` (`30px` -> `36px` -> `48px`). |
| `LegalNoticeView.tsx:41` | `legal` | `font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1` | Contourne `.type-*` (`24px` -> `36px`). |
| `AuthPortal.tsx:236` & `887` | `connexion` (connecté / non connecté) | `font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1` | Contourne `.type-*` (`24px` -> `36px`). |
| `App.tsx:441` & `465` | `ranger` (login & 403) | **`font-sans text-base font-bold text-[var(--text-primary)]`** (`16px`!) | **`<h1>` à `16px` en `Source Sans 3`** (même taille qu'un corps de texte), contournant la hiérarchie display. |
| `RangerDashboard.tsx:476` | `ranger` (connecté staff) | **`font-sans text-base font-bold text-[var(--text-primary)] mt-0.5`** (`16px`!) | Strictement calé sous le seuil `< 20px` du Profil C, mais sans différenciation hiérarchique avec `<h3>` (`text-base` aux lignes 681, 790, 1680, 1772, 1861) et `<h2>` (`text-base` aux lignes 548, 866, 1039, 1180, 1463, 1609). |

### 4.2. Surcharges `!important` Tailwind (`!text-*` / `!leading-*` — 38 occurrences)

Ces classes brisent la cohérence de `.type-body`, `.type-h3` et `.type-eyebrow` :
- `AhalaShowcase.tsx` (**23** occurrences) : lignes 389 (`type-body !text-[14px] !leading-[20px]`), 521 (`type-h3 !text-2xl sm:!text-3xl`), 524/784/809/834/859 (`type-body !text-sm`), 583/984 (`type-h3 !text-xl`), 586/646/691/901/935/988 (`type-body !text-xs sm:!text-sm`, descendant le corps de texte à `12px` sur mobile !).
- `ImpactBanner.tsx` (**6** occurrences) : lignes 109 (`!text-[#74C69D]`), 179 (`type-h3 !text-[21px] sm:!text-[22px]`), 184 (`type-body !text-[14px] !leading-[20px]`), 189 (`type-footnote !text-[#B7E4C7]`).
- `HeroCanopy.tsx` (**5** occurrences de couleur) : lignes 64, 89, 95, 101, 157.
- `App.tsx` (**3** occurrences) : ligne 169 (`type-h3 !text-xl`), ligne 173 (`type-body !text-xs sm:!text-sm` -> `12px` mobile sur descriptions de sentiers en accueil !).
- `DigitalEcoPass.tsx` (**1** occurrence) : ligne 592 (`type-h3 !text-white`).

### 4.3. Inventaire des Micro-Tailles (`text-[9px..13px]` et `text-xs`)

Total des classes arbitraires `text-[Npx]` dans `src/` : **210 occurrences** réparties comme suit :
- `text-[9px]` (**11 occurrences**) : `RangerDashboard.tsx:832` (`cumul global` KPI), `ColorAtlasDrawer.tsx:618` (badge), `InteractiveTopoMap.tsx` (7 libellés/échelle SVG), `ElevationProfile.tsx` (2 libellés axes/POI SVG).
- `text-[10px]` (**65 occurrences**) : dont `RangerDashboard.tsx` (en-têtes KPI/badges/axes SVG), `InteractiveTopoMap.tsx`, `ElevationProfile.tsx`, `CitizenSentinel.tsx` (7 occurrences), `ColorAtlasDrawer.tsx` (7 occurrences), `TrailCatalog.tsx` (5 occurrences : D+, Durée, Niveau, PMR, badge), `Navbar.tsx` (3 occurrences : ligne 307 sous-titre logo sur mobile, ligne 336 badge, ligne 548 chapternav badge), `BookingWizard.tsx` (2 occurrences), `App.tsx` (1 occurrence ligne 242 statut espèce).
- `text-[11px]` (**117 occurrences**) : réparties dans `HeroCanopy.tsx` (**13** occurrences : 3 légendes photo + télémétrie), `DigitalEcoPass.tsx` (**15** occurrences : champs du pass & Serment Zéro-Trace), `BookingWizard.tsx` (**13** occurrences : aides, formulaires, erreurs, notes mobilité), `CitizenSentinel.tsx` (**8** occurrences), `SpeciesAtlas.tsx` (**6** occurrences), `TrailCatalog.tsx` (**7** occurrences), `ColorAtlasDrawer.tsx` (**8** occurrences), `Navbar.tsx` (**3** occurrences), `AhalaShowcase.tsx` (**3** occurrences), `Co2BotanicalSprout.tsx` (**2** occurrences), `AuthPortal.tsx` (**2** occurrences), `ImpactBanner.tsx` (**1** occurrence), `App.tsx` (**1** occurrence), ainsi que `RangerDashboard.tsx`, `InteractiveTopoMap.tsx`, `ElevationProfile.tsx`.
- `text-[12px]` (2 : `Navbar.tsx:244`, `RangerDashboard`), `text-[13px]` (1 : `InteractiveTopoMap.tsx:503`), `text-[14px]` (2 : `ImpactBanner.tsx:184`, `AhalaShowcase.tsx:389`), `text-[18px]` (9 : métriques `RangerDashboard.tsx`), `text-[21px]` (2 : `Footer.tsx:70`, `ImpactBanner.tsx:179`), `text-[22px]` (1 : `ImpactBanner.tsx:179`).
- `text-xs` (`12px`) : **383 occurrences** exactes à travers **18 fichiers `.tsx`** (`RangerDashboard`: 83, `DigitalEcoPass`: 39, `AuthPortal`: 36, `BookingWizard`: 35, `ColorAtlasDrawer`: 30, `CitizenSentinel`: 27, `App`: 22, `AhalaShowcase`: 22, `TrailCatalog`: 22, `SpeciesAtlas`: 20, `Navbar`: 11, `Footer`: 10, `LegalNoticeView`: 10, `ElevationProfile`: 5, `HeroCanopy`: 3, `ImpactBanner`: 3, `InteractiveTopoMap`: 3, `Co2BotanicalSprout`: 2), majoritairement utilisées pour des paragraphes, libellés de formulaires, boutons et cellules de tableaux.

### 4.4. Troncatures (`truncate`, `line-clamp-*`) & `whitespace-nowrap`

| Fichier & Ligne | Classe | Contenu affecté | Risque fonctionnel |
| :--- | :--- | :--- | :--- |
| `Navbar.tsx:248` | `truncate sm:whitespace-normal block min-w-0` | Bandeau Temps 1 (`Entrée dès 500 FCFA · Zoo, Lac...`) | Masque l'information tarifaire et horaire sur mobile (`< 640px`). |
| `Navbar.tsx:304` | `truncate` | Titre marque `ECOPARK CAMEROUN` | Risque de coupure à `320px`. |
| `Navbar.tsx:307` | `truncate` | Sous-titre `YAOUNDÉ · AHALA...` (`10px`/`11px`) | Risque de coupure mobile + sous-dimensionnement. |
| `Navbar.tsx:645` | `truncate` | Bouton Vision mobile (`Vision : ...`) | Coupure possible à `320px`. |
| `Navbar.tsx` (6 lignes) | `whitespace-nowrap` | Liens Temps 1 / Global Nav / Chapternav | À mesurer sur `1024px` et zoom 200% pour vérifier absence de débordement horizontal. |
| `HeroCanopy.tsx:186, 199, 212` | `truncate` | Légendes des 3 photos (`Piscine Semi-Olympique & Toboggans`, `Sanctuaire & Pédagogie Nature`, `Hôtellerie Ewondo · Chanthel · Bene`) | Coupure d'information sur la grille `grid-cols-3` sur petit mobile. |
| `AhalaShowcase.tsx:601` | `type-footnote font-mono truncate tabular-nums` | Prix/fourchette tarifaire `hotel.priceRange` des hôtels | **P0 potentiel : troncature de prix/informations essentielles.** |
| `App.tsx:173` | `line-clamp-2` | Description de chacun des 6 sentiers sur l'Accueil | Suppression de texte informatif couplée à `!text-xs`. |
| `App.tsx:179` | `truncate pr-2` | `trail.biomeLabel` en pied de carte sentier | Coupure du nom de biome. |
| `TrailCatalog.tsx:380` | `line-clamp-3` | `trail.description` dans le catalogue | Coupure d'information descriptive. |
| `RangerDashboard.tsx:1097` | `line-clamp-1` | Titre de formule / détail pass dans file check-in | Coupure d'information opérationnelle guichet. |
| `ColorAtlasDrawer.tsx:850` | `truncate` | Étiquette dans le tiroir chromatique | Coupure secondaire. |

---

## 5. Contraintes E2E Existants Impératives (`src/utils/ecosystemE2E.test.ts`)

Toute proposition de remédiation (Livrable `ECOPARK_TYPOGRAPHY_TOKENS_V3.md` & `05_COMPONENT_REMEDIATION_PLAN.md`) doit composer avec les assertions codées en dur dans `src/utils/ecosystemE2E.test.ts:342-468` :
1. **Loi 1 (zéro tiret typographique)** : Aucun `\u2013` ni `\u2014` dans `index.html` et tous fichiers `.ts/.tsx/.css/.html` de `src/`.
2. **Présence obligatoire de sélecteurs dans `src/index.css`** : `.type-nav`, `.type-chapternav`, `.type-eyebrow`, `.type-hero`, `.type-h2`, `.type-h3`, `.type-tagline`, `.type-body`, `.cta-pill`, `.cta-chevron`, `.type-footnote`, `.bento-plus-btn`, `.touch-target-48`, `tabular-nums`, `max(1rem, 16px)`.
3. **Ratios WCAG AAA sur `--text-muted`** : `getContrastRatio('#36403A', '#E9F5ED') >= 7.0`, `getContrastRatio('#36403A', '#FFFFFF') >= 7.0`, `getContrastRatio('#C9D1CC', '#1F2421') >= 7.0`, `getContrastRatio('#C9D1CC', '#29302C') >= 7.0`.
4. **Hero `<h1>`** (`HeroCanopy.tsx`) : regex `/<h1[^>]*className="[^"]*type-hero[^"]*"[^>]*>([\s\S]*?)<\/h1>/` <= 12 mots se terminant par `.`.
5. **Bento Drawers (`ImpactBanner.tsx`)** : présence de `bento-plus-btn`, `aria-expanded`, 4 `bluf: "..."` de 40–55 mots.
6. **Tableau Tarifs (`AhalaShowcase.tsx`)** : `#pass-comparateur`, `#cross-sell-options`, présence de `<table` sans montage conditionnel `activeTab === 'tarifs' &&`.
7. **Cockpit Pro (`RangerDashboard.tsx`)** : interdiction explicite des chaînes `type-hero`, `ImmersiveSection`, `Barlow_Semi_Condensed` et `text-xl`.
