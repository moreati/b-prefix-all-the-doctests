r"""
>>> import sys
>>> import bar
>>> myrepr = bar.PrefixRepr()
>>> repr = myrepr.repr
>>> def _displayhook(value):
...     if value is not None:
...         sys.stdout.write(myrepr.repr(value))
>>> sys.displayhook = _displayhook
>>> u''
u''
>>> b''
b''
>>> bytes()
b''
>>> b'\0'
b'\x00'
>>> b"'"
b"'"
"""


def split(s):
    """
    >>> import sys
    >>> import bar
    >>> myrepr = bar.PrefixRepr()
    >>> repr = myrepr.repr
    >>> def _displayhook(value):
    ...     if value is not None:
    ...         sys.stdout.write(myrepr.repr(value))
    >>> sys.displayhook = _displayhook
    >>> repr = myrepr
    >>> split(u'a b c d e')
    [u'a', u'b', u'c', u'd', u'e']

    >>> split(b'a b c d e')
    [b'a', b'b', b'c', b'd', b'e']
    """
    return s.split()

def C(object):
    def join(self, seq):
        """
        >>> import sys
        >>> import bar
        >>> myrepr = bar.PrefixRepr()
        >>> repr = myrepr.repr
        >>> def _displayhook(value):
        ...     if value is not None:
        ...         sys.stdout.write(myrepr.repr(value))
        >>> sys.displayhook = _displayhook
        >>> c = C()
        >>> c.join([b'a', b'b', b'c', b'd', b'e']
        b'a!b!c!d!e'
        """
        return b'!'.join(seq)

