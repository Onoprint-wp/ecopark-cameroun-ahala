# Plan de Refonte ECOPARK Cameroun — Architecture de l'Information, Système Graphique & Parcours

**Dernière mise à jour :** 2026-10-29  
**Statut global :** Implémentation et vérifications terminées (Étapes I.1 à I.10 complètes à 100 %)

---

## 1. Inventaire de l'existant (Audit initial)

### 1.1 Architecture technique & fichiers clés
- **Application principale déployée (`etape0-site-live/`)** :
  - `etape0-site-live/index.html` (miroir synchronisé octet par octet dans `Prototype_Interactif_ECOPARK_NEW_LOOK.html` à la racine) : application web multi-routes (History API + query params + rewrites Vercel).
  - `etape0-site-live/vercel.json` : configuration des réécritures d'URL (routes canoniques et anciennes conservées) et en-têtes de sécurité.
  - `etape0-site-live/js/ecopark-data.js` : couche d'accès aux données hybride (`SupabaseRestDriver` + repli transparent `LocalDemoDriver` persisté dans `localStorage` sous `ecopark_db_v6`).
  - `etape0-site-live/content-snapshot.json` : instantané JSON de référence pour les activités, pass, hôtels, filières CFP, paramètres du site et événements.
  - `etape0-site-live/js/ecopark-admin.js` : logique de la console d'administration (`/admin`).
  - `etape0-site-live/audit-assets/ecopark-real-media/` : photographies authentiques du domaine d'Ahala et logo officiel (`cropped-LOGO-ECOPARK-Youtube.png`).
- **Vues internes et back-office existants (préservés à 100 %)** :
  - `view-PUB` : portail public multi-pages (`sec-PUB-01` à `sec-PUB-22`).
  - `view-RES` : tunnel de réservation (`/reserver`).
  - `view-ACC` : espace visiteur « Mes réservations » (`/mes-reservations` / `/mon-espace`).
  - `view-AGT` : guichet de caisse & scan QR (`/guichet`).
  - `view-EXP` : vue exploitation terrain.
  - `view-DIR` : tableau de bord direction (`/direction`).
  - `view-ADM` : console d'administration CRUD (`/admin`).
  - `view-DS` : référentiel design system interne.

### 1.2 Problèmes résolus par la refonte
1. **Omniprésence du vert (`#1D490D` / `#1F880B` / `#EDF4E7`)** : remplacée par le système graphique « Canopée vivante » reposant sur des surfaces neutres (`#F7F5EF` ivoire, `#FFFFFF` blanc), un texte principal anthracite (`#242824`) et 6 couleurs d'univers sémantiques distinctes des couleurs de statut.
2. **Répétitions et dispersion sur l'accueil (`sec-PUB-01`)** : fusion des introductions répétées en un seul Hero principal (`<h1>Prenez le frais. Vivez la nature.</h1>`) et structuration de l'Accueil selon l'ordre strict en 8 sections sans duplication du catalogue complet.
3. **Mentions techniques de développement exposées au public** : suppression des mentions publiques « V4 », « Architecture Multi-Pages », « Page 1/6 », « Parcours Transactionnel » et des avis non authentifiés (« 128 avis vérifiés »).
4. **Données simulées (« en direct ») et garanties commerciales non validées** : masquage des fausses jauges temps réel non reliées à une source vérifiée, masquage propre de la section Témoignages en l'absence de source authentifiée, et affichage conditionnel de l'Agenda selon les événements réellement publiés.
5. **Parcours de réservation confus (`view-RES`)** :
   - Séparation explicite en 4 parcours distincts (`1. Journée & Activités`, `2. Séjour & Hébergement 7j/7`, `3. Groupe, École ou Événement`, `4. Formation CFP MINEFOP`).
   - Alignement strict du stepper à 5 étapes (`1. Date et participants` → `2. Pass ou activités` → `3. Coordonnées` → `4. Récapitulatif et règlement` → `5. Résultat`).
   - Masquage du billet QR (`#demoTicketCard`) tant que la réservation n'est pas effectivement validée à l'étape 5.
   - Dates dynamiques calées sur le fuseau `Africa/Douala` (suppression de la date figée `2026-11-15`).
   - Affichage explicite du montant restant à régler au guichet lors du choix `Payer au guichet Ahala`.
   - Anonymisation du numéro de téléphone personnel dans le payload du QR Code public.

