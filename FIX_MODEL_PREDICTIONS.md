# Fix for Model 0% Accuracy Issue

## Problem

The XGBoost model was showing 0% accuracy because:
- Default `predict()` uses threshold 0.5
- With 1,140 diseases and sparse data, probabilities are all below 0.5
- Model predicts all zeros

## Solution

Changed prediction strategy from **threshold-based** to **top-k predictions**:

### Before (Threshold-based):
```python
y_pred = model.predict(X_test)  # Uses 0.5 threshold → all zeros
```

### After (Top-k):
```python
# Predict top-5 diseases per sample
# Always make at least 1 prediction per sample
# Use very low threshold (0.01) to ensure predictions
```

## Changes Made

1. **Top-K Strategy**: Predict top 5 diseases per sample
2. **Low Threshold**: 0.01 instead of 0.5
3. **Guaranteed Predictions**: At least 1 prediction per sample

## Next Steps

Re-run training:
```bash
cd ml_models/scripts
python train_xgboost.py
```

Expected improvement: Model should now make predictions and show non-zero accuracy.

---

**Note**: This is a common issue with sparse multi-label classification. Top-k strategy is more appropriate than threshold-based for this use case.

