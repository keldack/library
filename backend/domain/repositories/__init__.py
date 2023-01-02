import zope.interface
from typing import Sequence

from domain.models import Author

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