# 04 — Matrice Responsive, Reflow, Zoom 200% & États Interactifs

- **Branche** : `audit/typography-accessibility-v3` (`6157dd7` / parent `0f677f8`, `vite preview` + vérification DEV ciblée `ColorAtlasDrawer`)
- **Date de mesure** : 2026-11-14 (`Chromium headless`, animations/transitions neutralisées en régime permanent pour éliminer tout état transitoire)
- **Légende** :
  - `ovfDoc` : débordement horizontal racine (`documentElement.scrollWidth - innerWidth`) — masqué à `0` par `overflow-x: clip` sur `html, body`.
  - `clip` : nœuds rognés (`text-overflow: ellipsis`, `line-clamp`, ou ancêtre `overflow-hidden`).
  - `ovf` : nœuds débordant horizontalement de leur conteneur parent ou du viewport (hors rubans `overflow-x-auto` volontaires).
  - `lowC` : nœuds DOM actifs (hors SVG & images/dégradés) avec contraste WCAG < AA (`4.5:1` normal / `3.0:1` large).
  - `tap<44` : contrôles interactifs visibles de hauteur `< 44px` sur `width <= 1024px`.

---

## 1. Matrice 10 Viewports (9 Obligatoires + `1280x800`) sur `/` (Accueil, Mode Clair)

| Viewport | `ovfDoc` | Lignes mesurées | Min / Max (`px`) | `< 12px` | `< 14px` | `clip` | `ovf` | `lowC` | `tap<44` | Capture |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `320x700` | `0px` | 329 | `10` / `48` | 47 | 213 | **18** | 0 | 0 | **14** | [home_320x700_light.png](./screenshots/before/home_320x700_light.png) |
| `360x800` | `0px` | 329 | `10` / `48` | 47 | 213 | **16** | 0 | 0 | **14** | *(mesuré)* |
| `390x844` | `0px` | 329 | `10` / `48` | 47 | 213 | **16** | 0 | 0 | **14** | [home_390x844_light.png](./screenshots/before/home_390x844_light.png) |
| `430x932` | `0px` | 329 | `10` / `48` | 47 | 213 | **13** | 0 | 0 | **14** | [home_430x932_light.png](./screenshots/before/home_430x932_light.png) |
| `768x1024` | `0px` | 332 | `10` / `48` | 47 | 178 | **12** | 0 | 0 | **14** | [home_768x1024_light.png](./screenshots/before/home_768x1024_light.png) |
| `1024x768` | `0px` | 340 | `10` / `53.25` | 47 | 179 | **15** | **1** (`Footer`) | 0 | **17** | [home_1024x768_light.png](./screenshots/before/home_1024x768_light.png) |
| `1280x800` | `0px` | 345 | `10` / `66.56` | 47 | 184 | **12** | 0 | 0 | *(n/a)* | *(mesuré)* |
| `1366x768` | `0px` | 345 | `10` / `71.03` | 47 | 184 | **9** | 0 | 0 | *(n/a)* | *(mesuré)* |
| `1440x900` | `0px` | 345 | `10` / `74.88` | 47 | 184 | **7** | 0 | 0 | *(n/a)* | [home_1440x900_light.png](./screenshots/before/home_1440x900_light.png) |
| `1920x1080` | `0px` | 346 | `10` / `80` | 47 | 185 | **6** | 0 | 0 | *(n/a)* | [home_1920x1080_light.png](./screenshots/before/home_1920x1080_light.png) |

### Sondes typographiques calculées sur `/` (Mode Clair)

