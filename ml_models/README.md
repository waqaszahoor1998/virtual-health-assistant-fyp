# ML Models - Training and Usage Guide

## 📋 Overview

This directory contains scripts and trained models for disease prediction from symptoms.

**Recommended Models:**
- **XGBoost** ⭐ (Primary - Expected 75-85% accuracy)
- **Random Forest** (Baseline comparison - Expected 70-75% accuracy)

## 🚀 Quick Start

### Step 1: Prepare Data

First, clean and normalize the symptom data:

```bash
# Navigate to data scripts
cd data/scripts

# Run symptom cleaning script
python clean_symptoms.py
```

This creates:
- `data/processed/dataset_cleaned.xlsx` - Cleaned dataset
- `data/processed/symptom_disease_mapping.csv` - Symptom-disease mappings

### Step 2: Feature Engineering

Prepare data for ML training:

```bash
# Navigate to ML scripts
cd ml_models/scripts

# Run feature engineering
python feature_engineering.py
```

This creates:
- `ml_models/models/X_train.pkl` - Training features
- `ml_models/models/y_train.pkl` - Training labels
- `ml_models/models/symptom_vectorizer.pkl` - TF-IDF vectorizer
- `ml_models/models/disease_encoder.pkl` - Disease encoder

### Step 3: Train Models

Train XGBoost (recommended):

```bash
python train_xgboost.py
```

Train Random Forest (for comparison):

```bash
python train_random_forest.py
```

### Step 4: Models Ready!

Trained models are saved in `ml_models/models/`:
- `xgboost_model.pkl` - Trained XGBoost model
- `random_forest_model.pkl` - Trained Random Forest model
- Model metrics and info files

---

## 📁 Directory Structure

```
ml_models/
├── scripts/
│   ├── analyze_data.py          # Data analysis script
│   ├── clean_symptoms.py        # Symptom cleaning (in data/scripts)
│   ├── feature_engineering.py   # Feature engineering for ML
│   ├── train_xgboost.py         # Train XGBoost model
│   └── train_random_forest.py   # Train Random Forest model
├── models/                      # Trained models (generated)
│   ├── xgboost_model.pkl
│   ├── random_forest_model.pkl
│   ├── symptom_vectorizer.pkl
│   ├── disease_encoder.pkl
│   └── ...
└── training/                    # Training artifacts
```

---

## 🔧 Script Details

### 1. Feature Engineering (`feature_engineering.py`)

**What it does:**
- Converts symptoms to TF-IDF feature vectors
- Creates disease label encodings
- Splits data into train/validation/test sets (70%/15%/15%)
- Saves preprocessed data for training

**Outputs:**
- Feature matrices (X_train, X_val, X_test)
- Label matrices (y_train, y_val, y_test)
- Vectorizer and encoder objects

### 2. Train XGBoost (`train_xgboost.py`)

**What it does:**
- Trains XGBoost model on preprocessed data
- Uses early stopping on validation set
- Evaluates on test set
- Saves trained model and metrics

**Parameters:**
- n_estimators: 200
- max_depth: 6
- learning_rate: 0.1
- Uses multi-class classification

**Expected Performance:**
- Accuracy: 75-85%
- Fast training time

### 3. Train Random Forest (`train_random_forest.py`)

**What it does:**
- Trains Random Forest model
- Evaluates performance
- Shows feature importance
- Saves trained model

**Parameters:**
- n_estimators: 200
- max_depth: 15
- Provides feature importance insights

**Expected Performance:**
- Accuracy: 70-75%
- Good for baseline comparison

---

## 📊 Model Usage in Backend

The trained models are automatically loaded and used by the backend API:

```python
from app.utils.ml_service import get_ml_service

# Get ML service
ml_service = get_ml_service()

# Predict diseases from symptoms
predictions = ml_service.predict_diseases(
    symptoms=['fever', 'headache', 'nausea'],
    model_type='xgboost',
    top_k=5
)
```

---

## 🧪 Testing Models

### Test Prediction Manually:

```python
from app.utils.ml_service import get_ml_service

ml_service = get_ml_service()
ml_service.load_models()

# Test prediction
result = ml_service.predict_diseases(
    symptoms=['fever', 'cough', 'shortness of breath'],
    top_k=3
)

print(result)
```

### API Testing:

```bash
# Start backend server
cd backend
python run.py

# Test prediction endpoint (requires JWT token)
curl -X POST http://localhost:5000/api/diagnosis/predict \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "headache", "nausea"],
    "model_type": "xgboost",
    "top_k": 5
  }'
```

---

## 📈 Model Evaluation Metrics

Models are evaluated using:
- **Accuracy**: Exact match accuracy (all labels correct)
- **Precision (Macro)**: Average precision across all diseases
- **Recall (Macro)**: Average recall across all diseases
- **F1-Score (Macro)**: Harmonic mean of precision and recall
- **Micro-Averaged Metrics**: Overall performance across all predictions

---

## 🔄 Retraining Models

To retrain models with new data:

1. Update dataset in `data/raw/`
2. Run data cleaning: `python data/scripts/clean_symptoms.py`
3. Run feature engineering: `python ml_models/scripts/feature_engineering.py`
4. Retrain models: `python ml_models/scripts/train_xgboost.py`

---

## 🐛 Troubleshooting

### Models Not Found Error

**Error**: "ML models not available"

**Solution:**
```bash
# Ensure you've completed all steps:
# 1. Clean data
cd data/scripts
python clean_symptoms.py

# 2. Feature engineering
cd ml_models/scripts
python feature_engineering.py

# 3. Train models
python train_xgboost.py
```

### Out of Memory Error

**Solution:**
- Reduce `max_features` in feature_engineering.py
- Use smaller n_estimators in training scripts
- Process data in batches

### Low Accuracy

**Solutions:**
- Add more training data (see DATASET_RECOMMENDATIONS.md)
- Tune hyperparameters
- Try ensemble methods
- Check data quality

---

## 📚 Additional Resources

- ML Model Recommendations: `../ML_MODELS_RECOMMENDATION.md`
- Dataset Recommendations: `../DATASET_RECOMMENDATIONS.md`
- XGBoost Documentation: https://xgboost.readthedocs.io/
- Scikit-learn Documentation: https://scikit-learn.org/

---

## ✅ Next Steps

After training models:

1. **Integrate with Backend**: Models are automatically loaded by `ml_service.py`
2. **Test Predictions**: Use `/api/diagnosis/predict` endpoint
3. **Monitor Performance**: Track prediction accuracy in production
4. **Iterate**: Retrain with more data to improve accuracy

---

**Status**: Ready for training once data preprocessing is complete!

