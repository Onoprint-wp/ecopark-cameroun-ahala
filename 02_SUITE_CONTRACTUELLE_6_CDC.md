# SUITE CONTRACTUELLE COMPLÈTE — LES 6 CAHIERS DES CHARGES (CDC)
## Programme : Refonte Digitale 360°, Billetterie QR Mobile Money, Exploitation & Gouvernance — « ECOPARK CAMEROUN (Yaoundé-Ahala) »

- **Maître d'Ouvrage (Client) :** **ECOPARK YAOUNDÉ (ECOPARK CAMEROUN)** — Complexe Agro-Écotouristique, Hôtelier, Événementiel et de Formation Professionnelle, sis au Quartier Ahala Barrière (Axe lourd RN3 Yaoundé–Douala, face Station Tradex), BP Yaoundé, République du Cameroun.
  - **Promoteur & Président Directeur Général :** **Dr Christophe FOE NDI**
  - **Gérant Délégué (« ECOPARK NEW LOOK ») :** **M. Mgbatou Daryl**
- **Maître d'Œuvre (Titulaire) :** **ONOGRAPH SARL** (*« L'Architecte Invisible de l'Influence Visible »*) — Quartier Simbock, Yaoundé, République du Cameroun (`www.onograph.online` | `+237 6 70 72 80 87` | `info@onograph.online`).
- **Référence Contractuelle :** `MARCHE-ECOPARK-ONO-2026-10-SUITE-6CDC`
- **Périmètre de Référence :** Couverture intégrale des **77 écrans contractuels** (`DS-01..08`, `PUB-01..22`, `RES-01..12`, `ACC-01..06`, `AGT-01..09`, `EXP-01..07`, `DIR-01..05`, `ADM-01..08`), du schéma PostgreSQL/Supabase durci (`20261026000001_ecopark_schema_rls.sql`) et du contrat d'interface JSON Schema Draft 2020-12 (`lead-and-ticket-schema.json`).
- **Date d'effet :** Octobre 2026 — Force exécutoire et directement opposable entre les parties.

---

# CAHIER 1 — CCTP (CAHIER DES CLAUSES TECHNIQUES PARTICULIÈRES)

## Article 1.1 — Objet et Architecture Technique Globale
Le présent Cahier des Clauses Techniques Particulières (CCTP) fixe les spécifications d'ingénierie logicielle, d'architecture de données, de performance réseau et de résilience hors-ligne exigées pour la plateforme numérique unifiée **ECOPARK CAMEROUN**.

