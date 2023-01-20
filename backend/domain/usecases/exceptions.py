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


class LoginAlreadyUsed(Exception):
    """
    Exception when a login is already used by an user
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)


class CredentialException(Exception):
    """
    Exception when checking token
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)


