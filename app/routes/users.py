from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.user import User
from app.middleware.role_guard import role_required
from app.utils.errors import error_response, success_response

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = User.query.all()
    return success_response([u.to_dict() for u in users])

@users_bp.route('/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_role(user_id):
    data = request.get_json()
    role = data.get('role')

    if role not in ['viewer', 'analyst', 'admin']:
        return error_response("Role must be viewer, analyst or admin", 400)

    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)

    user.role = role
    db.session.commit()
    return success_response(user.to_dict(), "Role updated successfully")

@users_bp.route('/<int:user_id>/status', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_status(user_id):
    data = request.get_json()
    is_active = data.get('is_active')

    if is_active is None:
        return error_response("is_active field is required", 400)

    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)

    user.is_active = is_active
    db.session.commit()
    return success_response(user.to_dict(), "Status updated successfully")