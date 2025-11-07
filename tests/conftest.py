import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
from app import create_app
from extensions import db

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    })
    with app.app_context():
        yield app

@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()