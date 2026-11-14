# 08 - Changelog & Procédure de Rollback (Audit V3)

- **Branche isolée** : `audit/typography-accessibility-v3`
- **Branche parente intacte** : `feat/react-adobe-color-ahala` (`5f43b08`, aucune fusion vers `feat/react-adobe-color-ahala` ou `main`, aucun `git push`, aucun déploiement effectué)
- **Commits historiques déjà présents sur la branche** :
  - `68c2465` - `docs(ux-audit): add V3 typography & responsive audit deliverables and baseline screenshots`
  - `e7aaa03` - `docs(ux-audit): synchronize Phase 1 findings, 430x932/1024/1280 measurements, and V3 gate specs`
  - `a33e34f` - `feat(a11y-v3): complete Phase 2 & 3 typography, WCAG contrast, keyboard/ARIA & 360-context QA` *(repris et complété par le commit final unifié ci-dessous)*
- **Périmètre des modifications applicatives (Phase 2 & Phase 3 cumulées depuis `5f43b08`)** : **23 fichiers modifiés** (`src/`, `styles/`, `tokens/`, `tailwind.config.js`), **0 ajout npm** (`package.json` intact), **`src/utils/` intact**, **`src/data/` / tarifs FCFA / horaires / contacts / libellés métier intacts**, **`59` captures** régénérées dans `docs/ux-audit/screenshots/after/`.

---

## 1. Changelog Exhaustif par Lot

### Lot 1 - Socle CSS, Cascade Tailwind v4 & Design Tokens
- **`src/index.css`** :
  - Ajout de `@custom-variant dark (&:where(.dark, .dark *, [data-theme="dark"], [data-theme="dark"] *));` en ligne 2 pour rétablir tous les utilitaires `dark:*` lorsque l'OS est en Light.
  - Mise à jour de `--brand-primary` (`#74C69D`) et `--on-primary` (`#081C15`) en mode sombre (`8.68:1`), tout en préservant `--text-muted` AAA (`#36403A` Light `10.29:1` / `#C9D1CC` Dark `11.71:1`).
  - Ajout des tokens sémantiques `--status-open-text`, `--status-caution-text` et `--status-danger-text` (Light `#166534` / `#92400E` / `#991B1B` ; Dark `#74C69D` / `#FCD34D` / `#FCA5A5`).
  - Encapsulation de `html`, `body`, `h1..h4` dans `@layer base` et des classes typographiques / CTA / utilitaires UX dans `@layer components`, rétablissant la priorité de `@layer utilities` (dont `.font-mono` -> `JetBrains Mono`).
  - Normalisation V3 en `rem` : `.type-hero` mobile fluide (`clamp(2.25rem, 1.5rem + 4.5vw, 3rem)` + `overflow-wrap: break-word`), `.eco-container`, `max-width: 100%` sur `.cta-chevron`, `.type-page-title`, `.type-card-title`, `.type-body` (`16px` mobile / `17px` desktop, `lh 1.55/1.60`, tracking `0em`), `.type-body-compact`, `.type-nav` (`14px`), `.type-chapternav` (`13px`), `.type-footnote` (`13px`), `.type-badge` (`12px`), et échelle cockpit Profil C `.type-cockpit-h1` (`19px`), `h2` (`17px`), `h3` (`16px`), `kpi` (`18px`), `meta` (`12px`).
- **`styles/theme.css`**, **`tokens/color-tokens.json`**, **`tailwind.config.js`** :
  - Synchronisation documentaire avec `src/index.css` (SSoT runtime Tailwind v4) : tokens `--on-primary`, `--text-muted`, `--status-*-text` et échelle `typography.scaleRem` V3 ajoutés ; avertissement ajouté sur `tailwind.config.js` ; `0` `\u2013`/`\u2014` (`Loi 1`).

