---
name: ecopark-audit-remediation
description: Audit technique, UX/UI, SEO et éditorial du site actuel ecopark-yaounde.com avec la liste exhaustive des 21+ pages vides, bugs critiques, liens localhost, textes anglais oubliés et plan de remédiation. À utiliser pour corriger le site ou documenter l'audit client.
---

# Audit Digital & Plan de Remédiation : `ecopark-yaounde.com`

## 1. Synthèse de l'Existant Technique
- **CMS actuel** : WordPress 7.1.3 (Thème bloc `event-managerial-service` + plugin `Essential Blocks` + `WooCommerce 11.2.1` + `WPForms Lite` + `LWS Optimize`).
- **Diagnostic global** : Le site souffre d'un inachèvement majeur (> 60 % de pages vides, textes de démonstration en anglais avec prix en dollars, balise `<title>` vide, liens `localhost`, absence de billetterie malgré WooCommerce) qui pénalise directement le lancement de la dynamique **« ECOPARK NEW LOOK »**.

## 2. Les 8 Anomalies Critiques Identifiées (Preuves d'Audit)

### Cas n°1 : Plus de 21 pages du menu principal sont des « Coquilles Vides »
Ces pages sont publiées et accessibles dans le menu, mais ne contiennent qu'une bannière H2 et un bloc `<div class="wp-block-column"></div>` vide :
- **Section À Propos** : `/notre-histoire/`, `/notre-mission/`, `/nature-biodiversite/`, `/patrimoine-culture/`, `/nos-engagements/`
- **Section Agenda** : `/agenda/`, `/evenements-2/`, `/programme-du-mois/`, `/programme-du-week-end/`, `/evenements-passes/`
- **Section Offres & Fidélité** : `/offres-promotions/`, `/club-ecopark/`, `/presentation-2/`, `/inscription/`, `/avantages/`, `/mon-compte/`
- **Section Packs** : `/nos-packs/`, `/pack-couple/`, `/pack-ecole/`, `/pack-enfant/`, `/pack-entreprise/`, `/pack-sejour/` *(seuls `/pack-anniversaire/` et `/pack-famille/` ont du contenu)*
- **Section Services & Formation** : `/formation/`, `/filieres/`, `/agropastoral/`, `/decoration/`, `/hotellerie/`, `/pisciculture/`, `/restauration/`, `/transport/`, `/balade-en-foret/`

### Cas n°2 : Page `/restaurant/` polluée par un template de café américain en Dollars (`USD`)
- Après une courte introduction en français sur le *Château des Saveurs*, la page affiche le template anglophone non nettoyé :
  - Titres : *« Small-batch roasts, every day »*, *« Roasted in-house »*, *« Baked every morning »*, *« Made for lingering »*.
  - Faux menu : *« Velvet Flat White 4.50 USD »*, *« Butter Croissant 3.80 USD »*, *« The Morning Plate 12.00 USD »*.
  - Faux avis (*« Maya R. — regular since 2019 »*) et fausse adresse (*« On the corner of 5th and Main »*).

### Cas n°3 : Page `/nos-tarifs/` cassée & Commentaires de détresse sur `/contact/`
- La page `/nos-tarifs/` contient une balise `<img class="wp-image-987">` **sans attribut `src`** : la grille tarifaire est invisible.
- Sur `/contact/`, le bloc de commentaires WordPress a été laissé actif : des clients (ex. *Charlotte Manuella*) y réclament publiquement les prix d'entrée et de pique-nique.

### Cas n°4 : Lien `http://localhost/ecopark/#` & Compte à rebours expiré sur l'Accueil
- Le sous-titre Hero principal (*« Une Destination Unique À Yaoundé–Ahala... »*) est un lien pointant vers `http://localhost/ecopark/#`.
- Un compte à rebours affiche `00 JOURS 00 HEURES 00 MINUTES 00 SECONDES` en permanence.
- Le compteur statistique indique *« 50,000+ Utilisateurs Actifs »* (jargon logiciel inadapté à un parc écotouristique).

### Cas n°5 : Oublis d'édition Gutenberg dans les articles officiels
- L'article phare *« ECOPARK NEW LOOK : Cérémonie d'installation de la nouvelle équipe dirigeante »* contient en plein texte le placeholder Gutenberg non supprimé : **`Saisissez ici votre paragraphe`**.
- Tous les articles sont signés par le compte technique `Transistor` et certains permaliens sont numériques (`/2026/10/01/1744/`).

### Cas n°6 : Coquilles orthographiques sur les visuels & le formulaire `/preinscription/`
- Affiche du Centre de Formation en page d'accueil : *« Centre de **Fomation** Professionnelle »* (oubli du `r`) et *« filière **Agropostale** »* (au lieu d'*Agropastorale*).
- Formulaire `/preinscription/` : libellé cassé *« naissance Filière de »*, coquille *« Agropatoral »*, date en format américain `MM/DD/YYYY`, bouton `Submit` en anglais.

### Cas n°7 : Défaillance critique du SEO Technique
- Balise `<title>` de la page d'accueil réduite à un simple tiret **`-`** (Nom du site vide dans WordPress).
- Aucune balise `<meta name="description">`.
- 29 images sur 44 en page d'accueil n'ont pas d'attribut `alt`.

### Cas n°8 : Absence de Billetterie en ligne & Dispersion des contacts
- WooCommerce est chargé sur toutes les pages (ralentissant le site à ~20s de chargement initial) mais **aucun billet, hôtel ou pack n'est réservable en ligne**.
- **5 numéros de téléphone différents** sont dispersés sans guichet unique : `+237 672 56 45 98`, `+237 677 51 03 48`, `+237 698 13 11 34`, `+237 677 48 69 86`, `+237 675 76 34 94` / `+237 658 56 41 02`.

## 3. Règles de Validation avant toute Mise en Production (Checklist Qualité)
- [ ] Aucune page du menu ne doit être publiée sans contenu complet, visuels optimisés (WebP < 150 Ko) et appel à l'action (CTA).
- [ ] Zéro texte en anglais non traduit (*Submit*, *Cookie Consent*, placeholders de thème).
- [ ] Zéro lien `localhost` ou `#` mort.
- [ ] Orthographe irréprochable sur les termes clés : **Formation**, **Agropastorale**, **Pisciculture**, **Écotourisme**.
- [ ] Balises `<title>`, `<meta description>`, OpenGraph et Schema.org (`TouristAttraction`, `Hotel`, `Restaurant`, `EducationalOrganization`) renseignées sur chaque page.