L'architecture repose sur un **socle Web Autonome Haute Performance (SPA/MPA hybride sans dépendance lourde bloquante)** couplé à une couche de persistance transactionnelle **PostgreSQL 15+ / Supabase** et un moteur local de continuité d'activité (**Cache Hors-Ligne RN3** via `localStorage` et file d'attente transactionnelle `offlineScansQueue`).

## Article 1.2 — Exigences de Performance Réseau et Temps de Réponse
Compte tenu des conditions réelles de connectivité sur l'axe routier national n° 3 (RN3 — entrée sud de Yaoundé, secteur Ahala Barrière) et de la prépondérance des terminaux mobiles Android milieu de gamme utilisés par la clientèle et les agents de terrain :

1. **Temps de rendu initial en réseau local / cache chaud (TTFB & First Contentful Paint) :** strictement inférieur à **`500 ms`** (`< 0,5 seconde`).
2. **Temps d'interactivité complet sur réseau mobile 3G/4G Cameroun (MTN Cameroon / Orange Cameroun, profil 4G dégradé ou 3G+ à 1,6 Mbps / latence 150 ms) :** strictement inférieur à **`1 500 ms`** (`< 1,5 seconde` pour le Largest Contentful Paint — LCP).
3. **Temps d'exécution d'un changement de vue parmi les 77 écrans ou d'un recalcul budgétaire (`RES-03`) :** inférieur à **`50 ms`** côté client (zéro rechargement de page complet).
4. **Budget de poids applicatif :**
   - Document HTML/CSS/JS critique compressé (Brotli/Gzip) : **`<= 180 Ko`**.
   - Photographies du site d'Ahala optimisées (formats modernes WebP/AVIF, chargement différé `loading="lazy"` hors Hero `PUB-01`, ratios maîtrisés `16:10` et `4:3` sans déformation).
   - Zéro bibliothèque JavaScript externe superflue ralentissant le fil principal d'exécution (Main Thread Blocking Time `< 100 ms`).

## Article 1.3 — Couverture Opposable des 77 Écrans Contractuels (8 Familles)
Le Titulaire garantit la livraison fonctionnelle, interactive et unitaire des **77 écrans contractuels** répartis en **8 familles** sans aucun écran manquant, fusionné abusivement ou laissé à l'état de coquille vide :

| Code Famille | Plage d'Identifiants | Nombre d'Écrans | Périmètre Technique & Fonctionnel Opposable |
| :--- | :--- | :---: | :--- |
| **1. `DS`** | `DS-01` à `DS-08` | **8** | Design System exécutable : règles du logo, tokens CSS, typographies, grilles 12 colonnes, boutons/badges, formulaires anti-erreur, cartes d'offre et composants métier (simulateur, billet QR, scanner). |
| **2. `PUB`** | `PUB-01` à `PUB-22` | **22** | Portail public complet : Accueil (`PUB-01`), Plan des 6 pôles (`PUB-02`), Catalogue filtrable (`PUB-03`), Fiches détail (`PUB-04`), Faune/Flore (`PUB-05`), Piscine & Lac (`PUB-06`), *Château des Saveurs* en FCFA (`PUB-07`), Cités Hôtelières Ewondo/Chanthel/Bene (`PUB-08`, `PUB-09`), Grille tarifaire officielle (`PUB-10`), B2B & Écoles (`PUB-11`), CFP MINEFOP (`PUB-12`), Infos pratiques RN3 & Météo (`PUB-13`), Photothèque badgée (`PUB-14`), Agenda Mardi–Dimanche & Avis (`PUB-15`, `PUB-16`), FAQ (`PUB-17`), Contact & Prise de RDV (`PUB-18`), Recherche globale (`PUB-19`), Mentions légales/CGV (`PUB-20`), Page 404 (`PUB-21`), Maintenance (`PUB-22`). |
| **3. `RES`** | `RES-01` à `RES-12` | **12** | Tunnel de préparation et réservation : Profil de visite (`RES-01`), Date & composition (`RES-02`), Simulateur FCFA avec garde-fou tarif enfant (`RES-03`), Panier détaillé (`RES-04`), Coordonnées `+237` (`RES-05`), Devis groupe `DEV-2026-XXXX` (`RES-06`), Choix paiement OM/MoMo/Guichet (`RES-07`), Automate USSD 5 états sans code PIN (`RES-08`), Billet QR `ECP-2026-XXXXX` (`RES-09`), Confirmation devis (`RES-10`), Reprise sur échec/expiration (`RES-11`), Recherche dossier sans compte (`RES-12`). |
| **4. `ACC`** | `ACC-01` à `ACC-06` | **6** | Espace Visiteur / Client : Authentification OTP (`ACC-01`), Tableau de bord visite (`ACC-02`), Portefeuille billets QR (`ACC-03`), Suivi devis & RDV (`ACC-04`), Report gratuit 90 jours Garantie Pluie & Remboursement Mobile Money `RFD-2026-XXXX` (`ACC-05`), Préférences (`ACC-06`). |
| **5. `AGT`** | `AGT-01` à `AGT-09` | **9** | Poste Guichet & Contrôle : Prise de poste (`AGT-01`), Dashboard temps réel (`AGT-02`), Caisse tactile rapide FCFA (`AGT-03`), Encaissement espèces/MoMo & rendu monnaie (`AGT-04`), Scanner QR caméra/manuel (`AGT-05`), Matrice des 7 verdicts de contrôle (`AGT-06`), Recherche secours (`AGT-07`), Journal de vacation (`AGT-08`), Clôture contradictoire de caisse avec grille de billetage FCFA (`AGT-09`). |
| **6. `EXP`** | `EXP-01` à `EXP-07` | **7** | Gestion Opérationnelle : Météo & ouverture des 6 pôles (`EXP-01`), Planning & jauges (`EXP-02`), Instruction devis & proformas (`EXP-03`), Occupation Loges Ewondo/Chanthel/Bene (`EXP-04`), Précommandes cuisine 13h & Pergolas (`EXP-05`), Dossiers CFP (`EXP-06`), Guichet unique & Console de Closing WhatsApp (`EXP-07`). |
| **7. `DIR`** | `DIR-01` à `DIR-05` | **5** | Pilotage Exécutif : KPIs consolidés CA FCFA & fréquentation (`DIR-01`), Ventilation par canal Espèces/OM/MoMo/B2B (`DIR-02`), Analyse par pôle (`DIR-03`), RevPAR hôtelier & conversion B2B (`DIR-04`), Exports comptables CSV/PDF (`DIR-05`). |
| **8. `ADM`** | `ADM-01` à `ADM-08` | **8** | Administration Plateforme : Catalogue activités (`ADM-01`), Grille tarifaire & verrouillage tarif enfant (`ADM-02`), Quotas & fermetures (`ADM-03`), CMS éditorial & badges médias (`ADM-04`), Matrice RBAC 7 rôles (`ADM-05`), Paramètres légaux (`ADM-06`), Intégrations API clés masquées (`ADM-07`), Journal d'audit immuable SHA-256 (`ADM-08`). |

## Article 1.4 — Moteur de Billetterie QR Matriciel Autonome & Scanner Anti-Fraude à 7 Verdicts
1. **Génération de Billet QR Autonome (`RES-09`, `ACC-03`) :**
   - Chaque réservation confirmée ou pré-réservée génère un identifiant unique normalisé au format `^ECP-2026-[0-9]{5}$` (ex. `ECP-2026-84920`).
   - Le moteur embarqué dessine de manière déterministe une matrice SVG/Canvas haute densité intégrant les 3 motifs de positionnement standard (Finder Patterns `7x7`), l'horodatage, l'empreinte de contrôle et exportable hors-ligne en image PNG haute définition (`downloadOfflineQrTicketPng`) pour présentation au portail d'Ahala sans connexion Internet.
   - Tant que la passerelle de paiement n'est pas basculée en production bancaire définitive, chaque billet affiche le filigrane de sécurité obligatoire : **`BILLET DÉMONSTRATION — PROTOTYPE`**.
2. **Automate des 5 États de Paiement Mobile Money (`RES-08`, `RES-11`) :**
   - L'énumération SQL `payment_status` et l'automate frontal gèrent nativement les 5 états : `PENDING` (en attente de validation push USSD `#150#` Orange Money ou `*126#` MTN MoMo), `CONFIRMED` (confirmé par webhook signé), `FAILED` (solde insuffisant ou rejet opérateur), `EXPIRED` (délai USSD de 180 secondes dépassé) et `CANCELLED` (abandon client), avec reprise immédiate du panier sans ressaisie (`RES-11`).
3. **Scanner Anti-Fraude à 7 Verdicts (`AGT-05`, `AGT-06`) :**
   - Le contrôle d'accès aux tourniquets d'Ahala et à l'entrée de la Piscine Semi-Olympique évalue chaque code selon l'énumération stricte `qr_scan_verdict` comportant **7 verdicts exclusifs** :
     1. `VALID` (**1/7 — Billet valide**) : Autorisation d'entrée immédiate, décrémentation de la jauge disponible et horodatage atomique (`scanned = true`, `scannedAt = ISO-8601`).
     2. `USED` (**2/7 — Déjà utilisé**) : Blocage anti-rejeu immédiat (tentative de passage multiple avec le même QR code) en affichant l'heure exacte et le poste du premier scan.
     3. `WRONG_DATE` (**3/7 — Mauvaise date de visite**) : Billet valide mais émis pour une autre date que la date courante d'exploitation, avec proposition d'accès rapide au report de date (`ACC-05`).
     4. `EXPIRED` (**4/7 — Billet expiré**) : Date de validité révolue ou pré-réservation guichet de 11h00 non honorée dans le délai imparti (`hold_expires_at` dépassé).
     5. `CANCELLED` (**5/7 — Billet annulé**) : Billet ayant fait l'objet d'une annulation ou d'un remboursement Mobile Money (`RFD-2026-XXXX`).
     6. `WRONG_ZONE` (**6/7 — Prestation différente / Zone non incluse**) : Billet valide pour l'entrée Parc/Zoo (`500` / `1 000 FCFA`) présenté au point de contrôle de la Piscine Semi-Olympique (`1 500` / `2 500 FCFA`) ou d'une Cité Hôtelière sans que cette prestation figure dans `selected_activities`.
     7. `UNKNOWN` (**7/7 — Code QR inconnu**) : Référence inexistante ou signature altérée.

## Article 1.5 — Cache Hors-Ligne RN3 (`localStorage` + File `offlineScansQueue`)
Pour parer aux micro-coupures électriques (délestages ENEO) ou aux pertes de signal data mobile à l'entrée du parc d'Ahala Barrière :
1. Le poste agent (`AGT-01` à `AGT-09`) maintient en mémoire persistante navigateur (`localStorage`) un miroir chiffré/structuré de la liste des réservations attendues du jour (`EcoparkData.bookings`).
2. En cas de perte de connectivité réseau (`navigator.onLine === false` ou mode Hors-Ligne activé sur le terminal de contrôle), le scanner QR (`AGT-05`) bascule automatiquement et sans interruption sur la **validation locale instantanée**.
3. Chaque scan effectué hors-ligne horodate le billet localement (empêchant immédiatement un second passage sur le même terminal) et empile l'événement certifié dans la file persistante **`offlineScansQueue`** (`{ reference, scannedAt, agentPost, verdict, syncHash }`).
4. Dès le rétablissement de la liaison réseau avec Supabase, le démon de synchronisation vide de manière atomique et idempotente la file `offlineScansQueue`, met à jour la table `public.bookings` et inscrit une trace groupée dans `public.audit_logs` (`ADM-08`).

## Article 1.6 — Grille de Billetage Contradictoire en Coupures FCFA (`AGT-09`)
À chaque fin de vacation, l'écran de clôture de caisse (`AGT-09`) impose un comptage physique contradictoire des espèces en **Francs CFA BEAC (`XAF`)** avant toute validation :
1. **Ventilation par coupures officielles BEAC :** Saisie du nombre exact de billets et pièces pour les dénominations **`10 000 FCFA`**, **`5 000 FCFA`**, **`2 000 FCFA`**, **`1 000 FCFA`** et **`500 FCFA`** (billets/pièces).
2. **Calcul automatique de l'écart de caisse :** Le système compare la somme physique comptée au solde théorique des ventes espèces de la session (`Encaissements Espèces Guichet - Remboursements Espèces`).
3. **Seuil d'alerte critique à `2 000 FCFA` :**
   - Tout écart absolu strictement supérieur ou égal à **`2 000 FCFA`** (`|Écart| >= 2 000 FCFA`) déclenche automatiquement un **statut d'alerte rouge bloquant**, exige la saisie obligatoire d'un motif justificatif circonstancié par l'agent et le superviseur d'exploitation, génère un **Procès-Verbal de Clôture de Caisse PDF** (`printOfficialDocument`) et inscrit immédiatement une entrée critique dans le journal d'audit `ADM-08`.

## Article 1.7 — Schéma de Base de Données PostgreSQL / Supabase (8 Tables & RLS)
Le socle de données de production repose obligatoirement sur les **8 tables relationnelles** définies dans la migration officielle `supabase/migrations/20261026000001_ecopark_schema_rls.sql`, toutes protégées par **Row Level Security (`ENABLE ROW LEVEL SECURITY`)** :
1. `public.catalog_activities` : Catalogue des activités, pôles, jauges journalières et tarifs en FCFA, incluant la contrainte matérielle `chk_child_group_price_never_higher_than_individual CHECK (group_child_price_fcfa <= child_price_fcfa)`.
2. `public.sales_bundles` : Formules packagées coupe-file (`PASS_DECOUVERTE` à `2 500` / `1 500 FCFA`, `PASS_ROYALE` à `8 500` / `4 500 FCFA`, `PACK_COUPLE_EWONDO` à `45 000 FCFA`).
3. `public.lodge_cities` : Stock et tarification en temps réel des 3 cités hôtelières (`EWONDO` : 8 chambres de `25 000` à `30 000 FCFA` ; `CHANTHEL` : 12 chambres de `15 000` à `25 000 FCFA` ; `BENE` : 10 chambres de `10 000` à `15 000 FCFA`).
4. `public.bookings` : Réservations et billets QR (`ECP-2026-XXXXX`), états Mobile Money, verdicts de scan, gestion des pré-réservations 11h (`hold_expires_at`), reports de date à 90 jours (`rescheduled_from_date`, `reschedule_reason`) et remboursements (`refund_reference`, `refund_amount_fcfa`).
5. `public.group_quotes` : Demandes de devis groupes, écoles et séminaires (`DEV-2026-XXXX`) avec contrainte `CHECK (participants_count >= 10)`, option Salle *Menkii Essomba Anton* et navettes.
6. `public.cfp_applications` : Candidatures au CFP ECOPARK (`CFP-2026-XXXX`) avec contraintes strictes `CHECK (candidate_age >= 16)`, `CHECK (registration_fee_fcfa = 50000)` et `CHECK (tuition_fee_fcfa = 250000)`.
7. `public.appointments` : Prises de rendez-vous commercial, événementiel, scolaire et orientation CFP (`RDV-2026-XXXX`) sur les 4 créneaux garantis (`09h30`, `11h00`, `14h00`, `16h00`).
8. `public.audit_logs` : Journal d'audit immuable traçant toute opération sensible par acteur, rôle (`ecopark_role`) et horodatage serveur.

---

# CAHIER 2 — CCAG (CAHIER DES CLAUSES ADMINISTRATIVES GÉNÉRALES)

## Article 2.1 — Parties Contractantes et Hiérarchie des Pièces
Le présent marché est conclu entre **ECOPARK YAOUNDÉ**, représenté par son Promoteur **Dr Christophe FOE NDI** et son Gérant Délégué **M. Mgbatou Daryl**, d'une part, et l'agence d'ingénierie digitale **ONOGRAPH SARL**, d'autre part.
En cas de contradiction entre les documents, l'ordre de prévalence juridique décroissant est le suivant :
1. Le présent document regroupant les 6 Cahiers des Charges (`02_SUITE_CONTRACTUELLE_6_CDC.md`) ;
2. Le Contrat d'Interface Technique JSON Schema (`lead-and-ticket-schema.json`) ;
3. Le Schéma SQL et Règles RLS (`supabase/migrations/20261026000001_ecopark_schema_rls.sql`) ;
4. La Matrice de Couverture des 77 Écrans (`MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md`) ;
5. Le Cahier des Charges initial de Refonte 360° (`Cahier_des_Charges_Refonte_360_ECOPARK_Yaounde.md`).

## Article 2.2 — Cession Intégrale et Exclusive des Droits de Propriété Intellectuelle
Conformément aux dispositions de l'Accord de Bangui révisé (OAPI) et de la législation camerounaise sur le droit d'auteur et les droits voisins :
1. **Étendue de la cession :** Au fur et à mesure des paiements et de plein droit à la signature du Procès-Verbal de Réception Définitive, le Maître d'Œuvre (**ONOGRAPH SARL**) cède à titre **intégral, exclusif, définitif et irrévocable** au Maître d'Ouvrage (**ECOPARK YAOUNDÉ / Dr Christophe FOE NDI**) l'ensemble des droits patrimoniaux de propriété intellectuelle portant sur :
   - La totalité du **code source front-end et back-end** (`HTML5`, `CSS3`, `JavaScript ES2022+`, scripts d'automatisation, fonctions Edge/Serverless) ;
   - Les **Design Tokens, feuilles de style et composants UI/UX** de la direction artistique *« Canopée vivante — Le cercle du vivant »* (`DS-01` à `DS-08`) ;
   - Le **schéma de base de données relationnelle**, les migrations SQL, les politiques RLS et l'intégralité des données transactionnelles et analytiques collectées ;
   - Les **créations graphiques, plans d'orientation illustrés, photographies prises à Ahala, vidéos drone, supports d'impression (*Onoprint*) et contenus rédactionnels SEO**.
2. **Droits cédés :** Cette cession couvre les droits de reproduction, de représentation, d'adaptation, de modification, de traduction, d'hébergement, de distribution et d'exploitation commerciale sous toute forme, pour le **monde entier** et pour **toute la durée légale de protection de la propriété intellectuelle**.
3. **Neutralité de marque sur le Front-Office public (`DS-07`) :** Aucune signature publicitaire intrusive, bannière d'agence tierce ni mention propriétaire ne doit figurer dans l'en-tête (`header`) ou les écrans publics d'ECOPARK CAMEROUN.

## Article 2.3 — Clause de Réversibilité Totale et Absence de Verrouillage Propriétaire (Zero Vendor Lock-in)
1. **Standards ouverts exclusifs :** La plateforme est développée exclusivement sur des standards ouverts et auditables (HTML5/CSS3/JS natif, PostgreSQL standard, JSON Schema Draft 2020-12, export CSV/PDF universel). Aucun binaire obfusqué, CMS propriétaire verrouillé ou licence logicielle récurrente cachée ne peut être imposé au Maître d'Ouvrage.
2. **Dossier de Réversibilité Continuellement à Jour :** À tout moment, et sur simple notification écrite du Maître d'Ouvrage avec un préavis de **15 jours calendaires**, le Maître d'Œuvre s'engage à remettre sans frais supplémentaires un **Package de Réversibilité Complet** comprenant :
   - L'archive intégrale du dépôt Git avec historique complet des commits ;
   - Les scripts de migration SQL (`supabase/migrations/`) et un export intégral (`pg_dump` + fichiers CSV/JSON) des 8 tables de production ;
   - Les accès administrateur racine (`root` / `owner`) au nom de domaine, à l'hébergement Cloud/CDN, au projet Supabase et aux portails marchands MTN Mobile Money et Orange Money Cameroun ;
   - Une séance de transfert de compétences de **2 jours ouvrés** avec tout nouveau prestataire ou équipe interne désignée par le Dr Christophe FOE NDI.

## Article 2.4 — Planning d'Exécution, Pénalités de Retard et Plafond
1. **Respect des jalons :** Le calendrier d'exécution s'articule selon les jalons contractuels définis (correction des anomalies bloquantes sous **48 heures**, déploiement complet de la refonte et de la billetterie sur **90 jours**).
2. **Pénalités de retard :** En cas de dépassement d'une échéance contractuelle imputable exclusivement au Maître d'Œuvre, il sera appliqué de plein droit, et sans mise en demeure préalable, une pénalité forfaitaire égale à **`1/1000e` (0,1 %) du montant total hors taxes du marché par jour calendaire de retard**.
3. **Plafond des pénalités :** Le montant cumulé des pénalités de retard est plafonné à **`10 %` (dix pour cent)** du montant total hors taxes du marché. Au-delà de ce seuil, le Maître d'Ouvrage se réserve le droit de prononcer la résiliation du marché aux torts exclusifs du Titulaire.

## Article 2.5 — Procédure de Réception Contradictoire (VABF et VSR)
La recette du projet s'effectue en deux étapes contradictoires sanctionnées chacune par un Procès-Verbal signé par le Gérant Délégué (**M. Mgbatou Daryl**) et le Promoteur (**Dr Christophe FOE NDI**) :
1. **Vérification d'Aptitude et de Bon Fonctionnement (VABF — Recette Provisoire) :**
   - Inspection unitaire des **77 écrans contractuels** (`MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md` à `100 %`).
   - Test de bout en bout d'une réservation famille avec enfants (vérification du garde-fou tarif enfant à `500 FCFA`), émission du billet QR `ECP-2026-XXXXX`, simulation des **7 verdicts de scan** (`AGT-06`), test du mode hors-ligne (`offlineScansQueue`) et clôture de caisse contradictoire (`AGT-09`).
2. **Vérification de Service Régulier (VSR — Réception Définitive) :**
   - Période d'observation en conditions réelles d'exploitation à Ahala durant **30 jours calendaires consécutifs** incluant au moins **4 week-ends complets (samedis et dimanches)** sans incident bloquant non résolu dans les délais de GTR.

---

# CAHIER 3 — CCSE (CAHIER DES CLAUSES DE SÉCURITÉ ET D'EXPLOITATION)

## Article 3.1 — Conformité Légale et Réglementaire au Cameroun (Loi n° 2010/012)
L'architecture, l'hébergement et le traitement des données de la plateforme **ECOPARK CAMEROUN** respectent strictement :
1. La **Loi camerounaise n° 2010/012 du 21 décembre 2010** relative à la cybersécurité et à la cybercriminalité au Cameroun (notamment ses dispositions sur l'intégrité des systèmes d'information, la confidentialité des données à caractère personnel, la conservation des journaux de connexion et la valeur probante des écrits électroniques) ;
2. La **Loi n° 2010/013 du 21 décembre 2010** régissant les communications électroniques au Cameroun et les prescriptions de l'**ANTIC** (Agence Nationale des Technologies de l'Information et de la Communication) ;
3. La réglementation de la **CEMAC / BEAC** relative aux systèmes et moyens de paiement électronique (Mobile Money MTN / Orange Money).

## Article 3.2 — Politiques Row Level Security (RLS) sur PostgreSQL / Supabase
Aucune table de la base de données `public` ne peut être exposée sans politique **Row Level Security (RLS)** active :
1. **Tables de catalogue (`catalog_activities`, `sales_bundles`, `lodge_cities`) :** Lecture publique (`SELECT`) autorisée uniquement sur les offres actives (`is_active = TRUE`) ; écriture (`INSERT`, `UPDATE`, `DELETE`) strictement restreinte aux rôles authentifiés `responsable_exploitation` et `administrateur_plateforme`.
2. **Tables transactionnelles (`bookings`, `group_quotes`, `cfp_applications`, `appointments`) :**
   - Création unitaire contrôlée par validation de schéma et garde-fous SQL (`CHECK`).
   - Consultation par un visiteur (`visiteur_anonyme` / `client_connecte`) strictement limitée à son propre dossier via appariement exact du couple `(reference_code, visitor_phone)` ; **aucune requête client ne peut lister l'ensemble des réservations de la table**.
   - Mise à jour du statut de scan (`qr_status`, `scanned_at`, `scanned_by`) réservée aux rôles `agent_controle`, `agent_guichet` et `responsable_exploitation`.
3. **Table d'audit (`audit_logs`) :** Politique **Append-Only (`INSERT` uniquement)**. Les opérations `UPDATE`, `DELETE` et `TRUNCATE` sont formellement interdites à tous les rôles applicatifs, y compris `administrateur_plateforme`.

## Article 3.3 — Zéro Secret Exposé dans le Bundle Navigateur & Sécurité Mobile Money (`RES-08`, `ADM-07`)
1. **Absence totale de clés privées côté client :** Il est formellement interdit d'inclure dans le code HTML/JS distribué au navigateur :
   - La clé secrète **`SUPABASE_SERVICE_ROLE_KEY`** (seule la clé publique `ANON_KEY` bridée par RLS est autorisée côté client) ;
   - Les clés privées marchands **Orange Money WebPay API** ou **MTN MoMo Collection API** ;
   - Les identifiants SMTP ou jetons d'API WhatsApp Business Cloud.
2. **Masquage administratif (`ADM-07`) :** Sur l'écran d'administration des intégrations (`ADM-07`), toutes les clés d'API sont systématiquement obfusquées sous la forme `••••••••••••` et gérées exclusivement via des variables d'environnement serveur chiffrées (`Supabase Vault` / `Edge Functions Secrets`).
3. **Interdiction absolue de collecte de code PIN Mobile Money (`RES-08`) :** La plateforme web **ne demande jamais et ne comporte aucun champ permettant de saisir le code secret Mobile Money (PIN à 4 ou 5 chiffres)** du client. Le déclenchement du paiement s'opère exclusivement par notification Push USSD (`#150#` Orange Money ou `*126#` MTN Mobile Money) validée par le client directement sur le clavier sécurisé de son téléphone GSM, suivie d'une confirmation asynchrone par Webhook serveur signé HMAC-SHA256.

## Article 3.4 — Assainissement Systématique Anti-XSS et Validation des Entrées
1. Toutes les saisies issues des formulaires publics ou métiers (`RES-05`, `RES-06`, `PUB-12`, `PUB-18`, `AGT-07`, `EXP-07`) subissent un **assainissement systématique (Sanitization & HTML Entity Encoding)** avant stockage et avant toute injection dans le DOM, neutralisant les vecteurs d'attaque **Cross-Site Scripting (XSS)** (`<script>`, gestionnaires d'événements inline `onerror=`, URLs `javascript:`).
2. Toutes les charges utiles échangées entre le Frontend et la couche de données (`EcoparkData`) sont validées par rapport aux expressions régulières et bornes numériques du schéma **`lead-and-ticket-schema.json`** (validation stricte des numéros camerounais `^(\+?237)?(6[25-9][0-9]{7}|2[0-9]{8})$`, des identifiants `ECP-`, `DEV-`, `RDV-`, `CFP-` et des montants entiers positifs en FCFA).

