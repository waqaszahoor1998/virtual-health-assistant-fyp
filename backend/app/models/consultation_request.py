"""
Consultation request from patient to doctor (simple messaging / second opinion).
"""

from datetime import datetime
from app import db


class ConsultationRequest(db.Model):
    __tablename__ = 'consultation_requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True, index=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='open', nullable=False)
    doctor_response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'subject': self.subject,
            'message': self.message,
            'symptoms': self.symptoms,
            'status': self.status,
            'doctor_response': self.doctor_response,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
