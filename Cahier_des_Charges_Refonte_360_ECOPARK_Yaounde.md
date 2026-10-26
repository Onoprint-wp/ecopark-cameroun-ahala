# CAHIER DES CHARGES TECHNIQUE, FONCTIONNEL & CRÉATIF (CDC)
## Projet : Refonte Digitale 360°, Billetterie Mobile Money & Concierge IA — « ECOPARK NEW LOOK »

- **Maître d'Ouvrage (Client) :** **ECOPARK YAOUNDÉ** — Quartier Ahala Barrière (Face Station Tradex), Yaoundé
  - **Promoteur :** Dr Christophe FOE NDI
  - **Gérant Délégué (« ECOPARK NEW LOOK ») :** M. Mgbatou Daryl
- **Maître d'Œuvre (Agence) :** **ONOGRAPH SARL** (*« L'Architecte Invisible de l'Influence Visible »*) — Simbock, Yaoundé (`www.onograph.online` | `+237 6 70 72 80 87` | `info@onograph.online`)
- **Référence Document :** `CDC-ONO-ECOPARK-2026-10`
- **Prototype Associé :** [`Prototype_Interactif_ECOPARK_NEW_LOOK.html`](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/Prototype_Interactif_ECOPARK_NEW_LOOK.html)

---

## 1. CONTEXTE ET OBJECTIFS STRATÉGIQUES DU PROJET

Le **16 septembre 2026**, lors de l'installation officielle de la nouvelle équipe dirigeante d'ECOPARK Yaoundé (**dynamique « ECOPARK NEW LOOK »** pilotée par **M. Mgbatou Daryl**), le Promoteur **Dr Christophe FOE NDI** a fixé quatre objectifs prioritaires :
1. **Déployer une communication plus dynamique et moderne** ;
2. **Renforcer massivement la visibilité d'ECOPARK** à Yaoundé et au Cameroun ;
3. **Fidéliser durablement les visiteurs** (familles, entreprises, écoles, touristes) ;
4. **Augmenter directement la fréquentation et le chiffre d'affaires** sur l'ensemble des pôles (Loisirs, Hôtellerie, Restauration, Événementiel, Formation Professionnelle).

Or, l'audit technique réalisé en octobre 2026 sur la plateforme `https://ecopark-yaounde.com` a mis en évidence **7 anomalies critiques** qui bloquent aujourd'hui la conversion commerciale :
- **Anomalie #1 :** Lien principal de la bannière Hero pointant vers `http://localhost/ecopark/#` et balise SEO `<title>-</title>` réduite à un simple tiret.
- **Anomalie #2 :** Compteur expiré à `00:00:00:00`, jargon SaaS *« 50,000+ Utilisateurs Actifs »*, photos déformées en forme de pilules et fautes d'orthographe sur l'affiche officielle du CFP (*« Centre de Fomation »*, *« Agropostale »*).
- **Anomalie #3 :** **Plus de 21 pages du menu principal sont totalement vides** (`<div class="wp-block-column"></div>`), soit plus de 60 % du site (`/pack-entreprise/`, `/pack-ecole/`, `/notre-histoire/`, `/formation/`, `/hotellerie/`, `/transport/`, etc.).
- **Anomalie #4 :** La page `/restaurant/` (*Le Château des Saveurs*) affiche un template américain non nettoyé en anglais avec des prix en dollars (`Velvet Flat White $4.50`, `Butter Croissant $3.80`, `5th and Main`).
- **Anomalie #5 :** La page `/nos-tarifs/` charge une balise `<img class="wp-image-987">` sans attribut `src` (page blanche), obligeant les clients (ex. *Charlotte Manuella*) à réclamer les tarifs en commentaire public sur `/contact/`.
- **Anomalie #6 :** L'article officiel du 18 septembre 2026 annonçant *ECOPARK NEW LOOK* contient en plein milieu le texte par défaut *« Saisissez ici votre paragraphe »* et est signé `Transistor`.
- **Anomalie #7 :** Le formulaire `/preinscription/` du CFP comporte un libellé inversé (*« naissance Filière de »*), une faute à *« Agropatoral »*, un bouton non traduit *« Submit »* et aucune option de paiement Mobile Money.

Le présent **Cahier des Charges (CDC)** définit les spécifications exactes que couvre notre **Prototype Interactif (`Prototype_Interactif_ECOPARK_NEW_LOOK.html`)** et qui seront déployées en production.

---

## 2. PÉRIMÈTRE FONCTIONNEL EN 6 LOTS OPÉRATIONNELS

