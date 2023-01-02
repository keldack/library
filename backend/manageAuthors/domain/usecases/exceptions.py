class KeyDoesNotExist(Exception):
    """
    Exception for a specific key of an entity that does not exist
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)