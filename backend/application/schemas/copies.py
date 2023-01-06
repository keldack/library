from typing import Optional
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from domain.models import Copy, Book


@zope.interface.implementer(IInputSchema)
class CopyInputSchema(BaseModel):
    """
    Schema used for creation and update of a book from application
    """
    id: int | None = None
    place : Optional[str]
    book: int

    def to_domain(self) -> Copy:
        
        return Copy(
            id = self.id, 
            place = self.place,
            book = Book(id=self.book)
        )
