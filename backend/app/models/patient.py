"""
Patient Model for Virtual Health Assistant.

This module defines the Patient database model which stores patient-specific
information and medical data. Each Patient is linked to a User account via
the user_id foreign key, establishing a one-to-one relationship.

The Patient model contains:
- Personal information (name, DOB, gender, contact info)
- Medical information (blood type, allergies, medical history)
- Relationship links to diagnoses, prescriptions, and appointments
"""

from datetime import datetime
from app import db


class Patient(db.Model):
    """
    Patient Model - Database table for storing patient profiles.
    
    This model represents a patient in the Virtual Health Assistant system.
    Each patient record is linked to exactly one User account (via user_id),
    and can have multiple diagnoses, prescriptions, and appointments.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        user_id (int): Foreign key to users table (one-to-one relationship)
        first_name (str): Patient's first name (max 100 chars, required)
        last_name (str): Patient's last name (max 100 chars, required)
        date_of_birth (date): Patient's date of birth (optional)
        gender (str): Patient's gender (max 20 chars, optional)
        phone (str): Contact phone number (max 20 chars, optional)
        address (str): Residential address (text, optional)
        blood_type (str): Patient's blood type (max 10 chars, optional)
        allergies (str): Known allergies - stored as JSON or comma-separated (optional)
        medical_history (str): Medical history - stored as JSON text (optional)
        created_at (datetime): Record creation timestamp (auto-set)
        updated_at (datetime): Last update timestamp (auto-updated)
    
    Relationships:
        - One-to-one with User model (via user_id)
        - One-to-many with Diagnosis model
        - One-to-many with Prescription model
        - One-to-many with Appointment model
    
    Example:
        ```python
        patient = Patient(
            user_id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 15),
            gender="Male",
            blood_type="O+",
            allergies='["Peanuts", "Penicillin"]'
        )
        db.session.add(patient)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'patients'
    
    # Primary key - unique identifier for each patient record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to users table - establishes one-to-one relationship
    # Each patient must be linked to exactly one user account
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # ==================== PERSONAL INFORMATION ====================
    
    # Patient's first name - required field for identification
    first_name = db.Column(db.String(100), nullable=False)
    
    # Patient's last name - required field for identification
    last_name = db.Column(db.String(100), nullable=False)
    
    # Date of birth - used for age calculation and medical reference
    date_of_birth = db.Column(db.Date, nullable=True)
    
    # Gender identity - optional demographic information
    gender = db.Column(db.String(20), nullable=True)
    
    # Contact phone number - for appointment reminders and communication
    phone = db.Column(db.String(20), nullable=True)
    
    # Residential address - full address text for medical records
    address = db.Column(db.Text, nullable=True)
    
    # ==================== MEDICAL INFORMATION ====================
    
    # Blood type - important for medical procedures and transfusions
    # Common values: A+, A-, B+, B-, AB+, AB-, O+, O-
    blood_type = db.Column(db.String(10), nullable=True)
    
    # Known allergies - stored as JSON array or comma-separated list
    # Example: '["Peanuts", "Penicillin", "Latex"]' or "Peanuts, Penicillin"
    allergies = db.Column(db.Text, nullable=True)
    
    # Medical history - stored as JSON object with past conditions, surgeries, etc.
    # Example: '{"past_conditions": ["Diabetes"], "surgeries": ["Appendectomy"]}'
    medical_history = db.Column(db.Text, nullable=True)
    
    # ==================== TIMESTAMPS ====================
    
    # Record creation timestamp - automatically set when record is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Last update timestamp - automatically updated whenever record is modified
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """
        Convert Patient object to dictionary for JSON serialization.
        
        This method is used when sending patient data to the frontend via API.
        It converts all relevant fields to a dictionary format, handling date
        serialization and ensuring all values are JSON-compatible.
        
        Returns:
            dict: Patient data as dictionary with the following keys:
                - id: Patient ID
                - user_id: Associated user ID
                - first_name: First name
                - last_name: Last name
                - date_of_birth: Date of birth (ISO format string or None)
                - gender: Gender
                - phone: Phone number
                - address: Address
                - blood_type: Blood type
                - allergies: Allergies (as stored)
                - created_at: Creation timestamp (ISO format string)
        
        Example:
            ```python
            patient_dict = patient.to_dict()
            # Returns: {'id': 1, 'first_name': 'John', ...}
            ```
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'address': self.address,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

