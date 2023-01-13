from __future__ import annotations
from typing import List, Optional

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


class LocalBookBaseSchema(BaseModel):

    id: int
    title: str


class AuthorInfoSchema(AuthorBaseSchema):

    books: Optional[List[LocalBookBaseSchema]]



