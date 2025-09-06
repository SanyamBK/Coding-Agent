from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from .models import CustomUser, db

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register/', methods=['POST'])
def register_user():
    """Register a new user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if CustomUser.query.filter_by(username=username).first():
        return jsonify({"detail": "User already exists"}), 400

    new_user = CustomUser(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"detail": "User created successfully"}), 201

@user_blueprint.route('/token/', methods=['POST'])
def login():
    """Authenticate user and return access and refresh tokens."""
#    Expect JSON: {"username": "...", "password": "..."}
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'detail': 'Invalid username or password'}), 401

    user = CustomUser.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'detail': 'Invalid username or password'}), 401

    access = create_access_token(identity=user.username)
    refresh = create_refresh_token(identity=user.username)
    return jsonify({'refresh': refresh, 'access': access}), 200
# Your code

@user_blueprint.route('/list/', methods=['GET'])
# Implement authorization
def list_users():
    """Return all user records for authenticated users."""
    # Require a valid JWT; flask-jwt-extended will handle missing/invalid tokens
    @jwt_required()
    def _inner():
        users = CustomUser.query.all()
        return jsonify([{'username': u.username} for u in users]), 200

    return _inner()
# Your code


