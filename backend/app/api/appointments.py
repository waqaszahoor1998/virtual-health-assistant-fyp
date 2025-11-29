"""Appointment API endpoints - placeholder for future implementation."""

from flask import jsonify
from app.api import api_bp


@api_bp.route('/appointments', methods=['POST'])
def create_appointment():
    """Create appointment - placeholder."""
    return jsonify({'message': 'Create appointment - pending implementation'}), 200

