from marshmallow import Schema, fields, validates, ValidationError, validate
from ressources.rules.schema import RuleSchema


class PolicySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    action = fields.Str(required=True, validate=validate.OneOf(['allow', 'deny']))
    enabled = fields.Bool(required=True)
    firewall_id = fields.Int(load_only=True)
    rules = fields.List(fields.Nested(RuleSchema), dump_only=True)

@validates('action')
def validate_action(self, value):
    if value not in ['allow', 'deny']:
        raise ValidationError("Action must be 'allow' or 'deny'")

class PolicyFiltersSchema(Schema):
    name = fields.Str(required=False)
    action = fields.Str(validate=validate.OneOf(['allow', 'deny']))
    enabled = fields.Bool()
    firewall_id = fields.Int(required=False)

class PolicyArgsSchema(PolicyFiltersSchema):
    page = fields.Int(
        required=False,
        load_default=1,
        metadata={'description': 'Page number for pagination'}
    )
    per_page = fields.Int(
        required=False,
        load_default=10,
        metadata={'description': 'Items per page (max 100)'},
        validate=lambda x: 1 <= x <= 100
    )

class PaginatedPolicySchema(Schema):
    items = fields.List(fields.Nested(PolicySchema))
    total = fields.Int(metadata={'description': 'Total number of items'})
    page = fields.Int(metadata={'description': 'Current page number'})
    per_page = fields.Int(metadata={'description': 'Items per page'})

class PolicyToggleResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    enabled = fields.Bool()
    action = fields.Str()
    message = fields.Str()