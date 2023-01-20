import zope.interface
from datetime import datetime, timedelta
from wired import service_factory
from jose import jwt, JWTError

from config import settings

from domain.providers import IAuthenticationProvider
from domain.models import User, Token
from domain.usecases.exceptions import CredentialException


@service_factory(for_=IAuthenticationProvider, name="jwt")
@zope.interface.implementer(IAuthenticationProvider)
class JWTAuthenticationService:
    """
    Service for JWT authentication
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()


    def authenticate(self, user: User):
        """
        Authenticate user and generate token
        """
        
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"user": user.login, "expire": expire.isoformat()}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return Token(token=encoded_jwt, type="Bearer")


    def check_authorization(self, token: str) -> str:
        """
        Check token authorization
        """
        try:
            parts = token.split()
            payload = jwt.decode(parts[1], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError as jwt_error:
            print("ERROR - Check_authorization JWTError", jwt_error)
            raise CredentialException("Invalid credentials")

        if datetime.utcnow().isoformat() > payload["expire"]:
            raise CredentialException("Token expired")    
            
        return payload["user"]
            
        
