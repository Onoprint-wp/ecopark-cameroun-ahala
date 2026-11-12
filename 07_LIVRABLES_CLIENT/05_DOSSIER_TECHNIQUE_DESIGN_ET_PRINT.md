# 🛠️ 05 - DOSSIER TECHNIQUE CODE-FIRST, DESIGN SYSTEM & PRINT FOGRA39 (`05_DOSSIER_TECHNIQUE_DESIGN_ET_PRINT.md`)

* **Projet** : **ECOPARK CAMEROUN (Yaoundé - Ahala, RN3)**
* **Architecture** : Hybride `PROFIL A` (Zero-Build HTML5/CSS3/JS) + `PROFIL C` (Dual-DB `LocalDemoDriver` + `SupabaseDriver` PostgreSQL 16 RLS) + `PROFIL D` (PWA Mobile `manifest.json` + `sw.js`).

---

## 1. Arborescence Physique du Code Source & Commandes de Recette

```text
ECO-PARK/
├── ADR_00_STACK_DECISION.md                  # Décision d'architecture Tech Radar (T1.5)
├── tokens.json                               # Design Tokens W3C (Light, Dark OLED #090D16, Sun Mode >= 7:1)
├── manifest.json                             # Manifeste PWA Mobile Offline-First
├── robots.txt / llms.txt / agents.txt        # Indexation Agentic GEO 2026 (9 bots IA)
├── sitemap.xml                               # Sitemap multilingue hreflang (fr, en, x-default)
├── Prototype_Interactif_ECOPARK_NEW_LOOK.html # Miroir strict de etape0-site-live/index.html
├── etape0-site-live/                         # Dossier de production déployé sur Vercel
│   ├── index.html                            # Application unifiée (78 écrans, Tri-Thème, JSON-LD @graph)
│   ├── vercel.json                           # 12 routes propres + en-têtes de sécurité
│   ├── manifest.json & sw.js                 # Socle PWA & cache hors-ligne
│   ├── content-snapshot.json                 # Snapshot initial du catalogue et des réglages
│   ├── locales/ (fr.json, en.json)           # Dictionnaires bilingues FR / EN
│   └── js/
│       ├── ecopark-data.js                   # Couche Dual-DB, tenant_id, sanitizeForRole, SecureStore, deleteAccount
│       └── ecopark-admin.js                  # Console CRUD ADM-01..09, garde-fous FCFA & Magic Bytes
├── supabase/
│   ├── migrations/ (8 migrations SQL)        # Schéma relationnel, RLS 100%, SHA-256 audit_logs, SYSCOHADA, tenant_id
│   └── tests/                                # Bancs de tests PGlite WebAssembly (81 tests RLS + 112 tests Data)
├── ecopark-geo-2026/                         # 25 livrables SEO / GEO IA 2026 & Copywriting 3 Cerveaux
└── 07_LIVRABLES_CLIENT/                      # 6 livrables Code-First + 6 Fiches Métiers (<= 80 lignes)
```

### Commandes de Vérification Automatisée
* `npm run test:db` : Exécute les **81 contrôles SQL/RLS/Audit** sous PGlite (`supabase/tests/rls_governance.test.mjs`).
* `npm run test:data` : Exécute les **112 contrôles de contrat Data Layer** (`supabase/tests/data_layer.contract.test.mjs`).
* `python scripts/verify_refonte_complete.py` : Exécute les **47 contrôles E2E Playwright** (Design, 5 rubriques, 8 blocs accueil, 5 scénarios auto-service, responsive `360px-1440px`, missions A4, Direction et Compta SYSCOHADA).
* `python scripts/test_phase9_v4_and_recette.py` : Exécute les **16 contrôles E2E Phase 9 V4**.

---

## 2. Variables d'Environnement (`.env.example`) & Sécurité DevSecOps

