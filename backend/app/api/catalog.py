"""
Catalog API endpoints (symptoms + diseases).

Why this exists:
  - The ML pipeline stores a large set of disease names in artifacts (e.g.
    ml_models/models/unique_diseases.txt) and symptom strings in processed data.
  - The UI previously used a small hardcoded symptom list, making the dataset
    feel \"empty\" even when ML artifacts were large.

These endpoints expose the database-backed catalogs so the frontend can:
  - fetch a large list of symptoms for search/autocomplete
  - fetch a large list of diseases for reference

Population is handled by a CLI command (see app/cli/catalog.py).
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.api import api_bp
from app.models.symptom import Symptom
from app.models.disease import Disease


def _get_pagination_args():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 200, type=int)
    per_page = max(1, min(per_page, 1000))
    return page, per_page


@api_bp.route("/catalog/symptoms", methods=["GET"])
@jwt_required()
def list_symptoms_catalog():
    """
    List/search symptom catalog entries.

    Query params:
      - q: optional search query (substring match)
      - page, per_page: pagination
    """
    try:
        q = (request.args.get("q") or "").strip()
        page, per_page = _get_pagination_args()

        query = Symptom.query
        if q:
            query = query.filter(Symptom.name.ilike(f"%{q}%"))

        pagination = query.order_by(Symptom.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return jsonify(
            {
                "items": [s.to_dict() for s in pagination.items],
                "total": pagination.total,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "q": q,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": f"Failed to list symptoms: {str(e)}"}), 500


@api_bp.route("/catalog/diseases", methods=["GET"])
@jwt_required()
def list_diseases_catalog():
    """
    List/search disease catalog entries.

    Query params:
      - q: optional search query (substring match)
      - page, per_page: pagination
    """
    try:
        q = (request.args.get("q") or "").strip()
        page, per_page = _get_pagination_args()

        query = Disease.query
        if q:
            query = query.filter(Disease.name.ilike(f"%{q}%"))

        pagination = query.order_by(Disease.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return jsonify(
            {
                "items": [d.to_dict() for d in pagination.items],
                "total": pagination.total,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "q": q,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": f"Failed to list diseases: {str(e)}"}), 500

