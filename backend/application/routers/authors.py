from fastapi import APIRouter, status, HTTPException, Request, Response
from typing import List

from application.schemas.authors import AuthorInputSchema, AuthorBaseSchema, AuthorInfoSchema
from application.schemas.books import BookBaseSchema

from domain.models import Author
from domain.usecases.authors import CreateAuthor, ReadAuthors, ReadAuthor, UpdateAuthor, DeleteAuthor, ReadBooksOfAuthor
from domain.usecases.exceptions import KeyDoesNotExist

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.get("", response_model=List[AuthorBaseSchema])
async def get_all_authors():
    """Get all authors"""
    authors = ReadAuthors().execute()
    return [author.to_schema() for author in authors]


@router.get("/{author_id}", response_model=AuthorInfoSchema)
async def get_author_by_id(author_id: int):
    """Get an author by its id"""
    try:
        author = ReadAuthor().execute(author_id)
        return author.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorBaseSchema
    )
async def create_author(request: Request, response: Response, schema: AuthorInputSchema) -> AuthorBaseSchema:
    """Create an author"""
    author: Author = schema.to_domain() 
    author = CreateAuthor().execute(author)
    response.headers["Location"] = f"{request.base_url}authors/{author.id}"
    return author


@router.put("/{author_id}", response_model=AuthorBaseSchema)
async def modify_author(author_id: int, schema: AuthorInputSchema) -> AuthorBaseSchema:
    """Modify an author"""
    
    try:
        author: Author = schema.to_domain()
        author.id = author_id
        author = UpdateAuthor().execute(author)
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


@router.get("/{author_id}/books", response_model=List[BookBaseSchema])
async def get_books_of_author(author_id: int):
    """Get all books of an author id"""
    try:
        books = ReadBooksOfAuthor().execute(author_id)
        print("Books are", books)
        return [book.to_schema() for book in books]
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))