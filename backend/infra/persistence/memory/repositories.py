import zope.interface
from typing import Sequence
from wired import service_factory

from infra.persistence.memory import MemoryDatabase

from domain.repositories import IAuthorRepository
from domain.models import Author

@service_factory(for_=IAuthorRepository, name="memory")
@zope.interface.implementer(IAuthorRepository)
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
        Returns specific author for id
        """
        return self.memory_db.get_entity(Author, author_id)

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