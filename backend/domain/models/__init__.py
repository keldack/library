from __future__ import annotations

from dataclasses import dataclass, KW_ONLY, field
from typing import Set, Optional, Sequence
import datetime

@dataclass
class Author:

    _: KW_ONLY
    id: int = None
    name: str
    books: Optional[Sequence[Book]] = field(default_factory=list)

    def to_schema(self):
        return self.__dict__.copy()

@dataclass
class Book:

    _: KW_ONLY
    id: int = None
    isbn: str
    title: str
    authors: Set[Author]


@dataclass
class Copy:

    _: KW_ONLY
    id: int = None
    book: Book
    place: str


@dataclass
class Checkout:

    _: KW_ONLY
    id: int = None
    copy: Copy
    on_date: datetime.date = datetime.date.today()
