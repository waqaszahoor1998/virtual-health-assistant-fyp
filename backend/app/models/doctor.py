"""
Doctor model for storing doctor information.
"""

from datetime import datetime
from app import db


class Doctor(db.Model):
    """Doctor model representing doctor profiles."""
    
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Personal information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(200), nullable=True)
    license_number = db.Column(db.String(50), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Practice information
    hospital_clinic = db.Column(db.String(200), nullable=True)
    address = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert Doctor object to dictionary."""
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

