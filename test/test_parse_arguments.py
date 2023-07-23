#pylint: disable=C0103
"""Module providing parse_arguments function unit tests"""

# pylint: disable=C0413, E0401
import unittest
from unittest.mock import patch
from io import StringIO

# Import src function
import sys
import os.path
src_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_dir)
from main import parse_arguments
# pylint: enable=C0413, E0401

class ParseArgumentsUnitTests(unittest.TestCase):
    """Class containing unit tests for the parse_arguments function"""

    def test_expected_input(self):
        """A basic test of the function"""
        args = parse_arguments(['input.csv', 'output.csv'])
        self.assertTrue(args.src_file[0] == 'input.csv')
        self.assertTrue(args.out_file[0] == 'output.csv')

    @patch('sys.stderr', new_callable=StringIO)
    def test_missing_output_file(self, mock_stderr):
        """Test behavior with missing output file"""
        with self.assertRaises(SystemExit):
            _ = parse_arguments(['input.csv'])
        expected_error = r"error: the following arguments are required: out_file"
        self.assertRegex(mock_stderr.getvalue(), expected_error)

    @patch('sys.stderr', new_callable=StringIO)
    def test_missing_both_files(self, mock_stderr):
        """Test behavior with both files missing"""
        with self.assertRaises(SystemExit):
            _ = parse_arguments([])
        expected_error = r"error: the following arguments are required: src_file, out_file"
        self.assertRegex(mock_stderr.getvalue(), expected_error)

    @patch('sys.stderr', new_callable=StringIO)
    def test_no_arguments(self, mock_stderr):
        """Test behavior with no provided arguments"""
        with self.assertRaises(SystemExit):
            _ = parse_arguments(None)
        expected_error = r"error: the following arguments are required: src_file, out_file"
        self.assertRegex(mock_stderr.getvalue(), expected_error)

if __name__ == '__main__':
    unittest.main()
