"""
Application entry point for development server.

Run this file to start the Flask development server.
For production, use a WSGI server like Gunicorn.
"""

import os
from app import create_app

# Create Flask application instance
# Uses FLASK_ENV environment variable or defaults to 'development'
app = create_app(os.environ.get('FLASK_ENV', 'development'))


if __name__ == '__main__':
    """
    Run the Flask development server.
    
    Development server is not suitable for production.
    Use Gunicorn or uWSGI for production deployment.
    """
    # Get port from environment variable or use default 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    # debug=True enables auto-reload on code changes
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=port,
        debug=True  # Enable debug mode in development
    )

