import pytest
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from extensions import db
from ressources.services.base_service import BaseService


class TestModel(db.Model):
    __tablename__ = "test_models"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class TestService(BaseService):
    model = TestModel
    allowed_filters = {"name"}
    unique_field = "name"


@pytest.fixture
def app(app):
    """Utilise l'app Flask de tests avec DB SQLite in-memory."""
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_record(app):
    """Crée un enregistrement de tests."""
    record = TestModel(name="Sample")
    db.session.add(record)
    db.session.commit()
    return record

def test_create_success(app):
    result = TestService.create(name="Firewall A")
    assert result.id is not None
    assert result.name == "Firewall A"
    assert db.session.get(TestModel, result.id) is not None


def test_create_missing_unique_field(app):
    with pytest.raises(HTTPException) as e:
        TestService.create()
    assert e.value.code == 400


def test_create_duplicate_name(app, sample_record):
    with pytest.raises(HTTPException) as e:
        TestService.create(name="Sample")
    assert e.value.code == 409


def test_get_existing_record(app, sample_record):
    result = TestService.get(sample_record.id)
    assert result.name == "Sample"


def test_get_not_found(app):
    with pytest.raises(HTTPException) as e:
        TestService.get(999)
    assert e.value.code == 404


def test_update_success(app, sample_record):
    updated = TestService.update(sample_record.id, name="Updated")
    assert updated.name == "Updated"
    assert db.session.get(TestModel, sample_record.id).name == "Updated"


def test_update_empty_name(app, sample_record):
    with pytest.raises(HTTPException) as e:
        TestService.update(sample_record.id, name="   ")
    assert e.value.code == 400


def test_update_duplicate_name(app, sample_record):
    second = TestModel(name="Second")
    db.session.add(second)
    db.session.commit()
    with pytest.raises(HTTPException) as e:
        TestService.update(second.id, name="Sample")
    assert e.value.code == 409


def test_delete_success(app, sample_record):
    deleted = TestService.delete(sample_record.id)
    assert deleted.name == "Sample"
    assert db.session.get(TestModel, sample_record.id) is None


def test_delete_not_found(app):
    with pytest.raises(HTTPException) as e:
        TestService.delete(999)
    assert e.value.code == 404


def test_list_all(app):
    TestService.create(name="A")
    TestService.create(name="B")

    result = TestService.list()
    assert isinstance(result, list)
    assert len(result) >= 2


def test_list_with_valid_filter(app):
    TestService.create(name="FilterMe")
    results = TestService.list(filters={"name": "FilterMe"})
    assert len(results) == 1
    assert results[0].name == "FilterMe"


def test_list_with_invalid_filter(app):
    with pytest.raises(HTTPException) as e:
        TestService.list(filters={"invalid": "x"})
    assert e.value.code == 400


def test_list_with_pagination(app):
    for i in range(12):
        TestService.create(name=f"fw{i}")

    page_1 = TestService.list(page=1, per_page=5)
    assert page_1["page"] == 1
    assert len(page_1["items"]) == 5
    assert page_1["total"] >= 10
