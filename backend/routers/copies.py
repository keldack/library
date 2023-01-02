from fastapi import APIRouter

router = APIRouter()

from fastapi import APIRouter

router = APIRouter(
    prefix="/copies",
    tags=["copies"]
)

@router.get("")
async def get_all_copies():
    """Get all books"""
    return {"books": []}


@router.get("/{copy_id}")
async def get_copy_by_id(book_id: str):
    """Get a book by its id"""
    return {"username": "Unknown"}


@router.post("")
async def create_copy():
    """Get all books"""
    return {"books": []}


@router.put("/{copy_id}")
async def modify_copy(copy_id: str):
    """Modify a copy"""
    return {"username": "Unknown"}


@router.delete("/{copy_id}")
async def delete_copy(copy_id: str):
    """Delete a copy"""
    return {"username": "Unknown"}

