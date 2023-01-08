from fastapi import APIRouter, status, Request, Response
from application.schemas.checkout import CheckoutInputSchema

from domain.models import Checkout
from domain.usecases.checkouts import CreateCheckout

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
async def create_checkout(request: Request, response: Response, schema: CheckoutInputSchema):
    """Create a checkout"""
    checkout: Checkout = schema.to_domain()
    checkout = CreateCheckout().execute(checkout)
    response.headers["Location"] = f"{request.base_url}checkouts/{checkout.id}"
    return checkout.to_schema()


@router.put("/{checkout_id}")
async def modify_checkout(checkout_id: str):
    """Modify a checkout"""
    return {"username": "Unknown"}


@router.delete("/{checkout_id}")
async def delete_checkout(checkout_id: str):
    """Delete a copy"""
    return {"username": "Unknown"}