### LOT 1 — Refonte de l'Architecture Web & Rédaction des 21+ Pages Vides (35 Pages)
1. **Correction chirurgicale immédiate (Sous 48h) :**
   - Suppression du lien `http://localhost/ecopark/#`, du compteur `00:00:00:00`, du texte *« Saisissez ici votre paragraphe »* et du template anglais/USD sur `/restaurant/`.
   - Fermeture et nettoyage des commentaires parasites sur les pages statiques (`/contact/`).
   - Remplacement du compte auteur `Transistor` par **« Direction de la Communication ECOPARK »**.
2. **Rédaction SEO & Habillage Visuel des 21+ Pages Vides :**
   - **Pôle Institutionnel :** `/notre-histoire/`, `/notre-mission/`, `/nature-biodiversite/`, `/patrimoine-culture/`, `/nos-engagements/`.
   - **Pôle Agenda & Fidélité :** `/agenda/`, `/programme-du-mois/`, `/programme-du-week-end/`, `/offres-promotions/`, `/club-ecopark/`.
   - **Pôle Packs (7 Pages de Vente) :** `/pack-entreprise/`, `/pack-ecole/`, `/pack-famille/`, `/pack-couple/`, `/pack-enfant/`, `/pack-detente/`, `/pack-sejour/`.
   - **Pôle Formation (CFP) :** `/formation/`, `/filieres/`, `/agropastoral/`, `/hotellerie/`, `/pisciculture/`, `/preinscription/`.
   - **Pôle Logistique :** `/transport/` (présentation et réservation des navettes de 5, 18 et 32 places).

---

### LOT 2 — Moteur de Billetterie, Calculateur de Budget & Paiement Mobile Money (`/nos-tarifs/`)
1. **Grille Tarifaire Officielle Interactive (100 % en FCFA) :**
   - Affichage clair des tarifs **Enfants**, **Adultes** et **Groupes (dès 10 personnes)**.
2. **Calculateur Dynamique de Sortie :**
   - Bascule **Semaine (Mardi–Vendredi)** vs **Week-end & Jours Fériés** ajustant automatiquement le tarif Enfant de l'Espace Piscine Moderne (`1 500 FCFA` en semaine / `2 500 FCFA` le week-end).
   - Détection automatique du seuil **Groupe (≥ 10 visiteurs)** appliquant la remise de **-30 %** sur le Parc Animalier/Zoo (`700 FCFA`), la Pirogue (`700 FCFA`), le Cheval (`700 FCFA`) et la Forêt/Musée (`500 à 700 FCFA`).
3. **Encaissement Mobile Money & Billet QR Code :**
   - Intégration passerelle de paiement **MTN Mobile Money & Orange Money Cameroun**.
   - Génération automatique d'un **E-Billet PDF / QR Code** envoyé instantanément sur le WhatsApp et l'email du client pour contrôle rapide à l'entrée d'Ahala.

---

### LOT 3 — Module Gastronomie (*Le Château des Saveurs*) & Réservation des 3 Hôtels
1. **Carte Digitale Interactive du Restaurant `/restaurant/` :**
   - Suppression complète des éléments américains en dollars (`$4.50`, `$3.80`).
   - Catalogue filtrable en **FCFA** : *Poissons frais des étangs d'Ahala braisés*, *Poulet DG*, *Grillades & Brochettes*, *Boissons & Rafraîchissements*, *Formules Buffets Groupes & Mariages*.
   - Module de réservation de table ou de **Pergola privée au bord du lac**.
2. **Système de Booking pour les 3 Hôtels d'ECOPARK (`/hebergement/`) :**
   - **Hôtel EWONDO (Standing Prestige) :** 4 Suites + 4 Mini-suites climatisées (`25 000 – 30 000 FCFA / nuitée`).
   - **Hôtel CHANTHEL (Standing Confort) :** 12 Chambres confortables (`15 000 / 20 000 / 25 000 FCFA / nuitée`).
   - **Hôtel BENE (Séjour Nature Accessible) :** Chambres économiques (`10 000 – 15 000 FCFA / nuitée`).
   - Calendrier de disponibilité, sélection du nombre de nuitées et paiement d'acompte ou totalité via Mobile Money.

---

### LOT 4 — Configurateur Devis B2B / Écoles & Portail Digital du CFP d'Ecopark
1. **Configurateur de Devis Instantané B2B & Scolaire :**
   - Calculateur de devis proforma pour les **Séminaires d'Entreprises, Ministères et ONG** (location de la **Salle de conférence *Menkii Essomba Anton***, pauses-café, déjeuner au *Château des Saveurs*, activités Team Building).
   - Calculateur pour les **Sorties Scolaires** (forfait élève + réservation des bus navettes de **5, 18 ou 32 places**).
