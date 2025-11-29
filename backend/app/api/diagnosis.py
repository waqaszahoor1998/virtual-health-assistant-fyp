"""Diagnosis API endpoints - placeholder for future implementation."""

from flask import jsonify
from app.api import api_bp


@api_bp.route('/diagnosis/predict', methods=['POST'])
def predict_diagnosis():
    """ML model prediction endpoint - placeholder."""
    return jsonify({'message': 'Diagnosis prediction - pending ML model integration'}), 200

