"""Module providing parse_arguments function unit tests"""
import unittest

# Import src function
import sys
import os.path
src_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_dir)
from main import parse_arguments

class ParseArgumentsUnitTests(unittest.TestCase):
    """Class containing unit tests for the parse_arguments function"""


if __name__ == '__main__':
    unittest.main()
