from typing import Optional
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema

from domain.models import User

@zope.interface.implementer(IInputSchema)
class UserInputSchema(BaseModel):
    """
    Schema used for user creation
    """
    login: str
    email: str
    password: str
    
    def to_domain(self) -> User:

        return User(
            login=self.login, 
            email=self.email, 
            password=self.password
        )

@zope.interface.implementer(IInputSchema)
class LoginInputSchema(BaseModel):
    """
    Schema for login process
    """
    login: str


# Output schemas
class TokenBaseSchema(BaseModel):
    """
    Schema to return token
    """
    token: str
    type: str


class UserBaseSchema(BaseModel):
    """
    Base schema when returning user information
    """
    login: str
    email: str
