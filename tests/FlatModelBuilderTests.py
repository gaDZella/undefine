import unittest
import FlatModelBuilder
from Model.FragmentType import FragmentType
from Model.Fragment import Fragment


class FlatModelBuilderTests(unittest.TestCase):

    def test_emptyFile(self):
        file = ""
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [])

    def test_singleLineFile(self):
        file = "abc\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("abc\n", FragmentType.Body)
        ])

    def test_IfConditionSimple(self):
        file = " #if   test1 \nendif"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            (" #if   test1 \n", FragmentType.IfStatement),
            ("endif", FragmentType.Body)
        ])

    def test_IfCondition(self):
        file = "#if test1 && test2 || test3\nend"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#if test1 && test2 || test3\n", FragmentType.IfStatement),
            ("end", FragmentType.Body)
        ])

    def test_IfElseCondition(self):
        file = "#if cond \nifBody\n#else\nelseBody\n#endif"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#if cond \n", FragmentType.IfStatement),
            ("ifBody\n", FragmentType.Body),
            ("#else\n", FragmentType.ElseStatement),
            ("elseBody\n", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement),
        ])

    def test_IfConditionComplex(self):
        file = "#if !test1 && (!test2 || test3) \n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#if !test1 && (!test2 || test3) \n", FragmentType.IfStatement)
        ])

    def test_ElifConditionComplex(self):
        file = "#elif !test1 && (!test2 || test3) \n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#elif !test1 && (!test2 || test3) \n", FragmentType.ElIfStatement)
        ])

    def test_singleBody(self):
        file = "a\n#if DebugTest\nbb\nccc\n#endif\neeee"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("a\n", FragmentType.Body),
            ("#if DebugTest\n", FragmentType.IfStatement),
            ("bb\nccc\n", FragmentType.Body),
            ("#endif\n", FragmentType.EndIfStatement),
            ("eeee", FragmentType.Body)
        ])

    def test_Constants(self):
        file = 'string if = "#if", else = "#else", elif = "#elif", endif = "#endif";'
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ('string if = "#if", else = "#else", elif = "#elif", endif = "#endif";', FragmentType.Body)
        ])

    def test_Comment(self):
        file = "// comment\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("// comment\n", FragmentType.Body)
        ])

    def test_Comment2(self):
        file = "// #if test\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("// #if test\n", FragmentType.Body)
        ])

    def test_MultilineComment(self):
        file = "/* test*/\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("/* test*/\n", FragmentType.Body)
        ])

    def test_LineCommentInsideMultilineComment(self):
        file = "/* \n // test \n */end"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("/* \n // test \n */end", FragmentType.Body)
        ])

    def test_MultiLineCommentInsideLineComment(self):
        file = "// /* \n #if test \n //*/"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("// /* \n", FragmentType.Body),
            (" #if test \n", FragmentType.IfStatement),
            (" //*/", FragmentType.Body)
        ])

    def test_MultiLineCommentInsideLineComment_Complex(self):
        file = "// /* */ /* \n #if test // /* \n //*/ */"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("// /* */ /* \n", FragmentType.Body),
            (" #if test ", FragmentType.IfStatement),
            ("// /* \n //*/ */", FragmentType.Body)
        ])

    def test_IfInsideMultilineComment(self):
        file = "/* \n // #if test\n */ #endif\n*/"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("/* \n // #if test\n */", FragmentType.Body),
            (" #endif\n", FragmentType.EndIfStatement),
            ("*/", FragmentType.Body)
        ])

    def test_LineCommentInIfLine(self):
        file = "#if x // comment\n body \n #endif\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#if x ", FragmentType.IfStatement),
            ("// comment\n body \n", FragmentType.Body),
            (" #endif\n", FragmentType.EndIfStatement)
        ])

    def test_LineCommentEndIfEOF(self):
        file = "//#if x\n//body\n//#endif"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("//#if x\n//body\n//#endif", FragmentType.Body)
        ])

    def test_embeddedConditions(self):
        file = "#if dt\n line1\n #if sl\n line 2\n #else\n line 3\n #endif\n line 4\n #endif"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#if dt\n", FragmentType.IfStatement),
            (" line1\n", FragmentType.Body),
            (" #if sl\n", FragmentType.IfStatement),
            (" line 2\n", FragmentType.Body),
            (" #else\n", FragmentType.ElseStatement),
            (" line 3\n", FragmentType.Body),
            (" #endif\n", FragmentType.EndIfStatement),
            (" line 4\n", FragmentType.Body),
            (" #endif", FragmentType.EndIfStatement)
        ])

    def test_IfNotCondition(self):
        file = "#if!test1 && test2\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#if!test1 && test2\n", FragmentType.IfStatement)
        ])

    def test_ElIfNotCondition(self):
        file = "#elif!test1 && test2\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("#elif!test1 && test2\n", FragmentType.ElIfStatement)
        ])

    def test_IfConditionSpaces(self):
        file = "    #       if test1 && test2\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       if test1 && test2\n", FragmentType.IfStatement)
        ])

    def test_ElIfConditionSpaces(self):
        file = "    #       elif test1 && test2\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       elif test1 && test2\n", FragmentType.ElIfStatement)
        ])

    def test_ElseConditionSpaces(self):
        file = "    #       else\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       else\n", FragmentType.ElseStatement)
        ])

    def test_EndIfConditionSpaces(self):
        file = "    #       endif\n"
        m = FlatModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       endif\n", FragmentType.EndIfStatement)
        ])

    def _check_Model(self, act, exp):
        self.assertEqual(len(act), len(exp))
        exp = list(Fragment(t[1], t[0]) for t in exp)
        for i in range(0, len(exp)):
            check_fragments(self, act[i], exp[i])


def check_fragments(self, act, exp):
    self.assertEqual(act.type, exp.type)
    self.assertEqual(act.text, exp.text)