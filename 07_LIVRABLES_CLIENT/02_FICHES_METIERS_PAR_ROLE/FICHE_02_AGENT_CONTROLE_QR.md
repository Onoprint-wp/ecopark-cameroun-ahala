# FICHE METIER 02 : AGENT DE CONTROLE D'ACCES & SCAN QR
**Projet** : ECOPARK CAMEROUN (Yaoundé-Ahala)
**Rôle RBAC** : `agent_controle` (Scan QR Tourniquet, Validation Entrées, Mode Offline First)
**Objectif** : Contrôler chaque visiteur en moins de 3 secondes et bloquer 100 % des billets falsifiés ou déjà utilisés.

---

## 1. Prise de Poste au Tourniquet (08h15)
1. Ouvrir l'application PWA ECOPARK sur le smartphone de contrôle et activer le **Mode Soleil (`sunMode`)**.
2. Vérifier que la liste locale des billets pré-vendus est synchronisée (bandeau vert **Base Locale Sync OK**).
3. Tester le lecteur caméra sur le QR Code de test affiché au poste de garde.

---

## 2. Procédure de Scan Visiteur
1. Présenter la caméra à 15 cm du QR Code du visiteur (écran smartphone ou billet imprimé).
2. Observer le retour visuel et sonore immédiat :
   - **ECRAN VERT + BIP COURT (`VALIDE`)** : Autoriser le passage et orienter vers la pose du bracelet correspondant au tarif affiché.
   - **ECRAN ORANGE (`DEJA SCANNE`)** : Bloquer le passage. L'écran affiche l'heure exacte du premier scan (`used_at`). Appeler le superviseur en cas de contestation.
   - **ECRAN ROUGE (`INVALIDE / FALSIFIE`)** : Signature cryptographique incorrecte ou billet annulé. Refuser l'accès et diriger le visiteur vers le Guichet Billetterie.

---

## 3. Gestion des Groupes & Ecoles
1. Pour un billet collectif (sortie scolaire ou entreprise), scanner le QR Code Maître du responsable de groupe.
2. Compter physiquement les participants et valider le compteur par paliers sur l'écran (`Validation groupée : N / Total`).
3. Vérifier la présence de l'accompagnateur adulte obligatoire.

---

## 4. Fonctionnement Sans Réseau (Coupure 4G)
- Le scanner fonctionne **100 % hors-ligne** grâce à la vérification cryptographique locale et au cache `IndexedDB`.
- Ne jamais laisser entrer un visiteur "à l'œil" sous prétexte d'une panne réseau : le scan local reste opérationnel en permanence.
- Dès le retour du signal 4G/Wi-Fi, les horodatages de passage remontent automatiquement au serveur central.
