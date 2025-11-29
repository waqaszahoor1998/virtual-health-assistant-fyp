"""
Doctor Model for Virtual Health Assistant.

This module defines the Doctor database model which stores doctor-specific
information including professional credentials and practice details. Each Doctor
is linked to a User account via the user_id foreign key.

The Doctor model contains:
- Personal information (name, specialization, license)
- Practice information (hospital/clinic, address)
- Relationship links to diagnoses, prescriptions, and appointments
"""

from datetime import datetime
from app import db


class Doctor(db.Model):
    """
    Doctor Model - Database table for storing doctor profiles.
    
    This model represents a doctor in the Virtual Health Assistant system.
    Each doctor record is linked to exactly one User account (via user_id),
    and can have multiple diagnoses, prescriptions, and appointments with patients.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        user_id (int): Foreign key to users table (one-to-one relationship)
        first_name (str): Doctor's first name (max 100 chars, required)
        last_name (str): Doctor's last name (max 100 chars, required)
        specialization (str): Medical specialization/field (max 200 chars, optional)
        license_number (str): Medical license number (max 50 chars, unique, optional)
        phone (str): Contact phone number (max 20 chars, optional)
        hospital_clinic (str): Hospital or clinic name (max 200 chars, optional)
        address (str): Practice address (text, optional)
        created_at (datetime): Record creation timestamp (auto-set)
        updated_at (datetime): Last update timestamp (auto-updated)
    
    Relationships:
        - One-to-one with User model (via user_id)
        - One-to-many with Diagnosis model
        - One-to-many with Prescription model
        - One-to-many with Appointment model
    
    Example:
        ```python
        doctor = Doctor(
            user_id=2,
            first_name="Jane",
            last_name="Smith",
            specialization="Cardiology",
            license_number="MD12345",
            hospital_clinic="City Hospital"
        )
        db.session.add(doctor)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'doctors'
    
    # Primary key - unique identifier for each doctor record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to users table - establishes one-to-one relationship
    # Each doctor must be linked to exactly one user account
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # ==================== PERSONAL INFORMATION ====================
    
    # Doctor's first name - required field for identification
    first_name = db.Column(db.String(100), nullable=False)
    
    # Doctor's last name - required field for identification
    last_name = db.Column(db.String(100), nullable=False)
    
    # Medical specialization - field of expertise
    # Examples: "Cardiology", "Pediatrics", "Internal Medicine", "Surgery"
    specialization = db.Column(db.String(200), nullable=True)
    
    # Medical license number - unique identifier for professional verification
    # Should be unique across all doctors for validation
    license_number = db.Column(db.String(50), nullable=True, unique=True)
    
    # Contact phone number - for patient communication and scheduling
    phone = db.Column(db.String(20), nullable=True)
    
    # ==================== PRACTICE INFORMATION ====================
    
    # Hospital or clinic name where doctor practices
    hospital_clinic = db.Column(db.String(200), nullable=True)
    
    # Practice address - full address of clinic/hospital
    address = db.Column(db.Text, nullable=True)
    
    # ==================== TIMESTAMPS ====================
    
    # Record creation timestamp - automatically set when record is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Last update timestamp - automatically updated whenever record is modified
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """
        Convert Doctor object to dictionary for JSON serialization.
        
        This method is used when sending doctor data to the frontend via API.
        It converts all relevant fields to a dictionary format, handling date
        serialization and ensuring all values are JSON-compatible.
        
        Returns:
            dict: Doctor data as dictionary with the following keys:
                - id: Doctor ID
                - user_id: Associated user ID
                - first_name: First name
                - last_name: Last name
                - specialization: Medical specialization
                - license_number: License number
                - phone: Phone number
                - hospital_clinic: Hospital/clinic name
                - created_at: Creation timestamp (ISO format string)
        
        Example:
            ```python
            doctor_dict = doctor.to_dict()
            # Returns: {'id': 1, 'first_name': 'Jane', ...}
            ```
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'phone': self.phone,
            'hospital_clinic': self.hospital_clinic,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

