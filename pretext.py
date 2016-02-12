from __future__ import print_function

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

try:
    import reprlib
except ImportError:
    import repr as reprlib

import sys

__all__ = [
    'activate',
    'Repr',
    'PrefixRepr',
    'BytesRepr',
    'UnicodeRepr',
    'prepr',
    'urepr',
    'pdisplayhook',
    'bdisplayhook',
    'udisplayhook',
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
        self.maxlong = sys.maxsize
        self.maxtuple = sys.maxsize
        self.maxother = sys.maxsize

    def repr_bool(self, obj, level):
        return '%s' % obj


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

    def repr_bytes(self, obj, level):
        return self._old_repr(obj)

    def repr_unicode(self, obj, level):
        return self._old_repr(obj)


class BytesRepr(PrefixRepr):
    """A Repr that prefixes byte strings, and doesn't truncate

    This mirrors the behaviour of repr() in Python 3.x.

    >>> py3_repr = BytesRepr().repr
    >>> py3_repr(b'0123456789')
    "b'0123456789'"
    >>> py3_repr(u'0123456789')
    "'0123456789'"
    """

    def repr_str(self, obj, level):
        if str is bytes:
            # Python 2.x
            return b'b%s' % (self._old_repr(obj),)
        else:
            # Python 3.x
            return self._old_repr(obj)

    def repr_unicode(self, obj, level):
        # Only Python 2.x has a builtin type called unicode
        r = self._old_repr(obj)
        assert r[0] == 'u'
        return r[1:]


class UnicodeRepr(PrefixRepr):
    """A Repr that prefixes textual (unicode) strings & doesn't truncate

    This mirrors the behaviour of repr() in Python 2.x.

    >>> py2_repr = UnicodeRepr().repr
    >>> py2_repr(b'0123456789')
    "'0123456789'"
    >>> py2_repr(u'0123456789')
    "u'0123456789'"
    """

    def repr_str(self, obj, level):
        if str is bytes:
            return self._old_repr(obj)
        else:
            return u'u%s' % (self._old_repr(obj),)

    def repr_bytes(self, obj, level):
        r = self._old_repr(obj)
        assert r[0] == 'b'
        return r[1:]


prepr = PrefixRepr().repr
brepr = BytesRepr().repr
urepr = UnicodeRepr().repr

def _displayhook(value, repr_fn):
    if value is None:
        return
    # Set '_' to None to avoid recursion
    builtins._ = None
    text = repr_fn(value)
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        bytes = text.encode(sys.stdout.encoding, 'backslashreplace')
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(bytes)
        else:
            text = bytes.decode(sys.stdout.encoding, 'strict')
            sys.stdout.write(text)
    sys.stdout.write("\n")
    builtins._ = value

def pdisplayhook(value):
    _displayhook(value, prepr)

def bdisplayhook(value):
    _displayhook(value, brepr)

def udisplayhook(value):
    _displayhook(value, urepr)

def activate(repr=brepr, displayhook=bdisplayhook):
    """Replace the builtin repr & sys.displayhook with versions that prefix

    The defaults causes the repr() of any string to be the same as it would
    on Python 3.x. So after `activate()` is called `repr(b'foo') == "b'foo'"`
    and `repr(u'bar') == "'bar'"`. Even on Python 2.x.

    >>> import pretext; pretext.activate()
    >>> b'Now your byte-string doctests can work on Python 2.6, 2.7, & 3.3+'
    b'Now your byte-string doctests can work on Python 2.6, 2.7, & 3.3+'
    >>> u"By default unicode strings aren't prefixed, just like on Python 3.x"
    "By default unicode strings aren't prefixed, just like on Python 3.x"

    >>> pretext.activate(pretext.urepr, pretext.udisplayhook)
    >>> [b'However you can choose Python 2.x', u'behaviour if you prefer']
    ['However you can choose Python 2.x', u'behaviour if you prefer']

    >>> pretext.activate(pretext.prepr, pretext.pdisplayhook)
    >>> (b'Or prefix all the strings', u'all the time')
    (b'Or prefix all the strings', u'all the time')
    """
    builtins.repr = repr
    sys.displayhook = displayhook

