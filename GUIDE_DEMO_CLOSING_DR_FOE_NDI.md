# PROTOCOLE DE DÉMONSTRATION LIVE EN 7 MINUTES (STYLE KEYNOTE)
## Destinataires : Dr Christophe FOE NDI (Promoteur ECOPARK) & M. Mgbatou Daryl (Directeur du Parc)
**URL de Production :** [`https://ecopark-cameroun-ahala.vercel.app`](https://ecopark-cameroun-ahala.vercel.app)

---

## Objectif Stratégique de la Démonstration
Ne pas présenter une « liste technique d'écrans », mais prouver en direct sur l'écran du Promoteur que la nouvelle plateforme résout ses **3 enjeux financiers et opérationnels immédiats** :
1. **Zéro coulage de caisse au portail d'Ahala** grâce au Billet QR à contrôle unique (`1er scan = Valide`, `2e scan = Rejet automatique`).
2. **Remplissage des Loges (Ewondo, Chanthel, Bene) et de la Salle « Menkii Essomba Anton » en semaine** grâce aux modules **Prendre RDV (`/rdv`)** et **Facture Proforma Groupe en 2 minutes**.
3. **Visibilité comptable instantanée le dimanche soir** grâce au **PV de Clôture de Caisse PDF** et à l'**Export CSV (Excel)** en 1 clic.

---

## Déroulé Chronométré en 5 Actes (7 Minutes)

### ACTE 1 — L'Électrochoc Visuel & La Réassurance Ahala (00:00 → 01:15)
**Action à l'écran :** Ouvrir [`https://ecopark-cameroun-ahala.vercel.app/`](https://ecopark-cameroun-ahala.vercel.app/)
1. Pointer le **bandeau météo & trafic en direct** tout en haut (`En direct d'Ahala Barrière (RN3 Face Tradex) : 27 °C Ensoleillé • Accès RN3 Fluide • Garantie Pluie : Report Gratuit 1 Clic`).
2. Cliquer sur les miniatures du **Hero 50/50** (*Lac & Pirogues*, *Piscine & Eau*, *Saveurs & Loges*) pour montrer l'animation **HyperFrames** synchronisée avec les cartes de prix en **FCFA** (`500 / 1 000 FCFA`, `1 500 / 2 500 FCFA`, `10 000 – 30 000 FCFA`).
3. Descendre jusqu'au **Plan Vectoriel SVG Interactif d'Ahala** (`#sec-PUB-13`) et cliquer sur **`Animer l'itinéraire A → E`**, puis ouvrir une photo de la galerie en **Plein Écran HD (Lightbox Liquid Glass)**.
- **Phrase clé au Promoteur :** *« Finis les faux prix en dollars (`\$4.50`) et les 21 pages vides de l'ancien site. En 3 secondes, une famille de Yaoundé voit le vrai lac d'Ahala, le gorille "ToTo", la météo sur place et les vrais tarifs en FCFA. »*

---

### ACTE 2 — La Machine à Cash Famille & L'Anti-Fraude au Tourniquet (01:15 → 03:15)
**Action à l'écran :** Cliquer sur **`Réserver & Billets`** dans l'en-tête (`#sec-RES-03`).
1. Cliquer en 1 clic sur le bouton **`Pass Journée Royale (Repas inclus) — 8 500 / 4 500 FCFA`** : montrer l'**odomètre cinétique FCFA** qui anime instantanément le total et la règle de protection : **« Entrée enfant garantie à 500 FCFA »**.
2. Dans les options à la carte, sélectionner :
   - **Spécialité Château des Saveurs** : `Poulet DG Royal & Plantain Mûr` • `Service 13h30` (zéro attente en cuisine).
   - **Navette Climatisée Yaoundé** : `Carrefour Bastos (Départ 09h15)`.
3. Cliquer sur **`Générer & Enregistrer mon Billet QR`** : le Pass 3D façon Apple Wallet se déplie avec son code unique (`ECP-2026-XXXXX`) accompagné de la **Carte de Soulagement Dopaminergique Post-Formulaire** (`#dopamineReliefCard`) et du bouton **Pont Direct WhatsApp 1-Clic** (`+237 697 13 62 03`).
4. Cliquer sur **`Télécharger Pass QR Hors-Ligne (Image PNG)`** : montrer que le visiteur repart avec son billet enregistré en image dans son téléphone, utilisable même s'il n'a plus de forfait Internet en arrivant à Ahala Barrière.
5. **Le Moment de Vérité (Anti-Coulage, Mode Hors-Ligne RN3 & Billetage FCFA) :**
   - Cliquer sur le bouton flottant en bas à droite **`Mode Démo & Back-Office (77 Écrans)`** $\rightarrow$ aller sur **`Guichet / Contrôle (AGT-05)`** (ou ouvrir `/guichet`).
   - Cliquer une **1re fois** sur **`Vérifier dans la BDD`** : l'écran affiche en vert **`1/7 • BILLET VALIDE — AUTORISER L'ENTRÉE`**.
   - Cliquer une **2e fois** sur le même bouton 2 secondes plus tard : l'écran vire au rouge **`2/7 • BILLET DÉJÀ UTILISÉ — REFUSER L'ENTRÉE`** avec l'heure exacte du 1er passage.
   - Basculer le commutateur **`Mode Hors-Ligne RN3`** : prouver que même en cas de coupure 3G/4G à Ahala Barrière, le tourniquet continue de scanner les billets en cache local et synchronise la file d'attente au retour du réseau.
   - Montrer la **Grille de Billetage Contradictoire en coupures FCFA (`AGT-08`)** (`10 000`, `5 000`, `2 000`, `1 000`, `500 FCFA`) qui calcule l'écart en temps réel et déclenche une alerte d'audit dès `2 000 FCFA` d'écart.
- **Phrase clé au Promoteur :** *« Aucun billet papier ne peut plus être revendu deux fois à l'entrée, même si la connexion Internet coupe sur la RN3, et chaque coupure FCFA en caisse est comptée contradictoirement. »*

---

### ACTE 3 — Le Moteur B2B : Écoles, Ministères, ONG & Mariages (03:15 → 04:45)
**Action à l'écran :** Cliquer sur **`Prendre RDV`** puis sur **`Devis Groupe`** dans l'en-tête.
1. Dans **`Prendre RDV`** (`/rdv`), sélectionner **`Repérage Mariage & Réception`** (Salle Polyvalente *Menkii Essomba Anton*), choisir le créneau **`11h00 – 12h00`** et cliquer sur **`Confirmer mon RDV`** (`RDV-2026-XXXX`).
2. Ouvrir **`Devis Groupe`** : sélectionner **`Séminaire Ministère / ONG / Entreprise`** (ou *Excursion scolaire*), saisir `60 participants`, cocher la **Navette Climatisée 32 places**, puis cliquer sur **`Imprimer / PDF Proforma`**.
3. Montrer la **Facture Proforma Officielle** générée instantanément avec le détail en FCFA, prête à être signée par un directeur d'école ou un ministère.

---

### ACTE 4 — Le Campus CFP Agréé MINEFOP & La Garantie Pluie Yaoundé (04:45 → 05:45)
**Action à l'écran :** Aller sur **`Formation CFP`** puis sur **`Mon Espace`**.
1. Ouvrir la candidature **CFP ECOPARK** : montrer les **5 filières officielles** (*Hôtellerie, Restauration, Décoration, Agropastorale, Pisciculture*), les frais officiels (`50 000 FCFA` d'inscription + `250 000 FCFA` payables en **4 tranches**) et le contrôle réglementaire MINEFOP ($\ge 16\text{ ans}$).
2. Ouvrir **`Mon Espace`** (`#view-ACC`) :
   - Filtrer par **`Dossiers CFP`**, **`RDV`** ou **`Billets QR`**, ou taper une référence dans le champ de recherche (`RES-12`).
   - Cliquer sur **`Reporter date`** sur un billet (`ACC-05`) : montrer la **Garantie Pluie / Météo Yaoundé (Report gratuit en 1 clic)** qui rassure les familles hésitant à réserver en saison des pluies.

---

### ACTE 5 — Le Poste de Commandement du Promoteur à 18h00 (05:45 → 07:00)
**Action à l'écran :** Basculer sur **`Exploitation (EXP-07)`**, **`Direction (DIR-01 / DIR-05)`** (`/direction`) puis **`Admin / CMS (ADM-09)`** (`/admin`).
1. Dans **`EXP-07`**, montrer la **Console de Closing WhatsApp en 1 Clic** (`+237 697 13 62 03`) qui permet à l'équipe d'envoyer un billet QR, une Proforma PDF ou de bloquer une Suite VIP à la **Cité Ewondo (`25 000 – 30 000 FCFA`)**.
2. Dans **`ADM-09 (Inbox Unifiée des Leads & Billets en 1 Clic)`**, montrer que tous les flux entrants (`Billets QR`, `Devis B2B`, `RDV`, `Candidatures CFP`) arrivent dans une boîte unique filtrable où le Gérant change le statut (`Nouveau` $\rightarrow$ `Confirmé` $\rightarrow$ `Traité`) en 1 clic avec traçabilité dans le journal d'audit SHA-256 (`ADM-08`).
3. Dans **`DIR-01`**, cliquer sur **`Rapport Exécutif Imprimable (DIR-05)`** pour afficher le **Procès-Verbal de Clôture de Caisse Contradictoire**.
4. Cliquer sur **`Exporter Base Complète CSV (Excel)`** : ouvrir le fichier `.csv` téléchargé dans Microsoft Excel devant le Promoteur.
- **Conclusion de Closing :** *« Docteur, tout ce que vous venez de voir tourne déjà en direct sur `ecopark-cameroun-ahala.vercel.app`, accompagné des 6 Cahiers des Charges contractuels, des Design Tokens W3C et du cahier d'impression Onoprint pour vos panneaux RN3 et vos menus. Dès votre validation, nous branchons vos comptes marchands Orange Money / MTN MoMo et nous basculons sur votre domaine `ecopark-yaounde.com`. »*
