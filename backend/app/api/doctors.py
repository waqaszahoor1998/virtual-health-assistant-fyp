"""
Doctor API endpoints.

Handles CRUD operations for doctor management.
Requires authentication and appropriate role permissions.
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app import db
from app.models.user import User
from app.models.doctor import Doctor


@api_bp.route('/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    """
    Get list of doctors.
    
    Query parameters:
    - page (int): Page number for pagination (default: 1)
    - per_page (int): Items per page (default: 20)
    - search (str): Search by name, specialization, or license
    - specialization (str): Filter by specialization
    
    Returns:
        JSON response with list of doctors
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        specialization = request.args.get('specialization', '').strip()
        
        # Build query
        query = Doctor.query
        
        # Apply search filter
        if search:
            query = query.filter(
                db.or_(
                    Doctor.first_name.ilike(f'%{search}%'),
                    Doctor.last_name.ilike(f'%{search}%'),
                    Doctor.specialization.ilike(f'%{search}%'),
                    Doctor.license_number.ilike(f'%{search}%')
                )
            )
        
        # Apply specialization filter
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
        
        # Paginate results
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'doctors': [d.to_dict() for d in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get doctors: {str(e)}'}), 500


@api_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor(doctor_id):
    """
    Get doctor by ID.
    
    Args:
        doctor_id (int): Doctor ID
    
    Returns:
        JSON response with doctor data
    """
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        return jsonify(doctor.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get doctor: {str(e)}'}), 500


@api_bp.route('/doctors', methods=['POST'])
@jwt_required()
def create_doctor():
    """
    Create a new doctor profile.
    
    Only users with doctor role can create doctor profiles.
    Expected JSON payload:
    {
        "first_name": "Dr. Jane",
        "last_name": "Smith",
        "specialization": "Cardiology",
        "license_number": "LIC12345",
        "phone": "1234567890",
        "hospital_clinic": "City Hospital",
        "address": "123 Medical St"
    }
    
    Returns:
        JSON response with created doctor data
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Only doctors can create their own profile
        if current_user.role != 'doctor':
            return jsonify({'error': 'Only doctors can create doctor profiles'}), 403
        
        # Check if profile already exists
        existing_doctor = Doctor.query.filter_by(user_id=user_id).first()
        if existing_doctor:
            return jsonify({'error': 'Doctor profile already exists'}), 409
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create doctor profile
        new_doctor = Doctor(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            specialization=data.get('specialization'),
            license_number=data.get('license_number'),
            phone=data.get('phone'),
            hospital_clinic=data.get('hospital_clinic'),
            address=data.get('address')
        )
        
        # Save to database
        db.session.add(new_doctor)
        db.session.commit()
        
        return jsonify({
            'message': 'Doctor profile created successfully',
            'doctor': new_doctor.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create doctor: {str(e)}'}), 500


@api_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def update_doctor(doctor_id):
    """
    Update doctor profile.
    
    Args:
        doctor_id (int): Doctor ID
    
    Expected JSON payload (all fields optional):
    {
        "first_name": "Dr. Jane",
        "specialization": "Cardiology",
        ...
    }
    
    Returns:
        JSON response with updated doctor data
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get doctor
        doctor = Doctor.query.get_or_404(doctor_id)
        
        # Check permissions (doctors can only update their own profile)
        if current_user.role == 'doctor' and doctor.user_id != user_id:
            return jsonify({'error': 'Unauthorized to update this doctor'}), 403
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        updateable_fields = [
            'first_name', 'last_name', 'specialization', 'license_number',
            'phone', 'hospital_clinic', 'address'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(doctor, field, data[field])
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'message': 'Doctor profile updated successfully',
            'doctor': doctor.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update doctor: {str(e)}'}), 500


@api_bp.route('/doctors/<int:doctor_id>/patients', methods=['GET'])
@jwt_required()
def get_doctor_patients(doctor_id):
    """
    Get all patients for a specific doctor.
    
    This includes patients who have appointments or diagnoses with this doctor.
    
    Args:
        doctor_id (int): Doctor ID
    
    Returns:
        JSON response with list of patients
    """
    try:
        # Verify doctor exists
        doctor = Doctor.query.get_or_404(doctor_id)
        
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        # Check permissions
        if current_user.role == 'doctor' and doctor.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Import models
        from app.models.diagnosis import Diagnosis
        from app.models.appointment import Appointment
        
        # Get unique patient IDs from diagnoses and appointments
        diagnosis_patient_ids = db.session.query(Diagnosis.patient_id).filter_by(doctor_id=doctor_id).distinct().all()
        appointment_patient_ids = db.session.query(Appointment.patient_id).filter_by(doctor_id=doctor_id).distinct().all()
        
        # Combine and get unique patient IDs
        patient_ids = set()
        for (pid,) in diagnosis_patient_ids:
            patient_ids.add(pid)
        for (pid,) in appointment_patient_ids:
            patient_ids.add(pid)
        
        # Get patients
        from app.models.patient import Patient
        patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()
        
        return jsonify({
            'doctor_id': doctor_id,
            'patients': [p.to_dict() for p in patients],
            'total': len(patients)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get doctor patients: {str(e)}'}), 500
