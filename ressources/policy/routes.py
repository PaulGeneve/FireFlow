from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from ressources.auth.decorators import admin_required, user_or_admin_required
from ressources.policy.schema import PolicySchema, PolicyArgsSchema, PolicyToggleResponseSchema
from ressources.policy.service import list_policies, create_policy, delete_policy

policy = Blueprint("policy", __name__, url_prefix="/policy", description="Policy management")

@policy.route("/")
class PolicyCollection(MethodView):
    @jwt_required()
    @user_or_admin_required
    @policy.arguments(PolicyArgsSchema, location="query")
    @policy.response(200, PolicySchema(many=True))
    def get(self, args):
        return list_policies(args)

    @jwt_required()
    @admin_required
    @policy.arguments(PolicyArgsSchema)
    @policy.response(201, PolicySchema)
    def post(self, data):
        return create_policy(**data)

@policy.route("/<int:policy_id>")
class PolicyItem(MethodView):
    @jwt_required()
    @admin_required
    @policy.arguments(PolicyArgsSchema)
    def delete(self, policy_id):
        return delete_policy(policy_id)

    @jwt_required()
    @admin_required
    @policy.arguments(PolicyArgsSchema)
    @policy.response(200, PolicySchema)
    def put(self, data, policy_id):
        from ressources.policy.service import update_policy
        return update_policy(policy_id, **data)

@policy.route("/<int:policy_id>/toggle")
class PolicyToggle(MethodView):
    @jwt_required()
    @admin_required
    @policy.response(200, PolicyToggleResponseSchema)
    def post(self, policy_id):
        from ressources.policy.service import toggle_policy
        return toggle_policy(policy_id)