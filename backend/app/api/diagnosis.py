"""
Diagnosis API endpoints.

Handles disease prediction from symptoms using ML models.
Requires authentication and doctor role for creating diagnoses.
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app import db
from app.models.user import User
from app.models.diagnosis import Diagnosis
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.utils.ml_service import get_ml_service


@api_bp.route('/diagnosis/predict', methods=['POST'])
@jwt_required()
def predict_diagnosis():
    """
    Predict diseases from symptoms using ML model.
    
    Expected JSON payload:
    {
        "symptoms": ["fever", "headache", "nausea"],
        "model_type": "xgboost" (optional, defaults to "xgboost"),
        "top_k": 5 (optional, number of predictions to return)
    }
    
    Returns:
        JSON response with predicted diseases and confidence scores
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Only doctors can use prediction
        if current_user.role != 'doctor':
            return jsonify({'error': 'Only doctors can use diagnosis prediction'}), 403
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'symptoms' not in data:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        symptoms = data['symptoms']
        
        # Validate symptoms
        if not isinstance(symptoms, list):
            return jsonify({'error': 'Symptoms must be a list'}), 400
        
        if len(symptoms) == 0:
            return jsonify({'error': 'At least one symptom is required'}), 400
        
        if len(symptoms) > 20:
            return jsonify({'error': 'Maximum 20 symptoms allowed'}), 400
        
        # Get ML service and check availability
        ml_service = get_ml_service()
        
        if not ml_service.is_available():
            return jsonify({
                'error': 'ML models not available. Please train models first.',
                'instructions': 'Run ml_models/scripts/feature_engineering.py and train_xgboost.py'
            }), 503
        
        # Get prediction parameters
        model_type = data.get('model_type', 'xgboost')
        top_k = data.get('top_k', 5)
        
        # Make prediction
        try:
            prediction_result = ml_service.predict_diseases(
                symptoms=symptoms,
                model_type=model_type,
                top_k=top_k
            )
            
            return jsonify({
                'success': True,
                'prediction': prediction_result
            }), 200
        
        except Exception as e:
            return jsonify({
                'error': f'Prediction failed: {str(e)}'
            }), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to predict diagnosis: {str(e)}'}), 500


@api_bp.route('/diagnosis', methods=['POST'])
@jwt_required()
def create_diagnosis():
    """
    Create a diagnosis record.
    
    Expected JSON payload:
    {
        "patient_id": 1,
        "symptoms": ["fever", "headache"],
        "predicted_diseases": [{"disease": "Migraine", "confidence": 0.85}],
        "confirmed_disease": "Migraine" (optional),
        "notes": "Patient complains of severe headache..." (optional)
    }
    
    Returns:
        JSON response with created diagnosis
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Only doctors can create diagnoses
        if current_user.role != 'doctor':
            return jsonify({'error': 'Only doctors can create diagnoses'}), 403
        
        # Get doctor profile
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['patient_id', 'symptoms']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify patient exists
        patient_id = data['patient_id']
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Create diagnosis record
        import json as json_lib
        new_diagnosis = Diagnosis(
            patient_id=patient_id,
            doctor_id=doctor.id,
            symptoms=json_lib.dumps(data['symptoms']),
            predicted_diseases=json_lib.dumps(data.get('predicted_diseases', [])),
            confirmed_disease=data.get('confirmed_disease'),
            notes=data.get('notes')
        )
        
        # Save to database
        db.session.add(new_diagnosis)
        db.session.commit()
        
        return jsonify({
            'message': 'Diagnosis created successfully',
            'diagnosis': new_diagnosis.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create diagnosis: {str(e)}'}), 500


@api_bp.route('/diagnosis/<int:diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis(diagnosis_id):
    """
    Get diagnosis by ID.
    
    Args:
        diagnosis_id (int): Diagnosis ID
    
    Returns:
        JSON response with diagnosis data
    """
    try:
        diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
        
        # Get current user for permission check
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        # Check permissions
        if current_user.role == 'patient':
            # Patients can only view their own diagnoses
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient or diagnosis.patient_id != patient.id:
                return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(diagnosis.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get diagnosis: {str(e)}'}), 500
