"""
Diagnosis Model for Virtual Health Assistant.

This module defines the Diagnosis database model which stores diagnosis records
containing symptoms, ML-predicted diseases, and doctor-confirmed diagnoses.
Each diagnosis links a patient, doctor, symptoms, and disease information.
"""

from datetime import datetime
from app import db


class Diagnosis(db.Model):
    """
    Diagnosis Model - Database table for storing diagnosis records.
    
    This model represents a medical diagnosis made by a doctor for a patient.
    It stores the symptoms presented, ML model predictions, and the doctor's
    final confirmed diagnosis. This creates a record of the diagnostic process.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        patient_id (int): Foreign key to patients table (required)
        doctor_id (int): Foreign key to doctors table (required)
        symptoms (str): JSON array of symptoms reported (required)
        predicted_diseases (str): JSON array of ML model predictions (optional)
        confirmed_disease (str): Doctor's final confirmed diagnosis (optional)
        notes (str): Additional notes about the diagnosis (optional)
        created_at (datetime): Record creation timestamp (auto-set)
    
    Relationships:
        - Many-to-one with Patient model (via patient_id)
        - Many-to-one with Doctor model (via doctor_id)
        - One-to-many with Prescription model
    
    Example:
        ```python
        diagnosis = Diagnosis(
            patient_id=1,
            doctor_id=1,
            symptoms='["fever", "headache", "nausea"]',
            predicted_diseases='[{"disease": "Migraine", "confidence": 0.85}]',
            confirmed_disease="Migraine",
            notes="Patient responds well to rest and medication"
        )
        db.session.add(diagnosis)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'diagnoses'
    
    # Primary key - unique identifier for each diagnosis record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to patients table - which patient this diagnosis is for
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Foreign key to doctors table - which doctor made this diagnosis
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # ==================== DIAGNOSIS INFORMATION ====================
    
    # Symptoms reported by patient - stored as JSON array string
    # Example: '["fever", "headache", "fatigue", "muscle pain"]'
    symptoms = db.Column(db.Text, nullable=False)
    
    # ML model predictions - stored as JSON array of disease predictions
    # Example: '[{"disease": "Influenza", "confidence": 0.92}, ...]'
    predicted_diseases = db.Column(db.Text, nullable=True)
    
    # Doctor's confirmed final diagnosis - the actual disease confirmed by doctor
    # This may differ from ML predictions based on doctor's clinical judgment
    confirmed_disease = db.Column(db.String(200), nullable=True)
    
    # Additional notes about the diagnosis - clinical observations, etc.
    notes = db.Column(db.Text, nullable=True)
    
    # ==================== TIMESTAMPS ====================
    
    # Record creation timestamp - when diagnosis was made
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        Convert Diagnosis object to dictionary for JSON serialization.
        
        This method is used when sending diagnosis data to the frontend via API.
        It converts all relevant fields to a dictionary format, ensuring all
        JSON fields are properly handled.
        
        Returns:
            dict: Diagnosis data as dictionary with the following keys:
                - id: Diagnosis ID
                - patient_id: Associated patient ID
                - doctor_id: Associated doctor ID
                - symptoms: Symptoms as stored (JSON string)
                - predicted_diseases: ML predictions as stored (JSON string)
                - confirmed_disease: Confirmed disease name
                - notes: Additional notes
                - created_at: Creation timestamp (ISO format string)
        
        Example:
            ```python
            diagnosis_dict = diagnosis.to_dict()
            # Returns: {'id': 1, 'patient_id': 1, 'symptoms': '[...]', ...}
            ```
        """
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

