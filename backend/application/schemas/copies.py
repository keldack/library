from typing import Optional
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from application.schemas.books import BookBaseSchema
from domain.models import Copy, Book


@zope.interface.implementer(IInputSchema)
class CopyInputSchema(BaseModel):
    """
    Schema used for creation and update of a copy from application
    """
    id: int | None = None
    place : Optional[str]
    book_id: int

    def to_domain(self) -> Copy:
        
        return Copy(
            id = self.id, 
            place = self.place,
            book = Book(id=self.book_id)
        )


@zope.interface.implementer(IInputSchema)
class PatchCopyInputSchema(BaseModel):
    """
    Schema used for creation and update of a copy 
    """
    
    place : str

    def to_domain(self) -> Copy:
        
        return Copy(
            id = self.id, 
            place = self.place,
        )


# Output schemas
class CopyBaseSchema(BaseModel):
    """
    Schema used to get copy base schema
    """
    id: int | None = None
    place : Optional[str]


class CopyInfoSchema(CopyBaseSchema):
    """
    Schema used to get copy information with book
    """
    book: BookBaseSchema

