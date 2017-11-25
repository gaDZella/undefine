import json
import unittest
import SharpCleaner
import tempfile
import shutil
import os


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_dir = tempfile.gettempdir()
        cls.test_dir = os.path.join(env_dir, "clean#Tests")
        shutil.rmtree(cls.test_dir, ignore_errors=True)
        shutil.copytree(os.path.join(os.path.dirname(SharpCleaner.__file__), "tests", "testFiles"), cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def test_choice_1(self):
        self._test_chose(1)

    def test_choice_2(self):
        self._test_chose(2)

    def _test_choice_3_encodings(self):
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

    def test_choice_11(self):
        self._test_chose(11)

    def _test_chose(self, name):
        in_file_path = str.format("{}/{}.in.cs", self.test_dir, name)
        out_file_path = str.format("{}/{}.out.cs", self.test_dir, name)
        keys_json_path = str.format("{}/{}.args.json", self.test_dir, name)
        with open(keys_json_path) as keys_file:
            keys = json.load(keys_file)
        p = SharpCleaner.SharpCleaner(keys)
        p.clean_file(in_file_path)
        self._assert_files_are_equal(out_file_path, in_file_path)

    def _assert_files_are_equal(self, expected, actual):
        with open(expected, 'r') as ef:
            e_data = ef.read()
        with open(actual, 'r') as af:
            a_data = af.read()
        self.assertMultiLineEqual(a_data, e_data)
