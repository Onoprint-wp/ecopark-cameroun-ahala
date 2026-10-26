---
name: ecopark-booking-architecture
description: Architecture technique du système de billetterie en ligne, réservation hôtelière (Ewondo, Chanthel, Bene), commande de Packs, préinscription au Centre de Formation (CFP) et paiement Mobile Money (MTN MoMo / Orange Money) pour ECOPARK Yaoundé.
---

# Architecture Billetterie, Réservation & Paiement Mobile Money : ECOPARK Yaoundé

## 1. Objectif Métier
Remplacer les boutons passifs renvoyant vers 5 numéros WhatsApp différents par un **Moteur de Réservation & Billetterie Unifié** permettant d'encaisser instantanément via **MTN Mobile Money, Orange Money et Carte Bancaire**, tout en générant des billets QR Code et confirmations automatiques sur WhatsApp et Email.

## 2. Les 4 Tunnels de Conversion à Supporter

### Tunnel A : Billetterie Activités & Pass Journée (B2C)
- **Sélection** : Date de visite + Nombre d'Adultes / Enfants / Groupe (application automatique du tarif réduit dès 10 personnes : ex. 700 FCFA au lieu de 1 000 FCFA pour Zoo, Pirogue, Cheval, Forêt).
- **Options combinables** :
  - Entrée Parc Animalier / Zoo (500 / 1 000 FCFA)
  - Accès Piscine (1 500 / 2 500 FCFA selon jour semaine/week-end)
  - Balade en Pirogue, Cheval, Forêt, Musée, Bibliothèque, Pêche ludique.
  - Option **Navette Ecopark** (prise en charge A/R Yaoundé : 5, 18 ou 32 places).
- **Livrable client** : Billet électronique PDF + QR Code envoyé par WhatsApp et Email.

### Tunnel B : Réservation Hôtelière (3 Établissements sur site)
- **Sélection** : Check-in / Check-out, Nombre d'invités, Choix de l'établissement :
  1. **Hôtel EWONDO** : 4 Suites & 4 Mini-suites (`25 000 – 30 000 FCFA / nuit`)
  2. **Hôtel CHANTHEL** : 12 Chambres confortables (`15 000 – 25 000 FCFA / nuit`)
  3. **Hôtel BENE** : Chambres accessibles (`10 000 – 15 000 FCFA / nuit`)
- **Mode de règlement** : Acompte Mobile Money (ex. 30 % ou 100 %) pour bloquer la chambre + confirmation immédiate à la réception.

### Tunnel C : Réservation de Packs & Événementiel (B2C / B2B / Écoles)
- **7 Packs configurables** : *Pack Famille, Pack Anniversaire, Pack Couple, Pack École, Pack Enfant, Pack Entreprise, Pack Séjour* + location de la salle **Menkii Essomba Anton** et traiteur **Le Château des Saveurs**.
- **Fonctionnement** : Simulateur de devis instantané selon l'effectif + prise de rendez-vous / paiement d'acompte Mobile Money.

### Tunnel D : Préinscription Digitale au Centre de Formation Professionnelle (CFP)
- **Formulaire corrigé et validé (Zod / Validation stricte)** :
  - Identité complète, âge (≥ 16 ans), diplôme, choix parmi les **5 filières exactes** : *Hôtellerie, Restauration, Décoration, Agropastorale, Pisciculture*.
  - Paiement en ligne des frais d'inscription (**50 000 FCFA**) et suivi des 4 tranches de scolarité (**250 000 FCFA**).

## 3. Centralisation WhatsApp & Assistant IA
- **Guichet Unique** : Unifier les 5 numéros actuels derrière un point d'entrée principal assisté par un **Agent IA WhatsApp / Web** capable de :
  - Répondre en < 5 secondes sur les tarifs, l'itinéraire (Station Tradex Ahala), les horaires et les disponibilités.
  - Qualifier et router automatiquement la demande vers le bon responsable interne (*Réception Hôtels*, *Direction CFP*, *Château des Saveurs*, *Service Navettes*).
