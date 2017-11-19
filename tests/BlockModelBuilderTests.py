import unittest
from BlockModelBuilder import BlockModelBuilder
from FileModel.ConditionBlock import ConditionBlock
from FileModel.Branch import Branch
from tests.FlatModelBuilderTests import check_fragments
from FileModel.FragmentType import FragmentType
from FileModel.FileFragment import  FileFragment


class BlockModelBuilderTests(unittest.TestCase):

    def test_1(self):
        b = self._build_Model([
            ("#if a", FragmentType.IfStatement),
            ("a body", FragmentType.Body),
            ("#else", FragmentType.ElseStatement),
            ("else body", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement)
        ])

        self._check_Model(b, [
            ConditionBlock(
                Branch(FileFragment(
                    FragmentType.IfStatement, "#if a"),
                    [
                        "a body"
                    ]),
                [
                    Branch(FileFragment(
                        FragmentType.ElseStatement, "#else"),
                        [
                            "else body"
                        ]),

                ],
                "#endif"
            )
        ])

    def _build_Model(self, tuples):
        fs = (FileFragment(t[1], t[0]) for t in tuples)
        return list(BlockModelBuilder.build(fs))

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
        self._check_Branches(act.start, exp.start)
        self.assertEqual(len(act.next), len(exp.next))
        for i in range(0, len(exp.next)):
            self._check_Branches(act.next[i], exp.next[i])
        self.assertEqual(act.end, exp.end)

    def _check_Branches(self, act, exp):
        check_fragments(self, act.condition, exp.condition)
        self._check_Model(act.body, exp.body)
