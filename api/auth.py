from flask import Blueprint, request, jsonify
from .models import User
from .utils import generate_token, verify_token
from flask_jwt_extended import create_access_token
import pyotp

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with email, password, and OTP secret."""
    data = request.get_json()
    user = User.find_by_email(data['email'])
    if user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(
        email=data['email'],
        password=data['password'],
        otp_secret=pyotp.random_base32()  # Generate a new OTP secret
    )
    new_user.save_to_db()
    access_token = create_access_token(identity=new_user.id)
    return jsonify({'token': access_token, 'otp_secret': new_user.otp_secret}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user with email, password, and OTP."""
    data = request.get_json()
    user = User.find_by_email(data['email'])
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    otp = data.get('otp')
    if not pyotp.TOTP(user.otp_secret).verify(otp):
        return jsonify({'message': 'Invalid OTP'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'token': access_token}), 200
