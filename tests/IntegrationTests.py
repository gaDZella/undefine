import unittest
import SharpCleaner
import tempfile
import shutil
import os


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_dir = tempfile.gettempdir()
        cls.test_dir = env_dir + "/clean#Tests/singleTrue/"
        shutil.rmtree(cls.test_dir, ignore_errors=True)
        shutil.copytree(os.path.dirname(os.getcwd()) + "/tests/testFiles/singleTrue/", cls.test_dir)

    def test_choice_1(self):
        self._test_chose(1)

    def test_choice_2(self):
        self._test_chose(2)

    def test_choice_3_encodings(self):
        self._test_chose("3_encodings")

    def test_choice_4(self):
        self._test_chose(4)

    def test_choice_5(self):
        self._test_chose(5)

    def test_choice_6(self):
        self._test_chose(6)

    def test_choice_7(self):
        self._test_chose(7)

    def test_choice_8(self):
        self._test_chose(8)

    def test_choice_9(self):
        self._test_chose(9)

    def test_choice_10(self):
        self._test_chose(10)

    def _test_chose(self, number):
        file_name = str.format("{0}.cs", number)
        file = str.format("{}/{}/{}", self.test_dir, "source", file_name)
        e_file = str.format("{}/{}/{}", self.test_dir, "result", file_name)
        p = SharpCleaner.SharpCleaner({"TEST": True})
        p.clean_file(file)
        self._assert_files_are_equal(e_file, file)

    def _assert_files_are_equal(self, expected, actual):
        with open(expected, 'r') as ef:
            e_data = ef.read()
        with open(actual, 'r') as af:
            a_data = af.read()
        self.assertMultiLineEqual(a_data, e_data)
