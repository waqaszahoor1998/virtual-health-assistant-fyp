#!/usr/bin/env python3
"""
LightGBM Model Training Script.

Trains a LightGBM model for multi-label disease classification.
LightGBM often outperforms XGBoost and is faster to train.

Expected accuracy: 40-60%
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
    import lightgbm as lgb
    from sklearn.multioutput import MultiOutputClassifier
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("⚠️  LightGBM not installed. Installing required packages...")
    print("   Run: pip install lightgbm")

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


def train_lightgbm_model(X_train, y_train, X_val, y_val):
    """
    Train LightGBM model for multi-label classification.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
    
    Returns:
        MultiOutputClassifier: Trained model
    """
    print("\n" + "=" * 60)
    print("TRAINING LIGHTGBM MODEL")
    print("=" * 60)
    
    # LightGBM parameters
    base_lgb = lgb.LGBMClassifier(
        objective='binary',  # Binary classification for each disease
        n_estimators=200,
        max_depth=8,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_samples=20,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    # Wrap with MultiOutputClassifier for multi-label classification
    model = MultiOutputClassifier(base_lgb, n_jobs=-1)
    
    print("\nModel parameters:")
    print(f"  - Base classifier: LightGBM")
    print(f"  - n_estimators: {base_lgb.n_estimators}")
    print(f"  - max_depth: {base_lgb.max_depth}")
    print(f"  - learning_rate: {base_lgb.learning_rate}")
    print(f"  - Multi-label strategy: One binary classifier per disease")
    print(f"  - Number of diseases: {y_train.shape[1]}")
    
    print("\nTraining model...")
    print(f"This will train one binary classifier for each of {y_train.shape[1]} diseases...")
    print("(This may take 5-15 minutes depending on your system)")
    
    start_time = time.time()
    
    # Train model
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    print(f"\n✓ Training completed in {training_time:.2f} seconds")
    
    return model


def evaluate_model(model, X_test, y_test, disease_names):
    """
    Evaluate model performance on test set.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        disease_names: List of disease names
    
    Returns:
        dict: Evaluation metrics
    """
    print("\n" + "=" * 60)
    print("EVALUATING MODEL")
    print("=" * 60)
    
    # Get prediction probabilities
    print("Getting prediction probabilities...")
    y_pred_proba_list = model.predict_proba(X_test)
    
    # Convert to probability matrix
    y_pred_proba = np.array([proba[:, 1] if proba.shape[1] > 1 else proba[:, 0] 
                            for proba in y_pred_proba_list]).T
    
    # Use top-k predictions per sample
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
    
    print(f"  Total predictions made: {y_pred.sum()}")
    print(f"  Samples with predictions: {(y_pred.sum(axis=1) > 0).sum()}/{y_pred.shape[0]}")
    
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
    
    # Store metrics
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


def save_model(model, metrics, model_name='lightgbm_model'):
    """Save trained model and metrics."""
    print(f"\nSaving model to {MODEL_DIR}...")
    
    # Save model
    model_file = MODEL_DIR / f'{model_name}.pkl'
    joblib.dump(model, model_file)
    print(f"✓ Saved model: {model_file}")
    
    # Save metrics
    metrics_file = MODEL_DIR / f'{model_name}_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Saved metrics: {metrics_file}")
    
    # Save model info
    base_estimator = model.estimators_[0] if hasattr(model, 'estimators_') else model
    
    model_info = {
        'model_name': 'LightGBM',
        'model_type': 'Multi-label Classifier (MultiOutputClassifier)',
        'metrics': metrics,
        'parameters': {
            'n_estimators': base_estimator.n_estimators if hasattr(base_estimator, 'n_estimators') else 'Unknown',
            'max_depth': base_estimator.max_depth if hasattr(base_estimator, 'max_depth') else 'Unknown',
            'learning_rate': base_estimator.learning_rate if hasattr(base_estimator, 'learning_rate') else 'Unknown',
            'objective': base_estimator.objective if hasattr(base_estimator, 'objective') else 'Unknown'
        }
    }
    
    info_file = MODEL_DIR / f'{model_name}_info.json'
    with open(info_file, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"✓ Saved model info: {info_file}")


def main():
    """Main function to train LightGBM model."""
    print("=" * 60)
    print("LIGHTGBM MODEL TRAINING")
    print("=" * 60)
    
    if not LIGHTGBM_AVAILABLE:
        print("\n❌ LightGBM not available!")
        print("Please install LightGBM:")
        print("  pip install lightgbm")
        return
    
    try:
        # Check if preprocessed data exists
        if not (MODEL_DIR / 'X_train.pkl').exists():
            raise FileNotFoundError(
                "Preprocessed data not found!\n"
                "Please run feature_engineering.py first."
            )
        
        # Load preprocessed data
        X_train, X_val, X_test, y_train, y_val, y_test = load_preprocessed_data()
        
        # Load disease names
        with open(MODEL_DIR / 'unique_diseases.txt', 'r') as f:
            disease_names = [line.strip() for line in f.readlines()]
        
        print(f"Training for {len(disease_names)} diseases")
        
        # Train model
        model = train_lightgbm_model(X_train, y_train, X_val, y_val)
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test, disease_names)
        
        # Save model
        save_model(model, metrics, 'lightgbm_model')
        
        print("\n" + "=" * 60)
        print("✓ LIGHTGBM MODEL TRAINING COMPLETE!")
        print("=" * 60)
        print(f"\nModel saved: {MODEL_DIR / 'lightgbm_model.pkl'}")
        print(f"Accuracy: {metrics['accuracy']*100:.2f}%")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
