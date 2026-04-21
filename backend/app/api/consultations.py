"""
Consultation requests: patient asks a doctor; doctor responds.
"""

import json as json_lib
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app import db
from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.consultation_request import ConsultationRequest


@api_bp.route('/consultations', methods=['POST'])
@jwt_required()
def create_consultation():
    try:
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        if current_user.role != 'patient':
            return jsonify({'error': 'Only patients can create consultation requests'}), 403

        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        subject = (data.get('subject') or '').strip()
        message = (data.get('message') or '').strip()
        if not subject or not message:
            return jsonify({'error': 'subject and message are required'}), 400

        doctor_id = data.get('doctor_id')
        if doctor_id is not None:
            doctor_id = int(doctor_id)
            if not Doctor.query.get(doctor_id):
                return jsonify({'error': 'Doctor not found'}), 404

        symptoms = data.get('symptoms')
        symptoms_json = None
        if symptoms is not None:
            if not isinstance(symptoms, list):
                return jsonify({'error': 'symptoms must be a list when provided'}), 400
            symptoms_json = json_lib.dumps(symptoms)

        req = ConsultationRequest(
            patient_id=patient.id,
            doctor_id=doctor_id,
            subject=subject,
            message=message,
            symptoms=symptoms_json,
            status='open',
        )
        db.session.add(req)
        db.session.commit()

        return jsonify({'message': 'Consultation request created', 'consultation': req.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/consultations', methods=['GET'])
@jwt_required()
def list_consultations():
    try:
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        if current_user.role == 'patient':
            patient = Patient.query.filter_by(user_id=user_id).first()
            if not patient:
                return jsonify({'consultations': [], 'total': 0}), 200
            q = ConsultationRequest.query.filter_by(patient_id=patient.id)
        elif current_user.role == 'doctor':
            doctor = Doctor.query.filter_by(user_id=user_id).first()
            if not doctor:
                return jsonify({'consultations': [], 'total': 0}), 200
            q = ConsultationRequest.query.filter(
                (ConsultationRequest.doctor_id == doctor.id) | (ConsultationRequest.doctor_id.is_(None))
            )
        else:
            return jsonify({'error': 'Unauthorized'}), 403

        consultations = q.order_by(ConsultationRequest.created_at.desc()).all()
        return jsonify({
            'consultations': [c.to_dict() for c in consultations],
            'total': len(consultations),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/consultations/<int:consultation_id>/respond', methods=['PUT'])
@jwt_required()
def respond_consultation(consultation_id):
    try:
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'doctor':
            return jsonify({'error': 'Only doctors can respond'}), 403

        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404

        req = ConsultationRequest.query.get_or_404(consultation_id)
        if req.doctor_id is not None and req.doctor_id != doctor.id:
            return jsonify({'error': 'This request is assigned to another doctor'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        response_text = (data.get('doctor_response') or '').strip()
        if not response_text:
            return jsonify({'error': 'doctor_response is required'}), 400

        status = data.get('status', 'answered')
        if status not in ('answered', 'closed'):
            return jsonify({'error': 'Invalid status'}), 400

        req.doctor_id = doctor.id
        req.doctor_response = response_text
        req.status = status
        db.session.commit()

        return jsonify({'message': 'Response saved', 'consultation': req.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
