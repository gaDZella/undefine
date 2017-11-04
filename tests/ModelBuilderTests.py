import unittest
from ModelBuilder import *
from FileModel.FragmentType import *


class ModelBuilderTests(unittest.TestCase):

    def test_emptyFile(self):
        file = ""
        m = ModelBuilder.build(file)

        self.assertEqual(0, len(m.fragments))

    def test_singleLineFile(self):
        file = "abc\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))
        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("abc\n", m.fragments[0].text)

    def test_IfConditionSimple(self):
        file = " #if   test1 \nendif"
        m = ModelBuilder.build(file)

        self.assertEqual(2, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual(" #if   test1 \n", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("endif", m.fragments[1].text)

    def test_IfCondition(self):
        file = "#if test1 && test2 || test3\nend"
        m = ModelBuilder.build(file)

        self.assertEqual(2, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("#if test1 && test2 || test3\n", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("end", m.fragments[1].text)

    def test_IfElseCondition(self):
        file = "#if cond \nifBody\n#else\nelseBody\n#endif"
        m = ModelBuilder.build(file)

        self.assertEqual(5, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("#if cond \n", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("ifBody\n", m.fragments[1].text)

        self.assertEqual(FragmentType.ElseStatement, m.fragments[2].type)
        self.assertEqual("#else\n", m.fragments[2].text)

        self.assertEqual(FragmentType.Body, m.fragments[3].type)
        self.assertEqual("elseBody\n", m.fragments[3].text)

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[4].type)
        self.assertEqual("#endif", m.fragments[4].text)

    def test_IfConditionComplex(self):
        file = "#if !test1 && (!test2 || test3) \n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("#if !test1 && (!test2 || test3) \n", m.fragments[0].text)

    def test_ElifConditionComplex(self):
        file = "#elif !test1 && (!test2 || test3) \n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.ElIfStatement, m.fragments[0].type)
        self.assertEqual("#elif !test1 && (!test2 || test3) \n", m.fragments[0].text)

    def test_singleBody(self):
        file = "a#if DebugTest\nbb\nccc\n#endif\neeee"
        m = ModelBuilder.build(file)

        self.assertEqual(5, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("a", m.fragments[0].text)

        self.assertEqual(FragmentType.IfStatement, m.fragments[1].type)
        self.assertEqual("#if DebugTest\n", m.fragments[1].text)

        self.assertEqual(FragmentType.Body, m.fragments[2].type)
        self.assertEqual("bb\nccc\n", m.fragments[2].text)

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[3].type)
        self.assertEqual("#endif\n", m.fragments[3].text)

        self.assertEqual(FragmentType.Body, m.fragments[4].type)
        self.assertEqual("eeee", m.fragments[4].text)

    def test_Comment(self):
        file = "// comment\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("// comment\n", m.fragments[0].text)

    def test_Comment2(self):
        file = "// #if test\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("// #if test\n", m.fragments[0].text)

    def test_MultilineComment(self):
        file = "/* test*/\n"
        m = ModelBuilder.build(file)

        self.assertEqual(2, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("/* test*/", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("\n", m.fragments[1].text)

    def test_LineCommentInsideMultilineComment(self):
        file = "/* \n // test \n */end"
        m = ModelBuilder.build(file)

        self.assertEqual(2, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("/* \n // test \n */", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("end", m.fragments[1].text)

    def test_IfInsideMultilineComment(self):
        file = "/* \n // #if test\n */ #endif\n*/"
        m = ModelBuilder.build(file)

        self.assertEqual(3, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("/* \n // #if test\n */", m.fragments[0].text)

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[1].type)
        self.assertEqual(" #endif\n", m.fragments[1].text)

        self.assertEqual(FragmentType.Body, m.fragments[2].type)
        self.assertEqual("*/", m.fragments[2].text)

    def test_LineCommentInIfLine(self):
        file = "#if x // comment\n body \n #endif\n"
        m = ModelBuilder.build(file)

        self.assertEqual(4, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("#if x ", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("// comment\n", m.fragments[1].text)

        self.assertEqual(FragmentType.Body, m.fragments[2].type)
        self.assertEqual(" body \n", m.fragments[2].text)

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[3].type)
        self.assertEqual(" #endif\n", m.fragments[3].text)

    def test_LineCommentEndIfEOF(self):
        file = "//#if x\n//body\n//#endif"
        m = ModelBuilder.build(file)

        self.assertEqual(3, len(m.fragments))

        self.assertEqual(FragmentType.Body, m.fragments[0].type)
        self.assertEqual("//#if x\n", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual("//body\n", m.fragments[1].text)

        self.assertEqual(FragmentType.Body, m.fragments[2].type)
        self.assertEqual("//#endif", m.fragments[2].text)

    def test_embeddedConditions(self):
        file = "#if dt\n line1\n #if sl\n line 2\n #else\n line 3\n #endif\n line 4\n #endif"
        m = ModelBuilder.build(file)

        self.assertEqual(9, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("#if dt\n", m.fragments[0].text)

        self.assertEqual(FragmentType.Body, m.fragments[1].type)
        self.assertEqual(" line1\n", m.fragments[1].text)

        self.assertEqual(FragmentType.IfStatement, m.fragments[2].type)
        self.assertEqual(" #if sl\n", m.fragments[2].text)

        self.assertEqual(FragmentType.Body, m.fragments[3].type)
        self.assertEqual(" line 2\n", m.fragments[3].text)

        self.assertEqual(FragmentType.ElseStatement, m.fragments[4].type)
        self.assertEqual(" #else\n", m.fragments[4].text)

        self.assertEqual(FragmentType.Body, m.fragments[5].type)
        self.assertEqual(" line 3\n", m.fragments[5].text)

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[6].type)
        self.assertEqual(" #endif\n", m.fragments[6].text)

        self.assertEqual(FragmentType.Body, m.fragments[7].type)
        self.assertEqual(" line 4\n", m.fragments[7].text)

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[8].type)
        self.assertEqual(" #endif", m.fragments[8].text)

    def test_IfNotCondition(self):
        file = "#if!test1 && test2\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("#if!test1 && test2\n", m.fragments[0].text)

    def test_ElIfNotCondition(self):
        file = "#elif!test1 && test2\n"
        model = ModelBuilder.build(file)

        self.assertEqual(1, len(model.fragments))

        self.assertEqual(FragmentType.ElIfStatement, model.fragments[0].type)
        self.assertEqual("#elif!test1 && test2\n", model.fragments[0].text)

    def test_IfConditionSpaces(self):
        file = "    #       if test1 && test2\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.IfStatement, m.fragments[0].type)
        self.assertEqual("    #       if test1 && test2\n", m.fragments[0].text)

    def test_ElIfConditionSpaces(self):
        file = "    #       elif test1 && test2\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.ElIfStatement, m.fragments[0].type)
        self.assertEqual("    #       elif test1 && test2\n", m.fragments[0].text)

    def test_ElseConditionSpaces(self):
        file = "    #       else\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.ElseStatement, m.fragments[0].type)
        self.assertEqual("    #       else\n", m.fragments[0].text)

    def test_EndIfConditionSpaces(self):
        file = "    #       endif\n"
        m = ModelBuilder.build(file)

        self.assertEqual(1, len(m.fragments))

        self.assertEqual(FragmentType.EndIfStatement, m.fragments[0].type)
        self.assertEqual("    #       endif\n", m.fragments[0].text)