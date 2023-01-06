import zope.interface
from typing import Sequence

from domain.models import Author, Book, Copy, Checkout


class IAuthorRepository(zope.interface.Interface):
    """
    Interface for author repository actions
    """

    def get_all_authors(self) -> Sequence[Author]:
        """
            Returns all authors
        """
        ...

    def get_author_by_id(self, author_id: int) -> Author:
        """
            Returns specific author for id
        """
        ...

    def create_author(self, author: Author) -> Author:
        """
        Create an author from the Author entity
        """
        ...

    def update_author(self, author: Author) -> Author:
        """
        Updtae author from the Author entity
        """
        ...

    def delete_author(self, author_id: int):
        """
        Delete the author of id
        """
        ...


class IBookRepository(zope.interface.Interface):
    """
    Interface for book repository actions
    """

    def get_all_books(self) -> Sequence[Book]:
        """
            Returns all books
        """
        ...

    def get_all_books_for_author(self, author: Author) -> Sequence[Book]:
        """
            Returns all books of an author
        """
        ...

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Returns specific book for id
        """
        ...

    def get_book_by_isbn(self, book_isbn: str) -> Book:
        """
        Returns specific book for id
        """
        ...

    def create_book(self, book: Book) -> Book:
        """
        Create a book from the entity Book
        """
        ...

    def update_book(self, book: Book) -> Book:
        """
        Update author from the Author entity
        """
        ...

    def delete_book(self, book_id: int):
        """
        Delete the book of id
        """
        ...


class ICopyRepository(zope.interface.Interface):
    """
    Interface for copies repository actions
    """

    def get_copy_by_id(self, copy_id: int) -> Copy:
        """
        Create a new copy of a book in the library
        """
        ...

    def create_copy(self, copy: Copy) -> Copy:
        """
        Create a new copy of a book in the library
        """
        ...

    def patch_copy(self, copy: Copy) -> Copy:
        """
        Update partial information of a copy
        """
        ...

    def delete_copy(self, copy_id:int):
        """
        Delete the copy from the library
        """

    def return_copy(self, copy_id: int):
        """
        Make the return to the library of checkout copy
        """

    
class ICheckoutRepository(zope.interface.Interface):
    """
    Interface for checkouts repository actions
    """

    def create_checkout(self, checkout: Checkout) -> Checkout:
        """
        Create the checkout of a copy of a book
        """
        ...


    def prolongate_checkout(self, checkout: Checkout, days_duration: int) -> Checkout:
        """
        Prolongates a checkout of 'duration' days
        """
        ...

    def close_checkout(self, checkout: Checkout) -> Checkout:
        """
        Close the checkout as copy returns to library
        """
        ...