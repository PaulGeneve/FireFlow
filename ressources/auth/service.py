from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from models.user import User
from extensions import db
from ressources.auth.constant import UserRole
from utils import check_allowed_filter


def register_user(**data):
    """
    Register a new user.
    :param data: User data (name, email, password, role)
    :return: Created User instance
    """
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password')
    role = data.get('role', UserRole.USER).lower()

    if not name or not email or not password:
        abort(400, message="Name, email and password are required")

    if not UserRole.is_valid(role):
        abort(400, message=f"Invalid role. Allowed roles: {', '.join(UserRole.all())}")

    try:
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        abort(409, message="User with this name or email already exists")

def login_user(**data):
    """
    Authenticate a user and return access token.
    :param data:
    :return:
    """
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()
    if not user or not user.check_password(password):
        abort(401, message="Invalid username or password.")

    access_token = create_access_token(identity=user.uuid)
    refresh_token = create_refresh_token(identity=user.uuid)
    return {
        "message": "Login successful.",
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    }


def list_user(filters=None):
    """
    List User records from the database, optionally filtered by provided criteria.
    :param filters:
    :return:
    """
    query = db.select(User)
    allowed_filters = {'name', 'email', 'role'}
    if filters:
        for attr, value in filters.items():
            check_allowed_filter(attr, allowed_filters)
            query = query.filter(getattr(User, attr) == value)
    return db.session.scalars(query).all()
