from typing import List
import zope.interface
from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import User
from domain.providers import IUserProvider, IAuthenticationProvider
from domain.usecases.exceptions import KeyDoesNotExist, LoginAlreadyUsed


@zope.interface.implementer(IUseCase)
class CreateUser(UseCaseWrapper):
    """Use case for user creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.user_repository: IUserProvider = self.inject(IUserProvider, "user")

    def execute(self, user: User):

        # Ensure login available
        found_user = self.user_repository.get_user_by_identifier(user.login)
        if not found_user:
            # Login is available, we can create the user
            user = self.user_repository.create_user(user)
            return user
        else:
            raise LoginAlreadyUsed(f"Login '{user.login}' already used")


@zope.interface.implementer(IUseCase)
class UserMe(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.user_repository: IUserProvider = self.inject(IUserProvider, "user")
        self.authenticate_service: IAuthenticationProvider = self.inject(IAuthenticationProvider, "authentication")

    def execute(self, login: str):
        return self.user_repository.get_user_by_identifier(login)



@zope.interface.implementer(IUseCase)
class Login(UseCaseWrapper):
    """
    Log in the user with login
    """
    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.user_repository: IUserProvider = self.inject(IUserProvider, "user")
        self.authenticate_service: IAuthenticationProvider = self.inject(IAuthenticationProvider, "authentication")

    def execute(self, login: str):
        user = self.user_repository.get_user_by_identifier(login)
        # TO DO : user as authentication result ....
        if user is None:
            raise KeyDoesNotExist(f"Invalid login '{login}'")

        # TO DO: then generate token
        token = self.authenticate_service.authenticate(user)

        return token

@zope.interface.implementer(IUseCase)
class GetAllUsers(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.user_repository: IUserProvider = self.inject(IUserProvider, "user")

    def execute(self) -> List[User]:
        return self.user_repository.get_all_users()


@zope.interface.implementer(IUseCase)
class GetUser(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.user_repository: IUserProvider = self.inject(IUserProvider, "user")

    def execute(self, user_login: str) -> User:
        user = self.user_repository.get_user_by_identifier(user_login)
        if not user:
            raise KeyDoesNotExist(f"No user for login '{user_login}'")
