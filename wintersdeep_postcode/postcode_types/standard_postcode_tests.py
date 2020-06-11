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
        self.assertIsNotNone ( test_A_delimiter.match("E21A2ST") )
        self.assertIsNone    ( test_A_delimiter.match("E21 2ST") )
        self.assertIsNone    ( test_A_delimiter.match("WHATEVR") )
        self.assertRaises(error, StandardPostcode.GetParseRegex, '[')

    ## tests that, at a glance, the regular expression being returned by the factory
    #  appears to able to successfully parse good values, and reject bad ones.
    def test__StandardPostcode_GetParseRegex__regex(self):
        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        self.assertIsNotNone( test_regex.match("A1 1AA") )
        self.assertIsNotNone( test_regex.match("A11 1AA") )
        self.assertIsNotNone( test_regex.match("A1A 1AA") )
        self.assertIsNotNone( test_regex.match("AA1 1AA") )
        self.assertIsNotNone( test_regex.match("AA11 1AA") )
        self.assertIsNotNone( test_regex.match("AA1A 1AA") )

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

    ## Test that the standard postcodes outward code property words as expected.
    def test__StandardPostcode_outward_code(self):

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
     
        regex_match = test_regex.match("AB1C 2DE")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.outward_code, "AB1C")
        
        regex_match = test_regex.match("AB12 3CD")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.outward_code, "AB12")
        
        regex_match = test_regex.match("AB1 2CD")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.outward_code, "AB1")
        
        regex_match = test_regex.match("A1B 2CD")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.outward_code, "A1B")
        
        regex_match = test_regex.match("A12 3BC")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.outward_code, "A12")
        
        regex_match = test_regex.match("A1 2BC")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.outward_code, "A1")

    ## Test that the standard postcodes inward code property words as expected.
    def test__StandardPostcode_inward_code(self):

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
     
        regex_match = test_regex.match("AB1C 2DE")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.inward_code, "2DE")
        
        regex_match = test_regex.match("AB12 3CD")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.inward_code, "3CD")
        
        regex_match = test_regex.match("AB1 2CD")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.inward_code, "2CD")
        
        regex_match = test_regex.match("A1B 2CD")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.inward_code, "2CD")
        
        regex_match = test_regex.match("A12 3BC")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.inward_code, "3BC")
        
        regex_match = test_regex.match("A1 2BC")
        postcode = StandardPostcode(regex_match)
        self.assertEqual(postcode.inward_code, "2BC")

    ## Tests the the standard postcode object __str__ method works as expected.
    def test__StandardPostcode_str(self):

        test_candidates = [ 
            "AB1C 2DE", "AB12 3CD", "AB1 2CD", "A1B 2CD", "A12 3CD", "A1 2BC"
        ]

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        
        for test_string in test_candidates:
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertEqual( str(postcode), test_string)

    ## Tests that fault numbers haven't changed as this would constitute 
    #  breaking changes.
    def test__StandardPostcode__fault_numbers(self):
        self.assertEqual( int(StandardPostcode.ExpectedSingleDigitDistrict), 201 )
        self.assertEqual( int(StandardPostcode.ExpectedDoubleDigitDistrict), 202 )
        self.assertEqual( int(StandardPostcode.NoZeroDistrict), 203 )
        self.assertEqual( int(StandardPostcode.NoTenDistrict), 204 )
        self.assertEqual( int(StandardPostcode.SubdistrictsUnsupported), 205 )
        self.assertEqual( int(StandardPostcode.UnexpectedDistrictSubdivision), 206 )
        self.assertEqual( int(StandardPostcode.UnusedCharacterInFirstPosition), 207)

    ## Checks that the method we use to bind tests and faults is working
    def test__StandardPostcode_Validate__fault_assignment(self):
    
        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        
        # we'll just trigger a fault and make sure an error is assigned to it
        def check_for_fault(postcode, fault):
            regex_match = test_regex.match(postcode)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertTrue(fault in faults)
        
        check_for_fault("BR10 2XX", StandardPostcode.ExpectedSingleDigitDistrict)
        check_for_fault("LL9 2XX", StandardPostcode.ExpectedDoubleDigitDistrict)
        check_for_fault("LL0 2XX", StandardPostcode.NoZeroDistrict)
        check_for_fault("BL10 2XX", StandardPostcode.NoTenDistrict)            
        check_for_fault("XY7N 2XX", StandardPostcode.SubdistrictsUnsupported)            
        check_for_fault("N1S 2XX", StandardPostcode.UnexpectedDistrictSubdivision)            
        check_for_fault("X1 2XX", StandardPostcode.UnusedCharacterInFirstPosition)            




if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ## 

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()