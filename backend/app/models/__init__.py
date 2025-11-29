"""
Database models for the Virtual Health Assistant.

This package contains all SQLAlchemy models for the database schema.
Models are organized by domain (user, patient, doctor, etc.)
"""

# Import all models so they are registered with SQLAlchemy
from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.diagnosis import Diagnosis
from app.models.prescription import Prescription
from app.models.appointment import Appointment
from app.models.drug import Drug
from app.models.disease import Disease
from app.models.symptom import Symptom

__all__ = [
    'User',
    'Patient',
    'Doctor',
    'Diagnosis',
    'Prescription',
    'Appointment',
    'Drug',
    'Disease',
    'Symptom'
]

