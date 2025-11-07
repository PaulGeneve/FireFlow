class UserRole:
    USER = 'user'
    ADMIN = 'admin'

    @classmethod
    def all(cls):
        return {cls.USER, cls.ADMIN}

    @classmethod
    def is_valid(cls, role):
        return role in cls.all()