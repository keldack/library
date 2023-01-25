import zope.interface
import datetime
from typing import Sequence
from wired import service_factory

from domain.providers import IAuthorProvider, IBookProvider, ICopyProvider, ICheckoutProvider
from domain.models import Author, Book, Copy, Checkout

from .library.models import Author as DB_Author, Book as DB_Book, Copy as DB_Copy, Checkout as DB_Checkout

def book_to_entity(book: DB_Book, relation_level:int = 0) -> Book:
    if book:
        book = Book(
            id = book.pk,
            isbn = book.isbn,
            title = book.title,
            authors = [author_to_entity(author, relation_level-1) for author in book.authors] if relation_level else [],
        )
    return book

def author_to_entity(author: DB_Author, relation_level:int = 0) -> Author:
    if author:
        author = Author(
            id = author.pk, 
            name=author.name,
            books=[book_to_entity(book, relation_level-1) for book in author.books]  if relation_level else [],
        )
    return author

def copy_to_entity(copy: DB_Copy, relation_level:int = 0):
    if copy:
        copy = Copy(
            id = copy.pk,
            place = copy.place,
            book = book_to_entity(copy.book, relation_level-1) if relation_level else None
        )
    return copy

def checkout_to_entity(checkout: DB_Checkout, relation_level:int = 0):
    if checkout:
        checkout = Checkout(
            id = checkout.pk,
            borrower = checkout.borrower, 
            on_date=checkout.on_date,
            return_date=checkout.return_date,
            copy = copy_to_entity(checkout.copy, relation_level-1) if relation_level else None
        )
    return checkout


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

@service_factory(for_=IAuthorProvider, name="django")
@zope.interface.implementer(IAuthorProvider)
class AuthorDjangoRepository:

    @classmethod
    def __wired_factory__(cls, container):
        return cls()


    def get_all_authors(self) -> Sequence[Author]:
        """
            Returns all authors
        """
        authors = DB_Author.objects.all()
        return [author_to_entity(author) for author in authors]

    def get_author_by_id(self, author_id: int) -> Author:
        """
        Returns specific author for id and boosk written by the author
        """
        author = get_or_none(DB_Author, pk=author_id)
        return author_to_entity(author, relation_level=1)

    def create_author(self, author: Author) -> Author:
        """
        Create an author from the Author entity
        """
        author_db: DB_Author()
        author_db.name = author.name
        author_db.save()
        return author_to_entity(author_db)


    def update_author(self, author: Author) -> Author:
        """
        Update author from the Author entity
        """
        author_db = DB_Author.objects.get(pk = author.id)
        author_db.name = author.name
        author_db.save()
        return author_to_entity(author_db)


    def delete_author(self, author_id: int):
        """
        Delete the author of id
        """
        author_db = DB_Author.objects.get(pk = author_id)
        author_db.delete()


    def get_books_of_author(self, author: Author) -> Sequence[Book]:
        """
        Get all books of an author
        """
        author_db = DB_Author.objects.get(pk = author.id)
        return [book_to_entity(book) for book in author_db.books]


