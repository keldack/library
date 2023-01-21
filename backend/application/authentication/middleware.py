# import inspect
# from typing import Tuple, Callable, List, Dict

# from fastapi import FastAPI
# from starlette.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError
# from starlette.middleware.authentication import AuthenticationMiddleware
# from starlette.requests import HTTPConnection
# from starlette.authentication import BaseUser
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


from domain.providers import IAuthenticationProvider
from domain.usecases.exceptions import CredentialException


class LibraryAuthenticationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, authentication_service: IAuthenticationProvider):
        BaseHTTPMiddleware.__init__(self, app)
        self.authentication_service = authentication_service

    async def dispatch(self, request, call_next):
        
        try:
            if "Authorization" not in request.headers:
                raise CredentialException("No Authorization in header")

            user_id: str = self.authentication_service.check_authorization(request.headers["Authorization"])
            request.user_id = user_id
            print("Middleware in nomnal case")

        except CredentialException as exception:
            print("Middleware in CredentialException")
            return Response(
                content={"message": str(exception)}, status_code = 401
            )

        response = await call_next(request)
        return response


# class FastAPIAuthBackend(AuthenticationBackend):
#     """ Auth Backend for FastAPI """

#     def __init__(self, token_verifier: IAuthenticationProvider, excluded_urls: List[str] = None):
#         """ Auth Backend constructor. Part of an AuthenticationMiddleware as backend.

#             verify_header (callable): A function handle that returns a list of scopes and a BaseUser
#             excluded_urls (List[str]): A list of URL paths (e.g. ['/login', '/contact']) the middleware should not check for user credentials ( == public routes)
#         """
#         self.token_verifier = token_verifier
#         self.excluded_urls = [] if excluded_urls is None else excluded_urls

#     async def authenticate(self, conn: HTTPConnection) -> Tuple[AuthCredentials, BaseUser]:
#         """ The 'magic' happens here. The authenticate method is invoked each time a route is called that the middleware is applied to.
#         Args:
#             conn (HTTPConnection): An HTTP connection by FastAPI/Starlette
#         Returns:
#             Tuple[AuthCredentials, BaseUser]: A tuple of AuthCredentials (scopes) and a user object that is or inherits from BaseUser
#         """
#         if conn.url.path in self.excluded_urls:
#             return AuthCredentials(scopes=[]), "Unauthenticated User"

#         try:
#             if inspect.iscoroutinefunction(self.verify_header):
#                 scopes, user = await self.verify_header(conn.headers)
#             else:
#                 scopes, user = self.verify_header(conn.headers)

#         except Exception as exception:
#             raise AuthenticationError(exception) from None

#         return AuthCredentials(scopes=scopes), user



# def AuthMiddleware(
#         app: FastAPI,
#         token_verifier: IAuthenticationProvider,
#         excluded_urls: List[str] = None
# ):
#     """ Factory method, returning an AuthenticationMiddleware
#     Intentionally not named with lower snake case convention as this is a factory method returning a class. Should feel like a class.
#     Args:
#         app (FastAPI): The FastAPI instance the middleware should be applied to. The `add_middleware` function of FastAPI adds the app as first argument by default.
#         verify_token (Callable[[str], Tuple[List[str], BaseUser]]): A function handle that returns a list of scopes and a BaseUser
#         auth_error_handler (Callable[[Request, Exception], JSONResponse]): Optional error handler for creating responses when an exception was raised in verify_authorization_header
#         excluded_urls (List[str]): A list of URL paths (e.g. ['/login', '/contact']) the middleware should not check for user credentials ( == public routes)
#     Examples:
#         ```python
#         def verify_authorization_header(auth_header: str) -> Tuple[List[str], FastAPIUser]:
#             scopes = ["admin"]
#             user = FastAPIUser(first_name="Code", last_name="Specialist", user_id=1)
#             return scopes, user
#         app = FastAPI()
#         app.add_middleware(AuthMiddleware, verify_authorization_header=verify_authorization_header)
#         ```
#     """
#     return AuthenticationMiddleware(
#         app, 
#         backend=FastAPIAuthBackend(
#             token_verifier=token_verifier, 
#             excluded_urls=excluded_urls,
#         ),
#     )
