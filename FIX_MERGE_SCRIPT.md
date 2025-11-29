# Critical Fix: Merge Script Issue

## Problem Found

The merge script was **grouping all records by disease** and combining symptoms, which:
- ✅ Reduced dataset from thousands to 1,140 records (1 per disease)
- ❌ This is **wrong for ML training** - we need multiple samples per disease!

## Why This Is Bad

For machine learning:
- We need **multiple training examples per disease**
- The model learns from seeing the same disease with different symptom combinations
- 1 record per disease = model can't learn patterns

## Fix Applied

Changed merge script to **keep all individual records** instead of merging by disease:
- Preserves all training samples
- Multiple records per disease = better training data
- Should give us thousands of records instead of 1,140

## Next Steps

1. **Re-run merge script** to create proper expanded dataset:
   ```bash
   python data/scripts/merge_datasets.py
   ```

2. **Re-run feature engineering** with new expanded dataset:
   ```bash
   cd ml_models/scripts
   python feature_engineering.py
   ```

3. **Re-train models** with more training samples:
   ```bash
   python train_xgboost.py
   ```

Expected result:
- Before: 1,140 records (1 per disease) → 794 training samples
- After: 7,000+ records (multiple per disease) → 5,000+ training samples
- This should fix the 0% accuracy issue!

