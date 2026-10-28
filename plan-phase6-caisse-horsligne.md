# Plan Phase 6 : Caisse Guichet, Billetage Physique & Contrôle Hors-Ligne

## But
Câbler la grille de billetage physique et de clôture de caisse contradictoire (coupures FCFA) dans `AGT-08/09`, doter le scanner `AGT-05` d'un cache de validation hors-ligne en cas de coupure réseau sur la RN3, et dynamiser les indicateurs de caisse et de direction.

## Tâches

- [ ] **Tâche 1 : Grille de billetage physique interactive (`AGT-08/09`)**
  - Insérer dans `AGT-08` le tableau de comptage physique par coupures FCFA (Billets : 10 000, 5 000, 2 000, 1 000, 500 ; Pièces : 500, 100, 50, 25).
  - Calculer en temps réel le total physique, la comparaison au total théorique de la session et le calcul de l'écart.
  - → *Vérifier :* Saisir 10x 10 000 FCFA affiche 100 000 FCFA en total physique et recalcule l'écart en direct.

- [ ] **Tâche 2 : Gestion des alertes d'écart de caisse (seuil 2 000 FCFA)**
  - Implémenter les trois états d'écart : Conforme (0 FCFA, vert), Tolérance mineure (<= 2 000 FCFA, orange), Alerte critique (> 2 000 FCFA, rouge avec mention "Rapport d'incident Direction requis").
  - Tracer l'événement de clôture dans le journal d'audit via `EcoparkData`.
  - → *Vérifier :* Un écart de 5 000 FCFA affiche le badge rouge d'alerte critique.

- [ ] **Tâche 3 : PV de clôture enrichi et imprimable (`@media print`)**
  - Mettre à jour `printOfficialDocument('CLOSURE')` pour ventiler le décompte des coupures physiques, les montants théoriques, l'écart et les emplacements de visa (Caissière & Direction).
  - → *Vérifier :* Clic sur "PV Clôture PDF" ouvre la modale avec le tableau détaillé du billetage.

- [ ] **Tâche 4 : Cache de validation hors-ligne pour le scanner d'entrée (`AGT-05`)**
  - Mettre en place un magasin local synchrone des billets valides pour permettre la validation même sans connexion Internet (`navigator.onLine === false`).
  - Stocker les scans hors-ligne dans une file d'attente locale (`offlineScansQueue`).
  - → *Vérifier :* Couper le réseau (mode offline Playwright) permet de valider un billet sans erreur réseau.

- [ ] **Tâche 5 : Synchronisation automatique de reconnexion**
  - Écouter l'événement `online` et vider automatiquement la file d'attente des scans vers le magasin `EcoparkData`.
  - Afficher un badge de statut : "Réseau OK" ou "Hors-Ligne RN3 (X scan(s) en attente)".
  - → *Vérifier :* Reconnecter le réseau synchronise les scans et met à jour le compteur en ligne.

- [ ] **Tâche 6 : Dynamisation des compteurs Guichet & Direction**
  - Connecter les cartes de session `AGT-08` et `DIR-01` aux ventes et billets réels de `EcoparkData` (remplacement des données figées de `posStats`).
  - → *Vérifier :* Une vente rapide walk-in incrémente immédiatement le montant des espèces et le nombre d'entrées.

- [ ] **Tâche 7 : Script de test d'intégration automatisé (`scripts/test_phase6_caisse_horsligne.py`)**
  - Créer le banc de test couvrant la saisie de billetage, l'écart de caisse, le PV de clôture, le scan hors-ligne et la synchronisation.
  - Ajouter la commande `"test:phase6"` dans `package.json`.
  - → *Vérifier :* `npm run test:phase6` valide 100 % des assertions sans erreur.

- [ ] **Tâche 8 : Synchronisation stricte des fichiers et vérification finale**
  - Répercuter à l'identique dans `Prototype_Interactif_ECOPARK_NEW_LOOK.html` et vérifier l'invariant `git diff --no-index` = 0.
  - Vérifier 0 caractère > `0x25FF`.
  - Exécuter la suite complète de non-régression (`npm run test:all` / tests locaux).
  - → *Vérifier :* 0 erreur console, 100 % des tests existants passent.

## Critères de Réussite (Done When)
- [ ] La caissière peut saisir le décompte physique de ses coupures FCFA et visualiser l'écart immédiatement.
- [ ] Le seuil d'alerte de 2 000 FCFA déclenche le protocole d'incident.
- [ ] Le scanner du portail valide les billets même sans connexion Internet sur la RN3.
- [ ] Les scans hors-ligne sont réconciliés dès le retour du réseau.
- [ ] Le PV de clôture officiel s'imprime proprement en A4 avec les signatures.
- [ ] `npm run test:phase6` et toute la suite de tests existante passent à 100 %.
- [ ] `index.html` et `Prototype_Interactif_ECOPARK_NEW_LOOK.html` sont rigoureusement identiques.

## Notes
- Respect absolu de la palette 60-30-10 et de la couleur d'accent Ocre Bronze (`#C47D2B`).
- Monnaie : FCFA (séparateur de milliers sans décimales).
- Aucun stockage de clés privées dans le navigateur.
