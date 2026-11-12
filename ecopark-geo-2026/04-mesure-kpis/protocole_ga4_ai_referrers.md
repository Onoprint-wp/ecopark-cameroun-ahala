# 📈 PROTOCOLE DE TRACKING DES RÉFÉRENTS IA (`detectAiReferrer`) & ATTRIBUTION GEO

## 1. Détection Automatique des Moteurs IA dans le Front-Office
La fonction `detectAiReferrer()` intégrée dans `etape0-site-live/index.html` inspecte `document.referrer` et les paramètres `utm_source` pour identifier et enregistrer les visites issues des moteurs de réponse IA :
* `chatgpt.com` / `chat.openai.com` -> Canal `AI_SEARCH_CHATGPT`
* `perplexity.ai` -> Canal `AI_SEARCH_PERPLEXITY`
* `claude.ai` -> Canal `AI_SEARCH_CLAUDE`
* `gemini.google.com` -> Canal `AI_SEARCH_GEMINI`
* `copilot.microsoft.com` -> Canal `AI_SEARCH_COPILOT`
* `?utm_source=sticker_sav_qr` -> Canal physique `PRINT_QR_STICKER_AHALA`

## 2. Rattachement au Baromètre de Direction (`DIR-02`)
Chaque réservation ou demande de devis issue d'un référent IA conserve son canal d'origine dans `localStorage` (`ecopark_ai_referrer_channel`) afin d'alimenter la vue analytique Direction `DIR-02`.
