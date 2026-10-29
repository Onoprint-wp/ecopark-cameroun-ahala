# Journal de Validation & Données Métier — ECOPARK Cameroun

**Dernière mise à jour :** 2026-10-29  
**Statut :** Refonte, Fiches de Mission A4, Dispatch Automatique Commande → Poste et Alertes Temps Réel terminés et validés à 100 % (35/35 contrôles de refonte + 333/333 tests existants réussis)

---

## 1. Vérification des Contrastes de la Palette Graphique « Canopée vivante » (Section B.1)

Les 9 tokens de départ ont été vérifiés selon la formule de luminance relative WCAG 2.1 face aux surfaces claires (`#FFFFFF` blanc et `#F7F5EF` ivoire) et au texte clair (`#FFFFFF`) :

| Rôle sémantique | Token CSS | Code Hex | Ratio sur `#FFFFFF` | Ratio sur `#F7F5EF` | Conformité WCAG AA (Texte >= 4,5:1 / UI & Grand texte >= 3:1) | Règle d'emploi appliquée |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Marque ECOPARK** | `--eco-brand` | `#254B28` | **9,61 : 1** | **8,83 : 1** | Conforme AAA | Bouton principal « Réserver », en-tête, repères institutionnels |
| **Nature et découverte** | `--eco-nature` | `#527A35` | **4,78 : 1** | **4,39 : 1** | Conforme AA sur `#FFFFFF` ; variante `--eco-nature-text: #3F6128` (**6,72 : 1** sur blanc, **6,17 : 1** sur ivoire) | Badges, bordures hautes et repères de l'univers Nature & Faune |
| **Eau et loisirs** | `--eco-water` | `#176B80` | **6,09 : 1** | **5,59 : 1** | Conforme AA | Univers Lac, Pirogues, Piscine semi-olympique & Pêche |
| **Hébergement** | `--eco-lodge` / `--eco-lodging` | `#A45138` | **5,14 : 1** | **4,72 : 1** | Conforme AA | Cités Hôtelières Bene, Chanthel, Ewondo VIP & Suites |
| **Restauration** | `--eco-dining` | `#946015` | **5,13 : 1** | **4,71 : 1** | Conforme AA | Restaurant Le Château des Saveurs & Pergolas |
| **Formation (CFP)** | `--eco-cfp` / `--eco-training` | `#4D5685` | **6,63 : 1** | **6,09 : 1** | Conforme AA | Campus CFP agréé MINEFOP (5 filières) |
| **Texte principal** | `--eco-text` | `#242824` | **14,82 : 1** | **13,61 : 1** | Conforme AAA | Titres, prix, corps de texte (>= 16 px) |
| **Fond clair** | `--eco-bg` | `#F7F5EF` | — | — | Surface neutre principale | Fond général du site et des pages transversales |
| **Surfaces** | `--eco-surface` | `#FFFFFF` | — | — | Cartes, panneaux, formulaires | Surfaces neutres majoritaires |