```ini
# Configuration Publique Supabase (uniquement la clé ANON publique côté navigateur)
SUPABASE_URL=https://votre-projet-ecopark.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Identifiant Multi-Tenant par défaut
ECOPARK_TENANT_ID=ecopark-yaounde-ahala
```
* **Règle Absolue (Loi 4.2)** : La clé privée `SUPABASE_SERVICE_ROLE_KEY` n'est jamais exposée dans le code client ni préfixée par `NEXT_PUBLIC_` ou `VITE_`.

---

## 3. Spécifications d'Impression Industrielle (`CMJN FOGRA39`) & Gabarits Physiques

### 3.1 Table Chromatique `HEX <-> CMJN FOGRA39 (TAC <= 300 %) <-> Pantone <-> RAL`
* **Vert Canopée Maître (`#1D490D` / `#254B28`)** : `C82 M32 Y100 K56` *(TAC 270 %)* | **Pantone 3435 C** | **RAL 6005**
* **Vert Feuille (`#1F880B` / `#527A35`)** : `C83 M5 Y100 K12` *(TAC 200 %)* | **Pantone 362 C** | **RAL 6018**
* **Bleu Lagon (`#176B80`)** : `C85 M30 Y25 K10` *(TAC 150 %)* | **Pantone 7705 C** | **RAL 5021**
* **Terre Cuite Loges (`#A45138`)** : `C20 M75 Y85 K15` *(TAC 195 %)* | **Pantone 7523 C** | **RAL 8004**
* **Ocre Bronze Saveurs (`#C47D2B` / `#946015`)** : `C18 M52 Y92 K8` *(TAC 170 %)* | **Pantone 7565 C** | **RAL 1024**
* **Encre Végétale (`#1E281B` / `#242824`)** : `C75 M60 Y72 K80` *(Titres)* / `C0 M0 Y0 K100` *(Corps < 12pt)* | **Pantone 419 C** | **RAL 6015**

### 3.2 Gabarit #1 : Sticker Vinyle Indélébile QR Code (Tables Restaurant, Loges & SAV Équipement)
* **Dimensions finies (*Trim Box*)** : `70 mm x 70 mm` (coins arrondis `6 mm`).
* **Fond Perdu (*Bleed*)** : **`3 mm` sur les 4 côtés** (`76 mm x 76 mm` format brut).
* **Zone de Sécurité Interne (*Safe Zone*)** : **`4 mm` à l'intérieur du trait de coupe**.
* **Résolution & Polices** : **`300 DPI` réels** + **100 % des textes vectorisés en courbes (*Outlines*)**.
* **Support** : Vinyle polymère adhésif permanent + lamination mate anti-UV et anti-humidité équatoriale.
* **URL QR Code (`Niveau H - 30 %`)** : `https://ecopark-cameroun-ahala.vercel.app/?utm_source=sticker_sav_qr`.

### 3.3 Gabarit #2 : Ticket de Caisse Thermique Guichet (`80 mm` - `AGT-03`)
* **Largeur papier** : `80 mm` (zone d'impression utile `72 mm`), impression thermique directe noir pur `100 % K`.
* **Contenu obligatoire** : En-tête `ECOPARK CAMEROUN - Yaoundé Ahala (RN3)`, horodatage `Africa/Douala`, détail des lignes en `tabular-nums`, total net en **FCFA**, mode de règlement, référence `ECP-2026-XXXXX`, signature `SIG-V4-*` et QR Code centré (`35 mm x 35 mm`).

### 3.4 Gabarit #3 : Ordre de Mission A4 (`#printableMissionSheetA4`) & PV de Clôture A4 (`AGT-09`)
* **Format** : `A4 Portrait (210 x 297 mm)` généré nativement via `@media print` (`printOfficialDocument()`).
* **Éléments de contrôle** : QR Code de mission `<= 92px`, check-list d'exécution, bloc des **3 Visas** (Assignation, Émargement Agent, Clôture & Note `/100`), et tableau contradictoire des coupures BEAC pour la clôture de caisse.
