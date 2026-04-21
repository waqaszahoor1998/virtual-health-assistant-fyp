"""
API routes package.

This package contains all API endpoints organized by domain.
Uses Flask blueprints for modular route organization.
"""

from flask import Blueprint

# Create main API blueprint
# All routes in this package will be prefixed with '/api'
api_bp = Blueprint('api', __name__)

# Import all route modules to register them with the blueprint
# Import here to avoid circular imports
from app.api import auth, patients, doctors, diagnosis, drugs, prescriptions, appointments, consultations

