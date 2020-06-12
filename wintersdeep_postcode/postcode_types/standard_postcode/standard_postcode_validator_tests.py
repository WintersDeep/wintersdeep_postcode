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
from wintersdeep_postcode.postcode_types.standard_postcode.standard_postcode import StandardPostcode
from wintersdeep_postcode.postcode_types.standard_postcode.standard_postcode_validator import StandardPostcodeValidator

## Unit Test class for the StandardPostcodeValidator class
class TestStandardPostcodeValidator(TestCase):

    ## Sets up class members used across several tests.
    #  @param cls the type of class that is invoking this method.
    @classmethod
    def setUpClass(cls):
        cls.PostcodeRegex = StandardPostcode.GetParseRegex(r"\ ")

    ## Creates a postcode using the standard delimiter.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode_string the postcode that is to be made into an object.
    #  @returns the postcode string as a standardpostcode object.
    @classmethod
    def createStandardPostcode(cls, postcode_string):
        regex_match = cls.PostcodeRegex.match(postcode_string)
        postcode_result = StandardPostcode(regex_match)
        return postcode_result

    ## Wikipedia: Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE
    #  LD, SM, SR, WC, WN, ZE. Tests that standard postcode observes these rules.
    def test__StandardPostcodeValidator_CheckAreasWithOnlySingleDigitDistricts(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_raises_fault = [ "BR", "FY", "HA", "HD", "HG", "HR", "HS", 
            "HX", "JE", "LD", "SM", "WC", "WN", "ZE" ]

        for test in test_raises_fault:

            postcode = self.createStandardPostcode(fr"{test}9 1AB")
            self.assertFalse(StandardPostcodeValidator.CheckAreasWithOnlySingleDigitDistricts(postcode))

            postcode = self.createStandardPostcode(fr"{test}10 1AB")
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithOnlySingleDigitDistricts(postcode))
            

    ## Wikipedia: Areas with only double-digit districts: AB, LL, SO. Tests that standard postcode 
    #  observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithOnlyDoubleDigitDistricts(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_raises_fault = [ "AB", "LL", "SO" ]

        for test in test_raises_fault:

            postcode = self.createStandardPostcode(fr"{test}10 1AB")
            self.assertFalse(StandardPostcodeValidator.CheckAreasWithOnlyDoubleDigitDistricts(postcode))

            postcode = self.createStandardPostcode(fr"{test}9 1AB")
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithOnlyDoubleDigitDistricts(postcode))

    ## Wikipedia: Areas with a zero districts: BL, BS, CM, CR, FY, HA, PR, SL, SS. Tests 
    #  that standard postcode observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithDistrictZero(self):

        # we usually only test the failure route as the "good" route are to be 
        # covered in another test and should cover this scenario. Due to the 
        # inversion of the logic on this test, we'll also hand pick a few goods.

        test_not_raises_fault = [ "BL", "BS", "CM", "CR", "FY", "HA", "PR", "SL", "SS" ]
        test_raises_fault = [ "BR", "WC", "SM", "SR" ]

        for test in test_not_raises_fault:

            postcode = self.createStandardPostcode(fr"{test}0 1AB")
            self.assertFalse(StandardPostcodeValidator.CheckAreasWithDistrictZero(postcode))

        for test in test_raises_fault:

            postcode = self.createStandardPostcode(fr"{test}0 1AB")
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithDistrictZero(postcode))
            

    ## Wikipedia: Areas without a 10 districts: BL, CM, CR, FY, HA, PR, SL, SS. Tests 
    #  that standard postcode observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithoutDistrictTen(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_raises_fault = [ "BL", "CM", "CR", "FY", "HA", "PR", "SL", "SS" ]
        
        for test in test_raises_fault:

            postcode = self.createStandardPostcode(fr"{test}10 1AB")
            self.assertTrue(StandardPostcodeValidator.CheckAreasWithoutDistrictTen(postcode))
            
    ## Wikipedia: Areas with subdivided districts: EC1-4, SW1, W1, WC1, WC2, E1, 
    #  N1, NW, and SE. Tests that standard postcode observes this rules.
    def test__StandardPostcodeValidator_CheckAreasWithSubdistricts(self):

        # we are only going to test the failure route in this test, as good postcodes are to be 
        # covered in another test and should cover this scenario.

        test_raises_fault = [ "A", "B", "C", "FY", "HA", "PR", "SL", "SS", "WC" ]
        
        for test in test_raises_fault:

            postcode = self.createStandardPostcode(fr"{test}5A 1AB")
            self.assertTrue( StandardPostcodeValidator.CheckAreasWithSubdistricts(postcode) )

        postcode = self.createStandardPostcode(r"WC1A 1AB")
        self.assertFalse( StandardPostcodeValidator.CheckAreasWithSubdistricts(postcode) )

    ## Tests that where we know about specific subdistricts the parser will only allow
    #  elements from the selection.
    def test__StandardPostcodeValidator_CheckAreasWithSpecificSubdistricts(self):
        
        postcode = self.createStandardPostcode(r"N1C 9XX")
        self.assertFalse( StandardPostcodeValidator.CheckAreasWithSpecificSubdistricts(postcode) )

        postcode = self.createStandardPostcode(r"N1P 9XX")
        self.assertFalse( StandardPostcodeValidator.CheckAreasWithSpecificSubdistricts(postcode) )
        
        postcode = self.createStandardPostcode(r"N1R 9XX")
        self.assertTrue( StandardPostcodeValidator.CheckAreasWithSpecificSubdistricts(postcode) )

    ## Tests the validator that checks for unsed characters in the first postition.
    def test__StandardPostcodeValidator_CheckFirstPositionExcludes(self):
        
        bad_first_characters = [ "Q", "V", "X" ]
        
        for character in bad_first_characters:
            postcode = self.createStandardPostcode(fr"{character}1 9XX")
            self.assertTrue(StandardPostcodeValidator.CheckFirstPositionExcludes(postcode))

        postcode = self.createStandardPostcode(r"W1 9XX")
        self.assertFalse(StandardPostcodeValidator.CheckFirstPositionExcludes(postcode))
        
    ## Tests the validator that checks for unsed characters in the second postition.
    def test__StandardPostcodeValidator_CheckSecondPositionExcludes(self):
        
        bad_second_characters = [ "I", "J", "Z" ]
        
        for character in bad_second_characters:
            postcode = self.createStandardPostcode(fr"A{character}1 9XX")
            self.assertTrue(StandardPostcodeValidator.CheckSecondPositionExcludes(postcode), character)

        postcode = self.createStandardPostcode(r"WL1 9XX")
        self.assertFalse(StandardPostcodeValidator.CheckSecondPositionExcludes(postcode))
        
    ## Tests the validator that checks for unsed characters in the second postition.
    def test__StandardPostcodeValidator_CheckSingleDigitAreaSubdistricts(self):
        
        test_list = [
            (False, "ABCDEFGHJKPSTUW"),
            (True, "ILMNOQRVXYZ")
        ]
        
        for expected_result, character_list in test_list:
            for character in character_list:
                postcode = self.createStandardPostcode(fr"A1{character} 9XX")
                check = StandardPostcodeValidator.CheckSingleDigitAreaSubdistricts(postcode)
                self.assertEqual(expected_result, check)
        
    ## Tests the validator that checks for unsed characters in the fourth postition.
    def test__StandardPostcodeValidator_CheckDoubleDigitAreaSubdistricts(self):
        test_list = [
            (False, "ABEHMNPRVWXY"),
            (True, "CDFGIJKLOQSTUZ")
        ]
        
        for expected_result, character_list in test_list:
            for character in character_list:
                postcode = self.createStandardPostcode(fr"AA1{character} 9XX")
                check = StandardPostcodeValidator.CheckDoubleDigitAreaSubdistricts(postcode)
                self.assertEqual(expected_result, check, postcode)
        
    ## Tests the validator that checks for unsed characters in the fourth postition.
    def test__StandardPostcodeValidator_CheckFirstUnitCharacterExcludes(self):
        
        test_list = [
            (False, "ABDEFGHJLNPQRSTUWXYZ"),
            (True, "CIKMOV")
        ]
        
        for expected_result, character_list in test_list:
            for character in character_list:
                postcode = self.createStandardPostcode(fr"AA1 9{character}X")
                check = StandardPostcodeValidator.CheckFirstUnitCharacterExcludes(postcode)
                self.assertEqual(expected_result, check, postcode)
        
    ## Tests the validator that checks for unsed characters in the fourth postition.
    def test__StandardPostcodeValidator_CheckSecondUnitCharacterExcludes(self):
        
        test_list = [
            (False, "ABDEFGHJLNPQRSTUWXYZ"),
            (True, "CIKMOV")
        ]
        
        for expected_result, character_list in test_list:
            for character in character_list:
                postcode = self.createStandardPostcode(fr"AA1 9X{character}")
                check = StandardPostcodeValidator.CheckSecondUnitCharacterExcludes(postcode)
                self.assertEqual(expected_result, check, postcode)
        
    

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ## 

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()