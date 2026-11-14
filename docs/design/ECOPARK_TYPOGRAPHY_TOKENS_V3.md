# ECOPARK TYPOGRAPHY TOKENS V3 — Spécification Complète & Gouvernance Cascade CSS

- **Statut** : Proposition d'architecture soumise à validation (Phase 1 / Livrable Tâche 4)
- **Branche** : `audit/typography-accessibility-v3`
- **Référentiel amont** : [03_TYPOGRAPHY_FINDINGS.md](../ux-audit/03_TYPOGRAPHY_FINDINGS.md), [04_RESPONSIVE_AND_REFLOW_MATRIX.md](../ux-audit/04_RESPONSIVE_AND_REFLOW_MATRIX.md), Fiche mémo n°4 (`src/index.css`) et contraintes E2E (`src/utils/ecosystemE2E.test.ts:343-468`).

---

## 1. Choix Architectural : Le Modèle Hybride (`@theme` + `@layer components` `.type-*`)

Trois stratégies ont été évaluées par rapport aux constats de l'audit :

| Stratégie | Avantages | Inconvénients / Risques | Décision |
| :--- | :--- | :--- | :--- |
| **Option A : Tout Tailwind Utility** (`text-base`, `font-mono` sans `.type-*`) | Simple pour des ajustements isolés | Casse `ecosystemE2E.test.ts:392-409` (exige `.type-hero`, `.type-body`, `.type-nav`, etc.) ; duplique les `clamp()` et interlettrages sur 12 composants | **Rejetée** |
| **Option B : Classes `.type-*` hors `@layer`** *(statu quo)* | S'applique sans configuration | Override les utilitaires Tailwind (`@layer utilities`), casse `.type-footnote.font-mono` (forcé en `Source Sans 3`), oblige les **38 `!text-*`**, omet `@custom-variant dark` | **Rejetée** |
| **Option C : Modèle Hybride `@theme` + Tokens CSS + `@layer components` `.type-*`** | Préserve 100% des classes `.type-*` et des tests E2E ; permet aux utilitaires (`font-mono`, `text-*`) de fonctionner **sans `!important`** ; active `dark:*` en Tailwind v4 ; convertit tout en `rem` scalable à 200% | Nécessite une discipline de placement (`@layer base` puis `@layer components`) dans `src/index.css` | **Recommandée** |

### Directives structurelles obligatoires dans `src/index.css`

1. **Activer le variant sombre par classe et attribut** dès la ligne 2 :
   ```css
   @import "tailwindcss";
   @custom-variant dark (&:where(.dark, .dark *, [data-theme="dark"], [data-theme="dark"] *));
   ```
   *(Résout la cause racine P0-1 : `bg-emerald-50 dark:bg-emerald-950`, `text-amber-700 dark:text-amber-300`, etc. fonctionnent enfin lorsque l'utilisateur bascule en Dark alors que l'OS préfère Light.)*
2. **Envelopper `html`, `body`, `h1..h4` dans `@layer base { ... }`** et **toutes les classes `.type-*`, `.cta-*`, `.eco-*` dans `@layer components { ... }`** afin que `@layer utilities` Tailwind (`.font-mono`, `.text-[var(--on-primary)]`, etc.) conserve sa priorité nominale sans jamais recourir à `!important`.
3. **Strictement zéro `U+2013` / `U+2014`** (Loi 1 testée dans `ecosystemE2E.test.ts:346-372`, y compris dans les commentaires CSS).

---

## 2. Tokens Typographiques V3 (`:root` + `@theme`) — Échelle Complète en `rem`

### 2.1. Familles de polices (inchangées, déjà vérifiées `loaded` via `document.fonts`)

