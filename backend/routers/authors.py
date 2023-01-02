from fastapi import APIRouter, status, HTTPException
from domain.schemas.authors import AuthorSchema

from domain.usecases.authors import CreateAuthor, ReadAuthors, DeleteAuthor

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.get("")
async def get_all_authors():
    """Get all authors"""
    authors = ReadAuthors().execute()
    return [author.to_schema() for author in authors]


@router.get("/{user_id}")
async def get_author_by_id(user_id: int):
    """Get an author by its id"""
    return {"username": "Unknown"}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(schema: AuthorSchema) -> AuthorSchema:
    """Create an author"""
    author = CreateAuthor().execute(schema)
    return author.to_schema()


@router.put("/{user_id}")
async def modify_author(user_id: int):
    """Modify an author"""
    return {"username": "Unknown"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(user_id: int):
    """Delete an author"""
    author = DeleteAuthor().execute(user_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author does not exist")


