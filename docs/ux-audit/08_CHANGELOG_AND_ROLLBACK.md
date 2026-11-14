# 08 - Changelog & Procédure de Rollback (Audit V3)

- **Branche isolée** : `audit/typography-accessibility-v3`
- **Branche parente intacte** : `feat/react-adobe-color-ahala` (point de départ `6157dd7`, aucun merge vers `feat/react-adobe-color-ahala` ou `main`, aucun déploiement effectué)
- **Commits Phase 1 déjà enregistrés sur la branche** :
  - `68c2465` - `docs(ux-audit): add V3 typography & responsive audit deliverables and baseline screenshots`
  - `e7aaa03` - `docs(ux-audit): synchronize Phase 1 findings, 430x932/1024/1280 measurements, and V3 gate specs`
- **Périmètre des modifications applicatives (Phase 2 & Phase 3)** : **23 fichiers modifiés** (`src/`, `styles/`, `tokens/`, `tailwind.config.js`), **0 ajout npm** (`package.json` intact), **0 donnée métier altérée** (tarifs FCFA, horaires, contacts, routes et logo officiels inchangés), **59 captures** archivées dans `docs/ux-audit/screenshots/after/`.

---

## 1. Changelog Exhaustif par Lot

### Lot 1 - Socle CSS, Cascade Tailwind v4 & Design Tokens
- **`src/index.css`** :
  - Ajout de `@custom-variant dark (&:where(.dark, .dark *, [data-theme="dark"], [data-theme="dark"] *));` en ligne 2 pour rétablir tous les utilitaires `dark:*` lorsque l'OS est en Light.
  - Mise à jour de `--brand-primary` (`#74C69D`) et `--on-primary` (`#081C15`) en mode sombre (`8.68:1`, minimum `6.04:1` sous simulation daltonisme), tout en préservant `--text-muted` AAA (`#36403A` Light `10.29:1` / `#C9D1CC` Dark `11.71:1`).
  - Ajout des tokens sémantiques `--status-open-text`, `--status-caution-text` et `--status-danger-text` (Light `#166534` / `#92400E` / `#991B1B` ; Dark `#74C69D` / `#FCD34D` / `#FCA5A5`).
  - Encapsulation de `html`, `body`, `h1..h4` dans `@layer base` et de toutes les classes typographiques / CTA / utilitaires UX dans `@layer components`, rétablissant la priorité de `@layer utilities` (notamment `.font-mono` -> `JetBrains Mono`).
  - Normalisation V3 en `rem` : `.type-hero` mobile fluide (`clamp(2.25rem, 1.5rem + 4.5vw, 3rem)` + `overflow-wrap: break-word`, sans `hyphens: auto`), `.eco-container` (`padding-inline: clamp(16px, 2vw, 2.5rem)` évitant une sur-marge `64px` sous zoom `200%` `390x844` afin de garder `"écologique"` entier), `max-width: 100%` sur `.cta-chevron`, `.type-page-title`, `.type-card-title`, `.type-body` (`16px` mobile / `17px` desktop, `lh 1.55/1.60`, tracking `0em`), `.type-body-compact`, `.type-nav` (`14px`), `.type-chapternav` (`13px`), `.type-footnote` (`13px`), `.type-badge` (`12px`), et échelle cockpit Profil C `.type-cockpit-h1` (`19px`), `h2` (`17px`), `h3` (`16px`), `kpi` (`18px`), `meta` (`12px`).
- **`styles/theme.css`**, **`tokens/color-tokens.json`**, **`tailwind.config.js`** :
  - Alignés documentairement avec `src/index.css` (SSoT runtime Tailwind v4) : tokens `--on-primary`, `--text-muted`, `--status-*-text` et échelle `typography.scaleRem` V3 ajoutés ; commentaire d'avertissement sur `tailwind.config.js`. *(Note Loi 1 : `ecosystemE2E.test.ts` contrôle `index.html` et `src/` à `0` `\u2013`/`\u2014`, et tous les reliquats `\u2014` dans `styles/theme.css` et `tokens/color-tokens.json` ont également été remplacés par `-` : `0` `\u2013`/`\u2014` sur `index.html`, `src/`, `styles/`, `tokens/` et `tailwind.config.js`.)*

