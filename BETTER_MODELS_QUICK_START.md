# 🚀 Better Models Quick Start Guide

## Goal: Improve Accuracy from 30% to 60-80%+

---

## ⚡ Fastest Way (Recommended)

### Step 1: Install New ML Libraries

```bash
cd /Users/m.w.zahoor/Desktop/rehan

# Activate virtual environment (if using one)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install new ML libraries
pip install lightgbm catboost tensorflow
```

### Step 2: Train Better Models

```bash
cd ml_models/scripts

# Option A: Train all models (best results)
python train_lightgbm.py
python train_catboost.py
python train_neural_network.py
python train_ensemble.py

# Option B: Just fastest improvement (recommended)
python train_lightgbm.py      # ~10 min, good improvement
python train_neural_network.py # ~20 min, best accuracy
python train_ensemble.py       # ~5 min, combines all
```

---

## 📊 What to Expect

### Current Performance:
- XGBoost: 30.33% accuracy
- Random Forest: 8.61% accuracy

### Expected After Training:
- LightGBM: **40-60%** accuracy (+10-30%)
- CatBoost: **45-65%** accuracy (+15-35%)
- Neural Network: **50-70%** accuracy (+20-40%)
- Ensemble: **45-65%** accuracy (+15-35%)

---

## 🎯 Recommended Approach

**Start with LightGBM** (fastest improvement):
```bash
pip install lightgbm
python ml_models/scripts/train_lightgbm.py
```

**Then Neural Network** (best accuracy):
```bash
pip install tensorflow
python ml_models/scripts/train_neural_network.py
```

**Finally Ensemble** (combines all):
```bash
python ml_models/scripts/train_ensemble.py
```

---

## ⏱️ Time Estimate

- **LightGBM**: 10-15 minutes
- **Neural Network**: 20-30 minutes
- **CatBoost**: 15-20 minutes
- **Ensemble**: 5-10 minutes

**Total**: ~1-1.5 hours for all models

---

## 📝 Notes

- All models use your expanded dataset (2,272 training samples)
- Models saved in `ml_models/models/`
- You can train them one at a time or all together
- Ensemble combines all available trained models

---

**Ready to improve accuracy!** Start with Step 1 above. 🚀

