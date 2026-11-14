# 07 - Checklist WCAG 2.2 AA / AAA & Vérifications Manuelles

- **Branche** : `audit/typography-accessibility-v3`
- **Date de vérification** : 2026-11-14
- **Objectif** : distinguer rigoureusement ce qui est prouvé par tests automatisés (`Playwright Chromium` sur **`238` contextes**, `node --test`, `wcagContrast.ts`) de ce qui reste **réellement non testé** et à valider manuellement sur matériel physique, navigateurs tiers ou lecteurs d'écran.

---

## 1. Critères Vérifiés Automatiquement (Passe Unifiée `238` Contextes + Tests Unitaires)

| Critère WCAG 2.2 | Niveau | Méthode & Périmètre vérifié | Résultat mesuré (build final) | Réserves / Limites |
| :--- | :---: | :--- | :--- | :--- |
| **1.4.3 Contraste (minimum)** | AA | Calcul colorimétrique Canvas RGBA (`oklch` + `rgb`) sur **`238` contextes** (`vite preview` `dist/` + DEV `ColorAtlasDrawer` `#pillars`, `#scales` x5 familles Light/Dark, `#tester`) + sonde `35` `<text>` SVG `/activites` L/D + `wcagContrast.ts` | **`0 / 238` échec HTML actif `< 4.5:1`** (`--on-primary` Dark `#081C15`/`#74C69D` **`8.68:1`**, `amber-800` **`7.09:1`**) ; **`0 / 70` échec SVG** (boussole `"N"` halo `#141816` `3px` -> **`17.92:1`**) | Contrôles désactivés RBAC (`guichet`/`comptable`) exemptés WCAG ; textes posés sur photographies Hero évalués visuellement sur PNG |
| **1.4.6 Contraste (amélioré)** | AAA | `--text-muted` mesuré via `src/utils/wcagContrast.ts` et testé dans `ecosystemE2E.test.ts` | **`10.29:1`** (Light `#36403A` sur `#F6FBF8`) et **`11.71:1`** (Dark `#C9D1CC` sur `#121614`) | Ciblé sur les paires éditoriales et notes principales |
| **1.4.4 Redimensionnement du texte (200%)** | AA | Simulation `html { font-size: 32px }` et `html { zoom: 2 }` sur `/`, `/decouvrir`, `/reserver`, `/tarifs`, `/activites` et `/exploitation` (`390x844` & `1440x900`) | **PASS (`0 / 19` `docOverflowPx`, `0 / 19` `clippedCount`, `0 / 19` `overflowingCount`)** ; `"ECOPARK CAMEROUN"` sans rognage visuel sur `zoom_font200_390x844.png` | Exception native `<select>` mono-ligne fermé sur `"Élevage, Bassins & Flore (LC / NT)"` à `32px` (`scrollW 447 > clientW 298` sans débordement carte/page) ; zoom navigateur natif iOS/desktop à valider sur matériel réel |
| **1.4.10 Redistribution (Reflow)** | AA | Viewports `320x700` à `1920x1080` + `640x400` sur les `14` routes publiques et `/exploitation` RBAC | **`0 / 238` `docOverflowPx` (`scrollWidth === vw`)**, `0` troncature HTML | Ruban horizontal `.eco-chapternav-scroll` et tableaux `overflow-x-auto` défilables volontairement ; `<select>` `CitizenSentinel` `trail.name` long (`scrollW > clientW`) sans débordement parent/document |
| **1.4.11 Contraste non textuel & `:focus-visible`** | AA | Boutons statuts `emerald-800` / `amber-800` / `red-800` (Light) & `-300` (Dark), bordures `--border-default` et contrôle `:focus-visible` (`3px solid`) | **PASS (`0` erreur sur `238` contextes)** | Modes OS `prefers-contrast: more` et `forced-colors: active` non simulés |
| **1.4.12 Espacement du texte** | AA | Styles calculés sur `.type-body` (`16/17px`, `lh 1.55/1.60`, `ls 0em`) et `.type-body-compact` | **PASS (`line-height >= 1.5x`, `letter-spacing: 0em`)** | Surcharge utilisateur externe (`2x` interlignage, `0.12em` lettres) non injectée |
| **1.3.1 / 2.1.1 / 2.1.2 / 2.4.3 / 4.1.2 Clavier, Modales, `inert` & ARIA** | A / AA | **`6 / 6` suites clavier Playwright PASS** : `AhalaShowcase` (`ArrowRight`/`End`/`Home`/`ArrowLeft`), `Navbar` (`Escape` dropdown daltonisme + drawer mobile `#mobile-nav-drawer` + restauration focus), `DigitalEcoPass` (`inert` + `aria-hidden` synchronisés dès la création du pass, `0` fuite `Tab` sur `12` pressions Recto/Verso, transfert `Enter`), `RangerDashboard` Modales 1/2/3 (`role="dialog"`, `aria-modal="true"`, `aria-labelledby`, `htmlFor`/`id` des `<textarea>`, piège `Tab`, `Escape` + retour focus + repli focus vers `<h2>` à la suppression du bouton M2), `ColorAtlasDrawer` (`Enter`, piège `18` `Tab` + `Shift+Tab`, `Escape` capture + retour focus) | **PASS (`6 / 6` suites)** | Restitution vocale réelle à valider au lecteur d'écran (NVDA / VoiceOver) |
| **2.5.8 Taille de cible tactile** | AA | Audit Playwright de tous contrôles HTML autonomes sur `vw <= 1024px` (`320`, `360`, `390`, `430`, `640`, `768`, `1024`) | **`0 / 238` défaut (`smallTapCount = 0`)** | Liens prose inline `tel:`/`mailto:` exemptés WCAG 2.5.8 *Inline* et marqueurs SVG `InteractiveTopoMap` compensés par boutons HTML `>= 44px` |
| **1.4.1 / Daltonisme & Stabilité CLS** | - | Activation `deuteranopia`, `protanopia`, `tritanopia` (`0` overflow, `0` contraste) + `PerformanceObserver` CLS sur `5` routes | **`CLS <= 0.05446`** (`/` `0.05446`, `/activites` `0.00582`, `/decouvrir` `0.00720`, `/reserver` `0.00467`, `/exploitation` `0.00034`) | Appréciation perceptive clinique sur matériel réel non substituée par filtre SVG |

