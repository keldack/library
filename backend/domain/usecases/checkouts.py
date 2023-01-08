import zope.interface


from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Checkout
from domain.repositories import ICheckoutRepository
from domain.usecases.exceptions import KeyDoesNotExist

@zope.interface.implementer(IUseCase)
class CreateCheckout(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutRepository = self.inject(ICheckoutRepository, "persistence")

    def execute(self, checkout: Checkout):

        self.checkout_repository.create_checkout(checkout)
        return checkout


@zope.interface.implementer(IUseCase)
class ReadCheckouts(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutRepository = self.inject(ICheckoutRepository, "persistence")

    def execute(self):
        return self.checkout_repository.get_all_checkouts()


@zope.interface.implementer(IUseCase)
class ReadCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutRepository = self.inject(ICheckoutRepository, "persistence")

    def execute(self, checkout_id: int):
        checkout: Checkout = self.checkout_repository.get_checkout_by_id(checkout_id)
        if checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout_id}")
        return checkout


@zope.interface.implementer(IUseCase)
class PatchCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutRepository = self.inject(ICheckoutRepository, "persistence")

    def execute(self, checkout: Checkout):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout.id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout.id}")
        self.checkout_repository.patch_checkout(checkout)
        return checkout


@zope.interface.implementer(IUseCase)
class ProlongateCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutRepository = self.inject(ICheckoutRepository, "persistence")

    def execute(self, checkout: Checkout):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout.id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout.id}")
        self.checkout_repository.patch_checkout(checkout)
        return checkout


@zope.interface.implementer(IUseCase)
class DeleteCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutRepository = self.inject(ICheckoutRepository, "persistence")

    def execute(self, checkout: Checkout):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout.id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout.id}")
        self.checkout_repository.patch_checkout(checkout)
        return checkout
