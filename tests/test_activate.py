"""
>>> import sys, pretext
>>> pretext.activate()
>>> bytes()
b''
>>> b'0123456789'
b'0123456789'
>>> u'0123456789'
'0123456789'
"""


def str_func():
    """
    This function's doctest does not override displayhook, thus checking
    that other doctests do not leak their sys.displayhook override.

    >>> str_func()
    'I return a native str'
    """
    return 'I return a native str'


def bytes_func():
    """
    >>> import sys, pretext
    >>> pretext.activate()
    >>> bytes_func()
    b'I return a byte string'
    """
    return b'I return a byte string'


def textual_func():
    """
    >>> import sys, pretext
    >>> pretext.activate(pretext.urepr, pretext.udisplayhook)
    >>> textual_func()
    u'I return a textual (unicode) string'
    """
    return u'I return a textual (unicode) string'

def bool_func(rv):
    """
    >>> import sys, pretext; pretext.activate()
    >>> bool_func(True)
    True
    >>> bool_func(False)
    False
    >>> 1 == 1
    True
    >>> 1 == 2
    False
    """
    return rv
