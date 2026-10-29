---
trigger: always_on
---

# ECOPARK Cameroun — Règles de Qualité, Vérification & Interdictions Strictes

## 1. Interdictions absolues (Anti-patterns)
1. Ne pas corriger le site uniquement par un changement de palette CSS.
2. Ne pas employer du vert pour presque tous les éléments.
3. Ne pas ajouter une couleur différente à chaque bloc sans logique sémantique.
4. Ne pas construire toutes les pages à partir de la même succession monotone de cartes.
5. Ne pas répéter les mêmes paragraphes ou introductions sur plusieurs pages.
6. Ne pas cacher les informations essentielles (tarifs, horaires, conditions d'accès/admission) dans des accordéons fermés.
7. Ne jamais inventer des tarifs, agréments, témoignages, capacités ou conditions.
8. Ne jamais afficher une météo, un trafic routier, un stock de chambres ou une disponibilité « en direct » sans source temps réel vérifiée.
9. Ne jamais afficher des garanties commerciales (ex. remboursement automatique, garantie pluie gratuite) sans conditions validées par la direction.
10. Ne laisser aucun bouton sans effet ni lien mort.
11. Ne jamais afficher un billet confirmé avant l'enregistrement effectif de la réservation.
12. Ne jamais déformer les proportions du logo officiel ni remplacer les photographies réelles du parc sans raison.
13. Ne jamais masquer un problème de mise en page avec un `zoom` global ou un `transform: scale()` sur la page.
14. Tolérance zéro pour le défilement horizontal global (`overflow-x`) sur mobile et tablette.
15. Ne pas dupliquer les fichiers de règles, les plans ou les composants.
16. Ne pas réécrire inutilement la pile technique ni ajouter de dépendances lourdes.
17. Préserver impérativement le travail existant et les intégrations opérationnelles (`EcoparkData`, console `/admin`, caisse `/guichet`, vue `/direction`, migrations Supabase).
18. Ne jamais déclarer le travail terminé sur la seule base d'une compilation ou d'un test statique réussi.

## 2. Critères de validation multi-écrans et fonctionnels
Contrôler systématiquement l'application aux largeurs :
- **`360px`**, **`390px`**, **`768px`**, **`1280px`**, **`1440px`**.

Vérifications obligatoires avant clôture :
- Absence de chevauchement et absence de défilement horizontal (`scrollWidth <= clientWidth`).
- Navigation principale, sous-vues et modales intégralement utilisables au clavier.
- Distinction claire des rubriques même sans leurs couleurs (titres, icônes SVG, photos, structure).
- Cohérence stricte des tarifs et des unités entre l'accueil, le catalogue, les fiches, la page tarifs et les calculateurs.
- Exactitude des totaux calculés pour plusieurs compositions (famille 2 adultes + 2 enfants, groupe >= 10 pers., séjour multi-nuits).
- Application des jours de fermeture (lundi fermé pour les activités journée) et des catégories d'âge (`< 3 ans`, `3–12 ans`, `13+ ans`).
- Distinction honnête des états de réservation et de paiement + conservation des saisies au retour arrière.
- Fonctionnement des anciennes URL (`/activites`, `/fiche-activite`, `/hebergements`, `/hotellerie`, `/restaurant`, `/pack-ecole`, `/pack-entreprise`, `/formation`, `/nos-tarifs`, `/tarifs`, `/agenda`, `/contact`, `/mon-espace`, `/reserver`, `/guichet`, `/direction`, `/admin`) et des nouvelles routes.
- Absence totale de jargon technique ou mentions de développement (`V4`, `Page 1/6`, `Architecture Multi-Pages`, `Parcours Transactionnel`) dans les pages publiques.

## 3. Recette utilisateur autonome (5 parcours clés)
Un visiteur doit pouvoir trouver et accomplir sans aide :
1. Le prix d'une journée pour **deux adultes et deux enfants**.
2. Les conditions (horaires arrivée/départ, capacité, équipements) et le prix d'une **chambre**.
3. Le formulaire de devis d'une **sortie scolaire**.
4. Les conditions d'admission et frais d'une **formation CFP**.
5. Le **statut explicite** et les actions associées d'une réservation existante dans `Mes réservations`.
