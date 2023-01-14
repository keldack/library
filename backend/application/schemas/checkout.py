from datetime import date
from typing import Optional
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from application.schemas.copies import CopyBaseSchema
from application.schemas.books import BookBaseSchema
from domain.models import Checkout, Copy, Prolongation


@zope.interface.implementer(IInputSchema)
class CheckoutInputSchema(BaseModel):
    """
    Schema used for creation and update of a book from application
    """
    id: int | None = None
    copy_id: int
    borrower: str

    def to_domain(self) -> Checkout:
        
        return Checkout(
            id = self.id, 
            borrower = self.borrower,
            copy = Copy(id=self.copy_id),
        )

@zope.interface.implementer(IInputSchema)
class CheckoutProlongationInputSchema(BaseModel):
    """
    Schema for checkout prolongation
    """
    days: int
    checkout_id: int | None = None

    def to_domain(self) -> Prolongation:
        
        return Prolongation(days = self.days, checkout_id = self.checkout_id)

# Output Schemas
class CheckoutBaseSchema(BaseModel):

    id: int
    on_date: date
    return_date: date
    borrower: str
    

class CheckoutInfoSchema(CheckoutBaseSchema):
    
    copy_id: int
    book_isbn: str
    book_title: str
