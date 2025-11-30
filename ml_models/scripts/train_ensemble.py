#!/usr/bin/env python3
"""
Ensemble Model Training Script.

Combines multiple models (XGBoost, Random Forest, LightGBM, CatBoost, Neural Network)
using voting or stacking to improve accuracy.

Expected accuracy: 45-65% (5-10% improvement over single models)
"""

import joblib
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score
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
    
    # Convert sparse to dense
    if hasattr(X_train, 'toarray'):
        X_train = X_train.toarray()
    if hasattr(X_val, 'toarray'):
        X_val = X_val.toarray()
    if hasattr(X_test, 'toarray'):
        X_test = X_test.toarray()
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def load_trained_models():
    """
    Load all available trained models.
    
    Returns:
        dict: Dictionary of model_name -> model
    """
    models = {}
    
    # Try to load XGBoost
    xgb_file = MODEL_DIR / 'xgboost_model.pkl'
    if xgb_file.exists():
        try:
            models['xgboost'] = joblib.load(xgb_file)
            print("✓ Loaded XGBoost model")
        except:
            print("⚠️  Could not load XGBoost model")
    
    # Try to load Random Forest
    rf_file = MODEL_DIR / 'random_forest_model.pkl'
    if rf_file.exists():
        try:
            models['random_forest'] = joblib.load(rf_file)
            print("✓ Loaded Random Forest model")
        except:
            print("⚠️  Could not load Random Forest model")
    
    # Try to load LightGBM
    lgb_file = MODEL_DIR / 'lightgbm_model.pkl'
    if lgb_file.exists():
        try:
            models['lightgbm'] = joblib.load(lgb_file)
            print("✓ Loaded LightGBM model")
        except:
            print("⚠️  Could not load LightGBM model")
    
    # Try to load CatBoost
    cat_file = MODEL_DIR / 'catboost_model.pkl'
    if cat_file.exists():
        try:
            models['catboost'] = joblib.load(cat_file)
            print("✓ Loaded CatBoost model")
        except:
            print("⚠️  Could not load CatBoost model")
    
    # Try to load Neural Network
    nn_file = MODEL_DIR / 'neural_network_model.h5'
    if nn_file.exists():
        try:
            import tensorflow as tf
            models['neural_network'] = tf.keras.models.load_model(str(nn_file))
            print("✓ Loaded Neural Network model")
        except:
            print("⚠️  Could not load Neural Network model")
    
    return models


def get_prediction_proba(model, X, model_type='standard'):
    """
    Get prediction probabilities from a model.
    
    Args:
        model: Trained model
        X: Input features
        model_type: Type of model ('standard', 'neural_network')
    
    Returns:
        np.array: Probability matrix (n_samples, n_labels)
    """
    if model_type == 'neural_network':
        # Neural network returns probabilities directly
        return model.predict(X, verbose=0)
    else:
        # MultiOutputClassifier returns list of arrays
        y_pred_proba_list = model.predict_proba(X)
        return np.array([proba[:, 1] if proba.shape[1] > 1 else proba[:, 0] 
                        for proba in y_pred_proba_list]).T


def ensemble_predict(models, X, method='weighted_average'):
    """
    Make ensemble predictions from multiple models.
    
    Args:
        models: Dictionary of model_name -> model
        X: Input features
        method: 'weighted_average', 'voting', or 'stacking'
    
    Returns:
        np.array: Probability matrix (n_samples, n_labels)
    """
    print(f"\nMaking ensemble predictions using {method}...")
    
    all_probas = []
    model_weights = {
        'xgboost': 0.3,
        'lightgbm': 0.25,
        'neural_network': 0.25,
        'catboost': 0.1,
        'random_forest': 0.1
    }
    
    # Get predictions from each model
    for model_name, model in models.items():
        try:
            model_type = 'neural_network' if model_name == 'neural_network' else 'standard'
            proba = get_prediction_proba(model, X, model_type)
            weight = model_weights.get(model_name, 0.1)
            all_probas.append((proba, weight))
            print(f"  ✓ {model_name}: shape {proba.shape}, weight {weight}")
        except Exception as e:
            print(f"  ⚠️  Error with {model_name}: {str(e)}")
            continue
    
    if not all_probas:
        raise ValueError("No models could make predictions!")
    
    # Combine predictions
    if method == 'weighted_average':
        # Weighted average of probabilities
        total_weight = sum(w for _, w in all_probas)
        ensemble_proba = sum(proba * weight for proba, weight in all_probas) / total_weight
    
    elif method == 'voting':
        # Simple average
        ensemble_proba = np.mean([proba for proba, _ in all_probas], axis=0)
    
    else:
        # Default to weighted average
        total_weight = sum(w for _, w in all_probas)
        ensemble_proba = sum(proba * weight for proba, weight in all_probas) / total_weight
    
    return ensemble_proba