## Article 3.5 — Contrôle d'Accès par Rôles (Matrice RBAC des 7 Rôles — `ADM-05`)
Le système applique le principe du moindre privilège à travers l'énumération stricte des **7 rôles contractuels (`ecopark_role`)** :
1. **`visiteur_anonyme`** : Consultation du site public (`PUB-01..22`), simulation budgétaire (`RES-01..04`), soumission de réservation/devis/RDV/candidature CFP (`RES-05..12`).
2. **`client_connecte`** : Droits du visiteur + accès à son portefeuille de billets QR, suivi de ses devis/RDV, report de date gratuit à 90 jours et demande de remboursement (`ACC-01..06`).
3. **`agent_guichet`** : Vente rapide au guichet, encaissement espèces/MoMo, émission de tickets thermiques/QR, journal de vacation et clôture contradictoire de caisse (`AGT-01..04`, `AGT-07..09`).
4. **`agent_controle`** : Scan de billets QR aux tourniquets et à la piscine, visualisation des 7 verdicts et synchronisation hors-ligne (`AGT-01`, `AGT-05..07`).
5. **`responsable_exploitation`** : Supervision quotidienne des 6 pôles, gestion des jauges, instruction des devis B2B/écoles, planning des Loges Ewondo/Chanthel/Bene, précommandes cuisine 13h, dossiers CFP et Console de Closing WhatsApp (`EXP-01..07` + supervision `AGT`).
6. **`direction`** : Tableaux de bord exécutifs du Promoteur Dr Christophe FOE NDI et du Gérant Délégué, suivi consolidé des recettes FCFA par canal, RevPAR hôtelier et exports comptables CSV/PDF (`DIR-01..05`).
7. **`administrateur_plateforme`** : Paramétrage du catalogue, de la grille tarifaire (sous contrainte du garde-fou tarif enfant), des quotas, du CMS, des rôles utilisateurs, des passerelles API et consultation du journal d'audit (`ADM-01..08`).