---

## 2. Arborescence Cible & Correspondance des Routes

### 2.1 Navigation principale cible (5 rubriques + utilitaires)
| Ordre | Rubrique principale | Slug canonique | Couleur d'accent (Token) | Pictogramme SVG | Contenus regroupés |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Découvrir le parc** | `/decouvrir` (alias `/activites`) | Nature `#527A35` & Eau `#176B80` | Feuille / Canopée & Boussole | Présentation du domaine d'Ahala, Catalogue filtrable des activités, Fiches détaillées des activités (`/fiche-activite`), Galerie photographique pertinente |
| **2** | **Séjour & restaurant** | `/sejour-restaurant` | Hébergement `#A45138` & Restauration `#946015` | Pavillon hôtelier & Tasse/Table | Sous-rubrique Hébergements (`/hebergements`) avec fiches des 4 cités et conditions 14h/11h, Sous-rubrique Restaurant Le Château des Saveurs (`/restaurant`) avec carte, prix par plat et modalités |
| **3** | **Groupes & événements** | `/groupes-evenements` | Marque `#254B28` / Nature `#527A35` | Groupe / Participants | Sorties scolaires (`/pack-ecole`, 500 FCFA/élève), Entreprises & associations (`/pack-entreprise`), Mariages & réceptions (Salle Menkii 500 places), Navettes 5/18/32 places, Demande de devis adapté |
| **4** | **Formations** | `/formations` (alias `/formation`) | Formation `#4D5685` | Toque académique | Présentation du CFP agréé MINEFOP, 5 filières, Objectifs & débouchés, Programme (30 % théorie / 70 % pratique), Durée (12 mois), Admission (dès 16 ans), Frais vérifiés (50k + 250k FCFA en 4 tranches), Candidature |
| **5** | **Préparer ma visite** | `/preparer-ma-visite` | Base neutre (`#F7F5EF` / `#176B80`) | Boussole d'orientation | Tarifs, pass & calculateur express (`/tarifs`), Horaires et jours d'ouverture, Accès RN3 Face Tradex & transport, Services pratiques, Agenda (`/agenda`), Questions fréquentes |

**Accès utilitaires permanents :**
- **Logo ECOPARK** → `/` (Accueil)
- **Mes réservations** → `/mes-reservations` (alias `/mon-espace`)
- **Bouton principal « Réserver »** → `/reserver` (accès unifié aux 4 parcours)

### 2.2 Table de correspondance des anciennes et nouvelles routes

