from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from ressources.auth.decorators import admin_required, user_or_admin_required
from ressources.common.schemas import Error404Schema, Error409Schema, Error400Schema
from ressources.rules.schema import RuleSchema, RuleArgsSchema
from ressources.rules.service import list_rules, create_rule, delete_rule

rule = Blueprint('rule', __name__, url_prefix='/rules', description='Rule management')

@rule.route('/')
class RuleCollection(MethodView):
    @jwt_required()
    @user_or_admin_required
    @rule.arguments(RuleArgsSchema, location='query')
    @rule.response(200, RuleSchema(many=True))
    @rule.alt_response(400, schema=Error400Schema, description="Invalid filter")
    def get(self, args):
        return list_rules(args)

    @jwt_required()
    @admin_required
    @rule.arguments(RuleArgsSchema)
    @rule.response(201, RuleSchema)
    @rule.alt_response(409, schema=Error409Schema, description="Rule already exists")
    def post(self, data):
        return create_rule(**data)

@rule.route('/<int:rule_id>')
class RuleItem(MethodView):
    @jwt_required()
    @admin_required
    @rule.response(204, description="Rule deleted")
    @rule.alt_response(404, schema=Error404Schema, description="Rule not found")
    def delete(self, rule_id):
        return delete_rule(rule_id)

    @jwt_required()
    @admin_required
    @rule.arguments(RuleArgsSchema)
    @rule.response(200, RuleSchema)
    @rule.alt_response(404, schema=Error404Schema, description="Rule not found")
    @rule.alt_response(409, schema=Error409Schema, description="Name already exists")
    def put(self, data, rule_id):
        from ressources.rules.service import update_rule
        return update_rule(rule_id, **data)