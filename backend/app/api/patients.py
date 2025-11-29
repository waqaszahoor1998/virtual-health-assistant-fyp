"""Patient API endpoints - placeholder for future implementation."""

from flask import jsonify
from app.api import api_bp


@api_bp.route('/patients', methods=['GET'])
def get_patients():
    """Get list of patients - placeholder."""
    return jsonify({'message': 'Patients endpoint - pending implementation'}), 200


@api_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID - placeholder."""
    return jsonify({'message': f'Get patient {patient_id} - pending implementation'}), 200

