from fastapi import APIRouter, status, HTTPException, Request, Response
from typing import List

from application.schemas.users import TokenBaseSchema, UserBaseSchema, UserInputSchema, LoginInputSchema
from domain.models import User
from domain.usecases.users import Login, UserMe, CreateUser, GetAllUsers, GetUser
from domain.usecases.exceptions import LoginAlreadyUsed, KeyDoesNotExist, CredentialException

public_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

private_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@public_router.post("/login", response_model=TokenBaseSchema)
async def login(schema: LoginInputSchema):
    """Login a user"""
    try:
        token = Login().execute(schema.login)
        return token.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    

@private_router.get("/me", response_model=UserBaseSchema)
async def user_me(request: Request):
    """Register a new user, very simple process just for the demo"""

    try:
        token = request.headers["authorization"]
        use_case = UserMe()
        authenticate_service = use_case.authenticate_service
        login = authenticate_service.check_authorization(token)

        user = use_case.execute(login)
        return user.to_schema()
    except CredentialException as exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception))


@private_router.post("", response_model=UserBaseSchema)
async def create_user(schema: UserInputSchema):
    """Create an user"""
    user: User = schema.to_domain() 
    try:
        user = CreateUser().execute(user)
        return user.to_schema()
    except LoginAlreadyUsed as exception:
        raise HTTPException(status_code=400, detail=str(exception))


@private_router.get("", response_model=List[UserBaseSchema])
async def get_all_users():
    """Create an user"""
    users = GetAllUsers().execute()
    return [user.to_schema() for user in users]


@private_router.get("/{identifier}", response_model=UserBaseSchema)
async def get_user(identifier: str):
    """Create an user"""
    user = GetUser().execute(identifier)
    return user.to_schema()


