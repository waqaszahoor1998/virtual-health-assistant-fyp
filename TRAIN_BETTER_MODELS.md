# 🚀 Train Better Models - Improve Accuracy

## 🎯 Goal: Boost Accuracy from 30% to 60-80%+

Current models (XGBoost: 30%, Random Forest: 9%) are too low. Let's train better models!

---

## 📋 Available Better Models

### 1. Neural Network (Deep Learning) ⭐ HIGHEST PRIORITY

**Expected Accuracy**: 50-70%  
**Why**: Best for complex multi-label classification

**Install & Train:**
```bash
# Install TensorFlow
pip install tensorflow

# Train model
cd ml_models/scripts
python train_neural_network.py
```

**Time**: 15-30 minutes

---

### 2. LightGBM ⭐ HIGH PRIORITY

**Expected Accuracy**: 40-60%  
**Why**: Often outperforms XGBoost, faster training

**Install & Train:**
```bash
# Install LightGBM
pip install lightgbm

# Train model
cd ml_models/scripts
python train_lightgbm.py
```

**Time**: 5-15 minutes

---

### 3. CatBoost ⭐ HIGH PRIORITY

**Expected Accuracy**: 45-65%  
**Why**: Excellent for categorical features and imbalanced data

**Install & Train:**
```bash
# Install CatBoost
pip install catboost

# Train model
cd ml_models/scripts
python train_catboost.py
```

**Time**: 10-20 minutes

---

### 4. Ensemble Model ⭐ RECOMMENDED

**Expected Accuracy**: 45-65% (5-10% boost)  
**Why**: Combines strengths of all models

**Train:**
```bash
# First train at least 2 individual models, then:
cd ml_models/scripts
python train_ensemble.py
```

**Time**: 5-10 minutes (after individual models trained)

---

## 🚀 Quick Start - Train All Better Models

### Step 1: Install Dependencies

```bash
pip install lightgbm catboost tensorflow
```

### Step 2: Train Models (Recommended Order)

```bash
cd ml_models/scripts

# 1. LightGBM (fastest, good improvement)
python train_lightgbm.py

# 2. CatBoost (good for our data)
python train_catboost.py

# 3. Neural Network (best accuracy, takes longer)
python train_neural_network.py

# 4. Ensemble (combines all)
python train_ensemble.py
```

---

## 📊 Expected Results

| Model | Current | Expected | Improvement |
|-------|---------|----------|-------------|
| **XGBoost** | 30.33% | 30.33% | Baseline |
| **LightGBM** | - | **40-60%** | +10-30% |
| **CatBoost** | - | **45-65%** | +15-35% |
| **Neural Network** | - | **50-70%** | +20-40% |
| **Ensemble** | - | **45-65%** | +15-35% |

---

## 💡 Recommendation

**Train in this order:**

1. **LightGBM** (quick win, 30 min)
2. **Neural Network** (best accuracy, 30 min)
3. **Ensemble** (combine all, 10 min)

**Expected outcome**: Accuracy should improve to **50-70%**!

---

## ⚡ Fast Track (Just Best Models)

If you want fastest improvement:

```bash
# Install
pip install lightgbm tensorflow

# Train
cd ml_models/scripts
python train_lightgbm.py      # Fast, good improvement
python train_neural_network.py # Best accuracy
python train_ensemble.py       # Combine both
```

**Expected**: 50-65% accuracy in ~1 hour

---

## 📝 Notes

- All models use the same expanded dataset (2,272 training samples)
- Models will be saved in `ml_models/models/`
- Ensemble combines all available trained models
- You can train models individually or all at once

---

**Let's improve that accuracy!** 🚀

