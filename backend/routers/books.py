from fastapi import APIRouter

from domain.schemas.books import BookInputSchema

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("")
async def get_all_books():
    """Get all books"""
    return {"books": []}


@router.get("/{book_id}")
async def get_book_by_id(book_id: str):
    """Get a book by its id"""
    return {"username": "Unknown"}


@router.put("/{book_id}")
async def create_and_modify_book(book_id: str, schema: BookInputSchema):
    """Modify a book"""
    return {"username": "Unknown"}


@router.delete("/{book_id}")
async def delete_book(book_id: str):
    """Delete a book"""
    return {"username": "Unknown"}


@router.get("/{book_id}/copies")
async def get_copies_of_book(book_id: str):
    """Get all copies of a book"""
    return {"username": "Unknown"}