### Lot 2 - Parcours Public, En-tête, Pied de page & Conversion
- **`src/components/layout/Navbar.tsx`** : suppression de `truncate` sur Temps 1 (`Garantie Météo RN3`) avec `flex-wrap` + `basis-[260px]` ; suppression des coupures sur la marque `ECOPARK CAMEROUN` / `POSTE EXPLOITATION RN3` à `320px` et `1280-1440px` + `min-w-[168px]` et garde logo `max-w-[44px] max-h-[44px]` pour éviter l'écrasement à zoom 200% (`390px` / `1440px`) ; fermeture via `Escape` sur `#mobile-nav-drawer` et sur le menu daltonisme (plus fermeture au clic extérieur) avec restauration du focus vers le bouton déclencheur ; plancher `12px` et cibles `>= 44px`.
- **`src/components/layout/Footer.tsx`** : correction du débordement `1024x768` (`24h/24 - 7j/7`), espacement `"Hôtels Ewondo / Chanthel / Bene"` pour prévenir tout débordement `body.scrollWidth` à zoom `200%` (`390px`/`1440px`), remplacement du titre figé par `1.3125rem` scalable, cibles tactiles `min-h-[44px]` sur liens téléphone/e-mail sous `<= 1024px`, `overflow-x-clip` sur `<footer>` et `min-w-0 break-words` sur les colonnes `1-3` pour supprimer tout débordement `body.scrollWidth` à zoom 200% (`/reserver`, `/tarifs`).
- **`src/components/layout/ImmersiveSection.tsx`** & **`src/components/discovery/HeroCanopy.tsx`** : bascule d'`overflow-hidden` bloquant vers un confinement sans `ancestor-clip` sur le Hero `<h1>` à `390x844` zoom 200%, ajout de `flex-wrap` sur l'en-tête télémétrie `HeroCanopy.tsx` contre tout chevauchement sous zoom `200%` (`1440x900`), suppression de `truncate` sur les 3 légendes photo et suppression des `!text-*` ; conservation stricte du contrat `<h1>` `.type-hero` / `.cta-pill` / `.cta-chevron`.
- **`src/components/discovery/ImpactBanner.tsx`** : suppression des `6` `!important`, migration vers `.type-h3` / `.type-card-title`, `.type-body-compact` et `.type-footnote` tout en préservant `.bento-plus-btn`, `aria-expanded` et les 4 blocs `bluf:`.
- **`src/components/discovery/AhalaShowcase.tsx`** : retrait de `truncate` sur `hotel.priceRange` et sur titres tronqués, ajout de `min-w-0 max-w-full` et retrait de `shrink-0` sur la rangée `role="tablist"`, navigation clavier WAI-ARIA Tabs (`ArrowLeft`/`ArrowRight`/`ArrowUp`/`ArrowDown`/`Home`/`End` + `tabIndex` dynamique et `aria-labelledby`), retrait de `shrink-0` sur le conteneur CTA `WhatsApp Hôtels` (`max-w-full`, fin du débordement `1485px > 1440px` sous zoom `200%`), suppression des `23` `!text-*`, onglets `min-h-[44px]`, et maintien permanent du `<table id="pass-comparateur">` / `#cross-sell-options`.
- **`src/components/booking/BookingWizard.tsx`** : remplacement des couleurs faible contraste (`text-emerald-600`, `text-red-600`, `text-white` Dark) par `--status-open-text`, `--status-danger-text`, `--on-primary` ; steppers `-`/`+` portés à `44x44px` minimum ; checkbox Charte `shrink-0` (`16x16px` dans `<label>` `>= 44px`) ; enveloppement propre du ruban étapes `1-2-3` sous zoom 200% `390px` ; `font-sans` explicite sur titres `<h4>` et sous-titres tarifaires `< 20px`.
- **`src/components/booking/DigitalEcoPass.tsx`** & **`src/components/booking/Co2BotanicalSprout.tsx`** : isolation clavier stricte entre faces Recto et Verso 3D via `.inert` DOM natif + attribut HTML `inert` et `aria-hidden` synchronisés (0 fuite `Tab` vers la face masquée, transfert propre du focus Recto <-> Verso via `Enter`, `aria-pressed` sur le bouton toggle, modale d'annulation en `role="dialog" aria-modal="true" aria-labelledby="ecopass-cancel-title"` + `Escape`), contraste CO2 via `--status-open-text`, boutons Dark via `--on-primary`, retrait de `!text-white`, boutons tactiles `min-h-[44px]`, mode `OLED` avec tuiles internes sombres cohérentes et badges `>= 12px`.

### Lot 3 - Cartographie, Catalogue, Biodiversité, Sentinelle, Auth, Légales & Cockpit
- **`src/App.tsx`** : unification des `<h1>` secondaires via `.type-page-title` et `/exploitation` (`unauth`/`403`) via `.type-cockpit-h1` ; correction contrastes `text-amber-700` -> `--status-caution-text` et `text-white` -> `text-[var(--on-primary)]` ; suppression `line-clamp-2`/`truncate` et `!important` sur cartes sentiers Accueil ; ajout d'`overflow-x-clip` sur le conteneur principal applicatif (zoom 200% `scrollWidth === vw`) et `min-h-[70vh]` / `min-h-screen` sur les conteneurs de chargement `isAuthLoading` (`/mon-espace`, `/exploitation`) réduisant le CLS de `/exploitation` de `0.65414` à `0`.
- **`src/components/biodiversity/SpeciesAtlas.tsx`** : ajustement filtres (`p-2.5 sm:p-5`, `<select>` UICN `appearance-none pl-[8px] pr-[22px] sm:pl-2.5 sm:pr-7` + chevron `aria-hidden`, libellés métier intacts dont `"Élevage, Bassins & Flore (LC / NT)"` tenant avec marge positive à `320x700` `+1.74px`, `390x844` `+68.94px`, `1440x900` `+0.98px` et `0` débordement page/carte à `390x844` zoom `200%`), ajout de `max-w-full text-left` sur les boutons catégories/sentiers (`zoom 200%`), correction `bg-emerald-50` Dark et pilules header (`bg-[#1F2421]/75 text-[#E9F5ED]`), wrap de la ligne titre + badge UICN, passage à `.type-page-title` et cibles `min-h-[44px]`.
- **`src/components/map/InteractiveTopoMap.tsx`** & **`src/components/map/ElevationProfile.tsx`** : barre `Calques` en `flex-wrap max-w-full` (fin des débordements `320-430px`), contrôles zoom/simulateur HTML en `>= 44x44px` jusqu'à `<= 1024px` (`xl:min-h-[36/38px]` au lieu de `sm:min-h-[...]`), retrait de `scale-[1.02]` débordant dans `ElevationProfile`, encadré info élargi `156x42` et tous les `<text>` SVG (`28` dans `InteractiveTopoMap` + `15` dans `ElevationProfile`) rehaussés de `11px` à `>= 12px`.
- **`src/components/trails/TrailCatalog.tsx`** : correction `Avis Éco-Garde` et badges `obs. terrain` via `--status-caution-text` et `dark:*`, retrait de `line-clamp-3` et de `font-serif italic` sous `20px` (remplacé par `font-sans italic`), description relevée en `.type-body-compact`, barre d'actions en `flex-wrap` (zoom 200%) et cibles `>= 44px` jusqu'à `1024px` (`xl:min-h-[32/36px]`).
- **`src/components/field/CitizenSentinel.tsx`** : passage des métadonnées `10px/11px` à `12px` (`0.75rem`), boutons actifs Dark en `--on-primary`, cibles `>= 44px` jusqu'à `1024px` (`xl:min-h-[36px]`) et empilement `flex-col sm:flex-row w-full sm:w-auto` sur les 3 `<select>` du flux communautaire (fin de l'écrasement à `26px` sur `390x844`).
- **`src/components/auth/AuthPortal.tsx`** & **`src/components/legal/LegalNoticeView.tsx`** : passage de `Ouvrir le Cockpit Pro` à `bg-amber-800 text-white` (`7.09:1`), titre de carte en `type-cockpit-h2` (`17px` `Source Sans 3`) lorsque `mode === 'staff_login'` sur `/exploitation` (respect strict Profil C `< 20px` et hiérarchie `h1 19px > h2 17px`), labels `--status-caution-text`, lien `"Mot de passe oublié ?"` en `min-h-[44px]`, sortie du `<button>` `"Lire la Politique de Confidentialité (Loi n° 2010/012)"` hors du `<label>` avec `min-h-[44px]`, `<h1>` `.type-page-title`, et corps juridique complet `LegalNoticeView` (paragraphes + listes) élevé vers `.type-body` (`16-17px`, `lh 1.55-1.60`).
- **`src/components/admin/RangerDashboard.tsx`** : refonte Profil C strictement `< 20px` en `Source Sans 3` / `JetBrains Mono` (`.type-cockpit-h1` `19px`, `h2` `17px`, `h3` `16px`, `kpi` `18px`, `meta` `12px`, `0` `text-xl`, `0` `Barlow`), ARIA complet sur les `3` modales (`role="dialog"`, `aria-modal="true"`, `aria-labelledby`, piège `Tab`/`Shift+Tab`, fermeture `Escape` et restauration du focus déclencheur), reflow zoom `200%` `390x844` (header session `flex-col sm:flex-row`, anneau CO2 `max-w-full aspect-square`, badges et lignes sentiers `flex-wrap max-w-full`), empilement propre des `<select>` Sentier/Catégorie sur mobile, jauge quota `<input type="range">` et boutons filtres en `>= 44px` jusqu'à `<= 1024px` (`xl:min-h-[32/36px]`), retrait de `line-clamp-1`, `28` labels `<text>` de l'histogramme SVG passés de `11px` à `12px`, et boutons statuts haute accessibilité (`emerald-800`, `amber-800`, `red-800` Light / `-300` Dark).
- **`src/components/design-system/ColorAtlasDrawer.tsx`** : plancher `12px`, footnote conforme, contraste `#scales` calculé sur les 5 familles Light/Dark avec fallback encre `#000000` (`4.80:1` sur `earth-500` `#A46E3B`), clé React composite `key={`${activeScaleFamily}-${st.step}`}` évitant tout réemploi transitoire DOM lors du changement d'onglet, puces d'échelon opaques, activation clavier (`role="button" tabIndex={0}`), et onglet `#tester` corrigé (`44x44px` sur inputs couleur/hex, `<h4>` `font-sans`, retrait de `truncate` sur `"Achromatopsie (Niveaux de gris)"`).

