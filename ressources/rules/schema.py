import re
from marshmallow import Schema, fields, validates, ValidationError

class RuleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    source = fields.Str(required=True)
    destination = fields.Str(required=True)
    filtering_policy_id = fields.Int(load_only=True)

class RuleArgsSchema(Schema):
    name = fields.Str(required=False)
    source = fields.Str(required=False)
    destination = fields.Str(required=False)
    port = fields.Str(required=False)
    filtering_policy_id = fields.Int(required=False)

class RuleFilterSchema(Schema):
    """Schéma contenant uniquement les filtres métier"""
    name = fields.Str(required=False)
    source = fields.Str(required=False)
    destination = fields.Str(required=False)
    filtering_policy_id = fields.Int(required=False)

class RuleArgsSchema(RuleFilterSchema):
    """Schéma qui hérite des filtres et ajoute la pagination"""
    page = fields.Int(
        required=False,
        load_default=1,
        metadata={'description': 'Page number for pagination'}
    )
    per_page = fields.Int(
        required=False,
        load_default=10,
        metadata={'description': 'Items per page (max 100, default 2)'}
    )

class PaginatedRuleSchema(Schema):
    items = fields.List(fields.Nested(RuleSchema))
    total = fields.Int(metadata={'description': 'Total number of items'})
    page = fields.Int(metadata={'description': 'Current page number'})
    per_page = fields.Int(metadata={'description': 'Items per page'})


@validates('source')
def validate_source(self, value):
    """Valide le format CIDR"""
    if value and not self._is_valid_cidr(value):
        raise ValidationError("Invalid CIDR format (e.g., 192.168.1.0/24 or 0.0.0.0/0)")

@validates('destination')
def validate_destination(self, value):
    """Valide le format IP ou CIDR."""
    if value and not self._is_valid_cidr(value) and not self._is_valid_ip(value):
        raise ValidationError("Invalid IP or CIDR format")

@validates('port')
def validate_port(self, value):
    """Valide le format port (80, 443, 8000-8100, etc.)."""
    if value and not re.match(r'^\d+(-\d+)?$', value):
        raise ValidationError("Invalid port format (e.g., 80 or 8000-8100)")

@staticmethod
def _is_valid_cidr(value):
    """Valide un CIDR basique."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    return bool(re.match(pattern, value))

@staticmethod
def _is_valid_ip(value):
    """Valide une IP basique."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return bool(re.match(pattern, value))

