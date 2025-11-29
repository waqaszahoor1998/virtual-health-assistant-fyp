"""Doctor API endpoints - placeholder for future implementation."""

from flask import jsonify
from app.api import api_bp


@api_bp.route('/doctors', methods=['GET'])
def get_doctors():
    """Get list of doctors - placeholder."""
    return jsonify({'message': 'Doctors endpoint - pending implementation'}), 200

