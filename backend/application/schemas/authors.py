from __future__ import annotations
from typing import List

from pydantic import BaseModel
import zope.interface

from application.schemas import IInputSchema
from domain.models import Author


@zope.interface.implementer(IInputSchema)
class AuthorInputSchema(BaseModel):

    id: int | None = None
    name: str | None = None

    def to_domain(self) -> Author:
        return Author(id = self.id, name = self.name)


# Outputs schemas
class AuthorBaseSchema(BaseModel):

    id: int
    name: str


from application.schemas.books import BookBaseSchema

class AuthorInfoSchema(AuthorBaseSchema):

    books: "List[BookBaseSchema]"

AuthorInfoSchema.update_forward_refs()

