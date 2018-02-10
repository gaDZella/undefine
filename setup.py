import unittest
from setuptools import setup


def test_suite():
    test_loader = unittest.TestLoader()
    suite = test_loader.discover('tests', pattern='*.py')
    return suite


setup(
    name="undefine",
    version="0.0.1",
    description="C# Preprocessor tool",
    install_requires=["joblib", "chardet", "sympy"],
    test_suite='setup.test_suite'
)
