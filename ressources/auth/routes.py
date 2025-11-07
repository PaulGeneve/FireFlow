from flask.views import MethodView
from flask_smorest import Blueprint
from ressources.auth.schema import UserArgsSchema, UserSchema, UserLoginSchema, UserTokenSchema
from ressources.auth.service import register_user, login_user

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register')
class AuthRegister(MethodView):
    @auth.arguments(UserArgsSchema)
    @auth.response(201, UserSchema)
    def post(self, data):
        return register_user(**data), 201


@auth.route('/login')
class AuthLogin(MethodView):
    @auth.arguments(UserLoginSchema)
    @auth.response(200, UserTokenSchema)
    def post(self, data):
        return login_user(**data), 200
