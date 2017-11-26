import unittest
from BlockModelBuilder import build, SyntaxException
from FileModel.ConditionBlock import ConditionBlock
from FileModel.Branch import Branch
from tests.FlatModelBuilderTests import check_fragments
from FileModel.FragmentType import FragmentType
from FileModel.FileFragment import FileFragment


class BlockModelBuilderTests(unittest.TestCase):
    def test_empty(self):
        b = self._build_Model([])

        self._check_Model(b, [])

    def test_single_if_block(self):
        b = self._build_Model([
            ("#if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "#if a"),
                        [
                            "a body"
                        ])
                ],
                "#endif"
            )
        ])

    def test_single_empty_if_block(self):
        b = self._build_Model([
            ("#if a", FragmentType.IfStatement),
            ("#endif", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "#if a"),
                        [])
                ],
                "#endif"
            )
        ])

    def test_single_if_block_with_context(self):
        b = self._build_Model([
            ("before", FragmentType.Body),
            ("#if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement),
            ("after", FragmentType.Body),
        ])

        self._check_Model(b, [
            "before",
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "#if a"),
                        [
                            "a body"
                        ])
                ],
                "#endif"
            ),
            "after"
        ])

    def test_nested_single_if_block(self):
        b = self._build_Model([
            ("#if a", FragmentType.IfStatement),
            ("#if b", FragmentType.IfStatement),
            ("b body", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement),
            ("#endif", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "#if a"),
                        [
                            ConditionBlock(
                                [
                                    Branch(
                                        FileFragment(FragmentType.IfStatement, "#if b"),
                                        [
                                            "b body"
                                        ])
                                ],
                                "#endif"
                            )
                        ])
                ],
                "#endif"
            )
        ])

    def test_single_if_else_block(self):
        b = self._build_Model([
            ("#if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("#else", FragmentType.ElseStatement),
            ("else body", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "#if a"),
                        [
                            "a body"
                        ]),
                    Branch(
                        FileFragment(FragmentType.ElseStatement, "#else"),
                        [
                            "else body"
                        ])
                ],
                "#endif"
            )
        ])

    def test_single_if_elif_elif_else_block(self):
        b = self._build_Model([
            ("#if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("#elif b", FragmentType.ElIfStatement),
            ("b body", FragmentType.Body),
            ("#elif c", FragmentType.ElIfStatement),
            ("c body", FragmentType.Body),
            ("#else", FragmentType.ElseStatement),
            ("else body", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "#if a"),
                        [
                            "a body"
                        ]),
                    Branch(
                        FileFragment(FragmentType.ElIfStatement, "#elif b"),
                        [
                            "b body"
                        ]),
                    Branch(
                        FileFragment(FragmentType.ElIfStatement, "#elif c"),
                        [
                            "c body"
                        ]),
                    Branch(
                        FileFragment(FragmentType.ElseStatement, "#else"),
                        [
                            "else body"
                        ]),
                ],
                "#endif"
            )
        ])

    def test_complex_nested_blocks(self):
        b = self._build_Model([
            ("if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("elif b", FragmentType.ElIfStatement),
            ("b body", FragmentType.Body),
            ("if aa", FragmentType.IfStatement),
            ("if aaa", FragmentType.IfStatement),
            ("aaa body", FragmentType.Body),
            ("endif aaa", FragmentType.EndIfStatement),
            ("else", FragmentType.ElseStatement),
            ("else aa body", FragmentType.Body),
            ("endif aa", FragmentType.EndIfStatement),
            ("b body2", FragmentType.Body),
            ("endif b", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                [
                    Branch(
                        FileFragment(FragmentType.IfStatement, "if a"),
                        [
                            "a body"
                        ]),
                    Branch(
                        FileFragment(FragmentType.ElIfStatement, "elif b"),
                        [
                            "b body",
                            ConditionBlock(
                                [
                                    Branch(
                                        FileFragment(FragmentType.IfStatement, "if aa"),
                                        [
                                            ConditionBlock(
                                                [
                                                    Branch(
                                                        FileFragment(FragmentType.IfStatement, "if aaa"),
                                                        [
                                                            "aaa body"
                                                        ])
                                                ],
                                                "endif aaa"
                                            ),
                                        ]),
                                    Branch(
                                        FileFragment(FragmentType.ElseStatement, "else"),
                                        [
                                            "else aa body"
                                        ])
                                ],
                                "endif aa"
                            ),
                            "b body2"
                        ])
                ],
                "endif b"
            )
        ])

    def test_exception_no_endif(self):
        self.assertRaises(SyntaxException, lambda: self._build_Model([
            ("if a", FragmentType.IfStatement)
        ]))

    def test_exception_elif_only(self):
        self.assertRaises(SyntaxException, lambda: self._build_Model([
            ("elif a", FragmentType.ElIfStatement)
        ]))

    def test_exception_else_only(self):
        self.assertRaises(SyntaxException, lambda: self._build_Model([
            ("else", FragmentType.ElseStatement)
        ]))

    def test_exception_endif_only(self):
        self.assertRaises(SyntaxException, lambda: self._build_Model([
            ("endif", FragmentType.EndIfStatement)
        ]))

    def test_exception_2_endif(self):
        self.assertRaises(SyntaxException, lambda: self._build_Model([
            ("if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("endif", FragmentType.EndIfStatement),
            ("endif", FragmentType.EndIfStatement)
        ]))

    def test_exception_nested_not_paired(self):
        self.assertRaises(SyntaxException, lambda: self._build_Model([
            ("if a", FragmentType.IfStatement),
            ("if aa", FragmentType.IfStatement),
            ("aa body", FragmentType.Body),
            ("endif", FragmentType.EndIfStatement),
            ("else", FragmentType.ElseStatement),
            ("else body", FragmentType.Body),
        ]))

    @staticmethod
    def _build_Model(tuples):
        fs = (FileFragment(t[1], t[0]) for t in tuples)
        return list(build(fs))

    def _check_Model(self, act, exp):
        self.assertEqual(len(act), len(exp))

        for i in range(0, len(exp)):
            act_i = act[i]
            exp_i = exp[i]
            self.assertEqual(type(act_i), type(exp_i))
            if type(act_i) is ConditionBlock:
                self._check_Block(act_i, exp_i)
            else:
                self.assertEqual(act_i, exp_i)

    def _check_Block(self, act, exp):
        self.assertEqual(len(act.branches), len(exp.branches))
        for i in range(0, len(exp.branches)):
            self._check_Branches(act.branches[i], exp.branches[i])
        self.assertEqual(act.end, exp.end)

    def _check_Branches(self, act, exp):
        check_fragments(self, act.condition, exp.condition)
        self._check_Model(act.body, exp.body)