### Lot 2 - Parcours Public, En-tête, Pied de page & Conversion
- **`src/components/layout/Navbar.tsx`** : suppression de `truncate` sur Temps 1 (`Garantie Météo RN3`) avec `flex-wrap` + `basis-[260px]` ; garde logo `max-w-[44px] max-h-[44px]` ; retrait de `flex-1`, `min-w-[168px]` et `overflow-x-clip` sur le bouton marque avec `min-w-0 max-w-full break-words` pour permettre aux boutons d'action de passer dessous sous zoom `200%` (`390x844`) et `zoom: 2` sans jamais couper `"ECOPARK CAMEROUN"` ni déborder du parent ; fermeture via `Escape` sur `#mobile-nav-drawer` et sur le menu daltonisme (plus clic extérieur) avec restauration du focus déclencheur ; plancher `12px` et cibles `>= 44px`.
- **`src/components/layout/Footer.tsx`** : correction du débordement `1024x768`, espacement `"Hôtels Ewondo / Chanthel / Bene"`, titre en `1.3125rem`, cibles `min-h-[44px]` sous `<= 1024px`, `overflow-x-clip` sur `<footer>` et `min-w-0 break-words` sur colonnes `1-3`.
- **`src/components/layout/ImmersiveSection.tsx`** & **`src/components/discovery/HeroCanopy.tsx`** : confinement sans clipping sur Hero `<h1>` à zoom `200%`, `flex-wrap` sur l'en-tête télémétrie, retrait de `truncate` et `!text-*`, conservation stricte de `<h1>` `.type-hero` / `.cta-pill` / `.cta-chevron`.
- **`src/components/discovery/ImpactBanner.tsx`** : retrait des `!important`, migration vers `.type-h3` / `.type-card-title`, `.type-body-compact` et `.type-footnote` tout en préservant `.bento-plus-btn`, `aria-expanded` et les 4 blocs `bluf:`.
- **`src/components/discovery/AhalaShowcase.tsx`** : retrait de `truncate` et `!text-*`, `min-w-0 max-w-full`, navigation clavier WAI-ARIA Tabs (`ArrowLeft`/`ArrowRight`/`ArrowUp`/`ArrowDown`/`Home`/`End` + `tabIndex` dynamique et `aria-labelledby`), onglets `min-h-[44px]` et maintien de `#pass-comparateur` / `#cross-sell-options`.
- **`src/components/booking/BookingWizard.tsx`** : tokens contraste `--status-open-text`, `--status-danger-text`, `--on-primary` ; steppers `44x44px` ; checkbox Charte `shrink-0` dans `<label> >= 44px` ; ruban étapes `flex-wrap`.
- **`src/components/booking/DigitalEcoPass.tsx`** & **`src/components/booking/Co2BotanicalSprout.tsx`** : isolation clavier stricte Recto <-> Verso 3D via `.inert` DOM natif + attribut HTML `inert` + `aria-hidden` synchronisés dans `useEffect` à chaque changement d'état (y compris transition pass vide -> pass actif, sans liste de dépendances restrictive), `0` fuite `Tab`, transfert ordonné du focus lors du basculement, `aria-pressed` sur le bouton toggle, et modale d'annulation `role="dialog" aria-modal="true" aria-labelledby="ecopass-cancel-title"` + `Escape`.

### Lot 3 - Cartographie, Catalogue, Biodiversité, Sentinelle, Auth, Légales, Atelier & Cockpit
- **`src/App.tsx`** : unification `.type-page-title` et `/exploitation` (`.type-cockpit-h1`) ; contrastes `--status-caution-text` / `--on-primary` ; `overflow-x-clip` sur le wrapper principal ; `min-h-[70vh]` sur `/mon-espace` et clés React distinctes (`ranger-loading`, `ranger-login`, `ranger-403`, `ranger-dashboard`) + `min-h-screen` sur toutes les branches de `/exploitation` réduisant le CLS de `/exploitation` de `0.25775` à **`0.00034`**.
- **`src/components/biodiversity/SpeciesAtlas.tsx`** : ajustement filtres (`p-2.5 sm:p-5`, wrapper `sm:min-w-[260px]`, `<select>` UICN `appearance-none pl-[8px] pr-[22px] sm:pl-2.5 sm:pr-7` + chevron `aria-hidden`, libellé `"Élevage, Bassins & Flore (LC / NT)"` intact tenant avec marge libre à `320x700` `+1.55px`, `390x844` `+68.55px`, `1440x900` `+27.98px`), `bg-emerald-50` Dark corrigé, `.type-page-title` et cibles `min-h-[44px]`.
- **`src/components/map/InteractiveTopoMap.tsx`** & **`src/components/map/ElevationProfile.tsx`** : barre `Calques` `flex-wrap`, contrôles zoom `>= 44x44px` jusqu'à `1024px`, retrait `scale-[1.02]`, encadré info élargi `156x42`, tous `<text>` SVG portés à `>= 12px`, et halo `#141816` (`strokeWidth="3" paintOrder="stroke"`) sur le `"N"` de la boussole (`17.92:1` vs `2.47:1`).
- **`src/components/trails/TrailCatalog.tsx`** : badges `--status-caution-text`, retrait `line-clamp-3`, passage des deux `<select>` (`Secteur` et `Statut`) à `w-full sm:w-auto sm:flex-initial` pour éliminer la compression à `68px` sous `320x700` / `360x800` et le clipping sous `zoom 200%`, cibles `>= 44px` jusqu'à `1024px`.
- **`src/components/field/CitizenSentinel.tsx`** : métadonnées `>= 12px`, boutons Dark en `--on-primary`, cibles `>= 44px` jusqu'à `1024px`, `flex-col sm:flex-row` sur les `3` `<select>`.
- **`src/components/auth/AuthPortal.tsx`** & **`src/components/legal/LegalNoticeView.tsx`** : bouton `Ouvrir le Cockpit Pro` `bg-amber-800 text-white` (`7.09:1`), titre `mode === 'staff_login'` en `.type-cockpit-h2` (`17px` `Source Sans 3`), lien `"Mot de passe oublié ?"` `min-h-[44px]`, bouton confidentialité sorti du `<label>`, et corps juridique `.type-body` (`16-17px`).
- **`src/components/admin/RangerDashboard.tsx`** : refonte Profil C `< 20px` en `Source Sans 3` / `JetBrains Mono` ; ARIA complet sur les `3` modales (`role="dialog"`, `aria-modal="true"`, `aria-labelledby`, `<label htmlFor>` / `id` sur `closure-reason-input` et `intervention-note-input`, piège `Tab`/`Shift+Tab`, `Escape`, restauration du focus déclencheur et repli explicite vers `#sentinel-moderation` `<h2>` lorsque le bouton de Modale 2 est démonté après résolution ; retrait de `focus:outline-none` sur les `textarea`) ; notice Modale 1 à `14px` (`text-sm`) ; en-tête carte `"Carte ->"` avec `flex-wrap gap-1 min-w-0` et `<select>` `reportTrailFilter` passé à `w-full sm:w-auto sm:flex-initial` + `aria-label` (fin du débordement sous zoom `200%` `390x844`) ; labels SVG `12px` et boutons haute accessibilité.
- **`src/components/design-system/ColorAtlasDrawer.tsx`** : plancher `12px`, encre fallback `#000000` sur `earth-500`, clé composite `key={`${activeScaleFamily}-${st.step}`}`, inputs `#tester` `44x44px`, gestion clavier complète sur le panneau `role="dialog"` (entrée focus sur ouverture, piège `Tab`/`Shift+Tab`, `Escape` en phase capture avec `stopImmediatePropagation`, restauration focus déclencheur, `type="button"` sur fermeture).

