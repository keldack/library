from datetime import date
from typing import Optional
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from domain.models import Checkout, Copy


@zope.interface.implementer(IInputSchema)
class CheckoutInputSchema(BaseModel):
    """
    Schema used for creation and update of a book from application
    """
    id: int | None = None
    copy_id: int
    on_date: date
    borrower: str

    def to_domain(self) -> Checkout:
        
        return Checkout(
            id = self.id, 
            borrower = self.borrower,
            on_date = self.on_date,
            copy = Copy(id=self.copy)
        )

