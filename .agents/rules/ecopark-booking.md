---
trigger: always_on
---

# ECOPARK Cameroun — Règles des Parcours de Réservation & Intégrité Transactionnelle

## 1. Parcours distincts par nature de besoin
Ne jamais mélanger estimation, demande de devis, candidature, paiement et confirmation dans un formulaire unique confus. Implémenter 4 parcours adaptés :
1. **Journée au parc** :
   `1. Date et participants` → `2. Pass ou activités` → `3. Coordonnées` → `4. Récapitulatif et règlement` → `5. Résultat`.
2. **Hébergement** :
   `1. Dates et voyageurs` → `2. Chambre` → `3. Coordonnées` → `4. Récapitulatif et règlement` → `5. Résultat`.
3. **Groupe ou événement** :
   `1. Projet` → `2. Date et effectif` → `3. Prestations` → `4. Coordonnées` → `5. Accusé de réception de la demande de devis`.
4. **Formation (CFP)** :
   Parcours de candidature distinct (`1. Filière et session` → `2. Profil et admission` → `3. Coordonnées et envoi` → `4. Accusé de réception de candidature`).

## 2. Cohérence des étapes et persistance des saisies
- L'indicateur d'étapes (stepper) doit correspondre **exactement** à l'ordre réel des champs et des écrans.
- Le retour à l'étape précédente conserve intégralement les saisies déjà effectuées.
- Un récapitulatif actualisé, lisible et détaillant les unités et quantités accompagne la progression.

## 3. Honnêteté des statuts et règles de validation
- **Ne jamais présenter un aperçu (preview) comme un billet valide ou confirmé** avant la validation et l'enregistrement effectifs.
- **Ne jamais annoncer un paiement réussi** à partir d'un simple clic sans vérification/retour d'état réel.
- **Ne jamais annoncer une réservation confirmée** sans enregistrement effectif dans la couche de données (`EcoparkData`).
- Distinguer explicitement les statuts :
  - `Devis envoyé / Demande de devis enregistrée` (en attente d'étude commerciale)
  - `Demande reçue` (candidature formation ou demande de disponibilité)
  - `Réservation en attente de règlement` (paiement au guichet ou virement)
  - `Paiement en attente de confirmation` (Mobile Money initié mais non encore validé)
  - `Confirmée` (réservation validée avec référence officielle)
- Lorsque le **paiement au guichet** est choisi, afficher explicitement le **montant restant à régler au guichet** en FCFA.
- Une intégration absente ou hors-ligne doit déclencher une action honnête (ex. enregistrement d'une demande de réservation avec référence à présenter ou confirmer) et jamais une fausse simulation de débit bancaire/Mobile Money.

## 4. Règles calendaires et fuseau horaire métier
- Utiliser exclusivement le fuseau **`Africa/Douala`** (UTC+1) pour toutes les dates métier.
- **Ne laisser aucune date de démonstration préremplie** (ex. `2026-11-15`) dans les champs publics.
- Adapter le calendrier au service sélectionné :
  - **Journée au parc / Activités** : parc fermé le **lundi** (sauf jour férié exceptionnel documenté) ; ouvert mardi–vendredi `09h00–18h00`, samedi–dimanche `09h00–19h00`. Bloquer ou signaler explicitement les lundis et dates passées.
  - **Hébergement** : réception ouverte `7j/7` (`24h/24` sur réservation) ; arrivée dès `14h00`, départ avant `11h00` ; autoriser les arrivées/départs tous les jours de la semaine avec `date de départ > date d'arrivée`.

## 5. Sécurité et confidentialité
- **Ne jamais demander ni enregistrer un code PIN Mobile Money** (Orange Money / MTN MoMo) dans l'interface.
- Protéger les données personnelles : le payload du code QR d'un billet ou d'une réservation ne doit contenir que la référence unique et un jeton de vérification (ne pas exposer en clair le numéro de téléphone ou l'adresse e-mail dans l'image QR).
- Ne jamais déclencher de paiement réel ni envoyer de requêtes externes réelles lors des tests automatisés.