### Phase 3 - Passe Unifiée Finale, Tests, Captures & Rapports
- **Tests unitaires & E2E inchangés (`package.json` & `src/utils/` intacts)** : **`37/37` sous-tests (`10` suites `node:test`)**, `npx tsc -p tsconfig.app.json --noEmit` et `npm run build` verts.
- **Passe Playwright unifiée finale sur build `dist/` (`4179`) + `vite dev` (`5179`)** : **`238` contextes DOM**, **`6/6` suites clavier**, **`3/3` daltonisme**, **`CLS <= 0.05446`** (`/` `0.05446`, `/exploitation` `0.00034`), **`0/70` échec contraste texte SVG**, et **`59` PNG** régénérés dans `docs/ux-audit/screenshots/after/`.
- **Livrables Phase 3 synchronisés** : `docs/ux-audit/06_BEFORE_AFTER_VISUAL_QA.md`, `docs/ux-audit/07_WCAG_MANUAL_CHECKLIST.md`, `docs/ux-audit/08_CHANGELOG_AND_ROLLBACK.md` et `docs/ux-audit/screenshots/after/` (`59 PNG`).
- **Nettoyage & contrôle final** : suppression de tous fichiers temporaires (`_tmp*`, `verify_*`, `__pycache__`), arrêt des serveurs de test, contrôle Loi 1 (`0` `\u2013`/`\u2014`) et exécution finale de vérification sur commit propre.

---

## 2. Procédures de Rollback Sécurisées

### Option A - Rollback d'un composant ou d'un lot ciblé (depuis la baseline Phase 1 `e7aaa03`)
```powershell
# Revenir à la baseline Phase 1 sur un fichier spécifique (ex: RangerDashboard)
git restore --source=e7aaa03 -- src/components/admin/RangerDashboard.tsx

# Revenir uniquement sur le Lot 1 tokens/CSS
git restore --source=e7aaa03 -- src/index.css styles/theme.css tailwind.config.js tokens/color-tokens.json
```

### Option B - Annuler un commit complet
```powershell
git log --oneline -n 5
git revert <commit-hash>
```

### Option C - Abandonner l'intégralité de la branche d'audit sans risque
La branche parente `feat/react-adobe-color-ahala` (`5f43b08`) n'a reçu aucune modification pendant l'audit :
```powershell
git checkout feat/react-adobe-color-ahala
git branch -D audit/typography-accessibility-v3
```
*(Si un rebuild production est souhaité après rollback : exécuter `npm test && npm run build`.)*
