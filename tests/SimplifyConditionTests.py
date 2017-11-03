import unittest
from Condition import *


class SimplifyConditionTests(unittest.TestCase):
    def test_no_keys(self):
        condition = "!(aB || b) &&   (c)|| ! Ab"
        res = Condition.simplify(condition, {})

        self.assertEqual("!(aB || b) &&   (c)|| ! Ab", res)

    def test_missing_key(self):
        condition = "!(aB || b) &&   (c)|| ! Ab"
        res = Condition.simplify(condition, {"d": True})

        self.assertEqual("!(aB || b) &&   (c)|| ! Ab", res)

    def test_1_true(self):
        condition = "(a && b)"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual('b', res)

    def test_1_false(self):
        condition = "(a && b)"
        res = Condition.simplify(condition, {"a": False})

        self.assertEqual(False, res)

    def test_IgnoreCase(self):
        condition = "(a && A) && aA"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual('aA', res)

    def test_IgnoreCase2(self):
        condition = "( a && !A) || a1 || !A2"
        res = Condition.simplify(condition, {"A": True})

        self.assertEqual('a1 || !A2', res)

    def test_1_true_2(self):
        condition = "a || b"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual(True, res)

    def test_1_complex(self):
        condition = "!(a || b) && c || !d"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual("!d", res)

    def test_2_complex(self):
        condition = "((a && c) || (!b && d)) && !e"
        res = Condition.simplify(condition, {"a": True, "b": False})

        self.assertEqual("!e && (c || d)", res)
