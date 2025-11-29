"""
Machine Learning Service.

Handles loading and using trained ML models for disease prediction.
"""

import joblib
import numpy as np
from pathlib import Path
import json
from flask import current_app


class MLPredictionService:
    """
    Service class for ML model predictions.
    
    Handles loading models, preprocessing symptoms, and making predictions.
    """
    
    def __init__(self):
        """Initialize ML service with model paths."""
        # Get models directory from config
        self.models_dir = Path(current_app.config.get('ML_MODELS_DIR', 
            Path(__file__).parent.parent.parent / 'ml_models' / 'models'
        ))
        
        # Model files
        self.xgboost_model_file = self.models_dir / 'xgboost_model.pkl'
        self.random_forest_model_file = self.models_dir / 'random_forest_model.pkl'
        self.vectorizer_file = self.models_dir / 'symptom_vectorizer.pkl'
        self.encoder_file = self.models_dir / 'disease_encoder.pkl'
        self.diseases_file = self.models_dir / 'unique_diseases.txt'
        
        # Loaded components (lazy loading)
        self.xgboost_model = None
        self.random_forest_model = None
        self.vectorizer = None
        self.encoder = None
        self.disease_names = None
        self.model_loaded = False
    
    def load_models(self):
        """
        Load ML models and preprocessing components.
        
        Uses lazy loading - only loads when needed.
        """
        if self.model_loaded:
            return
        
        try:
            # Check if models exist
            if not self.xgboost_model_file.exists():
                raise FileNotFoundError(
                    f"XGBoost model not found at {self.xgboost_model_file}.\n"
                    "Please train models first using ml_models/scripts/train_xgboost.py"
                )
            
            print(f"Loading ML models from {self.models_dir}...")
            
            # Load XGBoost model (primary model)
            self.xgboost_model = joblib.load(self.xgboost_model_file)
            print("✓ Loaded XGBoost model")
            
            # Load Random Forest model (optional, for comparison)
            if self.random_forest_model_file.exists():
                self.random_forest_model = joblib.load(self.random_forest_model_file)
                print("✓ Loaded Random Forest model")
            
            # Load vectorizer
            self.vectorizer = joblib.load(self.vectorizer_file)
            print("✓ Loaded symptom vectorizer")
            
            # Load disease encoder
            self.encoder = joblib.load(self.encoder_file)
            print("✓ Loaded disease encoder")
            
            # Load disease names
            if self.diseases_file.exists():
                with open(self.diseases_file, 'r') as f:
                    self.disease_names = [line.strip() for line in f.readlines()]
                print(f"✓ Loaded {len(self.disease_names)} disease names")
            
            self.model_loaded = True
            print("✓ All ML components loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading ML models: {e}")
            raise
    
    def preprocess_symptoms(self, symptoms):
        """
        Preprocess symptoms list into feature vector.
        
        Args:
            symptoms (list): List of symptom strings
        
        Returns:
            numpy.ndarray: Feature vector ready for model
        """
        if not self.vectorizer:
            self.load_models()
        
        # Join symptoms into a single string (as used during training)
        symptom_text = ' '.join(symptoms).lower()
        
        # Transform using TF-IDF vectorizer
        feature_vector = self.vectorizer.transform([symptom_text])
        
        # Convert to dense array (required by XGBoost)
        feature_vector = feature_vector.toarray()
        
        return feature_vector
    
    def predict_diseases(self, symptoms, model_type='xgboost', top_k=5):
        """
        Predict diseases from symptoms.
        
        Args:
            symptoms (list): List of symptom strings
            model_type (str): 'xgboost' or 'random_forest'
            top_k (int): Number of top predictions to return
        
        Returns:
            dict: Prediction results with diseases and confidence scores
        """
        if not self.model_loaded:
            self.load_models()
        
        # Select model
        if model_type == 'xgboost':
            model = self.xgboost_model
        elif model_type == 'random_forest' and self.random_forest_model:
            model = self.random_forest_model
        else:
            model = self.xgboost_model  # Default to XGBoost
        
        # Preprocess symptoms
        feature_vector = self.preprocess_symptoms(symptoms)
        
        # Make prediction
        # For MultiOutputClassifier, predict_proba returns a list of arrays
        # Each array contains [prob_class_0, prob_class_1] for that label
        proba_list = model.predict_proba(feature_vector)
        
        # Extract probabilities for positive class (class 1) for each disease
        # Convert list of arrays to a single array of probabilities
        probabilities = np.array([proba[0][1] if proba[0].shape[0] > 1 else proba[0][0] 
                                  for proba in proba_list])
        
        # Get disease names
        if not self.disease_names:
            with open(self.diseases_file, 'r') as f:
                self.disease_names = [line.strip() for line in f.readlines()]
        
        # Create predictions with confidence scores
        predictions = []
        for i, prob in enumerate(probabilities):
            if prob > 0.01:  # Only include diseases with >1% probability
                predictions.append({
                    'disease': self.disease_names[i],
                    'confidence': float(prob)
                })
        
        # Sort by confidence and get top_k
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        top_predictions = predictions[:top_k]
        
        return {
            'predictions': top_predictions,
            'model_used': model_type,
            'symptoms': symptoms,
            'total_predictions': len(predictions)
        }
    
    def is_available(self):
        """Check if ML models are available."""
        return self.xgboost_model_file.exists()


# Global instance (singleton pattern)
_ml_service = None


def get_ml_service():
    """
    Get global ML service instance.
    
    Returns:
        MLPredictionService: ML service instance
    """
    global _ml_service
    if _ml_service is None:
        _ml_service = MLPredictionService()
    return _ml_service

