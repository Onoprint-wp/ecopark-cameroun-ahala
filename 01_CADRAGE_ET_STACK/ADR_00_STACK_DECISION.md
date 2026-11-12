# 🧭 ADR 00 : DÉCISION D'ARCHITECTURE & RADAR TECHNOLOGIQUE 2026 (`ADR_00_STACK_DECISION.md`)

Ce fichier est synchronisé avec `/ADR_00_STACK_DECISION.md` à la racine du dépôt.

* **Profil retenu** : **Hybride `PROFIL A` (Zero-Build Ultra-Fast Web) + `PROFIL C` (Dual-DB Offline-First SaaS/POS + Supabase RLS) + `PROFIL D` (PWA Mobile Terrain Offline-First)**.
* **Langage Principal** : **JavaScript ES2024 (ESM) / SQL PostgreSQL 16 (PL/pgSQL) / HTML5 / CSS3** (avec tests E2E Playwright en Python 3.12 et tests de contrat PGlite en Node.js 22).
