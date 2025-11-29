"""
Prescription API endpoints.

Handles CRUD operations for prescriptions issued by doctors to patients.
Requires authentication and doctor role for creating prescriptions.
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app import db
from app.models.user import User
from app.models.prescription import Prescription
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.diagnosis import Diagnosis


@api_bp.route('/prescriptions', methods=['POST'])
@jwt_required()
def create_prescription():
    """
    Create a new prescription.
    
    Allows doctors to create prescriptions for patients based on a diagnosis.
    Validates that the doctor is authorized and the patient/diagnosis exist.
    
    Expected JSON payload:
    {
        "diagnosis_id": 1,
        "patient_id": 1,
        "drugbank_id": "DB00001",
        "drug_name": "Aspirin",
        "dosage": "500mg",
        "frequency": "Twice daily",
        "duration": "7 days",
        "instructions": "Take with food"
    }
    
    Returns:
        JSON response with created prescription data (201 Created)
    
    Error Responses:
        - 400: Bad request (missing required fields or invalid data)
        - 401: Unauthorized (missing or invalid JWT token)
        - 403: Forbidden (user is not a doctor)
        - 404: Not found (patient, doctor, or diagnosis not found)
        - 500: Internal server error
    """
    try:
        # Get current user from JWT token
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Only doctors can create prescriptions
        if current_user.role != 'doctor':
            return jsonify({'error': 'Only doctors can create prescriptions'}), 403
        
        # Get doctor profile
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['diagnosis_id', 'patient_id', 'drugbank_id', 'drug_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify diagnosis exists
        diagnosis_id = data['diagnosis_id']
        diagnosis = Diagnosis.query.get(diagnosis_id)
        if not diagnosis:
            return jsonify({'error': 'Diagnosis not found'}), 404
        
        # Verify patient exists
        patient_id = data['patient_id']
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Verify diagnosis belongs to patient
        if diagnosis.patient_id != patient_id:
            return jsonify({'error': 'Diagnosis does not belong to specified patient'}), 400
        
        # Create prescription record
        new_prescription = Prescription(
            diagnosis_id=diagnosis_id,
            patient_id=patient_id,
            doctor_id=doctor.id,
            drugbank_id=data['drugbank_id'],
            drug_name=data['drug_name'],
            dosage=data.get('dosage'),
            frequency=data.get('frequency'),
            duration=data.get('duration'),
            instructions=data.get('instructions')
        )
        
        # Save to database
        db.session.add(new_prescription)
        db.session.commit()
        
        return jsonify({
            'message': 'Prescription created successfully',
            'prescription': new_prescription.to_dict()
        }), 201
    
    except Exception as e:
        # Rollback database transaction on error
        db.session.rollback()
        return jsonify({'error': f'Failed to create prescription: {str(e)}'}), 500


@api_bp.route('/prescriptions/<int:prescription_id>', methods=['GET'])
@jwt_required()
def get_prescription(prescription_id):
    """
    Get prescription by ID.
    
    Retrieves a specific prescription by its ID. Patients can only view
    their own prescriptions, while doctors can view all prescriptions.
    
    Args:
        prescription_id (int): Prescription ID
    
    Returns:
        JSON response with prescription data (200 OK)
    
    Error Responses:
        - 401: Unauthorized
        - 403: Forbidden (patient trying to view another patient's prescription)
        - 404: Not found (prescription doesn't exist)
        - 500: Internal server error
    """
    try:
        # Get prescription
        prescription = Prescription.query.get_or_404(prescription_id)
        
        # Get current user for permission check
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check permissions based on user role
        if current_user.role == 'patient':
            # Patients can only view their own prescriptions
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient or prescription.patient_id != patient.id:
                return jsonify({'error': 'Unauthorized - cannot view this prescription'}), 403
        # Doctors can view all prescriptions (no additional check needed)
        
        return jsonify(prescription.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get prescription: {str(e)}'}), 500


@api_bp.route('/prescriptions/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_prescriptions(patient_id):
    """
    Get all prescriptions for a specific patient.
    
    Retrieves all prescriptions issued to a patient. Patients can only view
    their own prescriptions, while doctors can view all patients' prescriptions.
    
    Args:
        patient_id (int): Patient ID
    
    Query Parameters:
        limit (int): Maximum number of results (default: 20)
        offset (int): Number of results to skip (default: 0)
    
    Returns:
        JSON response with list of prescriptions (200 OK)
    
    Error Responses:
        - 401: Unauthorized
        - 403: Forbidden (patient trying to view another patient's prescriptions)
        - 404: Not found (patient doesn't exist)
        - 500: Internal server error
    """
    try:
        # Verify patient exists
        patient = Patient.query.get_or_404(patient_id)
        
        # Get current user for permission check
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check permissions
        if current_user.role == 'patient':
            # Patients can only view their own prescriptions
            patient_user = Patient.query.filter_by(user_id=user_id).first()
            if not patient_user or patient_user.id != patient_id:
                return jsonify({'error': 'Unauthorized - cannot view this patient\'s prescriptions'}), 403
        # Doctors can view all patients' prescriptions
        
        # Get pagination parameters
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Query prescriptions for patient
        prescriptions = Prescription.query.filter_by(patient_id=patient_id)\
            .order_by(Prescription.created_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        # Convert to dictionaries
        prescriptions_list = [prescription.to_dict() for prescription in prescriptions]
        
        return jsonify({
            'patient_id': patient_id,
            'count': len(prescriptions_list),
            'prescriptions': prescriptions_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get patient prescriptions: {str(e)}'}), 500

