doctest-prefix-all-the-strings
==============================

.. image:: https://travis-ci.org/moreati/pretext
    :target: https://travis-ci.org/moreati/pretext

This package is an experiment in writing doctests that involve strings,
and that are cross-compatible with Python 2.6, 2.7, and 3.3+.

The problem
-----------

Suppose you have the following doctest

.. code:: python

    >>> textfunc()
    u'I return a textual (unicode) string'

    >>> bytesfunc()
    b'I return a byte (binary) string'

On Python 3.x the first test case will fail, because doctest will compare
``repr(textfunc())`` which will not include a ``u''`` prefix.

On Python 2.x the second test will fail, because ``repr(bytesfunc())`` will
not include the ``b''`` prefix.

If the tests cases are editted to remove the prefixes, i.e.

.. code:: python

    >>> textfunc()
    'I return a textual (unicode) string'

    >>> bytesfunc()
    'I return a byte (binary) string'

then the failures will be reversed. ``textfunc()`` will now fail on Python 2.x,
``bytesfunc()`` will fail on Python 3.x.

The hack
--------

Replace ``repr()`` and ``sys.displayhook`` with versions that always prefix
string literals, regardless of the Python version. Now the doctests can

- directly show the string values returned by functions/methods,
  without resorting to ``print()``, or ``.encode()`` etc
- successfully test the examples on all Python versions 

Proof of concept:

.. code:: python

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


Alternatives
------------

If you're ready to run screaming at the above, there are alternatives e.g.

- Wrap byte-string returns in ``bytearray()``.
  ``repr(bytearray(b'abc')) == "bytearray(b'abc'))"`` on all versions of
  python that have ``bytearray()`` (2.6 onward) e.g.

  .. code:: python

       >>> bytearray(bytesfunc())
       bytearray(b'I return a byte (binary) string')

- Support Python 3.x exclusively
- Use ``print(bytesfunc().decode('ascii'))`` and choose your input values carefully
- Use ``#doctest: +SKIP``
- Use ``#doctest: +ELLIPSIS``
