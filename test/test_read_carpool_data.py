#pylint: disable=C0103
"""Module providing read_carpool_data function unit tests"""

# pylint: disable=C0413, E0401
import unittest
from unittest.mock import patch
from io import StringIO

# Import src function
import sys
import os.path
src_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_dir)
from main import read_carpool_data
# pylint: enable=C0413, E0401

class ReadCarpoolDataUnitTests(unittest.TestCase):
    """Class containing unit tests for the match_riders_randomly function"""

    def test_basic(self):
        """Test function"""
        return 0


if __name__ == '__main__':
    unittest.main()
