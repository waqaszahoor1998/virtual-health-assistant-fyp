"""Diagnosis model for storing diagnosis records."""

from datetime import datetime
from app import db


class Diagnosis(db.Model):
    """Diagnosis model representing patient diagnoses."""
    
    __tablename__ = 'diagnoses'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # Diagnosis information
    symptoms = db.Column(db.Text, nullable=False)  # JSON array of symptoms
    predicted_diseases = db.Column(db.Text, nullable=True)  # JSON array from ML model
    confirmed_disease = db.Column(db.String(200), nullable=True)  # Doctor's final diagnosis
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert Diagnosis object to dictionary."""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'symptoms': self.symptoms,
            'predicted_diseases': self.predicted_diseases,
            'confirmed_disease': self.confirmed_disease,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

