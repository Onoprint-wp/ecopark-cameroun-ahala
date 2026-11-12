# 🎨 DESIGN SYSTEM STITCH : ECOPARK CAMEROUN (`.stitch/DESIGN.md`)

Ce document constitue le référentiel `.stitch/DESIGN.md` synchronisé avec `DESIGN.md`, `tokens.json` et `02_CHARTE_GRAPHIQUE_ET_MOTION_2026.md`.

* **Projet Google Stitch** : `projects/522000543872634848`
* **Direction Artistique** : **« Canopée Vivante - Le cercle du vivant » (V4)**
* **Accroche Centrale** : **« Prenez le frais. Vivez la nature. »**

## 1. Tokens Sémantiques & Tri-Thème `Zero-FOUC`
* **Palette Sémantique** :
  * `--eco-brand: #254B28` | `--eco-nature: #527A35` | `--eco-water: #176B80`
  * `--eco-lodge: #A45138` | `--eco-dining: #946015` | `--eco-cfp: #4D5685`
  * `--eco-text: #242824` | `--eco-bg: #F7F5EF` | `--eco-surface: #FFFFFF`
* **3 Thèmes supportés (`data-theme`)** :
  1. `light` : Fond `#F7F5EF`, cartes `#FFFFFF`, texte `#242824`.
  2. `dark` (OLED) : Fond `#090D16`, cartes `#111827`, texte `#F3F7F2`.
  3. `sun` (Plein Soleil Terrain) : Fond `#FFFFFF`, texte `#000000`, bordures `2px solid #143306`, contraste `>= 7.5:1`.

## 2. Règles d'Interface & Motion `60fps`
* **Typographie** : `Barlow Semi Condensed` (Titres) + `Source Sans 3` (Corps `>= 16px`), `font-variant-numeric: tabular-nums` sur tous les montants en FCFA.
* **Cibles Tactiles** : Hauteur minimale `44px` à `48px` sur tous les boutons, filtres et onglets de la barre mobile `#v4MobileBottomNav`.
* **Zéro Emoji OS** : Iconographie 100 % vectorielle SVG linéaire monochrome (`.svg-mono`).
* **Print & Sticker QR** : Profil `ISO Coated v2 / FOGRA39` (`TAC <= 300 %`), Sticker Vinyle QR `70x70 mm` avec **`Bleed 3mm`**, **`Safe Zone 4mm`**, **`300 DPI`** et polices vectorisées (**`Outlines`**).