| Élément mesuré | `320x700` | `390x844` | `1440x900` | Police calculée | Observation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temps 1 `Garantie Météo RN3` | `12px / 16px` (`ellipsis:+418px`) | `12px / 16px` (`ellipsis:+351px`) | `12px / 16px` | Source Sans 3 | Coupé sur mobiles `< 640px` |
| Marque `ECOPARK CAMEROUN` | `16px / 16px` (`ellipsis:+12px`) | `16px / 16px` | `20px / 20px` | Barlow Semi Condensed | Coupé à `320px` (et `1366–1440px` sur `/exploitation`) |
| Sous-titre `Yaoundé - Ahala • Dès 500 FCFA` | `10px / 15px` (`ellipsis:+33px`) | `10px / 15px` | `11px / 16.5px` | Source Sans 3 | `< 12px` sur tous viewports |
| Lien `.type-nav` (`Carte & Activités`) | *(drawer)* | *(drawer)* | `12px / 16px` (`ls -0.12px`) | Source Sans 3 | `< 14px` sur desktop |
| `.type-hero` (`Complexe écologique et loisirs`) | `48px / 52px` (`ls -0.144px`) | `48px / 52px` | `74.88px / 78.62px` (`ls -1.1232px`) | Barlow Semi Condensed | `80px` à `1920px` ; `11.08:1` |
| `.type-tagline` (`Respirez en forêt...`) | `19px / 23px` (`ls 0.228px`) | `19px / 23px` | `24px / 28px` (`ls 0.216px`) | Barlow Semi Condensed | `19px < 20px` display sur mobile |
| `.type-body` (`Jardin Zoologique...`) | `15px / 22px` (`ls -0.24px`) | `15px / 22px` | `17px / 25px` (`ls -0.374px`) | Source Sans 3 | `< 16px` mobile + tracking négatif |
| `hotel-price-range` (`10 000 à 15 000 FCFA`) | `12px / 16px` | `12px / 16px` | `12px / 16px` | **Source Sans 3** *(attendu JetBrains Mono)* | Écrasement cascade CSS par `.type-footnote` unlayered |

---

## 2. Matrice des 14 Routes Publiques + Cockpit `/exploitation` (Light vs Dark)

| Route | Onglet / Vue vérifié | `390x844` Light (`clip` / `ovf` / `lowC` / `tap<44`) | `390x844` Dark (`lowC`) | `1440x900` Light (`clip` / `lowC`) | `1440x900` Dark (`lowC`) | Constats dominants |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `/` | Accueil | `16` / `0` / `0` / `14` | `0` | `7` / `0` | `0` | Temps 1, légendes Hero, `line-clamp-2` sentiers |
| `/hebergements` | `panel-hebergements` actif | `16` / `0` / `0` / `14` | `0` | `7` / `0` | `0` | `.type-footnote.font-mono` rendu en `Source Sans 3` |
| `/restaurant` | `panel-saveurs` actif | `16` / `0` / `0` / `14` | `0` | `7` / `0` | `0` | Titres tronqués sur cartes Showcase/Accueil |
| `/tarifs` | `panel-tarifs` actif (`<table>`) | `16` / `0` / `0` / `14` | `0` | `7` / `0` | `0` | Idem |
| `/pack-entreprise` | `panel-entreprise` actif | `16` / `0` / `0` / `14` | `0` | `7` / `0` | `0` | Idem |
| `/formation` | `panel-formation` actif | `16` / `0` / `0` / `14` | `0` | `7` / `0` | `0` | Idem |
| `/activites` | Carte SVG + Catalogue | `7` / **`6`** / **`1`** / **`41`** | **`6`** | `2` / **`1`** | **`6`** | `Calques` (`+44/+81px` à `390px`, `+112/+148px` à `320px`, `+5/+42px` `POIs` et `+4px` `Sportif` à `430x932`, `+24px` à `1024px`) ; `Avis Éco-Garde` `4.16:1` Light / `1.68–2.64:1` Dark |
| `/decouvrir` | `SpeciesAtlas` | `1` / **`1`** / **`1`** / **`26`** | **`19`** | `0` / **`1`** | **`19`** | `<select>` UICN **`+132px`** à `390px` (`+199px` à `320px`, `+48/+93px` à `430x932`) ; `bg-emerald-50` Dark = **`1.40:1`** ; onglet `2.47:1` Dark |
| `/reserver` | `BookingWizard` Étape 1 | `1` / `0` / **`1`** / **`14`** | **`3`** | `0` / **`1`** | **`3`** | `858 places` **`3.26:1`** Light ; pastille + CTA **`2.47:1`** Dark |
| `/mon-espace` | `DigitalEcoPass` anon. | `1` / `0` / `0` / **`16`** | **`3`** | `0` / `0` | **`3`** | 3 boutons `--brand-primary` + `text-white` = **`2.47:1`** Dark |
| `/connexion` | `AuthPortal` login | `1` / `0` / `0` / **`16`** | **`1`** | `0` / `0` | **`1`** | Bouton `Se connecter` = **`2.47:1`** Dark |
| `/mentions-legales` | `LegalNoticeView` (`mentions`) | `1` / `0` / `0` / **`22`** | **`1`** | `0` / `0` | **`1`** | Corps légal `12px / 16px` ; onglet actif = **`2.47:1`** Dark |
| `/cgv` | `LegalNoticeView` (`cgv`) | `1` / `0` / `0` / **`18`** | **`1`** | `0` / `0` | **`1`** | Corps légal `12px / 16px` ; onglet actif = **`2.47:1`** Dark |
| `/confidentialite` | `LegalNoticeView` (`confid.`) | `1` / `0` / `0` / **`19`** | **`1`** | `0` / `0` | **`1`** | Corps légal `12px / 16px` ; onglet actif = **`2.47:1`** Dark |
| `/exploitation` | `RangerDashboard` (`admin`) | `0` / **`1`** (`+226px`) / **`14`** / **`31`** | **`41`** | **`2`** (`marque`) / **`14`** | **`41`** | `<select>` `+226px` (`+293px` à `320px`, `+163px` à `430x932`), `Administration` `+7px` à `1280px`, marque coupée à `1366–1440px`, boutons `-600` & `amber-700` < AA, Dark `1.12–3.13:1` |

