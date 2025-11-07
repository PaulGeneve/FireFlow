from extensions import db
from models.user import User
from models.firewalls import Firewalls
from models.filtering_policy import FilteringPolicy
from models.rules import Rules
from ressources.auth.constant import UserRole


def seed_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        users = create_users()
        firewalls = create_firewalls()
        policies = create_policies(firewalls)
        rules = create_rules(policies)
        print(f"   - {len(users)} users")
        print(f"   - {len(firewalls)} firewalls")
        print(f"   - {len(policies)} policies")
        print(f"   - {len(rules)} rules")


def create_users():
    users = [
        {
            'name': 'paul',
            'email': 'paul@example.com',
            'password': 'paul123',
            'role': UserRole.ADMIN
        },
        {
            'name': 'thomas',
            'email': 'thomas@example.com',
            'password': 'thomas123',
            'role': UserRole.USER
        },
        {
            'name': 'enzo',
            'email': 'enzo@example.com',
            'password': 'enzo123',
            'role': UserRole.USER
        },
    ]

    user_objects = []
    for user_data in users:
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            role=user_data['role']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        user_objects.append(user)

    db.session.commit()
    return user_objects


def create_firewalls():
    firewalls_data = [
        {
            'name': 'FW-PROD-01',
            'ip_address': '192.168.1.1',
            'location': 'Paris DC1'
        },
        {
            'name': 'FW-PROD-02',
            'ip_address': '192.168.1.2',
            'location': 'Paris DC2'
        },
        {
            'name': 'FW-DEV-01',
            'ip_address': '10.0.1.1',
            'location': 'Dev Environment'
        },
    ]

    firewall_objects = []
    for fw_data in firewalls_data:
        fw = Firewalls(**fw_data)
        db.session.add(fw)
        firewall_objects.append(fw)

    db.session.commit()
    return firewall_objects


def create_policies(firewalls):
    policies_data = [
        {
            'name': 'ALLOW-WEB',
            'firewall_id': firewalls[0].id,
            'enabled': True,
            'action': 'allow'
        },
        {
            'name': 'DENY-ALL',
            'firewall_id': firewalls[0].id,
            'enabled': False,
            'action': 'deny'
        },
        {
            'name': 'ALLOW-SSH',
            'firewall_id': firewalls[1].id,
            'enabled': True,
            'action': 'allow'
        },
        {
            'name': 'DEV-ALLOW-ALL',
            'firewall_id': firewalls[2].id,
            'enabled': True,
            'action': 'allow'
        },
    ]

    policy_objects = []
    for policy_data in policies_data:
        policy = FilteringPolicy(**policy_data)
        db.session.add(policy)
        policy_objects.append(policy)

    db.session.commit()
    return policy_objects


def create_rules(policies):
    rules_data = [
        {
            'name': 'HTTP-RULE',
            'filtering_policy_id': policies[0].id,
            'source': '0.0.0.0/0',
            'destination': '192.168.1.100',
            'port': '80',
        },
        {
            'name': 'HTTPS-RULE',
            'filtering_policy_id': policies[0].id,
            'source': '0.0.0.0/0',
            'destination': '192.168.1.100',
            'port': '443',
        },
        {
            'name': 'SSH-ADMIN',
            'filtering_policy_id': policies[2].id,
            'source': '10.0.0.0/24',
            'destination': '192.168.1.1',
            'port': '22',
        },
    ]

    rule_objects = []
    for rule_data in rules_data:
        rule = Rules(**rule_data)
        db.session.add(rule)
        rule_objects.append(rule)

    db.session.commit()
    return rule_objects
