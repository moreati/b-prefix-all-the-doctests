pretext
=======

.. image:: https://travis-ci.org/moreati/b-prefix-all-the-doctests.svg
    :target: https://travis-ci.org/moreati/b-prefix-all-the-doctests

This package makes it easy to write doctests that involve strings, and
still have those doctests work with Python 2.6, 2.7, and 3.3+.

Just `import pretext` and call `pretext.activate()`. By default Python 3.x
`repr()` behaviour is used

.. code:: python

    >>> import pretext; pretext.activate()
    >>> b'Now strings have a consistant repr on Python 2.x & 3.x'
    b'Now strings have a consistant repr on all Python versions'
    >>> u'Unicode strings & nested strings work too'.split()
    ['Unicode', 'strings', '&', 'nested', 'strings', 'work', 'too']

The problem
-----------

Suppose you have the following doctest, and you aren't using pretext

.. code:: python

    >>> textfunc()
    u'I return a textual (unicode) string'

    >>> bytesfunc()
    b'I return a byte (binary) string'

On Python 2.x ``textfunc()`` will pass. On Python 3.x it will fail.
This is because doctest compares the expected value with ``repr(textfunc())``,
and on Python 3.x the `repr()` will not include a ``u''`` prefix.

On Python 2.x ``bytesfunc()`` will fail. On Python 3.x it will pass.
This is because on Python 2.x ``repr(bytesfunc())`` won't include the ``b''``
prefix.

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
