from flask_login import UserMixin


class User(UserMixin):
    __users__ = {}
    __slots__ = ('name', 'account')

    @property
    def is_authenticated(self):
        """return True if the user is authenticated
        """
        return True

    @property
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    @staticmethod
    def get(name):
        return User.__users__.get(name)

    @staticmethod
    def save(user):
        User.__users__[user.get_id()] = user

    @staticmethod
    def delete(user):
        if User.__users__.get(user.get_id()):
            del User.__users__[user.get_id()]
