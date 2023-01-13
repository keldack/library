from typing import List
from fastapi import APIRouter, HTTPException, status, Request, Response

from application.schemas.checkout import CheckoutInputSchema, CheckoutBaseSchema, CheckoutInfoSchema
from domain.models import Checkout
from domain.usecases.checkouts import CreateCheckout, ReadCheckout, ReadCheckouts, ModifyCheckout, ProlongateCheckout, DeleteCheckout
from domain.usecases.exceptions import KeyDoesNotExist

router = APIRouter()

from fastapi import APIRouter

router = APIRouter(
    prefix="/checkouts",
    tags=["checkouts"]
)

@router.get("", response_model=List[CheckoutBaseSchema])
async def get_all_checkouts():
    """Get all checkouts"""
    checkouts = ReadCheckouts().execute()
    return [checkout.to_schema() for checkout in checkouts]

@router.get("/{checkout_id}", response_model=CheckoutInfoSchema)
async def get_checkout_by_id(checkout_id: int):
    """Get a checkout by its id"""
    try:
        checkout = ReadCheckout().execute(checkout_id)
        return checkout.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_checkout(request: Request, response: Response, schema: CheckoutInputSchema):
    """Create a checkout"""
    checkout: Checkout = schema.to_domain()
    checkout = CreateCheckout().execute(checkout)
    response.headers["Location"] = f"{request.base_url}checkouts/{checkout.id}"
    return checkout.to_schema()


@router.put("/{checkout_id}")
async def modify_checkout(checkout_id: str, schema: CheckoutInputSchema):
    """Modify a checkout for """
    try:
        checkout: Checkout = schema.to_domain()
        checkout.id = checkout_id
        checkout = PatchCheckout().execute(checkout)
        return checkout.to_schema()
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))        


@router.delete("/{checkout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checkout(checkout_id: str):
    """Delete a checkout"""
    try:
        DeleteCheckout().execute(checkout_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
