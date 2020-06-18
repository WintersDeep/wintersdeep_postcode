# python3 imports
from os.path import abspath, dirname, join
from sys import path as python_path
from unittest import TestCase

# determine where we are running (needed to patch PYTHON_PATH)
TEST_CASE_PATH = abspath( __file__ )
TEST_CASE_DIRECTORY = dirname( TEST_CASE_PATH )
PROJECT_ROOT_DIRECTORY = abspath( join( TEST_CASE_DIRECTORY, ".." ) )

# patch up PYTHON_PATH if required.
if not PROJECT_ROOT_DIRECTORY in python_path:
    python_path.insert(0, PROJECT_ROOT_DIRECTORY)

# project imports
from wintersdeep_postcode.exceptions.parse_error import ParseError

## Unit Test class for ParseError
class TestParseError(TestCase):

    ## Tests that the parse error object is being properly derived - possibly a 
    #  trivial check, but ensures that we remember to note this as a breaking
    #  change if we modify it down the line (some people may catch on these types)
    def test__ParseError__parse_error_types(self):
        parser_obj = object()
        error_object = ParseError("", parser_obj)
        self.assertIsInstance(error_object, Exception)
        self.assertIsInstance(error_object, ValueError)
        self.assertIsInstance(error_object, ParseError)
        self.assertNotIsInstance(error_object, TypeError)

    ## Tests that parse errors are being constructed properly.
    def test__ParseError_ctor(self):
        parser_obj = object()
        error_object = ParseError("abc123", parser_obj)
        self.assertEqual( str(error_object), "Invalid postcode structure 'abc123'." )
        self.assertEqual( error_object.source_input, 'abc123')
        self.assertIs( error_object.source_parser, parser_obj )

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()