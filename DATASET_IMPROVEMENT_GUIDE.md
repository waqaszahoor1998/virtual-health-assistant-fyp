# Complete Dataset Improvement Guide

## 🎯 Goal: Improve ML Model Accuracy

**Current Performance:**
- Training Samples: 753
- Exact Match Accuracy: 7-8%
- Precision: 85-87%

**Target Performance:**
- Training Samples: 10,000-15,000
- Expected Accuracy: 60-80%
- Expected Precision: 90-95%

---

## 📋 Complete Workflow

### Step 1: Install Kaggle API

```bash
pip install kaggle
```

### Step 2: Set Up Kaggle Credentials

1. Create a Kaggle account (if you don't have one): https://www.kaggle.com/
2. Go to Account Settings → API → Create New API Token
3. Download `kaggle.json`
4. Place it in your home directory:
   - **macOS/Linux**: `~/.kaggle/kaggle.json`
   - **Windows**: `C:\Users\YourUsername\.kaggle\kaggle.json`
5. Set correct permissions:
   - **macOS/Linux**: `chmod 600 ~/.kaggle/kaggle.json`
   - **Windows**: Right-click → Properties → Security → Remove all permissions except your user

### Step 3: Download Additional Datasets

Run the download script:

```bash
python data/scripts/download_kaggle_datasets.py
```

**Expected downloads:**
- Disease Symptom Description Dataset (~5,000 records)
- Symptom2Disease Dataset (~1,200 records)
- Disease Prediction ML Dataset (~5,000 records)
- Medical Symptoms Dataset (~3,000 records)

**Total expected: 14,000+ records**

---

### Step 4: Normalize Datasets

Normalize all downloaded datasets to a common format:

```bash
python data/scripts/normalize_datasets.py
```

**What this does:**
- Standardizes symptom names across datasets
- Standardizes disease names
- Handles different file formats
- Removes duplicates
- Creates unified format

**Output:**
- `datasets/processed/normalized_datasets.xlsx`
- Statistics: `datasets/processed/normalization_stats.json`

---

### Step 5: Merge Datasets

Merge normalized datasets with existing cleaned dataset:

```bash
python data/scripts/merge_datasets.py
```

**What this does:**
- Combines all normalized datasets
- Merges with existing dataset
- Groups by disease and combines symptoms
- Validates data quality
- Creates final training-ready dataset

**Output:**
- `data/processed/dataset_expanded_final.xlsx`
- Statistics: `data/processed/expanded_dataset_stats.json`

---

### Step 6: Update Feature Engineering

The feature engineering script now automatically detects and uses the expanded dataset if available.

Run feature engineering:

```bash
cd ml_models/scripts
python feature_engineering.py
```

**What this does:**
- Loads expanded dataset (or falls back to original)
- Creates TF-IDF feature vectors
- Prepares disease labels
- Splits into train/val/test sets

**Output:**
- Preprocessed data in `ml_models/models/`
- Feature matrices (X_train, X_val, X_test)
- Label matrices (y_train, y_val, y_test)
- Vectorizer and encoder objects

---

### Step 7: Retrain Models

Train XGBoost model:

```bash
python train_xgboost.py
```

Train Random Forest model:

```bash
python train_random_forest.py
```

**Expected improvements:**
- More accurate predictions
- Better disease coverage
- More robust model performance

---

### Step 8: Compare Results

Compare old vs new model performance:

**Old Metrics (753 samples):**
- Exact Match Accuracy: 7-8%
- Precision: 85-87%

**New Metrics (10,000+ samples) - Expected:**
- Exact Match Accuracy: 60-80%
- Precision: 90-95%

---

## 📊 Dataset Sources

### Primary Datasets (Recommended)

1. **Disease Symptom Description Dataset**
   - Kaggle: https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
   - Size: ~5,000 records
   - Format: CSV
   - Content: Disease, Symptom, Description

2. **Symptom2Disease Dataset**
   - Kaggle: https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
   - Size: ~1,200 records
   - Format: CSV/JSON
   - Content: Symptoms → Disease

3. **Disease Prediction ML Dataset**
   - Kaggle: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
   - Size: ~5,000 records
   - Format: CSV
   - Content: Binary symptom features, Disease

4. **Medical Symptoms Dataset**
   - Kaggle: https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms
   - Size: ~3,000 records
   - Format: CSV
   - Content: Comprehensive symptom lists

### Alternative Datasets

If primary datasets are unavailable:

5. **Alternative Disease Symptom Dataset**
   - Kaggle: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset
   - Size: ~5,000 records

---

## 🔧 Troubleshooting

### Issue: Kaggle API Authentication Failed

**Solution:**
1. Verify `kaggle.json` is in correct location
2. Check file permissions (should be 600)
3. Verify JSON file is valid (no extra commas, brackets)

### Issue: Dataset Format Not Recognized

**Solution:**
1. Manually inspect dataset structure
2. Modify normalization script for specific dataset
3. Or skip problematic datasets

### Issue: Memory Errors During Processing

**Solution:**
1. Process datasets one at a time
2. Use chunking for large files
3. Increase system RAM
4. Close other applications

### Issue: Datasets Not Found

**Solution:**
1. Download manually from Kaggle
2. Extract to `datasets/raw/{dataset_name}/`
3. Then run normalization and merge scripts

---

## 📁 File Structure

```
project/
├── datasets/
│   ├── raw/                    # Downloaded datasets (raw)
│   │   ├── disease_symptom_description/
│   │   ├── symptom2disease/
│   │   └── ...
│   └── processed/              # Normalized datasets
│       ├── normalized_datasets.xlsx
│       └── normalization_stats.json
├── data/
│   ├── processed/
│   │   ├── dataset_cleaned.xlsx          # Original cleaned
│   │   ├── dataset_expanded_final.xlsx   # Final merged (NEW)
│   │   └── expanded_dataset_stats.json
│   └── scripts/
│       ├── download_kaggle_datasets.py
│       ├── normalize_datasets.py
│       └── merge_datasets.py
└── ml_models/
    └── scripts/
        └── feature_engineering.py  # Updated to use expanded dataset
```

---

## ✅ Checklist

- [ ] Install Kaggle API
- [ ] Set up Kaggle credentials
- [ ] Download datasets
- [ ] Normalize datasets
- [ ] Merge datasets
- [ ] Verify expanded dataset quality
- [ ] Run feature engineering
- [ ] Retrain XGBoost model
- [ ] Retrain Random Forest model
- [ ] Compare accuracy improvements
- [ ] Update backend to use improved models

---

## 📈 Expected Timeline

- **Download datasets**: 10-30 minutes (depends on internet speed)
- **Normalize datasets**: 5-15 minutes
- **Merge datasets**: 2-5 minutes
- **Feature engineering**: 10-30 minutes (depends on dataset size)
- **Train models**: 30-60 minutes (XGBoost + Random Forest)

**Total time: 1-2 hours**

---

## 🎯 Success Criteria

After completing all steps:

✅ Expanded dataset has 10,000+ records  
✅ Dataset quality is validated (80%+ completeness)  
✅ Models are retrained with expanded data  
✅ Accuracy improved to 60-80%  
✅ Precision improved to 90%+  

---

## 💡 Tips

1. **Start with one dataset** - Test the pipeline with one dataset first
2. **Validate at each step** - Check outputs before proceeding
3. **Keep backups** - Save original datasets
4. **Monitor progress** - Check statistics files for validation
5. **Be patient** - Large datasets take time to process

---

## 📝 Notes

- All scripts include comprehensive error handling
- Progress is shown during execution
- Statistics are saved for validation
- Original datasets are preserved (not modified)
- Feature engineering automatically uses expanded dataset if available

---

**Last Updated**: December 2024

**Next Steps**: Run through the workflow and compare model improvements!

