"""
Patient model for storing patient information.
"""

from datetime import datetime
from app import db


class Patient(db.Model):
    """
    Patient model representing patient profiles.
    
    Linked to User model via user_id foreign key.
    Stores patient-specific information like medical history.
    """
    
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Personal information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    
    # Medical information
    blood_type = db.Column(db.String(10), nullable=True)
    allergies = db.Column(db.Text, nullable=True)  # JSON or comma-separated
    medical_history = db.Column(db.Text, nullable=True)  # JSON
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert Patient object to dictionary."""
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

