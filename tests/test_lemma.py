import unittest
from pylila.lemma import Lemma


class TestSum(unittest.TestCase):
    def test_valid_lemma(self):
        l = Lemma('86867')
        self.assertTrue(len(l.graph) > 0)

    def test_invalid_lemma(self):
        l = Lemma('ciccio')
        self.assertFalse(len(l.graph) > 0)
