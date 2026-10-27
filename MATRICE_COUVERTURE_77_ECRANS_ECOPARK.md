# Matrice de Couverture Contractuelle — 77 Écrans & Design System ECOPARK
**Direction artistique validée :** « Canopée vivante — Le cercle du vivant »  
**Projet Google Stitch MCP :** [`projects/522000543872634848`](https://stitch.withgoogle.com/projects/522000543872634848?pli=1) — *ECOPARK Yaoundé Interactive Prototype*  
**Design System Stitch :** `assets/b1b40a03aba8496187426e4b86791929` (*Canopée Vivante — Barlow Semi Condensed + Source Sans 3 — `#FFFFFF` / `#1D490D` / `#1F880B` / `#EDF4E7` / `#1E281B`*)  
**Prototype Interactif Local :** [`Prototype_Interactif_ECOPARK_NEW_LOOK.html`](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/Prototype_Interactif_ECOPARK_NEW_LOOK.html)  
**Spécification Design System :** [`DESIGN.md`](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/DESIGN.md)

---

## 1. Synthèse de Couverture par Famille (77 IDs Contractuels)

| Famille | Plage d'IDs | Nombre d'écrans | Écran Stitch MCP de référence (`projectId: 522000543872634848`) | Vue & Inspecteur dans le Prototype Interactif Local | Statut |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **1. Design System & Bibliothèque** | `DS-01` à `DS-08` | **8** | `screens/3187720b20ab494fa69cdab177ea818b` (*DS-01 à DS-08 — Design System & Bibliothèque ECOPARK*) | Onglet **Design System (`DS-01..08`)** + `DESIGN.md` | ✅ 100 % |
| **2. Site Public** | `PUB-01` à `PUB-22` | **22** | `screens/7025c0b5991843d5930f95919096c5ef` (*PUB-01 Accueil Maître Cameroun*) & `screens/c5af5fe0f7c0444782f3c4afcf9d2640` (*PUB-03 à PUB-20 Catalogue, Tarifs, Hôtels, Restauration, CFP*) | Onglets **Site Public (`PUB-01..22`)** avec sous-navigation complète | ✅ 100 % |
| **3. Préparation, Devis & Réservation** | `RES-01` à `RES-12` | **12** | `screens/5a2ed012815b4b75b3431d49da1f9607` (*Préparer ma Visite*) & `screens/40df1022e39742a4b04d1a1aafd5565d` (*RES-01 à RES-12 & ACC-01 à ACC-06*) | Onglet **Visite, Devis & Billetterie (`RES-01..12`)** | ✅ 100 % |
| **4. Espace Visiteur / Client** | `ACC-01` à `ACC-06` | **6** | `screens/40df1022e39742a4b04d1a1aafd5565d` (*RES-01 à RES-12 & ACC-01 à ACC-06 — Réservation, Billet QR & Espace Visiteur*) | Onglet **Espace Visiteur (`ACC-01..06`)** | ✅ 100 % |
| **5. Guichet & Contrôle des Entrées** | `AGT-01` à `AGT-09` | **9** | `screens/770c3f5f3c804ed18e0c545d3c53f8c1` (*AGT-01 à AGT-09 & EXP-01 à EXP-07 — Espace Guichet & Exploitation*) | Onglet **Guichet & Scan QR (`AGT-01..09`)** | ✅ 100 % |
| **6. Exploitation & Gestion Opérationnelle** | `EXP-01` à `EXP-07` | **7** | `screens/770c3f5f3c804ed18e0c545d3c53f8c1` (*AGT-01 à AGT-09 & EXP-01 à EXP-07 — Espace Guichet & Exploitation*) | Onglet **Exploitation (`EXP-01..07`)** | ✅ 100 % |
| **7. Pilotage & Direction** | `DIR-01` à `DIR-05` | **5** | `screens/2e7d3d78ae00442f864fc298980ef37e` (*DIR-01 à DIR-05 & ADM-01 à ADM-08 — Direction & Administration*) | Onglet **Direction (`DIR-01..05`)** | ✅ 100 % |
| **8. Administration de la Plateforme** | `ADM-01` à `ADM-08` | **8** | `screens/2e7d3d78ae00442f864fc298980ef37e` (*DIR-01 à DIR-05 & ADM-01 à ADM-08 — Direction & Administration*) | Onglet **Administration (`ADM-01..08`)** | ✅ 100 % |
| **TOTAL CONTRACTUEL** | **`DS` + `PUB` + `RES` + `ACC` + `AGT` + `EXP` + `DIR` + `ADM`** | **77** | **7 planches maîtresses + 6 médias locaux Cameroun dans Stitch** | **77 vues inspectables individuellement + 5 états transverses + 7 rôles** | ✅ **77 / 77** |

---

## 2. Détail Unitaire des 77 Écrans Contractuels

### Famille 1 — Design System & Bibliothèque (`DS-01` à `DS-08`)
| ID | Intitulé officiel | Contenu & Règles vérifiées | Médias / Références |
| :--- | :--- | :--- | :--- |
| `DS-01` | Couverture, principes graphiques et règles d'usage du logo | Logo circulaire original `EcoPark CAMEROUN` sur disque blanc, zone de protection, interdiction de refonte typographique ou de fond sombre altérant le disque. | `cropped-LOGO-ECOPARK-Youtube.png` |
| `DS-02` | Couleurs, contrastes, typographies et échelle de texte | `--color-white: #FFFFFF`, `--color-brand-deep: #1D490D`, `--color-brand-leaf: #1F880B`, `--color-surface-soft: #EDF4E7`, `--color-text: #1E281B`. Contrastes WCAG AA/AAA vérifiés. `Barlow Semi Condensed` + `Source Sans 3`. | `DESIGN.md` §3-4 |
| `DS-03` | Grille, espacements, rayons, ombres et motifs végétaux | Grille 12 colonnes (max `1280px`), base `4px/8px`, rayons standards `8px/12px/16px`, cadrage asymétrique feuille `32px 8px 32px 8px` réservé aux photos, motif SVG radial léger. | `DESIGN.md` §5 |
| `DS-04` | Boutons, liens, badges, étiquettes et icônes | Primaire `#1D490D` texte `#FFFFFF`, secondaire `#FFFFFF` bordure `#1D490D` (aucun bouton jaune en action principale). Badges de statut et badges d'origine photo. | `DESIGN.md` §6.1-6.2 |
| `DS-05` | Champs de formulaire, sélecteurs, calendrier, compteurs et messages de validation | Champs `48px`, compteurs `- / +` avec règle anti-erreur tarif enfant, calendrier de visite, messages d'erreur explicites. | `DESIGN.md` §6.3 |
| `DS-06` | Cartes d'offre, cartes d'hébergement, tableaux de tarifs, accordéons, onglets et modales | Cartes activités avec prix FCFA lisible, cartes loges Ewondo/Chanthel/Bene, tableaux comparatifs, modales de détail. | `DESIGN.md` §6.4 |
| `DS-07` | En-tête, navigation principale, navigation mobile, fil d'Ariane et pied de page | En-tête public épuré (sans barre d'administration ni marque d'agence tierce), menu mobile tiroir, fil d'Ariane, pied de page Ahala. | `DESIGN.md` §6.5 |
| `DS-08` | Composants métier : simulateur, panier, billet QR de démonstration, carte de contrôle d'entrée, indicateurs et tableaux de gestion | Simulateur budgétaire FCFA, billet QR (`BILLET DÉMONSTRATION — PROTOTYPE`), scanner 7 états, KPIs d'exploitation. | `DESIGN.md` §6.6 |

### Famille 2 — Site Public (`PUB-01` à `PUB-22`)
| ID | Intitulé officiel | Contenu & Ancrage Local Cameroun | Photo locale associée |
| :--- | :--- | :--- | :--- |
| `PUB-01` | Accueil | Hero lumineux en canopée à Yaoundé-Ahala, horaires `09h00–18h00`, 6 pôles d'expérience, accès direct simulateur FCFA. | `balade_pirogue3.jpg` (Réelle) + `local_cameroon_family_canopy.png` |
| `PUB-02` | Découvrir ECOPARK : présentation, plan d'orientation illustré et engagements | Vision du complexe agro-écotouristique d'Ahala Barrière, plan illustré des 6 zones (Zoo, Lac, Piscine, Saveurs, Loges, CFP). | `IMG_20260829_172016-1-scaled.jpg` (Réelle) |
| `PUB-03` | Catalogue des expériences et activités avec filtres | Filtres par public (Famille, Enfants, Groupes, Détente), prix FCFA clairs dès la carte. | `balade_pirogue3.jpg`, `chimpanze.jpeg` (Réelles) |
| `PUB-04` | Fiche détail d'une activité ou expérience | Fiche détaillée (ex. Balade en pirogue sur le lac d'Ahala : `500 FCFA` enfant / `1 000 FCFA` adulte, gilets fournis, horaires). | `balade_pirogue3.jpg` (Réelle) |
| `PUB-05` | Nature, faune et espaces de découverte | Jardin zoologique et botanique : chimpanzés, tortues géantes, autruches, paons, antilopes, sensibilisation écologique. | `chimpanze.jpeg` (Réelle) + `local_cameroon_gorilla_sanctuary.png` |
| `PUB-06` | Loisirs aquatiques et activités de plein air | Piscine semi-olympique (`1 500` / `2 500 FCFA`), pédalo, équitation (`500` / `1 000 FCFA`), manèges enfants. | `local_cameroon_pool_pirogue.png` |
| `PUB-07` | Restauration et espaces de détente | *Le Château des Saveurs* — gastronomie camerounaise authentique en `FCFA` (poisson braisé d'Ahala, plantains mûrs, Ndolè, poulet DG). Zéro faux menu en dollars. | `IMG-20260713-WA0051_043420.jpg` (Réelle) + `local_cameroon_gastronomy_pergola.png` |
| `PUB-08` | Hébergement : vue d'ensemble | Présentation comparative des 3 cités hôtelières : Loges **Ewondo**, **Chanthel** et **Bene** (`10 000` à `30 000 FCFA`). | `chambre.jpeg` (Réelle) |
| `PUB-09` | Fiche détail d'une formule d'hébergement | Détail Loge **Ewondo** (`25 000 FCFA` Standard / `30 000 FCFA` VIP, climatisation, petit-déjeuner, accès parc). | `chambre.jpeg` (Réelle) |
| `PUB-10` | Tarifs, formules et conditions | Grille officielle complète en `FCFA` : Zoo (`500`/`1 000`), Piscine (`1 500`/`2 500`), Pirogue/Cheval (`500`/`1 000`), Packs Famille & Groupes. | — |
| `PUB-11` | Groupes, écoles, entreprises et événements | Offres B2B & scolaires : excursions pédagogiques maternelles/primaires/collèges, séminaires d'entreprise, mariages, arbres de Noël. | `IMG-20260809-WA0009.jpg` (Réelle) + `local_cameroon_school_excursion.png` |
| `PUB-12` | Formation professionnelle : présentation, filières, conditions et candidature | **CFP ECOPARK** (Autorisation MINEFOP) : Aquaculture, Hôtellerie-Restauration, Agriculture/Élevage (`50 000 FCFA` inscription + `250 000 FCFA` scolarité). | `1786968889976.jpg` (Réelle) + `local_cameroon_cfp_students.png` |
| `PUB-13` | Informations pratiques : horaires, accès, localisation, conseils de visite et météo indicative | Accès N3 Yaoundé–Douala (Ahala Barrière, après station Tradex), parking gratuit, météo locale Yaoundé. | — |
| `PUB-14` | Galerie média | Photothèque filtrable distinguant explicitement les photos réelles d'ECOPARK et les visuels d'illustration temporaires. | Toutes les photos réelles + locales |
| `PUB-15` | Actualités ou événements | Programmation culturelle, vacances scolaires, journées portes ouvertes CFP (sans aucun texte placeholder oublié). | `IMG-20260827-WA00031.jpg` (Réelle) |
| `PUB-16` | Fiche détail d'une actualité ou d'un événement | Détail complet d'un événement au parc avec réservation directe et programme horaire. | `IMG-20260809-WA0009.jpg` (Réelle) |
| `PUB-17` | Foire aux questions (FAQ) | Réponses claires sur les tarifs enfants (3-12 ans), moyens de paiement (MTN MoMo, Orange Money, espèces au guichet), repas et groupes. | — |
| `PUB-18` | Contact et localisation | Coordonnées officielles ECOPARK (`+237 697 13 62 03` / `675 56 26 55`, `contact@ecopark-yaounde.com`), formulaire direct. | — |
| `PUB-19` | Recherche globale et résultats | Recherche instantanée dans les activités, tarifs, hébergements et formations avec états plein et vide. | — |
| `PUB-20` | Pages légales : mentions légales, confidentialité, conditions de vente ou de réservation, cookies | Mentions légales ECOPARK CAMEROUN (Yaoundé-Ahala), politique RGPD/données personnelles, CGV billetterie. | — |
| `PUB-21` | Page 404 | Écran d'erreur 404 bienveillant dans la charte *Canopée vivante* avec retour rapide à l'accueil et aux tarifs. | — |
| `PUB-22` | Page maintenance ou service momentanément indisponible | Écran d'information en cas de maintenance programmée avec contact téléphonique d'urgence. | — |

### Famille 3 — Préparation de Visite, Devis & Réservation (`RES-01` à `RES-12`)
| ID | Intitulé officiel | Règles métier & Garde-fous |
| :--- | :--- | :--- |
| `RES-01` | Assistant « Préparer ma visite » | Choix du profil de visite (Famille, Couple, Groupe d'amis, Excursion scolaire, Séminaire entreprise, Séjour Loges). |
| `RES-02` | Sélection de la date, du créneau et de la composition du groupe | Sélecteur de date, compteurs Adultes (13+ ans), Enfants (3–12 ans), Tout-petits (<3 ans : Gratuit). |
| `RES-03` | Simulateur de budget et sélection des prestations | Calcul temps réel en `FCFA`. **Garde-fou actif** : le tarif enfant reste à `500 FCFA` (jamais remplacé par un tarif groupe à `700 FCFA` qui pénaliserait les familles/écoles). |
| `RES-04` | Panier ou récapitulatif détaillé des prestations | Détail ligne par ligne (Zoo, Piscine, Pirogue, Équitation, Repas, Loges) avec sous-totaux par tranche d'âge. |
| `RES-05` | Coordonnées du visiteur ou du responsable de groupe | Saisie nom, téléphone Cameroun (`+237 6XX XX XX XX`), email optionnel, souhaits particuliers. |
| `RES-06` | Demande de devis groupe, école, entreprise ou événement | Formulaire dédié dès 20 personnes ou besoin sur-mesure, générant une référence de dossier traçable (`DEV-2026-XXXX`). |
| `RES-07` | Choix du mode de règlement ou de réservation | Choix entre **Orange Money**, **MTN Mobile Money** ou **Pré-réservation avec paiement au guichet d'Ahala**. |
| `RES-08` | Écran de paiement Mobile Money en mode démonstration | **Sécurité stricte** : aucun champ de code PIN secret sur le site. Explication de la notification USSD sur le téléphone du client et sélecteur d'état (*En attente*, *Confirmé*, *Échoué*, *Annulé*, *Expiré*). |
| `RES-09` | Confirmation de réservation avec billet QR de démonstration | Mention explicite **`BILLET DÉMONSTRATION — PROTOTYPE`**, QR code + code lisible `ECP-2026-84920`, téléchargement PDF / partage WhatsApp. |
| `RES-10` | Confirmation de demande de devis avec numéro de suivi | Récapitulatif de la demande de devis groupe/école avec délai de réponse et contact commercial ECOPARK. |
| `RES-11` | Échec, expiration ou annulation de paiement avec reprise | Écran dédié permettant de relancer la notification Mobile Money ou de basculer en paiement au guichet sans perdre son panier. |
| `RES-12` | Recherche et consultation d'une réservation par référence | Recherche rapide par code `ECP-XXXX` ou numéro de téléphone pour retrouver son billet sans compte obligatoire. |

### Famille 4 — Espace Visiteur / Client (`ACC-01` à `ACC-06`)
| ID | Intitulé officiel | Fonctionnalités clés |
| :--- | :--- | :--- |
| `ACC-01` | Connexion, création deaccès ou vérification par code | Connexion simple par numéro de téléphone (`+237`) ou email avec code OTP de démonstration. |
| `ACC-02` | Tableau de bord visiteur | Vue synthétique de la prochaine visite à ECOPARK Ahala, météo du jour et billets actifs. |
| `ACC-03` | Mes réservations et billets | Liste des réservations passées et à venir avec accès en 1 clic au billet QR `ECP-2026-84920`. |
| `ACC-04` | Mes demandes de devis et échanges | Suivi des devis scolaires ou entreprises (*En étude*, *Proposition envoyée*, *Validé*). |
| `ACC-05` | Demande de modification, report ou annulation | Formulaire de report de date de visite selon les conditions d'ECOPARK. |
| `ACC-06` | Profil, coordonnées et préférences | Mise à jour des informations du visiteur et préférences de notification (SMS / WhatsApp / Email). |

### Famille 5 — Guichet & Contrôle des Entrées (`AGT-01` à `AGT-09`)
| ID | Intitulé officiel | Fonctionnalités clés |
| :--- | :--- | :--- |
| `AGT-01` | Connexion agent et choix du poste | Sélection du poste (*Guichet Entrée Principale Ahala*, *Caisse Piscine*, *Contrôle Tourniquet Zoo*, *Réception Loges*). |
| `AGT-02` | Tableau de bord guichet du jour | Affluence en temps réel, jauge piscine, arrivées groupes attendues et recettes de la session. |
| `AGT-03` | Vente rapide au guichet | Clavier tactile rapide : Entrée Zoo (`500`/`1 000 FCFA`), Piscine (`1 500`/`2 500 FCFA`), Pirogue (`500`/`1 000 FCFA`), Cheval (`500`/`1 000 FCFA`). |
| `AGT-04` | Encaissement et émission de billet | Encaissement Espèces FCFA ou Mobile Money guichet, calcul du rendu monnaie et impression thermique du ticket QR. |
| `AGT-05` | Scan et vérification de billet QR | Caméra de scan et saisie manuelle de secours du code `ECP-2026-XXXXX`. |
| `AGT-06` | Résultats de contrôle : valide, déjà utilisé, mauvaise date, expiré, annulé, prestation différente, code inconnu | Simulateur interactif des **7 verdicts de contrôle** avec code couleur à fort contraste et motif précis. |
| `AGT-07` | Recherche manuelle par nom, téléphone ou référence | Retrouver un visiteur ayant oublié son téléphone ou dont l'écran est endommagé. |
| `AGT-08` | Journal des ventes et entrées de la session | Historique horodaté de tous les tickets émis et scannés par l'agent durant sa vacation. |
| `AGT-09` | Clôture de caisse et écarts | Comptage contradictoire espèces FCFA / Mobile Money, déclaration d'écart éventuel et signature de fin de poste. |

### Famille 6 — Exploitation & Gestion Opérationnelle (`EXP-01` à `EXP-07`)
| ID | Intitulé officiel | Fonctionnalités clés |
| :--- | :--- | :--- |
| `EXP-01` | Vue d'exploitation quotidienne | Tableau de bord chef d'exploitation : météo Ahala, ouvertures des 6 pôles, effectifs présents et alertes. |
| `EXP-02` | Gestion des réservations et calendrier de capacité | Planning journalier et hebdomadaire des réservations individuelles et jauges par activité. |
| `EXP-03` | Gestion des demandes de devis groupes et événements | Instruction des dossiers écoles et entreprises, application de remises validées et génération de proforma FCFA. |
| `EXP-04` | Gestion des hébergements et disponibilités | Planning d'occupation des Loges **Ewondo** (`25k-30k`), **Chanthel** (`15k-25k`) et **Bene** (`10k-15k`), statuts ménage/check-in. |
| `EXP-05` | Gestion des réservations restauration et espaces | Réservations de tables et pergolas au *Château des Saveurs*, banquets et menus groupes. |
| `EXP-06` | Gestion des candidatures de formation | Suivi des dossiers d'inscription au **CFP ECOPARK** (Aquaculture, Hôtellerie, Agro-pastoral), pièces jointes et statut d'admission. |
| `EXP-07` | Centre de messages, réclamations et demandes de contact | Boîte de réception unifiée des demandes visiteurs (remplaçant les commentaires publics sans réponse). |

### Famille 7 — Pilotage & Direction (`DIR-01` à `DIR-05`)
| ID | Intitulé officiel | Fonctionnalités clés |
| :--- | :--- | :--- |
| `DIR-01` | Tableau de bord direction | Vue exécutive (Dr Christophe FOE NDI / Direction) : chiffre d'affaires consolidé FCFA, fréquentation et satisfaction. |
| `DIR-02` | Suivi des recettes, réservations et ventes par canal | Répartition des encaissements : Guichet Espèces vs En ligne Orange Money / MTN MoMo vs Virements B2B. |
| `DIR-03` | Fréquentation par activité, période et segment | Analyse comparative Zoo, Piscine, Lac, Restauration, Hôtellerie et CFP par semaine/mois. |
| `DIR-04` | Taux d'occupation hébergement et performance des offres groupes | RevPAR et taux de remplissage des cités Ewondo, Chanthel et Bene ; taux de conversion des devis scolaires/entreprises. |
| `DIR-05` | Rapports et exports | Génération d'états comptables et opérationnels en CSV / PDF sur période personnalisée. |

### Famille 8 — Administration de la Plateforme (`ADM-01` à `ADM-08`)
| ID | Intitulé officiel | Fonctionnalités clés |
| :--- | :--- | :--- |
| `ADM-01` | Catalogue des activités, offres et formules | Création/édition des activités, horaires, photos autorisées et rattachement aux pôles du parc. |
| `ADM-02` | Grille tarifaire, règles par âge, périodes et promotions | Paramétrage des prix unitaires en `FCFA`, tranches d'âge (<3 ans, 3-12 ans, 13+ ans) et verrouillage anti-erreur sur les remises enfants. |
| `ADM-03` | Quotas, capacités, horaires et fermetures exceptionnelles | Définition des jauges maximales (Piscine, Pirogues, Loges) et fermeture temporaire d'une attraction pour maintenance. |
| `ADM-04` | Contenus éditoriaux, médias, actualités et FAQ | CMS intégré pour publier les actualités, mettre à jour la carte du *Château des Saveurs* en FCFA et gérer les badges photos. |
| `ADM-05` | Utilisateurs internes, rôles et permissions | Matrice RBAC des **7 rôles** avec principe du moindre privilège. |
| `ADM-06` | Paramètres du site, coordonnées, horaires et textes légaux | Coordonnées officielles d'Ahala, liens réseaux sociaux et mentions légales. |
| `ADM-07` | Paramètres d'intégration : paiement, messagerie, analytique, sans secrets exposés | État des passerelles Orange Money / MTN MoMo / SMTP avec clés masquées (`••••••••••••`) et mode Sandbox/Production. |
| `ADM-08` | Journal d'audit et historique des actions sensibles | Traçabilité immuable des modifications de tarifs, annulations de billets et clôtures de caisse (Auteur, Rôle, Date/Heure, Action). |


---

## 9. Extensions Production Déployées (Prise de RDV, Écosystème WhatsApp 5 Piliers & Pack des 7 Compléments)

| Module / Référence | Écrans Enrichis | Fonctionnalités Actives en Production (`https://ecopark-cameroun-ahala.vercel.app`) |
| :--- | :--- | :--- |
| **Module Prise de RDV (`/rdv`)** | `PUB-18`, `ACC-04`, `EXP-07`, `ADM-08` | Section dédiée `#sec-PUB-18` (4 motifs : *Mariages/Galas*, *Séminaires B2B/Ministères/ONG*, *Repérage Écoles*, *Orientation CFP*), modale `#modalRdvBox` avec 4 créneaux garantis (`09h30`, `11h00`, `14h00`, `16h00`), génération de référence `RDV-2026-XXXX` et table SQL `public.appointments`. |
| **Guichet Unique & Closing WhatsApp** | `RES-04`, `RES-09`, `EXP-07` | Portefeuille WhatsApp client (`#whatsappConciergeCard`) avec 4 Quick Replies, bon de commande pré-calculé sans ressaisie, option gourmande 1 clic (*Poisson Braisé & Pergola 13h*), garantie tarif guichet 11h et Console de Closing Agent en 1 clic (`EXP-07`). |
| **Recherche & Filtres Dossiers Client** | `RES-12`, `ACC-01` à `ACC-06` | Recherche instantanée `#accSearchInput` par référence (`ECP-`, `DEV-`, `RDV-`, `CFP-`) ou téléphone `+237`, filtres par catégorie incluant les candidatures CFP, et rechargement 3D direct d'un billet QR (`loadBookingIntoQrPass`). |
| **Mode Hors-Ligne & Documents PDF** | `RES-09`, `RES-10`, `AGT-09`, `DIR-05` | Téléchargement du Billet QR en image PNG haute définition hors-ligne (`downloadOfflineQrTicketPng`) pour le portail d'Ahala sans forfait data, et impression/export PDF de la **Facture Proforma Officielle** et du **PV de Clôture de Caisse** (`printOfficialDocument`). |
| **Garantie Pluie Tropicale Yaoundé** | `ACC-05` | Modale `#modalRescheduleBox` permettant le report de date sans frais en 1 clic sur tout billet QR ou rendez-vous. |
| **Logistique Cuisine 13h & Navette** | `PUB-07`, `RES-03`, `EXP-05` | Sélecteurs contextuels `#kitchenPreorderSubpanel` (*Poisson Braisé, Poulet DG, Ndolé Royal* + créneau *12h30 / 13h30 / 15h00*) et `#shuttlePickupSubpanel` (*Poste Centrale, Carrefour Bastos, Carrefour Mvan, Nsimeyong* + flotte *18/32 pl. ou VIP 5 pl.*). |
| **Météo Ahala, Avis Vérifiés & Export CSV** | `PUB-01`, `PUB-13`, `PUB-15`, `DIR-05` | Bandeau météo & trafic RN3 en direct (`#ahalaLiveWeatherBar`), 4 témoignages vérifiés (`#sec-PUB-15`), barre de raccourcis mobiles (`#mobileQuickNavPills`) et export comptable complet au format CSV compatible Microsoft Excel (`exportEcoparkDatabaseCSV`). |
