#!/usr/bin/env python3
"""Client CLI autonome pour l'API officielle Higgsfield (https://api.higgsfield.ai).

Synchronise avec le Skill global Antigravity (`~/.gemini/config/skills/higgsfield/`).
Resout automatiquement les identifiants dans l'ordre suivant :
  1. Surcharge locale optionnelle (`.env.local` / `.env`)
  2. Variables d'environnement du processus (`HF_KEY`, `HF_API_KEY_ID` + `HF_API_KEY_SECRET`, etc.)
  3. Registre Utilisateur Windows (`HKCU\\Environment`) sans redemarrage de l'IDE
"""

from __future__ import annotations

import runpy
from pathlib import Path

GLOBAL_SKILL_SCRIPT = (
    Path.home() / ".gemini" / "config" / "skills" / "higgsfield" / "scripts" / "higgsfield_api.py"
)

if __name__ == "__main__":
    if not GLOBAL_SKILL_SCRIPT.is_file():
        raise SystemExit(f"[ERREUR] Skill global introuvable : {GLOBAL_SKILL_SCRIPT}")
    runpy.run_path(str(GLOBAL_SKILL_SCRIPT), run_name="__main__")