*(Les 6 routes principales `/`, `/activites`, `/decouvrir`, `/reserver`, `/tarifs` et `/exploitation` ont été contrôlées sans débordement documentaire racine `ovfDoc = 0px` sur l'ensemble des 10 viewports en mode clair ; les 9 autres routes publiques sur 5 viewports Light/Dark `320`, `390`, `430`, `768`, `1440` ; et toutes les 15 routes à `430x932` Light/Dark avec `ovfDoc = 0px`. Hors `/` et grilles `#`, `Footer` `24h/24 · 7j/7` déborde de `parent-out:+32px` à `1024x768`.)*

---

## 3. Matrice Zoom 200% & Reflow WCAG 1.4.4 / 1.4.10

| Scénario | Route & Viewport | Mode appliqué | `ovfDoc` | Éléments `fixed-px` vs baseline | `clip` / `ovf` combinés | Observations mesurées | Capture |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `/_390x844_font200` | `/` (`390x844`) | `html { font-size: 32px }` | `0px` | **53** nœuds | **43** | `.type-hero` (`96px`) **`ancestor-clip:+113px`** (`scrollW 423 > clientW 310` dans `ImmersiveSection`), `à Yaoundé, Ahala.` déborde (`+44px`), marque réduite à `"E."` / `"YA..."`, Temps 1 & Bento figés | [zoom_font200_390x844.png](./screenshots/before/zoom_font200_390x844.png) |
| `/_1440x900_font200` | `/` (`1440x900`) | `html { font-size: 32px }` | `0px` | **60** nœuds | **39** | `.type-hero` (`104px`, `pass`) ; header/chapternav débordent dans leurs boîtes (`642/1500` `+97px`, `Client` `+615px`, `Groupes...` `+434px`) | [zoom_font200_1440x900.png](./screenshots/before/zoom_font200_1440x900.png) |
| `/decouvrir_390x844_font200` | `/decouvrir` (`390x844`) | `html { font-size: 32px }` | `0px` | *(non comparé : delta non passé)* | **43** | `<select>` `Tous statuts (8)` déborde jusqu'à `+532px/+613px`, badges `UICN` jusqu'à `+236px` | *(mesuré)* |
| `/reserver_390x844_font200` | `/reserver` (`390x844`) | `html { font-size: 32px }` | `0px` | *(non comparé : delta non passé)* | **6** | Étape `3` du stepper déborde (`vp-right:+59px;parent-out:+132px`) ; Temps 1, marque & Footer | *(mesuré)* |
| `/_1440x900_csszoom2` | `/` (`1440x900`) | `html { zoom: 2 }` | `0px` | *(n/a zoom CSS)* | **44** | `.type-hero` (`74.88px`), header/chapternav débordent (`642/1500` `+156px`, `Client` `+700px`, `CFP Agréé` `+886px`) | *(mesuré)* |
| `/tarifs_640x400_reflow640` | `/tarifs` (`640x400`) | Viewport `640x400` (~200% d'un 1280px) | `0px` | *(reflow)* | **6** | Reflow sans barre horizontale racine ; `.type-hero` `48px` conforme ; `6` troncatures résiduelles (légendes Hero & cartes) | *(mesuré)* |
| `/exploitation_1440x900_font200` | `/exploitation` (admin, `1440x900`) | `html { font-size: 32px }` | `0px` | **339** nœuds | **2** | Majorité du cockpit en `px` Tailwind/arbitraires reste figée ; `Cockpit Pro`, `642/1500`, `Administration` débordent ; `Difficile` `+30px` | *(mesuré)* |

*(Contrôle complémentaire sur `/` à `430x932` avec `html { font-size: 32px }` : `ovfDoc = 0px`.)*

---

## 4. Matrice Exhaustive des États Interactifs, Modales & Rôles RBAC (Tous Capturés au Runtime)

| État / Scénario mesuré | Lignes | `P0` / `P1` | Résultats mesurés & visuels | Capture / Preuve |
| :--- | :---: | :---: | :--- | :--- |
| **`MobileDrawer` ouvert (`320x700` & `390x844`)** | 31 | `1` / `17` | Tiroir lisible en Light ; Temps 1 derrière en-tête coupé (`ellipsis:+351px`) | [state_mobile_drawer_320x700.png](./screenshots/before/state_mobile_drawer_320x700.png) |
| **`ImpactBanner` tiroirs BLUF ouverts (`390` & `1440`)** | 329+ | *inclus `/`* | BLUF affiché sans rognage ; description Bento reste figée en `14px` (`!text-[14px]`) | [state_bento_drawer_390x844.png](./screenshots/before/state_bento_drawer_390x844.png) |
| **`BookingWizard` Étape 2 (`390x844`, erreurs)** | 111 | `4` / *ref.* | `3` messages d'erreur rouges `text-red-600` à **`4.26:1`** (< `4.5:1`) + Temps 1 tronqué + steppers `w-8 h-8` (`32px`) | [state_booking_step2_390x844.png](./screenshots/before/state_booking_step2_390x844.png) |
| **`BookingWizard` Étape 3 (`390x844`) & Confirm** | 123 / 118 | `4` / `2` | `-0 FCFA` (`3.26:1`), `+8,4 kg CO₂` (`3.26:1`), checkbox `on` (`3.49:1`), `text-[11px]` | [state_booking_step3_390x844.png](./screenshots/before/state_booking_step3_390x844.png) |
| **`DigitalEcoPass` Recto / Verso (`390x844`)** | 118 | `2` / *ref.* | `+8,4 kg CO₂` (**`3.65:1`**), `text-[11px]` multiples, cibles `< 44px` | [state_ecopass_recto_390x844.png](./screenshots/before/state_ecopass_recto_390x844.png) |
| **`DigitalEcoPass` modes `Plein Soleil` & `OLED`** | 135 / 135 | `1` / `46` | `+8,4 kg CO₂` reste à **`3.65:1`** ; en mode `OLED`, les tuiles internes restent sur fond blanc hors thème sombre global | [state_ecopass_oled_1440x900.png](./screenshots/before/state_ecopass_oled_1440x900.png) |
| **`CitizenSentinel` `form` & `feed` (client auth)** | 132 / 178 | `0` / `45` & `81` | Contraste `>= AA` sur flux & cartes, mais `45`–`81` P1 (`text-[10px]`/`text-[11px]` métadonnées photo) | [state_sentinel_feed_1440x900.png](./screenshots/before/state_sentinel_feed_1440x900.png) |
| **`AuthPortal` modes `register` / `staff` / `recover`** | 87 / 78 / 81 | `1` / `4` / `1` | Sur `#staff` : `Cockpit Pro` & `Accès Réservé...` à `4.49:1`, bouton `Ouvrir le Cockpit Pro` à **`3.20:1`** | *(mesuré CSV)* |
| **Daltonisme `Deutéranopie` (`1440x900`)** | *(DOM root)* | *(filtre)* | `data-vision="deuteranopia"` actif, `html { filter: url("#filter-deuteranopia") }` vérifié | [state_daltonism_deuteranopia_1440x900.png](./screenshots/before/state_daltonism_deuteranopia_1440x900.png) |
| **`ColorAtlasDrawer` (`vite dev` 3 onglets)** | 181 | `4` / `87` | `#scales` : **`4` P0** (`2.87:1`–`4.40:1`), **`83` nœuds `< 12px`** sur badges `9px–11px` ; en prod `/atelier-couleurs` redirige vers Accueil | [state_color_atlas_dev_1440x900.png](./screenshots/before/state_color_atlas_dev_1440x900.png) |
| **`/exploitation` RBAC (`unauth`, `403`, `guichet`, `comptable`, modale)** | 68 / 61 / 333 / 379 / 14 | `4` / `1` / `2` / `1` / `0` | `unauth` : `4` P0 (`3.20–4.49:1`) ; `403` : `1` P0 (`4.49:1`) ; `guichet` : `2` P0 (`Check-In` `3.65`, badge `4.49`) + `30` P2 disabled ; `comptable` : `1` P0 (`4.49`) + `30` P2 disabled ; modale fermeture : `0` P0 | [cockpit_guichet_1440x900_light.png](./screenshots/before/cockpit_guichet_1440x900_light.png) |

---

## 5. Index des Captures Avant Correction (`docs/ux-audit/screenshots/before/`) — **54 PNG**

- **Viewports `/` (Light & Dark)** : `home_320x700_light.png`, `home_390x844_light.png`, `home_390x844_light_full.png`, `home_430x932_light.png`, `home_430x932_dark.png`, `home_768x1024_light.png`, `home_1024x768_light.png`, `home_1440x900_light.png`, `home_1440x900_light_full.png`, `home_1920x1080_light.png`, `home_390x844_dark.png`, `home_1440x900_dark.png`.
- **Zoom 200%** : `zoom_font200_390x844.png`, `zoom_font200_1440x900.png`.
- **Routes publiques (Light & Dark)** : `route_hebergements_390x844_light.png`, `route_hebergements_1440x900_light.png`, `route_hebergements_1440x900_dark.png`, `route_restaurant_1440x900_light.png`, `route_tarifs_390x844_light.png`, `route_tarifs_1440x900_light.png`, `route_tarifs_1440x900_dark.png`, `route_pack_entreprise_1440x900_light.png`, `route_formation_1440x900_light.png`, `route_activites_390x844_light.png`, `route_activites_430x932_light.png`, `route_activites_1440x900_light.png`, `route_decouvrir_390x844_light.png`, `route_decouvrir_430x932_light.png`, `route_decouvrir_1440x900_light.png`, `route_reserver_step1_390x844_light.png`, `route_reserver_step1_1440x900_light.png`, `route_mon_espace_anon_390x844_light.png`, `route_mon_espace_anon_1440x900_light.png`, `route_legal_cgv_390x844_light.png`.
- **Cockpit `/exploitation` (RBAC & Modale)** : `cockpit_admin_390x844_light.png`, `cockpit_admin_430x932_light.png`, `cockpit_admin_1440x900_light.png`, `cockpit_admin_1440x900_dark.png`, `cockpit_guichet_1440x900_light.png`, `cockpit_comptable_1440x900_light.png`, `cockpit_modal_closure_1440x900.png`.
- **États interactifs & DEV** : `state_mobile_drawer_320x700.png`, `state_mobile_drawer_390x844.png`, `state_bento_drawer_390x844.png`, `state_bento_drawer_1440x900.png`, `state_booking_step2_390x844.png`, `state_booking_step3_390x844.png`, `state_ecopass_recto_390x844.png`, `state_ecopass_verso_390x844.png`, `state_ecopass_sunlight_1440x900.png`, `state_ecopass_oled_1440x900.png`, `state_sentinel_feed_1440x900.png`, `state_daltonism_deuteranopia_1440x900.png`, `state_color_atlas_dev_1440x900.png`.
