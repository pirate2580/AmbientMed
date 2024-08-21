from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from pymongo import MongoClient
import os
from app.models.user_model import User
from dotenv import load_dotenv
from datetime import timedelta


# Create a Flask Blueprint
login_bp = Blueprint('login_bp', __name__)

user_model = User()

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and Password are required"}), 400

    # Find user by email
    user = user_model.get_by_email(email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Verify password
    if not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid password"}), 401

    # Generate JWT
    token = create_access_token(identity=str(user['_id']), expires_delta=timedelta(hours=1))
    return jsonify({"auth": True, "token": token}), 200

@login_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and Password are required"}), 400

    user = user_model.get_by_email(email)
    if user:
        return jsonify({"message": "This user already exists"}), 400
    # Hash password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = {
        "email": email,
        "password": hashed_password
    }

    try:
        user_model.create(new_user)
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"message": f"Error registering user: {str(e)}"}), 500
