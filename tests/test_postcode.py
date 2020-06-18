# python3 imports
from os.path import abspath, dirname, join
from sys import path as python_path
from unittest import TestCase
from re import compile

# determine where we are running (needed to patch PYTHON_PATH)
TEST_CASE_PATH = abspath( __file__ )
TEST_CASE_DIRECTORY = dirname( TEST_CASE_PATH )
PROJECT_ROOT_DIRECTORY = abspath( join( TEST_CASE_DIRECTORY, ".." ) )

# patch up PYTHON_PATH if required.
if not PROJECT_ROOT_DIRECTORY in python_path:
    python_path.insert(0, PROJECT_ROOT_DIRECTORY)

# project imports
from wintersdeep_postcode.postcode import Postcode

## Unit Test class for Postcode
class TestPostcode(TestCase):

    ## tests that the Postcode CompileRegex function works as expected.
    def test__Postcode_CompileRegex(self):

        # make sure we are actually compiling - this should throw
        from re import error
        self.assertRaises(error, Postcode.CompileRegex, '[')

        # make sure we are anchoring and preserving case senstivity
        regex = Postcode.CompileRegex('this')
        self.assertIsNotNone(regex.match('this'))
        self.assertIsNone(regex.match(' this'))
        self.assertIsNone(regex.match('this '))
        self.assertIsNone(regex.match('THIS'))

        regex = Postcode.CompileRegex("this","and","that")
        self.assertIsNotNone(regex.match('thisandthat'))
        self.assertIsNone(regex.match('this'))

    ## test the Postcode classes ctor
    def test__Postcode_ctor(self):
        fake_regex = object()
        postcode = Postcode(fake_regex)
        self.assertIs(postcode._original_regex_match, fake_regex)
        self.assertFalse(postcode.is_validated)

    ## tests the Poscode postcode_type accessor
    def test__Postcode_postcode_type(self):
        fake_regex = object()
        postcode = Postcode(fake_regex)
        self.assertEqual(postcode.postcode_type, "unspecified")

    ## test the repr function of the postcode.
    def test__Postcode_repr(self):
        from wintersdeep_postcode import parse_postcode
        self.assertEqual( repr( parse_postcode("WR1 2AX") ), "<StandardPostcode: WR1 2AX>" )
        self.assertEqual( repr( parse_postcode("GIR 0AA") ), "<SpecialCasePostcode: GIR 0AA>" )

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()