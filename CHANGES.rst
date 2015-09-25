=========
Changelog
=========

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
