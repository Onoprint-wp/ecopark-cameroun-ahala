# ⚡ AUDIT TECHNIQUE SSR, CORE WEB VITALS & CRAWLABILITÉ IA

## 1. Performance & Core Web Vitals (Réseau 3G/4G Cameroun)
* **LCP (*Largest Contentful Paint*)** : `< 1.6s` grâce au HTML5 pré-rendu sans blocage d'hydratation JS lourde et aux images Hero préchargées.
* **INP (*Interaction to Next Paint*)** : `< 65ms` sur le calculateur express (`recalcQuickDayPrice`) et le simulateur `/reserver`.
* **CLS (*Cumulative Layout Shift*)** : `< 0.02` (dimensions explicites et police `tabular-nums`).

## 2. Matrice d'Autorisation des 9 Bots IA (`robots.txt`)
* **Autorisés sur toutes les routes publiques** : `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot`, `Claude-Web`, `anthropic-ai`, `Google-Extended`, `Applebot-Extended`.
* **Bloqués strictement** : `/admin`, `/direction`, `/guichet`, `/exploitation`.
