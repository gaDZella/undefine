import unittest
import Condition


class SimplifyConditionTests(unittest.TestCase):
    def test_no_keys_no_simplification(self):
        condition = "!(aB || b) &&   (c)|| ! Ab"
        res = Condition.simplify(condition, {})

        self.assertEqual("!(aB || b) &&   (c)|| ! Ab", res)

    def test_missing_key_no_simplification(self):
        condition = "!(aB || b) &&   (c)|| ! Ab"
        res = Condition.simplify(condition, {"d": True})

        self.assertEqual("!(aB || b) &&   (c)|| ! Ab", res)

    def test_equals_true(self):
        condition = "a == true"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual(True, res)

    def test_equals_false(self):
        condition = "a == false"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual(False, res)

    # sympy issue ((
    def _test_equals_in_brackets(self):
        condition = "(a == true)"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual(True, res)

    def test_true(self):
        condition = "true"
        res = Condition.simplify(condition, {})

        self.assertEqual(True, res)

    def test_false(self):
        condition = "false"
        res = Condition.simplify(condition, {})

        self.assertEqual(False, res)

    def test_1_simple_and_true(self):
        condition = "(a && b)"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual('b', res)

    def test_1_simple_and_false(self):
        condition = "(a && b)"
        res = Condition.simplify(condition, {"a": False})

        self.assertEqual(False, res)

    def test_1_simple_or_true(self):
        condition = "a || b"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual(True, res)

    def test_1_simple_or_false(self):
        condition = "a || b"
        res = Condition.simplify(condition, {"a": False})

        self.assertEqual("b", res)

    def test_ignore_case(self):
        condition = "(a && A) && aA"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual('aA', res)

    def test_ignore_case2(self):
        condition = "( a && !A) || a1 || !A2"
        res = Condition.simplify(condition, {"A": True})

        self.assertEqual('a1 || !A2', res)

    def test_1_complex(self):
        condition = "!(a || b) && c || !d"
        res = Condition.simplify(condition, {"a": True})

        self.assertEqual("!d", res)

    def test_2_complex(self):
        condition = "((a && c) || (!b && d)) && !e"
        res = Condition.simplify(condition, {"a": True, "b": False})

        self.assertEqual("!e && (c || d)", res)
