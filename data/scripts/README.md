# Dataset Improvement Scripts

Scripts for downloading, normalizing, and merging additional datasets to improve ML model accuracy.

## 📋 Overview

These scripts help expand the training dataset from **753 samples** to **10,000+ samples**, which should improve model accuracy from **7-8%** to **60-80%**.

---

## 🚀 Quick Start

### Step 1: Download Datasets

```bash
# Install Kaggle API
pip install kaggle

# Set up Kaggle credentials
# 1. Go to https://www.kaggle.com/settings
# 2. Create API token
# 3. Save kaggle.json to ~/.kaggle/
# 4. Run: chmod 600 ~/.kaggle/kaggle.json

# Run download script
python data/scripts/download_kaggle_datasets.py
```

### Step 2: Normalize Datasets

```bash
# Normalize all downloaded datasets to common format
python data/scripts/normalize_datasets.py
```

### Step 3: Merge Datasets

```bash
# Merge all normalized datasets into final training dataset
python data/scripts/merge_datasets.py
```

### Step 4: Retrain Models

```bash
# Run feature engineering with expanded dataset
cd ml_models/scripts
python feature_engineering.py

# Train XGBoost model
python train_xgboost.py

# Train Random Forest model
python train_random_forest.py
```

---

## 📁 Scripts

### 1. `download_kaggle_datasets.py`

Downloads recommended datasets from Kaggle.

**What it does:**
- Downloads 4+ datasets from Kaggle
- Extracts zip files automatically
- Organizes files in `datasets/raw/` directory

**Required:**
- Kaggle account (free)
- Kaggle API token (`kaggle.json`)

**Output:**
- Datasets in `datasets/raw/{dataset_name}/`

---

### 2. `normalize_datasets.py`

Normalizes all datasets to a common format.

**What it does:**
- Standardizes symptom names across datasets
- Standardizes disease names
- Handles different file formats (CSV, Excel, JSON)
- Removes duplicates
- Creates unified format

**Output:**
- `datasets/processed/normalized_datasets.xlsx`
- `datasets/processed/normalized_datasets.csv`
- `datasets/processed/normalization_stats.json`

---

### 3. `merge_datasets.py`

Merges normalized datasets with existing cleaned dataset.

**What it does:**
- Combines all normalized datasets
- Merges with existing cleaned dataset
- Groups by disease and combines symptoms
- Validates data quality
- Creates final training-ready dataset

**Output:**
- `data/processed/dataset_expanded_final.xlsx`
- `data/processed/dataset_expanded_final.csv`
- `data/processed/expanded_dataset_stats.json`

---

## 📊 Expected Results

### Before:
- **Training samples**: 753
- **Diseases**: 1,508
- **Accuracy**: 7-8%
- **Precision**: 85-87%

### After:
- **Training samples**: 10,000-15,000
- **Diseases**: 1,500+
- **Expected Accuracy**: 60-80%
- **Expected Precision**: 90-95%

---

## 🔧 Manual Dataset Download (Alternative)

If Kaggle API doesn't work, download datasets manually:

1. Visit Kaggle datasets:
   - https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
   - https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
   - https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
   - https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms

2. Download and extract to `datasets/raw/{dataset_name}/`

3. Then run normalization and merge scripts

---

## ⚠️ Troubleshooting

### Kaggle API Issues

**Error: "Kaggle credentials not found"**
- Download `kaggle.json` from Kaggle settings
- Place in `~/.kaggle/kaggle.json`
- Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

**Error: "Permission denied"**
- Run: `chmod 600 ~/.kaggle/kaggle.json`

### Dataset Format Issues

If a dataset has unexpected format:
1. Check the dataset structure manually
2. Modify normalization script for that specific dataset
3. Or skip that dataset and use others

### Memory Issues

If scripts run out of memory:
- Process datasets one at a time
- Use chunking for large files
- Increase system memory

---

## 📝 Notes

- All scripts include comprehensive error handling
- Progress is shown during execution
- Statistics are saved for validation
- Original datasets are preserved (not modified)

---

## 🔄 Next Steps

After merging datasets:

1. ✅ Verify expanded dataset quality
2. ✅ Update feature engineering to use expanded dataset
3. ✅ Retrain ML models
4. ✅ Compare old vs new accuracy
5. ✅ Update backend to use improved models

---

**Last Updated**: December 2024

