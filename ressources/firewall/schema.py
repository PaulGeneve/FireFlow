from marshmallow import Schema, fields
from ressources.policy.schema import PolicySchema

class FirewallSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    ip_address = fields.Str(required=True)
    filtering_policies = fields.List(fields.Nested(PolicySchema), dump_only=True)


class FirewallFiltersSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=False)
    location = fields.Str(required=False)

class FirewallArgsSchema(FirewallFiltersSchema):
    page = fields.Int(
        required=False,
        load_default=1,
        metadata={'description': 'Page number for pagination'}
    )
    per_page = fields.Int(
        required=False,
        load_default=5,
        metadata={'description': 'Items per page (max 100)'},
        validate=lambda x: 1 <= x <= 100
    )

class PaginatedFirewallSchema(Schema):
    items = fields.List(fields.Nested(FirewallSchema))
    total = fields.Int(metadata={'description': 'Total number of items'})
    page = fields.Int(metadata={'description': 'Current page number'})
    per_page = fields.Int(metadata={'description': 'Items per page'})


class PolicyStatisticsSchema(Schema):
    total = fields.Int()
    active = fields.Int()
    inactive = fields.Int()
    allow = fields.Int()
    deny = fields.Int()


class RuleStatisticsSchema(Schema):
    total = fields.Int()
    in_active_policies = fields.Int()
    in_inactive_policies = fields.Int()


class StatisticsSchema(Schema):
    policies = fields.Nested(PolicyStatisticsSchema)
    rules = fields.Nested(RuleStatisticsSchema)


class FirewallStatisticsResponseSchema(Schema):
    firewall = fields.Nested(FirewallSchema)
    statistics = fields.Nested(StatisticsSchema)