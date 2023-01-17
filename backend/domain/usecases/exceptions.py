class KeyDoesNotExist(Exception):
    """
    Exception for a specific key of an entity that does not exist
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ISBNAlreadyUsed(Exception):
    """
    Exception when ISBN is already used by a book reference
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)


class CopyAlreadyCheckouted(Exception):
    """
    Exception when a copy is already engaged in a checkout
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)