2. **Refonte du Tunnel d'Inscription au CFP (`/preinscription/`) :**
   - Correction orthographique intégrale (*« Centre de Formation Professionnelle »*, *« Production Agropastorale »*, *« Filière souhaitée »*, bouton *« Valider ma préinscription »*).
   - Présentation détaillée des **5 filières DQP/CQP (12 mois, 70 % pratique)** : *Hôtellerie, Restauration, Décoration, Production Agropastorale, Pisciculture*.
   - Paiement Mobile Money des frais d'inscription (**`50 000 FCFA`**) et affichage de l'échéancier des 4 tranches de scolarité (**`250 000 FCFA`** : `100 000` + `50 000` + `50 000` + `50 000 FCFA`).

---

### LOT 5 — Guichet Unique & Concierge IA WhatsApp 24/7 (« ONOGRAPH IA Inside »)
1. **Unification des 5 Numéros Téléphoniques :**
   - Centralisation des 5 numéros actuels derrière un **Guichet Unique WhatsApp Business** et un widget web actif 24h/24 et 7j/7.
2. **Entraînement sur la Base de Connaissances Officielle (`ecopark-context`) :**
   - Réponse instantanée (`< 5 secondes`) aux questions sur les tarifs en FCFA, l'itinéraire exact (*Quartier Ahala Barrière, face station Tradex*), les horaires (*Mardi–Dimanche dès 09h00*), les chambres d'hôtel et le CFP.
   - Escalade automatique vers un conseiller humain pour les grands événements (mariages, séminaires > 50 personnes).

---

### LOT 6 — Design System « Nature & Prestige », Performances & Rebranding Print
1. **Charte Graphique & UI Mobile-First (`ecopark-design-system`) :**
   - Palette officielle : Vert Canopée (`#0D5C3A`), Or Savane (`#D97706`), Bleu Lagon (`#0284C7`), Terre Cacao (`#5A1830`), Fond Crème (`#F8FAFC`).
   - Lisibilité maximale en plein soleil sur smartphone (contraste WCAG AA/AAA) et grilles photos haute définition `16:10` / `4:3` (suppression des découpes en pilules qui écrasent les visuels).
2. **Exigences Techniques & SEO Local :**
   - Temps de chargement initial `< 2,0 secondes` sur réseau mobile 3G/4G au Cameroun (images WebP/AVIF).
   - Balisage complet `Schema.org` (`TouristAttraction`, `Hotel`, `Restaurant`, `EducationalOrganization`) et optimisation Google Business Profile sur Yaoundé.
3. **Supports Print & Signalétique (*Onoprint*) :**
   - Livraison des fichiers HD et impression : nouvelle affiche CFP sans faute, carte plastifiée du *Château des Saveurs* en FCFA, plaquette commerciale B2B et **Plan illustré d'orientation du Parc**.

---

## 3. PLANNING DE LIVRAISON (90 JOURS) & GARANTIES ONOGRAPH

| Phase | Délai | Livrables Clés | Critère de Validation (Recette) |
| :--- | :--- | :--- | :--- |
| **Phase 1 : Quick Wins** | **J+1 à J+7 (Urgences en 48h)** | Suppression du lien `localhost`, du café US en dollars, réparation de `/nos-tarifs/` et de l'affiche CFP. | 0 lien cassé, 0 prix en dollars, grille FCFA en ligne. |
| **Phase 2 : Contenus & Design** | **Semaines 2 à 3** | Charte *ECOPARK NEW LOOK*, shooting photo/drone à Ahala, rédaction et mise en ligne des 21 pages vides. | 35/35 pages du menu complètes et illustrées. |
| **Phase 3 : Billetterie MoMo** | **Semaines 4 à 6** | Moteur de réservation (Pass activités, 3 Hôtels, 7 Packs, CFP) avec paiement MTN MoMo & Orange Money + QR Code. | Transaction test MoMo/OM + réception du billet QR Code. |
| **Phase 4 : Concierge IA** | **Semaines 6 à 7** | Déploiement du Chatbot IA Web & WhatsApp 24/7 unifiant les 5 numéros de téléphone. | Temps de réponse `< 5s` avec 100 % d'exactitude tarifaire. |
| **Phase 5 : Campagne 360°** | **Semaines 8 à 10** | Lancement média TikTok/FB/IG + Journée VIP avec 5 à 10 influenceurs de Yaoundé à Ahala. | Hausse mesurable du trafic web et des réservations week-end. |
| **Phase 6 : Transfert & ROI** | **Semaines 11 à 12** | Formation de l'équipe interne d'ECOPARK + livraison du Dashboard KPIs temps réel + 3 mois de maintenance. | Procès-verbal de réception définitive. |
