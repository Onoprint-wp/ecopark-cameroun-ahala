# 07 - Checklist WCAG 2.2 AA / AAA & Vérifications Manuelles

- **Branche** : `audit/typography-accessibility-v3`
- **Date de vérification** : 2026-11-14
- **Objectif** : distinguer rigoureusement ce qui est prouvé par tests automatisés (`Playwright Chromium` sur **`360` contextes**, `node --test`, `wcagContrast.ts`) de ce qui reste **non testé / à vérifier manuellement** sur appareils réels ou technologies d'assistance.

---

## 1. Critères Vérifiés Automatiquement (Passe Unifiée `360` Contextes + Tests Unitaires)

| Critère WCAG 2.2 | Niveau | Méthode & Périmètre vérifié | Résultat mesuré (build final) | Réserves / Limites |
| :--- | :---: | :--- | :--- | :--- |
| **1.4.3 Contraste (minimum)** | AA | Calcul colorimétrique Canvas RGBA (support `oklch` + `rgb`) sur **`360` contextes** (`vite preview` `dist/` + DEV `ColorAtlasDrawer` `#pillars`, `#scales` x5 familles Light/Dark, `#tester`) + `wcagContrast.ts` | **`0 / 360` échec actif `< 4.5:1`** (y compris `#scales` x5 familles L/D et `--on-primary` Dark `#081C15`/`#74C69D` `8.68:1`) | Contrôles désactivés RBAC (`guichet`/`comptable`) exemptés WCAG ; textes sur photographies Hero évalués par inspection visuelle des PNG |
| **1.4.6 Contraste (amélioré)** | AAA | `--text-muted` mesuré au runtime sur `360` contextes et testé dans `ecosystemE2E.test.ts` | **`10.29:1` à `11.71:1`** (`--text-primary` `14.07-16.80:1`) | Ciblé sur les paires de texte éditorial et notes principales |
| **1.4.4 Redimensionnement du texte (200%)** | AA | Simulation `html { font-size: 32px }` sur `/`, `/decouvrir`, `/reserver`, `/tarifs`, `/activites` et `/exploitation` (`390x844` & `1440x900`) | **PASS (`0 / 12` `docOverflowX`, `0 / 12` `boxOverflows`, `0 / 12` `clippingIssues`)** | Exception native `<select>` fermé sur libellé `34` caractères à `32px` (`390x844` zoom `200%`) sans débordement carte/page ; zoom navigateur natif OS à contrôler sur matériel réel |
| **1.4.10 Redistribution (Reflow)** | AA | Viewports `320x700` à `1920x1080` + `640x400` sur les `14` routes publiques et `/exploitation` RBAC | **`0 / 360` `docOverflowX` (`scrollWidth === vw`)**, `0 / 360` `boxOverflows` | Ruban horizontal `.eco-chapternav-scroll` et tableaux `overflow-x-auto` défilables volontairement |
| **1.4.11 Contraste non textuel & `:focus-visible`** | AA | Boutons statuts `emerald-800` / `amber-800` / `red-800` (Light) & `-300` (Dark), bordures `--border-default` et contrôle `:focus-visible` (`Tab` / `Shift+Tab`) | **PASS** (`outline: 3px solid`, `0` erreur sur `360` contextes) | Modes OS `prefers-contrast: more` et Windows `forced-colors` non simulés |
| **1.4.12 Espacement du texte** | AA | Styles calculés sur `.type-body` (`16/17px`, `lh 1.55/1.60`, `ls 0em`) et `.type-body-compact` | **PASS** (`line-height >= 1.5x`, `letter-spacing: 0em`) | Surcharge utilisateur par feuille CSS externe (`2x` interlignage, `0.12em` lettres) non injectée |
| **1.3.1 / 2.1.1 / 2.1.2 / 2.4.3 / 4.1.2 Clavier, Modales, `inert` & ARIA** | A / AA | Tests Playwright automatisés (**`9 / 9` PASS**) sur `Navbar` (drawer mobile + dropdown daltonisme `Escape` + retour focus), `Tab`/`Shift+Tab` `:focus-visible`, `AhalaShowcase` (`ArrowRight`/`ArrowLeft`), `DigitalEcoPass` (`inert` + `aria-hidden` + `0` fuite `Tab` sur `12` pressions Recto/Verso + transfert `Enter`), `RangerDashboard` Modales 1/2/3 (`role="dialog"`, `aria-modal="true"`, `aria-labelledby`, piège `Tab`, `Escape` + retour focus), `ColorAtlasDrawer` (`Escape`) | **PASS (`9 / 9`)** | Annonce vocale effective au lecteur d'écran à valider manuellement avec NVDA / VoiceOver |
| **2.5.8 Taille de cible tactile** | AA | Audit Playwright de tous contrôles HTML autonomes sur `vw <= 1024px` (`320`, `360`, `390`, `430`, `640`, `768`, `1024`) | **`0 / 360` défaut (`touchUnder44 = 0`)** (y compris `BookingWizard` checkbox Charte `shrink-0` dans `<label>` `>= 44px`) | Liens prose inline `tel:`/`mailto:` exemptés WCAG 2.5.8 *Inline* et marqueurs SVG `InteractiveTopoMap` compensés par boutons HTML `>= 44px` |
| **1.4.1 / Daltonisme & Stabilité CLS** | - | Activation réelle `deuteranopia`, `protanopia`, `tritanopia` (`0` overflow, `0` contraste) + `PerformanceObserver` CLS sur `5` routes | **`CLS <= 0.05446`** (`/` `0.05446`, `/activites` `0.00582`, `/decouvrir` `0.00775`, `/reserver` `0.00467`, `/exploitation` `0`) | Appréciation perceptive clinique sur matériel réel non substituée par simulation matricielle |

