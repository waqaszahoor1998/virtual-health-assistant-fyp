"""Drug model for storing drug information from DrugBank."""

from app import db


class Drug(db.Model):
    """Drug model representing drugs from DrugBank database."""
    
    __tablename__ = 'drugs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drugbank_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    indication = db.Column(db.Text, nullable=True)
    mechanism_of_action = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert Drug object to dictionary."""
        return {
            'id': self.id,
            'drugbank_id': self.drugbank_id,
            'name': self.name,
            'description': self.description,
            'indication': self.indication,
            'mechanism_of_action': self.mechanism_of_action,
        }

