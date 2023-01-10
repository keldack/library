from typing import Any

from fastapi import FastAPI, Request
from config import settings
from config.registry import LibraryRegistry

from application.routers.authors import router as authors_router
from application.routers.books import router as books_router
from application.routers.copies import router as copies_router
from application.routers.checkouts import router as checkouts_router

LibraryRegistry.init_registry_and_scan()

print(LibraryRegistry.check_all_registered())

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(copies_router)
app.include_router(checkouts_router)


@app.get("/") 
async def hello_api(request: Request):
    environment = settings.MODE["environment"]
    return {
        "message":f"Welcome to Library API in {environment}. See /docs in API for more details",
    }
