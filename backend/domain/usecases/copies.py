import zope.interface
from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Copy
from domain.providers import ICopyProvider, IBookProvider
from domain.usecases.exceptions import KeyDoesNotExist

@zope.interface.implementer(IUseCase)
class CreateCopy(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.copy_repository: ICopyProvider = self.inject(ICopyProvider, "persistence")
        self.book_repository: IBookProvider = self.inject(IBookProvider, "persistence")

    def execute(self, copy: Copy):

        #1 - Check book exists to create a copy of it
        found_book = self.book_repository.get_book_by_id(copy.book.id)
        if found_book is None:
            raise KeyDoesNotExist(f"Copy creation - No book for id {copy.book.id}")

        copy = self.copy_repository.create_copy(copy)
        return copy


@zope.interface.implementer(IUseCase)
class ReadCopies(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.copy_repository: ICopyProvider = self.inject(ICopyProvider, "persistence")

    def execute(self):
        return self.copy_repository.get_all_copies()


@zope.interface.implementer(IUseCase)
class ReadCopy(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.copy_repository: ICopyProvider = self.inject(ICopyProvider, "persistence")

    def execute(self, copy_id: int):
        copy: Copy = self.copy_repository.get_copy_by_id(copy_id)
        if copy is None:
            raise KeyDoesNotExist(f"No copy for id {copy_id}")
        return copy


@zope.interface.implementer(IUseCase)
class PatchCopy(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.copy_repository: ICopyProvider = self.inject(ICopyProvider, "persistence")

    def execute(self, copy: Copy):
        found_copy = self.copy_repository.get_copy_by_id(copy.id)
        if found_copy is None:
            raise KeyDoesNotExist(f"No author for id {copy.id}")
        found_copy.place = copy.place
        self.copy_repository.patch_copy(found_copy)
        return found_copy


@zope.interface.implementer(IUseCase)
class DeleteCopy(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.copy_repository: ICopyProvider = self.inject(ICopyProvider, "persistence")

    def execute(self, copy_id: int):
        found_copy = self.copy_repository.get_copy_by_id(copy_id)
        if found_copy is None:
            raise KeyDoesNotExist(f"No copy for id {copy_id}")
        
        copy = self.copy_repository.delete_copy(copy_id)
        return copy
