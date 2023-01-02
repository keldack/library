from core.singleton import Singleton
from typing import Type, Any, Dict

class MemoryDatabase(Singleton):
    """
    Memory Repository is just a domain entity object storage like a DB memory. It is instantiated as singleton
    """

    def __init__(self):
        
        if not self.initDone():
            Singleton.__init__(self)
            self._repo: Dict = {}
            self._id: int = 0

    def __get_new_id(self):
        self._id += 1
        return self._id


    def add_entity(self, entity: object):
        """
        Add an object with an id
        """
        entity.id = self.__get_new_id()
        self._repo.setdefault(entity.__class__.__name__, {})[entity.id] = entity
        return entity

    
    def replace_entity(self, entity: object):
        """
        Add an object with an id
        """
        self._repo.setdefault(entity.__class__.__name__, {})[entity.id] = entity
        return entity


    def get_entity(self, cls: Type[Any], object_id: int):
        """
        Get object for class cls with specific id object_id
        """
        return self._repo.get(cls.__name__, {}).get(id, None)


    def get_entities_type(self, cls: Type[Any]):
        """
        Get all entities for a specific class
        """
        return self._repo.get(cls.__name__, {}).values()


    def delete_entity(self, cls: Type[Any], object_id: int):
        """
        Delete object for class cls with specific id object_id
        """
        return self._repo.get(cls.__name__, {}).pop(object_id, None)
        