| Route / URL entrante | Type | Cible dans l'application | Comportement / Redirection logique |
| :--- | :--- | :--- | :--- |
| `/` | Canonique | Accueil (`view-PUB` — `ACCUEIL`) | Restructuré selon l'ordre strict en 8 blocs (Section D) |
| `/decouvrir` | Nouvelle canonique | Découvrir le parc (`view-PUB` — `PUB-03`) | Présentation du domaine + Catalogue des 8 activités |
| `/activites` | Ancienne (conservée) | Découvrir le parc (`view-PUB` — `PUB-03`) | Maintenue et résolue vers « Découvrir le parc » |
| `/fiche-activite` | Conservée | Fiche détaillée activité (`view-PUB` — `PUB-04`) | Gabarit complet Fiche Activité (déroulement, inclus/non inclus, conditions, activités complémentaires) |
| `/sejour-restaurant` | Nouvelle canonique | Séjour & restaurant (`view-PUB` — `PUB-09`) | Sous-rubrique Hébergements (4 cités) + Sous-rubrique Restaurant Le Château des Saveurs |
| `/hebergements`, `/hotellerie` | Anciennes (conservées) | Séjour & restaurant (`view-PUB` — `PUB-09`) | Ouvre « Séjour & restaurant » sur les 4 Cités Hôtelières |
| `/restaurant` | Ancienne (conservée) | Séjour & restaurant (`view-PUB` — `PUB-07` / `PUB-09`) | Ouvre « Séjour & restaurant » sur le Restaurant Le Château des Saveurs |
| `/groupes-evenements` | Nouvelle canonique | Groupes & événements (`view-PUB` — `PUB-11`) | Sorties scolaires, Entreprises, Mariages (Salle Menkii 500 places) & Devis |
| `/pack-ecole`, `/pack-entreprise` | Anciennes (conservées) | Groupes & événements (`view-PUB` — `PUB-11`) | Ouvre le gabarit Groupes & événements et accès devis |
| `/formations`, `/formation` | Canonique & Ancienne | Formations CFP (`view-PUB` — `PUB-12`) | Gabarit complet CFP MINEFOP (5 filières, 12 mois, dès 16 ans, frais, candidature) |
| `/preparer-ma-visite` | Nouvelle canonique | Préparer ma visite (`view-PUB` — `PUB-10`) | Calculateur express, Tarifs & pass, Horaires, Accès RN3, Agenda, FAQ |
| `/nos-tarifs`, `/tarifs` | Anciennes (conservées) | Préparer ma visite (`view-PUB` — `PUB-10`) | Ouvre « Préparer ma visite » sur la grille tarifaire et le calculateur |
| `/agenda`, `/evenements` | Anciennes (conservées) | Préparer ma visite (`view-PUB` — `PUB-16`) | Ouvre l'agenda hebdomadaire |
| `/contact`, `/rdv`, `/rendez-vous` | Anciennes (conservées) | Préparer ma visite (`view-PUB` — `PUB-13` / `PUB-18`) | Ouvre Accès RN3, Contact & Rendez-vous |
| `/mes-reservations`, `/mon-espace` | Nouvelle & Ancienne | Mes réservations (`view-ACC` — `ACC-02`) | Réservations, billets QR, demandes de devis et statuts |
| `/reserver` | Canonique | Parcours de réservation (`view-RES` — `RES-01`) | 4 parcours distincts + stepper 5 étapes |
| `/guichet`, `/direction`, `/admin` | Back-office (conservées) | `view-AGT`, `view-DIR`, `view-ADM`, `view-EXP` | Outils d'exploitation, d'assignation de missions A4 et d'administration 100 % opérationnels |

---

## 3. Module Opérationnel : Assignation d'une tâche & Fiche de mission imprimable A4

Suite à la demande d'outillage des équipes terrain d'Ahala, un module complet d'**Assignation de tâches et génération de Fiches de Mission A4** a été intégré dans les vues d'exploitation :
- **Exploitation Terrain (`#view-EXP` → `#sec-EXP-MISSIONS`)** :
  - Bandeau de suivi temps réel : nombre de missions du jour (fuseau `Africa/Douala`), missions actives (`En cours sur poste`), missions validées (`Terminées & Validées`) et couverture des **4 pôles terrain**.
  - **4 modèles métiers pré-configurés en 1 clic** respectant les tokens graphiques « Canopée vivante » :
    1. **Guichet & Caisse (`GUICHET_CAISSE` — `#527A35`)** : Caisse Entrée RN3, fond de caisse `50 000 FCFA`, encaissement Espèces/MoMo sans code PIN, clôture contradictoire.
    2. **Contrôle QR Piscine & Lac (`CONTROLE_QR` — `#176B80`)** : Scan QR hors-ligne 7 états au tourniquet piscine et embarcadère pirogues, port obligatoire du gilet homologué.
    3. **Hébergements 3 Cités (`HEBERGEMENT` — `#A45138`)** : Cités Ewondo VIP, Chanthel Confort & Bene Standard, Check-in `14h00` / Check-out `11h00`, réception `7j/7`.
    4. **Cuisine Le Château des Saveurs (`CUISINE_SAVEURS` — `#946015`)** : Mise en place des précommandes `12h30`, Poisson braisé d'Ahala (`5 000 FCFA`), Poulet DG Royal (`6 500 FCFA`), service « Zéro Attente » `13h00`.
  - Formulaire complet d'assignation (`#expMissionAssignForm`) avec choix du pôle, de l'agent (matricule & fonction), de la date (`Africa/Douala`), du créneau horaire, de la priorité, de l'intitulé, de la zone d'affectation, de la dotation matériel, des objectifs et des points de contrôle (check-list).
  - Registre filtrable des missions (`#expMissionsTable`) avec progression de statut en 1 clic (`Assignée` → `En cours sur poste` → `Terminée & Validée`) et journalisation dans `db.auditLogs`.
