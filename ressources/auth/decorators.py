from functools import wraps
from flask_smorest import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from extensions import db
from models.user import User
from ressources.auth.constant import UserRole


def admin_required(fn):
    """
    Décorateur pour les routes réservées aux admins.
    Usage: @admin_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_uuid = get_jwt_identity()
        user = db.session.scalar(
            db.select(User).filter_by(uuid=user_uuid)
        )

        if not user or user.role != UserRole.ADMIN:
            abort(403, message="Admin access required")

        return fn(*args, **kwargs)
    return wrapper


def user_or_admin_required(fn):
    """
    Décorateur pour les routes accessibles aux users et admins.
    Usage: @user_or_admin_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_uuid = get_jwt_identity()
        print(user_uuid)
        user = db.session.scalar(
            db.select(User).filter_by(uuid=user_uuid)
        )
        print(user)

        if not user:
            abort(403, message="Authentication required")

        return fn(*args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """
    Décorateur flexible pour plusieurs rôles.
    Usage: @role_required(UserRole.ADMIN, UserRole.USER)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)

            if not user or user.role not in allowed_roles:
                abort(403, message="Insufficient permissions")

            return fn(*args, **kwargs)
        return wrapper
    return decorator
