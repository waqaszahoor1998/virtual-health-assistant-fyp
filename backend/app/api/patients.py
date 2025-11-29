"""
Patient API endpoints.

Handles CRUD operations for patient management.
Requires authentication and appropriate role permissions.
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app import db
from app.models.user import User
from app.models.patient import Patient


@api_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    """
    Get list of patients.
    
    For doctors: Returns all patients
    For patients: Returns only their own profile
    
    Query parameters:
    - page (int): Page number for pagination (default: 1)
    - per_page (int): Items per page (default: 20)
    - search (str): Search by name or email
    
    Returns:
        JSON response with list of patients
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        
        # Build query based on user role
        if current_user.role == 'patient':
            # Patients can only see their own profile
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient:
                return jsonify({
                    'patients': [],
                    'total': 0,
                    'page': page,
                    'per_page': per_page
                }), 200
            
            return jsonify({
                'patients': [patient.to_dict()],
                'total': 1,
                'page': 1,
                'per_page': 1
            }), 200
        
        elif current_user.role == 'doctor':
            # Doctors can see all patients
            query = Patient.query
            
            # Apply search filter if provided
            if search:
                # Search in patient names only (email is in User table, would need join)
                query = query.filter(
                    db.or_(
                        Patient.first_name.ilike(f'%{search}%'),
                        Patient.last_name.ilike(f'%{search}%'),
                        Patient.phone.ilike(f'%{search}%')
                    )
                )
            
            # Paginate results
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return jsonify({
                'patients': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }), 200
        
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    
    except Exception as e:
        return jsonify({'error': f'Failed to get patients: {str(e)}'}), 500


@api_bp.route('/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    """
    Get patient by ID.
    
    Args:
        patient_id (int): Patient ID
    
    Returns:
        JSON response with patient data
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get patient
        patient = Patient.query.get_or_404(patient_id)
        
        # Check permissions
        if current_user.role == 'patient':
            # Patients can only view their own profile
            if patient.user_id != user_id:
                return jsonify({'error': 'Unauthorized to view this patient'}), 403
        
        # Doctors can view any patient
        return jsonify(patient.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get patient: {str(e)}'}), 500


@api_bp.route('/patients', methods=['POST'])
@jwt_required()
def create_patient():
    """
    Create a new patient profile.
    
    Only patients can create their own profile.
    Expected JSON payload:
    {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "phone": "1234567890",
        "address": "123 Main St",
        "blood_type": "O+",
        "allergies": "Peanuts, Penicillin"
    }
    
    Returns:
        JSON response with created patient data
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Only patients can create their own profile
        if current_user.role != 'patient':
            return jsonify({'error': 'Only patients can create patient profiles'}), 403
        
        # Check if profile already exists
        existing_patient = Patient.query.filter_by(user_id=user_id).first()
        if existing_patient:
            return jsonify({'error': 'Patient profile already exists'}), 409
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create patient profile
        new_patient = Patient(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            phone=data.get('phone'),
            address=data.get('address'),
            blood_type=data.get('blood_type'),
            allergies=data.get('allergies')
        )
        
        # Save to database
        db.session.add(new_patient)
        db.session.commit()
        
        return jsonify({
            'message': 'Patient profile created successfully',
            'patient': new_patient.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create patient: {str(e)}'}), 500


@api_bp.route('/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    """
    Update patient profile.
    
    Args:
        patient_id (int): Patient ID
    
    Expected JSON payload (all fields optional):
    {
        "first_name": "John",
        "last_name": "Doe",
        ...
    }
    
    Returns:
        JSON response with updated patient data
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get patient
        patient = Patient.query.get_or_404(patient_id)
        
        # Check permissions
        if current_user.role == 'patient':
            # Patients can only update their own profile
            if patient.user_id != user_id:
                return jsonify({'error': 'Unauthorized to update this patient'}), 403
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        updateable_fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone', 'address', 'blood_type', 'allergies', 'medical_history'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(patient, field, data[field])
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'message': 'Patient profile updated successfully',
            'patient': patient.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update patient: {str(e)}'}), 500


@api_bp.route('/patients/<int:patient_id>/history', methods=['GET'])
@jwt_required()
def get_patient_history(patient_id):
    """
    Get patient medical history.
    
    Includes diagnoses, prescriptions, and appointments.
    
    Args:
        patient_id (int): Patient ID
    
    Returns:
        JSON response with patient history
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get patient
        patient = Patient.query.get_or_404(patient_id)
        
        # Check permissions
        if current_user.role == 'patient':
            if patient.user_id != user_id:
                return jsonify({'error': 'Unauthorized'}), 403
        
        # Import models for history
        from app.models.diagnosis import Diagnosis
        from app.models.prescription import Prescription
        from app.models.appointment import Appointment
        
        # Get history data
        diagnoses = Diagnosis.query.filter_by(patient_id=patient_id).order_by(Diagnosis.created_at.desc()).all()
        prescriptions = Prescription.query.filter_by(patient_id=patient_id).order_by(Prescription.created_at.desc()).all()
        appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.appointment_date.desc()).all()
        
        return jsonify({
            'patient_id': patient_id,
            'diagnoses': [d.to_dict() for d in diagnoses],
            'prescriptions': [p.to_dict() for p in prescriptions],
            'appointments': [a.to_dict() for a in appointments]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get patient history: {str(e)}'}), 500
