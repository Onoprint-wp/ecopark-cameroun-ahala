---
trigger: always_on
---

# ECOPARK Cameroun — Architecture de l'Information & Source Unique des Données

## 1. Navigation principale et accès utilitaires
Navigation principale limitée à **5 entrées explicites** :
1. **Découvrir le parc** (Présentation du domaine, Catalogue des activités, Fiches détaillées des activités, Galerie pertinente)
2. **Séjour & restaurant** (Sous-rubrique Hébergements & fiches chambres/catégories, Sous-rubrique Restaurant Le Château des Saveurs, carte & modalités)
3. **Groupes & événements** (Sorties scolaires, Entreprises et associations, Mariages et réceptions, Espaces/capacités/prestations vérifiés, Demande de devis adaptée)
4. **Formations** (Présentation du CFP agréé MINEFOP, Filières, Conditions d'admission, Durée/frais/calendrier vérifiés, Demande d'information et candidature)
5. **Préparer ma visite** (Tarifs et pass, Horaires et jours d'ouverture, Accès et transport RN3 Ahala, Services pratiques, Agenda, Questions fréquentes)

Accès utilitaires permanents :
- **Mes réservations** (suivi des billets, réservations et demandes du visiteur)
- Bouton principal **« Réserver »** (traitement identique sur toutes les pages)
- **Logo officiel** renvoyant toujours vers l'accueil (`/`)

Navigation mobile :
- Conserver une navigation lisible et un accès direct à la réservation sans masquer les contenus ni superposer plusieurs barres flottantes concurrentes.

## 2. Ordre et structure de la page d'Accueil (`/`)
L'accueil oriente et donne envie, sans reproduire le catalogue complet ni empiler plusieurs introductions :
1. **Une seule introduction principale** : photographie réelle du parc, titre `« Prenez le frais. Vivez la nature. »`, présentation courte, CTA principal `« Découvrir les activités »`, CTA secondaire `« Préparer ma visite »`.
2. **Les expériences principales** : sélection photographique, intitulés compréhensibles, accès direct aux fiches détaillées.
3. **Choisir son projet** : 5 entrées d'orientation (`Passer une journée`, `Séjourner`, `Organiser une sortie de groupe`, `Organiser un événement`, `Se former`).
4. **Les formules journée** : aperçu synthétique, prix et inclusions vérifiés avec unités, accès à la comparaison détaillée.
5. **Hébergement et restauration** : deux entrées distinctes et clairement différenciées.
6. **Agenda** : afficher uniquement les événements réellement renseignés ; masquer proprement la section si aucun événement n'est publié.
7. **Témoignages** : afficher uniquement des témoignages authentifiés et autorisés ; masquer proprement la section si aucune source exploitable n'existe.
8. **Informations pratiques** : adresse (Ahala Barrière, face station Tradex RN3), horaires, accès, contact.

## 3. Gabarits métiers obligatoires
- **Fiche activité** : nom et galerie ; présentation courte ; durée, âge, tarif (avec unité), accès ; déroulement ; inclus et non inclus ; conditions et équipements ; réservation ; activités complémentaires pertinentes.
- **Fiche hébergement** : galerie ; capacité ; équipements ; prix avec unité explicite (`par chambre et par nuit`) ; conditions d'arrivée et de départ ; disponibilités réelles ou demande de disponibilité ; réservation.
- **Restaurant** : lieu et cuisine ; carte et prix ; horaires ; modalités de service ; accueil groupes ; réservation ou contact.
- **Groupes et événements** : type de projet ; espaces et capacités ; prestations ; conditions ; formulaire de devis adapté.
- **Formation** : filière ; objectifs et débouchés documentés ; programme ; durée ; admission ; frais ; prochaine session ; candidature.
- **Hiérarchie éditoriale** : un seul `H1` explicite par page, sous-titres logiques (`H2`, `H3`), prix et conditions déterminantes immédiatement visibles hors accordéons (réserver les accordéons aux détails secondaires).

## 4. Source unique des informations (Single Source of Truth)
- Centraliser dans le modèle de données partagé (`content-snapshot.json`, `EcoparkData`, catalogue unifié) : activités, tarifs, catégories d'âge, inclusions des pass, hébergements, horaires et fermetures, conditions de réservation, contacts.
- Toutes les cartes, fiches, tableaux comparatifs et calculateurs consomment les mêmes données.
- **Unité obligatoire sur chaque prix** : `par personne`, `enfant (3–12 ans)` ou `adulte (13+ ans)`, `par chambre et par nuit`, `par groupe`, `forfait duo`, etc.
- En cas de conflit documentaire sur un tarif, ne pas trancher arbitrairement en silence : documenter l'écart dans `docs/ecopark-validation.md`.
- Supprimer des vues publiques toute mention technique ou de développement (`« V4 »`, `« Architecture Multi-Pages »`, `« Page 1/6 »`, `« Parcours Transactionnel »`, etc.).
- Conserver la compatibilité des anciennes URL et routes directes via correspondance et redirections propres.