- **Guichet & Contrôle (`#view-AGT` → `#agtActiveMissionBanner`)** : bandeau permanent affichant la mission active du caissier/contrôleur avec accès direct en 1 clic à sa **Fiche de Mission A4** et au panneau d'exploitation.
- **Administration (`#view-ADM` → `#sec-ADM-05`)** : bouton d'action rapide `#admOpenMissionsBtn` (`Assigner une tâche / Fiche de mission A4 →`) dans la gestion des comptes de l'équipe.
- **Fiche de Mission Officielle Imprimable A4 (`#printableMissionSheetA4` via `openMissionSheetA4` / `printOfficialDocument('MISSION', id)`)** :
  - En-tête officiel avec logo ECOPARK (proportions préservées), badge du pôle, référence unique `MSN-2026-XXXX`, date `Africa/Douala (UTC+1)` et **QR Code SVG** de vérification d'ordre de mission (`#missionSheetQrContainer`).
  - Cartouche Agent affecté (Nom, Matricule, Fonction, Autorité d'affectation) & Poste/Horaires.
  - Intitulé de la tâche, objectif opérationnel, dotation matériel remise et garde-fou réglementaire ECOPARK.
  - Check-list interactive de contrôle terrain (cochable à l'écran et à l'impression).
  - **3 cadres d'émargement contradictoire** : *1. Visa Responsable Exploitation*, *2. Émargement Agent (Prise de poste)*, *3. Visa Clôture & Remise Dotation*.

---

## 4. Étapes d'exécution et état d'avancement

- [x] **Étape 1 — Audit des routes, composants, contenus, données et intégrations**
- [x] **Étape 2 — Installation des règles persistantes (`.agents/rules/ecopark-*.md`)**
- [x] **Étape 3 — Rédaction du plan et du document de validation (`docs/ecopark-*.md`)**
- [x] **Étape 4 — Centralisation des tokens graphiques (`tokens.json`, CSS `:root`) et de la source unique (`window.ECOPARK_SOURCE_UNIQUE`)**
- [x] **Étape 5 — Refonte de la navigation principale (5 rubriques + utilitaires) et des routes Vercel (`etape0-site-live/vercel.json`)**
- [x] **Étape 6 — Restructuration de l'Accueil (`/`) en 8 sections ordonnées avec un seul `<h1>` et suppression du jargon de développement**
- [x] **Étape 7 — Application des gabarits métier complets (Fiche activité, Hébergement, Restaurant, Groupes & événements, Formation CFP, Préparer ma visite, Mes réservations)**
- [x] **Étape 8 — Restructuration des parcours de réservation (`/reserver`) en 4 parcours et 5 étapes sans billet confirmé prématuré ni date figée `2026-11-15`**
- [x] **Étape 9 — Vérifications multi-écrans (`360px`, `390px`, `768px`, `1280px`, `1440px`), tests automatisés (10 suites, 367 assertions validées à 100 %) et captures**
- [x] **Étape 10 — Mise à jour finale des documents de suivi et livraison**
- [x] **Étape 11 — Implémentation et validation du module « Assignation d'une tâche & Fiche de mission imprimable A4 » sur les 4 pôles d'exploitation d'Ahala**
