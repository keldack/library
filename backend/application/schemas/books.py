from __future__ import annotations
from typing import Sequence, Optional, List
from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from application.schemas.authors import AuthorBaseSchema
from domain.models import Author, Book


@zope.interface.implementer(IInputSchema)
class BookInputSchema(BaseModel):
    """
    Schema used for creation and update of a book from application
    """
    id: int | None = None
    isbn : Optional[str]
    title: Optional[str]
    authors: Sequence[int]

    def to_domain(self) -> Book:
        
        return Book(
            id = self.id, 
            isbn = self.isbn,
            title = self.title,
            authors = [Author(id=author_id) for author_id in self.authors]
        )


# Output schemas
class BookBaseSchema(BaseModel):
    """
    Schema used to get books information
    """
    id: int
    isbn: str
    title: str
    


class BookInfoSchema(BookBaseSchema):
    
    authors: List[AuthorBaseSchema]



