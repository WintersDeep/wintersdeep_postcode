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
from wintersdeep_postcode.postcode_types.standard_postcode_validator import StandardPostcodeValidator

## Unit Test class for the StandardPostcodeValidator class
class TestStandardPostcodeValidator(TestCase):

    ## Wikipedia: Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE
    #  LD, SM, SR, WC, WN, ZE. Tests that standard postcode observes these rules.
    def test__StandardPostcodeValidator_CheckAreasWithOnlySingleDigitDistricts(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "BR", "FY", "HA", "HD", "HG", "HR", "HS", 
            "HX", "JE", "LD", "SM", "SR", "WC", "WN", "ZE" ]

        for test in test_raises_fault:

            test_string = fr"{test}9 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertFalse(StandardPostcodeValidator.CheckAreasWithOnlySingleDigitDistricts(postcode))

            test_string = fr"{test}10 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithOnlySingleDigitDistricts(postcode))
            

    ## Wikipedia: Areas with only double-digit districts: AB, LL, SO. Tests that standard postcode 
    #  observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithOnlyDoubleDigitDistricts(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "AB", "LL", "SO" ]

        for test in test_raises_fault:

            test_string = fr"{test}10 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertFalse(StandardPostcodeValidator.CheckAreasWithOnlyDoubleDigitDistricts(postcode))

            test_string = fr"{test}9 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithOnlyDoubleDigitDistricts(postcode))

    ## Wikipedia: Areas with a zero districts: BL, BS, CM, CR, FY, HA, PR, SL, SS. Tests 
    #  that standard postcode observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithDistrictZero(self):

        # we usually only test the failure route as the "good" route are to be 
        # covered in another test and should cover this scenario. Due to the 
        # inversion of the logic on this test, we'll also hand pick a few goods.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_not_raises_fault = [ "BL", "BS", "CM", "CR", "FY", "HA", "PR", "SL", "SS" ]
        test_raises_fault = [ "BR", "WC", "SM", "SR" ]

        for test in test_not_raises_fault:

            test_string = fr"{test}0 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertFalse(StandardPostcodeValidator.CheckAreasWithDistrictZero(postcode))

        for test in test_raises_fault:

            test_string = fr"{test}0 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithDistrictZero(postcode))
            

    ## Wikipedia: Areas without a 10 districts: BL, CM, CR, FY, HA, PR, SL, SS. Tests 
    #  that standard postcode observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithoutDistrictTen(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "BL", "CM", "CR", "FY", "HA", "PR", "SL", "SS" ]
        
        for test in test_raises_fault:

            test_string = fr"{test}10 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithoutDistrictTen(postcode))
            
    ## Wikipedia: Areas with subdivided districts: EC1-4, SW1, W1, WC1, WC2, E1, 
    #  N1, NW, and SE. Tests that standard postcode observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithSubdistricts(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_regex = StandardPostcode.GetParseRegex(r"\ ")    
        test_raises_fault = [ "A", "B", "C", "FY", "HA", "PR", "SL", "SS", "WC" ]
        
        for test in test_raises_fault:

            test_string = fr"{test}5A 1AB"
            regex_match = test_regex.match(test_string)
            postcode = StandardPostcode(regex_match)
            self.assertTrue( StandardPostcodeValidator.CheckAreasWithSubdistricts(postcode) )

        test_string = fr"WC1A 1AB"
        regex_match = test_regex.match(test_string)
        postcode = StandardPostcode(regex_match)
        self.assertFalse( StandardPostcodeValidator.CheckAreasWithSubdistricts(postcode) )

    ## Tests that where we know about specific subdistricts the parser will only allow
    #  elements from the selection.
    def test__StandardPostcodeValidator_CheckAreasWithSpecificSubdistricts(self):
        test_regex = StandardPostcode.GetParseRegex(r"\ ")    

        regex_match = test_regex.match("N1C 9XX")
        postcode = StandardPostcode(regex_match)
        self.assertFalse( StandardPostcodeValidator.CheckAreasWithSpecificSubdistricts(postcode) )

        regex_match = test_regex.match("N1P 9XX")
        postcode = StandardPostcode(regex_match)
        self.assertFalse( StandardPostcodeValidator.CheckAreasWithSpecificSubdistricts(postcode) )
        
        regex_match = test_regex.match("N1R 9XX")
        postcode = StandardPostcode(regex_match)
        self.assertTrue( StandardPostcodeValidator.CheckAreasWithSpecificSubdistricts(postcode) )


if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ## 

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()