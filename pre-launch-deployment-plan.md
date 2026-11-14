# Plan de Finalisation Médias & Mise en Production Vercel - ECOPARK CAMEROUN

## Goal
Finaliser l'assainissement des médias publics (`public/images/ahala/`), verrouiller les accès de l'équipe et déployer en production sur `https://ecopark-cameroun-ahala.vercel.app/` le build vérifié sans aucune régression UX, mobile (`375x812`) ou sécurité.

## Tasks
- [x] Task 1: Purger les 6 planches de maquettes internes non référencées de `public/images/ahala/` (`AGT_01_*`, `DIR_01_*`, `DS_01_*`, `PUB_01_*`, `PUB_03_*`, `RES_01_*`). -> Verify: 0 référence dans le dépôt, 11 images publiques restantes, garde-fou ajouté dans `src/utils/ecosystemE2E.test.ts`.
- [ ] Task 2: Intégrer les photographies réelles d'Ahala pour `sp-1`, `sp-4`, `sp-5`, `sp-6`, `sp-7` (`src/data/initialParkData.ts`) et les gammes `bene`, `chanthel`, `ewondo`, `suites-vip` (`src/components/discovery/AhalaShowcase.tsx`), puis calibrer `getPhotoObjectPosition()` (`src/utils/ecoRouting.ts`). -> Verify: `/zoo` et `/hebergements` affichent chaque photo dédiée sans sujet tronqué. **En attente des photos terrain.**
- [x] Task 3: Remplacer `Printemps / Été / Automne / Hiver` par les 4 saisons équatoriales de Yaoundé (type `EquatorialSeason` dans `src/types/ecosystem.ts`, 8 fiches dans `src/data/initialParkData.ts`). -> Verify: 0 saison européenne dans `src/` et dans le bundle, garde-fou E2E ajouté.
- [x] Task 4: Mode d'authentification retenu : moteur `Web Crypto` autonome. -> Verify: `vercel env ls production` ne liste aucune variable `VITE_SUPABASE_*` (Supabase reste activable plus tard sans changer le code).
- [x] Task 5: Rotation des 6 accès initiaux de l'équipe (nouveaux sels et hachages PBKDF2 de mots de passe aléatoires de 20 caractères, rotation datée du 2026-11-14, coffre local obsolète automatiquement écarté). -> Verify: 6/6 nouveaux identifiants valides hors dépôt, 6/6 anciens mots de passe rejetés (`src/utils/ecoAuth.test.ts`).
- [x] Task 6: Porte de qualité complète. -> Verify: `npm test` 47/47, `npm run build` 0 erreur, contrôle `ci.yml` reproduit (84 réécritures, 9 migrations SQL, 0 maquette, 0 secret dans `dist/` et dans le dépôt).
- [x] Task 7: Commit `2ba7010` puis `vercel --prod`. -> Verify: déploiement `dpl_BDCJCfb3ms4sHcES1a6pvSwRMAsY` en statut `READY` et alias `https://ecopark-cameroun-ahala.vercel.app`.
- [x] Task 8: Recette en direct sur `https://ecopark-cameroun-ahala.vercel.app/` en `1440x900` et `375x812`. -> Verify: routes directes, isolation des billets, verrou `/exploitation`, mot de passe révoqué refusé, règles `/reserver`, `scrollWidth <= 375px`, 0 erreur console. **15/15 contrôles validés en production le 14/11/2026.**

## Done When
- [x] Aucun fichier de debug ni planche de maquette interne dans `dist/`.
- [x] Les 47/47 tests automatisés et `npm run build` passent à 100 %.
- [x] Les routes SPA (`/Connexion`, `/cgv`, `/confidentialite`, `/zoo`, `/carte`, `/mon-pass`, `/cockpit-pro`...) répondent en production en conservant leur URL exacte.
- [x] L'accès anonyme à `/mon-espace` n'expose aucune donnée tierce et `/exploitation` bloque tout visiteur non habilité.
- [x] L'affichage mobile `375x812` en production affiche `scrollWidth <= 375px`.

## Notes
- Les nouveaux mots de passe de l'équipe ne sont jamais versionnés : ils sont remis via un fichier local hors dépôt.
- En mode autonome, un changement de mot de passe depuis « Mon Compte » ne vaut que pour le navigateur où il est effectué. Une rotation globale passe par un nouveau build (procédure de ce lot) ou par Supabase Auth.
- Le commit est local sur la branche `audit/typography-accessibility-v3` (non poussé sur GitHub).
