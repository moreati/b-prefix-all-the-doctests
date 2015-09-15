doctest-prefix-all-the-literals
===============================

This package is an experiment in writing doctests that involve strings,
and that are cross-compatible with Python 2.6, 2.7, and 3.3+.

The problem
-----------

Suppose you have the following doctest

.. code:: python

    >>> myfunc()
    u'I return a textual (unicode) string'

    >>> otherfunc()
    b'I return a byte (binary) string'

On Python 3.x the first test case will fail, because doctest will compare
the repr(myfunc()) will not include the u'' prefix.

On Python 2.x the second test will fail, because repr(otherfunc()) will
not include the b'' prefix.

If the tests cases are editted to remove the prefixes, i.e.

.. code:: python

    >>> myfunc()
    'I return a textual (unicode) string'

    >>> otherfunc()
    'I return a byte (binary) string'

then the failures will be reversed. myfunc() will now fail on Python 2.x,
otherfunc will fail on Python 3.x.

The hack
--------

Replace `repr()` and `sys.displayhook` with versions that always prefix
string literals, regardless of the Python version. Now the doctests can

 - directly show the string values returned by functions/methods,
   without resorting to `print()`, or .encode() etc
 - test the examples on all Python versions 

.. include:: foo.py

Alternatives
------------

If you're ready to run screaming at the above, there are alternatives e.g.

 - Wrap bytestring returns in `bytearray()`.
   `repr(bytearray(b'abc')) == "bytearray(b'abc'))"` on all versions of
   python that have `bytearray()` (2.6 onward) e.g.

   ::
       >>> bytearray(otherfunc())
       bytearray(b'I return a byte (binary) string')