| Rôle CSS | Famille active | Seuil d'emploi (Fiche n°4) |
| :--- | :--- | :--- |
| `--font-display` / `--font-heading` | `'Barlow Semi Condensed', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | Titres & affichages **`>= 20px`** uniquement (Profils A & B) |
| `--font-sans` / `--font-body` | `'Source Sans 3', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` | Corps de texte, navigation, formulaires, et **100% du Profil C (`/exploitation`)** |
| `--font-mono` | `'JetBrains Mono', "Courier New", monospace` | Télémétrie, prix `FCFA`, horodatages, codes `ECP-*`, matrices |
| *(Correction `TrailCatalog`)* | Retrait de `font-serif` pour les sous-titres `12px` | `font-serif` pointait vers `Barlow Semi Condensed` (`< 20px` + italique synthétique) ; utiliser `--font-sans` italique `13px–14px` |

### 2.2. Paliers Typographiques Recommandés (Mobile `< 1024px` vs Desktop `>= 1024px`)

| Classe / Token | Profil | Mobile (`< 1024px`) | Desktop (`>= 1024px`) | `line-height` | `letter-spacing` | Problèmes résolus |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| `.type-hero` (`<h1>` Accueil) | **A** | `clamp(2.25rem, 1.5rem + 4.5vw, 3rem)` (`42.5px` à `320px`, `48px` à `>= 427px` ; `rem` scalable `>= 1.75x` à 200% avec `overflow-wrap: break-word`) *(alternatif anti-cassure mot : `min(3rem, 13.2vw)` mais bloque l'agrandissement à `51.5px` sur `390px`)* | `clamp(3.25rem, 5.2vw, 5rem)` (`52px..80px`) avec `max-width: 100%; overflow-wrap: break-word` | `1.08` mob / `1.05` desk | `-0.003em` / `-0.015em` | **Élimine `ancestor-clip:+113px` sur `390px` à 200% (`h1ScrollW 423 > 310`) tout en conservant le scaling WCAG 1.4.4** |
| `.type-page-title` *(nouveau, `<h1>` intérieurs)* | **B** | `clamp(1.75rem, 1.5rem + 2vw, 2.25rem)` (`28px..36px`) | `clamp(2.25rem, 2.5vw + 0.75rem, 3rem)` (`36px..48px`) | `1.14` / `1.10` | `-0.005em` | Unifie les 4 variantes disparates sur `/activites`, `/decouvrir`, `/reserver`, `/mon-espace`, `/connexion`, `/mentions-legales` |
| `.type-h2` (`<h2>` sections) | **A/B** | `2rem` (`32px`) | `clamp(2.25rem, 3.2vw, 3rem)` (`36px..48px`) | `1.15` / `1.10` | `0em` / `-0.003em` | Conserve la symétrie visuelle avec `.type-hero` |
| `.type-h3` (`<h3>` cartes majeures) | **B** | `1.3125rem` (`21px`) | `1.5rem` (`24px`) | `1.24` / `1.20` | `+0.005em` / `0em` | `Barlow Semi Condensed` (`>= 20px`), sans `!important` |
| `.type-tagline` (sous-titre Hero) | **A** | `1.25rem` (`20px`) | `1.5rem` (`24px`) | `1.25` / `1.20` | `+0.005em` / `0em` | Passe `>= 20px` dès mobile (cohérence seuil display) |
| `.type-card-title` *(nouveau, `<h3>` cartes compactes)* | **B** | `1.125rem` (`18px`) | `1.1875rem` (`19px`) | `1.30` | `0em` | Titres denses `< 20px` en `Source Sans 3` 700 (remplace `type-h3 !text-xl`) |
| `.type-body` *(corps principal)* | **B** | **`1rem` (`16px`)** *(au lieu de 15px)* | **`1.0625rem` (`17px`)** | **`1.55` mob / `1.60` desk** | **`0em`** *(au lieu de `-0.022em`)* | Atteint `>= 16px` mobile, supprime l'écrasement `-0.374px` sur `Source Sans 3` |
| `.type-body-compact` *(nouveau, cartes/listes)* | **B** | **`0.9375rem` (`15px`)** | **`1rem` (`16px`)** | **`1.50`** | **`0em`** | Remplace les **23 `!text-xs` (`12px`) / `!text-sm` (`14px`)** sur Bento, Hôtels, Sentiers |
| `.type-eyebrow` (surtitre) | **B** | `0.8125rem` (`13px`) | `0.875rem` (`14px`) | `1.30` | `+0.04em` (uppercase) / `0em` | Conserve `Source Sans 3` 600 ; augmente le minimum mobile `12 -> 13px` |
| `.type-nav` (navigation principale) | **B/C** | **`0.875rem` (`14px`)** | **`0.875rem` (`14px`)** | `1.35` | `0em` | Rehausse les liens `12px -> 14px` (élimine 517 occurrences P1) |
| `.type-chapternav` (ruban ancres) | **B** | **`0.8125rem` (`13px`)** titre + `0.75rem` (`12px`) note | **`0.8125rem` (`13px`)** titre + `0.75rem` (`12px`) note | `1.30` | `0em` | Remplace `11px` mobile / `12px` desktop ; scale à 200% |
| `.cta-pill` / `.cta-chevron` | **B** | `0.9375rem` (`15px`) | `0.9375rem` (`15px`) | `1.25` | `0em` | Conserve `min-height: 48px` ; améliore lisibilité CTA `14 -> 15px` |
| `.type-footnote` *(notes & prix)* | **B** | **`0.8125rem` (`13px`)** *(au lieu de 12px)* | **`0.8125rem` (`13px`)** | `1.42` | `0em` | En `@layer components`, respecte `.font-mono` (plus forcé en Sans 3) |
| `.type-badge` *(nouveau, remplace `text-[10px..11px]`)* | **B** | **`0.75rem` (`12px`)** | **`0.75rem` (`12px`)** | `1.33` | `+0.01em` | Plancher strict **`12px` (`0.75rem`)** sur le site public (`0` texte HTML `< 12px`) |
| `.type-cockpit-h1` *(nouveau, `/exploitation` `<h1>`)* | **C** | **`1.1875rem` (`19px`)** | **`1.1875rem` (`19px`)** | `1.26` | `-0.005em` | **Respecte strictement `< 20px` (0 `text-xl`, 0 Barlow)** tout en détachant `<h1>` de `<h2>` (`17px`) et `<h3>` (`16px`) |
| `.type-cockpit-h2` / `h3` | **C** | `1.0625rem` (`17px`) / `1rem` (`16px`) | idem | `1.30` / `1.35` | `0em` | Hiérarchie claire à 3 niveaux sous le plafond 20px |
| `.type-cockpit-kpi` | **C** | `1.125rem` (`18px`) | `1.125rem` (`18px`) | `1.20` | `0em` | Remplace `text-[18px]` figé en `rem` (`tabular-nums`) |
| `.type-cockpit-meta` | **C** | **`0.75rem` (`12px`)** *(plancher `0.71875rem` / `11.5px` exceptions axes)* | **`0.75rem` (`12px`)** | `1.35` | `0em` | Élimine les `9px` (`cumul global`) et `10px` du cockpit |

### 2.3. Justification des Écarts par Rapport aux Cibles Indicatives du Prompt Maître (Phase C)

Le tableau suivant documente explicitement chaque arbitrage où l'échelle V3 adapte la fourchette indicative du cahier des charges initial afin de respecter la densité réelle des écrans EcoPark :

| Rôle | Cible indicative Phase C | Proposition V3 | Justification technique mesurée |
| :--- | :---: | :---: | :--- |
| `.type-nav` | `15–16px` | **`14px` (`0.875rem`)** | À `1280px`, la Navbar affiche 6 liens + 3 badges/boutons sur une seule rangée (`shrink-0`) ; à `15–16px`, l'en-tête déborde dès `1280–1366px` même après abréviation des labels. `14px` respecte le seuil minimal P1 tout en préservant l'alignement horizontal sur `1280px`. |
| `.cta-pill` / `.cta-chevron` | `16px` (`bold`) | **`15px` (`0.9375rem`)**, `font-weight: 600/700` | Maintient les 2 CTAs Hero côte à côte sur mobile `>= 360px` sans étirer la hauteur des pilules au-delà de `52px`. *(Option `16px` envisageable sur `.cta-pill` principal si les libellés secondaires passent sous `.type-badge` ou empilement `flex-col`.)* |
| `.type-footnote` / Métadonnées | `14–15px` | **`13px` (`0.8125rem`)** | Suffisant pour élever les fourchettes de prix hôtels, mentions Bento et notes d'horaires au-dessus du plancher P2 (`>= 13px`) sans faire éclater les colonnes des tableaux comparatifs et cartes hôtels à `320px`. |
| `.type-badge` / Micro-étiquettes | `13–14px` | **`12px` (`0.75rem`)** | Garantit le **zéro nœud HTML `< 12px`** sur tout le site public tout en évitant la multi-ligne forcée sur les pastilles UICN, badges sentiers et compteurs `grid-cols-3`. |
| `.type-h2` / `.type-h3` (mobile) | `h2`: `28–36px`, `h3`: `22–24px` | `h2`: **`32px`**, `h3`: **`21px`** (majeur) / **`18px`** (`.type-card-title`) | Préserve la symétrie existante de la Fiche mémo n°4 (`32px` / `21px >= 20px` en `Barlow Semi Condensed`) et isole les cartes denses `< 20px` dans `.type-card-title` (`Source Sans 3` `18px–19px`). |
| `.type-cockpit-h1` | `< 20px` (Profil C) | **`19px` (`1.1875rem`)** | Seule marge disponible entre `h2` (`17px`), `h3` (`16px`) et le plafond strict `< 20px` (`ecosystemE2E.test.ts:461-464` interdit `text-xl`, `type-hero`, `Barlow_Semi_Condensed`). |

---

## 3. Tokens Sémantiques Couleur / Contraste (Complément Typographie WCAG AA/AAA)

Les contrastes mesurés `< 4.5:1` en Phase 1 résultent de trois familles de classes :
1. `text-white` sur `bg-[var(--brand-primary)]` (`2.47:1` en Dark sur `#52B788`).
2. `text-emerald-600` (`3.26:1`–`3.65:1` en Light sur `#E9F5ED`/`#FFFFFF`).
3. `text-amber-700` sur `#E9F5ED` (`4.49:1` < `4.5:1`) et boutons `-600` (`Fluide` `3.65:1`, `Balisé` `3.20:1`, `Résoudre` `4.02:1`, `Annuler` `4.26:1`).

