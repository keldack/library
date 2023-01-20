from typing import List
import zope
from wired import service_factory

from domain.providers import IUserProvider
from domain.models import User
from domain.usecases.exceptions import KeyDoesNotExist

from config import user_db
from commons.application.dictfile import DictFile


@service_factory(for_=IUserProvider, name="basic")
@zope.interface.implementer(IUserProvider)
class UserBasicProvider():
    """
    User interaction provider managing list of users with local text file
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()

    def __init__(self):
        
        self._db = user_db
        
    # Interface implementation
    def get_all_users(self) -> List[User]:
        """
        Get all users
        """
        print ("get_all_users")
        print(self._db.container)
        return [User(**user) for user in self._db.container.values()]


    def get_user_by_identifier(self, identifier: str) -> User:
        """
        Get an user from its identifier login
        """
        user: User = None
        if identifier in self._db.container:
            user = User(**self._db.container[identifier])
        return user

    def create_user(self, user: User) -> User:
        """
        Create a new user
        """
        if user.login in self._db.container:
            raise KeyError()

        self._db.add_entry({
            "login": user.login, "email": user.email
        })
        return user