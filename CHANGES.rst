=========
Changelog
=========

0.0.5
-----

.. attention:: This will be the final release of this module.
    I've agreed to transfer the package name to the `PreTeXt books`_ project.
    To continue using this module pin you version to `pretext<0.1`.

* Documentation fixups

.. _PreTeXt books: https://pretextbook.org/

0.0.4
-----

* Fixed #2: `repr` of `bool` instances [thanks to John Vandenberg]
* Changed development status to Beta

0.0.3
-----

* Added ``pretext.activate()`` for instant gratification

0.0.2
-----

* Added ``prepr()`` convenience function. This mimics the builtin ``repr()``
  but always prefixes byte strings with `b` and textual strings with `u`.
* Added ``UnicodeRepr``/``urepr()`` and ``BytesRepr``/``brepr()``
  to mimic Python 2.x ``repr()`` and ``Python 3.x`` repr() respectively
* Added ``pdisplayhook()``, ``udisplayhook()``, ``bdisplayhook`` for
  conveniently overriding ``sys.displayhook``

0.0.1
-----

* Initial release
