from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask.views import MethodView

from ressources.auth.decorators import admin_required, user_or_admin_required
from ressources.common.schemas import ErrorSchema, Error400Schema, Error409Schema, Error404Schema
from ressources.firewall.schema import FirewallSchema, FirewallArgsSchema, FirewallStatisticsResponseSchema, \
    PaginatedFirewallSchema
from ressources.firewall.service import create_firewall, list_firewalls, delete_firewall, get_firewall
from ressources.firewall.service import get_firewall_statistics


firewall = Blueprint("firewall", __name__, url_prefix="/firewalls", description="Firewall management")

@firewall.route("/")
class FirewallsCollection(MethodView):
    @jwt_required()
    @user_or_admin_required
    @firewall.arguments(FirewallArgsSchema, location="query")
    @firewall.response(200, FirewallSchema(many=True), description="List of firewalls")
    @firewall.response(200, PaginatedFirewallSchema, description="Paginated list of firewalls")
    @firewall.alt_response(400, schema=Error400Schema, description="Invalid filter")
    @firewall.alt_response(404, schema=Error404Schema, description="No results")
    def get(self, args):
        print(f"DEBUG - args brut: {args}")
        print(f"DEBUG - 'page' in args: {'page' in args}")
        print(f"DEBUG - args.get('page'): {args.get('page')}")
        page = args.get('page')
        per_page = args.get('per_page') or 10
        filters = {k: v for k, v in args.items() if k not in ['page', 'per_page']}

        print(f"DEBUG - page={page}, per_page={per_page}, filters={filters}")
        response = list_firewalls(filters=filters, page=page, per_page=per_page)
        print(f"DEBUG - result type: {type(response)}")

        return response

    @jwt_required()
    @admin_required
    @firewall.arguments(FirewallArgsSchema)
    @firewall.response(201, FirewallSchema)
    @firewall.alt_response(409, schema=Error409Schema, description="Firewall already exists")
    def post(self, data):
        return create_firewall(**data)

@firewall.route("/<int:firewall_id>")
class FirewallItem(MethodView):
    @jwt_required()
    @admin_required
    @firewall.response(204, description="Firewall deleted")
    @firewall.alt_response(404, schema=Error404Schema, description="Firewall not found")
    def delete(self, firewall_id):
        return delete_firewall(firewall_id)

    @jwt_required()
    @admin_required
    @firewall.arguments(FirewallArgsSchema)
    @firewall.response(200, FirewallSchema)
    @firewall.alt_response(404, schema=Error404Schema, description="Firewall not found")
    @firewall.alt_response(409, schema=Error409Schema, description="Name already exists")
    def put(self, data, firewall_id):
        from ressources.firewall.service import update_firewall
        return update_firewall(firewall_id, **data)

@firewall.route("/<int:firewall_id>/statistics")
class FirewallStatistics(MethodView):
    @jwt_required()
    @user_or_admin_required
    @firewall.response(200, FirewallStatisticsResponseSchema)
    @firewall.alt_response(404, schema=Error404Schema, description="Firewall not found")
    def get(self, firewall_id):
        return get_firewall_statistics(firewall_id)