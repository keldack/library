from config.singleton import Singleton
from typing import Type, Any, Dict


class _Node:

    def __init__(self, entity: Any):
        self.entity = entity

    def set_entity(self, entity: Any):
        self.entity = entity

class _Link:

    def __init__(self, source: _Node, target: _Node):
        self.source = source
        self.target = target

        
class MemoryDatabase(Singleton):
    """
    Memory Repository is just a domain entity object storage like a DB memory. It is instantiated as singleton
    """

    def __init__(self):
        
        if not self.initDone():
            Singleton.__init__(self)
            self._repo: Dict = {}
            self._nodes: Dict = {}
            self._links: Dict = {}
            self._id: int = 0

    def __get_new_id(self):
        self._id += 1
        return self._id


    def add_entity(self, entity: object):
        """
        Add an object with an id
        """
        # Set new id to re'cent entoty
        entity.id = self.__get_new_id()
        key = entity.__class__.__name__ + str(entity.id)
        n = _Node(entity)
        self._nodes[key] = n
        self._repo.setdefault(entity.__class__.__name__, {})[entity.id] = n
        return entity

    
    def replace_entity(self, entity: object):
        """
        Add an object with an id
        """
        key = entity.__class__.__name__ + str(entity.id)
        self._nodes[key].set_entity(entity)
        return entity


    def get_entity(self, cls: Type[Any], object_id: int):
        """
        Get object for class cls with specific id object_id
        """
        key = cls.__name__ + str(object_id)
        return self._nodes.get(key, None).entity

    
    def get_entity_by_value(self, cls: Type[Any], field: str, value: Any):
        """
        Get object for class cls with specific value of an attribute
        """
        cls_repo = self._nodes.get(cls.__name__, {})
        result = [node.entity for key, node in cls_repo.items() if node.entity.__dict__[field]==value]
        return result


    def get_entities_type(self, cls: Type[Any]):
        """
        Get all entities for a specific class
        """
        return [node.entity for node in self._repo.get(cls.__name__, {}).values()]


    def delete_entity(self, cls: Type[Any], object_id: int):
        """
        Delete object for class cls with specific id object_id
        """
        key = cls.__name__ + str(object_id)
        node = self._nodes.pop(key, None)
        self.__delete_all_relations(node.entity)
        del self._repo.get(cls.__name__, {})[object_id]
        
    
    def add_relation(self, source: object, target: object, relation: str):
        """
        Add an oriented relation between two entities and reciprocity if specified
        """
        skey = source.__class__.__name__ + str(source.id)        
        tkey = target.__class__.__name__ + str(target.id)
        self._links.setdefault(skey, {}).setdefault(relation, []).append(tkey)
        self._links.setdefault(tkey, {}).setdefault(relation, []).append(skey)


    def remove_relation(self, source: object, target: object, relation: str):
        """
        Remove an oriented relation and its reciprocity idf specified
        """
        skey = source.__class__.__name__ + str(source.id)        
        tkey = target.__class__.__name__ + str(target.id)
        self._links.setdefault(skey, {}).setdefault(relation, []).remove(tkey)
        self._links.setdefault(tkey, {}).setdefault(relation, []).remove(skey)


    def __delete_all_relations(self, entity: object):
        key = entity.__class__.__name__ + str(entity.id)
        for relation, other_keys in self._links[key].items():
            for other_key in other_keys:
                del self._links[other_key][relation]
        del self._links[key]

