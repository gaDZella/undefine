import unittest
from ModelBuilder import ModelBuilder
from FileModel.FragmentType import FragmentType


class ModelBuilderTests(unittest.TestCase):

    def test_emptyFile(self):
        file = ""
        m = ModelBuilder.build(file)

        self._check_Model(m, [])

    def test_singleLineFile(self):
        file = "abc\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("abc\n", FragmentType.Body)
        ])

    def test_IfConditionSimple(self):
        file = " #if   test1 \nendif"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            (" #if   test1 \n", FragmentType.IfStatement),
            ("endif", FragmentType.Body)
        ])

    def test_IfCondition(self):
        file = "#if test1 && test2 || test3\nend"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#if test1 && test2 || test3\n", FragmentType.IfStatement),
            ("end", FragmentType.Body)
        ])

    def test_IfElseCondition(self):
        file = "#if cond \nifBody\n#else\nelseBody\n#endif"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#if cond \n", FragmentType.IfStatement),
            ("ifBody\n", FragmentType.Body),
            ("#else\n", FragmentType.ElseStatement),
            ("elseBody\n", FragmentType.Body),
            ("#endif", FragmentType.EndIfStatement),
        ])

    def test_IfConditionComplex(self):
        file = "#if !test1 && (!test2 || test3) \n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#if !test1 && (!test2 || test3) \n", FragmentType.IfStatement)
        ])

    def test_ElifConditionComplex(self):
        file = "#elif !test1 && (!test2 || test3) \n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#elif !test1 && (!test2 || test3) \n", FragmentType.ElIfStatement)
        ])

    def test_singleBody(self):
        file = "a#if DebugTest\nbb\nccc\n#endif\neeee"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("a", FragmentType.Body),
            ("#if DebugTest\n", FragmentType.IfStatement),
            ("bb\nccc\n", FragmentType.Body),
            ("#endif\n", FragmentType.EndIfStatement),
            ("eeee", FragmentType.Body)
        ])

    def test_Comment(self):
        file = "// comment\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("// comment\n", FragmentType.Body)
        ])

    def test_Comment2(self):
        file = "// #if test\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("// #if test\n", FragmentType.Body)
        ])

    def test_MultilineComment(self):
        file = "/* test*/\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("/* test*/", FragmentType.Body),
            ("\n", FragmentType.Body)
        ])

    def test_LineCommentInsideMultilineComment(self):
        file = "/* \n // test \n */end"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("/* \n // test \n */", FragmentType.Body),
            ("end", FragmentType.Body)
        ])

    def test_IfInsideMultilineComment(self):
        file = "/* \n // #if test\n */ #endif\n*/"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("/* \n // #if test\n */", FragmentType.Body),
            (" #endif\n", FragmentType.EndIfStatement),
            ("*/", FragmentType.Body)
        ])

    def test_LineCommentInIfLine(self):
        file = "#if x // comment\n body \n #endif\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#if x ", FragmentType.IfStatement),
            ("// comment\n", FragmentType.Body),
            (" body \n", FragmentType.Body),
            (" #endif\n", FragmentType.EndIfStatement)
        ])

    def test_LineCommentEndIfEOF(self):
        file = "//#if x\n//body\n//#endif"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("//#if x\n", FragmentType.Body),
            ("//body\n", FragmentType.Body),
            ("//#endif", FragmentType.Body)
        ])

    def test_embeddedConditions(self):
        file = "#if dt\n line1\n #if sl\n line 2\n #else\n line 3\n #endif\n line 4\n #endif"
        m = ModelBuilder.build(file)

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
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#if!test1 && test2\n", FragmentType.IfStatement)
        ])

    def test_ElIfNotCondition(self):
        file = "#elif!test1 && test2\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("#elif!test1 && test2\n", FragmentType.ElIfStatement)
        ])

    def test_IfConditionSpaces(self):
        file = "    #       if test1 && test2\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       if test1 && test2\n", FragmentType.IfStatement)
        ])

    def test_ElIfConditionSpaces(self):
        file = "    #       elif test1 && test2\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       elif test1 && test2\n", FragmentType.ElIfStatement)
        ])

    def test_ElseConditionSpaces(self):
        file = "    #       else\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       else\n", FragmentType.ElseStatement)
        ])

    def test_EndIfConditionSpaces(self):
        file = "    #       endif\n"
        m = ModelBuilder.build(file)

        self._check_Model(m, [
            ("    #       endif\n", FragmentType.EndIfStatement)
        ])

    def _check_Model(self, act, exp):
        self.assertEqual(len(act), len(exp))

        for i in range(0, len(exp)):
            self.assertEqual(act[i].text, exp[i][0])
            self.assertEqual(act[i].type, exp[i][1])
