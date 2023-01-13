import zope.interface
import datetime

from domain.interfaces import IUseCase
from domain.usecases import UseCaseWrapper
from domain.models import Checkout, CheckoutStatus
from domain.providers import ICheckoutProvider
from domain.usecases.exceptions import KeyDoesNotExist

@zope.interface.implementer(IUseCase)
class CreateCheckout(UseCaseWrapper):
    """Use case for author creation"""

    def __init__(self):
        UseCaseWrapper.__init__(self)
        self.checkout_repository: ICheckoutProvider = self.inject(ICheckoutProvider, "persistence")

    def execute(self, checkout: Checkout):
        d = datetime.date.today()
        
        #1 Checkout starts at current day
        checkout.on_date = d
        # .. and for a full 2 weeks period
        checkout.due_date = d + datetime.timedelta(days=14)
        checkout.state = CheckoutStatus.OPENED

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

    def execute(self, checkout_id: Checkout, prolongation_days: int):
        found_checkout = self.checkout_repository.get_checkout_by_id(checkout_id)
        if found_checkout is None:
            raise KeyDoesNotExist(f"No checkout for id {checkout_id}")
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
        found_checkout.state = CheckoutStatus.CLOSED

        self.checkout_repository.return_checkout(found_checkout)
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
        self.checkout_repository.delete_checkout(checkout)
        return checkout
