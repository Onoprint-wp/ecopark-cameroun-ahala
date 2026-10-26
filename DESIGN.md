# DESIGN SYSTEM ECOPARK — DOCUMENTATION OFFICIELLE (DS-01 à DS-08)
## Direction artistique validée : « Canopée vivante — Le cercle du vivant »

- **Marque :** **ECOPARK** (Yaoundé–Ahala, Cameroun)
- **Projet Google Stitch synchronisé :** [`projects/522000543872634848`](https://stitch.withgoogle.com/projects/522000543872634848?pli=1) (`assets/b1b40a03aba8496187426e4b86791929`)
- **Prototype Interactif Complet (77 Écrans) :** [`Prototype_Interactif_ECOPARK_NEW_LOOK.html`](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/Prototype_Interactif_ECOPARK_NEW_LOOK.html)
- **Matrice Contractuelle :** [`MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md`](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md)

---

## DS-01 — Vue Générale de la Marque, Concept & Règles du Logo

### 1.1 Concept Graphique : « Le cercle du vivant »
- **Principe fondateur :** Construire l'ensemble du système visuel à partir de la **rosette végétale du logo original** :
  - **Le cercle** rassemble les publics (familles, amis, écoles, entreprises, administrations, étudiants) ;
  - **Les feuilles** expriment la diversité des expériences (nature & faune, eau & loisirs, restauration, hébergement, événements, formation professionnelle) ;
  - **Le blanc (`#FFFFFF`)** organise la lecture et garantit la clarté des offres et des prix en FCFA.
- **Règle de dénomination :** *« Le cercle du vivant »* désigne exclusivement la direction artistique. **ECOPARK** reste le seul nom de marque officiel.

### 1.2 Règles d'Emploi du Logo Original (`EcoPark CAMEROUN`)
- **Fichier de référence :** [`audit-assets/ecopark-real-media/cropped-LOGO-ECOPARK-Youtube.png`](file:///c:/Users/PcGamerCm/Downloads/ECO-PARK/audit-assets/ecopark-real-media/cropped-LOGO-ECOPARK-Youtube.png)
- **Intégrité absolue :**
  - Conserver sa forme circulaire, son disque blanc (`#FFFFFF`), sa couronne de feuilles vertes, son lettrage `EcoParK` et la mention rouge `CAMEROUN`.
  - **Interdictions :** Ne jamais redessiner le logo avec une police approchante, ne pas étirer ses proportions, ne pas supprimer la mention rouge `CAMEROUN`, ne pas créer de variante simplifiée non approuvée.
  - **Zone de protection :** Maintenir un espace libre minimal équivalent à `16 %` du diamètre du disque autour du logo.
  - **Dimensions minimales :** `44px × 44px` sur mobile ; `56px × 56px` sur ordinateur.

---

## DS-02 — Architecture des Tokens à 3 Niveaux & États Sémantiques

### Niveau 1 : Tokens Primitifs (Valeurs Brutes)
```css
:root {
  /* Palette issue du logo raster fourni */
  --prim-white: #FFFFFF;
  --prim-green-deep: #1D490D;
  --prim-green-deep-hover: #153609;
  --prim-green-leaf: #1F880B;
  --prim-mist-soft: #EDF4E7;
  --prim-mist-border: #D5E5CD;
  --prim-ink-vegetal: #1E281B;
  --prim-ink-muted: #4A5946;

  /* États fonctionnels (indépendants du rouge du logo) */
  --prim-success-fg: #155724;
  --prim-success-bg: #E8F5E9;
  --prim-warning-fg: #7A4F01;
  --prim-warning-bg: #FFF8E1;
  --prim-error-fg: #B3261E;
  --prim-error-bg: #FCEEEE;
  --prim-info-fg: #0B57D0;
  --prim-info-bg: #E8F0FE;
  --prim-disabled-fg: #788275;
  --prim-disabled-bg: #E6ECE3;
}
```

### Niveau 2 : Tokens Sémantiques (Rôles Fonctionnels)
| Token Sémantique | Valeur Liée | Rôle dans l'Interface |
| :--- | :--- | :--- |
| `--color-surface-primary` | `var(--prim-white)` (`#FFFFFF`) | Surface dominante de lecture, cartes, en-tête public, tableaux. |
| `--color-surface-secondary` | `var(--prim-mist-soft)` (`#EDF4E7`) | Brume végétale pour alterner les sections et regrouper les formulaires. |
| `--color-action-primary` | `var(--prim-green-deep)` (`#1D490D`) | Action principale, titres majeurs, navigation active. |
| `--color-accent-leaf` | `var(--prim-green-leaf)` (`#1F880B`) | Repères visuels, puces de statut, compteurs actifs. |
| `--color-text-primary` | `var(--prim-ink-vegetal)` (`#1E281B`) | Texte principal (contraste $> 13:1$ sur `#FFFFFF`). |
| `--color-text-secondary` | `var(--prim-ink-muted)` (`#4A5946`) | Métadonnées, légendes, aides de saisie (contraste $> 6.5:1$ WCAG AA). |
| `--color-border-subtle` | `var(--prim-mist-border)` (`#D5E5CD`) | Séparateurs de cartes et bordures de tableaux. |
| `--color-focus-ring` | `#1F880B` (`outline 3px solid`) | Anneau de focus clavier visible sur tous les éléments interactifs. |

### Niveau 3 : Tokens de Composants (Usage Ciblé)
- **Bouton Principal :** `--btn-primary-bg: var(--color-action-primary)` (`#1D490D`), `--btn-primary-text: #FFFFFF`. *(Aucun bouton principal jaune).*
- **Bouton Secondaire :** `--btn-secondary-bg: #FFFFFF`, `--btn-secondary-text: #1D490D`, `--btn-secondary-border: 1.5px solid #1D490D`.
- **Séparation Statut de Paiement vs Disponibilité :**
  - *Disponibilité prestation :* `Disponible` (Icône `✓` + Vert), `Capacité limitée` (Icône `◔` + Ambre), `Complet / Fermé` (Icône `✕` + Gris/Erreur — non réservable).
  - *Statut transactionnel :* `En attente de confirmation` (Icône `⏳` + Bleu/Ambre), `Confirmé` (Icône `✔` + Vert), `Échoué` (Icône `⚠` + Rouge fonctionnel), `Annulé` / `Expiré`.

---

## DS-03 — Typographies, Grille, Motifs & Photographie en Contexte Local

### 3.1 Typographies
- **Titres (`Barlow Semi Condensed`, graisses `600` et `700`) :**
  - `Display / H1` : fluide de `36px` (mobile) à `56px` (ordinateur), `line-height: 1.12`.
  - `H2` : `28px` (mobile) à `40px` (ordinateur), `line-height: 1.2`.
  - `H3` : `22px` à `28px`, `line-height: 1.28`.
- **Textes & Interfaces (`Source Sans 3`, graisses `400` et `600`) :**
  - Texte courant : `16px` à `18px`, `line-height: 1.6`.
  - Informations secondaires / tableaux : `14px`, `line-height: 1.45`.
  - Police de repli système : `system-ui, -apple-system, Segoe UI, Roboto, sans-serif`.

### 3.2 Grille, Largeurs & Motifs
- **Conteneur maximal :** `1 280 px`, centré, avec marges latérales de `16px` à `20px` sur mobile et `48px` sur ordinateur.
- **Grille :** 12 colonnes sur ordinateur (`gap: 24px`), 8 colonnes sur tablette (`gap: 20px`), 1 colonne fluide sur téléphone (`320px+`).
- **Base d'espacement :** Multiples de `4px` / `8px` (`4, 8, 12, 16, 24, 32, 48, 64px`).
- **Cadrage Feuille Asymétrique :** Réservé aux grandes photographies mises en avant (`border-radius: 32px 8px 32px 8px`). Les cartes, champs et boutons conservent des rayons simples (`8px` à `12px`) et une hauteur tactile minimale de `48px`.
- **Motif radial :** Fragments légers et espacés inspirés de la géométrie radiale des feuilles du logo (`opacity: 0.04`), uniquement en bordure de section (jamais sous un bloc de texte courant).

### 3.3 Photographie en Contexte Local Camerounais (Yaoundé–Ahala)
- **Priorité 1 — Photographies réelles du site d'Ahala (`audit-assets/ecopark-real-media/`) :**
  - `balade_pirogue3.jpg` (Étang et pirogue à ECOPARK Ahala)
  - `chimpanze.jpeg` (Faune du parc animalier d'ECOPARK)
  - `chambre.jpeg` (Hébergement sur site)
  - `IMG-20260713-WA0051_043420.jpg`, `IMG_20260829_172016-1-scaled.jpg`, `IMG-20260809-WA0009.jpg` (Vues réelles du site et des espaces d'Ahala)
- **Priorité 2 — Visuels de démonstration en contexte local camerounais (`audit-assets/stitch-canopee-vivante/`) :**
  - Familles camerounaises, élèves et enseignants camerounais en excursion, étudiants camerounais en formation pratique CFP, gastronomie locale (poisson braisé, plantains) sous les pergolas.
  - **Règle de transparence :** Tout visuel conceptuel ou temporaire porte explicitement le badge `Visuel de démonstration (Contexte local Cameroun)`.
