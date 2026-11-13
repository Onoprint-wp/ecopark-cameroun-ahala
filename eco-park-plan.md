# Plan Directeur d'Implémentation — Écosystème Complet ECO-PARK

## 1. Vision & Objectif Global
Concevoir et implémenter l'écosystème applicatif complet **ECO-PARK** (*Réserve Forestière, Écotourisme Régulé & Pilotage Environnemental*), bâti sur l'esthétique **Atlas Botanique & Cartographie Éditoriale** et sur la **recommandation chromatique hybride** :
1. **Rythme éditorial mixte intra-page** : alternance maîtrisée entre surfaces lumineuses haute lisibilité (`Soft Mist #E9F5ED` / `#F6FBF8`) pour la lecture, les filtres et les formulaires, et sections immersives profondes (`Deep Forest #1B4332` et `Deep Bark #1F2421`) pour le Hero, les bandeaux d'impact biodiversité et le pied de page.
2. **Moteur global adaptatif `Auto (Système) · Clair (Plein Soleil) · Sombre (OLED / Éco-Énergie)`** : synchronisation sans flash (anti-FOUC) avec l'appareil, persistance utilisateur, contrastes renforcés WCAG 2.1 AA/AAA et filtres d'accessibilité daltonisme.

---

## 2. Architecture de l'Écosystème Applicatif (5 Piliers)

1. **Socle Design System & Accessibilité Universelle**
   - Tokens CSS/JSON unifiés (`tokens/color-tokens.json`, `src/styles/theme.css` avec `@theme` Tailwind v4).
   - Moteur `Theme & Vision Engine` (`Auto`, `Clair`, `Sombre`, `Deutéranopie`, `Protanopie`, `Tritanopie`, `prefers-reduced-motion`).
   - Tiroir/Vue **Atelier Chromatique** interactif accessible à tout moment.
2. **Portail Découverte & Cartographie Interactive (Front-Office Public)**
   - Accueil éditorial mixte (Hero Canopée sombre `#1B4332` → Sections claires `Soft Mist` → Bandeau Impact sombre → Cartes Éco-Services).
   - **Carte Topographique Interactive SVG** & Catalogue des sentiers filtrable (difficulté, durée, dénivelé, accessibilité PMR, biome, statut en temps réel).
   - **Atlas Biodiversité (Faune & Flore)** : fiches d'espèces endémiques, saisonnalité d'observation et charte zéro-trace.
3. **Billetterie à Quota Écologique & Éco-Mobilité (Parcours Réservation)**
   - Réservation horodatée régulée selon la capacité écologique quotidienne du parc.
   - Choix d'expériences (*Accès Sentiers*, *Sortie Éco-Guide*, *Atelier Botanique*, *Pack Mobilité Douce*).
   - Calculateur de **CO₂ évité** et bonus éco-mobilité (train/navette/vélo), générant un **Éco-Pass numérique avec QR Code SVG**.
4. **Compagnon Visiteur sur Terrain (« Mon Éco-Pass & Sentinelle Nature »)**
   - Portefeuille local des billets réservés, itinéraires favoris, bascule rapide *Plein Soleil / Basse Consommation OLED*.
   - Module participatif **Sentinelle Nature** permettant aux visiteurs de signaler une observation d'espèce rare ou un incident sur sentier.
