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

    ## Wikipedia: Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE
    #  LD, SM, SR, WC, WN, ZE. Tests that standard postcode observes these rules.
    def test__StandardPostcode_Validate__single_digit_districts(self):

        from wintersdeep_postcode.exceptions.validation_error import ValidationError

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "BR", "FY", "HA", "HD", "HG", "HR", "HS", 
            "HX", "JE", "LD", "SM", "SR", "WC", "WN", "ZE" ]

        expected_error = StandardPostcode.ExpectedSingleDigitDistrict
        self.assertEqual(int(expected_error), 201)

        for test in test_raises_fault:

            test_string = fr"{test}9 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertFalse(faults)

            test_string = fr"{test}10 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertTrue( expected_error in faults )

    ## Wikipedia: Areas with only double-digit districts: AB, LL, SO. Tests that standard postcode 
    #  observes this rules.
    def test__StandardPostcode_Validate__double_digit_districts(self):

        from wintersdeep_postcode.exceptions.validation_error import ValidationError

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "AB", "LL", "SO" ]

        expected_error = StandardPostcode.ExpectedDoubleDigitDistrict
        self.assertEqual(int(expected_error), 202)

        for test in test_raises_fault:

            test_string = fr"{test}10 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertFalse(faults)

            test_string = fr"{test}9 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertTrue( expected_error in faults )

    ## Wikipedia: Areas with a zero districts: BL, BS, CM, CR, FY, HA, PR, SL, SS. Tests 
    #  that standard postcode observes this rules.
    def test__StandardPostcode_Validate__no_zero_district(self):

        from wintersdeep_postcode.exceptions.validation_error import ValidationError

        # we usually only test the failure route as the "good" route are to be 
        # covered in another test and should cover this scenario. Due to the 
        # inversion of the logic on this test, we'll also hand pick a few goods.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_not_raises_fault = [ "BL", "BS", "CM", "CR", "FY", "HA", "PR", "SL", "SS" ]
        test_raises_fault = [ "BR", "WC", "SM", "SR" ]

        test_error = StandardPostcode.NoZeroDistrict
        self.assertEqual(int(test_error), 203)

        for test in test_not_raises_fault:

            test_string = fr"{test}0 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertFalse(faults)

        for test in test_raises_fault:

            test_string = fr"{test}0 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertTrue( test_error in faults )

    ## Wikipedia: Areas without a 10 districts: BL, CM, CR, FY, HA, PR, SL, SS. Tests 
    #  that standard postcode observes this rules.
    def test__StandardPostcode_Validate__no_ten_district(self):

        from wintersdeep_postcode.exceptions.validation_error import ValidationError

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "BL", "CM", "CR", "FY", "HA", "PR", "SL", "SS" ]
        
        test_error = StandardPostcode.NoTenDistrict
        self.assertEqual(int(test_error), 204)

        for test in test_raises_fault:

            test_string = fr"{test}10 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            faults = StandardPostcode.Validate(postcode)
            self.assertTrue( test_error in faults, test)


if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ## 

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()