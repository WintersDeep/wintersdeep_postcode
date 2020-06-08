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
from wintersdeep_postcode.postcode_types.standard_postcode import StandardPostcode

## Unit Test class for the StandardPostcode class
class TestStandardPostcode(TestCase):

    ## tests that the function responsible for creating the parser regex, respects the
    #  whitespace delimiter that is passed to it.
    def test__StandardPostcode_GetParseRegex__delimiter(self):

        from re import error

        test_A_delimiter = StandardPostcode.GetParseRegex("A")
        self.assertIsNotNone ( test_A_delimiter.match("E20A2ST") )
        self.assertIsNone    ( test_A_delimiter.match("E20 2ST") )
        self.assertIsNone    ( test_A_delimiter.match("WHATEVR") )
        self.assertRaises(error, StandardPostcode.GetParseRegex, '[')

    ## tests that, at a glance, the regular expression being returned by the factory
    #  appears to able to successfully parse good values, and reject bad ones.
    def test__StandardPostcode_GetParseRegex__regex(self):
        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        self.assertIsNotNone( test_regex.match("A0 0AA") )
        self.assertIsNotNone( test_regex.match("A00 0AA") )
        self.assertIsNotNone( test_regex.match("A0A 0AA") )
        self.assertIsNotNone( test_regex.match("AA0 0AA") )
        self.assertIsNotNone( test_regex.match("AA00 0AA") )
        self.assertIsNotNone( test_regex.match("AA0A 0AA") )

    ## tests that the standard postcode object allocates local members as expected.
    def test__StadardPostcode_ctor(self):
    
        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
    
        regex_match = test_regex.match("A1 2BC")
        test_postcode = StandardPostcode(regex_match)
        self.assertEqual(test_postcode.outward_area, "A")
        self.assertEqual(test_postcode.outward_district, 1)
        self.assertEqual(test_postcode.outward_subdistrict, "")
        self.assertEqual(test_postcode.inward_sector, 2)
        self.assertEqual(test_postcode.inward_unit, "BC")

        regex_match = test_regex.match("A12 3BC")
        test_postcode = StandardPostcode(regex_match)
        self.assertEqual(test_postcode.outward_area, "A")
        self.assertEqual(test_postcode.outward_district, 12)
        self.assertEqual(test_postcode.outward_subdistrict, "")
        self.assertEqual(test_postcode.inward_sector, 3)
        self.assertEqual(test_postcode.inward_unit, "BC")
        
        regex_match = test_regex.match("A1B 2CD")
        test_postcode = StandardPostcode(regex_match)
        self.assertEqual(test_postcode.outward_area, "A")
        self.assertEqual(test_postcode.outward_district, 1)
        self.assertEqual(test_postcode.outward_subdistrict, "B")
        self.assertEqual(test_postcode.inward_sector, 2)
        self.assertEqual(test_postcode.inward_unit, "CD")
        
        regex_match = test_regex.match("AB1 2CD")
        test_postcode = StandardPostcode(regex_match)
        self.assertEqual(test_postcode.outward_area, "AB")
        self.assertEqual(test_postcode.outward_district, 1)
        self.assertEqual(test_postcode.outward_subdistrict, "")
        self.assertEqual(test_postcode.inward_sector, 2)
        self.assertEqual(test_postcode.inward_unit, "CD")
        
        regex_match = test_regex.match("AB12 3CD")
        test_postcode = StandardPostcode(regex_match)
        self.assertEqual(test_postcode.outward_area, "AB")
        self.assertEqual(test_postcode.outward_district, 12)
        self.assertEqual(test_postcode.outward_subdistrict, "")
        self.assertEqual(test_postcode.inward_sector, 3)
        self.assertEqual(test_postcode.inward_unit, "CD")
        
        regex_match = test_regex.match("AB1C 2DE")
        test_postcode = StandardPostcode(regex_match)
        self.assertEqual(test_postcode.outward_area, "AB")
        self.assertEqual(test_postcode.outward_district, 1)
        self.assertEqual(test_postcode.outward_subdistrict, "C")
        self.assertEqual(test_postcode.inward_sector, 2)
        self.assertEqual(test_postcode.inward_unit, "DE")

        # final check for some general properties
        self.assertEqual(test_postcode.postcode_type, "standard")
        self.assertFalse(test_postcode.is_validated)
        self.assertIs(test_postcode._original_regex_match, regex_match)

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()