import zope.interface

from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Book
from domain.providers import IBookProvider, IAuthorProvider
from domain.usecases.exceptions import KeyDoesNotExist, ISBNAlreadyUsed


def check_authors_of_book_exist(book :Book, author_repository: IAuthorProvider):
    for author in book.authors:
        if not author_repository.get_author_by_id(author.id):
            raise KeyDoesNotExist(f"No author for id {author.id}")
            

def check_isbn_not_already_used(book: Book, book_repository: IBookProvider):
    books_with_isbn = book_repository.get_book_by_isbn(book.isbn)
    error = False
    if books_with_isbn:
        if book.id:
            # book is already created, we just check the found book for isbn is the same id, 
            # since we are in modification case, else we raise exception
            if book.id != books_with_isbn.id:
                error = True
        else:        
            error = True
    if error:
        raise ISBNAlreadyUsed(f"ISBN {book.isbn} already used for '{books_with_isbn.title}'")


@zope.interface.implementer(IUseCase)
class CreateBook(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")
        self.author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self, book: Book):

        #1 - Rules - we check authors exist
        check_authors_of_book_exist(book, self.author_repository)

        #2 - Rules - we check ISBN not already  used
        check_isbn_not_already_used(book, self.book_repository)

        self.book_repository.create_book(book)
        return book


@zope.interface.implementer(IUseCase)
class UpdateBook(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")
        self.author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self, book: Book):
        #1 - Check book already exists
        found_book = self.book_repository.get_book_by_id(book.id)
        if found_book is None:
            raise KeyDoesNotExist(f"No book for id {book.id}")

        #2 - Rules - we check authors exist
        check_authors_of_book_exist(book, self.author_repository)

        #3 - Rules - we check ISBN not already  used
        check_isbn_not_already_used(book, self.book_repository)

        self.book_repository.update_book(book)
        return book


@zope.interface.implementer(IUseCase)
class ReadBooks(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")

    def execute(self):
        return self.book_repository.get_all_books()


@zope.interface.implementer(IUseCase)
class ReadBook(UseCaseWrapper):


    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")

    def execute(self, book_id: int) -> Book:
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise KeyDoesNotExist(f"No book for id {book_id}")

        return book


@zope.interface.implementer(IUseCase)
class DeleteBook(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")

    def execute(self, book_id: int):
        found_book = self.book_repository.get_book_by_id(book_id)
        if found_book is None:
            raise KeyDoesNotExist(f"No book for id {book_id}")
        
        author = self.book_repository.delete_book(book_id)
        return author


@zope.interface.implementer(IUseCase)
class GetCopiesOfBook(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")

    def execute(self, book_id: int):
        found_book = self.book_repository.get_book_by_id(book_id)
        if found_book is None:
            raise KeyDoesNotExist(f"No book for id {book_id}")
        
        copies = self.book_repository.get_copies(found_book)
        return copies



