from fastapi import FastAPI
from core.config import settings
from core.registry import LibraryRegistry

from routers.authors import router as authors_router
from routers.books import router as books_router
from routers.copies import router as copies_router
from routers.checkouts import router as checkouts_router

LibraryRegistry.init_registry_and_scan()

print(LibraryRegistry.check_all_registered())

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(copies_router)
app.include_router(checkouts_router)


@app.get("/")
async def hello_api():

    return {"message":f"Welcome to Library API in {settings.MODE.environment}. See /docs in API for more details"}


