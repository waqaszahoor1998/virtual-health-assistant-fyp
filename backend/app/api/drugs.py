"""Drug API endpoints - placeholder for future implementation."""

from flask import jsonify
from app.api import api_bp


@api_bp.route('/drugs/search', methods=['GET'])
def search_drugs():
    """Search drugs from DrugBank - placeholder."""
    return jsonify({'message': 'Drug search - pending implementation'}), 200


@api_bp.route('/drugs/suggest', methods=['POST'])
def suggest_drugs():
    """Suggest drugs based on diagnosis - placeholder."""
    return jsonify({'message': 'Drug suggestion - pending implementation'}), 200

