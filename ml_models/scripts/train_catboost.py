#!/usr/bin/env python3
"""
CatBoost Model Training Script.

Trains a CatBoost model for multi-label disease classification.
CatBoost excels at handling categorical features and imbalanced data.

Expected accuracy: 45-65%
"""

import joblib
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score
)
import time

try:
    from catboost import CatBoostClassifier
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.dummy import DummyClassifier
    from sklearn.base import BaseEstimator
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    print("⚠️  CatBoost not installed. Installing required packages...")
    print("   Run: pip install catboost")

# Define paths
MODEL_DIR = Path(__file__).parent.parent / 'models'
SCRIPTS_DIR = Path(__file__).parent


def load_preprocessed_data():
    """Load preprocessed training data."""
    print("Loading preprocessed data...")
    
    X_train = joblib.load(MODEL_DIR / 'X_train.pkl')
    X_val = joblib.load(MODEL_DIR / 'X_val.pkl')
    X_test = joblib.load(MODEL_DIR / 'X_test.pkl')
    y_train = joblib.load(MODEL_DIR / 'y_train.pkl')
    y_val = joblib.load(MODEL_DIR / 'y_val.pkl')
    y_test = joblib.load(MODEL_DIR / 'y_test.pkl')
    
    # Convert sparse matrices to dense
    print("Converting sparse matrices to dense format...")
    if hasattr(X_train, 'toarray'):
        X_train = X_train.toarray()
    if hasattr(X_val, 'toarray'):
        X_val = X_val.toarray()
    if hasattr(X_test, 'toarray'):
        X_test = X_test.toarray()
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


class CustomMultiOutputClassifier(BaseEstimator):
    """Custom MultiOutputClassifier that handles diseases with no positive examples."""
    
    def __init__(self, base_estimator, n_jobs=-1):
        self.base_estimator = base_estimator
        self.n_jobs = n_jobs
        self.estimators_ = []
        self.dummy_estimators_ = []
        self.disease_indices_ = []
    
    def fit(self, X, y):
        """Train one classifier per disease, using dummy classifier for diseases with no positives."""
        n_diseases = y.shape[1]
        self.estimators_ = []
        self.dummy_estimators_ = []
        self.disease_indices_ = []
        
        print(f"\nTraining {n_diseases} binary classifiers...")
        skipped = 0
        
        for i in range(n_diseases):
            y_col = y[:, i]
            
            # Check if disease has any positive examples
            if y_col.sum() == 0:
                # Use DummyClassifier that always predicts 0
                dummy = DummyClassifier(strategy='constant', constant=0)
                dummy.fit(X, y_col)
                self.dummy_estimators_.append((i, dummy))
                self.disease_indices_.append(i)
                skipped += 1
            else:
                # Train CatBoost classifier
                estimator = CatBoostClassifier(
                    iterations=200,
                    depth=8,
                    learning_rate=0.05,
                    loss_function='Logloss',
                    eval_metric='Logloss',
                    random_seed=42,
                    verbose=False,
                    task_type='CPU'
                )
                estimator.fit(X, y_col)
                self.estimators_.append((i, estimator))
                self.disease_indices_.append(i)
            
            if (i + 1) % 100 == 0:
                print(f"  Trained {i + 1}/{n_diseases} classifiers... (skipped {skipped})")
        
        print(f"\n✓ Training complete: {len(self.estimators_)} CatBoost + {len(self.dummy_estimators_)} Dummy classifiers")
        return self
    
    def predict_proba(self, X):
        """Get prediction probabilities for all diseases."""
        n_samples = X.shape[0]
        n_diseases = len(self.estimators_) + len(self.dummy_estimators_)
        
        probas = []
        all_indices = sorted([idx for idx, _ in self.estimators_] + [idx for idx, _ in self.dummy_estimators_])
        
        proba_matrix = np.zeros((n_diseases, n_samples, 2))
        
        for idx, estimator in self.estimators_:
            proba = estimator.predict_proba(X)
            proba_matrix[idx] = proba
        
        for idx, dummy in self.dummy_estimators_:
            proba = dummy.predict_proba(X)
            proba_matrix[idx] = proba
        
        # Convert to list format expected by MultiOutputClassifier interface
        for i in range(n_diseases):
            probas.append(proba_matrix[i])
        
        return probas


def train_catboost_model(X_train, y_train, X_val, y_val):
    """
    Train CatBoost model for multi-label classification.
    Handles diseases with no positive examples using DummyClassifier.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
    
    Returns:
        CustomMultiOutputClassifier: Trained model
    """
    print("\n" + "=" * 60)
    print("TRAINING CATBOOST MODEL")
    print("=" * 60)
    
    print("\nModel parameters:")
    print(f"  - Base classifier: CatBoost")
    print(f"  - iterations: 200")
    print(f"  - depth: 8")
    print(f"  - learning_rate: 0.05")
    print(f"  - Multi-label strategy: One binary classifier per disease")
    print(f"  - Number of diseases: {y_train.shape[1]}")
    print(f"  - Handling: DummyClassifier for diseases with no positives")
    
    print("\nTraining model...")
    print("(This may take 10-20 minutes depending on your system)")
    
    start_time = time.time()
    
    # Use custom classifier that handles edge cases
    model = CustomMultiOutputClassifier(None, n_jobs=-1)
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    print(f"\n✓ Training completed in {training_time:.2f} seconds ({training_time/60:.1f} minutes)")
    
    return model


