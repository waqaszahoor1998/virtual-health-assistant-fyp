"""
Disease Model for Virtual Health Assistant.

This module defines the Disease database model which stores disease information
from the training dataset. This serves as a catalog/reference table for
diseases that can be predicted by the ML model.
"""

from app import db


class Disease(db.Model):
    """
    Disease Model - Database table for storing disease catalog information.
    
    This model represents a disease in the system catalog. It stores essential
    disease information including name, description, and category. This is used
    as a reference table for disease lookups and ML model predictions.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        name (str): Disease name (max 200 chars, required, unique, indexed)
        description (str): Detailed disease description (optional)
        category (str): Disease category/type (max 100 chars, optional)
    
    Relationships:
        - Referenced in Diagnosis model (via disease name in predicted/confirmed fields)
    
    Note:
        This model stores disease catalog information. Diagnoses reference diseases
        by name rather than direct foreign key for flexibility.
    
    Example:
        ```python
        disease = Disease(
            name="Migraine",
            description="A neurological condition characterized by recurrent headaches",
            category="Neurological"
        )
        db.session.add(disease)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'diseases'
    
    # Primary key - unique identifier for each disease record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Disease name - official or common name of the disease
    # Must be unique (no duplicate disease names)
    # Indexed for fast text searches
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    
    # Disease description - detailed information about the disease
    # Can include symptoms, causes, prevalence, etc.
    description = db.Column(db.Text, nullable=True)
    
    # Disease category - classification/type of disease
    # Examples: "Neurological", "Cardiovascular", "Respiratory", "Infectious"
    category = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        """
        Convert Disease object to dictionary for JSON serialization.
        
        This method is used when sending disease data to the frontend via API.
        It converts all relevant fields to a dictionary format, ensuring all
        values are JSON-compatible.
        
        Returns:
            dict: Disease data as dictionary with the following keys:
                - id: Disease ID
                - name: Disease name
                - description: Disease description
                - category: Disease category
        
        Example:
            ```python
            disease_dict = disease.to_dict()
            # Returns: {'id': 1, 'name': 'Migraine', 'description': '...', ...}
            ```
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
        }

