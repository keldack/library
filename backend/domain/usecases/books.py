import zope.interface
from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Book
from domain.repositories import IBookRepository, IAuthorRepository
from domain.usecases.exceptions import KeyDoesNotExist


def check_authors_of_book_exist(book :Book, author_repository: IAuthorRepository):
    for author in book.authors:
        if not author_repository.get_author_by_id(author.id):
            raise KeyDoesNotExist(f"No author for id {author.id}")


@zope.interface.implementer(IUseCase)
class CreateBook(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookRepository = self.inject(IBookRepository, "persistence")
        self.author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, book: Book):

        #1 - Rules - we check authors exist
        check_authors_of_book_exist(book, self.author_repository)

        self.book_repository.create_book(book)
        return book


@zope.interface.implementer(IUseCase)
class ReadBooks(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookRepository = self.inject(IBookRepository, "persistence")

    def execute(self):
        return self.book_repository.get_all_books()


@zope.interface.implementer(IUseCase)
class ReadBook(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookRepository = self.inject(IBookRepository, "persistence")

    def execute(self, book_id: int) -> Book:
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise KeyDoesNotExist(f"No book for id {book_id}")
        return book


@zope.interface.implementer(IUseCase)
class UpdateBook(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookRepository = self.inject(IBookRepository, "persistence")

    def execute(self, book: Book):
        found_book = self.book_repository.get_book_by_id(book.id)
        if found_book is None:
            raise KeyDoesNotExist(f"No author for id {book.id}")
        self.book_repository.update_book(book)
        return book


@zope.interface.implementer(IUseCase)
class DeleteBook(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.book_repository: IBookRepository = self.inject(IBookRepository, "persistence")

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
        self.book_repository: IBookRepository = self.inject(IBookRepository, "persistence")

    def execute(self, book_id: int):
        found_book = self.book_repository.get_book_by_id(book_id)
        if found_book is None:
            raise KeyDoesNotExist(f"No book for id {book_id}")
        
        author = self.book_repository.delete_author(book_id)
        return author



