# 🧭 ADR 00 : DÉCISION D'ARCHITECTURE & RADAR TECHNOLOGIQUE 2026 (`ADR_00_STACK_DECISION.md`)

* **Projet** : **ECOPARK CAMEROUN (Yaoundé - Ahala, RN3)**
* **Date de décision** : 12 Novembre 2026
* **Statut** : **APPROUVÉ (VERROUILLÉ POUR T2, T3, T4, T5)**
* **Architecture retenue** : **Combinaison Hybride `PROFIL A` (Zero-Build Ultra-Fast Web) + `PROFIL C` (Dual-DB Offline-First SaaS/POS + Supabase RLS) + `PROFIL D` (PWA Mobile Terrain Offline-First)**

---

## 1. Grille d'Évaluation Objective du Projet (Notation 1 à 5)

| Critère d'Évaluation | Score `/5` | Justification Technique & Terrain (Yaoundé - Ahala) |
| :--- | :---: | :--- |
| **1. Besoin SEO / GEO IA Public** | **5 / 5** | Destination éco-touristique majeure du Cameroun : nécessité d'un HTML pré-rendu instantané (`LCP < 1.8s` sur 3G), balisage Schema.org `@graph` (`TouristAttraction`, `OfferCatalog`, `FAQPage`, `HowTo`) et indexation directe par les 9 bots IA (`GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`). |
| **2. Complexité État & Logique Métier** | **5 / 5** | 78 écrans couvrant 6 familles (`PUB`, `RES`, `ACC`, `AGT`, `EXP`, `DIR`, `ADM`), simulateur tarifaire multi-formules, billetage BEAC contradictoire, Fiches de Mission A4 à 3 Visas, notation RH `/100` et Grand Livre analytique SYSCOHADA à 6 axes. |
| **3. Contrainte Réseau Terrain (*Offline*)** | **5 / 5** | Le site d'Ahala subit des micro-coupures 3G/4G et électriques aux heures de pointe du week-end. Le guichet POS (`AGT-03`) et le scanner QR aux tourniquets (`AGT-05`) doivent fonctionner à 100 % hors-ligne via `localStorage` / `IndexedDB` et `offlineScansQueue` avec resynchronisation idempotente. |
| **4. Cible Appareil & Ergonomie** | **5 / 5** | Double usage : smartphones Android/iOS des visiteurs et des agents de portail en plein soleil tropical (`390x844`, `Sun Mode >= 7:1`, cibles `>= 48px`) + postes desktop/tablettes de caisse, d'exploitation et de direction (`1440x900`). |
| **5. Volumétrie & Sécurité Multi-Rôles** | **5 / 5** | 8 rôles stricts (`visiteur`, `client_b2b`, `agent_guichet`, `agent_controle`, `responsable_exploitation`, `comptable`, `direction`, `administrateur_plateforme`), isolation Multi-Tenant (`tenant_id`), `ENABLE ROW LEVEL SECURITY` sur 100 % des tables PostgreSQL et journal d'audit immuable chaîné `SHA-256`. |
| **6. Vélocité de Déploiement & Résilience** | **5 / 5** | Architecture *Zero-Build* pour le Front-Office (aucune dépendance fragile au runtime, déploiement statique CDN Vercel instantané) couplée à un moteur PostgreSQL/PGlite testable localement à 100 % en WebAssembly. |

---

## 2. Choix du Profil Technologique : Hybride `PROFIL A` + `PROFIL C` + `PROFIL D (PWA)`

Conformément à la matrice de `/agency-tech-radar`, ECOPARK CAMEROUN combine trois volets complémentaires dans un dépôt unifié :

1. **Volet Vitrine & Conversion (`PROFIL A - Zero-Build Ultra-Fast Web`)** :
   * **Rendu** : HTML5 sémantique pré-rendu dans `etape0-site-live/index.html` (et son miroir racine), CSS3 natif gouverné par `tokens.json` (variables CSS `--eco-*`, `tabular-nums`, Tri-Thème `Zero-FOUC Light / Dark OLED / Sun Mode`), JavaScript ES2024 modulaire sans surcharge de framework lourd.
   * **Avantage décisif** : Temps de chargement initial quasi nul sur réseau mobile 3G camerounais, lisibilité immédiate par les crawlers LLM sans exécution JS obligatoire, et zéro risque de casse de build en production.
2. **Volet Caisse POS, Exploitation & ERP Direction (`PROFIL C - Dual-DB SaaS/POS`)** :
   * **Couche d'accès aux données (`etape0-site-live/js/ecopark-data.js`)** : Architecture à double pilote (`LocalDemoDriver` sur `localStorage`/`IndexedDB` + `SupabaseDriver` sur PostgreSQL 16 + Realtime WebSockets) avec bascule automatique hors-ligne et file d'attente `offlineScansQueue`.
   * **Base de données & Sécurité (`supabase/migrations/`)** : 8 migrations SQL PostgreSQL 16 avec `ENABLE ROW LEVEL SECURITY` systématique, clé d'isolation Multi-Tenant `tenant_id`, contrôle MFA `aal2` pour la publication des tarifs par la Direction, et chaîne de hachage `SHA-256` (`audit_logs`).
   * **Tests de contrat en local (`supabase/tests/`)** : Exécution déterministe sur **PGlite (PostgreSQL en WebAssembly)** permettant de valider 100 % des politiques RLS, triggers et RPC sans dépendre d'une connexion réseau externe.
3. **Volet Application Terrain Guichet & Scanner QR (`PROFIL D - PWA Mobile Offline-First`)** :
   * **Socle Mobile** : Progressive Web App (PWA) installable sur Android et iOS via `manifest.json` et Service Worker `sw.js`, stockage sécurisé des jetons de session (`SecureStore` pattern), ergonomie *Thumb-Zone* à 4 onglets mobiles et flux de suppression/anonymisation de compte (`deleteAccount`).

---

## 3. Langage Principal & Standards d'Ingénierie

* **Langage Principal** : **JavaScript ES2024 (ESM) / SQL PostgreSQL 16 (PL/pgSQL) / HTML5 / CSS3** (avec outillage d'orchestration et de recette E2E en **Python 3.12 + Playwright** et **Node.js 22**).
* **Arithmétique Financière (Loi 3.1)** : Tous les montants monétaires (`FCFA` / `XAF`) sont stockés et manipulés exclusivement sous forme d'entiers (`INTEGER` en SQL, `Math.round()` en JavaScript). Aucun type `Float` n'est autorisé sur un champ de prix, de caisse ou de comptabilité.
* **Animations & Rendu (Loi 2.2)** : Animations GPU `60fps` limitées aux propriétés composites `transform` et `opacity`, avec désactivation automatique sous `@media (prefers-reduced-motion: reduce)`.
* **Hébergement & CI/CD** : Déploiement sur **Vercel Edge Network** (`etape0-site-live/vercel.json`) + **Supabase Cloud** + pipeline **GitHub Actions** (`.github/workflows/ci.yml`).
