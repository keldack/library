import zope.interface
from typing import Sequence
from wired import service_factory

from commons.application.memorydb import MemoryDatabase

from domain.providers import IAuthorProvider, IBookProvider, ICopyProvider, ICheckoutProvider
from domain.models import Author, Book, Copy, Checkout, CheckoutStatus

@service_factory(for_=IAuthorProvider, name="memory")
@zope.interface.implementer(IAuthorProvider)
class AuthorRepository:

    @classmethod
    def __wired_factory__(cls, container):
        return cls()

    def __init__(self):
        self.memory_db = MemoryDatabase()

    def get_all_authors(self) -> Sequence[Author]:
        """
            Returns all authors
        """
        return self.memory_db.get_entities_type(Author)

    def get_author_by_id(self, author_id: int) -> Author:
        """
        Returns specific author for id and boosk written by the author
        """
        author: Author = self.memory_db.get_entity(Author, author_id)
        if author:
            author.books = self.memory_db.get_relations(author, Book, "author")
        return author

    def create_author(self, author: Author) -> Author:
        """
        Create an author from the Author entity
        """
        self.memory_db.add_entity(author)
        return author


    def update_author(self, author: Author) -> Author:
        """
        Update author from the Author entity
        """
        self.memory_db.replace_entity(author)
        return author


    def delete_author(self, author_id: int):
        """
        Delete the author of id
        """
        return self.memory_db.delete_entity(Author, author_id)


    def get_books_of_author(self, author: Author) -> Sequence[Book]:
        """
        Get all books of an author
        """
        return self.memory_db.get_relations(author, Book, "author")


@service_factory(for_=IBookProvider, name="memory")
@zope.interface.implementer(IBookProvider)
class BookRepository():
    """
    Interface for book repository actions
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()

    def __init__(self):
        self.memory_db = MemoryDatabase()


    def get_all_books(self) -> Sequence[Book]:
        """
            Returns all books
        """
        books = self.memory_db.get_entities_type(Book)
        return books


    def get_book_by_id(self, book_id: int) -> Book:
        """
        Returns specific book for id
        """
        book = self.memory_db.get_entity(Book, book_id)
        if book:
            book.authors = self.memory_db.get_relations(book, Author, "author")
        return book


    def get_book_by_isbn(self, book_isbn: str) -> Book:
        """
        Returns specific book for id
        """
        return self.memory_db.get_entity_by_value(Book, "isbn", book_isbn)


    def create_book(self, book: Book) -> Book:
        """
        Create a book from the entity Book
        """
        self.memory_db.add_entity(book)
        for author in book.authors:
            self.memory_db.add_relation(book, author, "author")
        return book


    def update_book(self, book: Book) -> Book:
        """
        Update author from the Author entity
        """
        self.memory_db.replace_entity(book)
        self.memory_db.remove_all_relations(book, "author")
        for author in book.authors:
            self.memory_db.add_relation(book, author, "author")
        
        return book


    def delete_book(self, book_id: int):
        """
        Delete the book of id
        """
        return self.memory_db.delete_entity(Book, book_id)


    def get_copies(self, book: Book) -> Sequence[Copy]:
        """
        Get all copies of a book
        """
        copies = self.memory_db.get_relations(book, Copy, "copies")
        return copies


@service_factory(for_=ICopyProvider, name="memory")
@zope.interface.implementer(ICopyProvider)
class CopyRepository():
    """
    Interface for copy repository actions
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()

    def __init__(self):
        self.memory_db = MemoryDatabase()

    
    def get_copy_by_id(self, copy_id: int) -> Copy:
        """
        Create a new copy of a book in the library
        """
        copy = self.memory_db.get_entity(Copy, copy_id)
        if copy:
            copy.book = self.memory_db.get_the_relation(copy, Book, "copy")

        return copy


    def create_copy(self, copy: Copy) -> Copy:
        """
        Create a new copy of a book in the library
        """
        self.memory_db.add_entity(copy)
        self.memory_db.add_relation(copy, copy.book, "copy")
        # return copy
        return self.get_copy_by_id(copy.id)  # As we want full schema for output with book relation

    def patch_copy(self, copy: Copy) -> Copy:
        """
        Update partial information of a copy
        """
        self.memory_db.replace_entity(copy)
        return copy


    def delete_copy(self, copy_id:int):
        """
        Delete the copy from the library
        """
        return self.memory_db.delete_entity(Copy, copy_id)


    def return_checkouted_copy(self, copy_id: int):
        """
        Make the return to the library of checkout copy
        """
        return self.memory_db.get_entity(Copy, copy_id)
        

@service_factory(for_=ICheckoutProvider, name="memory")
@zope.interface.implementer(ICheckoutProvider)
class CheckoutRepository():
    """
    Interface for checkout repository actions
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()        

    def __init__(self):
        self.memory_db = MemoryDatabase()


    def create_checkout(self, checkout: Checkout) -> Checkout:
        """
        Create the checkout of a copy of a book
        """
        self.memory_db.add_entity(checkout)
        self.memory_db.add_relation(checkout.copy, checkout, "checkout")
        return checkout

    def modify_checkout(self, checkout: Checkout) -> Checkout:
        """
        Modify the checkout 
        """
        found_checkout: Checkout = self.memory_db.get_entity(checkout.id)


    def prolongate_checkout(self, checkout: Checkout, days_duration: int) -> Checkout:
        """
        Prolongates a checkout of 'duration' days
        """
        checkout: Checkout = self.memory_db.get

    def close_checkout(self, checkout: Checkout) -> Checkout:
        """
        Close the checkout as copy returns to library
        """
        found_checkout: Checkout = self.memory_db.get_entity(checkout.id)
        found_checkout.state = CheckoutStatus.CLOSED
    