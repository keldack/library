from typing import Any

from fastapi import FastAPI, Request
from config import settings
from config.registry import LibraryRegistry

from application.routers.authors import public_router as authors_public_router
from application.routers.authors import private_router as authors_private_router
from application.routers.books import public_router as books_public_router
from application.routers.books import private_router as books_private_router
from application.routers.copies import router as copies_router
from application.routers.checkouts import router as checkouts_router
from application.routers.users import public_router as users_public_router
from application.routers.users import private_router as users_private_router

from application.authentication.middleware import LibraryAuthenticationMiddleware

from domain.providers import IAuthenticationProvider


LibraryRegistry.init_registry_and_scan()

print(LibraryRegistry.check_all_registered())

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

if settings.WITH_AUTHENTICATION:
    public_app = FastAPI()
    private_app = FastAPI()

    public_app.include_router(users_public_router)
    public_app.include_router(authors_public_router)
    public_app.include_router(books_public_router)

    private_app.include_router(users_private_router)
    private_app.include_router(authors_private_router)
    private_app.include_router(books_private_router)
    private_app.include_router(copies_router)
    private_app.include_router(checkouts_router)

    private_app = LibraryAuthenticationMiddleware(
        private_app,
        authentication_service=LibraryRegistry.get_registry().create_container().get(
            IAuthenticationProvider, 
            name=settings.MODE["authentication"],
        )
    )

    app.mount(path="/", app=public_app)
    app.mount(path="/", app=private_app)

else:    

    app.include_router(users_public_router)
    app.include_router(authors_public_router)
    app.include_router(books_public_router)
    app.include_router(users_private_router)
    app.include_router(authors_private_router)
    app.include_router(books_private_router)
    app.include_router(copies_router)
    app.include_router(checkouts_router)



@app.get("/") 
async def hello_api(request: Request):
    environment = settings.MODE["environment"]
    return {
        "message":f"Welcome to Library API in {environment}. See /docs in API for more details",
    }
