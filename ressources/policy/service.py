from flask_smorest import abort
from models.filtering_policy import FilteringPolicy
from extensions import db
from ressources.services.base_service import BaseService
from ressources.firewall.service import get_firewall


class PolicyService(BaseService):
    model = FilteringPolicy
    allowed_filters = {'id', 'name', 'firewall_id', 'enabled', 'action'}


def create_policy(**data):
    """Crée une policy. Peut valider que le firewall existe."""
    if 'firewall_id' in data:
        get_firewall(data['firewall_id'])

    return PolicyService.create(**data)


def get_policy(policy_id):
    return PolicyService.get(policy_id)


def update_policy(policy_id, **data):
    return PolicyService.update(policy_id, **data)


def delete_policy(policy_id):
    return PolicyService.delete(policy_id)


def list_policies(filters=None, page=None, per_page=50):
    return PolicyService.list(filters, page, per_page)


def toggle_policy(policy_id):
    """
    Enables or disables a policy without deleting it.
    Useful for temporary maintenance or testing.

    :param policy_id: ID de la policy
    :return: Dict avec le nouvel état
    """
    policy = db.session.get(FilteringPolicy, policy_id)

    if not policy:
        abort(404, message="Policy not found")

    policy.enabled = not policy.enabled
    db.session.commit()

    return {
        'id': policy.id,
        'name': policy.name,
        'enabled': policy.enabled,
        'action': policy.action,
        'message': f"Policy '{policy.name}' {'enabled' if policy.enabled else 'disabled'} successfully"
    }
