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


class IOutputSchema(zope.interface.Interface):
    """
    Interface for output schema exiting domain via output port
    """
    ...