## Article 3.6 — Journal d'Audit Immuable Chaîné par Hachage SHA-256 (`ADM-08`)
Toute action sensible exécutée sur la plateforme (modification d'un tarif dans `ADM-02`, changement de jauge dans `ADM-03`, émission d'un remboursement `RFD-2026-XXXX` dans `ACC-05`, validation d'un devis dans `EXP-03`, clôture de caisse ou alerte d'écart `>= 2 000 FCFA` dans `AGT-09`) génère automatiquement un enregistrement dans `public.audit_logs` (`ADM-08`).
Chaque entrée d'audit comporte une **empreinte cryptographique SHA-256 chaînée** calculée sur la concaténation de l'empreinte de l'entrée précédente (`prev_hash`), de l'horodatage UTC ISO-8601, de l'identifiant de l'acteur (`actor_name`), de son rôle (`actor_role`), du code d'action (`action_code`) et du détail de l'opération, garantissant la détection immédiate de toute tentative d'altération postérieure.

---

# CAHIER 4 — CCÉDITORIAL (CAHIER DES CLAUSES ÉDITORIALES & RÈGLES MÉTIER)

## Article 4.1 — Exclusivité Absolue du Franc CFA (`FCFA` / `XAF`)
1. **Unité monétaire unique :** L'intégralité des prix, tarifs, simulateurs, devis proforma, paniers, menus du restaurant *Le Château des Saveurs*, nuitées hôtelières, frais de scolarité CFP, tableaux de bord et exports comptables est exprimée **exclusivement en Francs CFA (`FCFA` / code ISO 4217 `XAF`)**, sous forme de nombres entiers séparés par une espace insécable pour les milliers (ex. `1 500 FCFA`, `25 000 FCFA`, `250 000 FCFA`).
2. **Tolérance zéro devise étrangère :** La présence d'un seul montant en dollars américains (`$`, `USD`), en euros (`€`, `EUR`) ou d'un texte résiduel de template anglophone non traduit (tel que l'ancienne anomalie `Velvet Flat White $4.50` ou le bouton `Submit`) sur l'un quelconque des 77 écrans constitue un **motif de rejet immédiat de recette**.

## Article 4.2 — Règle Immuable de Sanctuarisation du Tarif Enfant (`RES-03`, `ADM-02`)
Afin de protéger le pouvoir d'achat des familles camerounaises et des établissements scolaires en excursion à Ahala :
1. **Tranches d'âge officielles :**
   - **Tout-petits (`< 3 ans`) :** Accès **100 % GRATUIT (`0 FCFA`)** au Parc et au Jardin Zoologique.
   - **Enfants (`3 à 12 ans inclus`) :** Tarif réduit sanctuarisé.
   - **Adultes (`13 ans et plus`) :** Tarif standard.
2. **Sanctuarisation mathématique et contractuelle :**
   - Le tarif d'entrée au Parc & Jardin Zoologique pour un enfant (3–12 ans) est fixé à **`500 FCFA`** (contre `1 000 FCFA` pour un adulte en individuel et `700 FCFA` pour un adulte en groupe `>= 10 personnes`).
   - **Invariance de la règle anti-erreur :** Lorsqu'une réservation ou une excursion dépasse le seuil de groupe (`>= 10 participants`), **le tarif enfant ne peut en aucun cas basculer au tarif groupe adulte de `700 FCFA`**. Le tarif enfant en groupe doit toujours satisfaire l'inégalité stricte :
     $$\text{group\_child\_price\_fcfa} \le \text{child\_price\_fcfa}$$
   - Cette règle est verrouillée à la fois dans le moteur de calcul JavaScript (`RES-03`), dans l'interface d'administration (`ADM-02`) et au niveau du moteur PostgreSQL via la contrainte `chk_child_group_price_never_higher_than_individual`.
3. **Tarification Piscine Semi-Olympique (`PUB-06`, `PUB-10`, `RES-03`) :**
   - Adulte : **`2 500 FCFA`** (et `2 000 FCFA` en tarif groupe adulte).
   - Enfant (3–12 ans) : **`1 500 FCFA` en Semaine Promotionnelle (Mardi–Vendredi)** et **`2 500 FCFA` les Week-ends (Samedi–Dimanche) & Jours Fériés**.

## Article 4.3 — Terminologie Officielle du CFP ECOPARK Agréé MINEFOP (`PUB-12`, `EXP-06`)
Toute communication et tout formulaire relatifs au **Centre de Formation Professionnelle (CFP) d'ECOPARK** respectent scrupuleusement la nomenclature officielle agréée par le **MINEFOP (Ministère de l'Emploi et de la Formation Professionnelle)** :
1. **Diplômes délivrés :** **DQP** (*Diplôme de Qualification Professionnelle*) et **CQP** (*Certificat de Qualification Professionnelle*), formation d'une durée de **12 mois** structurée à **70 % de pratique intensive sur les infrastructures réelles d'ECOPARK Ahala** et 30 % de théorie.
2. **Les 5 Filières officielles (orthographe contrôlée) :**
   1. **Hôtellerie** (gestion des hébergements, réception, gouvernance sur les Cités Ewondo, Chanthel et Bene) ;
   2. **Restauration** (arts culinaires camerounais et internationaux au *Château des Saveurs*) ;
   3. **Décoration** (événementiel, scénographie de mariages, galas et séminaires à la Salle *Menkii Essomba Anton*) ;
   4. **Production Agropastorale** (agriculture intégrée et élevage — *interdiction absolue des coquilles « Agropostale » ou « Agropatoral »*) ;
   5. **Pisciculture** (aquaculture, gestion des étangs de production et reproduction d'Ahala).
3. **Conditions d'admission et tarification CFP :**
   - Âge minimum requis du candidat : **`>= 16 ans`** révolus à la date de candidature (`CHECK (candidate_age >= 16)`).
   - **Frais d'inscription :** **`50 000 FCFA`** payables par MTN Mobile Money, Orange Money ou au guichet.
   - **Frais de scolarité annuelle :** **`250 000 FCFA`**, payables soit intégralement (total `300 000 FCFA` inscription incluse), soit selon l'échéancier officiel en **4 tranches** : **`100 000 FCFA` + `50 000 FCFA` + `50 000 FCFA` + `50 000 FCFA`**.

## Article 4.4 — Horaires d'Ouverture, Fermeture Hebdomadaire du Lundi et Ancrage Local
1. **Jours et horaires d'ouverture du Parc :** ECOPARK CAMEROUN est ouvert au public du **Mardi au Dimanche, de `09h00` à `18h00`** (avec prolongations événementielles les vendredis et week-ends ainsi qu'un accueil `24h/24` pour les résidents des Cités Hôtelières Ewondo, Chanthel et Bene).
2. **Fermeture hebdomadaire du Lundi :** Le Parc de loisirs et le Jardin Zoologique sont **fermés au public tous les lundis** pour entretien écologique, soins vétérinaires de la faune, traitement des bassins et maintenance préventive (hors jours fériés tombant un lundi ou privatisation B2B exceptionnelle autorisée dans `ADM-03`). Le calendrier de réservation (`RES-02`) signale explicitement cette règle.
3. **Transparence Photographique (`DS-04`, `PUB-14`, `ADM-04`) :** Chaque visuel affiché sur la plateforme porte un badge d'origine explicite distinguant les **Photographies Réelles d'ECOPARK Yaoundé-Ahala** (`Photo réelle ECOPARK Ahala`) des visuels d'illustration contextualisés Cameroun dans l'attente du renouvellement photographique complet.

