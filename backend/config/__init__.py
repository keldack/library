import os
from dotenv import load_dotenv
from pydantic import BaseSettings
from application import version

load_dotenv()

dev = {
    "environment": "development", 
    "persistence": "memory",
    "user": "basic",
    "authentication": "jwt",
}

staging = {
    "environment": "staging", 
    "persistence": "memory",
    "user": "basic",
    "authentication": "jwt",
}

prod = {
    "environment": "production", 
    "persistence": "django",
    "user": "basic",
    "authentication": "jwt",
}

class Settings(BaseSettings):

    PROJECT_NAME:str = "Library"
    PROJECT_VERSION:str = version
    MODE = dev

    #Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"                         
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    WITH_AUTHENTICATION = False

settings = Settings()

from commons.application.dictfile import DictFile

user_db = DictFile("users.txt", "login")