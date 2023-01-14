from __future__ import annotations
from typing import Optional, Sequence
from enum import Enum
from dataclasses import dataclass, KW_ONLY, field
import datetime


class Entity:
   
    def to_schema(self):        
        return self.__dict__.copy()


@dataclass
class Author(Entity):

    _: KW_ONLY
    id: int = None
    name: Optional[str] = field(default_factory=str)
    books: Optional[Sequence[Book]] = field(default_factory=list)
    
    def to_schema(self):
        schema = Entity.to_schema(self) 
        schema["books"] = [book.to_schema() for book in self.books]
        return schema

@dataclass
class Book(Entity):

    _: KW_ONLY
    id: int = None
    isbn: Optional[str] = field(default_factory=str)
    title: Optional[str] = field(default_factory=str)
    authors: Optional[Sequence[Author]] = field(default_factory=list)

    def to_schema(self):
        schema = Entity.to_schema(self) 
        schema["authors"] = [author.to_schema() for author in self.authors]
        return schema

    
@dataclass
class Copy(Entity):

    _: KW_ONLY
    id: int = None
    book: Book = None
    place: Optional[str] = field(default_factory=str)

    def to_schema(self):
        schema = Entity.to_schema(self) 
        if self.book:
            schema["book"] = self.book.to_schema()
        return schema
    

@dataclass
class Checkout(Entity):

    _: KW_ONLY
    id: int = None
    copy: Copy
    on_date: datetime.date = field(default=datetime.date.today())
    return_date: datetime.date = field(default=datetime.date.today() + datetime.timedelta(days=15))
    borrower: str

    def to_schema(self):
        schema = Entity.to_schema(self) 
        schema["copy"] = self.copy.to_schema()
        return schema

    def prolongate(self, days:int):
        self.return_date += datetime.timedelta(days=days)

@dataclass
class Prolongation(Entity):

    _: KW_ONLY
    checkout_id: int
    days: int