---

# CAHIER 5 — CCGRAPHIQUE (CAHIER DES CLAUSES GRAPHIQUES & ACCESSIBILITÉ)

## Article 5.1 — Direction Artistique Validée : « Canopée vivante — Le cercle du vivant »
L'identité visuelle numérique d'ECOPARK CAMEROUN applique sans dérogation la direction artistique officielle **« Canopée vivante — Le cercle du vivant »** (`DESIGN.md` et `DS-01` à `DS-08`), inspirée de la lumière naturelle filtrant à travers la canopée forestière d'Ahala Barrière et de la géométrie circulaire du logo historique d'ECOPARK.

## Article 5.2 — Intégrité Absolue du Logo Original `EcoPark CAMEROUN` (`DS-01`)
1. Le logo officiel circulaire **`EcoPark CAMEROUN`** (`cropped-LOGO-ECOPARK-Youtube.png`) est un actif patrimonial intouchable.
2. Il doit **toujours** être présenté sur un **disque ou cartouche de fond blanc pur (`#FFFFFF`)** garantissant sa lisibilité, entouré d'une zone de protection minimale égale à `25 %` de son diamètre.
3. Il est formellement interdit de redessiner sa typographie, de modifier ses couleurs intrinsèques, de l'écraser homothétiquement ou de l'apposer directement sur un fond sombre ou photographique sans son médaillon blanc protecteur.

