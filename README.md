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
| [`/guichet`](https://ecopark-cameroun-ahala.vercel.app/guichet) | `AGT-01` à `AGT-09` | Caisse rapide walk-in, scanner de contrôle QR à **7 verdicts** (anti-fraude double scan), PV de clôture de caisse et export CSV. |
| [`/direction`](https://ecopark-cameroun-ahala.vercel.app/direction) | `DIR-01` à `DIR-05` | Pilotage exécutif en FCFA, répartition Mobile Money / Guichet, rapport imprimable et export comptable CSV (Excel). |
| [`/admin`](https://ecopark-cameroun-ahala.vercel.app/admin) | `ADM-01` à `ADM-08` | Gouvernance des 7 rôles, verrouillage tarifaire enfant `500 FCFA`, passerelles sans secrets exposés et journal d'audit immuable. |

---

## 2. Architecture du Dépôt

- [`etape0-site-live/index.html`](./etape0-site-live/index.html) : Bundle de production autonome déployé sur Vercel (`77/77` écrans, `68` icônes SVG linéaires monochromes, `0` dépendance externe lourde).
- [`etape0-site-live/vercel.json`](./etape0-site-live/vercel.json) : Configuration du routage propre Vercel et des en-têtes de cache.
- [`supabase/migrations/20261026000001_ecopark_schema_rls.sql`](./supabase/migrations/20261026000001_ecopark_schema_rls.sql) : Schéma PostgreSQL / Supabase complet avec politiques **Row Level Security (RLS)** pour les 8 tables métier (`catalog_activities`, `sales_bundles`, `lodge_cities`, `bookings`, `group_quotes`, `cfp_applications`, `appointments`, `audit_logs`).
- [`DESIGN.md`](./DESIGN.md) : Documentation officielle du Design System *« Canopée vivante — Le cercle du vivant »* (Triade 60-30-10 + Ocre Bronze `#C47D2B`, typographies, grilles Bento et animations HyperFrames).
- [`MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md`](./MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md) : Matrice de traçabilité des 77 écrans contractuels (`DS`, `PUB`, `RES`, `ACC`, `AGT`, `EXP`, `DIR`, `ADM`).
- [`GUIDE_DEMO_CLOSING_DR_FOE_NDI.md`](./GUIDE_DEMO_CLOSING_DR_FOE_NDI.md) : Protocole de démonstration live en 7 minutes (5 actes) pour la présentation exécutive.
- [`verify_live_monochrome_prod.py`](./verify_live_monochrome_prod.py) : Suite de tests E2E automatisés Playwright vérifiant la production Vercel (`12` routes HTTP 200 dont `/agenda`, `27/27` images, `0` emoji OS, `0` erreur console, double-scan anti-fraude, report de date sans frais et parcours complets).

---

## 3. Exécution des Tests E2E sur la Production

```powershell
python verify_live_monochrome_prod.py
```
