# python3 imports
from os.path import abspath, dirname, join
from sys import path as python_path
from unittest import TestCase
from re import compile

# determine where we are running (needed to patch PYTHON_PATH)
TEST_CASE_PATH = abspath( __file__ )
TEST_CASE_DIRECTORY = dirname( TEST_CASE_PATH )
PROJECT_ROOT_DIRECTORY = abspath( join( TEST_CASE_DIRECTORY, ".." , "..") )

# patch up PYTHON_PATH if required.
if not PROJECT_ROOT_DIRECTORY in python_path:
    python_path.insert(0, PROJECT_ROOT_DIRECTORY)

# project imports
from wintersdeep_postcode.postcode import Postcode

## Unit Test class for the postcode_types module
class TestPostcodeTypesModule(TestCase):

    ## tests that the module exports are setup correctly, any change to this 
    #  constitutes breaking changes
    def test__postcode_types__exports(self):

        # makes sure these still exist 
        from wintersdeep_postcode.postcode_types import \
            postcode_type_objects, postcode_type_keys, postcode_type_map

        # make sure all the lists are populated.
        self.assertGreater( len(postcode_type_objects), 0 ) 
        self.assertGreater( len(postcode_type_keys), 0 ) 
        self.assertGreater( len(postcode_type_map.items()), 0 ) 

        # make sure all the types being expressed are what we expect.
        self.assertTrue( all( issubclass(t, Postcode) for t in postcode_type_objects ) )
        self.assertTrue( all( isinstance(t, str) for t in postcode_type_keys ) )
        self.assertTrue( all( isinstance(t[0], str) and issubclass(t[1], Postcode) \
            for t in postcode_type_map.items() ) )


if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()