pretext
=======

.. image:: https://travis-ci.org/moreati/b-prefix-all-the-doctests.svg
    :target: https://travis-ci.org/moreati/b-prefix-all-the-doctests

Write doctests with strings that work in Python 2.x *and* Python 3.x.

Just `import pretext` and call `pretext.activate()`. By default Python 3.x
`repr()` behaviour is used

.. code:: python

    >>> import pretext; pretext.activate()
    >>> b'Byte strings now have the same repr on Python 2.x & 3.x'
    b'Byte strings now have the same repr on Python 2.x & 3.x'
    >>> u'Unicode strings & nested strings work too'.split()
    ['Unicode', 'strings', '&', 'nested', 'strings', 'work', 'too']

The problem
-----------

Suppose you have the following functions and doctests

.. code:: python

    def textfunc():
        """
        >>> textfunc()
        u'A unicode string'
        """
        return u'A unicode string'

    def bytesfunc()
        """
        >>> bytesfunc()
        b'A byte string'
        """
        return b'A byte string'

Without pretext

- ``textfunc()`` will pass on Python 2.x, but fail on 3.x.
- ``bytesfunc()`` will fail on Python 2.x, but pass on 3.x.

This is because doctest compares the expected result (from the doc-string)
with the ``repr()`` of the returned value.

- ``repr(u'foo')`` returns ``u'foo'`` on Python 2.x, but ``'foo'`` on 3.x
- ``repr(b'bar')`` returns ``'bar'`` on Python 2.x, but ``b'bar'`` on 3.x

If the doctests are editted to remove the prefixes

.. code:: python

    def textfunc():
        """
        >>> textfunc()
        'A unicode string'
        """
        return u'A unicode string'

    def bytesfunc()
        """
        >>> bytesfunc()
        'A byte string'
        """
        return b'A byte string'

then the failures will be reversed

- ``textfunc()`` will now fail on Python 2.x, but pass on 3.x.
- ``bytesfunc()`` will now pass on Python 2.x, but fail on 3.x.

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
    >>> import pretext
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

If you're ready to run screaming at the above, there are alternatives

- pytest_ provides ``#doctest: ALLOW_UNICODE`` and (from 2.9.0) ``#doctest: ALLOW_BYTES`` directives_

- `lxml`_ includes `lxml.html.usedoctest`_ and `lxml.usedoctest`_ modules for HTML and XML.

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

.. _pytest: http://pytest.org
.. _directives: http://pytest.org/latest/doctest.html
.. _lxml: https://pypi.python.org/pypi/lxml
.. _lxml.html.usedoctest: http://lxml.de/api/lxml.html.usedoctest-module.html
.. _lxml.usedoctest: http://lxml.de/api/lxml.usedoctest-module.html