**Couleurs de statut (strictement distinctes des couleurs de catégorie et toujours accompagnées d'un libellé explicite) :**
- **Succès / Confirmé** : `--status-success-text: #1B5E20` sur `--status-success-bg: #EAF5EC` (bordure `#A5D6A7`, contraste > 7,5:1).
- **Avertissement / Pré-réservation guichet** : `--status-warning-text: #7C4A03` sur `--status-warning-bg: #FEF6E7` (bordure `#F5C77E`, contraste > 7,2:1).
- **Erreur / Fermé / Refusé** : `--status-error-text: #B42318` sur `--status-error-bg: #FDF2F2` (bordure `#F5B7B1`, contraste > 5,8:1).
- **Information / En étude** : `--status-info-text: #1E4E8C` sur `--status-info-bg: #EEF4FF` (bordure `#B8D4FE`, contraste > 7,4:1).

---

## 2. Source Unique des Informations & Données Métier Vérifiées (Section F)

Toutes les données affichées sur les cartes, fiches, tableaux de tarifs et résumés de réservation proviennent de la source unique centralisée (`window.ECOPARK_SOURCE_UNIQUE`, synchronisée avec `etape0-site-live/content-snapshot.json` et `EcoparkData`) :

### 2.1 Données confirmées et unités explicites
- **Localisation** : Quartier Ahala Barrière, juste en face de la station Tradex Ahala, Route Nationale N°3 (entrée sud de Yaoundé, Cameroun). Parking intérieur gratuit et sécurisé de **150 places**. Navettes climatisées de **5, 18 et 32 places** sur réservation.
- **Contacts officiels affichés** : `+237 697 13 62 03` (WhatsApp & réservations), `+237 675 56 26 55`, `info@ecopark-yaounde.com`.
- **Horaires et fermetures** :
  - **Parc & activités de loisirs** : Mardi au dimanche dès **09h00** (fermeture **18h00**). **Fermé le lundi** pour maintenance hebdomadaire.
  - **Hébergements (Cités Hôtelières)** : Ouverts **7j/7** (réception 24h/24) ; arrivée (**Check-in**) dès **14h00**, départ (**Check-out**) jusqu'à **11h00**.
  - **Restaurant Le Château des Saveurs** : Mardi au dimanche de **11h30 à 20h30** (service continu 7j/7 pour les résidents hôteliers).
- **Catégories d'âge et tarifs d'entrée** :
  - **Moins de 3 ans** : **0 FCFA** (accès parc gratuit).
  - **Enfant (3 à 12 ans)** : **500 FCFA / enfant** (tarif entrée enfant protégé, y compris en sortie scolaire).
  - **Adulte (13 ans et +)** : **1 000 FCFA / adulte** (tarif groupe **700 FCFA / adulte** dès 20 adultes).
- **Tarifs des activités et formules (avec unités explicites)** :
  - **Balade en pirogue sur le lac (45 min)** : `500 FCFA / enfant` • `1 000 FCFA / adulte` (par personne).
  - **Parc animalier (« ToTo ») & botanique** : `500 FCFA / enfant` • `1 000 FCFA / adulte` (par personne).
  - **Piscine semi-olympique surveillée** : `1 500 FCFA / enfant` (prévente/semaine) ou `2 500 FCFA / enfant` (guichet week-end) • `2 500 FCFA / adulte` (par personne).
  - **Promenade à cheval & manèges** : `500 FCFA / enfant` • `1 000 FCFA / adulte` (par personne).
  - **Musée patrimonial & bibliothèque** : `500 FCFA / enfant` • `1 000 FCFA / adulte` (par personne).
  - **Pass Découverte Nature (Zoo + Pirogue + Cheval)** : `1 500 FCFA / enfant` • `2 500 FCFA / adulte` (par personne).
  - **Pass Journée Royale (Zoo + Piscine + Pirogue + Repas chaud)** : `4 500 FCFA / enfant` • `8 500 FCFA / adulte` (par personne).
  - **Pack Escapade Couple VIP (Loge Ewondo + 2 Repas + Parc/Piscine/Pirogue)** : `45 000 FCFA` (1 nuit, forfait pour 2 adultes) / `70 000 FCFA` (2 nuits).
- **Hébergements (par nuit)** :
  - **Cité Bene (Standard)** : `10 000 – 15 000 FCFA / nuit`.
  - **Cité Chanthel (Confort)** : `15 000 – 25 000 FCFA / nuit`.
  - **Cité Ewondo (VIP Climatisé)** : `25 000 – 30 000 FCFA / nuit` (Day-Use repos journée : `15 000 FCFA`).
  - **Suites Privées Prestige VIP** : `30 000 – 45 000 FCFA / nuit`.
- **Restaurant Le Château des Saveurs (par plat / par menu)** :
  - **Poisson braisé d'Ahala** : `5 000 FCFA / plat`.
  - **Poulet DG Royal** : `6 500 FCFA / plat`.
  - **Ndolé Royal aux crevettes** : `5 500 FCFA / plat`.
  - **Menu Enfant Complet (< 12 ans)** : `2 500 FCFA / menu`.
- **Groupes & Événements** :
  - **Salle polyvalente « Menkii Essomba Anton »** : capacité vérifiée de **500 places assises** (climatisée et sonorisée).
  - **Forfait excursion scolaire** : dès `1 500 FCFA / élève` (entrée enfant protégée à `500 FCFA / élève`).
  - **Forfait séminaire entreprise** : dès `12 500 FCFA / participant`.
  - **Forfait mariage & gala** : dès `15 000 FCFA / invité`.
- **Formations CFP MINEFOP** :
  - **5 filières** : Hôtellerie, Restauration, Décoration, Agropastorale, Pisciculture.
  - **Durée & diplômes** : **12 mois** (30 % théorie, 70 % pratique sur le domaine) ; délivrance des titres **DQP**, **CQP** et Attestation reconnue par le MINEFOP.
  - **Admission** : dès **16 ans** (fiche d'inscription, copie CNI ou acte de naissance, dernier bulletin/diplôme, 4 photos 4×4).
  - **Frais officiels** : **50 000 FCFA** d'inscription + **250 000 FCFA** de scolarité annuelle payable en **4 tranches** (`100 000 FCFA` + `3 × 50 000 FCFA`).

### 2.2 Points documentés et règles de prudence appliquées
1. **Témoignages visiteurs (Section D.7)** : aucune source externe d'avis authentifiés avec autorisation écrite n'étant connectée, la section `#homeBlock7Testimonials` est masquée (`display: none`) et la mention « 4.9 / 5 (128 avis vérifiés) » a été retirée des vues publiques.
2. **Agenda hebdomadaire (Section D.6)** : alimenté par les 4 rendez-vous hebdomadaires publiés dans `content-snapshot.json` ; la fonction `syncAgendaVisibilityFromData()` masque automatiquement la section si la liste des événements publiés est vide.
3. **Jauges de rareté simulées (Section H)** : les badges de stock simulés en temps réel (`#pubEwondoScarcityBadge`, `#simPergolaRemainingBadge`, `#simEwondoRemainingText`, `#barometerAccordion`) sont masqués en vue visiteur pour ne présenter aucune fausse donnée temps réel.

---

## 3. Résultats des Contrôles Automatisés & Vérifications Multi-Écrans (Sections I.9 & J)

### 3.1 Suites de tests automatisés exécutées (10 suites — 100 % de réussite)

| Suite de vérification | Commande exécutée | Résultat | Détails |
| :--- | :--- | :--- | :--- |
| **Vérification complète Refonte « Canopée vivante » & Missions/Alertes A4** | `python scripts/verify_refonte_complete.py` | **41 / 41 OK** | Règles `.agents/rules/`, docs, parité `index.html`, palette 9 tokens, police >= 16px, cibles >= 44px, 5 rubriques, 1 seul H1, 8 blocs Accueil dans l'ordre, 5 gabarits métier, 5 scénarios auto-service, 4 parcours & 5 étapes de réservation, 7 routes canoniques, 5 largeurs responsive, module d'assignation de tâches (4 pôles) + Fiche de mission A4 imprimable + Règle `1 Commande = 1 Fiche de Mission selon le poste` + Centre d'alertes temps réel avec acquittement + Matrice des 6 Processus d'Approbation + 3 Visas interactifs + Baromètre Direction (11 services) |
| **Gouvernance SQL, RLS & Audit SHA-256** | `npm run test:db` | **75 / 75 OK** | 5 migrations idempotentes (dont `20261029000001_operational_missions_alerts.sql`), RLS visiteur/exploitation/direction/admin/guichet, RPCs `sign_mission_visa` (3 Visas) & `acknowledge_operational_alert`, garde-fous tarifs, chaîne d'audit SHA-256 |
| **Contrat de la couche de données** | `npm run test:data` | **108 / 108 OK** | `SupabaseDriver`, `LocalDemoDriver`, `operational_missions`, `operational_alerts`, `signMissionVisa`, `acknowledgeAlert`, synchronisation et validation des schémas |
| **Navigateur & bascule Supabase / Hors-ligne** | `python scripts/test_data_layer_browser.py` | **19 / 19 OK** | Mode démo, mode Supabase avec validation stricte du téléphone WhatsApp, mode réseau coupé |
| **Console d'administration CRUD** | `python scripts/test_admin_console.py` | **51 / 51 OK** | Authentification par rôle, édition, duplication, publication MFA, journal d'audit |
| **Responsive Console d'administration** | `python scripts/test_admin_responsive.py` | **20 / 20 OK** | Lisibilité et ergonomie mobile/tablette/desktop de l'interface d'administration |
| **Intégration Phase 5** | `python scripts/test_phase5_integration.py` | **18 / 18 OK** | Flux de réservation, devis groupe, candidature CFP et persistance |
| **Caisse & Guichet hors-ligne Phase 6** | `python scripts/test_phase6_caisse_horsligne.py` | **20 / 20 OK** | Scan QR, encaissement guichet, file hors-ligne et réconciliation |
| **Orchestration 360° Phase 7** | `python scripts/test_phase7_orchestration_360.py` | **22 / 22 OK** | Cohérence inter-vues Visiteur ↔ Guichet ↔ Exploitation ↔ Direction |
| **Cahier de recette & non-régression Phase 9** | `python scripts/test_phase9_v4_and_recette.py` | **16 / 16 OK** | 24 anomalies historiques corrigées, XSS, signature QR, masquage PII |

### 3.2 Contrôles responsive aux 5 largeurs exigées (Section I.9)
- **`360 px` (Mobile compact)** : `scrollWidth - clientWidth = 0 px`, navigation mobile lisible, cibles >= 44 px, aucune superposition de barres flottantes.
- **`390 px` (Mobile standard)** : `scrollWidth - clientWidth = 0 px`, tiroir mobile à 5 rubriques + barre inférieure à 4 accès opérationnels.
- **`768 px` (Tablette)** : `scrollWidth - clientWidth = 0 px`, passage fluide des grilles en 1 à 2 colonnes.
- **`1280 px` (Desktop standard)** : `scrollWidth - clientWidth = 0 px`, barre de navigation principale à 5 rubriques + `Mes réservations` + `Réserver` intégralement visible sur une seule ligne.
- **`1440 px` (Grand écran)** : `scrollWidth - clientWidth = 0 px`, alignement sur conteneur `1360 px` et hiérarchie visuelle « Canopée vivante ».

### 3.3 Validation des 5 scénarios utilisateurs en auto-service (Section H)
1. **Connaître le prix d'une journée pour 2 adultes et 2 enfants** : vérifié via le calculateur express `#quickDayPriceCalculator` dans *Préparer ma visite* (`Entrée Parc & Zoo seule : 3 000 FCFA`, `Pass Découverte Nature : 8 000 FCFA`, `Zoo + Piscine + Pirogue : 14 000 FCFA`, `Pass Journée Royale repas inclus : 26 000 FCFA`).
2. **Vérifier les conditions et le prix d'une chambre** : vérifié dans *Séjour & restaurant → Hébergements* (`Cité Bene 10 000 – 15 000 FCFA / nuit`, `Cité Chanthel 15 000 – 25 000 FCFA / nuit`, `Cité Ewondo VIP 25 000 – 30 000 FCFA / nuit`, `Suites Privées 30 000 – 45 000 FCFA / nuit`, `Check-in : 14h00 • Check-out : 11h00`, réception `7j/7`).
3. **Trouver le formulaire de devis pour une sortie scolaire** : vérifié dans *Groupes & événements* (`500 FCFA / élève` protégé, forfait dès `1 500 FCFA / élève`, Salle Menkii `500 places`, navettes `5, 18 et 32 places`, bouton principal « Demander un devis adapté à mon projet » et onglet dédié dans `/reserver`).
4. **Connaître les conditions d'admission d'une formation** : vérifié dans *Formations* (5 filières agréées MINEFOP, admission `dès 16 ans`, durée `12 mois`, inscription `50 000 FCFA` + scolarité `250 000 FCFA` en `4 tranches`, bouton de candidature en ligne).
5. **Comprendre le statut d'une réservation existante** : vérifié dans *Mes réservations* (`/mes-reservations`) avec libellés de statut explicites (`Confirmé`, `En étude`), références (`ECP-2026-84920`, `DEV-2026-3104`) et actions contextuelles (`Reporter ma date`, `Demander une annulation`, `Télécharger`).

### 3.4 Captures visuelles générées (`audit-assets/qa-refonte/`)
1. `01_accueil_canopee_vivante.png` : Accueil restructuré (« Prenez le frais. Vivez la nature. », navigation 5 rubriques, surfaces ivoire/blanc).
2. `02_catalogue_et_fiche_activite.png` : Fiche activité détaillée avec date dynamique et calculateur FCFA.
3. `03_hebergement_cites.png` : Sous-rubrique Hébergements (4 Cités, tarifs par nuit et conditions Check-in 14h00 / Check-out 11h00).
4. `04_restaurant_chateau_des_saveurs.png` : Sous-rubrique Restaurant Le Château des Saveurs (lieu, cuisine, carte en FCFA, horaires et modalités).
5. `05_formation_cfp_minefop.png` : Gabarit complet Formations CFP MINEFOP (5 filières, 12 mois, admission dès 16 ans, frais en 4 tranches).
6. `06_reservation_parcours_5_etapes.png` : Parcours de réservation restructuré (4 onglets de parcours + stepper 5 étapes dans l'ordre exact, sans billet QR prématuré).
7. `07_assignation_taches_exploitation.png` : Module d'assignation de tâches (`#sec-EXP-MISSIONS`) avec KPIs, 4 modèles de pôles terrain (Guichet, Contrôle QR, Hébergements, Cuisine), formulaire d'affectation, Matrice des 6 Processus d'Approbation et registre filtrable.
8. `08_fiche_mission_imprimable_a4.png` : Fiche de Mission Officielle Imprimable A4 (`#printableMissionSheetA4`) avec en-tête, logo, QR Code SVG de mission (92 px), dotation matériel, check-list terrain et 3 cadres d'émargement interactifs (`Visa #1`, `Visa #2`, `Visa #3`).
9. `09_mon_espace_sans_troncature.png` : Espace `Mes réservations` (`/mes-reservations`) avec boutons `Fiche Mission A4` et `Consulter Proforma` sans aucune troncature.
10. `10_direction_barometre_services.png` : Tableau de bord Direction (`/direction`) avec le baromètre des 11 services (8 services porteurs/réguliers et 3 services en sous-performance).
