"""
Flask application factory.

Wiring for new readers:
  create_app() loads config from config.py (DB URL, JWT, ML_MODELS_DIR, …),
  attaches SQLAlchemy + JWT + Migrate, enables CORS for /api, and mounts
  the api_bp blueprint at URL prefix /api (see app/api/__init__.py).
  Route modules (auth, diagnosis, …) import api_bp and register routes on it.

Frontend (Vite) talks to /api/... on the same host or via proxy; see
frontend/vite.config.js.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Allow local `.env` to win over inherited shell env (common on dev machines).
load_dotenv(override=True)

from config import config


# Initialize extensions (will be initialized in create_app)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """
    Application factory function.
    Creates and configures the Flask application instance.
    
    Args:
        config_name (str): Name of the configuration to use.
                          Defaults to 'development' if not provided.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Get configuration name from environment variable or use default
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS (Cross-Origin Resource Sharing) for frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints (API routes)
    # Import here to avoid circular imports
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register CLI commands
    from app.cli.seed import seed_db_command
    app.cli.add_command(seed_db_command)
    from app.cli.catalog import build_catalog_command
    app.cli.add_command(build_catalog_command)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables (only in development)
    if config_name == 'development':
        with app.app_context():
            db.create_all()
    
    return app


def register_error_handlers(app):
    """
    Register custom error handlers for the application.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return {'error': 'Bad request'}, 400


# Import models to ensure they are registered with SQLAlchemy
# Import here to avoid circular imports
from app.models import user, patient, doctor, diagnosis, prescription, appointment, consultation_request

