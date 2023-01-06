from pydantic import BaseModel
from typing import Optional
import zope.interface

from application.schemas import IInputSchema
from domain.models import Author

@zope.interface.implementer(IInputSchema)
class AuthorSchema(BaseModel):

    id: int | None = None
    name: str | None = None

    def to_domain(self) -> Author:
        return Author(id = self.id, name = self.name)
