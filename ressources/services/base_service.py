from sqlalchemy.exc import IntegrityError
from flask_smorest import abort
from extensions import db

class BaseService:
    """
    Generic base service for CRUD operations.
    Uses repository pattern to isolate business logic from persistence.

    Attributes:
        model: SQLAlchemy model class
        allowed_filters: Set of filterable field names
        unique_field: Field name for uniqueness validation (default: 'name')
    """
    model = None
    allowed_filters = set()
    unique_field = 'name'

    @classmethod
    def create(cls, **data):
        """
        Creates a new record in the database.

        :param data: Record attributes
        :return: Created model instance
        :raises: 400 if unique field is missing, 409 if already exists
        """
        unique_value = data.get(cls.unique_field, "").strip()
        if not unique_value:
            abort(400, message=f"{cls.unique_field.capitalize()} is required")

        try:
            instance = cls.model(**data)
            db.session.add(instance)
            db.session.commit()
            return instance
        except IntegrityError:
            db.session.rollback()
            abort(409, message=f"A {cls.model.__tablename__[:-1]} with this {cls.unique_field} already exists")

    @classmethod
    def get(cls, record_id):
        """
        Retrieves a record by its primary key.

        :param record_id: Record ID
        :return: Model instance
        :raises: 404 if not found
        """
        instance = db.session.get(cls.model, record_id)
        if not instance:
            abort(404, message=f"{cls.model.__tablename__.capitalize()[:-1]} not found")
        return instance

    @classmethod
    def update(cls, record_id, **data):
        """
        Updates an existing record.

        :param record_id: Record ID
        :param data: Fields to update
        :return: Updated model instance
        :raises: 404 if not found, 400 if validation fails, 409 if unique constraint violated
        """
        instance = cls.get(record_id)

        if cls.unique_field in data:
            unique_value = data[cls.unique_field].strip()
            if not unique_value:
                abort(400, message=f"{cls.unique_field.capitalize()} cannot be empty")
            data[cls.unique_field] = unique_value

        try:
            for key, value in data.items():
                setattr(instance, key, value)
            db.session.commit()
            return instance
        except IntegrityError:
            db.session.rollback()
            abort(409, message=f"A {cls.model.__tablename__[:-1]} with this {cls.unique_field} already exists")

    @classmethod
    def delete(cls, record_id):
        """
        Deletes a record by its ID.

        :param record_id: Record ID
        :return: Deleted model instance
        :raises: 404 if not found
        """
        instance = cls.get(record_id)
        db.session.delete(instance)
        db.session.commit()
        return {"message": f"{cls.model.__tablename__.capitalize()[:-1]} deleted successfully"}

    @classmethod
    def list(cls, filters=None, page=None, per_page=2):
        """
        Lists records with optional filtering and pagination.

        :param filters: Dict of filter criteria (only allowed_filters are accepted)
        :param page: Page number for pagination (optional)
        :param per_page: Items per page (max 100, default 50)
        :return: List of model instances or paginated dict with items/total/page/per_page
        :raises: 400 if invalid filter provided
        """
        query = db.select(cls.model)

        if filters:
            for attr, value in filters.items():
                if attr not in cls.allowed_filters:
                    abort(400, message=f"Invalid filter: {attr}")

                if value is None or (isinstance(value, str) and not value.strip()):
                    abort(400, message=f"Filter '{attr}' cannot be empty")

                query = query.filter(getattr(cls.model, attr) == value)

        if page is not None:
            per_page = min(per_page, 100)
            total = db.session.scalar(db.select(db.func.count()).select_from(query.subquery()))
            items = db.session.scalars(query.offset((page - 1) * per_page).limit(per_page)).all()

            return {
                'items': items,
                'total': total,
                'page': page,
                'per_page': per_page
            }
        results = db.session.scalars(query).all()

        if filters and not results:
            abort(404, message=f"No {cls.model.__tablename__} found matching the provided filters")

        return results