## Article 5.3 — Règle Chromatique `60-30-10` et Tokens CSS Officiels (`DS-02`, `DS-04`)
La répartition chromatique de chaque écran respecte rigoureusement l'équilibre lumineux **`60 % — 30 % — 10 %`** afin de garantir une fraîcheur visuelle optimale et une lisibilité parfaite en extérieur :
1. **`60 %` — Surfaces Claires Dominantes (Lumière & Respiration) :**
   - Blanc pur (`--color-white: #FFFFFF`) pour le fond principal des pages et des cartes.
   - Vert Brume Végétale très doux (`--color-surface-soft: #EDF4E7`) pour les sections alternées et les encadrés de respiration.
2. **`30 %` — Structure Botanique & Typographie Forestière :**
   - Vert Forêt Profond (`--color-brand-deep: #1D490D`) pour la structuration identitaire, les en-têtes majeurs et les boutons d'action primaires (avec texte `#FFFFFF`).
   - Encre Carbone Végétal (`--color-text: #1E281B`) pour le corps de texte haute lisibilité.
3. **`10 %` — Accents Vivants & Signalétique Métier :**
   - Vert Feuille Vivante (`--color-brand-leaf: #1F880B`) pour les états actifs, bordures de sélection et indicateurs de vitalité.
   - Ocre Bronze Cameroun (`--color-accent-ochre: #C47D2B`) réservé exclusivement aux badges de distinction VIP (Cité Ewondo, Pass Journée Royale, étiquettes patrimoniales).
   - **Interdiction stricte des boutons jaunes en action principale (`DS-04`) :** Aucun bouton d'appel à l'action primaire (CTA) ne peut utiliser un fond jaune ou orangé criard dégradant le contraste du texte.

