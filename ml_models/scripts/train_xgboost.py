#!/usr/bin/env python3
"""
XGBoost Model Training Script.

Trains XGBoost model for multi-label disease classification from symptoms.
This is the primary recommended model with expected accuracy of 75-85%.
"""

import joblib
import json
from pathlib import Path
import numpy as np
from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, multilabel_confusion_matrix
)
import time

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
    
    # Convert sparse matrices to dense (XGBoost requires dense arrays)
    print("Converting sparse matrices to dense format...")
    X_train = X_train.toarray()
    X_val = X_val.toarray()
    X_test = X_test.toarray()
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def train_xgboost_model(X_train, y_train, X_val, y_val):
    """
    Train XGBoost model for multi-label classification.
    
    For multi-label classification, we use OneVsRestClassifier wrapper
    which trains one binary classifier per disease.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
    
    Returns:
        OneVsRestClassifier: Trained model
    """
    print("\n" + "=" * 60)
    print("TRAINING XGBOOST MODEL")
    print("=" * 60)
    
    from sklearn.multioutput import MultiOutputClassifier
    
    # XGBoost parameters for binary classification (used per label)
    base_xgb = XGBClassifier(
        objective='binary:logistic',  # Binary classification for each disease
        n_estimators=100,  # Number of boosting rounds (reduced for faster training)
        max_depth=6,  # Maximum tree depth
        learning_rate=0.1,  # Learning rate
        subsample=0.8,  # Subsample ratio
        colsample_bytree=0.8,  # Column subsample ratio
        min_child_weight=3,  # Minimum sum of instance weight
        gamma=0.1,  # Minimum loss reduction
        reg_alpha=0.1,  # L1 regularization
        reg_lambda=1.0,  # L2 regularization
        base_score=0.5,  # Initial prediction score (required for binary:logistic)
        random_state=42,
        n_jobs=-1,  # Use all available CPUs
        eval_metric='logloss',  # Evaluation metric for binary
        tree_method='hist'  # Tree construction algorithm
    )
    
    # Wrap with MultiOutputClassifier for multi-label classification
    # This trains one binary classifier per disease
    model = MultiOutputClassifier(base_xgb, n_jobs=-1)
    
    print("\nModel parameters:")
    print(f"  - Base classifier: XGBoost")
    print(f"  - n_estimators: {base_xgb.n_estimators}")
    print(f"  - max_depth: {base_xgb.max_depth}")
    print(f"  - learning_rate: {base_xgb.learning_rate}")
    print(f"  - Multi-label strategy: One binary classifier per disease")
    print(f"  - Number of diseases: {y_train.shape[1]}")
    
    print("\nTraining model...")
    print(f"This will train one binary classifier for each of {y_train.shape[1]} diseases...")
    print("(This may take 10-30 minutes depending on your system)")
    start_time = time.time()
    
    # Train model (MultiOutputClassifier handles multi-label automatically)
    # It trains one binary XGBoost classifier per disease
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    print(f"\n✓ Training completed in {training_time:.2f} seconds")
    
    return model


