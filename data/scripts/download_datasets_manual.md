# Manual Dataset Download Guide

Since Kaggle API requires authentication, here's how to download datasets manually:

## 📥 Quick Download Links

### 1. Disease Symptom Description Dataset ⭐ PRIMARY
- **Direct Link**: https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
- **Download**: Click "Download" button (requires Kaggle account login)
- **Save to**: `datasets/raw/disease_symptom_description/`

### 2. Symptom2Disease Dataset
- **Direct Link**: https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
- **Download**: Click "Download" button
- **Save to**: `datasets/raw/symptom2disease/`

### 3. Disease Prediction Using ML
- **Direct Link**: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
- **Download**: Click "Download" button
- **Save to**: `datasets/raw/disease_prediction_ml/`

### 4. Medical Symptoms Dataset
- **Direct Link**: https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms
- **Download**: Click "Download" button
- **Save to**: `datasets/raw/medical_symptoms/`

---

## 📋 Step-by-Step Instructions

### Step 1: Create Directory Structure

```bash
cd /Users/m.w.zahoor/Desktop/rehan
mkdir -p datasets/raw/disease_symptom_description
mkdir -p datasets/raw/symptom2disease
mkdir -p datasets/raw/disease_prediction_ml
mkdir -p datasets/raw/medical_symptoms
```

### Step 2: Download from Kaggle

1. Visit each dataset link above
2. Sign in to Kaggle (or create free account)
3. Click the "Download" button
4. Extract the ZIP file
5. Move CSV/Excel files to the appropriate directory

### Step 3: Verify Downloads

After downloading, your structure should look like:
```
datasets/raw/
├── disease_symptom_description/
│   └── *.csv (or *.xlsx)
├── symptom2disease/
│   └── *.csv
├── disease_prediction_ml/
│   └── *.csv
└── medical_symptoms/
    └── *.csv
```

### Step 4: Continue with Normalization

Once files are in place:

```bash
python data/scripts/normalize_datasets.py
python data/scripts/merge_datasets.py
```

---

## 🔄 Alternative: Use Python requests (if you have direct links)

I can create a script that downloads from direct download links if you provide them, but Kaggle requires authentication for downloads.

---

## 💡 Tip

If you have Kaggle account:
1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New API Token"
4. Download `kaggle.json`
5. Place in `~/.kaggle/kaggle.json`
6. Then run: `python data/scripts/download_kaggle_datasets.py`

---

**Note**: Manual download is perfectly fine and works the same way!

