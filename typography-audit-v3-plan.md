# Audit Typographique & Accessibilité ECOPARK V3 - Plan d'Exécution Multi-Agents

## Goal
Exécuter l'audit complet, la normalisation des design tokens et les correctifs typographiques/responsive de `feat/react-adobe-color-ahala` (`C:\Users\PcGamerCm\Downloads\ECO-PARK`) sur une branche isolée `audit/typography-accessibility-v3`, sans régression métier ni déploiement en production.

## Agent & Subagent Topology

| Rôle | Type / Mode Antigravity | Périmètre d'action | Droits d'écriture |
|---|---|---|---|
| **Coordinateur** | Agent principal (session courante) | Branche Git, arbitrages avec l'utilisateur, intégration des lots, `npm test` / `npm run build` | Complet (validation finale) |
| **`research`** | Sous-agent `research` (`Workspace: inherit`) | Phase A : cartographie statique des routes, vues, onglets, `<h1>`, overrides `!text-*` et `truncate` | Lecture seule |
| **`qa-measurer`** | Sous-agent custom (`EnableWriteTools: true`, `Workspace: inherit`) + Python Playwright | Phases B & F : serveur `vite preview`, mesures `getComputedStyle()`, zoom 200 %, captures avant/après, rapports `docs/ux-audit/` | `docs/ux-audit/` + script scratch |
| **`browser`** | Sous-agent `browser` (`Model: flash`) | Contrôle visuel interactif des états dynamiques (menu mobile, daltonisme, cartes bento `+`, wizard, Espace QR) | Navigation webview seule |
| **`design-tokens-architect`** | Sous-agent custom (`EnableWriteTools: true`, `Workspace: inherit`) | Phase C & Lot 1 : `ECOPARK_TYPOGRAPHY_TOKENS_V3.md`, plan de remédiation et refonte `src/index.css` | `docs/design/`, `docs/ux-audit/05_*`, `src/index.css` |
| **`ui-public-conversion`** | Sous-agent custom (`EnableWriteTools: true`, `Workspace: share`) | Phase E Lot 2 : `Navbar.tsx`, `HeroCanopy.tsx`, `ImpactBanner.tsx`, `AhalaShowcase.tsx`, `BookingWizard.tsx`, `DigitalEcoPass.tsx`, `Footer.tsx` | Isolé sur ses 7 fichiers TSX |
| **`ui-atlas-cockpit`** | Sous-agent custom (`EnableWriteTools: true`, `Workspace: share`) | Phase E Lot 3 : `App.tsx`, `InteractiveTopoMap.tsx`, `ElevationProfile.tsx`, `TrailCatalog.tsx`, `SpeciesAtlas.tsx`, `CitizenSentinel.tsx`, `AuthPortal.tsx`, `LegalNoticeView.tsx`, `RangerDashboard.tsx` | Isolé sur ses 9 fichiers TSX |

> **Règle d'orchestration :** Task 2 et Task 3 tournent en **parallèle** (lecture seule). Un **point de validation utilisateur (Gate)** sépare l'audit (Tasks 2-4) de l'écriture CSS/TSX (Tasks 5-7). Task 6 et Task 7 tournent en **parallèle** sur `Workspace: share` avec zéro fichier partagé.

