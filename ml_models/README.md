# ML models (training + artifacts)

Scripts build TF-IDF features and train classifiers; the **Flask app** loads outputs from `models/` via `backend/app/utils/ml_service.py`.

## Train the model the API uses (LightGBM)

From `ml_models/scripts/`:

```bash
python feature_engineering.py
python train_lightgbm.py
```

This expects processed data under `data/processed/` (see `feature_engineering.py` for filenames). It writes **`models/lightgbm_model.pkl`** plus vectorizer/encoder pickles and `metadata.json`.

## Other scripts

`train_xgboost.py`, `train_random_forest.py`, `train_neural_network.py`, `train_stacking_ensemble.py`, etc. are for **experiments**; only LightGBM (and optionally XGBoost/RF if `.pkl` files exist) is wired in `ml_service.py` unless you extend that module.

## Documentation

**[docs/PROJECT_GUIDE.md](../docs/PROJECT_GUIDE.md)** — metrics, `DEMO_ML_FALLBACK`, and troubleshooting.
