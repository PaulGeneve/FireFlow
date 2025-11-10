from flask_smorest import abort
from models.rules import Rules
from extensions import db

from ressources.services.base_service import BaseService
from models.rules import Rules
from ressources.policy.service import get_policy



class RuleService(BaseService):
    model = Rules
    allowed_filters = {'id', 'name', 'policy_id', 'source', 'destination'}
    unique_field = 'name'


def create_rule(**data):
    if 'policy_id' in data:
        get_policy(data['policy_id'])

    return RuleService.create(**data)

def get_rule(rule_id):
    return RuleService.get(rule_id)

def update_rule(rule_id, **data):
    return RuleService.update(rule_id, **data)

def delete_rule(rule_id):
    return RuleService.delete(rule_id)

def list_rules(filters=None, page=None, per_page=50):
    return RuleService.list(filters, page, per_page)
