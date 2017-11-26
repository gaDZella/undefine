import json
import unittest
import SharpCleaner
import tempfile
import shutil
import os
from CleanResult import CleanResult


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
        self._test_choice(1)

    def test_choice_1_1(self):
        self._test_choice("1_1")

    def test_choice_2(self):
        self._test_choice(2)

    def _test_choice_3_encodings(self):
        self._test_choice("3_encodings")

    def test_choice_4(self):
        self._test_choice(4)

    def test_choice_5(self):
        self._test_choice(5)

    def test_choice_6(self):
        self._test_choice(6)

    def test_choice_7(self):
        self._test_choice(7)

    def test_choice_8(self):
        self._test_choice(8)

    def test_choice_9(self):
        self._test_choice(9)

    def test_choice_10(self):
        self._test_choice(10)

    def test_choice_11(self):
        self._test_choice(11)

    def test_choice_syntax_error(self):
        self._test_choice("syntax_error")

    def _test_choice(self, name):
        in_file_path = str.format("{}/{}.in.cs", self.test_dir, name)
        out_file_path = str.format("{}/{}.out.cs", self.test_dir, name)
        keys_json_path = str.format("{}/{}.args.json", self.test_dir, name)
        res_json_path = str.format("{}/{}.res.json", self.test_dir, name)
        with open(keys_json_path) as keys_file:
            keys = json.load(keys_file)
        with open(res_json_path) as res_file:
            res = json.load(res_file)
        with open(out_file_path, 'r') as out_file:
            exp_text = out_file.read()

        exp_res = CleanResult(exp_text, res["error"], res["code_lines"], res["total_lines"])
        p = SharpCleaner.SharpCleaner(keys)
        act_res = p.clean_file(in_file_path, False)
        self._assert_results_are_equal(exp_res, act_res)

    def _assert_results_are_equal(self, exp, act):
        self.assertEqual(exp.error, act.error, "error")
        if exp.error is None:
            self.assertMultiLineEqual(exp.text, act.text, "text")
        self.assertEqual(exp.total_lines, act.total_lines, "total_lines")
        self.assertEqual(exp.code_lines, act.code_lines, "code_lines")
