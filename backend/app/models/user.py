"""
User model for authentication and authorization.

This model stores user information and links to either Patient or Doctor profiles.
Uses JWT-based authentication with password hashing.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """
    User model representing authenticated users in the system.
    
    This table stores basic user information and links to either
    a Patient or Doctor profile based on the user's role.
    Uses JWT-based authentication with password hashing.
    
    Attributes:
        id (int): Primary key, auto-increment
        email (str): User's email address (unique, used for login)
        password_hash (str): Hashed password (never store plain passwords)
        role (str): User role ('patient' or 'doctor')
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
        is_active (bool): Whether account is active
    """
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User email (must be unique, used as login identifier)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    
    # Password hash (hashed password, never store plain text)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User role: 'patient' or 'doctor'
    role = db.Column(db.String(50), nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    # One-to-one relationship with Patient (if role is 'patient')
    patient_profile = db.relationship(
        'Patient',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    # One-to-one relationship with Doctor (if role is 'doctor')
    doctor_profile = db.relationship(
        'Doctor',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password):
        """
        Hash and set the user's password.
        
        Args:
            password (str): Plain text password to hash
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """String representation of User object."""
        return f'<User {self.email} ({self.role})>'
    
    def to_dict(self):
        """
        Convert User object to dictionary for JSON serialization.
        Excludes sensitive information like password_hash.
        
        Returns:
            dict: User data as dictionary (without password)
        """
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }

