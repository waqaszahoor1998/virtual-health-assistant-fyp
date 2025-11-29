"""Prescription API endpoints - placeholder for future implementation."""

from flask import jsonify
from app.api import api_bp


@api_bp.route('/prescriptions', methods=['POST'])
def create_prescription():
    """Create prescription - placeholder."""
    return jsonify({'message': 'Create prescription - pending implementation'}), 200

