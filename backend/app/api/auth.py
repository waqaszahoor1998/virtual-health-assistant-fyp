"""
Authentication API endpoints.

Handles user registration, login, logout, and token verification.
Uses JWT (JSON Web Tokens) for authentication with email/password.
"""

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app.api import api_bp
from app import db
from app.models.user import User


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "secure_password",
        "role": "patient" or "doctor"
    }
    
    Returns:
        JSON response with user data and JWT tokens
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email format (basic validation)
        email = data['email'].strip().lower()
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password length
        password = data['password']
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Validate role
        role = data['role'].lower()
        if role not in ['patient', 'doctor']:
            return jsonify({'error': 'Invalid role. Must be "patient" or "doctor"'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        new_user = User(
            email=email,
            role=role
        )
        
        # Hash and set password
        new_user.set_password(password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Create JWT tokens for the new user
        # Identity is the user ID stored in the token
        access_token = create_access_token(identity=str(new_user.id))
        refresh_token = create_refresh_token(identity=str(new_user.id))
        
        # Return success response with tokens
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        # Rollback database transaction on error
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """
    User login endpoint.
    
    Authenticates user with email and password, returns JWT tokens.
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "user_password"
    }
    
    Returns:
        JSON response with user data and JWT tokens (access and refresh)
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Normalize email (lowercase and strip whitespace)
        email = data['email'].strip().lower()
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if account is active
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated. Please contact support.'}), 403
        
        # Create JWT tokens
        # Identity is the user ID stored in the token
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Return success response with tokens and user info
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    
    Returns a new access token when the current one expires.
    Refresh token must be included in Authorization header.
    
    Returns:
        JSON response with new access token
    """
    try:
        # Get user ID from refresh token
        current_user_id = get_jwt_identity()
        
        # Create new access token
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500


@api_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout endpoint.
    
    In a simple JWT implementation, logout is handled client-side by
    removing the token. For token revocation, you would need a token blacklist.
    
    Returns:
        JSON response confirming logout
    """
    try:
        # In a more advanced implementation, you could:
        # 1. Add token to blacklist (requires Redis/database)
        # 2. Track active sessions
        
        # For now, logout is handled client-side by removing token
        return jsonify({
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500


@api_bp.route('/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """
    Verify authentication token validity.
    
    Protected endpoint that requires valid JWT token in Authorization header.
    If token is valid, returns user information.
    
    Returns:
        JSON response with token validity status and user info
    """
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Return user information
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Token verification failed: {str(e)}'}), 500


@api_bp.route('/auth/user', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.
    
    Protected endpoint that requires valid JWT token.
    Returns the user profile of the authenticated user.
    
    Returns:
        JSON response with current user data
    """
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        
        # Get user from database
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Return user information
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500
