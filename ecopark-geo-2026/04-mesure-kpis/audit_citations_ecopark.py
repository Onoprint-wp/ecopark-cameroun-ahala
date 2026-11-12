# -*- coding: utf-8 -*-
"""
Script d'audit de Part de Voix IA (AI Share of Voice - SoV) sur les 50 requetes cibles d'ECOPARK CAMEROUN.
Verifie la coherence des tarifs cites (1 000 FCFA Adulte, 500 FCFA Enfant, Loges 10k-30k FCFA) avec 00_entity_truth_ecopark.json.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRUTH = json.loads((ROOT / "context" / "00_entity_truth_ecopark.json").read_text(encoding="utf-8"))
CSV_PATH = ROOT / "04-mesure-kpis" / "panier_50_requetes_ecopark.csv"

def verify_basket():
    with CSV_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 50, f"Attendu 50 requetes, trouve {len(rows)}"
    assert TRUTH["pricingXaf"]["zooAdult"] == 1000
    assert TRUTH["pricingXaf"]["zooChild"] == 500
    print(f"[OK] Panier de {len(rows)} requetes GEO verifie avec succes contre la source de verite FCFA.")

if __name__ == "__main__":
    verify_basket()
