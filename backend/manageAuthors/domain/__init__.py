from typing import Any
import zope.interface


class IInputSchema(zope.interface.Interface):
    """
    Interface for input schema entering domain via input port
    """

    def to_domain(self) -> Any:
        """
        Create domain entity from the schema
        """
        ...


class IUseCase(zope.interface.Interface):
    """
    Use case interface
    """
    
    def execute(self, schema: IInputSchema):
        """
        execute the use case using the input schema
        """
        ...


