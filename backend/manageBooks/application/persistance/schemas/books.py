from typing import Sequence, Optional
from pydantic import BaseModel
import zope.interface

from domain.ports import IInputSchema


@zope.interface.implementer(IInputSchema)
class BookInputSchema(BaseModel):
    """
    Schema used for creation and update of a book from application
    """
    isbn : Optional[str]
    title: str
    authors: Sequence[int]