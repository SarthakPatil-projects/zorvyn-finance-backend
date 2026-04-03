from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User
from app.utils.errors import error_response, success_response
import hashlib

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return error_response("Name, email and password are required", 400)

    if User.query.filter_by(email=data['email']).first():
        return error_response("Email already exists", 409)

    role = data.get('role', 'viewer')
    if role not in ['viewer', 'analyst', 'admin']:
        return error_response("Role must be viewer, analyst or admin", 400)

    user = User(
        name=data['name'],
        email=data['email'],
        password=hash_password(data['password']),
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return success_response(user.to_dict(), "User registered successfully", 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return error_response("Email and password are required", 400)

    user = User.query.filter_by(email=data['email']).first()

    if not user or user.password != hash_password(data['password']):
        return error_response("Invalid email or password", 401)

    if not user.is_active:
        return error_response("Account is deactivated", 403)

    token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'name': user.name}
    )

    return success_response({
        'token': token,
        'user': user.to_dict()
    }, "Login successful")