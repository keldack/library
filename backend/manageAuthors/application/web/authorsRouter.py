from fastapi import APIRouter, status, HTTPException
from persistance.schemas.authors  import AuthorSchema

from domain.usecases.authorsUC import CreateAuthor, ReadAuthors, ReadAuthor, UpdateAuthor, DeleteAuthor
from domain.usecases.exceptions import KeyDoesNotExist

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.get("")
async def get_all_authors():
    """Get all authors"""
    authors = ReadAuthors().execute()
    return [author.to_schema() for author in authors]


@router.get("/{author_id}")
async def get_author_by_id(author_id: int):
    """Get an author by its id"""
    try:
        author = ReadAuthor().execute(author_id)
        return author.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(schema: AuthorSchema) -> AuthorSchema:
    """Create an author"""
    author = CreateAuthor().execute(schema)
    return author.to_schema()


@router.put("/{author_id_id}")
async def modify_author(author_id: int, schema: AuthorSchema) -> AuthorSchema:
    """Modify an author"""
    
    try:
        author = UpdateAuthor().execute(author_id, schema)
        return author.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int):
    """Delete an author"""

    try:
        DeleteAuthor().execute(author_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