### Table des Tokens Sémantiques Additionnels (vérifiés par `src/utils/wcagContrast.ts` + simulation daltonisme)

| Token CSS | Mode Clair (`:root`) | Contraste Light exact (`wcagContrast.ts`) | Mode Sombre (`.dark, [data-theme="dark"]`) | Contraste Dark exact (`wcagContrast.ts`) | Usage & alerte daltonisme |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--on-primary` *(existant, sous-utilisé)* | `#FFFFFF` | **`11.08:1`** sur `#1B4332` (min daltonisme `11.08:1`) | `#121614` sur `#52B788` *(existant)*<br>*(Recommandé V3 : `#081C15` sur `#74C69D`)* | **`7.38:1`** (`#121614`/`#52B788`)<br>**`8.68:1`** (`#081C15`/`#74C69D`) | **Remplace `text-white`** sur `bg-[var(--brand-primary)]`. *Note daltonisme* : `#121614` sur `#52B788` tombe à **`4.02:1`** sous deutéranopie ; `#081C15` sur `#74C69D` reste **`>= 6.04:1`** dans tous les modes. |
| `--status-open-text` *(nouveau)* | `#166534` (Emerald-800) | **`7.13:1`** (`#FFFFFF`), **`6.82:1`** (`#F6FBF8`), **`6.37:1`** (`#E9F5ED`) | `#74C69D` (Leaf-300) | **`8.96:1`** (`#121614`), **`7.73:1`** (`#1F2421`), **`6.64:1`** (`#29302C`) | Remplace `text-emerald-600` (`3.26:1`–`3.65:1`) et évite `#15803D` (`4.48:1` sur `#E9F5ED`) |
| `--status-caution-text` *(nouveau)* | `#92400E` (Amber-800) | **`7.09:1`** (`#FFFFFF`), **`6.78:1`** (`#F6FBF8`), **`6.33:1`** (`#E9F5ED`) | `#FCD34D` (Amber-300) | **`12.66:1`** (`#121614`), **`10.93:1`** (`#1F2421`), **`9.38:1`** (`#29302C`) | Remplace `text-amber-700` (`#B45309` = **`4.48:1`** mesuré/calculé sur `#E9F5ED`) |
| `--status-danger-text` *(nouveau)* | `#991B1B` (Red-800) *(ou `#B91C1C` `5.78:1` sur `#E9F5ED`)* | **`8.31:1`** (`#FFFFFF`), **`7.42:1`** (`#E9F5ED`) | `#FCA5A5` (Red-300) | **`9.62:1`** (`#121614`), **`8.30:1`** (`#1F2421`), **`7.12:1`** (`#29302C`) | Erreurs formulaires, statut fermé, annulation (`#DC2626` rejeté : `4.31:1` sur `#E9F5ED`) |
| Bouton statut `Fluide` / `Check-In` | `bg-emerald-800 text-white` (`#065F46`) | **`7.68:1`** (`#FFFFFF` sur `#065F46`, min daltonisme `7.68:1`) | `dark:bg-emerald-300 dark:text-[#081C15]` *(ou `#74C69D` / `#081C15`)* | **`8.68:1`** (`#081C15` sur `#74C69D`, min daltonisme **`6.04:1`**) | Remplace `bg-emerald-600 text-white` (`3.65:1`) |
| Bouton statut `Balisé` / Staff | `bg-amber-800 text-white` (`#92400E`) | **`7.09:1`** (`#FFFFFF` sur `#92400E`, min daltonisme **`4.69:1`**) | `dark:bg-amber-300 dark:text-[#121614]` (`#FCD34D`) | **`12.66:1`** sur `#121614` (`9.38:1` sur `#29302C`) | Remplace `bg-amber-600 text-white` (`3.20:1`) et évite `bg-amber-700` (`3.17:1` sous deutéranopie) |
| Bouton `Annuler` / Destructif | `bg-red-800 text-white` (`#991B1B`) | **`8.31:1`** (`#FFFFFF` sur `#991B1B`, min daltonisme **`5.15:1`**) | `dark:bg-red-300 dark:text-[#121614]` (`#FCA5A5`) | **`9.62:1`** sur `#121614` | Remplace `bg-red-600` (`4.26:1` / `4.02:1`) et évite `bg-red-700` qui chute à **`3.79:1`** sous deutéranopie (`< 4.5:1`) |

