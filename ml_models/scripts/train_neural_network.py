#!/usr/bin/env python3
"""
Neural Network Model Training Script.

Trains a Multi-Label Neural Network for disease classification from symptoms.
Neural networks can learn complex relationships and often outperform tree-based models
for multi-label classification problems.

Expected accuracy: 50-70%
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
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, callbacks
    TENSORFLOW_AVAILABLE = True
    
    # Optimize TensorFlow for maximum performance on any system
    # Automatically detects and uses all available CPU cores
    import os
    import multiprocessing
    
    # Detect number of CPU cores automatically (works on any system)
    num_cores = multiprocessing.cpu_count()
    
    # Configure TensorFlow to use all available CPU cores
    os.environ['TF_NUM_INTEROP_THREADS'] = str(num_cores)  # Parallel operations
    os.environ['TF_NUM_INTRAOP_THREADS'] = str(num_cores)  # Sequential operations
    
    # Enable optimizations (works on all platforms)
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'  # Enable optimizations
    
    # TensorFlow will automatically use available hardware:
    # - On Apple Silicon: Uses Metal GPU automatically
    # - On NVIDIA GPUs: Uses CUDA automatically
    # - On other systems: Uses CPU with all cores
    
    print("🚀 TensorFlow configured for optimal performance")
    print(f"   CPU cores detected: {num_cores}")
    print(f"   Using all {num_cores} CPU cores for training")
    print("   GPU acceleration: Will be used automatically if available")
    
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️  TensorFlow not installed. Installing required packages...")
    print("   Run: pip install tensorflow")

# Define paths
MODEL_DIR = Path(__file__).parent.parent / 'models'
SCRIPTS_DIR = Path(__file__).parent


def load_preprocessed_data():
    """
    Load preprocessed training data.
    
    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    print("Loading preprocessed data...")
    
    X_train = joblib.load(MODEL_DIR / 'X_train.pkl')
    X_val = joblib.load(MODEL_DIR / 'X_val.pkl')
    X_test = joblib.load(MODEL_DIR / 'X_test.pkl')
    y_train = joblib.load(MODEL_DIR / 'y_train.pkl')
    y_val = joblib.load(MODEL_DIR / 'y_val.pkl')
    y_test = joblib.load(MODEL_DIR / 'y_test.pkl')
    
    # Convert sparse matrices to dense (Neural Networks require dense arrays)
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


def build_neural_network(input_dim, output_dim):
    """
    Build a multi-label neural network.
    
    Args:
        input_dim (int): Number of input features (symptoms)
        output_dim (int): Number of output labels (diseases)
    
    Returns:
        keras.Model: Compiled neural network model
    """
    print("\nBuilding neural network architecture...")
    
    model = models.Sequential([
        # Input layer
        layers.Dense(512, activation='relu', input_shape=(input_dim,)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        
        # Hidden layer 1
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        
        # Hidden layer 2
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        
        # Hidden layer 3
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        
        # Output layer (multi-label: one output per disease)
        layers.Dense(output_dim, activation='sigmoid')  # Sigmoid for multi-label
    ])
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',  # Binary cross-entropy for multi-label
        metrics=['accuracy', 'precision', 'recall']
    )
    
    print("✓ Neural network built")
    print(f"  Input: {input_dim} features")
    print(f"  Output: {output_dim} diseases")
    print(f"  Total parameters: {model.count_params():,}")
    
    return model


def train_neural_network(model, X_train, y_train, X_val, y_val):
    """
    Train the neural network model.
    
    Args:
        model: Keras model
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
    
    Returns:
        keras.Model: Trained model
    """
    print("\n" + "=" * 60)
    print("TRAINING NEURAL NETWORK")
    print("=" * 60)
    
    print("\nModel architecture:")
    model.summary()
    
    # Callbacks for training
    early_stopping = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
    
    print("\nStarting training...")
    print("(This may take 15-30 minutes depending on your system)")
    
    start_time = time.time()
    
    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=[early_stopping, reduce_lr],
        verbose=1
    )
    
    training_time = time.time() - start_time
    print(f"\n✓ Training completed in {training_time:.2f} seconds")
    
    return model, history


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
    y_pred_proba = model.predict(X_test, verbose=0)
    
    # Use threshold for binary predictions
    # Default threshold is 0.5, but we can optimize
    threshold = 0.5
    y_pred = (y_pred_proba >= threshold).astype(int)
    
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
    
    return metrics, y_pred_proba


def save_model(model, metrics, history, model_name='neural_network_model'):
    """
    Save trained model and metrics.
    
    Args:
        model: Trained Keras model
        metrics: Evaluation metrics
        history: Training history
        model_name: Name for saved model file
    """
    print(f"\nSaving model to {MODEL_DIR}...")
    
    # Save Keras model
    model_file = MODEL_DIR / f'{model_name}.h5'
    model.save(str(model_file))
    print(f"✓ Saved model: {model_file}")
    
    # Save metrics
    metrics_file = MODEL_DIR / f'{model_name}_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Saved metrics: {metrics_file}")
    
    # Save model info
    model_info = {
        'model_name': 'Neural Network (Multi-Label)',
        'model_type': 'Deep Learning - Multi-Label Classifier',
        'architecture': 'Sequential',
        'layers': len(model.layers),
        'total_parameters': int(model.count_params()),
        'metrics': metrics,
        'parameters': {
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'loss': 'binary_crossentropy',
            'activation': 'sigmoid (multi-label)',
            'batch_size': 32,
            'epochs_trained': len(history.history['loss']) if history else 'Unknown'
        }
    }
    
    info_file = MODEL_DIR / f'{model_name}_info.json'
    with open(info_file, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"✓ Saved model info: {info_file}")


def main():
    """Main function to train neural network model."""
    print("=" * 60)
    print("NEURAL NETWORK MODEL TRAINING")
    print("=" * 60)
    
    if not TENSORFLOW_AVAILABLE:
        print("\n❌ TensorFlow not available!")
        print("Please install TensorFlow:")
        print("  pip install tensorflow")
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
        
        # Build model
        model = build_neural_network(X_train.shape[1], y_train.shape[1])
        
        # Train model
        model, history = train_neural_network(model, X_train, y_train, X_val, y_val)
        
        # Evaluate model
        metrics, y_pred_proba = evaluate_model(model, X_test, y_test, disease_names)
        
        # Save model
        save_model(model, metrics, history, 'neural_network_model')
        
        print("\n" + "=" * 60)
        print("✓ NEURAL NETWORK MODEL TRAINING COMPLETE!")
        print("=" * 60)
        print(f"\nModel saved: {MODEL_DIR / 'neural_network_model.h5'}")
        print(f"Accuracy: {metrics['accuracy']*100:.2f}%")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

