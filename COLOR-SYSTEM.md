# Système de Couleurs — ECO-PARK

Palette explorée, créée et auditée sur **Adobe Color** (`Explore`, `Color Wheel`, `Contrast Checker` WCAG 2.1 et `Color Blindness Simulator`).

---

## 1. Palette Principale ECO-PARK (Sur Mesure)

| Rôle | Nom | HEX | RGB | Usage recommandé |
| :--- | :--- | :---: | :---: | :--- |
| **Primaire** | **Deep Forest Green** | `#1B4332` | `rgb(27, 67, 50)` | En-têtes, boutons principaux (CTA), navigation, identité |
| **Secondaire** | **Fresh Leaf / Emerald** | `#52B788` | `rgb(82, 183, 136)` | Badges éco, états actifs, icônes, indicateurs positifs |
| **Accent** | **Warm Earth / Ochre** | `#D4A373` | `rgb(212, 163, 115)` | Mise en avant chaleureuse, étiquettes sentiers/nature, cartes |
| **Surface claire** | **Soft Mist / Sage** | `#E9F5ED` | `rgb(233, 245, 237)` | Fond de section naturel, cartes douces, arrière-plan |
| **Texte & Sombre** | **Deep Bark / Charcoal** | `#1F2421` | `rgb(31, 36, 33)` | Corps de texte haute lisibilité, bordures fortes, mode sombre |

---

## 2. Audit d'Accessibilité (Adobe Color)

### Ratios de contraste WCAG 2.1

| Combinaison | Texte (Premier plan) | Fond (Arrière-plan) | Ratio mesuré | WCAG AA | WCAG AAA | Composants UI |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Texte principal sur surface claire** | `#1F2421` | `#E9F5ED` | **14.07 : 1** | Validé | **Validé** | Validé |
| **Bouton primaire (texte blanc)** | `#FFFFFF` | `#1B4332` | **11.08 : 1** | Validé | **Validé** | Validé |
| **Bouton primaire (texte brume)** | `#E9F5ED` | `#1B4332` | **9.89 : 1** | Validé | **Validé** | Validé |
| **Badge / Carte Terre Ocres** | `#1F2421` | `#D4A373` | **6.97 : 1** | **Validé** | Grand texte | Validé |
| **Badge / Carte Feuille Émeraude** | `#1F2421` | `#52B788` | **6.37 : 1** | **Validé** | Grand texte | Validé |

### Simulation du daltonisme (`Color Blindness Simulator`)
- **Deutéranopie** : aucun conflit (`0 conflict`)
- **Protanopie** : aucun conflit (`0 conflict`)
- **Tritanopie** : aucun conflit (`0 conflict`)

---

## 3. Palettes d'inspiration extraites d'Adobe Color Explore

1. **Forest & Nature** (`forest nature`) : `#0D2329` · `#203B3A` · `#395246` · `#6D7F6A` · `#AAB89B`
2. **This Green** (`forest nature`) : `#616C59` · `#354737` · `#2F392B` · `#302E1E` · `#0A110B`
3. **Green bokeh background forest** (`forest nature`) : `#295937` · `#0B2516` · `#163625` · `#7AA968` · `#4D814B`
4. **Green Eco Tree** (`eco green`) : `#0D590A` · `#148C11` · `#25D91A` · `#63F250` · `#C2F2B8`
5. **Eco friendly** (`eco green`) : `#2D5A27` · `#84A98C` · `#CAD2C5` · `#52796F` · `#354F52`

---

## 4. Utilisation dans le projet

- **Design Tokens JSON (W3C)** : `tokens/color-tokens.json`
- **Variables CSS + Tailwind v4 (`@theme`)** : `styles/theme.css`
- **Configuration Tailwind v3** : `tailwind.config.js`

### Exemple CSS natif
```css
@import "./styles/theme.css";

.hero-card {
  background-color: var(--bg-surface);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

.cta-button {
  background-color: var(--brand-primary);
  color: var(--on-primary);
}
```

### Exemple Tailwind CSS (v4 ou v3)
```html
<section class="bg-surface text-ink border border-mist-300 rounded-2xl p-8">
  <span class="bg-leaf-500 text-bark-900 font-medium px-3 py-1 rounded-full text-sm">
    Réserve Naturelle
  </span>
  <h1 class="text-3xl font-bold mt-4">Bienvenue à ECO-PARK</h1>
  <p class="text-ink-muted mt-2">Un espace pensé pour la biodiversité durable.</p>
  <div class="mt-6 flex gap-4">
    <button class="bg-primary hover:bg-primary-hover text-white px-5 py-2.5 rounded-xl">
      Explorer le parc
    </button>
    <button class="bg-accent text-bark-900 px-5 py-2.5 rounded-xl">
      Carte des sentiers
    </button>
  </div>
</section>
```