## Tasks
- [x] **Task 1 (`Coordinateur`) :** Créer la branche `audit/typography-accessibility-v3` depuis `feat/react-adobe-color-ahala` (`6157dd7`, parent `0f677f8`) et vérifier la baseline → Verify: `git branch --show-current` retourne `audit/typography-accessibility-v3` et `npm test` + `npm run build` passent (32/32 tests).
- [x] **Task 2 (`research` -> rédaction `Coordinateur`, parallèle à Task 3) :** Inventorier les 8 `ActiveView`, 5 `ShowcaseTab`, 3 `LegalTab`, tiroirs, `<h1>`, overrides `!text-xs`/`!text-sm` et troncatures dans `src/` → Verify: `docs/ux-audit/01_ROUTE_AND_COMPONENT_INVENTORY.md` liste chaque route de `vercel.json` et `ecoRouting.ts` avec fichier/ligne confirmés.
- [x] **Task 3 (`qa-measurer` + `browser`, parallèle à Task 2) :** Lancer `npm run build && npm run preview` et exécuter l'audit Python Playwright sur les 9 viewports obligatoires (`320x700`, `360x800`, `390x844`, `430x932`, `768x1024`, `1024x768`, `1366x768`, `1440x900`, `1920x1080` + `1280x800` additionnel), thèmes Clair/Sombre, zoom 200 % et `/exploitation` (session staff) → Verify: `02_TYPOGRAPHY_INVENTORY.csv`, `03_TYPOGRAPHY_FINDINGS.md`, `04_RESPONSIVE_AND_REFLOW_MATRIX.md` et `screenshots/before/` contiennent des styles calculés réels, vérifications `document.fonts`, scroll interne et clipping.
- [ ] **Task 4 (`design-tokens-architect` -> GATE UTILISATEUR) :** Formaliser le modèle hybride ou strict dans `docs/design/ECOPARK_TYPOGRAPHY_TOKENS_V3.md` et `docs/ux-audit/05_COMPONENT_REMEDIATION_PLAN.md` (incluant impact sur `ecosystemE2E.test.ts`) → *(Livrables produits et audités ; validation explicite de l'utilisateur requise avant toute modification applicative en Tasks 5-8).*
- [ ] **Task 5 (`design-tokens-architect`) :** Appliquer le Lot 1 dans `src/index.css` (tokens `--text-*`/`--leading-*`, `.type-page-title`, `clamp()` 320 px sur `.type-hero`, corps mobile >= 16 px sans tracking compressé) et documenter le statut dormant de `styles/theme.css` / `tailwind.config.js` → Verify: `npm run build` vert et valeurs CSS conformes à la spec validée en Task 4.
- [ ] **Task 6 (`ui-public-conversion`, `Workspace: share`, parallèle à Task 7) :** Appliquer le Lot 2 sur le parcours public/conversion (suppression `truncate` sur prix et bandeau mobile, suppression `!text-xs`, plancher >= 13-14 px sur tarifs/cartes/boutons, tableaux 320 px) → Verify: `npx tsc -p tsconfig.app.json --noEmit` passe et 0 prix/condition/horaire tronqué dans les 7 composants du lot.
- [ ] **Task 7 (`ui-atlas-cockpit`, `Workspace: share`, parallèle à Task 6) :** Appliquer le Lot 3 sur les vues intérieures et `/exploitation` (unification des `<h1>` via `.type-page-title`, plancher >= 12 px dans `RangerDashboard.tsx` tout en conservant `< 20px` Profil C) → Verify: `npx tsc -p tsconfig.app.json --noEmit` passe et 0 `text-[9px]`/`text-[10px]` bloquant sur contenus critiques.
- [ ] **Task 8 (`Coordinateur`) :** Rapatrier les changements de Task 6 et Task 7 dans `audit/typography-accessibility-v3`, mettre à jour les assertions de `src/utils/ecosystemE2E.test.ts` validées en Task 4 et contrôler la Loi 1 (zéro `–`/`—`) → Verify: `npm test` (100 % pass) et `npm run build` réussissent sans modification de données métier.
- [ ] **Task 9 (`qa-measurer` + `Coordinateur`) :** Rejouer le benchmark Python Playwright avant/après sur les 9 viewports + zoom 200 % et livrer `06_BEFORE_AFTER_VISUAL_QA.md`, `07_WCAG_MANUAL_CHECKLIST.md` et `08_CHANGELOG_AND_ROLLBACK.md` → Verify: 0 débordement bloquant à 320 px/200 %, captures `screenshots/after/` archivées, rapport chiffré final sans déploiement.

## Done When
- [ ] Les 9 livrables `docs/ux-audit/01..08` et `docs/design/ECOPARK_TYPOGRAPHY_TOKENS_V3.md` sont complets, fondés uniquement sur des mesures réelles (ou marqués *non testé*).
- [ ] `npm test` et `npm run build` passent à 100 % sur `audit/typography-accessibility-v3`, sans altération des tarifs FCFA, horaires, contacts, palette ou routes.
- [ ] Tous les écarts P0/P1 de troncature, de corps `< 16 px` et de débordement à `320 px` / `200 %` sont résolus et prouvés avant/après.

## Notes
- **Règle de test critique :** `src/utils/ecosystemE2E.test.ts` impose 0 tiret `–`/`—` dans `src/` et `index.html`, contrastes `--text-muted` >= 7:1, 4 BLUF de 40-55 mots et scission Profil C `< 20px` dans `RangerDashboard.tsx`.
- **QA sans pollution npm :** Python Playwright (`python -m playwright`) + Chromium déjà en cache réalisent les captures et mesures Phase B/F sans ajouter de dépendance dans `package.json` (`axe-core` manuel ou injection éphémère en navigateur à documenter si utilisé).
- **Rollback :** Tout travail est isolé sur `audit/typography-accessibility-v3` ; aucune fusion sur `feat/react-adobe-color-ahala` ou `main` sans revue finale.
