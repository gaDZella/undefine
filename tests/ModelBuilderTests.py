import unittest
from ModelBuilder import *
from FileModel.FragmentType import *


class ModelBuilderTests(unittest.TestCase):

    def test_emptyFile(self):
        testFile = ""
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(0, len(fileModel.fragments))

    def test_singleLineFile(self):
        testFile = "abc\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))
        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("abc\n", fileModel.fragments[0].text)

    def test_IfConditionSimple(self):
        testFile = " #if   test1 \nendif"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(2, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual(" #if   test1 \n", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual("endif", fileModel.fragments[1].text)

    def test_IfCondition(self):
        testFile = "#if test1 && test2 || test3\nend"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(2, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("#if test1 && test2 || test3\n", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual("end", fileModel.fragments[1].text)

    def test_IfElseCondition(self):
        testFile = "#if cond \nifBody\n#else\nelseBody\n#endif"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(5, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("#if cond \n", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual("ifBody\n", fileModel.fragments[1].text)

        self.assertEqual(FragmentType.ElseStatement, fileModel.fragments[2].type)
        self.assertEqual("#else\n", fileModel.fragments[2].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[3].type)
        self.assertEqual("elseBody\n", fileModel.fragments[3].text)

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[4].type)
        self.assertEqual("#endif", fileModel.fragments[4].text)

    def test_IfConditionComplex(self):
        testFile = "#if !test1 && (!test2 || test3) \n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("#if !test1 && (!test2 || test3) \n", fileModel.fragments[0].text)

    def test_ElifConditionComplex(self):
        testFile = "#elif !test1 && (!test2 || test3) \n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.ElIfStatement, fileModel.fragments[0].type)
        self.assertEqual("#elif !test1 && (!test2 || test3) \n", fileModel.fragments[0].text)

    def test_singleBody(self):
        testFile = "a#if DebugTest\nbb\nccc\n#endif\neeee"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(5, len(fileModel.fragments))

        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("a", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[1].type)
        self.assertEqual("#if DebugTest\n", fileModel.fragments[1].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[2].type)
        self.assertEqual("bb\nccc\n", fileModel.fragments[2].text)

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[3].type)
        self.assertEqual("#endif\n", fileModel.fragments[3].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[4].type)
        self.assertEqual("eeee", fileModel.fragments[4].text)

    def test_Comment(self):
        testFile = "// comment\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("// comment\n", fileModel.fragments[0].text)

    def test_Comment2(self):
        testFile = "// #if test\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("// #if test\n", fileModel.fragments[0].text)

    def test_MultilineComment(self):
        testFile = "/* test*/\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(2, len(fileModel.fragments))

        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("/* test*/", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual("\n", fileModel.fragments[1].text)

    def test_LineCommentInsideMultilineComment(self):
        testFile = "/* \n // test \n */end"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(2, len(fileModel.fragments))

        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("/* \n // test \n */", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual("end", fileModel.fragments[1].text)

    def test_IfInsideMultilineComment(self):
        testFile = "/* \n // #if test\n */ #endif\n*/"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(3, len(fileModel.fragments))

        self.assertEqual(FragmentType.Body, fileModel.fragments[0].type)
        self.assertEqual("/* \n // #if test\n */", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[1].type)
        self.assertEqual(" #endif\n", fileModel.fragments[1].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[2].type)
        self.assertEqual("*/", fileModel.fragments[2].text)

    def test_LineCommentInIfLine(self):
        testFile = "#if x // comment\n body \n #endif\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(4, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("#if x ", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual("// comment\n", fileModel.fragments[1].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[2].type)
        self.assertEqual(" body \n", fileModel.fragments[2].text)

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[3].type)
        self.assertEqual(" #endif\n", fileModel.fragments[3].text)

    def test_embeddedConditions(self):
        testFile = "#if dt\n line1\n #if sl\n line 2\n #else\n line 3\n #endif\n line 4\n #endif"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(9, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("#if dt\n", fileModel.fragments[0].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[1].type)
        self.assertEqual(" line1\n", fileModel.fragments[1].text)

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[2].type)
        self.assertEqual(" #if sl\n", fileModel.fragments[2].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[3].type)
        self.assertEqual(" line 2\n", fileModel.fragments[3].text)

        self.assertEqual(FragmentType.ElseStatement, fileModel.fragments[4].type)
        self.assertEqual(" #else\n", fileModel.fragments[4].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[5].type)
        self.assertEqual(" line 3\n", fileModel.fragments[5].text)

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[6].type)
        self.assertEqual(" #endif\n", fileModel.fragments[6].text)

        self.assertEqual(FragmentType.Body, fileModel.fragments[7].type)
        self.assertEqual(" line 4\n", fileModel.fragments[7].text)

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[8].type)
        self.assertEqual(" #endif", fileModel.fragments[8].text)

    def test_IfNotCondition(self):
        testFile = "#if!test1 && test2\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("#if!test1 && test2\n", fileModel.fragments[0].text)

    def test_ElIfNotCondition(self):
        testFile = "#elif!test1 && test2\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.ElIfStatement, fileModel.fragments[0].type)
        self.assertEqual("#elif!test1 && test2\n", fileModel.fragments[0].text)

    def test_IfConditionSpaces(self):
        testFile = "    #       if test1 && test2\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.IfStatement, fileModel.fragments[0].type)
        self.assertEqual("    #       if test1 && test2\n", fileModel.fragments[0].text)

    def test_ElIfConditionSpaces(self):
        testFile = "    #       elif test1 && test2\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.ElIfStatement, fileModel.fragments[0].type)
        self.assertEqual("    #       elif test1 && test2\n", fileModel.fragments[0].text)

    def test_ElseConditionSpaces(self):
        testFile = "    #       else\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.ElseStatement, fileModel.fragments[0].type)
        self.assertEqual("    #       else\n", fileModel.fragments[0].text)

    def test_EndIfConditionSpaces(self):
        testFile = "    #       endif\n"
        fileModel = ModelBuilder.build(testFile)

        self.assertEqual(1, len(fileModel.fragments))

        self.assertEqual(FragmentType.EndIfStatement, fileModel.fragments[0].type)
        self.assertEqual("    #       endif\n", fileModel.fragments[0].text)