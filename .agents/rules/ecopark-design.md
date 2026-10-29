---
trigger: always_on
---

# ECOPARK Cameroun — Règles Graphiques & Accessibilité (Canopée Vivante)

## 1. Palette sémantique et rôles des couleurs
Tokens de départ obligatoires (vérifier et maintenir les contrastes WCAG AA >= 4,5:1 texte courant, >= 3:1 grand texte) :
- **Marque ECOPARK** : vert forêt `#254B28` (identité, en-tête, repères institutionnels, CTA global « Réserver »).
- **Nature et découverte** : vert feuillage `#527A35` (variante texte haute lisibilité sur fond clair : `#3D5E26`).
- **Eau et loisirs** : bleu pétrole `#176B80`.
- **Hébergement** : terre cuite `#A45138`.
- **Restauration** : ocre `#946015`.
- **Formation (CFP)** : indigo `#4D5685`.
- **Texte principal** : anthracite `#242824`.
- **Fond clair** : ivoire `#F7F5EF`.
- **Surfaces** : blanc `#FFFFFF`.

### Discipline d'emploi des couleurs
- Le vert de marque `#254B28` doit rester reconnaissable mais ne doit **jamais** colorer indistinctement tous les titres, prix, boutons, textes et fonds.
- Employer majoritairement des surfaces neutres (`#F7F5EF`, `#FFFFFF`, bordures neutres). Réserver les couleurs d'accent aux catégories, badges d'univers, repères visuels et éléments d'orientation utiles.
- Les pages transversales (**Tarifs / Préparer ma visite**, **Informations pratiques**, **Mes réservations**) utilisent une base neutre avec des références ponctuelles aux couleurs des univers concernés.
- Séparer strictement les couleurs de catégorie des **couleurs de statut** (succès, erreur, avertissement, information). Toujours accompagner un statut d'un **libellé texte explicite** (aucune information essentielle transmise uniquement par la couleur).

## 2. Identité commune « Canopée vivante »
- Conserver le logo officiel (`cropped-LOGO-ECOPARK-Youtube.png`) et ses proportions d'origine (ne jamais l'écraser ou le déformer).
- Maintenir une typographie cohérente (`Fraunces` / `Plus Jakarta Sans` / `JetBrains Mono`), une grille commune, des composants partagés, un langage photographique réel et homogène (domaine d'Ahala) et des règles communes d'espacement.
- Ne jamais transformer les univers en sites visuellement indépendants ni attribuer une couleur arbitraire à chaque bloc sans logique métier.

## 3. Différenciation multi-critères des rubriques
Chaque rubrique (Découvrir le parc, Séjour & restaurant, Groupes & événements, Formations, Préparer ma visite) doit être identifiable même sans la couleur par :
1. Son **titre explicite** ;
2. Son **pictogramme SVG** issu d'une même famille cohérente (interdiction d'utiliser des emojis comme système d'icônes d'interface) ;
3. Ses **photographies réelles** dédiées ;
4. Sa **structure de contenu** propre (gabarit adapté à l'objet métier, pas une simple répétition de grilles de cartes identiques) ;
5. Son **état actif explicite** dans la navigation (`aria-current="page"` + indicateur visuel).

## 4. Hiérarchie des actions
- **Action principale** : bouton plein (un seul bouton principal par bloc de décision ; éviter les boutons concurrents de poids égal).
- **Action secondaire** : bouton à contour (`outline`).
- **Action complémentaire** : lien texte avec flèche ou soulignement.
- Conserver exactement le même traitement visuel et fonctionnel pour le bouton global **« Réserver »** sur toutes les pages.

## 5. Accessibilité et lisibilité
- Contraste minimal **4,5:1** pour le texte courant et **3:1** pour le grand texte ; contrôles de formulaire et états `:focus-visible` nettement visibles.
- Corps de texte courant d'au moins **16 px** (`1rem`).
- Cibles tactiles principales d'au moins **44 × 44 px**.
- Navigation clavier complète (`Tab`, `Shift+Tab`, `Enter`, `Escape` pour les modales et tiroirs).
- Aucun contenu essentiel accessible uniquement au survol (`:hover`) ou dissimulé dans un accordéon.
- Respecter `prefers-reduced-motion: reduce`.
- Aucun texte essentiel intégré en dur dans une image sans équivalent textuel lisible et sélectionnable.
