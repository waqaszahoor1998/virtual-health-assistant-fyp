"""
Drug Model for Virtual Health Assistant.

This module defines the Drug database model which stores drug information
from the DrugBank database. This serves as a catalog/reference table for
drugs that can be prescribed to patients.
"""

from app import db


class Drug(db.Model):
    """
    Drug Model - Database table for storing drug catalog information.
    
    This model represents a drug in the DrugBank database catalog. It stores
    essential drug information including DrugBank ID, name, description,
    indications, and mechanism of action. This is used as a reference table
    for drug lookups and prescription suggestions.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        drugbank_id (str): Unique DrugBank identifier (e.g., 'DB00001', required)
        name (str): Drug name (max 200 chars, required, indexed for search)
        description (str): Detailed drug description (optional)
        indication (str): Medical indications for use (optional)
        mechanism_of_action (str): How the drug works (optional)
    
    Relationships:
        - One-to-many with Prescription model (via drugbank_id reference)
    
    Note:
        This model stores drug catalog information. Actual prescriptions
        reference drugs via drugbank_id rather than direct foreign key.
    
    Example:
        ```python
        drug = Drug(
            drugbank_id="DB00001",
            name="Aspirin",
            description="Nonsteroidal anti-inflammatory drug",
            indication="Pain relief, fever reduction",
            mechanism_of_action="Inhibits prostaglandin synthesis"
        )
        db.session.add(drug)
        db.session.commit()
        ```
    """
    
    __tablename__ = 'drugs'
    
    # Primary key - unique identifier for each drug record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # DrugBank ID - unique identifier from DrugBank database
    # Format: "DB00001", "DB00002", etc.
    # Indexed for fast lookups when searching by DrugBank ID
    drugbank_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Drug name - common or brand name
    # Indexed for fast text searches when users search for drugs
    name = db.Column(db.String(200), nullable=False, index=True)
    
    # Drug description - detailed information about the drug
    # Can include chemical structure, properties, etc.
    description = db.Column(db.Text, nullable=True)
    
    # Indications - medical conditions this drug is used to treat
    # Example: "Used for pain relief, fever reduction, and inflammation"
    indication = db.Column(db.Text, nullable=True)
    
    # Mechanism of action - how the drug works in the body
    # Example: "Inhibits cyclooxygenase enzymes, reducing prostaglandin synthesis"
    mechanism_of_action = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """
        Convert Drug object to dictionary for JSON serialization.
        
        This method is used when sending drug data to the frontend via API.
        It converts all relevant fields to a dictionary format, ensuring all
        values are JSON-compatible.
        
        Returns:
            dict: Drug data as dictionary with the following keys:
                - id: Drug ID
                - drugbank_id: DrugBank identifier
                - name: Drug name
                - description: Drug description
                - indication: Medical indications
                - mechanism_of_action: Mechanism of action
        
        Example:
            ```python
            drug_dict = drug.to_dict()
            # Returns: {'id': 1, 'drugbank_id': 'DB00001', 'name': 'Aspirin', ...}
            ```
        """
        return {
            'id': self.id,
            'drugbank_id': self.drugbank_id,
            'name': self.name,
            'description': self.description,
            'indication': self.indication,
            'mechanism_of_action': self.mechanism_of_action,
        }

