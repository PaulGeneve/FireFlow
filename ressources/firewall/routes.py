from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask.views import MethodView

from ressources.auth.decorators import admin_required, user_or_admin_required
from ressources.firewall.schema import FirewallSchema, FirewallArgsSchema, FirewallStatisticsResponseSchema
from ressources.firewall.service import create_firewall, list_firewalls, delete_firewall
from ressources.firewall.service import get_firewall_statistics


firewall = Blueprint("firewall", __name__, url_prefix="/firewalls", description="Firewall management")

@firewall.route("/")
class FirewallsCollection(MethodView):
    @jwt_required()
    @user_or_admin_required
    @firewall.arguments(FirewallArgsSchema, location="query")
    @firewall.response(200, FirewallSchema(many=True))
    def get(self, args):
        return list_firewalls(filters=args)

    @jwt_required()
    @admin_required
    @firewall.arguments(FirewallArgsSchema)
    @firewall.response(201, FirewallSchema)
    def post(self, data):
        return create_firewall(**data)

@firewall.route("/<int:firewall_id>")
class FirewallItem(MethodView):
    @jwt_required()
    @admin_required
    @firewall.response(204)
    def delete(self, firewall_id):
       return delete_firewall(firewall_id)

    @jwt_required()
    @admin_required
    @firewall.arguments(FirewallArgsSchema)
    @firewall.response(200, FirewallSchema)
    def put(self, data, firewall_id):
        from ressources.firewall.service import update_firewall
        return update_firewall(firewall_id, **data)

@firewall.route("/<int:firewall_id>/statistics")
class FirewallStatistics(MethodView):
    @jwt_required()
    @user_or_admin_required
    @firewall.response(200, FirewallStatisticsResponseSchema)
    def get(self, firewall_id):
        return get_firewall_statistics(firewall_id)