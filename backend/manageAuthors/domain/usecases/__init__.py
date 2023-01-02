from typing import Any
from config.config import settings
from config.registry import LibraryRegistry as Registry

class UseCaseWrapper:
    """
    Wrapper class whose every use case must inherit. Contains inject method to access dependencies in IOC manner
    """

    def __init__(self):
        self.container = None


    def inject(self, interface_, keyword_) -> Any:
        """
        Returns the object from the registry considering class and the keyword
        """
        if not self.container:
            self.container = Registry.get_registry().create_container()

        try:
            result = self.container.get(interface_, name=settings.MODE[keyword_])
        except Exception as e:
            print(e)
            # msg = f"Looking for class '{interface_}' with '{keyword_}' value as '{settings.MODE[keyword_]}' in service factory"
            # raise Exception(msg)
            raise e

        return result
