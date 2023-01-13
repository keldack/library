from datetime import date
from typing import Optional
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from application.schemas.copies import CopyBaseSchema
from application.schemas.books import BookBaseSchema
from domain.models import Checkout, Copy, CheckoutStatus


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
            state = CheckoutStatus.OPENED
        )


# Output Schemas
class CheckoutBaseSchema(BaseModel):

    id: int
    on_date: date
    due_date: date
    status: str
    copy_: CopyBaseSchema

class CheckoutInfoSchema(CheckoutBaseSchema):
    
    book: BookBaseSchema


