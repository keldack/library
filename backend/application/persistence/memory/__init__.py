from config.singleton import Singleton
from typing import Type, Any, Dict, Sequence


class _Node:

    def __init__(self, entity: Any):
        self.entity = entity

    def set_entity(self, entity: Any):
        self.entity = entity

# class _Link:

#     def __init__(self, source: _Node, target: _Node):
#         self.source = source
#         self.target = target

        
class MemoryDatabase(Singleton):
    """
    Memory Repository is just a domain entity object storage like a DB memory. It is instantiated as singleton
    """

    def __init__(self):
        
        if not self.initDone():
            Singleton.__init__(self)
            self._nodes: Dict[str, Dict[str, _Node]] = {}
            self._links: Dict[str, Dict[str, _Node]] = {}
            self._ids: Dict[str, int] = {}

    def __get_new_id(self, key: str):
        self._ids[key] = self._ids.get(key, 0) + 1
        return self._ids[key]


    def add_entity(self, entity: object):
        """
        Add an object with an id
        """
        # Set new id to recent entity
        type_ = entity.__class__.__name__
        entity.id = self.__get_new_id(type_)
        key = type_ + str(entity.id)
        self._nodes.setdefault(type_, {})[key] = _Node(entity)
        print(f"{type_} / {key} added")
        return entity

    
    def replace_entity(self, entity: object):
        """
        Add an object with an id
        """
        type_ = entity.__class__.__name__
        key = type_ + str(entity.id)
        self._nodes[type_][key].set_entity(entity)
        return entity


    def get_entity(self, cls: Type[Any], object_id: int):
        """
        Get object for class cls with specific id object_id
        """
        type_ = cls.__name__
        if type_ in self._nodes:
            key = type_ + str(object_id)
            if key in self._nodes[type_]:
                return self._nodes[type_][key].entity
        return None
        
    
    def get_entity_by_value(self, cls: Type[Any], field: str, value: Any):
        """
        Get object for class cls with specific value of an attribute
        """
        cls_repo = self._nodes.get(cls.__name__, {})
        return [node.entity for _, node in cls_repo.items() if node.entity.__dict__[field]==value]


    def get_entities_type(self, cls: Type[Any]):
        """
        Get all entities for a specific class
        """
        return [node.entity for node in self._nodes.get(cls.__name__, {}).values()]


    def delete_entity(self, cls: Type[Any], object_id: int):
        """
        Delete object for class cls with specific id object_id
        """
        type_ = cls.__name__
        key = type_ + str(object_id)
        self.__delete_all_relations(key)
        del self._nodes.get(type_, {})[key]
        
    
    def add_relation(self, source: object, target: object, relation: str):
        """
        Add an oriented relation between two entities and reciprocity if specified
        """
        stype = source.__class__.__name__
        ttype = target.__class__.__name__
        skey = stype + str(source.id)        
        tkey = ttype + str(target.id)
        self._links.setdefault(skey, {}).setdefault(relation, []).append((ttype, tkey))
        self._links.setdefault(tkey, {}).setdefault(relation, []).append((stype, skey))


    def remove_relation(self, source: object, target: object, relation: str):
        """
        Remove an oriented relation and its reciprocity idf specified
        """
        stype = source.__class__.__name__
        ttype = target.__class__.__name__
        skey = stype + str(source.id)        
        tkey = ttype + str(target.id)
        self._links.setdefault(skey, {}).setdefault(relation, []).remove((ttype, tkey))
        self._links.setdefault(tkey, {}).setdefault(relation, []).remove((stype, skey))


    def get_relations(self, entity: object, relation: str) -> Sequence[object]:
        """
        Get entities for a relation from an object
        """
        key = entity.__class__.__name__ + str(entity.id)
        result = []
        if key in self._links:
            result = [
                self._nodes[type_key][object_key].entity for type_key, object_key in self._links[key].get(relation, [])
            ]
        return result

    def __delete_all_relations(self, node_key: str):
        """
        Delete all relations for a key of node
        """
        if node_key in self._links:
            for relation, other_keys in self._links[node_key].items():
                for type_key, other_key in other_keys:
                    del self._links[other_key][relation]
            del self._links[node_key]