---

## 2. Éléments Réellement Non Testés (Vérifications Manuelles Requises Avant Fusion)

Les points suivants n'ont **pas** été exécutés dans la passe Playwright Chromium automatisée et restent **à vérifier manuellement** :

### A. Lecteurs d'écran réels (NVDA / JAWS / VoiceOver / TalkBack)
- [ ] **NVDA (Windows) & VoiceOver (macOS/iOS)** : vérifier l'annonce vocale réelle du `HeroCanopy`, des 4 boutons `.bento-plus-btn` (`aria-expanded`), des onglets `AhalaShowcase` (`role="tablist"`), du ruban d'étapes `BookingWizard` et des erreurs `aria-describedby` à l'étape 2.
- [ ] **DigitalEcoPass & Modales `RangerDashboard`** : confirmer au lecteur d'écran que la face `inert` n'est jamais exposée à l'arbre d'accessibilité vocal et que le titre `aria-labelledby` des 3 modales + modale d'annulation est lu à l'ouverture.

### B. Appareils physiques, Navigateurs Non-Chromium & Préférences OS
- [ ] **Matériel physique iOS Safari (iPhone) & Android Chrome** : tester le pinch-zoom tactile, l'absence d'auto-zoom iOS sur `<select>` (`SpeciesAtlas`, `RangerDashboard`), la fluidité tactile du Chapternav et le rendu réel des fontes sur écran physique.
- [ ] **Navigateurs non-Chromium (Firefox Gecko, Safari WebKit)** : vérifier le rendu typographique (`Barlow Semi Condensed`, `Source Sans 3`, `JetBrains Mono`), les View Transitions (ou fallback CSS) et le rendu natif de la popup `<option>` OS ouverte (`SpeciesAtlas` `"Élevage, Bassins & Flore (LC / NT)"`).
- [ ] **Modes système d'accessibilité OS (`prefers-contrast: more` & Windows High Contrast `forced-colors: active`)** : contrôler bordures, états focus, pastilles de statut et icônes SVG lorsque le système force les couleurs.
- [ ] **Audit tiers `axe-core`** *(optionnel)* : exécuter l'extension DevTools `axe` en navigateur sur les vues clés si un contrôle complémentaire externe sans ajout dans `package.json` est souhaité avant merge.
