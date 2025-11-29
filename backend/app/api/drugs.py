"""
Drug API endpoints.

Handles drug search and suggestions from DrugBank database.
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.utils.drugbank_service import get_drugbank_service


@api_bp.route('/drugs/search', methods=['GET'])
@jwt_required()
def search_drugs():
    """
    Search drugs from DrugBank database.
    
    Query parameters:
    - q (str): Search query (drug name)
    - limit (int): Maximum number of results (default: 20)
    
    Returns:
        JSON response with list of matching drugs
    """
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Search query (q) is required'}), 400
        
        if limit > 100:
            limit = 100  # Cap at 100 results
        
        # Get DrugBank service
        drugbank_service = get_drugbank_service()
        
        if not drugbank_service.is_available():
            return jsonify({
                'error': 'DrugBank database not available',
                'message': 'DrugBank CSV file not found'
            }), 503
        
        # Search drugs
        drugs = drugbank_service.search_drugs(query, limit=limit)
        
        return jsonify({
            'query': query,
            'count': len(drugs),
            'drugs': drugs
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to search drugs: {str(e)}'}), 500


@api_bp.route('/drugs/<drugbank_id>', methods=['GET'])
@jwt_required()
def get_drug(drugbank_id):
    """
    Get drug details by DrugBank ID.
    
    Args:
        drugbank_id (str): DrugBank ID (e.g., 'DB00001')
    
    Returns:
        JSON response with drug details
    """
    try:
        # Get DrugBank service
        drugbank_service = get_drugbank_service()
        
        if not drugbank_service.is_available():
            return jsonify({'error': 'DrugBank database not available'}), 503
        
        # Get drug
        drug = drugbank_service.get_drug_by_id(drugbank_id)
        
        if not drug:
            return jsonify({'error': 'Drug not found'}), 404
        
        return jsonify(drug), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get drug: {str(e)}'}), 500


@api_bp.route('/drugs/suggest', methods=['POST'])
@jwt_required()
def suggest_drugs():
    """
    Suggest drugs based on disease diagnosis.
    
    Expected JSON payload:
    {
        "disease": "Migraine",
        "limit": 10 (optional)
    }
    
    Returns:
        JSON response with suggested drugs
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'disease' not in data:
            return jsonify({'error': 'Disease name is required'}), 400
        
        disease_name = data['disease'].strip()
        
        if not disease_name:
            return jsonify({'error': 'Disease name cannot be empty'}), 400
        
        limit = data.get('limit', 10)
        if limit > 50:
            limit = 50  # Cap at 50 results
        
        # Get DrugBank service
        drugbank_service = get_drugbank_service()
        
        if not drugbank_service.is_available():
            return jsonify({
                'error': 'DrugBank database not available'
            }), 503
        
        # Get drug suggestions
        drugs = drugbank_service.suggest_drugs_for_disease(disease_name, limit=limit)
        
        return jsonify({
            'disease': disease_name,
            'count': len(drugs),
            'drugs': drugs
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to suggest drugs: {str(e)}'}), 500
