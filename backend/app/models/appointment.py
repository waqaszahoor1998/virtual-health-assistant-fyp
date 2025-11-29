"""
Appointment Model for Virtual Health Assistant.

This module defines the Appointment database model which stores appointment
scheduling information between patients and doctors. It tracks appointment
dates, status, reason, and notes.
"""

from datetime import datetime
from app import db


class Appointment(db.Model):
    """
    Appointment Model - Database table for storing appointment records.
    
    This model represents a scheduled appointment between a patient and a doctor.
    It tracks the appointment date/time, status, reason for visit, and any notes.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        patient_id (int): Foreign key to patients table (required)
        doctor_id (int): Foreign key to doctors table (required)
        appointment_date (datetime): Date and time of the appointment (required)
        status (str): Appointment status - 'scheduled', 'completed', or 'cancelled' (default: 'scheduled')
        reason (str): Reason for the appointment (optional)
        notes (str): Additional notes about the appointment (optional)
        created_at (datetime): Record creation timestamp (auto-set)
        updated_at (datetime): Last update timestamp (auto-updated)
    
    Relationships:
        - Many-to-one with Patient model (via patient_id)
        - Many-to-one with Doctor model (via doctor_id)
    
    Status Values:
        - 'scheduled': Appointment is scheduled for future
        - 'completed': Appointment has been completed
        - 'cancelled': Appointment was cancelled
    
    Example:
        ```python
        appointment = Appointment(
            patient_id=1,
            doctor_id=1,
            appointment_date=datetime(2024, 3, 15, 14, 30),
            status='scheduled',
            reason="Follow-up for previous diagnosis"
        )
        db.session.add(appointment)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'appointments'
    
    # Primary key - unique identifier for each appointment record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to patients table - which patient this appointment is for
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Foreign key to doctors table - which doctor this appointment is with
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    
    # ==================== APPOINTMENT DETAILS ====================
    
    # Appointment date and time - when the appointment is scheduled
    appointment_date = db.Column(db.DateTime, nullable=False)
    
    # Appointment status - tracks the current state of the appointment
    # Valid values: 'scheduled', 'completed', 'cancelled'
    # Default is 'scheduled' when appointment is first created
    status = db.Column(db.String(50), default='scheduled', nullable=False)
    
    # Reason for appointment - why the patient is scheduling this visit
    # Example: "Annual checkup", "Follow-up", "New symptoms"
    reason = db.Column(db.Text, nullable=True)
    
    # Additional notes - any special notes about the appointment
    notes = db.Column(db.Text, nullable=True)
    
    # ==================== TIMESTAMPS ====================
    
    # Record creation timestamp - when appointment was scheduled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Last update timestamp - automatically updated whenever record is modified
    # Useful for tracking when status changed (e.g., from scheduled to completed)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """
        Convert Appointment object to dictionary for JSON serialization.
        
        This method is used when sending appointment data to the frontend via API.
        It converts all relevant fields to a dictionary format, handling datetime
        serialization and ensuring all values are JSON-compatible.
        
        Returns:
            dict: Appointment data as dictionary with the following keys:
                - id: Appointment ID
                - patient_id: Associated patient ID
                - doctor_id: Associated doctor ID
                - appointment_date: Appointment date/time (ISO format string)
                - status: Appointment status
                - reason: Reason for appointment
                - notes: Additional notes
                - created_at: Creation timestamp (ISO format string)
        
        Example:
            ```python
            appointment_dict = appointment.to_dict()
            # Returns: {'id': 1, 'patient_id': 1, 'appointment_date': '2024-03-15T14:30:00', ...}
            ```
        """
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

