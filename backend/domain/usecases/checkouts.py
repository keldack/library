import zope.interface
import datetime

from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Checkout, Copy, Prolongation
from domain.providers import ICheckoutProvider, ICopyProvider
from domain.usecases.exceptions import KeyDoesNotExist, CopyAlreadyCheckouted

@zope.interface.implementer(IUseCase)
class CreateCheckout(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")
        self.copy_repository: ICopyProvider = self.inject(ICopyProvider, "persistence")

    def execute(self, checkout: Checkout):

        #1 check copy exist
        copy: Copy = self.copy_repository.get_copy_by_id(checkout.copy.id)
        if checkout is None:
            raise KeyDoesNotExist(f"No copy for id {checkout.copy.id}")

        #2 check copy is free (ie, is not already engaged in a checkout)
        found_checkout: Checkout = self.checkout_repository.get_checkout_by_copy_id(checkout.copy.id)
        if found_checkout:
            # We found a checkout for the copy, so thez copy is not free
            raise CopyAlreadyCheckouted(f"Copy {checkout.copy.id} already checkouted with {found_checkout.id}")


        d = datetime.date.today() 
        # Checkout starts at current day
        checkout.on_date = d
        # .. and for a full 2 weeks period
        checkout.due_date = d + datetime.timedelta(days=14)

        self.checkout_repository.create_checkout(checkout)
        return checkout


@zope.interface.implementer(IUseCase)
class ReadCheckouts(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self):
        return self.checkout_repository.get_all_checkouts()


@zope.interface.implementer(IUseCase)
class ReadCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self, checkout_id: int):
        checkout: Checkout = self.checkout_repository.get_checkout_by_id(checkout_id)
        if checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout_id}")
        return checkout


@zope.interface.implementer(IUseCase)
class ModifyCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self, checkout: Checkout):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout.id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout.id}")
        self.checkout_repository.modify_checkout(checkout)
        return checkout


@zope.interface.implementer(IUseCase)
class ProlongateCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self, prolongation: Prolongation):
        found_checkout: Checkout = self.checkout_repository.get_checkout_by_id(prolongation.checkout_id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {prolongation.checkout_id}")
        found_checkout.prolongate(prolongation.days)
        self.checkout_repository.patch_checkout(found_checkout)
        return found_checkout


@zope.interface.implementer(IUseCase)
class ReturnCheckout(UseCaseWrapper):

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self, checkout_id: int):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout_id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout_id}")

        self.checkout_repository.delete_checkout(found_checkout)
        return found_checkout


@zope.interface.implementer(IUseCase)
class DeleteCheckout(UseCaseWrapper):
    """
    Delete the checkout
    """
    
    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self, checkout: Checkout):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout.id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout.id}")
        self.checkout_repository.delete_checkout(checkout.id)
        return checkout
