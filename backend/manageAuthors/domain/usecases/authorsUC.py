import zope.interface
from domain import IUseCase
from domain.usecases import UseCaseWrapper
from application.persistance.schemas.authors import AuthorSchema
from domain.models import Author
from domain.ports import IAuthorProvider
from domain.usecases.exceptions import KeyDoesNotExist


@zope.interface.implementer(IUseCase)
class CreateAuthor(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self, schema: AuthorSchema):

        author: Author = schema.to_domain()
        self.author_repository.create_author(author)

        return author


@zope.interface.implementer(IUseCase)
class ReadAuthors(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self):
        return self._author_repository.get_all_authors()


@zope.interface.implementer(IUseCase)
class ReadAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self, author_id: int):
        author = self._author_repository.get_author_by_id(author_id)
        if author is None:
            raise KeyDoesNotExist(f"No author for id {author_id}")
        return author

@zope.interface.implementer(IUseCase)
class UpdateAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self, author_id: int, schema: AuthorSchema):
        the_author = self._author_repository.get_author_by_id(author_id)
        if the_author is None:
            raise KeyDoesNotExist(f"No author for id {author_id}")
        author: Author = schema.to_domain()
        author.id = author_id
        self._author_repository.update_author(author)
        return author


@zope.interface.implementer(IUseCase)
class DeleteAuthor(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self._author_repository: IAuthorProvider = self.inject(IAuthorProvider, "persistence")

    def execute(self, author_id):

        author = self._author_repository.delete_author(author_id)
        return author


