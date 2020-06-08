# python3 imports
from os.path import abspath, dirname, join
from sys import path as python_path
from unittest import TestCase

# determine where we are running (needed to patch PYTHON_PATH)
TEST_CASE_PATH = abspath( __file__ )
TEST_CASE_DIRECTORY = dirname( TEST_CASE_PATH )
PROJECT_ROOT_DIRECTORY = abspath( join( TEST_CASE_DIRECTORY, "..", ".." ) )

# patch up PYTHON_PATH if required.
if not PROJECT_ROOT_DIRECTORY in python_path:
    python_path.insert(0, PROJECT_ROOT_DIRECTORY)

# project imports
from wintersdeep_postcode.exceptions.validation_error import ValidationError

## Unit Test class for ValidationError
class TestValidationError(TestCase):

    ## Tests that the validation error object is being properly derived - possibly a 
    #  trivial check, but ensures that we remember to note this as a breaking
    #  change if we modify it down the line (some people may catch on these types)
    def test__ValidationError__parse_error_types(self):
        parser_obj = object()
        error_object = ValidationError(None, {})
        self.assertIsInstance(error_object, Exception)
        self.assertIsInstance(error_object, ValueError)
        self.assertIsInstance(error_object, ValidationError)
        self.assertNotIsInstance(error_object, TypeError)

    ## Tests that parse errors are being constructed properly.
    def test__ValidationError_ctor(self):

        mock_postcode = object()
        fault_reasons = {
            1001: "a reason this isn't a postcode",
            1026: "another reason this isn't a postcode"
        }
        
        error_object = ValidationError(mock_postcode, fault_reasons)
        self.assertIs( error_object.postcode, mock_postcode)
        self.assertIs( error_object.faults, fault_reasons )

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()