def evaluate_model(model, X_test, y_test, disease_names):
    """
    Evaluate model performance on test set.
    Uses top-k prediction strategy similar to XGBoost.
    """
    print("\n" + "=" * 60)
    print("EVALUATING MODEL")
    print("=" * 60)
    
    # Get prediction probabilities
    print("Getting prediction probabilities...")
    y_pred_proba_list = model.predict_proba(X_test)
    
    # Convert to probability matrix
    # Handle both list and array formats
    if isinstance(y_pred_proba_list, list):
        y_pred_proba = np.array([proba[:, 1] if proba.shape[1] > 1 else proba[:, 0] 
                                for proba in y_pred_proba_list]).T
    else:
        y_pred_proba = y_pred_proba_list
    
    # Use top-k predictions
    print("\nUsing top-k prediction strategy...")
    top_k = 3
    print(f"  Using top-{top_k} predictions per sample")
    
    y_pred = np.zeros_like(y_pred_proba, dtype=int)
    for i in range(y_pred_proba.shape[0]):
        top_k_indices = np.argsort(y_pred_proba[i])[-top_k:][::-1]
        top_k_indices = top_k_indices[y_pred_proba[i, top_k_indices] > 0.05]
        if len(top_k_indices) > 0:
            y_pred[i, top_k_indices] = 1
        else:
            top_idx = np.argmax(y_pred_proba[i])
            y_pred[i, top_idx] = 1
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    precision_micro = precision_score(y_test, y_pred, average='micro', zero_division=0)
    recall_micro = recall_score(y_test, y_pred, average='micro', zero_division=0)
    f1_micro = f1_score(y_test, y_pred, average='micro', zero_division=0)
    
    print(f"\nTest Set Performance:")
    print(f"  Accuracy (Exact Match): {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nMacro-Averaged Metrics:")
    print(f"  Precision: {precision_macro:.4f} ({precision_macro*100:.2f}%)")
    print(f"  Recall: {recall_macro:.4f} ({recall_macro*100:.2f}%)")
    print(f"  F1-Score: {f1_macro:.4f} ({f1_macro*100:.2f}%)")
    print(f"\nMicro-Averaged Metrics (Overall):")
    print(f"  Precision: {precision_micro:.4f} ({precision_micro*100:.2f}%)")
    print(f"  Recall: {recall_micro:.4f} ({recall_micro*100:.2f}%)")
    print(f"  F1-Score: {f1_micro:.4f} ({f1_micro*100:.2f}%)")
    
    metrics = {
        'accuracy': float(accuracy),
        'precision_macro': float(precision_macro),
        'recall_macro': float(recall_macro),
        'f1_macro': float(f1_macro),
        'precision_micro': float(precision_micro),
        'recall_micro': float(recall_micro),
        'f1_micro': float(f1_micro)
    }
    
    return metrics


def save_model(model, metrics, model_name='catboost_model'):
    """Save trained model and metrics."""
    print(f"\nSaving model to {MODEL_DIR}...")
    
    model_file = MODEL_DIR / f'{model_name}.pkl'
    joblib.dump(model, model_file)
    print(f"✓ Saved model: {model_file}")
    
    metrics_file = MODEL_DIR / f'{model_name}_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Saved metrics: {metrics_file}")
    
    model_info = {
        'model_name': 'CatBoost',
        'model_type': 'Multi-label Classifier (MultiOutputClassifier)',
        'metrics': metrics
    }
    
    info_file = MODEL_DIR / f'{model_name}_info.json'
    with open(info_file, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"✓ Saved model info: {info_file}")


def main():
    """Main function to train CatBoost model."""
    print("=" * 60)
    print("CATBOOST MODEL TRAINING")
    print("=" * 60)
    
    if not CATBOOST_AVAILABLE:
        print("\n❌ CatBoost not available!")
        print("Please install CatBoost:")
        print("  pip install catboost")
        return
    
    try:
        if not (MODEL_DIR / 'X_train.pkl').exists():
            raise FileNotFoundError(
                "Preprocessed data not found!\n"
                "Please run feature_engineering.py first."
            )
        
        X_train, X_val, X_test, y_train, y_val, y_test = load_preprocessed_data()
        
        with open(MODEL_DIR / 'unique_diseases.txt', 'r') as f:
            disease_names = [line.strip() for line in f.readlines()]
        
        print(f"Training for {len(disease_names)} diseases")
        
        model = train_catboost_model(X_train, y_train, X_val, y_val)
        metrics = evaluate_model(model, X_test, y_test, disease_names)
        save_model(model, metrics, 'catboost_model')
        
        print("\n" + "=" * 60)
        print("✓ CATBOOST MODEL TRAINING COMPLETE!")
        print("=" * 60)
        print(f"\nModel saved: {MODEL_DIR / 'catboost_model.pkl'}")
        print(f"Accuracy: {metrics['accuracy']*100:.2f}%")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

