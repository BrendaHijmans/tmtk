class ClassError(BaseException):
    """
    Error raised when unexpected class is found.

    :param found is the Object class of found
    :param expected is the required Object class.
    """
    def __init__(self, found, expected):
        self.found = found
        self.expected = expected

    def __str__(self):
        return "Got {} where {} was expected.".format(self.found, self.expected)


class DatatypeError(BaseException):
    """
    Error raised when incorrect datatype is found.

    :param found is the datatype of object.
    :param expected is the required datatype.
    """
    def __init__(self, found, expected):
        self.found = found
        self.expected = expected

    def __str__(self):
        return "Got {} where {} was expected.".format(self.found, self.expected)


class PathError(BaseException):
    """
    Error raised when not a correct path is given.
    """
    pass