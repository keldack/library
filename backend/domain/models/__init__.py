from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, KW_ONLY, field
from typing import Set, Optional, Sequence
import datetime

@dataclass
class Author:

    _: KW_ONLY
    id: int = None
    name: Optional[str] = field(default_factory=str)
    books: Optional[Sequence[Book]] = field(default_factory=list)

    def to_schema(self):
        return self.__dict__.copy()

@dataclass
class Book:

    _: KW_ONLY
    id: int = None
    isbn: Optional[str] = field(default_factory=str)
    title: Optional[str] = field(default_factory=str)
    authors: Optional[Set[Author]] = field(default_factory=list)

    def to_schema(self):
        return self.__dict__.copy()


@dataclass
class Copy:

    _: KW_ONLY
    id: int = None
    book: Optional[Book] = None
    place: Optional[str] = field(default_factory=str)

    def to_schema(self):
        return self.__dict__.copy()


class CheckoutStatus(str, Enum):
    OPENED = "Opened"
    CLOSED = "Closed"

@dataclass
class Checkout:

    _: KW_ONLY
    id: int = None
    copy: Copy
    on_date: datetime.date = field(default=datetime.date.today())
    borrower: str
    state: CheckoutStatus


    def to_schema(self):
        return self.__dict__.copy()