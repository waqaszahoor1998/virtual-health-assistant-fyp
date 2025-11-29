# Quick Download Guide - Kaggle Datasets

## ❗ Important: Kaggle Requires Authentication

I **cannot download datasets directly** because Kaggle requires:
- Your personal Kaggle account
- Your API credentials (kaggle.json file)

**But I've made it super easy!** Just follow these steps:

---

## 🚀 Option 1: Automatic Download (Recommended)

### Step 1: Get Kaggle API Token

1. Go to **https://www.kaggle.com/**
2. Sign in (or create free account)
3. Go to **https://www.kaggle.com/settings**
4. Scroll to **"API"** section
5. Click **"Create New API Token"**
6. This downloads `kaggle.json` file

### Step 2: Set Up Credentials

**macOS/Linux:**
```bash
# Create directory
mkdir -p ~/.kaggle

# Move kaggle.json file (or copy it)
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json

# Set permissions (required!)
chmod 600 ~/.kaggle/kaggle.json
```

**Windows (Command Prompt):**
```cmd
# Create directory
mkdir %USERPROFILE%\.kaggle

# Move kaggle.json file
move %USERPROFILE%\Downloads\kaggle.json %USERPROFILE%\.kaggle\kaggle.json
```

**Windows (PowerShell):**
```powershell
# Create directory
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.kaggle

# Move kaggle.json file
Move-Item $env:USERPROFILE\Downloads\kaggle.json $env:USERPROFILE\.kaggle\kaggle.json
```

### Step 3: Download Datasets Automatically

```bash
python data/scripts/download_datasets_simple.py
```

That's it! The script will download all 4 datasets automatically.

---

## 📥 Option 2: Manual Download (If API Doesn't Work)

### Step 1: Create Directory Structure

```bash
mkdir -p datasets/raw/disease_symptom_description
mkdir -p datasets/raw/symptom2disease
mkdir -p datasets/raw/disease_prediction_ml
mkdir -p datasets/raw/medical_symptoms
```

### Step 2: Download Each Dataset

1. **Disease Symptom Description** (~5,000 records)
   - URL: https://www.kaggle.com/datasets/kaushil268/disease-symptom-description-dataset
   - Download ZIP
   - Extract to: `datasets/raw/disease_symptom_description/`

2. **Symptom2Disease** (~1,200 records)
   - URL: https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
   - Download ZIP
   - Extract to: `datasets/raw/symptom2disease/`

3. **Disease Prediction ML** (~5,000 records)
   - URL: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
   - Download ZIP
   - Extract to: `datasets/raw/disease_prediction_ml/`

4. **Medical Symptoms** (~3,000 records)
   - URL: https://www.kaggle.com/datasets/rabieelkharoua/medical-symptoms
   - Download ZIP
   - Extract to: `datasets/raw/medical_symptoms/`

### Step 3: Continue with Normalization

```bash
python data/scripts/normalize_datasets.py
python data/scripts/merge_datasets.py
```

---

## ✅ After Download (Either Method)

Once datasets are downloaded, continue with:

```bash
# Normalize datasets
python data/scripts/normalize_datasets.py

# Merge datasets
python data/scripts/merge_datasets.py

# Retrain models with expanded dataset
cd ml_models/scripts
python feature_engineering.py
python train_xgboost.py
python train_random_forest.py
```

---

## 🔍 Verify Setup

Check if Kaggle is ready:

```bash
# Check if Kaggle API is installed
pip list | grep kaggle

# Check if credentials exist
ls ~/.kaggle/kaggle.json  # macOS/Linux
dir %USERPROFILE%\.kaggle\kaggle.json  # Windows
```

---

## 💡 Why Can't I Download Directly?

Kaggle protects datasets and requires:
- ✅ **Authentication** (your Kaggle account)
- ✅ **API token** (unique to your account)
- ✅ **Terms of service** (you must agree to usage terms)

This is normal and expected for data platforms.

---

## 🎯 Summary

1. **Get Kaggle API token** (5 minutes)
2. **Set up credentials** (2 minutes)
3. **Run download script** (10-30 minutes)
4. **Done!** Ready to normalize and merge

**Total time: ~15-40 minutes** (depending on download speed)

---

**Need help?** Check `DATASET_IMPROVEMENT_GUIDE.md` for detailed instructions.

