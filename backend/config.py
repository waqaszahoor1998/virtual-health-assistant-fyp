"""
Configuration settings for the Virtual Health Assistant backend.

This module contains all configuration classes for different environments
(development, production, testing).
"""

import os
from datetime import timedelta


class Config:
    """
    Base configuration class with common settings.
    All other configurations inherit from this class.
    """
    
    # Application secret key for session management and token signing
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/virtual_health_assistant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event system to save resources
    
    # JWT Configuration for authentication tokens
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expires in 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expires in 30 days
    JWT_ALGORITHM = 'HS256'  # Algorithm for JWT signing
    
    # CORS configuration - allows frontend to make requests
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # API rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_DEFAULT = "100 per hour"
    
    # ML Model paths
    ML_MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'models')
    
    # Data paths
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
    DRUGBANK_CSV = os.path.join(DATA_DIR, 'processed', 'drugbank_clean.csv')
    
    # Pagination
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    More verbose error messages and debugging enabled.
    """
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production environment configuration.
    Security features enabled, debug mode disabled.
    """
    DEBUG = False
    TESTING = False
    
    # In production, use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Stricter CORS in production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')


class TestingConfig(Config):
    """
    Testing environment configuration.
    Uses in-memory database for fast test execution.
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


# Configuration dictionary - maps environment names to config classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

