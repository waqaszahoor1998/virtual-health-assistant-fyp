"""Prescription model for storing prescription information."""

from datetime import datetime
from app import db


class Prescription(db.Model):
    """Prescription model representing patient prescriptions."""
    
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # Prescription details
    drugbank_id = db.Column(db.String(50), nullable=False)
    drug_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=True)
    frequency = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.String(100), nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert Prescription object to dictionary."""
        return {
            'id': self.id,
            'diagnosis_id': self.diagnosis_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'drugbank_id': self.drugbank_id,
            'drug_name': self.drug_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'duration': self.duration,
            'instructions': self.instructions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

