# ECOPARK CAMEROUN (Yaoundé-Ahala) — Plateforme Digitale 360° & Billetterie QR

[![Production Live Vercel](https://img.shields.io/badge/Production_Vercel-En_Ligne_200_OK-1D490D?style=for-the-badge)](https://ecopark-cameroun-ahala.vercel.app)
[![Couverture Contractuelle](https://img.shields.io/badge/Écrans_Contractuels-77%2F77_Validés-C47D2B?style=for-the-badge)](./MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md)
[![Design System](https://img.shields.io/badge/Design_System-Canopée_Vivante_60--30--10-1F880B?style=for-the-badge)](./DESIGN.md)

Plateforme web officielle, simulateur budgétaire en **Francs CFA (FCFA)**, billetterie électronique **QR Code coupe-file**, module de **Prise de RDV**, générateur de **Factures Proforma Groupes/Écoles**, portail d'admission **CFP MINEFOP** et back-office d'exploitation pour **ECOPARK CAMEROUN** (*Route Nationale N°3, Ahala Barrière, face station Tradex Ahala, Yaoundé*).

---

## 1. Liens Directs en Production (`https://ecopark-cameroun-ahala.vercel.app`)

| Route Production | Écrans Couverts | Description Fonctionnelle |
| :--- | :--- | :--- |
| [`/`](https://ecopark-cameroun-ahala.vercel.app/) | `PUB-01` à `PUB-22` | Accueil 50/50 Hero HyperFrames, météo d'Ahala en direct, Bento 6 univers (`340px`), carte SVG interactive `Zones A → E`, Lightbox HD, Agenda de la Semaine et avis vérifiés. |
| [`/agenda`](https://ecopark-cameroun-ahala.vercel.app/agenda) | `PUB-15` / `PUB-16` | Agenda de la Semaine (Mardi – Dimanche) : 4 temps forts filtrables par jour (*Mercredi Pédagogique & CFP*, *Vendredi Afterwork*, *Samedi Famille*, *Grand Dimanche Royal*), programme horaire détaillé et réservation d'événement en 1 clic sur Billet QR. |
| [`/reserver`](https://ecopark-cameroun-ahala.vercel.app/reserver) | `RES-01` à `RES-12` | Simulateur FCFA, baromètre de disponibilité en temps réel (anti-surbooking loges & pergolas), 4 packs 1-clic, sélecteur des 3 Cités Hôtelières (*Ewondo, Chanthel, Bene*), précommande cuisine 13h, navette Yaoundé, Pass QR 3D et téléchargement PNG hors-ligne. |
| [`/rdv`](https://ecopark-cameroun-ahala.vercel.app/rdv) | `PUB-18` / `EXP-07` | Prise de rendez-vous personnalisée (Repérage Mariage/Gala Salle *Menkii Essomba Anton*, Séminaire B2B/Ministère/ONG, Excursion Scolaire, Orientation CFP). |
| [`/nos-tarifs`](https://ecopark-cameroun-ahala.vercel.app/nos-tarifs) | `PUB-10` | Grille tarifaire officielle 100 % en FCFA avec protection stricte du tarif enfant à `500 FCFA`. |
| [`/hotellerie`](https://ecopark-cameroun-ahala.vercel.app/hotellerie) | `PUB-08` / `PUB-09` | Cités Hôtelières **Bene** (`10–15k FCFA`), **Chanthel** (`15–25k FCFA`) et **Ewondo VIP** (`25–30k FCFA`). |
| [`/restaurant`](https://ecopark-cameroun-ahala.vercel.app/restaurant) | `PUB-07` | Gastronomie camerounaise au **Château des Saveurs** (Poisson braisé des étangs d'Ahala, Poulet DG, Ndolé Royal, Pergolas). |
| [`/formation`](https://ecopark-cameroun-ahala.vercel.app/formation) | `PUB-12` / `EXP-06` | **Centre de Formation Professionnelle (CFP)** agréé MINEFOP : 5 filières, dès 16 ans, inscription `50 000 FCFA` + scolarité `250 000 FCFA` en 4 tranches. |
| [`/guichet`](https://ecopark-cameroun-ahala.vercel.app/guichet) | `AGT-01` à `AGT-09` | Caisse rapide walk-in, scanner de contrôle QR à **7 verdicts** (anti-fraude double scan + cache hors-ligne RN3), grille de billetage contradictoire en coupures FCFA (seuil d'alerte `2 000 FCFA`), PV de clôture A4 signé et export CSV. |
| [`/direction`](https://ecopark-cameroun-ahala.vercel.app/direction) | `DIR-01` à `DIR-05` | Pilotage exécutif en FCFA, répartition Mobile Money / Guichet, rapport imprimable et export comptable CSV (Excel). |
| [`/admin`](https://ecopark-cameroun-ahala.vercel.app/admin) | `ADM-01` à `ADM-09` | Gouvernance des 7 rôles, verrouillage tarifaire enfant `500 FCFA`, **Inbox Unifiée des Leads & Réservations (statuts en 1 clic)**, passerelles sans secrets exposés et journal d'audit immuable chaîné SHA-256. |

---

## 2. Architecture du Dépôt & Livrables 360°

### 2.1 Suite Documentaire & Contractuelle (Orchestration Multi-Agents 360°)
- [`00_STRATEGIE_ET_SOCIAL_LISTENING.md`](./00_STRATEGIE_ET_SOCIAL_LISTENING.md) : Analyse PESTEL Yaoundé-Ahala, 7 verbatims clients documentés (dont le cas *Charlotte Manuella*), benchmark tarifaire 100 % FCFA et matrice d'optimisation.
- [`01_NEURO_COPYWRITING_AIDA.md`](./01_NEURO_COPYWRITING_AIDA.md) : Architecture cognitive d'aversion à la perte, texte intégral des 7 blocs AIDA et les 4 messages de soulagement dopaminergique post-formulaire avec ponts WhatsApp 1-clic (`+237 697 13 62 03`).
- [`02_SUITE_CONTRACTUELLE_6_CDC.md`](./02_SUITE_CONTRACTUELLE_6_CDC.md) : Suite complète des **6 Cahiers des Charges** (CCTP, CCAG, CCSE, CCÉditorial, CCGraphique, CCTMA avec SLA chiffrés).
- [`lead-and-ticket-schema.json`](./lead-and-ticket-schema.json) : Contrat d'interface JSON Schema (Draft 2020-12) unifiant `BookingTicket`, `GroupQuoteLead`, `AppointmentLead`, `CfpApplicationLead` et `UnifiedLeadInboxItem`.
- [`tokens.json`](./tokens.json) & [`03_DIRECTIVES_PRINT_ET_IMAGES.md`](./03_DIRECTIVES_PRINT_ET_IMAGES.md) : Design Tokens sémantiques universels W3C (`$value`, `$type`, `$extensions.print`), correspondances HEX $\rightarrow$ CMJN (FOGRA39) $\rightarrow$ Pantone $\rightarrow$ RAL pour la signalétique RN3 Ahala (*Onoprint*) et 5 prompts IA photoréalistes contextualisés Cameroun.
- [`04_RAPPORT_RECETTE_ET_QUALITE_FINALE.md`](./04_RAPPORT_RECETTE_ET_QUALITE_FINALE.md) : Rapport final d'audit QA, SEO `Schema.org`, sécurité Anti-XSS et recette contradictoire (`369/369` assertions validées).

### 2.2 Code Source, Base de Données & Bancs de Tests
- [`etape0-site-live/index.html`](./etape0-site-live/index.html) & [`Prototype_Interactif_ECOPARK_NEW_LOOK.html`](./Prototype_Interactif_ECOPARK_NEW_LOOK.html) : Bundle de production autonome déployé sur Vercel (`77/77` écrans + `ADM-09` Inbox Leads 1-clic, `Schema.org` JSON-LD 4 entités, `0` caractère `> U+25FF`, parité stricte 100 %).
- [`etape0-site-live/vercel.json`](./etape0-site-live/vercel.json) : Configuration du routage propre Vercel et des en-têtes de cache.
- [`supabase/migrations/20261026000001_ecopark_schema_rls.sql`](./supabase/migrations/20261026000001_ecopark_schema_rls.sql) : Schéma PostgreSQL / Supabase complet avec politiques **Row Level Security (RLS)** et chaîne d'audit SHA-256.
- [`DESIGN.md`](./DESIGN.md) : Documentation officielle du Design System *« Canopée vivante — Le cercle du vivant »* (Triade 60-30-10 + Ocre Bronze `#C47D2B`, typographies, grilles Bento et animations HyperFrames).
- [`MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md`](./MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md) : Matrice de traçabilité des 77 écrans contractuels (`DS`, `PUB`, `RES`, `ACC`, `AGT`, `EXP`, `DIR`, `ADM`).
- [`GUIDE_DEMO_CLOSING_DR_FOE_NDI.md`](./GUIDE_DEMO_CLOSING_DR_FOE_NDI.md) : Protocole de démonstration live en 7 minutes (5 actes) pour la présentation exécutive.
- [`verify_live_monochrome_prod.py`](./verify_live_monochrome_prod.py) & [`scripts/test_phase7_orchestration_360.py`](./scripts/test_phase7_orchestration_360.py) : Suites de tests E2E automatisés Playwright (`369/369` contrôles validés sur 9 bancs de tests).

---

## 3. Exécution des Tests E2E & Bancs de Recette (369 Contrôles)

```powershell
npm run test:db          # 69/69  — PostgreSQL / Supabase RLS, garde-fou 500 FCFA & audit SHA-256
npm run test:data        # 98/98  — Contrat EcoparkData (LocalDemoDriver & PGlite SQL)
npm run test:browser     # 19/19  — Hydratation navigateur & repli hors-ligne RN3
npm run test:admin       # 51/51  — Console d'administration ADM-01..08 & photothèque
npm run test:responsive  # 20/20  — Non-débordement 1440px -> 390px
npm run test:phase5      # 18/18  — Vrai QR matriciel, @media print, verrouillage Lundi, caméra
npm run test:phase6      # 20/20  — Billetage contradictoire FCFA, seuil 2 000 FCFA & scan hors-ligne
npm run test:phase7      # 22/22  — Orchestration 360°, Schema.org JSON-LD, Inbox Leads 1-clic & Anti-XSS
npm run test:e2e:local   # 52/52  — Audit intégral des 12 routes, 77 écrans & double scan anti-fraude
```
