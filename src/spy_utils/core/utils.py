def is_int(s):
    """
    Checks whether the string represents an integer.

    :param s: the string to check
    :type s: str
    :return: True if an integer
    :rtype: bool
    """
    try:
        int(s)
        return True
    except:
        return False


def is_float(s):
    """
    Checks whether the string represents a float.

    :param s: the string to check
    :type s: str
    :return: True if a float
    :rtype: bool
    """
    try:
        float(s)
        return True
    except:
        return False


def is_bool(s):
    """
    Checks whether the string represents a bool.

    :param s: the string to check
    :type s: str
    :return: True if a bool
    :rtype: bool
    """
    try:
        bool(s)
        return True
    except:
        return False
