# FICHE METIER 06 : ADMINISTRATEUR PLATEFORME & DEVOPS
**Projet** : ECOPARK CAMEROUN (Yaoundé-Ahala)
**Rôle RBAC** : `super_admin` (Administration Supabase, RLS Multi-Tenant, Déploiement CI/CD, Sauvegardes & Loi 2024/017)
**Objectif** : Maintenir une disponibilité >= 99,9 %, garantir l'isolation RLS et exécuter les procédures de sécurité.

---

## 1. Vérification de Santé & Pipeline CI/CD
1. Avant toute mise en production sur la branche `main`, vérifier l'exécution de la pipeline `.github/workflows/ci.yml` :
   - `npm run test:db` (`81/81` assertions RLS et gouvernance SQL).
   - `npm run test:data` (`112/112` assertions couche de données et RBAC).
   - Sondes automatisées `/agency-guardrails-zero-error` (`ZERO-ERROR-GATE : GO`).
2. Contrôler le chargement du Service Worker PWA (`sw.js`) et la validité du fichier `manifest.json`.

---

## 2. Gestion des Comptes, Rôles RBAC & RLS Supabase
1. Les permissions reposent sur les politiques PostgreSQL Row-Level Security (`20261028000001_admin_crud_governance.sql` et `20261112000001_multi_tenant_and_compliance.sql`).
2. Ne jamais exposer la clé `SUPABASE_SERVICE_ROLE_KEY` dans le code front-end (`etape0-site-live/js/`). Seule la clé publique `ANON_KEY` est autorisée côté navigateur.
3. Vérifier que toute table métier critique conserve `ENABLE ROW LEVEL SECURITY` et la colonne `tenant_id`.

---

## 3. Sécurité des Médias & Stockage
1. Les téléversements d'images ou de documents dans la console admin sont filtrés par validation des **Magic Bytes** (`validateUploadMagicBytes` : signatures binaires `%PDF-`, `JPEG`, `PNG`, `WebP`).
2. Purger régulièrement les données de test via `EcoparkData.purgeTestQaResidues()` avant toute recette ou clôture comptable.

---

## 4. Conformité Loi N° 2024/017 (Cameroun) & Sauvegardes
1. Traiter sous **72 heures ouvrées** toute demande enregistrée dans la table `account_deletion_requests` issue de la fonction `EcoparkData.deleteAccount()`.
2. Vérifier chaque semaine le bon fonctionnement des sauvegardes automatiques PostgreSQL (PITR) et réaliser un test de restauration trimestriel sur environnement de staging.
