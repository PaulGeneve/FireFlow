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

class PolicyArgsSchema(Schema):
    name = fields.Str(required=False)
    action = fields.Str(validate=validate.OneOf(['allow', 'deny']))
    enabled = fields.Bool()
    firewall_id = fields.Int(required=False)


class PolicyToggleResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    enabled = fields.Bool()
    action = fields.Str()
    message = fields.Str()