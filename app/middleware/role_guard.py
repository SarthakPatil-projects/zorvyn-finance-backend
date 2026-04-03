from functools import wraps
from flask_jwt_extended import get_jwt
from app.utils.errors import error_response

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            if user_role not in roles:
                return error_response("Access denied. Insufficient permissions.", 403)
            return fn(*args, **kwargs)
        return decorated
    return wrapper