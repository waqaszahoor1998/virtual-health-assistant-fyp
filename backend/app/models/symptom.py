"""
Symptom Model for Virtual Health Assistant.

This module defines the Symptom database model which stores symptom information
from the training dataset. This serves as a catalog/reference table for
symptoms that can be used in ML model predictions.
"""

from app import db


class Symptom(db.Model):
    """
    Symptom Model - Database table for storing symptom catalog information.
    
    This model represents a symptom in the system catalog. It stores essential
    symptom information including name, description, and category. This is used
    as a reference table for symptom lookups and as input for ML model predictions.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        name (str): Symptom name (max 200 chars, required, unique, indexed)
        description (str): Detailed symptom description (optional)
        category (str): Symptom category/type (max 100 chars, optional)
    
    Relationships:
        - Referenced in Diagnosis model (via symptom names in symptoms field)
        - Used as input features for ML model predictions
    
    Note:
        This model stores symptom catalog information. Diagnoses reference symptoms
        by name (in JSON array) rather than direct foreign keys for flexibility.
    
    Example:
        ```python
        symptom = Symptom(
            name="Fever",
            description="Elevated body temperature above normal range",
            category="General"
        )
        db.session.add(symptom)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'symptoms'
    
    # Primary key - unique identifier for each symptom record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Symptom name - official or common name of the symptom
    # Must be unique (no duplicate symptom names)
    # Indexed for fast text searches when users select symptoms
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    
    # Symptom description - detailed information about the symptom
    # Can include characteristics, common causes, etc.
    description = db.Column(db.Text, nullable=True)
    
    # Symptom category - classification/type of symptom
    # Examples: "General", "Cardiovascular", "Neurological", "Respiratory", "Gastrointestinal"
    category = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        """
        Convert Symptom object to dictionary for JSON serialization.
        
        This method is used when sending symptom data to the frontend via API.
        It converts all relevant fields to a dictionary format, ensuring all
        values are JSON-compatible.
        
        Returns:
            dict: Symptom data as dictionary with the following keys:
                - id: Symptom ID
                - name: Symptom name
                - description: Symptom description
                - category: Symptom category
        
        Example:
            ```python
            symptom_dict = symptom.to_dict()
            # Returns: {'id': 1, 'name': 'Fever', 'description': '...', ...}
            ```
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
        }