> **Rappel AAA existant** : `--text-muted` reste strictement `#36403A` (Light, `9.61:1` sur `#E9F5ED` et `10.76:1` sur `#FFFFFF`) et `#C9D1CC` (Dark, `10.11:1` sur `#1F2421` et `8.67:1` sur `#29302C`) pour satisfaire `ecosystemE2E.test.ts:416-420`.

---

## 4. Garde-fous Zoom 200%, Contrôles Formulaires & Tactile (`44x44px` / `48x48px`)

1. **Garde-fou Anti-Clip Hero (Zoom 200% WCAG 1.4.4)** :
   - Mesure Phase 1 sur `390x844` sous `html { font-size: 32px }` : `.type-hero` passe à **`96px`**, portant la largeur du mot `"écologique"` / `"Complexe"` à `423px` dans une colonne utile de `310px` (`ancestor-clip:+113px` causé par l'`overflow-hidden` de `ImmersiveSection.tsx`).
   - **Arbitrage recommandé** : utiliser `clamp(2.25rem, 1.5rem + 4.5vw, 3rem)` + `overflow-wrap: anywhere; hyphens: auto;` et retirer l'`overflow-hidden` destructeur autour du flux textuel de `HeroCanopy` / `ImmersiveSection` (ou passer à `overflow-x: clip` en réduisant le padding latéral mobile de `px-10` à `px-4 sm:px-8` sous zoom). À l'inverse, `min(3rem, 13.2vw)` empêche mécaniquement tout débordement de mot sur `390px` mais bloque `.type-hero` à `51.48px` (`+7%` seulement au lieu de `200%`), enfreignant l'esprit de WCAG 1.4.4.
2. **Garde-fou `<select>` Anti-Overflow Mobile (`+132px` / `+226px`)** :
   - Tout `<select>` cohabitant avec le garde-fou iOS (`src/index.css:338`: `font-size: max(1rem, 16px) !important` sous `1024px`) doit avoir `min-w-0 max-w-full` (et `flex-1` / `w-full sm:w-auto` dans un parent `flex-wrap min-w-0`) afin que ses `<option>` longues ne forcent jamais le dépassement de la carte parente.
3. **Garde-fou Cibles Tactiles `44px–48px`** :
   - `.touch-target-44` (`min-width: 44px; min-height: 44px;`) pour les filtres denses, steppers `-`/`+` et boutons carte/tableaux ; `.touch-target-48` conservée pour la navigation principale, CTA primaires, Bento `+` et Cockpit Pro (`RangerDashboard`).

---

## 5. Gouvernance des Fichiers Tokens & Sources Dormantes

| Fichier | Rôle actuel | Action recommandée en Phase 2 |
| :--- | :--- | :--- |
| `src/index.css` | **Source Unique de Vérité (Runtime Vite)** | Recevra `@custom-variant dark`, `@layer base/components`, et les tokens typographiques/contrastes V3 |
| `styles/theme.css` | Dormant (divergent sur `--text-muted`) | Aligner `--text-muted` (`#36403A` / `#C9D1CC`) et ajouter un commentaire d'en-tête indiquant que `src/index.css` fait foi en production (ou supprimer s'il n'est référencé nulle part après validation) |
| `tokens/color-tokens.json` | Documentation JSON W3C | Synchroniser `--text-muted` et ajouter un nœud `typography` reflétant les paliers V3 |
| `tailwind.config.js` | Dormant (héritage Tailwind v3) | Marquer comme archive/référence IDE ou supprimer après confirmation utilisateur (Tailwind v4 lit uniquement `@theme` / `@custom-variant` dans `src/index.css`) |
