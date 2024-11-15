from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db
from app import app  # Assuming your app is initialized in __init__.py

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate users and return JWT.
    """
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    user = User.query.filter_by(email=email).first()  # Find user by email
    if user and user.check_password(password):  # Validate password
        access_token = create_access_token(identity=user.id)  # Generate JWT token
        return jsonify(access_token=access_token), 200  # Return the token
    
    return jsonify({"msg": "Invalid credentials"}), 401  # Invalid credentials

# Protected endpoint
@app.route('/protected', methods=['GET'])
@jwt_required()  # Ensure user is authenticated
def protected():
    """
    A protected endpoint that requires a valid JWT.
    """
    current_user = get_jwt_identity()  # Get user identity from JWT
    return jsonify(logged_in_as=current_user), 200

# Admin-only endpoint
@app.route('/admin', methods=['GET'])
@jwt_required()  # Ensure user is authenticated
def admin():
    """
    Admin-only endpoint that requires admin privileges.
    """
    current_user = get_jwt_identity()  # Get user ID from JWT
    user = User.query.get(current_user)  # Retrieve user from the database
    
    if user and user.is_admin:  # Check if the user is an admin
        return jsonify(message="Welcome, Admin!"), 200
    
    return jsonify(message="Access forbidden: Admins only."), 403

