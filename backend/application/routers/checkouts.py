from fastapi import APIRouter, HTTPException, status, Request, Response

from application.schemas.checkout import CheckoutSchema
from domain.models import Checkout
from domain.usecases.checkouts import CreateCheckout, ReadCheckout, ReadCheckouts, PatchCheckout, DeleteCheckout
from domain.usecases.exceptions import KeyDoesNotExist

router = APIRouter()

from fastapi import APIRouter

router = APIRouter(
    prefix="/checkouts",
    tags=["checkouts"]
)

@router.get("")
async def get_all_checkouts():
    """Get all checkouts"""
    checkouts = ReadCheckouts().execute()
    return [checkout.to_schema() for checkout in checkouts]

@router.get("/{checkout_id}")
async def get_checkout_by_id(checkout_id: int):
    """Get a checkout by its id"""
    try:
        checkout = ReadCheckout().execute(checkout_id)
        return checkout.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))

@router.post("")
async def create_checkout(request: Request, response: Response, schema: CheckoutSchema):
    """Create a checkout"""
    checkout: Checkout = schema.to_domain()
    checkout = CreateCheckout().execute(checkout)
    response.headers["Location"] = f"{request.base_url}checkouts/{checkout.id}"
    return checkout.to_schema()


@router.patch("/{checkout_id}")
async def modify_checkout(checkout_id: str, schema: CheckoutSchema):
    """Modify a checkout for """
    try:
        checkout: Checkout = schema.to_domain()
        checkout.id = checkout_id
        checkout = PatchCheckout().execute(checkout)
        return checkout.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))        

@router.delete("/{checkout_id}")
async def delete_checkout(checkout_id: str):
    """Delete a checkout"""
    try:
        DeleteCheckout().execute(checkout_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
