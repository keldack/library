import zope.interface
from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Author
from domain.repositories import IAuthorRepository
from domain.usecases.exceptions import KeyDoesNotExist


@zope.interface.implementer(IUseCase)
class CreateAuthor(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, author: Author):

        self.author_repository.create_author(author)
        return author


@zope.interface.implementer(IUseCase)
class ReadAuthors(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self):
        return self._author_repository.get_all_authors()


@zope.interface.implementer(IUseCase)
class ReadAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, author_id: int):
        author = self._author_repository.get_author_by_id(author_id)
        if author is None:
            raise KeyDoesNotExist(f"No author for id {author_id}")
        return author


@zope.interface.implementer(IUseCase)
class UpdateAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, author: Author):
        found_author = self._author_repository.get_author_by_id(author.id)
        if found_author is None:
            raise KeyDoesNotExist(f"No author for id {author.id}")
        self._author_repository.update_author(author)
        return author


@zope.interface.implementer(IUseCase)
class DeleteAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, author_id):
        found_author = self._author_repository.get_author_by_id(author_id)
        if found_author is None:
            raise KeyDoesNotExist(f"No author for id {author_id}")
        
        author = self._author_repository.delete_author(author_id)
        return author


@zope.interface.implementer(IUseCase)
class ReadBooksOfAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, author_id: int):
        found_author = self.author_repository.get_author_by_id(author_id)
        if found_author is None:
            raise KeyDoesNotExist(f"No author for id {author_id}")
        
        books = self.author_repository.get_books_of_author(found_author)
        return books