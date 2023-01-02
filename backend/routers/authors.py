from fastapi import APIRouter
from domain.schemas.authors import AuthorSchema

from domain.usecases.authors import CreateAuthor

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.get("")
async def get_all_authors():
    """Get all authors"""
    return {"authors": []}


@router.get("/{user_id}")
async def get_author_by_id(user_id: int):
    """Get an author by its id"""
    return {"username": "Unknown"}


@router.post("")
async def create_author(schema: AuthorSchema) -> AuthorSchema:
    """Create an author"""
    author = CreateAuthor().execute(schema)
    return author.to_schema()


@router.put("/{user_id}")
async def modify_author(user_id: int):
    """Modify an author"""
    return {"username": "Unknown"}


@router.delete("/{user_id}")
async def delete_author(user_id: int):
    """Delete an author"""
    return {"username": "Unknown"}

