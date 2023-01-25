import os
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

# As we use Django, just a trace of it

# import importlib.util
# import sys

# from django.core.asgi import get_asgi_application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.persistence.unchained.unchained.settings')
# django_application = get_asgi_application()

# # print("CWD", os.getcwd())
# # library_file = os.getcwd() + "/application/persistence/unchained/library/__init__.py"
# # spec = importlib.util.spec_from_file_location("library", library_file)
# # library_module = importlib.util.module_from_spec(spec)
# # sys.modules["library"] = library_module
# # spec.loader.exec_module(library_module)


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


from commons.fastapi.extension import test_decorateur

@app.get("/") 
@test_decorateur
async def hello_api(request: Request):
    environment = settings.MODE["environment"]
    return {
        "message":f"Welcome to Library API in {environment}. See /docs in API for more details",
    }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info") 