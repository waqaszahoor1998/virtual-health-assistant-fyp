#!/usr/bin/env bash
# Quick check: ML artifacts the Flask API expects (run from repo root).
# See docs/PROJECT_GUIDE.md for training commands.

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
MD="$ROOT/ml_models/models"

echo "Checking ml_models/models (under $MD)..."
for f in lightgbm_model.pkl symptom_vectorizer.pkl disease_encoder.pkl unique_diseases.txt; do
  if [[ -f "$MD/$f" ]]; then
    echo "  OK: $f"
  else
    echo "  MISSING: $f"
  fi
done
echo "Done. If lightgbm_model.pkl is missing, run ml_models/scripts/train_lightgbm.py after feature_engineering.py."
