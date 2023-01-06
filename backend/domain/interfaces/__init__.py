from typing import Any
import zope.interface

class IUseCase(zope.interface.Interface):
    """
    Use case interface
    """
    
    def execute(self, *args):
        """
        execute the use case using the input schema
        """
        ...


