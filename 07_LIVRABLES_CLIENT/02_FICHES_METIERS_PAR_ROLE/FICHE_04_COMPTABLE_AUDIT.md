# FICHE METIER 04 : COMPTABLE & AUDITEUR FINANCIER
**Projet** : ECOPARK CAMEROUN (Yaoundé-Ahala)
**Rôle RBAC** : `comptable` / `auditeur` (Lecture Financière, Rapprochement Mobile Money, Export OHADA & Journal d'Audit)
**Objectif** : Garantir l'exactitude à 100 % des recettes FCFA entre les relevés Mobile Money, la caisse espèces et la base Supabase.

---

## 1. Contrôle Quotidien des Recettes (J+1 à 09h00)
1. Ouvrir la Console Admin (`#admin-console`) et accéder aux vues **Réservations / Paiements** et **Journal d'Audit**.
2. Filtrer les transactions de la veille par canal de règlement :
   - **MTN Mobile Money (`MOMO`)**
   - **Orange Money (`OM`)**
   - **Espèces Guichet (`CASH`)**
   - **Virement / Chèque Entreprise (`B2B`)**

---

## 2. Rapprochement Bancaire & Mobile Money
1. Exporter le fichier CSV des transactions confirmées depuis la console ECOPARK.
2. Comparer le total et les références de transaction (`provider_tx_id`) avec les relevés marchands officiels MTN MoMo et Orange Money.
3. Vérifier qu'aucune réservation au statut `CONFIRMED` ne présente un montant encaissé inférieur au tarif catalogue hors remise B2B autorisée.

---

## 3. Audit de Sécurité & Détection d'Anomalies
1. Consulter l'onglet **Journal d'Audit (`audit_log`)** immuable :
   - Surveiller les actions sensibles : `DELETE`, `UPDATE` de statut de paiement, ou annulations après impression.
   - Vérifier l'identité de l'auteur (`actor_email`), son rôle et l'horodatage précis.
2. Contrôler le taux de billets émis non scannés ou annulés en caisse pour détecter toute tentative de fraude interne.

---

## 4. Clôture Mensuelle & Conformité OHADA
1. Générer l'état récapitulatif mensuel des ventes ventilé par catégorie :
   - Billetterie & Pass Loisirs
   - Location d'Espaces & Evénementiel (Pavillons, Mariages, Séminaires)
   - Restauration & Activités annexes
2. Archiver les pièces justificatives numériques (devis B2B validés, PV de caisse signés) conformément aux exigences de conservation comptable OHADA.