@service_factory(for_=IBookProvider, name="django")
@zope.interface.implementer(IBookProvider)
class BookDjangoRepository():
    """
    Interface for book repository actions
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()


    def get_all_books(self) -> Sequence[Book]:
        """
            Returns all books
        """
        return [book_to_entity(book) for book in DB_Book.objects.all()]


    def get_book_by_id(self, book_id: int) -> Book:
        """
        Returns specific book for id
        """
        book = get_or_none(DB_Book, pk=book_id)
        return book_to_entity(book, relation_level=1)

        
    def get_book_by_isbn(self, book_isbn: str) -> Book:
        """
        Returns specific book for id
        """
        book = get_or_none(Book, isbn=book_isbn)
        return book_to_entity(book, relation_level=1)
                

    def create_book(self, book: Book) -> Book:
        """
        Create a book from the entity Book
        """
        book_db: DB_Book = DB_Book()
        book_db.isbn = book.isbn
        for author in book.authors:
            author_db = Author.objects.get(pk = author.id)    
            book_db.authors.add(author_db)
        book_db.save()
        return book_to_entity(book_db, relation_level=1)


    def update_book(self, book: Book) -> Book:
        """
        Update author from the Author entity
        """
        book_db = DB_Book.objects.get(pk = book.id)
        book_db.isbn = book.isbn
        book_db.title = book.title
        book_db.authors.clear()
        for author in book.authors:
            author_db = Author.objects.get(pk = author.id)    
            book_db.authors.add(author_db)
        book_db.save()
        return book_to_entity(book_db, relation_level=1)


    def delete_book(self, book_id: int):
        """
        Delete the book of id
        """
        book_db = DB_Book.objects.get(pk = book_id)
        book_db.delete()


    def get_copies(self, book: Book) -> Sequence[Copy]:
        """
        Get all copies of a book
        """
        book_db = DB_Book.objects.get(pk = book.id)
        return [copy_to_entity(copy) for copy in book_db.copies]



@service_factory(for_=ICopyProvider, name="django")
@zope.interface.implementer(ICopyProvider)
class CopyDjangoRepository():
    """
    Interface for copy repository actions
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()

    
    def get_copy_by_id(self, copy_id: int) -> Copy:
        """
        Get the copy by its id
        """
        copy = get_or_none(Copy, pk = copy_id)
        return copy_to_entity(copy, relation_level=1)


    def create_copy(self, copy: Copy) -> Copy:
        """
        Create a new copy of a book in the library
        """
        copy_db = DB_Copy()
        copy_db.place = copy.place
        copy_db.book = DB_Book.objects.get(copy.book.id)
        copy_db.save()
        return copy_to_entity(copy_db, relation_level=1)

    def patch_copy(self, copy: Copy) -> Copy:
        """
        Update partial information of a copy
        """
        copy_db = DB_Copy.objects.get(pk=copy.id)
        copy_db.place = copy.place
        copy_db.save()
        return copy_to_entity(copy_db, relation_level=1)


    def delete_copy(self, copy_id:int):
        """
        Delete the copy from the library
        """
        DB_Copy.objects.get(pk=copy_id).delete()     
        

@service_factory(for_=ICheckoutProvider, name="django")
@zope.interface.implementer(ICheckoutProvider)
class CheckoutDjangoRepository():
    """
    Interface for checkout repository actions
    """

    @classmethod
    def __wired_factory__(cls, container):
        return cls()        

    
    def get_all_checkouts(self) -> Sequence[Checkout]:
        """
        Get all the checkouts
        """
        checkouts = DB_Checkout.objects.all()
        return [checkout_to_entity(checkout) for checkout in checkouts]


    def get_checkout_by_id(self, checkout_id: int) -> Checkout:
        """
        Get the checkout by its id
        """
        checkout = get_or_none(Checkout, checkout_id)
        return checkout_to_entity(checkout, relation_level=2)
        

    def get_checkout_by_copy_id(self, copy_id: int) -> Checkout:
        """
        Get the checkout by the id of the copy
        """
        copy = get_or_none(Copy, copy_id)
        return checkout_to_entity(copy.checkout, relation_level=2)


    def create_checkout(self, checkout: Checkout) -> Checkout:
        """
        Create the checkout of a copy of a book
        """
        checkout_db = DB_Checkout()
        checkout_db.borrower = checkout.borrower
        checkout_db.on_date = checkout.on_date
        checkout_db.return_date = checkout.return_date
        checkout_db.copy = DB_Copy.objects.get(checkout.copy.id)
        checkout_db.save()
        return checkout_to_entity(checkout_db, relation_level=2)


    def modify_checkout(self, checkout: Checkout) -> Checkout:
        """
        Modify the checkout 
        """
        checkout_db = DB_Checkout.objects.get(checkout.id)
        checkout_db.borrower = checkout.borrower
        checkout_db.on_date = checkout.on_date
        checkout_db.return_date = checkout.return_date
        checkout_db.copy = DB_Copy.objects.get(checkout.copy.id)
        checkout_db.save()
        return checkout_to_entity(checkout_db, relation_level=2)

        

    def patch_checkout(self, checkout: Checkout) -> Checkout:
        """
        Prolongates a checkout of 'duration' days
        """
        checkout_db = DB_Checkout.objects.get(checkout.id)
        checkout_db.return_date = checkout.return_date
        checkout_db.save()
        return checkout_to_entity(checkout_db, relation_level=2)


    def delete_checkout(self, checkout_id: int) -> Checkout:
        """
        Close the checkout as copy returns to library
        """
        DB_Checkout.objects.get(checkout_id).delete()
    