## Article 5.4 — Typographies Officielles et Rayons Asymétriques « Feuille » (`DS-02`, `DS-03`)
1. **Couple typographique obligatoire :**
   - Titres, montants FCFA et navigation structurante : **`Barlow Semi Condensed`** (graisses `600 SemiBold` et `700 Bold`).
   - Corps de texte, formulaires, tableaux de gestion et descriptions : **`Source Sans 3`** (graisses `400 Regular`, `600 SemiBold`).
   - Références de billets (`ECP-2026-XXXXX`), codes d'audit et horodatages : police chasse fixe (`JetBrains Mono` / `monospace`).
2. **Géométrie des composants (`DS-03`) :**
   - Grille fluide **12 colonnes** centrée (`max-width: 1280px`), échelle d'espacement modulaire de base `4px / 8px`.
   - Rayons de courbure standards des cartes et champs : `8px`, `12px` et `16px`.
   - **Cadrage organique « Feuille » (`border-radius: 32px 8px 32px 8px`) :** réservé exclusivement aux cadres photographiques mis en avant, avec interdiction absolue des découpes en forme de pilules (`border-radius: 999px`) qui mutilaient autrefois les photos du site.

## Article 5.5 — Interdiction Stricte des Emojis OS Colorés & Iconographie 100 % SVG (`DS-04`)
1. **Zéro Emoji OS Coloré (`0` caractère Unicode `> U+25FF`) :** Afin d'éviter toute dissonance esthétique entre Android, iOS et Windows et de préserver le standing institutionnel d'ECOPARK CAMEROUN, **aucun emoji système coloré (plage Unicode strictement supérieure à `U+25FF`, tels que les pictogrammes cartoon `🌴`, `🦁`, `🏊`, `✅`, `⚠️`) n'est toléré dans le code source ni dans les interfaces des 77 écrans**.
2. **Iconographie 100 % SVG Linéaire Monochrome :** Tous les pictogrammes d'interface, de météo, de faune, de paiement et de statut sont réalisés exclusivement en **SVG vectoriel linéaire monochrome** partageant une épaisseur de trait constante **`stroke-width="1.75"`**, `stroke-linecap="round"`, `stroke-linejoin="round"` et héritant dynamiquement de `currentColor`.

