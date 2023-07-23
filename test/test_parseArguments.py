#pylint: disable=C0103
"""Module providing parse_arguments function unit tests"""

# pylint: disable=C0413, E0401
import unittest

# Import src function
import sys
import os.path
src_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_dir)
from main import parse_arguments

# pylint: enable=C0413, E0401

class ParseArgumentsUnitTests(unittest.TestCase):
    """Class containing unit tests for the parse_arguments function"""

    def basic_test(self):
        """A basic test of the function"""
        parse_arguments([])

if __name__ == '__main__':
    unittest.main()
