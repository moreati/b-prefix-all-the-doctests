from __future__ import print_function

try:
    import reprlib
except ImportError:
    import repr as reprlib

import sys

__all__ = [
    'Repr',
    'PrefixRepr',
]


class Repr(reprlib.Repr):
    """A Repr that doesn't truncate it's output

    >>> myrepr = Repr().repr
    >>> myrepr('0123456789')
    "'0123456789'"
    >>> len(myrepr('0123456789'))
    12
    >>> len(myrepr('0123456789'*1000))
    10002
    """
    def __init__(self):
        self.maxlevel = sys.maxsize
        self.maxdict = sys.maxsize
        self.maxlist = sys.maxsize
        self.maxset = sys.maxsize
        self.maxfrozenset = sys.maxsize
        self.maxdeque = sys.maxsize
        self.maxarray = sys.maxsize
        self.maxlong = sys.maxsize
        self.maxstring = sys.maxsize
        self.maxother = sys.maxsize


class PrefixRepr(Repr):
    """A Repr that always prefixes any string, and doesn't truncate

    For byte strings this mirrors the behaviour of repr() in Python 3.x.
    For textual strings this mirrors the behaviour of repr() in Python 2.x.

    >>> prefix_repr = PrefixRepr().repr
    >>> prefix_repr(b'0123456789')
    "b'0123456789'"
    >>> prefix_repr(u'0123456789')
    "u'0123456789'"
    """

    def __init__(self):
        Repr.__init__(self)
        self._old_repr = repr

    def repr_str(self, obj, level):
        """Return the repr of a string, prefixed with b or u
        """
        if str is bytes:
            # Python 2.x
            return b'b%s' % (self._old_repr(obj),)
        else:
            # Python 3.x
            return u'u%s' % (self._old_repr(obj),)

