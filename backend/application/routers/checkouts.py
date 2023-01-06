from fastapi import APIRouter

router = APIRouter()

from fastapi import APIRouter

router = APIRouter(
    prefix="/checkouts",
    tags=["checkouts"]
)

@router.get("")
async def get_all_checkouts():
    """Get all checkouts"""
    return {"checkouts": []}


@router.get("/{checkout_id}")
async def get_checkout_by_id(checkout_id: int):
    """Get a checkout by its id"""
    return {"username": "Unknown"}


@router.post("")
async def create_checkout():
    """Create a checkout"""
    return {"books": []}


@router.put("/{checkout_id}")
async def modify_checkout(checkout_id: str):
    """Modify a checkout"""
    return {"username": "Unknown"}


@router.delete("/{checkout_id}")
async def delete_checkout(checkout_id: str):
    """Delete a copy"""
    return {"username": "Unknown"}

