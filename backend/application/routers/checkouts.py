from typing import List
from fastapi import APIRouter, HTTPException, status, Request, Response

from application.schemas.checkout import CheckoutInputSchema, CheckoutProlongationInputSchema, CheckoutBaseSchema, CheckoutInfoSchema
from domain.models import Checkout, Prolongation
from domain.usecases.checkouts import CreateCheckout, ReadCheckout, ReadCheckouts, ModifyCheckout, ProlongateCheckout, DeleteCheckout
from domain.usecases.exceptions import KeyDoesNotExist, CopyAlreadyCheckouted

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
        schema = checkout.to_schema()
        schema["copy_id"] = checkout.copy.id
        schema["book_isbn"] = checkout.copy.book.isbn
        schema["book_title"] = checkout.copy.book.title
        return schema
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_checkout(request: Request, response: Response, schema: CheckoutInputSchema):
    """Create a checkout"""
    try:
        checkout: Checkout = schema.to_domain()
        checkout = CreateCheckout().execute(checkout)
        response.headers["Location"] = f"{request.base_url}checkouts/{checkout.id}"
        schema = checkout.to_schema()
        schema["copy_id"] = checkout.copy.id
        schema["book_isbn"] = checkout.copy.book.isbn
        schema["book_title"] = checkout.copy.book.title
        return schema
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except CopyAlreadyCheckouted as already_exception:
        raise HTTPException(status_code=400, detail=str(already_exception))


@router.post("/{checkout_id}/prolongation", response_model=CheckoutInfoSchema)
async def prolongate_checkout(checkout_id: int, schema: CheckoutProlongationInputSchema):
    """Create a checkout"""
    prolongation: Prolongation = schema.to_domain()
    prolongation.checkout_id = checkout_id
    checkout = ProlongateCheckout().execute(prolongation)
    schema = checkout.to_schema()
    schema["copy_id"] = checkout.copy.id
    schema["book_isbn"] = checkout.copy.book.isbn
    schema["book_title"] = checkout.copy.book.title
    return schema


@router.put("/{checkout_id}", response_model=CheckoutInfoSchema)
async def modify_checkout(checkout_id: str, schema: CheckoutInputSchema):
    """Modify a checkout for """
    try:
        checkout: Checkout = schema.to_domain()
        checkout.id = checkout_id
        checkout = ModifyCheckout().execute(checkout)
        schema = checkout.to_schema()
        schema["copy_id"] = checkout.copy.id
        schema["book_isbn"] = checkout.copy.book.isbn
        schema["book_title"] = checkout.copy.book.title
        return schema
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))        
    except CopyAlreadyCheckouted as already_exception:
        raise HTTPException(status_code=400, detail=str(already_exception))

@router.delete("/{checkout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checkout(checkout_id: str):
    """Delete a checkout"""
    try:
        DeleteCheckout().execute(checkout_id)
    except KeyDoesNotExist as exception:
        raise HTTPException(status_code=404, detail=str(exception))
