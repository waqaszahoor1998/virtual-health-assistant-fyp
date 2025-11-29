"""Disease model for storing disease information."""

from app import db


class Disease(db.Model):
    """Disease model representing diseases in the system."""
    
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        """Convert Disease object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
        }

