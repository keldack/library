from typing import List
from fastapi import APIRouter, HTTPException, status, Request, Response

from application.schemas.books import BookInputSchema, BookBaseSchema, BookInfoSchema
from application.schemas.authors import AuthorBaseSchema
from domain.models import Book
from domain.usecases.books import CreateBook, ReadBooks, ReadBook, UpdateBook, DeleteBook, GetCopiesOfBook
from domain.usecases.exceptions import KeyDoesNotExist, ISBNAlreadyUsed

public_router = APIRouter(
    prefix="/books",
    tags=["books"]
)

private_router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@public_router.get("", response_model=List[BookBaseSchema])
async def get_all_books():
    """Get all books"""
    books = ReadBooks().execute()
    return [book.to_schema() for book in books]


@public_router.get("/{book_id}", response_model=BookInfoSchema)
async def get_book_by_id(book_id: int):
    """Get a book by its id"""
    try:
        book = ReadBook().execute(book_id)
        
        # Special remove ok books reference for iside authors
        schema = BookInfoSchema(
            id=book.id, 
            isbn=book.isbn, 
            title=book.title,
            authors = [
                AuthorBaseSchema(id=author.id, name = author.name) for author in book.authors
            ]
        )
        return schema

    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@private_router.post("", status_code=status.HTTP_201_CREATED, response_model=BookInfoSchema)
async def create_book(request: Request, response: Response, schema: BookInputSchema):
    """Create a book"""
    
    try:
        book: Book = schema.to_domain()
        book = CreateBook().execute(book)
        response.headers["Location"] = f"{request.base_url}books/{book.id}"
        return book.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except ISBNAlreadyUsed as isbn_exception:
        raise HTTPException(status_code=400, detail=str(isbn_exception))
    

@private_router.put("/{book_id}", response_model=BookInfoSchema)
async def modify_book(book_id: str, schema: BookInputSchema):
    """Modify a book"""
    try:
        book: Book = schema.to_domain()
        book.id = book_id
        book = UpdateBook().execute(book)
        return book.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except ISBNAlreadyUsed as isbn_exception:
        raise HTTPException(status_code=400, detail=str(isbn_exception))


@private_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete a book"""
    
    try:
        DeleteBook().execute(book_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@public_router.get("/{book_id}/copies")
async def get_copies_of_book(book_id: int):
    """Get all copies of a book"""
    
    try:
        return GetCopiesOfBook().execute(book_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    
