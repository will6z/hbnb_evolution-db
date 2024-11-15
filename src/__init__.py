from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from config import DevelopmentConfig
from models import db
from auth import auth_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize the database
db.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Admin-required endpoint
@app.route('/admin/data', methods=['POST', 'DELETE'])
@jwt_required()
def admin_data():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    # Admin-only functionality
    return jsonify({"msg": "Admin data processed"}), 200


# Example of securing resource-related endpoints with role checks
@app.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    current_user = get_jwt_identity()
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "You do not have permission to create places"}), 403
    # Proceed with creating a place
    return jsonify({"msg": "Place created successfully"}), 201