def evaluate_ensemble(models, X_test, y_test, disease_names):
    """
    Evaluate ensemble model performance.
    
    Args:
        models: Dictionary of trained models
        X_test: Test features
        y_test: Test labels
        disease_names: List of disease names
    
    Returns:
        dict: Evaluation metrics
    """
    print("\n" + "=" * 60)
    print("EVALUATING ENSEMBLE MODEL")
    print("=" * 60)
    
    # Get ensemble predictions
    y_pred_proba = ensemble_predict(models, X_test, method='weighted_average')
    
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
    
    print(f"\nEnsemble Model Performance:")
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
        'f1_micro': float(f1_micro),
        'models_used': list(models.keys())
    }
    
    return metrics


def save_ensemble_info(models, metrics):
    """Save ensemble model information."""
    print(f"\nSaving ensemble information...")
    
    ensemble_info = {
        'model_name': 'Ensemble Model',
        'model_type': 'Weighted Average Ensemble',
        'models_used': list(models.keys()),
        'method': 'weighted_average',
        'metrics': metrics
    }
    
    info_file = MODEL_DIR / 'ensemble_model_info.json'
    with open(info_file, 'w') as f:
        json.dump(ensemble_info, f, indent=2)
    print(f"✓ Saved ensemble info: {info_file}")
    
    metrics_file = MODEL_DIR / 'ensemble_model_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Saved ensemble metrics: {metrics_file}")


def main():
    """Main function to create and evaluate ensemble model."""
    print("=" * 60)
    print("ENSEMBLE MODEL EVALUATION")
    print("=" * 60)
    
    print("\nThis script combines multiple trained models for better accuracy.")
    print("Make sure you have trained at least 2 models first.")
    
    try:
        # Load preprocessed data
        X_train, X_val, X_test, y_train, y_val, y_test = load_preprocessed_data()
        
        # Load disease names
        with open(MODEL_DIR / 'unique_diseases.txt', 'r') as f:
            disease_names = [line.strip() for line in f.readlines()]
        
        # Load trained models
        print("\nLoading trained models...")
        models = load_trained_models()
        
        if len(models) < 2:
            print(f"\n⚠️  Only {len(models)} model(s) available. Need at least 2 models for ensemble.")
            print("Available models:")
            for name in models.keys():
                print(f"  - {name}")
            print("\nPlease train more models first:")
            print("  - python train_xgboost.py")
            print("  - python train_lightgbm.py")
            print("  - python train_catboost.py")
            print("  - python train_neural_network.py")
            return
        
        print(f"\n✓ Loaded {len(models)} models for ensemble:")
        for name in models.keys():
            print(f"  - {name}")
        
        # Evaluate ensemble
        metrics = evaluate_ensemble(models, X_test, y_test, disease_names)
        
        # Save ensemble info
        save_ensemble_info(models, metrics)
        
        print("\n" + "=" * 60)
        print("✓ ENSEMBLE MODEL EVALUATION COMPLETE!")
        print("=" * 60)
        print(f"\nEnsemble Accuracy: {metrics['accuracy']*100:.2f}%")
        print(f"Models combined: {', '.join(metrics['models_used'])}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

