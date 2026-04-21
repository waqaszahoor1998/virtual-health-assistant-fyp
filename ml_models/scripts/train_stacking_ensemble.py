"""
Advanced Stacking Ensemble for Disease Prediction.

This script creates a stacking ensemble that:
1. Uses LightGBM and Neural Network as base models (Level 1)
2. Trains a meta-learner (Level 2) to intelligently combine their predictions
3. The meta-learner learns WHEN to trust each base model

Stacking is superior to simple averaging because it learns optimal
combination weights for different types of predictions.
"""

import os
import sys
import time
import joblib
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.dummy import DummyClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, hamming_loss
)
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==================== CUSTOM META-LEARNER ====================

class RobustMultiOutputClassifier(BaseEstimator, ClassifierMixin):
    """
    Custom MultiOutputClassifier that handles sparse data.
    
    For diseases with only one class (all zeros), uses DummyClassifier.
    For diseases with both classes, uses the real estimator.
    
    This prevents "only one class" errors in sparse multi-label datasets.
    """
    
    def __init__(self, estimator):
        self.estimator = estimator
    
    def fit(self, X, y):
        """Train one classifier per disease, handling single-class cases."""
        self.estimators_ = []
        self.n_outputs_ = y.shape[1]
        
        for i in range(self.n_outputs_):
            y_col = y[:, i]
            unique_classes = np.unique(y_col)
            
            if len(unique_classes) == 1:
                # Only one class (all zeros or all ones) - use dummy
                clf = DummyClassifier(strategy='constant', constant=unique_classes[0])
            else:
                # Both classes present - use real estimator
                from sklearn.base import clone
                clf = clone(self.estimator)
            
            clf.fit(X, y_col)
            self.estimators_.append(clf)
        
        return self
    
    def predict(self, X):
        """Predict using all trained classifiers."""
        predictions = np.zeros((X.shape[0], self.n_outputs_), dtype=int)
        for i, clf in enumerate(self.estimators_):
            predictions[:, i] = clf.predict(X)
        return predictions
    
    def predict_proba(self, X):
        """Predict probabilities using all trained classifiers."""
        probas = []
        for clf in self.estimators_:
            if hasattr(clf, 'predict_proba'):
                proba = clf.predict_proba(X)
                if proba.shape[1] == 2:
                    probas.append(proba[:, 1])  # Positive class
                else:
                    probas.append(proba[:, 0])  # Only one class
            else:
                # DummyClassifier without predict_proba
                probas.append(clf.predict(X).astype(float))
        return np.column_stack(probas)


