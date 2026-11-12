# 🔄 03 - WORKFLOWS OPÉRATIONNELS, ONBOARDING ANTI-MÉFIANCE & BASCULEMENT J-0 (`03_WORKFLOWS_ONBOARDING_ET_BASCULEMENT_J0.md`)

* **Projet** : **ECOPARK CAMEROUN (Yaoundé - Ahala, RN3)**
* **Objectif** : Procédures *Si / Alors* sans jargon, rituel d'adhésion des équipes terrain, prise en main du CMS `/admin` en `< 60 secondes` et protocole de basculement en production (*Cutover J-0*).

---

## 1. Arbres de Décision Opérationnels (*Si / Alors*) par Pôle

### 1.1 Portail & Contrôle QR (`AGT-05` / `AGT-06`)
* **SI** le scan affiche le bandeau vert **`VALID (ACCÈS AUTORISÉ)`** -> **ALORS** remettre le bracelet couleur correspondant au Pass et inviter le visiteur à entrer.
* **SI** le scan affiche le bandeau rouge **`USED (DÉJÀ SCANNÉ)`** -> **ALORS** lire l'heure exacte du 1er passage affichée à l'écran, refuser l'entrée et orienter calmement vers le Guichet #1.
* **SI** le scan affiche **`WRONG_DATE` (Mauvaise date pour cause de pluie)** -> **ALORS** vérifier la Garantie Pluie 30 jours et valider le report sans supplément.
* **SI** la connexion 3G/4G coupe au portail -> **ALORS** continuer à scanner normalement : la file `offlineScansQueue` enregistre chaque passage en local, bloque les doublons et synchronise dès le retour du réseau (`syncOfflineScans()`).

### 1.2 Guichet Caisse POS & Clôture Contradictoire (`AGT-03` / `AGT-09`)
* **SI** un client paie en espèces FCFA au guichet -> **ALORS** sélectionner les prestations dans `AGT-03`, encaisser, cliquer sur `Émettre Ticket Espèces FCFA` et remettre le reçu imprimé `80 mm` muni de son QR Code.
* **SI** en fin de journée (`18h30`), l'écart entre le comptage physique des coupures BEAC (`physicalCashTotal`) et le théorique (`theoreticalCashTotal`) dépasse **`2 000 FCFA`** -> **ALORS** le bouton de clôture reste verrouillé jusqu'à saisie du motif justificatif et double signature sur le **PV de Clôture A4**.

### 1.3 Exploitation, Commandes & Fiches de Mission A4 (`EXP-01` à `EXP-06`)
* **SI** une réservation loge (`EWONDO`, `SUITES_PRIVEES`, `CHANTHEL`, `BENE`) ou un devis groupe est confirmé -> **ALORS** le système génère automatiquement la **Fiche de Mission A4 (`1 Commande = 1 Fiche de Mission`)** et déclenche une alerte sur le poste concerné.
* **SI** l'agent prend en charge la mission -> **ALORS** il clique sur `Acquitter l'alerte` et signe le **Visa #2** (statut passe à `EN_COURS`).
* **SI** la prestation est terminée et conforme -> **ALORS** le Responsable d'Exploitation signe le **Visa #3** et attribue la note superviseur `/40` (complétant le score automatique `/60` pour un total sur **`100 points`**).

---

## 2. Rituel Psychologique d'Onboarding Anti-Méfiance (Terrain Cameroun)

> **Principe Directeur** : Un outil digital imposé comme un « flicage » est saboté ; un outil présenté comme un **bouclier qui protège l'agent honnête et récompense son excellence** est adopté en 24 heures.

1. **Message d'ouverture du Promoteur (Dr Christophe FOÉ NDI)** :
   * *« Ce système ne vient pas surveiller des suspects : il vient protéger chaque caissière, chaque contrôleur et chaque chef de pôle contre les fausses accusations et les litiges clients. Quand votre caisse est juste et que vos missions sont signées, le logiciel prouve votre professionnalisme noir sur blanc. »*
2. **Mécanisme de la Prime Mensuelle d'Excellence Opérationnelle (30 Jours Zéro Écart)** :
   * Chaque agent cumule un score objectif sur `/100` (`#expAgentRatingsCardsGrid`).
   * Tout agent maintenant **30 jours consécutifs sans écart de caisse non justifié (`> 2 000 FCFA`)** et une moyenne `>= 90 / 100` sur ses Fiches de Mission A4 est automatiquement inscrit au **Palmarès d'Excellence RH** et éligible à la prime mensuelle de performance.

---

## 3. Guide d'Autonomie du Back-Office CMS `/admin` (`< 60 Secondes`)

| Action Souhaitée | Écran `/admin` | Manipulation en 3 Clics (`< 60s`) |
| :--- | :--- | :--- |
| **Mettre un plat en rupture à 14h00** | `ADM-04` (Agenda & Carte) | Cliquer sur le bouton **`En stock / En rupture`** face au plat (ex. *Poisson Braisé d'Ahala*) -> le simulateur public grise immédiatement l'option. |
| **Ajuster la jauge Piscine d'un samedi** | `ADM-03` (Jauges & Météo) | Saisir la capacité du jour (ex. `60`) sur la ligne *Piscine* et cliquer sur **`Enregistrer`**. |
| **Changer le bandeau météo d'Ahala** | `ADM-03` (Jauges & Météo) | Choisir le préréglage (`Ensoleillé 27°C`, `Affluence Week-end`, `Garantie Pluie`) et cliquer sur **`Publier le bandeau`**. |
| **Préparer puis publier un nouveau tarif** | `ADM-01` (Catalogue & Pass) | 1. *Exploitation* clique sur `Dupliquer`, saisit le nouveau prix et enregistre le **Brouillon**. 2. *Direction (MFA)* clique sur **`Publier`** -> remplace l'offre en ligne sans changer l'URL. |
| **Répondre en 1 clic à un Devis sur WhatsApp** | `ADM-09` (Inbox Leads) | Cliquer sur **`Relancer WhatsApp`** face au dossier -> ouvre WhatsApp pré-rempli avec le numéro et le récapitulatif du client. |

---

## 4. Protocole de Basculement J-0 (*Cutover*) & Marche en Double Commande (48h)

1. **H-24 avant Basculement (Figement & Balance d'Ouverture)** :
   * Vérifier les 14 tarifs du catalogue (`ADM-01`), les 4 cités hôtelières (`ADM-02`) et les 5 plats (`ADM-04`).
   * Saisir le fond de caisse initial BEAC dans `AGT-09` et exporter un premier **Journal Général SYSCOHADA CSV** (`DIR-05`) comme point zéro.
2. **J-0 à 08h30 (Ouverture Officielle des Postes)** :
   * Connexion des agents par matricule (`MAT-GUI-01`, `MAT-CTL-02`, `MAT-EXP-01`, `MAT-CPT-01`, `MAT-DIR-01`).
   * Vérification d'un scan QR test et purge immédiate des données de test via `EcoparkData.purgeTestQaResidues()`.
3. **J-0 et J+1 (Marche en Double Commande pendant 48h - Samedi & Dimanche)** :
   * Conservation parallèle de la souche papier de secours pendant les 2 premiers jours de week-end uniquement.
   * À `18h30` chaque soir : rapprochement entre le PV de Clôture A4 généré par `AGT-09` et les espèces physiques BEAC.
   * À `20h00` : envoi du **Condensé Exécutif WhatsApp** au Dr Christophe FOÉ NDI (`sendExecutiveWhatsAppDigest20h()`).
