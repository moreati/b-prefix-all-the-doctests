import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from hypothesis import given
from hypothesis import strategies as st

from pretext import prepr, brepr, urepr


@unittest.skipUnless(sys.version_info[0] == 2, "Python 2.x only")
class Python2TestCase(unittest.TestCase):
    @given(st.binary())
    def test_urepr_bytes(self, s):
        self.assertEqual(repr(s), urepr(s))

    @given(st.text())
    def test_urepr_unicode(self, s):
        self.assertEqual(repr(s), urepr(s))

    @given(st.lists(st.sampled_from([st.binary(), st.text()])))
    def test_urepr_in_list(self, l):
        self.assertEqual(repr(l), urepr(l))

    @given(st.binary())
    def test_brepr_bytes(self, s):
        self.assertEqual('b'+repr(s), brepr(s))

    @given(st.binary())
    def test_prepr_bytes(self, s):
        self.assertEqual('b'+repr(s), prepr(s))


@unittest.skipUnless(sys.version_info[0] == 3, "Python 3.x only")
class Python3TestCase(unittest.TestCase):

    @given(st.binary())
    def test_prepr_bytes(self, s):
        self.assertEqual(repr(s), brepr(s))

    @given(st.text())
    def test_brepr_unicode(self, s):
        self.assertEqual(repr(s), brepr(s))

    @given(st.lists(st.sampled_from([st.binary(), st.text()])))
    def test_brepr_in_list(self, l):
        self.assertEqual(repr(l), brepr(l))

    @given(st.text())
    def test_urepr_unicode(self, s):
        self.assertEqual('u'+repr(s), urepr(s))

    @given(st.text())
    def test_prepr_unicode(self, s):
        self.assertEqual('u'+repr(s), prepr(s))


if __name__ == '__main__':
    unittest.main()

