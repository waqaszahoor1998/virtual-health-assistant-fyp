"""
Machine Learning Service — inference for the Flask API.

Flow (high level):
  1) API routes in app/api/diagnosis.py call get_ml_service().
  2) Symptoms (list of strings) are joined and fed through the same
     TfidfVectorizer saved during training (symptom_vectorizer.pkl).
  3) The loaded classifier (default: LightGBM in MultiOutputClassifier)
     outputs per-disease probabilities; we sort and return top_k.

Artifacts live under ml_models/models/ at the repository root. Flask sets
ML_MODELS_DIR in config.py; the fallback path below uses parents[3] so it
resolves to the repo root even when current_app is not yet bound.
"""

import joblib
import numpy as np
from pathlib import Path
import json
from flask import current_app
import os
import hashlib

# backend/app/utils/ml_service.py -> parents[3] == repository root
_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_MODELS_DIR = _REPO_ROOT / "ml_models" / "models"


class MLPredictionService:
    """
    Loads vectorizer + classifier pickles and runs predict_proba for multi-label
    disease scoring. Optional XGBoost/Random Forest if matching .pkl files exist.
    """

    def __init__(self):
        """Resolve models directory (Flask config or repo-root ml_models/models)."""
        self.models_dir = Path(
            current_app.config.get("ML_MODELS_DIR", _DEFAULT_MODELS_DIR)
        )
        
        # Primary API model (train with ml_models/scripts/train_lightgbm.py)
        self.lightgbm_model_file = self.models_dir / 'lightgbm_model.pkl'
        self.xgboost_model_file = self.models_dir / 'xgboost_model.pkl'
        self.random_forest_model_file = self.models_dir / 'random_forest_model.pkl'
        self.vectorizer_file = self.models_dir / 'symptom_vectorizer.pkl'
        self.encoder_file = self.models_dir / 'disease_encoder.pkl'
        self.diseases_file = self.models_dir / 'unique_diseases.txt'
        
        # Loaded components (lazy loading)
        self.lightgbm_model = None
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
            if not self.lightgbm_model_file.exists():
                raise FileNotFoundError(
                    f"LightGBM model not found at {self.lightgbm_model_file}.\n"
                    "Please train models first using ml_models/scripts/train_lightgbm.py"
                )
            
            print(f"Loading ML models from {self.models_dir}...")
            
            self.lightgbm_model = joblib.load(self.lightgbm_model_file)
            print("✓ Loaded LightGBM model")
            
            # Load XGBoost model (optional, for comparison)
            if self.xgboost_model_file.exists():
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
    
    def predict_diseases(self, symptoms, model_type='lightgbm', top_k=5):
        """
        Predict diseases from symptoms.
        
        Args:
            symptoms (list): List of symptom strings
            model_type (str): 'lightgbm', 'xgboost', or 'random_forest'
            top_k (int): Number of top predictions to return
        
        Returns:
            dict: Prediction results with diseases and confidence scores
        """
        if not self.model_loaded:
            try:
                self.load_models()
            except Exception:
                if os.environ.get("DEMO_ML_FALLBACK") == "1":
                    return self._demo_predict(symptoms=symptoms, top_k=top_k)
                raise
        
        # Select model
        if model_type == 'lightgbm':
            model = self.lightgbm_model
        elif model_type == 'xgboost' and self.xgboost_model:
            model = self.xgboost_model
        elif model_type == 'random_forest' and self.random_forest_model:
            model = self.random_forest_model
        else:
            model = self.lightgbm_model  # Default to LightGBM (best model)
        
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
        if self.lightgbm_model_file.exists():
            return True
        return os.environ.get("DEMO_ML_FALLBACK") == "1"

    def _demo_predict(self, symptoms, top_k=5):
        symptom_text = " ".join([str(s).strip().lower() for s in symptoms if str(s).strip()])
        if not symptom_text:
            symptom_text = "unknown"

        buckets = [
            ("Migraine", ["headache", "nausea", "light", "photophobia", "sensitivity"]),
            ("Influenza", ["fever", "cough", "chills", "body", "fatigue", "sore"]),
            ("Gastroenteritis", ["vomiting", "diarrhea", "stomach", "abdominal", "cramp"]),
            ("Allergic Rhinitis", ["sneezing", "runny", "itchy", "watery", "allergy"]),
            ("Common Cold", ["cold", "congestion", "sneezing", "sore throat", "runny"]),
        ]

        scored = []
        for disease, keywords in buckets:
            score = sum(1 for k in keywords if k in symptom_text)
            scored.append((disease, score))

        if max(s for _, s in scored) == 0:
            h = int(hashlib.sha256(symptom_text.encode("utf-8")).hexdigest(), 16)
            chosen = buckets[h % len(buckets)][0]
            ordered = [chosen] + [d for d, _ in scored if d != chosen]
        else:
            ordered = [d for d, _ in sorted(scored, key=lambda x: x[1], reverse=True)]

        predictions = []
        for i, disease in enumerate(ordered[: max(1, int(top_k))]):
            confidence = float(max(0.15, 0.85 - (i * 0.18)))
            predictions.append({"disease": disease, "confidence": confidence})

        return {
            "predictions": predictions[:top_k],
            "model_used": "demo_fallback",
            "symptoms": symptoms,
            "total_predictions": len(predictions),
        }


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

