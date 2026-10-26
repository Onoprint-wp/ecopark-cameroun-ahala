---
name: ecopark-design-system
description: Design System officiel d'ECOPARK Yaoundé (« Canopée vivante — Le cercle du vivant ») — Palette #FFFFFF / #1D490D / #1F880B / #EDF4E7 / #1E281B, typographies Barlow Semi Condensed & Source Sans 3, logo circulaire original sur disque blanc, contexte local camerounais et couverture des 77 écrans contractuels.
---

# ECOPARK Design System — « Canopée vivante — Le cercle du vivant »

Ce skill régit toutes les interfaces d'**ECOPARK** (Yaoundé–Ahala, Cameroun) conformément au **Prompt Maître** et au projet Google Stitch [`projects/522000543872634848`](https://stitch.withgoogle.com/projects/522000543872634848?pli=1).

## 1. Principes Directeurs & Identité
- **Nom de marque** : **ECOPARK** (avec mention `CAMEROUN` dans le logo).
- **Direction artistique** : *« Canopée vivante — Le cercle du vivant »* (concept graphique interne : le cercle rassemble, les feuilles expriment la diversité des expériences, le blanc organise la lecture). Ne jamais utiliser ce concept comme nouveau nom officiel ni slogan obligatoire.
- **Logo original obligatoire** : Utiliser exclusivement `audit-assets/ecopark-real-media/cropped-LOGO-ECOPARK-Youtube.png` sur son disque blanc avec sa couronne de feuilles et la mention rouge `CAMEROUN`. Ne jamais le redessiner avec une police approchante.
- **Zéro marque tierce dans l'expérience publique** : Aucune bannière d'agence externe (`ONOGRAPH`) ni numéro personnel ne doit figurer dans le site public. L'outil de revue des 77 écrans doit être strictement séparé de la navigation visiteur.

## 2. Palette & Jetons CSS
```css
:root {
  --color-white: #FFFFFF;        /* Surface dominante de lecture */
  --color-brand-deep: #1D490D;   /* Titres, actions principales, navigation */
  --color-brand-leaf: #1F880B;   /* Repères actifs, accents végétaux */
  --color-surface-soft: #EDF4E7; /* Brume végétale (alternance sections & formulaires) */
  --color-text: #1E281B;         /* Texte principal à fort contraste */
}
```
- **Bouton principal** : fond `#1D490D`, texte `#FFFFFF`. **Interdiction d'utiliser le jaune comme couleur d'action principale.**
- **Bouton secondaire** : fond `#FFFFFF`, texte et bordure `#1D490D`.

## 3. Typographies
- **Titres (`--font-heading`)** : `'Barlow Semi Condensed'`, graisses `600` et `700` (de `36px` sur mobile à `56px` sur grand écran).
- **Textes & UI (`--font-sans`)** : `'Source Sans 3'`, graisses `400` et `600` (`16px` à `18px` courant, `14px` secondaire).

## 4. Photographie & Contexte Local Camerounais
1. **Priorité n°1** : Photos réelles d'ECOPARK à Yaoundé-Ahala (`audit-assets/ecopark-real-media/balade_pirogue3.jpg`, `chimpanze.jpeg`, `chambre.jpeg`, `IMG-20260713-WA0051_043420.jpg`, `IMG_20260829_172016-1-scaled.jpg`, `IMG-20260809-WA0009.jpg`, `1786968889976.jpg`), badgées `Photo réelle ECOPARK — Yaoundé-Ahala`.
2. **Priorité n°2** : Visuels en contexte local camerounais (`audit-assets/stitch-canopee-vivante/local_cameroon_*.png`) montrant des familles, écoliers, apprenants CFP et plats camerounais, explicitement signalés comme `Illustration temporaire — Contexte local Cameroun`.
3. **Interdiction absolue** : Aucun contenu ni tarif en dollars (`$4.50`), aucune photo trompeuse non badgée.

## 5. Règles Métier & Garde-Fous Critiques
- **Tarifs enfants** : Ne jamais appliquer automatiquement un tarif groupe de `700 FCFA` aux enfants lorsque le billet individuel enfant est à `500 FCFA`.
- **Paiement Mobile Money (Orange Money / MTN MoMo)** : Ne jamais demander de code PIN secret dans l'interface web. Séparer clairement les états *En attente*, *Confirmé*, *Échoué*, *Annulé* et *Expiré*.
- **Billet QR** : Toujours afficher la mention `BILLET DÉMONSTRATION — PROTOTYPE` et un code lisible (`ECP-2026-84920`).
