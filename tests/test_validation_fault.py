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
from wintersdeep_postcode.exceptions.validation_fault import ValidationFault

## Unit Test class for ValidationFault
class TestValidationFault(TestCase):

    ## The error number base that should be used to offset this clases error ids.
    #  @remarks each class is reserved 100 numbers from its base number.
    FaultBaseId = 0

    ## Tests that the validation fault object is constructed properly, and rejects duplicate codes.
    def test__ValidationFault_ctor(self):
        test_fault_number = TestValidationFault.FaultBaseId + 1
        test_fault_description = "This is a test of the ValidationFault class."
        validation_fault = ValidationFault(test_fault_number, test_fault_description)
        self.assertEqual(validation_fault.description, test_fault_description)
        self.assertEqual(str(validation_fault), test_fault_description)
        self.assertEqual(int(validation_fault), test_fault_number)
        self.assertEqual(validation_fault.id, test_fault_number)
        
        test_fault_number2 = TestValidationFault.FaultBaseId + 2
        test_fault_description2 = "This is a second test of the ValidationFault class."
        validation_fault2 = ValidationFault(test_fault_number2, test_fault_description2)
        
        self.assertRaises(ValueError, ValidationFault, test_fault_number2, test_fault_description2)

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()