### Phase 3 - Passe Unifiée Finale, Tests, Captures & Rapports
- **Tests conservés sans modification** : `src/utils/ecosystemE2E.test.ts` inchangé (`# tests 37 / # pass 37` répartis sur `10` blocs `node:test`, `# fail 0`) ; `npx tsc -p tsconfig.app.json --noEmit` et `npm run build` verts.
- **Passe Playwright unifiée finale sur build `dist/` + `vite dev`** : `360` contextes (`308` public, `12` zoom `200%`, `15` interactifs, `11` cockpit RBAC/modale, `14` `ColorAtlasDrawer` DEV), **`0` erreur console/page/contraste/clipping/boxOverflow/docOverflowX/touchUnder44/cockpitOver20/cockpitBarlow**, **`9/9` tests clavier**, **`3/3` modes daltonisme**, **`CLS <= 0.05446`**, **`59` PNG** régénérés dans `docs/ux-audit/screenshots/after/`.
- **Livrables Phase 3 ajoutés & mis à jour** : `docs/ux-audit/06_BEFORE_AFTER_VISUAL_QA.md`, `docs/ux-audit/07_WCAG_MANUAL_CHECKLIST.md`, `docs/ux-audit/08_CHANGELOG_AND_ROLLBACK.md`, `docs/ux-audit/screenshots/after/` (`59 PNG`), et mise à jour de `typography-audit-v3-plan.md`.
- **Fichiers temporaires supprimés & serveurs arrêtés** : scripts et rapports temporaires (`_tmp*`, `verify_*`, `__pycache__`) supprimés avant clôture ; serveurs `vite preview` et `vite dev` arrêtés.

---

## 2. Procédures de Rollback Sécurisées

### Option A - Rollback d'un composant ou d'un lot ciblé (avant commit Phase 2/3)
```powershell
# Revenir à la baseline Phase 1 sur un fichier spécifique (ex: RangerDashboard)
git restore --source=e7aaa03 -- src/components/admin/RangerDashboard.tsx

# Revenir uniquement sur tout le Lot 1 tokens/CSS
git restore --source=e7aaa03 -- src/index.css styles/theme.css tailwind.config.js tokens/color-tokens.json
```

### Option B - Annuler un commit complet après validation (si commit déjà effectué)
```powershell
git log --oneline -n 5
git revert <commit-hash-phase2-ou-phase3>
```

### Option C - Abandonner l'intégralité de la branche d'audit sans risque
La branche de travail `feat/react-adobe-color-ahala` n'a reçu aucune modification pendant l'audit :
```powershell
git checkout feat/react-adobe-color-ahala
git branch -D audit/typography-accessibility-v3
```
*(Si un rebuild production est souhaité après rollback : exécuter `npm test && npm run build`.)*
