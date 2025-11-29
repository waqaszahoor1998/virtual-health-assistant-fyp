"""
Prescription Model for Virtual Health Assistant.

This module defines the Prescription database model which stores prescription
information including drug details, dosage instructions, and administration
guidelines. Each prescription is linked to a diagnosis, patient, and doctor.
"""

from datetime import datetime
from app import db


class Prescription(db.Model):
    """
    Prescription Model - Database table for storing prescription records.
    
    This model represents a prescription issued by a doctor to a patient.
    It stores drug information from DrugBank, dosage instructions, frequency,
    duration, and additional administration instructions.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        diagnosis_id (int): Foreign key to diagnoses table (links to diagnosis)
        patient_id (int): Foreign key to patients table (who the prescription is for)
        doctor_id (int): Foreign key to doctors table (who issued the prescription)
        drugbank_id (str): DrugBank ID of the prescribed drug (required)
        drug_name (str): Name of the prescribed drug (required)
        dosage (str): Dosage instructions (e.g., "500mg", optional)
        frequency (str): How often to take (e.g., "Twice daily", optional)
        duration (str): How long to take (e.g., "7 days", optional)
        instructions (str): Additional administration instructions (optional)
        created_at (datetime): Record creation timestamp (auto-set)
    
    Relationships:
        - Many-to-one with Diagnosis model (via diagnosis_id)
        - Many-to-one with Patient model (via patient_id)
        - Many-to-one with Doctor model (via doctor_id)
    
    Example:
        ```python
        prescription = Prescription(
            diagnosis_id=1,
            patient_id=1,
            doctor_id=1,
            drugbank_id="DB00001",
            drug_name="Aspirin",
            dosage="500mg",
            frequency="Twice daily",
            duration="7 days",
            instructions="Take with food to reduce stomach irritation"
        )
        db.session.add(prescription)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'prescriptions'
    
    # Primary key - unique identifier for each prescription record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to diagnoses table - which diagnosis this prescription is for
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'), nullable=False)
    
    # Foreign key to patients table - which patient this prescription is for
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Foreign key to doctors table - which doctor issued this prescription
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # ==================== PRESCRIPTION DETAILS ====================
    
    # DrugBank ID - unique identifier from DrugBank database
    # Format: "DB00001", "DB00002", etc.
    drugbank_id = db.Column(db.String(50), nullable=False)
    
    # Drug name - common name of the prescribed medication
    # Example: "Aspirin", "Ibuprofen", "Amoxicillin"
    drug_name = db.Column(db.String(200), nullable=False)
    
    # Dosage - amount of drug per dose
    # Example: "500mg", "10ml", "2 tablets"
    dosage = db.Column(db.String(100), nullable=True)
    
    # Frequency - how often to take the medication
    # Example: "Once daily", "Twice daily", "Every 6 hours"
    frequency = db.Column(db.String(100), nullable=True)
    
    # Duration - how long to take the medication
    # Example: "7 days", "2 weeks", "As needed"
    duration = db.Column(db.String(100), nullable=True)
    
    # Additional instructions - special instructions for administration
    # Example: "Take with food", "Avoid alcohol", "Complete full course"
    instructions = db.Column(db.Text, nullable=True)
    
    # ==================== TIMESTAMPS ====================
    
    # Record creation timestamp - when prescription was issued
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        Convert Prescription object to dictionary for JSON serialization.
        
        This method is used when sending prescription data to the frontend via API.
        It converts all relevant fields to a dictionary format, handling date
        serialization and ensuring all values are JSON-compatible.
        
        Returns:
            dict: Prescription data as dictionary with the following keys:
                - id: Prescription ID
                - diagnosis_id: Associated diagnosis ID
                - patient_id: Associated patient ID
                - doctor_id: Associated doctor ID
                - drugbank_id: DrugBank ID
                - drug_name: Drug name
                - dosage: Dosage instructions
                - frequency: Frequency instructions
                - duration: Duration instructions
                - instructions: Additional instructions
                - created_at: Creation timestamp (ISO format string)
        
        Example:
            ```python
            prescription_dict = prescription.to_dict()
            # Returns: {'id': 1, 'drugbank_id': 'DB00001', ...}
            ```
        """
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

