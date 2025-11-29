# Dataset Improvement Plan - Enhance ML Model Accuracy

## 🎯 Goal

**Current**: 753 training samples → 7-8% accuracy, 85% precision  
**Target**: 11,000+ training samples → 60-80% accuracy, 90%+ precision

---

## 📊 Current Dataset Status

### Current Dataset:
- **File**: `data/raw/dataset 2 final.xlsx`
- **Total Records**: 3,963
- **Valid Records**: 1,077 (27.2% after cleaning)
- **Training Samples**: 753
- **Diseases**: 1,508 unique diseases
- **Problem**: Less than 0.5 samples per disease!

---

## 📥 Recommended Additional Datasets

### 1. Disease Symptom Dataset (Kaggle) ⭐ PRIMARY
- **Link**: https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
- **Size**: ~5,000+ records
- **Format**: CSV
- **Columns**: Disease, Symptom, Description
- **Status**: ✅ Recommended for immediate download

### 2. Symptom2Disease Dataset (Kaggle)
- **Link**: https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
- **Size**: ~1,200+ records
- **Format**: CSV/JSON
- **Columns**: Symptoms, Disease
- **Status**: ✅ Recommended

### 3. Disease Prediction Dataset (Kaggle)
- **Link**: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
- **Size**: ~5,000+ records
- **Format**: CSV
- **Columns**: Symptoms (binary), Disease
- **Status**: ✅ Recommended

### 4. Medical Symptoms Dataset (Kaggle)
- **Link**: https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms
- **Size**: ~3,000+ records
- **Format**: CSV
- **Status**: ✅ Recommended

### 5. Disease Prediction from Symptoms (Kaggle)
- **Link**: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset
- **Size**: ~5,000+ records
- **Status**: ✅ Alternative option

### 6. Symptom-Disease Mapping Dataset
- **Link**: Various Kaggle datasets
- **Total Expected**: 10,000-15,000 records combined

---

## 🔧 Implementation Plan

### Phase 1: Dataset Discovery & Download ✅

**Step 1.1**: Install Kaggle API
```bash
pip install kaggle
```

**Step 1.2**: Set up Kaggle credentials
- Download `kaggle.json` from Kaggle account settings
- Place in `~/.kaggle/kaggle.json`
- Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

**Step 1.3**: Create download script

### Phase 2: Dataset Processing & Normalization ✅

**Step 2.1**: Normalize symptom names across datasets
**Step 2.2**: Standardize disease names
**Step 2.3**: Merge datasets
**Step 2.4**: Remove duplicates
**Step 2.5**: Quality validation

### Phase 3: Retraining Models ✅

**Step 3.1**: Run feature engineering on expanded dataset
**Step 3.2**: Retrain XGBoost model
**Step 3.3**: Retrain Random Forest model
**Step 3.4**: Compare old vs new performance

---

## 📈 Expected Improvements

### Current Performance:
- Training Samples: 753
- Exact Match Accuracy: 7-8%
- Precision: 85-87%

### With Expanded Dataset (11,000+ samples):
- Training Samples: 11,000+
- Expected Accuracy: **60-80%**
- Expected Precision: **90-95%**
- Better disease coverage
- More robust predictions

---

## 🚀 Next Steps

1. Create dataset download script
2. Create dataset normalization script
3. Create dataset merging script
4. Download and process datasets
5. Retrain models with expanded data

---

## 📝 Files to Create

1. `data/scripts/download_kaggle_datasets.py` - Automated download
2. `data/scripts/normalize_datasets.py` - Standardize formats
3. `data/scripts/merge_datasets.py` - Combine all datasets
4. `data/scripts/validate_expanded_dataset.py` - Quality checks

---

**Let's start building the dataset improvement pipeline!**