def evaluate_model(model, X_test, y_test, disease_names, y_train=None):
    """
    Evaluate model performance on test set.
    
    Args:
        model: Trained model (MultiOutputClassifier)
        X_test: Test features
        y_test: Test labels
        disease_names: List of disease names
    
    Returns:
        dict: Evaluation metrics
    """
    print("\n" + "=" * 60)
    print("EVALUATING MODEL")
    print("=" * 60)
    
    # Get prediction probabilities (for MultiOutputClassifier, this returns list of arrays)
    # Each array contains probabilities for that label
    print("Getting prediction probabilities...")
    y_pred_proba_list = model.predict_proba(X_test)
    
    # Convert list of arrays to a single 2D array (n_samples, n_labels)
    # Each element is the probability of that disease for that sample
    y_pred_proba = np.array([proba[:, 1] if proba.shape[1] > 1 else proba[:, 0] 
                            for proba in y_pred_proba_list]).T
    
    # Diagnostic: Check prediction probabilities
    print("\n📊 Prediction Probability Statistics:")
    print(f"  Max probability: {y_pred_proba.max():.4f}")
    print(f"  Min probability: {y_pred_proba.min():.4f}")
    print(f"  Mean probability: {y_pred_proba.mean():.4f}")
    print(f"  Probabilities > 0.5: {(y_pred_proba > 0.5).sum()}")
    print(f"  Probabilities > 0.3: {(y_pred_proba > 0.3).sum()}")
    print(f"  Probabilities > 0.1: {(y_pred_proba > 0.1).sum()}")
    
    # Use top-k predictions per sample instead of fixed threshold
    # This is better for sparse multi-label classification
    print("\nUsing top-k prediction strategy...")
    
    # Find average number of diseases per sample in training data (need y_train access)
    # We'll use a reasonable top-k based on the data structure
    # For now, use top-3 predictions (most samples have 1 disease, so top-3 is reasonable)
    top_k = 3
    print(f"  Using top-{top_k} predictions per sample")
    
    # For each sample, predict top-k diseases
    y_pred = np.zeros_like(y_pred_proba, dtype=int)
    for i in range(y_pred_proba.shape[0]):
        # Get top-k indices (highest probabilities)
        top_k_indices = np.argsort(y_pred_proba[i])[-top_k:][::-1]
        # Only include predictions with probability > 0.05 (very low threshold)
        top_k_indices = top_k_indices[y_pred_proba[i, top_k_indices] > 0.05]
        if len(top_k_indices) > 0:
            y_pred[i, top_k_indices] = 1
        else:
            # Fallback: at least predict top-1 if all probabilities are very low
            top_idx = np.argmax(y_pred_proba[i])
            y_pred[i, top_idx] = 1
    
    print(f"  Total predictions made: {y_pred.sum()}")
    print(f"  Samples with predictions: {(y_pred.sum(axis=1) > 0).sum()}/{y_pred.shape[0]}")
    print(f"  Average predictions per sample: {y_pred.sum(axis=1).mean():.2f}")
    
    # Make predictions using standard method for comparison
    print("\nMaking predictions on test set...")
    y_pred_standard = model.predict(X_test)
    
    # Calculate metrics
    # For multi-label classification, we use subset accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Average metrics across all labels
    precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    # Micro-averaged metrics (overall performance)
    precision_micro = precision_score(y_test, y_pred, average='micro', zero_division=0)
    recall_micro = recall_score(y_test, y_pred, average='micro', zero_division=0)
    f1_micro = f1_score(y_test, y_pred, average='micro', zero_division=0)
    
    print(f"\nTest Set Performance:")
    print(f"  Accuracy (Exact Match): {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nMacro-Averaged Metrics:")
    print(f"  Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"  Recall: {recall:.4f} ({recall*100:.2f}%)")
    print(f"  F1-Score: {f1:.4f} ({f1*100:.2f}%)")
    print(f"\nMicro-Averaged Metrics (Overall):")
    print(f"  Precision: {precision_micro:.4f} ({precision_micro*100:.2f}%)")
    print(f"  Recall: {recall_micro:.4f} ({recall_micro*100:.2f}%)")
    print(f"  F1-Score: {f1_micro:.4f} ({f1_micro*100:.2f}%)")
    
    # Store metrics
    metrics = {
        'accuracy': float(accuracy),
        'precision_macro': float(precision),
        'recall_macro': float(recall),
        'f1_macro': float(f1),
        'precision_micro': float(precision_micro),
        'recall_micro': float(recall_micro),
        'f1_micro': float(f1_micro)
    }
    
    return metrics


def save_model(model, metrics, model_name='xgboost_model'):
    """
    Save trained model and metrics.
    
    Args:
        model: Trained model
        metrics: Evaluation metrics
        model_name: Name for saved model file
    """
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
    # Get base estimator for parameters
    base_estimator = model.estimators_[0] if hasattr(model, 'estimators_') else model
    
    model_info = {
        'model_name': 'XGBoost',
        'model_type': 'Multi-label Classifier (MultiOutputClassifier)',
        'features': base_estimator.n_features_in_ if hasattr(base_estimator, 'n_features_in_') else 'Unknown',
        'n_labels': len(model.estimators_) if hasattr(model, 'estimators_') else 'Unknown',
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
    """Main function to train XGBoost model."""
    print("=" * 60)
    print("XGBOOST MODEL TRAINING")
    print("=" * 60)
    
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
        model = train_xgboost_model(X_train, y_train, X_val, y_val)
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test, disease_names, y_train)
        
        # Save model
        save_model(model, metrics, 'xgboost_model')
        
        print("\n" + "=" * 60)
        print("✓ XGBOOST MODEL TRAINING COMPLETE!")
        print("=" * 60)
        print(f"\nModel saved: {MODEL_DIR / 'xgboost_model.pkl'}")
        print(f"Accuracy: {metrics['accuracy']*100:.2f}%")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