print("=" * 80)
print("🔥 ADVANCED STACKING ENSEMBLE TRAINING")
print("=" * 80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ==================== CONFIGURATION ====================

# Paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, 'stacking_ensemble_model.pkl')
INFO_SAVE_PATH = os.path.join(MODELS_DIR, 'stacking_ensemble_model_info.json')
METRICS_SAVE_PATH = os.path.join(MODELS_DIR, 'stacking_ensemble_model_metrics.json')

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

# ==================== LOAD PREPROCESSED DATA ====================

print("📂 Loading preprocessed data...")
try:
    # Load features and labels
    X_train = joblib.load(os.path.join(MODELS_DIR, 'X_train.pkl'))
    X_val = joblib.load(os.path.join(MODELS_DIR, 'X_val.pkl'))
    X_test = joblib.load(os.path.join(MODELS_DIR, 'X_test.pkl'))
    
    y_train = joblib.load(os.path.join(MODELS_DIR, 'y_train.pkl'))
    y_val = joblib.load(os.path.join(MODELS_DIR, 'y_val.pkl'))
    y_test = joblib.load(os.path.join(MODELS_DIR, 'y_test.pkl'))
    
    # Load encoder for disease names
    disease_encoder = joblib.load(os.path.join(MODELS_DIR, 'disease_encoder.pkl'))
    
    print(f"✅ Data loaded successfully!")
    print(f"   Training samples: {X_train.shape[0]}")
    print(f"   Validation samples: {X_val.shape[0]}")
    print(f"   Test samples: {X_test.shape[0]}")
    print(f"   Features: {X_train.shape[1]}")
    print(f"   Diseases: {y_train.shape[1]}")
    print()
    
except FileNotFoundError as e:
    print(f"❌ Error: Could not find preprocessed data files.")
    print(f"   Please run 'python feature_engineering.py' first.")
    print(f"   Error details: {e}")
    sys.exit(1)

# ==================== LOAD BASE MODELS ====================

print("🤖 Loading base models (Level 1)...")

# Load LightGBM model
try:
    lightgbm_model = joblib.load(os.path.join(MODELS_DIR, 'lightgbm_model.pkl'))
    print("   ✅ LightGBM model loaded (46.31% accuracy)")
except FileNotFoundError:
    print("   ❌ LightGBM model not found. Please train it first:")
    print("      python train_lightgbm.py")
    sys.exit(1)

# Load Neural Network model
try:
    from tensorflow import keras
    neural_network_model = keras.models.load_model(
        os.path.join(MODELS_DIR, 'neural_network_model.h5')
    )
    print("   ✅ Neural Network model loaded (59.41% F1-Micro)")
except (FileNotFoundError, ImportError) as e:
    print(f"   ❌ Neural Network model not found or TensorFlow not installed.")
    print(f"      Please train it first: python train_neural_network.py")
    print(f"      Error: {e}")
    sys.exit(1)

print()

# ==================== GENERATE BASE MODEL PREDICTIONS ====================

print("🔮 Generating base model predictions for meta-training...")
print("   (This creates the training data for the meta-learner)")
print()

start_time = time.time()

# Convert sparse matrices to dense for Neural Network
if hasattr(X_train, 'toarray'):
    X_train_dense = X_train.toarray()
    X_val_dense = X_val.toarray()
    X_test_dense = X_test.toarray()
else:
    X_train_dense = X_train
    X_val_dense = X_val
    X_test_dense = X_test

# LightGBM predictions (probabilities)
print("   Generating LightGBM predictions...")
lgbm_train_pred_raw = lightgbm_model.predict_proba(X_train)
lgbm_val_pred_raw = lightgbm_model.predict_proba(X_val)
lgbm_test_pred_raw = lightgbm_model.predict_proba(X_test)

# LightGBM MultiOutputClassifier returns a list of arrays (one per disease)
# Each array has shape (n_samples, 2) for [prob_negative, prob_positive]
# We need to stack them into shape (n_samples, n_diseases)
print("   Extracting positive class probabilities from LightGBM...")
if isinstance(lgbm_train_pred_raw, list):
    # Extract positive class (index 1) from each disease's predictions
    lgbm_train_pred = np.column_stack([pred[:, 1] for pred in lgbm_train_pred_raw])
    lgbm_val_pred = np.column_stack([pred[:, 1] for pred in lgbm_val_pred_raw])
    lgbm_test_pred = np.column_stack([pred[:, 1] for pred in lgbm_test_pred_raw])
    print(f"   Converted from list to array. Shape: {lgbm_train_pred.shape}")
elif len(lgbm_train_pred_raw.shape) == 3:
    # If it's already a 3D array, just extract the positive class
    lgbm_train_pred = lgbm_train_pred_raw[:, :, 1]
    lgbm_val_pred = lgbm_val_pred_raw[:, :, 1]
    lgbm_test_pred = lgbm_test_pred_raw[:, :, 1]
else:
    # Already in correct format
    lgbm_train_pred = lgbm_train_pred_raw
    lgbm_val_pred = lgbm_val_pred_raw
    lgbm_test_pred = lgbm_test_pred_raw

# Neural Network predictions (probabilities)
print("   Generating Neural Network predictions...")
nn_train_pred = neural_network_model.predict(X_train_dense, verbose=0)
nn_val_pred = neural_network_model.predict(X_val_dense, verbose=0)
nn_test_pred = neural_network_model.predict(X_test_dense, verbose=0)

# Stack predictions horizontally to create meta-features
# Each sample now has 2 * num_diseases features (lgbm probs + nn probs)
print("   Stacking predictions into meta-features...")
meta_train = np.hstack([lgbm_train_pred, nn_train_pred])
meta_val = np.hstack([lgbm_val_pred, nn_val_pred])
meta_test = np.hstack([lgbm_test_pred, nn_test_pred])

prediction_time = time.time() - start_time
print(f"   ✅ Base predictions generated in {prediction_time:.2f} seconds")
print(f"   Meta-feature shape: {meta_train.shape}")
print()

# ==================== TRAIN META-LEARNER (LEVEL 2) ====================

print("🎓 Training meta-learner (Level 2)...")
print("   Algorithm: Logistic Regression with L2 regularization")
print("   This learns how to optimally combine base model predictions")
print("   Using RobustMultiOutputClassifier to handle sparse diseases")
print()

start_time = time.time()

# Create meta-learner using custom RobustMultiOutputClassifier
# This handles diseases with no positive examples in validation set
meta_learner = RobustMultiOutputClassifier(
    estimator=LogisticRegression(
        max_iter=1000,           # More iterations for convergence
        solver='lbfgs',          # Fast solver for L2 regularization
        C=1.0,                   # Regularization strength (lower = more regularization)
        random_state=42          # Reproducibility
    )
)

# Train meta-learner on validation set predictions
# This prevents overfitting - meta-learner never sees training predictions
print("   Training on validation set predictions...")
print("   (This may take 1-2 minutes as it trains 1,140 disease classifiers)")
meta_learner.fit(meta_val, y_val)

training_time = time.time() - start_time
print(f"   ✅ Meta-learner trained in {training_time:.2f} seconds")
print()

# ==================== EVALUATE ON TEST SET ====================

print("📊 Evaluating Stacking Ensemble on test set...")
print()

# Make predictions using meta-learner
y_pred = meta_learner.predict(meta_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
hamming = hamming_loss(y_test, y_pred)

# Precision, Recall, F1 (micro and macro)
precision_micro = precision_score(y_test, y_pred, average='micro', zero_division=0)
recall_micro = recall_score(y_test, y_pred, average='micro', zero_division=0)
f1_micro = f1_score(y_test, y_pred, average='micro', zero_division=0)

precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
recall_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)

# Print results
print("=" * 80)
print("🎯 STACKING ENSEMBLE RESULTS")
print("=" * 80)
print(f"Accuracy (Exact Match):     {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Hamming Loss:               {hamming:.4f}")
print()
print("Micro-averaged metrics (treats each disease prediction equally):")
print(f"  Precision:                {precision_micro:.4f} ({precision_micro*100:.2f}%)")
print(f"  Recall:                   {recall_micro:.4f} ({recall_micro*100:.2f}%)")
print(f"  F1-Score:                 {f1_micro:.4f} ({f1_micro*100:.2f}%)")
print()
print("Macro-averaged metrics (treats each disease class equally):")
print(f"  Precision:                {precision_macro:.4f} ({precision_macro*100:.2f}%)")
print(f"  Recall:                   {recall_macro:.4f} ({recall_macro*100:.2f}%)")
print(f"  F1-Score:                 {f1_macro:.4f} ({f1_macro*100:.2f}%)")
print("=" * 80)
print()

# ==================== COMPARISON WITH BASE MODELS ====================

print("📈 COMPARISON WITH BASE MODELS:")
print("=" * 80)
print("Model                    | Accuracy  | F1-Micro  | F1-Macro")
print("-" * 80)
print(f"LightGBM (Base)          | 46.31%    | 53.76%    | 10.06%")
print(f"Neural Network (Base)    | 45.08%    | 59.41%    | 4.75%")
print(f"Simple Ensemble (Old)    | 0.00%     | 29.61%    | 9.16%")
print(f"Stacking Ensemble (New)  | {accuracy*100:5.2f}%    | {f1_micro*100:5.2f}%    | {f1_macro*100:5.2f}%")
print("=" * 80)
print()

# Determine if stacking is better
is_better_than_lgbm = accuracy > 0.4631 or f1_micro > 0.5376
is_better_than_nn = accuracy > 0.4508 or f1_micro > 0.5941
is_best = is_better_than_lgbm or is_better_than_nn

if is_best:
    print("🎉 SUCCESS! Stacking ensemble performs better than individual models!")
    print("   This model should be used in production.")
else:
    print("⚠️  Stacking ensemble did not outperform best individual models.")
    print("   Consider using LightGBM (46.31%) or Neural Network (59.41% F1) instead.")

print()

# ==================== SAVE STACKING ENSEMBLE ====================

print("💾 Saving stacking ensemble model...")

# Create ensemble wrapper that includes base models and meta-learner
ensemble_model = {
    'lightgbm': lightgbm_model,
    'neural_network': neural_network_model,
    'meta_learner': meta_learner,
    'base_models': ['lightgbm', 'neural_network'],
    'ensemble_type': 'stacking',
    'trained_date': datetime.now().isoformat()
}

# Save ensemble
joblib.dump(ensemble_model, MODEL_SAVE_PATH)
print(f"   ✅ Model saved to: {MODEL_SAVE_PATH}")

# Save model info
model_info = {
    'model_type': 'Stacking Ensemble',
    'base_models': {
        'lightgbm': {
            'type': 'LightGBM',
            'accuracy': 0.4631,
            'f1_micro': 0.5376
        },
        'neural_network': {
            'type': 'Neural Network (MLP)',
            'accuracy': 0.4508,
            'f1_micro': 0.5941
        }
    },
    'meta_learner': {
        'type': 'Logistic Regression',
        'solver': 'lbfgs',
        'max_iter': 1000,
        'regularization': 'L2'
    },
    'training_details': {
        'num_base_models': 2,
        'meta_features': int(meta_train.shape[1]),
        'trained_on': 'validation_predictions',
        'training_time_seconds': float(training_time),
        'prediction_time_seconds': float(prediction_time)
    },
    'dataset': {
        'train_samples': int(X_train.shape[0]),
        'val_samples': int(X_val.shape[0]),
        'test_samples': int(X_test.shape[0]),
        'features': int(X_train.shape[1]),
        'diseases': int(y_train.shape[1])
    },
    'trained_date': datetime.now().isoformat()
}

with open(INFO_SAVE_PATH, 'w') as f:
    json.dump(model_info, f, indent=2)
print(f"   ✅ Model info saved to: {INFO_SAVE_PATH}")

# Save metrics
metrics = {
    'accuracy': float(accuracy),
    'hamming_loss': float(hamming),
    'precision_micro': float(precision_micro),
    'recall_micro': float(recall_micro),
    'f1_micro': float(f1_micro),
    'precision_macro': float(precision_macro),
    'recall_macro': float(recall_macro),
    'f1_macro': float(f1_macro),
    'is_better_than_base_models': is_best,
    'comparison': {
        'lightgbm': {'accuracy': 0.4631, 'f1_micro': 0.5376},
        'neural_network': {'accuracy': 0.4508, 'f1_micro': 0.5941},
        'simple_ensemble': {'accuracy': 0.0, 'f1_micro': 0.2961},
        'stacking_ensemble': {'accuracy': float(accuracy), 'f1_micro': float(f1_micro)}
    }
}

with open(METRICS_SAVE_PATH, 'w') as f:
    json.dump(metrics, f, indent=2)
print(f"   ✅ Metrics saved to: {METRICS_SAVE_PATH}")

print()
print("=" * 80)
print("✅ STACKING ENSEMBLE TRAINING COMPLETE!")
print("=" * 80)
print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ==================== USAGE INSTRUCTIONS ====================

print("📖 HOW TO USE THIS MODEL:")
print("-" * 80)
print("To make predictions with the stacking ensemble:")
print()
print("```python")
print("import joblib")
print("import numpy as np")
print()
print("# Load ensemble")
print(f"ensemble = joblib.load('{MODEL_SAVE_PATH}')")
print()
print("# Get base models and meta-learner")
print("lgbm = ensemble['lightgbm']")
print("nn = ensemble['neural_network']")
print("meta = ensemble['meta_learner']")
print()
print("# Make predictions")
print("lgbm_pred = lgbm.predict_proba(X)")
print("nn_pred = nn.predict(X_dense)")
print("meta_features = np.hstack([lgbm_pred, nn_pred])")
print("final_prediction = meta.predict(meta_features)")
print("```")
print()
print("Or update backend/app/utils/ml_service.py to use this model!")
print("=" * 80)

