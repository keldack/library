# https://qastack.fr/programming/6760685/creating-a-singleton-in-python
# Méthode par métaclasse

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(object):
    _instance = None
    _initDone = False
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self): self._initDone = True

    def initDone(self): return self._initDone