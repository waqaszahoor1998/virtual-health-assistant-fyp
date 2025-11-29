"""
Appointment API endpoints.

Handles CRUD operations for appointment scheduling between patients and doctors.
Requires authentication and appropriate role permissions.
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.api import api_bp
from app import db
from app.models.user import User
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor


@api_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    """
    Create a new appointment.
    
    Allows patients to schedule appointments with doctors, or doctors to
    schedule appointments for their patients. Validates that both patient
    and doctor exist and are valid.
    
    Expected JSON payload:
    {
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_date": "2024-03-15T14:30:00",
        "reason": "Follow-up for previous diagnosis",
        "notes": "Patient requested morning appointment"
    }
    
    Returns:
        JSON response with created appointment data (201 Created)
    
    Error Responses:
        - 400: Bad request (missing required fields or invalid date)
        - 401: Unauthorized (missing or invalid JWT token)
        - 403: Forbidden (patient trying to create appointment for another patient)
        - 404: Not found (patient or doctor not found)
        - 500: Internal server error
    """
    try:
        # Get current user from JWT token
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['patient_id', 'doctor_id', 'appointment_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Permission check: Patients can only create appointments for themselves
        if current_user.role == 'patient':
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient or patient.id != data['patient_id']:
                return jsonify({'error': 'Patients can only create appointments for themselves'}), 403
        
        # Verify patient exists
        patient_id = data['patient_id']
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Verify doctor exists
        doctor_id = data['doctor_id']
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        # Parse appointment date
        try:
            appointment_date = datetime.fromisoformat(data['appointment_date'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid appointment_date format. Use ISO format: YYYY-MM-DDTHH:MM:SS'}), 400
        
        # Validate appointment is in the future
        if appointment_date < datetime.utcnow():
            return jsonify({'error': 'Appointment date must be in the future'}), 400
        
        # Create appointment record
        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            status='scheduled',
            reason=data.get('reason'),
            notes=data.get('notes')
        )
        
        # Save to database
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': new_appointment.to_dict()
        }), 201
    
    except Exception as e:
        # Rollback database transaction on error
        db.session.rollback()
        return jsonify({'error': f'Failed to create appointment: {str(e)}'}), 500


@api_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    """
    Get list of appointments.
    
    Retrieves appointments based on user role:
    - Patients: See only their own appointments
    - Doctors: See only their appointments with patients
    
    Query Parameters:
        patient_id (int): Filter by patient ID (doctors only)
        doctor_id (int): Filter by doctor ID (optional)
        status (str): Filter by status ('scheduled', 'completed', 'cancelled')
        date_from (str): Filter appointments from date (ISO format)
        date_to (str): Filter appointments to date (ISO format)
        page (int): Page number for pagination (default: 1)
        per_page (int): Items per page (default: 20)
    
    Returns:
        JSON response with list of appointments (200 OK)
    """
    try:
        # Get current user
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Build query based on user role
        if current_user.role == 'patient':
            # Patients can only see their own appointments
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient:
                return jsonify({
                    'appointments': [],
                    'total': 0,
                    'page': 1,
                    'per_page': 20
                }), 200
            
            query = Appointment.query.filter_by(patient_id=patient.id)
        
        elif current_user.role == 'doctor':
            # Doctors can see their appointments with patients
            doctor = Doctor.query.filter_by(user_id=user_id).first()
            if not doctor:
                return jsonify({
                    'appointments': [],
                    'total': 0,
                    'page': 1,
                    'per_page': 20
                }), 200
            
            query = Appointment.query.filter_by(doctor_id=doctor.id)
            
            # Optional: Filter by specific patient (doctor viewing one patient's appointments)
            patient_id_filter = request.args.get('patient_id', type=int)
            if patient_id_filter:
                query = query.filter_by(patient_id=patient_id_filter)
        else:
            return jsonify({'error': 'Invalid user role'}), 400
        
        # Apply filters
        status_filter = request.args.get('status')
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        date_from = request.args.get('date_from')
        if date_from:
            try:
                date_from_dt = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                query = query.filter(Appointment.appointment_date >= date_from_dt)
            except (ValueError, AttributeError):
                return jsonify({'error': 'Invalid date_from format'}), 400
        
        date_to = request.args.get('date_to')
        if date_to:
            try:
                date_to_dt = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                query = query.filter(Appointment.appointment_date <= date_to_dt)
            except (ValueError, AttributeError):
                return jsonify({'error': 'Invalid date_to format'}), 400
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Order by appointment date (upcoming first)
        query = query.order_by(Appointment.appointment_date.asc())
        
        # Paginate results
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Convert to dictionaries
        appointments_list = [appointment.to_dict() for appointment in pagination.items]
        
        return jsonify({
            'appointments': appointments_list,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get appointments: {str(e)}'}), 500


@api_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    """
    Get appointment by ID.
    
    Retrieves a specific appointment by its ID. Patients can only view
    their own appointments, while doctors can view their appointments.
    
    Args:
        appointment_id (int): Appointment ID
    
    Returns:
        JSON response with appointment data (200 OK)
    
    Error Responses:
        - 401: Unauthorized
        - 403: Forbidden (user trying to view appointment they don't have access to)
        - 404: Not found (appointment doesn't exist)
        - 500: Internal server error
    """
    try:
        # Get appointment
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Get current user for permission check
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check permissions based on user role
        if current_user.role == 'patient':
            # Patients can only view their own appointments
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient or appointment.patient_id != patient.id:
                return jsonify({'error': 'Unauthorized - cannot view this appointment'}), 403
        elif current_user.role == 'doctor':
            # Doctors can only view their own appointments
            doctor = Doctor.query.filter_by(user_id=user_id).first()
            if not doctor or appointment.doctor_id != doctor.id:
                return jsonify({'error': 'Unauthorized - cannot view this appointment'}), 403
        
        return jsonify(appointment.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get appointment: {str(e)}'}), 500


@api_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    """
    Update an existing appointment.
    
    Allows updating appointment status, date, reason, or notes.
    Only the doctor or patient associated with the appointment can update it.
    
    Expected JSON payload (all fields optional):
    {
        "appointment_date": "2024-03-15T14:30:00",
        "status": "completed",
        "reason": "Updated reason",
        "notes": "Updated notes"
    }
    
    Args:
        appointment_id (int): Appointment ID
    
    Returns:
        JSON response with updated appointment data (200 OK)
    
    Error Responses:
        - 400: Bad request (invalid data)
        - 401: Unauthorized
        - 403: Forbidden (user not authorized to update this appointment)
        - 404: Not found (appointment doesn't exist)
        - 500: Internal server error
    """
    try:
        # Get appointment
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Get current user for permission check
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check permissions
        can_update = False
        if current_user.role == 'patient':
            patient = Patient.query.filter_by(user_id=user_id).first()
            if patient and appointment.patient_id == patient.id:
                can_update = True
        elif current_user.role == 'doctor':
            doctor = Doctor.query.filter_by(user_id=user_id).first()
            if doctor and appointment.doctor_id == doctor.id:
                can_update = True
        
        if not can_update:
            return jsonify({'error': 'Unauthorized - cannot update this appointment'}), 403
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'appointment_date' in data:
            try:
                appointment.appointment_date = datetime.fromisoformat(data['appointment_date'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return jsonify({'error': 'Invalid appointment_date format'}), 400
        
        if 'status' in data:
            valid_statuses = ['scheduled', 'completed', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
            appointment.status = data['status']
        
        if 'reason' in data:
            appointment.reason = data['reason']
        
        if 'notes' in data:
            appointment.notes = data['notes']
        
        # Save changes
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update appointment: {str(e)}'}), 500


@api_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    """
    Delete an appointment.
    
    Allows cancelling/deleting an appointment. Only the doctor or patient
    associated with the appointment can delete it.
    
    Args:
        appointment_id (int): Appointment ID
    
    Returns:
        JSON response with success message (200 OK)
    
    Error Responses:
        - 401: Unauthorized
        - 403: Forbidden (user not authorized to delete this appointment)
        - 404: Not found (appointment doesn't exist)
        - 500: Internal server error
    """
    try:
        # Get appointment
        appointment = Appointment.query.get_or_404(appointment_id)
        
        # Get current user for permission check
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check permissions
        can_delete = False
        if current_user.role == 'patient':
            patient = Patient.query.filter_by(user_id=user_id).first()
            if patient and appointment.patient_id == patient.id:
                can_delete = True
        elif current_user.role == 'doctor':
            doctor = Doctor.query.filter_by(user_id=user_id).first()
            if doctor and appointment.doctor_id == doctor.id:
                can_delete = True
        
        if not can_delete:
            return jsonify({'error': 'Unauthorized - cannot delete this appointment'}), 403
        
        # Delete appointment
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete appointment: {str(e)}'}), 500

