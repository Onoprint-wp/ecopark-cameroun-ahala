# Plan de Tests, Vérifications et Corrections RBAC & Onboarding (8 Comptes)

## Goal
Vérifier de bout en bout (en local et en production sur `https://ecopark-cameroun-ahala.vercel.app`) les 8 types de comptes utilisateurs, leurs parcours d'onboarding et leurs workflows métiers, et corriger les 4 écarts détectés au code.

## Écarts Détectés à l'Audit Initial
1. **`visiteur_anonyme` bloqué sur `/mon-pass`** : `App.tsx` masque `<DigitalEcoPass />` derrière `<AuthPortal />` quand `!isAuthenticated`, empêchant de voir le Pass QR juste acheté ou de récupérer un billet unitaire via `ECP-2026-XXXXX` + téléphone/e-mail sans compte.
2. **2 rôles internes non pré-provisionnés** : `agent_guichet` (`GUICHET_CAISSE`) et `administrateur_plateforme` manquent dans `PROVISIONED_STAFF_ACCOUNTS` (`src/utils/ecoAuth.ts`), empêchant leur test réel hors Supabase.
3. **Anonymisation incomplète des billets (Loi n° 2010/012)** : `deleteMyAccount` supprime le compte dans `ecoAuth.ts` mais ne purge pas encore les coordonnées nominatives (`leadVisitor`, `ownerEmail`, `ownerUserId`) des `EcoPass` dans `EcoParkContext.tsx`.
4. **Périmètres `/exploitation` incomplets** : le curseur de jauge plafonne à `2 500` au lieu de `3 000` dans `RangerDashboard.tsx`, et il manque le tableau d'audit analytique SYSCOHADA (`comptable`) ainsi que le registre de gouvernance RBAC (`administrateur_plateforme` / `direction`).

## Tasks
- [x] **Task 1 (Coffre Staff 6/6)** : Générer les condensats salés `PBKDF2-HMAC-SHA256` (`120 000` itér.) pour `guichet@ecopark-yaounde.com` (`MAT-GUI-04`, `agent_guichet`) et `admin@ecopark-yaounde.com` (`MAT-ADM-00`, `administrateur_plateforme`) dans `src/utils/ecoAuth.ts`, et exposer `listProvisionedStaffDirectory()` + `getDeletionComplianceLog()` sans secret -> Verify: authentification réussie des 6 rôles staff en test unitaire.
- [x] **Task 2 (Workflow `visiteur_anonyme` sur `/mon-pass`)** : Ajouter `sessionUnlockedPassIds` (`sessionStorage`) et `lookupPassAnonymously(ref, contact)` dans `src/context/EcoParkContext.tsx`, puis mettre à jour `src/App.tsx` et `src/components/booking/DigitalEcoPass.tsx` pour afficher le billet fraîchement réservé ou recherché par référence sans exposer les autres billets -> Verify: un visiteur non connecté récupère `ECP-2026-8942` avec son téléphone/e-mail et voit l'encart d'onboarding 60s.
- [x] **Task 3 (Anonymisation Loi n° 2010/012 sur `EcoPass`)** : Ajouter `anonymizeUserPasses(userId, userEmail)` dans `src/context/EcoParkContext.tsx` et l'appeler dans `src/components/auth/AuthPortal.tsx` lors de `handleDeleteAccount` -> Verify: après suppression d'un `client_connecte`, le billet conserve son montant FCFA mais affiche `Client Anonymisé (Loi 2010/012)`.
- [x] **Task 4 (Cockpit Pro `/exploitation` & Profil C)** : Étendre le régulateur de jauge à `500-3000` dans `src/components/admin/RangerDashboard.tsx`, corriger les sous-titres `< 20px` en `font-sans`, et ajouter le panneau **Audit Financier SYSCOHADA** (`comptable`, `direction`, `administrateur_plateforme`) + la **Matrice RBAC des 6 postes** (`direction`, `administrateur_plateforme`) -> Verify: chaque rôle voit exactement ses contrôles habilités.
- [x] **Task 5 (Tests Unitaires & E2E Local des 8 Rôles)** : Étendre `src/utils/ecoAuth.test.ts` et `src/utils/ecosystemE2E.test.ts` pour couvrir les 8 `EcoParkRole`, les 6 comptes staff, la recherche unitaire anonyme, l'isolation des portefeuilles et l'anonymisation Loi 2010/012 -> Verify: `npm test` passe à 100 % (`0 fail`).
- [x] **Task 6 (Build & Conformité Loi 1/2/3)** : Exécuter `npm run build` et scanner `index.html` + `src/` -> Verify: `0` erreur TypeScript/Vite et `0` tiret `U+2013` / `U+2014`.
- [ ] **Task 7 (Déploiement Production)** : Commiter, pousser sur `origin/feat/react-adobe-color-ahala` et déployer via `npx vercel deploy --prod --yes` -> Verify: alias `https://ecopark-cameroun-ahala.vercel.app` à l'état `READY`.
- [ ] **Task 8 (Vérification Finale en Production)** : Exécuter un contrôle navigateur en direct sur `https://ecopark-cameroun-ahala.vercel.app` couvrant `visiteur_anonyme` (`/mon-pass` lookup), `client_connecte` (inscription 60s + portefeuille), `agent_guichet` (check-in actif / jauge grisée), `comptable` (audit SYSCOHADA lecture seule) et `administrateur_plateforme` (jauge `3000` + matrice RBAC) -> Verify: rapport navigateur 100 % `PASS` confirmé par `BROWSER_HOST_FACTS`.

## Done When
- [ ] Les 8 types de comptes et leurs workflows annoncés fonctionnent sans erreur en local (`npm test` + `npm run build`) et en direct sur `https://ecopark-cameroun-ahala.vercel.app`.
