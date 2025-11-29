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
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
    
    Returns:
        XGBClassifier: Trained model
    """
    print("\n" + "=" * 60)
    print("TRAINING XGBOOST MODEL")
    print("=" * 60)
    
    # XGBoost parameters for multi-label classification
    model = XGBClassifier(
        objective='multi:softprob',  # Multi-class classification
        n_estimators=200,  # Number of boosting rounds
        max_depth=6,  # Maximum tree depth
        learning_rate=0.1,  # Learning rate
        subsample=0.8,  # Subsample ratio
        colsample_bytree=0.8,  # Column subsample ratio
        min_child_weight=3,  # Minimum sum of instance weight
        gamma=0.1,  # Minimum loss reduction
        reg_alpha=0.1,  # L1 regularization
        reg_lambda=1.0,  # L2 regularization
        random_state=42,
        n_jobs=-1,  # Use all available CPUs
        eval_metric='mlogloss',  # Evaluation metric
        tree_method='hist'  # Tree construction algorithm
    )
    
    print("\nModel parameters:")
    print(f"  - n_estimators: {model.n_estimators}")
    print(f"  - max_depth: {model.max_depth}")
    print(f"  - learning_rate: {model.learning_rate}")
    print(f"  - objective: {model.objective}")
    
    print("\nTraining model...")
    start_time = time.time()
    
    # Train model with early stopping on validation set
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=True
    )
    
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
    
    # Make predictions
    print("Making predictions on test set...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
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
    model_info = {
        'model_name': 'XGBoost',
        'model_type': 'Multi-label Classifier',
        'features': model.n_features_in_,
        'classes': model.n_classes_ if hasattr(model, 'n_classes_') else 'Multiple',
        'metrics': metrics,
        'parameters': {
            'n_estimators': model.n_estimators,
            'max_depth': model.max_depth,
            'learning_rate': model.learning_rate
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
        metrics = evaluate_model(model, X_test, y_test, disease_names)
        
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