5. **Console Éco-Garde / Back-Office de Supervision (`/admin`)**
   - Tableau de bord opérationnel synchronisé en temps réel avec le portail visiteur : jauge de fréquentation par secteur, ouverture/fermeture dynamique des sentiers (ex. nidification, météo), suivi des réservations et modération des signalements *Sentinelle Nature*.
   - Télémétrie environnementale (qualité de l'air IQA, autonomie solaire du parc, CO₂ économisé).

---

## 3. Stack Technique & Arborescence Cible

- **Frontend & UI** : React 19, TypeScript 5, Vite 6, `@tailwindcss/vite` (Tailwind CSS v4 CSS-first), `lucide-react`
- **Navigation & État** : Routeur SPA multi-vues (`Accueil`, `Sentiers & Carte`, `Biodiversité`, `Billetterie`, `Mon Pass & Terrain`, `Console Éco-Garde`, `Atelier Couleurs`) + Store réactif typé persisté (`localStorage` + couche repository prête pour API REST / Supabase)
- **Typographie** : `Fraunces` (titres éditoriaux), `DM Sans` (interface & corps), `JetBrains Mono` (coordonnées GPS, télémétrie, ratios WCAG, QR pass)

```text
ECO-PARK/
├── tokens/
│   └── color-tokens.json              # Source W3C Design Tokens + métadonnées WCAG
├── public/                            # Icônes SVG & ressources statiques légères
├── src/
│   ├── styles/
│   │   └── theme.css                  # Tailwind v4 @theme + tokens Clair/Sombre/Immersif
│   ├── types/
│   │   └── ecosystem.ts               # Contrats TS (Trail, Species, Booking, Alert, Telemetry)
│   ├── data/
│   │   └── initialParkData.ts         # Données initiales réalistes (sentiers, faune, créneaux)
│   ├── context/
│   │   ├── ThemeContext.tsx           # Auto/Clair/Sombre + Daltonisme + anti-FOUC
│   │   └── EcoParkContext.tsx         # État partagé temps réel Visiteur <-> Éco-Garde
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx             # Navigation + Switch Auto/Clair/Sombre + Jauge live
│   │   │   ├── ImmersiveSection.tsx   # Conteneur de rythme éditorial sombre (#1B4332/#1F2421)
│   │   │   └── Footer.tsx             # Pied de page immersif Deep Bark + Sobriété numérique
│   │   ├── home/
│   │   │   ├── HeroCanopy.tsx         # Hero Canopée sombre + télémétrie parc en direct
│   │   │   └── ImpactBanner.tsx       # Bandeau sombre métriques CO2, solaire & biodiversité
│   │   ├── trails/
│   │   │   ├── InteractiveTopoMap.tsx # Carte topographique SVG cliquable (Clair & Sombre)
│   │   │   └── TrailCatalog.tsx       # Filtres multicritères + profils altimétriques
│   │   ├── biodiversity/
│   │   │   └── SpeciesAtlas.tsx       # Herbier & faune filtrable par biome/saison
│   │   ├── booking/
│   │   │   ├── BookingWizard.tsx      # Tunnel horodaté + quota + calculateur éco-mobilité
│   │   │   └── DigitalEcoPass.tsx     # Billet QR SVG prêt pour mobile plein soleil / OLED
│   │   ├── field/
│   │   │   └── CitizenSentinel.tsx    # Mode terrain + signalement participatif visiteur
│   │   ├── admin/
│   │   │   └── RangerDashboard.tsx    # Console Éco-Garde (statut sentiers, quotas, alertes)
│   │   └── design-system/
│   │       └── ColorAtlasDrawer.tsx   # Tiroir interactif Adobe Color & testeur WCAG
│   ├── App.tsx
│   └── main.tsx
├── index.html                         # Script synchrone anti-FOUC + filtres SVG daltonisme
├── COLOR-SYSTEM.md                    # Documentation de gouvernance chromatique
├── eco-park-plan.md                   # Plan directeur (ce fichier)
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 4. Plan d'Exécution Détaillé par Phases

### Phase 1 — Socle Technique, Tokens Hybrides & Moteur `Auto / Clair / Sombre`
- [x] **P1.1 — Initialisation Vite + React 19 + TypeScript + Tailwind v4** : Configurer `package.json`, `vite.config.ts` (`@tailwindcss/vite`), `tsconfig.json` et `lucide-react` tout en conservant `tokens/color-tokens.json` et `COLOR-SYSTEM.md` → **Verify** : `npm run dev` démarre sans erreur.
- [x] **P1.2 — Système CSS Hybride (`src/styles/theme.css`)** : Définir les 3 couches de tokens :
  1. *Primitives* (`forest`, `leaf`, `earth`, `mist`, `bark` `50 → 950`),
  2. *Surfaces adaptatives* (`--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--text-primary`, `--text-muted` renforcé à `#36403A` en Clair et `#C9D1CC` en Sombre, `--border-default` net `#8EBAA0` / `#46534B`),
  3. *Surfaces d'immersion éditoriale constantes* (`--surface-canopy: #1B4332`, `--surface-bark: #1F2421`, `--text-on-immersive: #E9F5ED`) pour rythmer les pages en Mode Clair comme en Mode Sombre → **Verify** : Tous les ratios ≥ 4.5:1 (AA) et ≥ 7:1 (AAA corps de texte).
- [x] **P1.3 — Moteur `ThemeContext` & Accessibilité Visuelle (`index.html`, `ThemeContext.tsx`)** : Script `<head>` zéro-flash FOUC, sélecteur 3 états (`auto`, `light`, `dark`), écoute temps réel du thème OS, et filtres SVG daltonisme (`normal`, `deuteranopia`, `protanopia`, `tritanopia`) → **Verify** : Rechargement sans flash + persistance `localStorage`.

### Phase 2 — Modèle de Données & Store Temps Réel de l'Écosystème
- [x] **P2.1 — Typage & Données Initiales (`src/types/ecosystem.ts`, `src/data/initialParkData.ts`)** : Modéliser 6 sentiers géolocalisés sur la carte SVG, 8 espèces emblématiques (faune/flore), créneaux horodatés avec quotas, télémétrie environnementale et signalements initiaux → **Verify** : `npx tsc --noEmit` passe à 100 %.
- [x] **P2.2 — Store Réactif Partagé (`src/context/EcoParkContext.tsx`)** : Gérer les réservations, la jauge quotidienne de biodiversité, le changement de statut d'un sentier par un Éco-Garde, et les signalements *Sentinelle Nature* avec sauvegarde `localStorage` et réinitialisation démo → **Verify** : Modifier un sentier en Console Éco-Garde met immédiatement à jour la Carte et la Billetterie.

### Phase 3 — Portail Public en Rythme Éditorial Mixte (Accueil, Carte SVG & Biodiversité)
- [x] **P3.1 — Shell Applicatif (`Navbar.tsx`, `ImmersiveSection.tsx`, `Footer.tsx`)** : Barre éditoriale sticky avec navigation par pôles, indicateur « Parc Ouvert · IQA », commutateur `Auto / Clair / Sombre`, bouton d'accès rapide à l'*Atelier Chromatique*, et Footer `Deep Bark` affichant l'éco-score de la page → **Verify** : Navigation clavier (`Tab`) et responsive mobile/tablette/desktop.
- [x] **P3.2 — Accueil Hybride (`HeroCanopy.tsx`, `ImpactBanner.tsx`)** : Alternance section sombre `HeroCanopy` (`#1B4332` + courbes topographiques SVG) → aperçu clair `Soft Mist` des sentiers actifs → bandeau sombre `ImpactBanner` (CO₂ évité, kWh solaires, espèces suivies) → **Verify** : Équilibre visuel Clair/Sombre respecté en mode Clair comme en mode Sombre intégral.
- [x] **P3.3 — Carte Topographique Interactive & Catalogue Sentiers (`InteractiveTopoMap.tsx`, `TrailCatalog.tsx`)** : Carte vectorielle interactive avec tracés colorés selon statut (`leaf-500` fluide, `earth-400` balisé/prudence, gris/rouge fermé), clic sur tracé synchronisé avec la fiche sentier et son profil d'élévation → **Verify** : Sélectionner un sentier sur la carte ou filtrer par biome/PMR met en surbrillance le parcours correspondant.
- [x] **P3.4 — Atlas Faune & Flore (`SpeciesAtlas.tsx`)** : Grille éditoriale filtrable (*Flore*, *Oiseaux*, *Mammifères*, *Amphibiens*) avec statut de conservation, période d'observation et sentiers associés → **Verify** : Filtres combinés fluides et badges accessibles sans conflit daltonisme.

### Phase 4 — Réservation Régulée, Compagnon Terrain & Console Éco-Garde
- [x] **P4.1 — Tunnel de Billetterie & Éco-Pass QR (`BookingWizard.tsx`, `DigitalEcoPass.tsx`)** : Choix de date/créneau (blocage automatique si quota atteint), sélection du mode de transport (calcul du CO₂ économisé + réduction Éco-Mobilité), génération d'un Éco-Pass avec QR Code SVG et décrémentation de la jauge du parc → **Verify** : Réserver 4 places met à jour la jauge biodiversité globale et ajoute le billet dans *Mon Pass*.
- [x] **P4.2 — Espace Terrain & Sentinelle Nature (`CitizenSentinel.tsx`)** : Consultation des Éco-Pass actifs (bouton plein écran haute lisibilité plein soleil), checklist zéro-trace et formulaire de signalement terrain (espèce observée ou obstacle sur un sentier précis) → **Verify** : Envoyer un signalement l'affiche instantanément dans la Console Éco-Garde.
- [x] **P4.3 — Console de Supervision Éco-Garde (`RangerDashboard.tsx`)** : Vue métier permettant de basculer l'état de chaque sentier (*Fluide* / *Prudence* / *Fermé nidification*), d'ajuster le plafond quotidien de visiteurs, de traiter les signalements citoyens et de suivre les KPIs écologiques → **Verify** : Fermer un sentier depuis `/admin` désactive sa réservation et met à jour la carte publique.
- [x] **P4.4 — Tiroir Atelier Chromatique Adobe Color (`ColorAtlasDrawer.tsx`)** : Intégrer l'inspecteur du Design System (5 piliers, échelles `50 → 950`, copie HEX/CSS/Tailwind en 1 clic, laboratoire de contraste WCAG en direct et sélecteur daltonisme) → **Verify** : Accessible depuis n'importe quel écran sans perdre l'état de navigation.

### Phase 5 — Vérification Finale de Bout en Bout (Qualité, Accessibilité & Navigateur)
- [x] **P5.1 — Compilation & Validation Statique** : Exécuter `npm run build` (`tsc -b && vite build`) et vérifier l'absence d'erreurs TypeScript, CSS ou d'imports inutilisés → **Verify** : Exit code `0` et découpage modulaire des chunks (< 500 kB).
- [x] **P5.2 — Audit Navigateur Complet (Clair, Sombre, Hybride, Daltonisme & Flux Métier)** : Ouvrir l'application dans le navigateur, tester le cycle complet (*Découverte Carte → Réservation Éco-Pass → Signalement Sentinelle → Bascule statut sentier dans Console Éco-Garde → Vérification répercussion côté Visiteur*) → **Verify** : 0 erreur console, contrastes nets partout, captures validées.

### Phase 6 — Animations Sobriété Cinétique, Synchronisation 360° & CI/CD GitHub Actions
- [x] **P6.1 — Moteur d'Animations Combinées GPU-Only (`ecoMotion.ts`, `Co2BotanicalSprout.tsx`, `GerminatingQrCode.tsx`)** : Transitions de vue Lisière Végétale, éclipse radiale Clair/OLED, parallaxe canopée, curseur géodésique, pousse botanique CO₂, QR germinatif en spirale, onde de statut sentier et sonar citoyen.
- [x] **P6.2 — Synchronisation Fonctionnelle 360° & Routage Vercel (`ecoRouting.ts`, `vercel.json`)** : Réconciliation atomique des quotas du jour (`reconcileTodayOccupancy`), pré-sélection sentier ↔ forfait FCFA, contrôle Check-In Guichet, compteur d'observations en direct et parité bidirectionnelle des 56 rewrites Vercel.
- [x] **P6.3 — Pipeline CI/CD Zero-Error Gate (`.github/workflows/ci.yml`)** : Exécution automatisée sur GitHub Actions (`npm ci` → `npm test` 25/25 → `npm run build` → audit d'intégrité `dist/` & SEO/GEO).

---

## 5. Critères d'Acceptation (`Done When`)
- [x] L'ensemble des **5 piliers de l'écosystème ECO-PARK** est fonctionnel et interconnecté via le store partagé.
- [x] Le **rythme éditorial mixte** (sections claires `Soft Mist` + sections d'immersion `Deep Forest / Deep Bark`) et le commutateur **`Auto / Clair / Sombre`** cohabitent sans friction ni flash au chargement.
- [x] Tous les textes secondaires, bordures, cartes, graphiques SVG et badges respectent **WCAG 2.1 AA/AAA** et **0 conflit daltonisme**.
- [x] Le build de production (`npm run build`), le pipeline GitHub Actions et la vérification interactive dans le navigateur sont validés.
