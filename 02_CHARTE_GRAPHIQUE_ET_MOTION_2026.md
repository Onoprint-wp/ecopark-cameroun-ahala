# 🎨 DESIGN SYSTEM & CHORÉGRAPHIE MOTION 2026 (`02_CHARTE_GRAPHIQUE_ET_MOTION_2026.md`)

* **Projet** : **ECOPARK CAMEROUN (Yaoundé - Ahala, RN3)**
* **Direction Artistique** : **« Canopée Vivante - Le cercle du vivant » (V4)**
* **Projet Google Stitch** : `projects/522000543872634848`
* **Référentiel W3C DTCG** : `tokens.json`

---

## 1. Architecture Chromatique Sémantique (`60-30-10`) & Moteur Tri-Thème `Zero-FOUC`

### 1.1Les 9 Tokens de Base « Canopée Vivante » (`--eco-*`)
* `--eco-brand` : `#254B28` (Vert Canopée Maître - CTA principaux, en-têtes statutaires)
* `--eco-nature` : `#527A35` (Vert Feuille & Faune - Pôle Zoo, Forêt & Botanique)
* `--eco-water` : `#176B80` (Bleu Lagon Ahala - Pôle Piscine, Lac & Pirogue)
* `--eco-lodge` : `#A45138` (Terre Cuite Hospitalité - Pôle 4 Cités Hôtelières : `Ewondo`, `Suites Privées`, `Chanthel`, `Bene`)
* `--eco-dining` : `#946015` (Ocre Doré Gastronomie - Restaurant *Le Château des Saveurs*)
* `--eco-cfp` : `#4D5685` (Indigo Académique - Centre de Formation Professionnelle CFP MINEFOP)
* `--eco-text` : `#242824` (Encre Végétale Haute Lisibilité - Contraste `> 13:1`)
* `--eco-bg` : `#F7F5EF` (Sable Botanique Naturel - Fond général `60 %`)
* `--eco-surface` : `#FFFFFF` (Blanc Pur Disque Logo - Cartes et tableaux)

### 1.2 Moteur Tri-Thème `Zero-FOUC` (`Light` / `Dark OLED` / `Sun Mode Terrain`)

| Thème (`data-theme`) | Fond Principal | Surface Carte | Texte Principal | Contraste Min | Usage Cible |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`light` (Défaut)** | `#F7F5EF` | `#FFFFFF` | `#242824` | `13.4:1 (AAA)` | Navigation familiale, découverte du parc et réservation en journée. |
| **`dark` (OLED `#090D16`)** | `#090D16` | `#111827` | `#F3F7F2` | `14.8:1 (AAA)` | Consultation nocturne, économie batterie OLED et poste de supervision. |
| **`sun` (Plein Soleil)** | `#FFFFFF` | `#FFFFFF` | `#000000` | `>= 7.5:1 (AAA)` | Agents de portail QR (`AGT-05`) et visiteurs sous soleil zénithal d'Ahala (`12h-15h`) : bordures renforcées `2px`, `backdrop-filter: none`. |

---

## 2. Typographie Fluide, Alignement Tabulaire FCFA & Élasticité Bilingue (`FR/EN +30 %`)

* **Titrages (`Barlow Semi Condensed`, `600`/`700`)** : `clamp(2.25rem, 4vw, 3.5rem)` sur le `H1` unique de l'accueil (`Prenez le frais. Vivez la nature.`).
* **Corps & Tableaux (`Source Sans 3`, `400`/`600`)** : `>= 16px` sur le corps de texte, `line-height: 1.6`.
* **Discipline Financière (`Loi 3.1`)** : Tous les prix en `FCFA`, compteurs de caisse (`AGT-03`, `AGT-09`), jauges (`ADM-03`) et totaux analytiques (`DIR-05`) appliquent obligatoirement `font-variant-numeric: tabular-nums`.
* **Élasticité Linguistique (`i18n FR/EN`)** : Tous les conteneurs de boutons et d'onglets acceptent une expansion de texte de `+30 %` sans troncature ni débordement horizontal de `320px` à `1440px`.

---

## 3. Chorégraphie Motion `60fps` & Accessibilité (`prefers-reduced-motion`)

