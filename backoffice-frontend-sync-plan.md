# Plan de Correction & Vérification : Synchronisation Backoffice <-> Frontend

## Goal
Corriger toutes les anomalies identifiées dans la communication entre le Backoffice (`/exploitation`) et le Frontend public/client (`/`, `/carte`, `/reserver`, `/mon-pass`), verrouiller les mutations RBAC dans le store et valider les 5 flux bidirectionnels en local et en production (`https://ecopark-cameroun-ahala.vercel.app`).

## Anomalies Ciblées
1. **Détournement de navigation inter-onglets** : `ACTIVE_VIEW`, `SELECTED_TRAIL`, `SELECTED_SPECIES`, `ACTIVE_PASS_ID` et `DRAWER_OPEN` sont stockés/écoutés dans `localStorage`, ce qui éjecte l'onglet `/exploitation` dès qu'un autre onglet navigue.
2. **Course critique sur `useRef` & absence de bus temps réel** : `handleStorageEvent` ne met pas à jour `trailsRef`/`passesRef` de manière synchrone et n'utilise pas `BroadcastChannel`.
3. **Gardes RBAC & courses critiques de réservation manquantes** : les mutateurs de `EcoParkContext.tsx` n'exigent pas de rôle staff habilité, et `BookingWizard.tsx` ne re-vérifie pas en direct la fermeture d'un sentier (`status === 'ferme'`) ni l'épuisement soudain de la jauge à la soumission finale.
4. **Pont Cloud Supabase absent côté `EcoParkContext`** : ajout d'un adaptateur dual non bloquant (`BroadcastChannel + Storage` par défaut, et synchronisation PostgREST `public.bookings` fidèle au schéma SQL si `VITE_SUPABASE_URL` est configuré) avec indicateur transparent dans `/exploitation`.

## Tasks
- [x] **Task 1 (Moteur `src/utils/ecoSyncBus.ts`)** : Créer le bus `BroadcastChannel('eco_park_ahala_v2_bus')`, les gardes RBAC purs (`canMutateBackofficeOps`, `canMutateCheckIn`, `canActorCancelPass`), la validation temps réel de réservation (`validateLiveBookingConstraints`) et le mappeur exact `EcoPass <-> public.bookings` -> Verify: module typé sans dépendance externe ni tiret interdit (Loi 1).
- [x] **Task 2 (Isolation d'onglet & Gardes Store dans `EcoParkContext.tsx`)** : Basculer les états d'UI (`ACTIVE_VIEW`, sélections, tiroir) sur `safeSessionStorage`, synchroniser `TRAILS`, `TELEMETRY`, `PASSES`, `REPORTS` via `BroadcastChannel` + `storage` avec mise à jour synchrone des `useRef`, et protéger `setDailyCapacity`, `updateTrailStatus`, `checkInPass`, `cancelPass`, `updateReportStatus`, `resetToSeedData` par les gardes RBAC -> Verify: 0 détournement d'onglet et rejet de toute mutation non habilitée.
- [x] **Task 3 (Protection Temps Réel dans `BookingWizard.tsx` & Télémétrie Sync dans `RangerDashboard.tsx`)** : Bloquer l'étape 1 et la validation finale si `selectedTrail.status === 'ferme'` ou si la jauge vient d'être abaissée sous `totalGuests` (avec bouton de bascule vers les zones ouvertes), et afficher l'état réel du canal de synchro dans `/exploitation` (`< 20px` Profil C) -> Verify: surréservation et réservation sur circuit fermé impossibles.
- [x] **Task 4 (Tests Automatisés `src/utils/backofficeFrontendSync.test.ts`)** : Tester les 5 contrats bidirectionnels (`Jauge`, `Sentiers`, `Émission/Annulation Pass`, `Check-In QR`, `Sentinelle Nature`), l'isolation inter-onglets, les gardes RBAC des 8 rôles et le mappeur `public.bookings` -> Verify: `npm test` passe à 100 % (`0 fail`).
- [x] **Task 5 (Build & Conformité Loi 1/2/3)** : Exécuter `npm run build` (`tsc -b && vite build`) -> Verify: `0` erreur TypeScript/Vite et `0` tiret `U+2013` / `U+2014`.
- [x] **Task 6 (Déploiement & Test E2E Multi-Onglets Local + Production)** : Déployer sur `https://ecopark-cameroun-ahala.vercel.app` et vérifier en navigateur multi-onglets (Onglet 1 = `/exploitation`, Onglet 2 = Frontend) en local et en production -> Verify: rapport 100 % `PASS` confirmé par `BROWSER_HOST_FACTS`.

## Done When
- [x] Les 5 flux bidirectionnels `Backoffice <-> Frontend` et l'isolation de navigation inter-onglets fonctionnent sans erreur ni régression en local et sur `https://ecopark-cameroun-ahala.vercel.app`.
