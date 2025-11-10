from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from models.filtering_policy import FilteringPolicy
from models.firewalls import Firewalls
from extensions import db
from ressources.services.base_service import BaseService
from utils import check_allowed_filter

class FirewallService(BaseService):
    model = Firewalls
    allowed_filters = {'id', 'name', 'location', 'ip_address'}


def create_firewall(**data):
    return FirewallService.create(**data)


def get_firewall(firewall_id):
    return FirewallService.get(firewall_id)


def update_firewall(firewall_id, **data):
    return FirewallService.update(firewall_id, **data)


def delete_firewall(firewall_id):
    return FirewallService.delete(firewall_id)


def list_firewalls(filters=None, page=None, per_page=50):
    return FirewallService.list(filters, page, per_page)

def get_firewall_statistics(firewall_id):
    """
    Retrieves detailed statistics for a firewall.

    :param firewall_id: Firewall ID
    :return: Dict with firewall info and statistics
    """
    from sqlalchemy.orm import joinedload

    fw = db.session.scalar(
        db.select(Firewalls)
        .options(joinedload(Firewalls.filtering_policies).joinedload(FilteringPolicy.rules))
        .filter_by(id=firewall_id)
    )

    if not fw:
        abort(404, message="Firewall not found")

    # Calculs des statistiques
    total_policies = len(fw.filtering_policies)
    active_policies = sum(1 for p in fw.filtering_policies if p.enabled)
    inactive_policies = total_policies - active_policies

    allow_policies = sum(1 for p in fw.filtering_policies if p.action == 'allow')
    deny_policies = sum(1 for p in fw.filtering_policies if p.action == 'deny')

    total_rules = sum(len(p.rules) for p in fw.filtering_policies)
    rules_in_active_policies = sum(len(p.rules) for p in fw.filtering_policies if p.enabled)

    return {
        'firewall': {
            'id': fw.id,
            'name': fw.name,
            'location': fw.location,
            'ip_address': fw.ip_address
        },
        'statistics': {
            'policies': {
                'total': total_policies,
                'active': active_policies,
                'inactive': inactive_policies,
                'allow': allow_policies,
                'deny': deny_policies
            },
            'rules': {
                'total': total_rules,
                'in_active_policies': rules_in_active_policies,
                'in_inactive_policies': total_rules - rules_in_active_policies
            }
        }
    }