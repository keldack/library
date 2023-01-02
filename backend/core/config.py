from pydantic import BaseSettings
from . import version, name as project_name

dev = {
    "environment": "development", 
    "persistence": "memory"
}

staging = {
    "environment": "staging", 
    "persistence": "memory"
}

prod = {
    "environment": "production", 
    "persistence": "django"
}

class Settings(BaseSettings):

    PROJECT_NAME:str = project_name
    PROJECT_VERSION:str = version
    MODE = dev

settings = Settings()