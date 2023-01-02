import zope.interface
from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.schemas.authors import AuthorSchema
from domain.models import Author
from domain.repositories import IAuthorRepository


@zope.interface.implementer(IUseCase)
class CreateAuthor(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.author_repository: IAuthorRepository = self.inject(IAuthorRepository, "persistence")

    def execute(self, schema: AuthorSchema):

        author: Author = schema.to_domain()
        self.author_repository.create_author(author)

        return author