* **Propriétés GPU Exclusives (`Loi 2.2`)** : Seules les propriétés composites `transform` (`translate3d`, `scale`) et `opacity` sont animées selon la courbe `cubic-bezier(0.16, 1, 0.3, 1)`. Aucune animation sur `width`, `height`, `top` ou `left`.
* **4 Timelines HyperFrames Actives** :
  1. `ecopark-hero-reel` : Sélecteur cinématique des 4 scènes d'Ahala.
  2. `ecopark-ahala-map` : Tracé vectoriel SVG reliant `RN3 Tradex -> Zone A -> Zone B -> Zone C -> Zone D -> Zone E`.
  3. `ecopark-qr-pass` : Odomètre FCFA (`150ms`) et déploiement du billet QR `ECP-2026-XXXXX`.
  4. `ecopark-rdv-flow` : Ouverture fluide des modales de rendez-vous et d'impression officielle A4.
* **Respect `prefers-reduced-motion: reduce`** : Désactivation instantanée de toutes les transitions cinétiques pour les utilisateurs sensibles.

---

## 4. Normes d'Impression Industrielle `CMJN FOGRA39` & Sticker Vinyle QR (`Bleed 3mm`)

### 4.1 Table de Correspondance Chromatique Print (`TAC <= 300 %`)

| Couleur Charte | Web HEX | Offset CMJN (`ISO Coated v2 / FOGRA39`) | Sérigraphie Pantone | Acier / Signalétique RAL |
| :--- | :---: | :--- | :--- | :--- |
| **Vert Canopée Profond** | `#1D490D` / `#254B28` | `C82 M32 Y100 K56` *(TAC 270 %)* | **Pantone 3435 C** | **RAL 6005** *(Vert mousse)* |
| **Vert Feuille Vivante** | `#1F880B` / `#527A35` | `C83 M5 Y100 K12` *(TAC 200 %)* | **Pantone 362 C** | **RAL 6018** *(Vert jaune)* |
| **Bleu Lagon Ahala** | `#176B80` | `C85 M30 Y25 K10` *(TAC 150 %)* | **Pantone 7705 C** | **RAL 5021** *(Bleu d'eau)* |
| **Terre Cuite Loges** | `#A45138` | `C20 M75 Y85 K15` *(TAC 195 %)* | **Pantone 7523 C** | **RAL 8004** *(Brun cuivré)* |
| **Ocre Bronze Saveurs** | `#C47D2B` / `#946015` | `C18 M52 Y92 K8` *(TAC 170 %)* | **Pantone 7565 C** | **RAL 1024** *(Jaune ocre)* |
| **Encre Végétale** | `#1E281B` / `#242824` | `C75 M60 Y72 K80` *(Titres)* / `K100` *(Corps)* | **Pantone 419 C** | **RAL 6015** *(Olive noir)* |

### 4.2 Gabarit Normalisé : Sticker Vinyle Indélébile QR Code (Tables Restaurant, Loges & SAV Équipement)
* **Usage Terrain** : Collé sur chaque table du *Château des Saveurs* (commande & carte FCFA), dans chaque chambre des 4 Cités Hôtelières (réception & room-service WhatsApp) et sur chaque équipement de caisse/borne QR (support technique SAV en 1 scan).
* **Spécifications Prépresse Obligatoires (`Loi 2.4`)** :
  * **Format Fini (*Trim Box*)** : `70 mm x 70 mm` (coins arrondis rayon `6 mm`).
  * **Fond Perdu (*Bleed*)** : **`3 mm` sur les 4 côtés** (format fichier brut `76 mm x 76 mm`).
  * **Zone de Sécurité Interne (*Safe Zone*)** : **`4 mm` à l'intérieur du trait de coupe** (aucun texte ni module QR dans cette marge).
  * **Résolution & Vectorisation** : **`300 DPI` réels** + **100 % des polices converties en courbes (*Outlines*)**.
  * **Support & Finition Tropicale** : Vinyle polymère adhésif permanent `3M` + lamination mate anti-UV, anti-humidité et résistante aux nettoyages détergents quotidiens.
  * **QR Code Dynamique Tracé** : Correction d'erreur **Niveau H (`30 %`)**, contraste `100 % K` sur réserve blanche `#FFFFFF`, URL tracée `?utm_source=sticker_sav_qr`.