## Article 5.6 — Accessibilité WCAG 2.2 Niveau AA en Plein Soleil Tropical (`DS-02`, `DS-05`)
Compte tenu de l'utilisation des smartphones par les visiteurs et les agents de contrôle en extérieur sous l'ensoleillement zénithal de Yaoundé :
1. **Ratio de contraste minimal :** Tout texte standard présente un ratio de contraste minimal de **`4.5:1`** (et **`>= 7:1` — niveau AAA** pour le couple `#1E281B` sur `#FFFFFF` à `15.2:1`, ainsi que `#FFFFFF` sur `#1D490D` à `10.4:1`).
2. **Zones tactiles ergonomiques :** Tous les boutons, compteurs `- / +`, filtres et champs de saisie (`DS-05`) respectent une hauteur minimale de cible tactile de **`48px x 48px`** pour prévenir les erreurs de saisie à une main.
3. **Double codage des verdicts (`AGT-06`) :** Aucun des 7 verdicts du scanner QR ne repose uniquement sur la couleur ; chacun associe un fond à haut contraste, une bordure distinctive, une icône SVG explicite (`stroke-width="1.75"`), un libellé textuel en capitales et un code d'action clair.

---

# CAHIER 6 — CCTMA (CAHIER DES CLAUSES DE TIERCE MAINTENANCE APPLICATIVE & SLA)

## Article 6.1 — Engagements de Niveau de Service (SLA) et Périodes Critiques d'Affluence à Ahala
Le Maître d'Œuvre s'engage sur des indicateurs de disponibilité et de réactivité renforcés, particulièrement durant les **périodes de pointe d'exploitation touristique à Ahala Barrière (Samedis, Dimanches, Mercredis après-midi, Jours Fériés camerounais et Vacances Scolaires)** :

| Indicateur Contractuel (SLA) | Seuil d'Engagement Opposable | Plage de Mesure & Pénalité Spécifique |
| :--- | :--- | :--- |
| **Taux de Disponibilité Mensuel de la Plateforme** | **`>= 99,9 %`** | Mesuré `24h/24, 7j/7` (indisponibilité cumulée maximale autorisée : `< 43 minutes / mois`). |
| **GTI (Garantie de Temps d'Intervention) — Critique (P1)** | **`< 30 minutes`** | Prise en charge effective par un ingénieur d'astreinte les **Samedis, Dimanches et Jours Fériés (`08h00–19h00`)** ainsi qu'en semaine. |
| **GTR (Garantie de Temps de Rétablissement) — Critique (P1)** | **`< 2 heures` (`120 min`)** | Rétablissement complet du service (ou activation d'un contournement opérationnel sans perte de recette) pour tout incident bloquant la billetterie, le paiement Mobile Money ou le scan QR le week-end. |
| **GTI / GTR — Incident Majeur non bloquant (P2)** | **GTI `< 2 heures` / GTR `< 8 heures`** | Anomalie dégradant une fonctionnalité secondaire (ex. filtre galerie, export PDF isolé) sans interrompre les encaissements. |
| **GTI / GTR — Anomalie Mineure ou Cosmétique (P3)** | **GTI `< 24 heures` / GTR `< 72 heures`** | Correction orthographique, ajustement d'alignement CSS ou mise à jour éditoriale. |

## Article 6.2 — Périmètre des 3 Maintenances (Corrective, Préventive et Évolutive)
1. **Maintenance Corrective (Garantie & TMA) :**
   - Diagnostic, isolation et correction définitive de tout bogue logiciel, régression d'interface sur l'un des 77 écrans, erreur de calcul budgétaire ou dysfonctionnement des webhooks MTN Mobile Money / Orange Money.
   - Incluse gratuitement à **100 % pendant les 3 premiers mois** suivant la réception définitive, puis dans le cadre du forfait TMA.
2. **Maintenance Préventive & Sécuritaire :**
   - Surveillance proactive des certificats SSL/TLS, de la latence de l'API Supabase et de l'intégrité des politiques RLS.
   - Mise à jour mensuelle des dépendances de sécurité, vérification trimestrielle de la chaîne de hachage SHA-256 du journal d'audit (`ADM-08`) et tests de charge avant chaque grande fête nationale ou période de fin d'année (Décembre / Janvier à Yaoundé).
3. **Maintenance Évolutive & Accompagnement Éditorial :**
   - Mise à jour des tarifs saisonniers, ajout de nouvelles formules packagées dans `public.sales_bundles`, publication des programmations événementielles hebdomadaires (`PUB-15`, `PUB-16`) et intégration des nouvelles photographies officielles d'Ahala fournies par la Direction.

## Article 6.3 — Politique de Sauvegarde Quotidienne et Plan de Reprise d'Activité (PRA)
1. **Sauvegardes automatisées quotidiennes (Point-in-Time Recovery) :**
   - L'intégralité des **8 tables PostgreSQL/Supabase** (`catalog_activities`, `sales_bundles`, `lodge_cities`, `bookings`, `group_quotes`, `cfp_applications`, `appointments`, `audit_logs`) ainsi que les fichiers médias font l'objet d'une **sauvegarde automatique chiffrée (AES-256) quotidienne à `02h00` (heure de Yaoundé, `UTC+1`)** avec rétention glissante sur **30 jours minimum** et archivage mensuel externe.
2. **Objectifs de Reprise (RPO & RTO) :**
   - **RPO (Recovery Point Objective — Perte de données maximale admissible) :** **`< 15 minutes`** grâce à la journalisation continue (WAL) et à la persistance locale de secours (`localStorage` / `offlineScansQueue`) sur les terminaux du guichet d'Ahala.
   - **RTO (Recovery Time Objective — Délai maximal de remontée complète après sinistre majeur) :** **`< 2 heures`**.
3. **Test semestriel de restauration :** Le Titulaire exécute tous les 6 mois un exercice réel de restauration des sauvegardes sur un environnement de pré-production isolé et transmet le rapport de validation à la Direction d'ECOPARK YAOUNDÉ.

---
**Fait à Yaoundé, en double exemplaire original et numérique certifié, pour valoir contrat opposable entre les parties.**

- **Pour le Maître d'Ouvrage — ECOPARK YAOUNDÉ :** Dr Christophe FOE NDI (Promoteur) & M. Mgbatou Daryl (Gérant Délégué)
- **Pour le Maître d'Œuvre — ONOGRAPH SARL :** La Direction Technique & Juridique
