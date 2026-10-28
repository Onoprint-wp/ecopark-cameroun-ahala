# Plan — Phase 5 : Raccordement du Site Public & Viabilité Terrain ECOPARK

## Goal
Raccorder les pages publiques (`/nos-tarifs`, `/reserver`, `/agenda`, `/restaurant`) aux données gérées en temps réel par `EcoparkData`, tout en intégrant les 5 correctifs critiques indispensables pour le fonctionnement réel à Ahala (vrai QR code scannable, impression propre `@media print`, verrouillage du lundi, validation des numéros camerounais et mentions légales/CGV).

---

## Tasks

- [ ] **Task 1 : Micro-générateur de vrai QR Code matriciel autonome**
  Intégrer une bibliothèque de génération QR matricielle autonome et ultra-légère (`< 15 Ko`, zéro dépendance) dans `etape0-site-live/vendor/qrcode.min.js`. Remplacer les rectangles statiques factices de `loadBookingIntoQrPass()` ([index.html#L4254](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/etape0-site-live/index.html#L4254)) et `downloadOfflineQrTicketPng()` ([index.html#L9723](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/etape0-site-live/index.html#L9723)) par le rendu réel du jeton de réservation, en supprimant la mention erronée `500 FCFA` en dur.
  → *Verify :* Générer un billet, scanner le QR affiché à l'écran et le PNG téléchargé avec l'appareil photo d'un smartphone et constater la lecture exacte de la référence `ECP-2026-XXXX`.

- [ ] **Task 2 : Feuille de style dédiée pour impression `@media print` (Billet & Ticket 80mm)**
  Ajouter les règles CSS `@media print` dans `index.html` pour masquer tous les éléments d'interface hors-contexte (navigation, footer, boutons admin, hero) et mettre en page proprement le billet client (A4 épuré) ou le ticket de caisse guichet (rouleau thermique 80mm).
  → *Verify :* Cliquer sur *Imprimer / Enregistrer en PDF* dans `#modalOfficialPrintBox` et vérifier dans l'aperçu d'impression que le document tient sur 1 page nette sans éléments parasites.

- [ ] **Task 3 : Verrouillage de la fermeture hebdomadaire le Lundi et dates passées**
  Mettre à jour les sélecteurs de date (`#bookDate`, `#quoteDate`, `#rdvDate`) pour interdire le choix du lundi (`day === 1`, jour de fermeture et repos animalier) ainsi que les dates antérieures à aujourd'hui, avec message d'information immédiat.
  → *Verify :* Tenter de sélectionner un lundi dans le simulateur de réservation et vérifier que la sélection est bloquée avec l'indication « Parc fermé le lundi ».

- [ ] **Task 4 : Validation stricte des numéros camerounais & case CGV obligatoire**
  Ajouter la validation regex des numéros de téléphone locaux (`+237 6XXXXXXXX` ou `6XXXXXXXX` - 9 chiffres) sur le formulaire de réservation et ajouter la case à cocher obligatoire d'acceptation des CGV et de la politique de report sous 90 jours avant déclenchement du paiement.
  → *Verify :* Saisir un numéro invalide (ex. `01234567`) puis un numéro valide (`697136203`) et vérifier que le bouton de commande reste bloqué tant que les CGV ne sont pas cochées.

- [ ] **Task 5 : Raccordement dynamique de la grille `/nos-tarifs` (PUB-10)**
  Remplacer le tableau HTML des tarifs statiques par un rendu dynamique alimenté par `EcoparkData.list('catalog_activities')` et `sales_bundles`, incluant la vignette photo administrée et le recalcul instantané en cas de mise à jour.
  → *Verify :* Modifier un prix dans `ADM-01`, naviguer sur `/nos-tarifs` et vérifier que la grille affiche immédiatement la nouvelle valeur sans recharger la page.

- [ ] **Task 6 : Raccordement dynamique du simulateur `/reserver` (RES-01..12)**
  Connecter les options du simulateur (activités à la carte, pass tout-inclus, cités hôtelières, navettes) aux données actives de `EcoparkData.content()`, éliminant les 151 constantes de prix codées en dur.
  → *Verify :* Ajouter ou désactiver une activité dans l'admin et vérifier son apparition ou retrait immédiat dans le simulateur de réservation.

- [ ] **Task 7 : Raccordement dynamique de `/agenda` (PUB-15/16) et du `/restaurant` (PUB-07)**
  Brancher l'agenda des événements hebdomadaires sur `agenda_events` et la carte du restaurant *Le Château des Saveurs* sur `menu_items`, avec masquage automatique des plats marqués « En rupture ».
  → *Verify :* Passer un plat en rupture dans `ADM-04` et vérifier qu'il est immédiatement grisé/indisponible sur la vue `/restaurant`.

- [ ] **Task 8 : Activation du flux caméra pour le scanner d'entrée (`AGT-05`)**
  Intégrer la lecture par caméra via l'API Web standard `navigator.mediaDevices.getUserMedia` dans la vue du contrôleur d'entrée `AGT-05`, avec sélecteur de caméra (avant/arrière), boîte de visée et déclenchement automatique du verdict de validation.
  → *Verify :* Ouvrir `AGT-05`, autoriser la caméra, viser l'écran d'un autre appareil affichant un billet et constater la validation automatique immédiate.

- [ ] **Task 9 : Phase X — Suite de tests automatisés & non-régression**
  Créer le script de vérification automatisée `scripts/test_phase5_integration.py` couvrant : décodage QR, aperçu print, blocage du lundi, validation téléphone, et synchronisation admin → public. Exécuter l'ensemble de la suite (`npm test`).
  → *Verify :* Exécuter `python scripts/test_phase5_integration.py` et `npm test` ; obtenir 100 % de succès avec 0 régression.

---

## Done When
- [ ] Les pages `/nos-tarifs`, `/reserver`, `/agenda` et `/restaurant` reflètent en direct les modifications apportées dans la console d'administration.
- [ ] Le QR code généré sur l'écran et sur le PNG téléchargeable est une vraie matrice 2D lisible par n'importe quel scanner ou smartphone.
- [ ] L'impression du billet et du reçu génère un document net sur 1 page via `@media print`.
- [ ] La réservation d'un lundi est techniquement impossible.
- [ ] Les numéros camerounais et l'accord sur les CGV sont strictement validés avant commande.
- [ ] Tous les tests de régression (`npm test`) passent avec succès.

---

## Notes
- Conserver le double pilote (`LocalDemoDriver` / `SupabaseDriver`) pour permettre le mode démo sans connexion.
- Respecter scrupuleusement la règle du design system Canopée Vivante (zéro caractère Unicode > `0x25FF`, palette 60-30-10 + Ocre Bronze).
- Maintenir les deux fichiers HTML en parfaite synchronisation (`etape0-site-live/index.html` et `Prototype_Interactif_ECOPARK_NEW_LOOK.html`).