---

## 2. Éléments Réellement Non Testés (Vérifications Manuelles Requises Avant Fusion)

Les points suivants n'ont **pas** été exécutés dans la passe Playwright Chromium headless et restent **réellement non testés** :

### A. Lecteurs d'écran réels (NVDA / JAWS / VoiceOver / TalkBack)
- [ ] **NVDA (Windows) & VoiceOver (macOS/iOS)** : vérifier l'annonce vocale effective du `HeroCanopy`, des 4 boutons `.bento-plus-btn` (`aria-expanded`), des onglets `AhalaShowcase` (`role="tablist"`), du ruban d'étapes `BookingWizard` et des messages d'erreur `aria-describedby` à l'étape 2.
- [ ] **DigitalEcoPass & Modales `RangerDashboard` / `ColorAtlasDrawer`** : confirmer au lecteur d'écran que la face `inert` du pass n'est jamais exposée à l'arbre d'accessibilité vocal et que le titre `aria-labelledby` des modales (plus déplacement focus vers `<h2>` après résolution d'une observation M2) est annoncé clairement.

### B. Matériel physique, Navigateurs Non-Chromium & Préférences Système OS
- [ ] **Matériel physique iOS Safari (iPhone) & Android Chrome** : tester le pinch-zoom tactile, l'absence de zoom involontaire iOS sur les `<select>` (`SpeciesAtlas`, `RangerDashboard`, `CitizenSentinel`), le défilement tactile du Chapternav et le rendu physique des polices.
- [ ] **Navigateurs non-Chromium (Firefox Gecko, Safari WebKit)** : vérifier le rendu typographique (`Barlow Semi Condensed`, `Source Sans 3`, `JetBrains Mono`), les View Transitions (ou fallback CSS) et l'affichage de la popup `<option>` native OS ouverte (`SpeciesAtlas` `"Élevage, Bassins & Flore (LC / NT)"` et `CitizenSentinel` noms complets de sentiers).
- [ ] **Modes OS d'accessibilité (`prefers-contrast: more` & Windows High Contrast `forced-colors: active`)** : contrôler bordures, anneaux `:focus-visible`, pastilles de statut et icônes SVG lorsque le système force sa propre palette.
- [ ] **Audit tiers `axe-core`** *(optionnel)* : exécuter l'extension DevTools `axe` en navigateur sur les vues clés si un contrôle externe complémentaire sans ajout dans `package.json` est souhaité avant fusion.
