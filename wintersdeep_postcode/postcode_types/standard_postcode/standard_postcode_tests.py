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

## Unit Test class for the StandardPostcode class
class TestStandardPostcode(TestCase):

    ## Sets up static memebers that are reused over tests.
    #  @param cls the class that is invoking this method.
    @classmethod
    def setUpClass(cls):
        cls.NormalRegex = StandardPostcode.GetParseRegex(r"\ ")

    ## Creates a standard postcode from an string.
    #  @param cls the class that is invoking this method.
    #  @param postcode_string the postcode string to convert.
    def createStandardPostcode(cls, postcode_string):
        regex_match = cls.NormalRegex.match(postcode_string)
        result_postcode = StandardPostcode(regex_match)
        return result_postcode

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

        test_list = [
            "A1 1AA",
            "A11 1AA",
            "A1A 1AA",
            "AA1 1AA",
            "AA11 1AA",
            "AA1A 1AA"
        ]

        for test_string in test_list:
            self.assertIsNotNone( test_regex.match(test_string) )

    ## tests that the standard postcode object allocates local members as expected.
    def test__StandardPostcode_ctor(self):

        test_list = [
            (r"A1 2BC",     "A",    1,  "",     2, "BC"),
            (r"A12 3BC",    "A",    12, "",     3, "BC"),
            (r"A1B 2CD",    "A",    1,  "B",    2, "CD"),
            (r"AB1 2CD",    "AB",   1,  "",     2, "CD"),
            (r"AB12 3CD",   "AB",   12, "",     3, "CD"),
            (r"AB1C 2DE",   "AB",   1,  "C",    2, "DE")
        ]
        
        for postcode, area, district, subdistrict, sector, unit in test_list:
            test_postcode = self.createStandardPostcode(postcode)
            self.assertEqual(test_postcode.outward_area, area)
            self.assertEqual(test_postcode.outward_district, district)
            self.assertEqual(test_postcode.outward_subdistrict, subdistrict)
            self.assertEqual(test_postcode.inward_sector, sector)
            self.assertEqual(test_postcode.inward_unit, unit)
            self.assertEqual(test_postcode.postcode_type, "standard")
            self.assertFalse(test_postcode.is_validated)

    ## Test that the standard postcodes outward code property words as expected.
    def test__StandardPostcode_outward_code(self):

        test_list = [
            ("AB1C 2DE", "AB1C"),
            ("AB12 3CD", "AB12"),
            ("AB1 2CD", "AB1"),
            ("A1B 2CD", "A1B"),
            ("A12 3BC", "A12"),
            ("A1 2BC", "A1")
        ]

        for postcode, outward_code in test_list:
            postcode = self.createStandardPostcode(postcode)
            self.assertEqual(postcode.outward_code, outward_code)

    ## Test that the standard postcodes inward code property words as expected.
    def test__StandardPostcode_inward_code(self):

        test_list = [
            ("AB1C 2DE", "2DE"),
            ("AB12 3CD", "3CD"),
            ("AB1 2CD", "2CD"),
            ("A1B 2CD", "2CD"),
            ("A12 3BC", "3BC"),
            ("A1 2BC", "2BC")
        ]

        for postcode, inward_code in test_list:
            postcode = self.createStandardPostcode(postcode)
            self.assertEqual(postcode.inward_code, inward_code)

    ## Tests the the standard postcode object __str__ method works as expected.
    def test__StandardPostcode_str(self):

        test_candidates = [ 
            "AB1C 2DE", "AB12 3CD", "AB1 2CD", "A1B 2CD", "A12 3CD", "A1 2BC"
        ]

        for test_string in test_candidates:
            postcode = self.createStandardPostcode(test_string)
            self.assertEqual( str(postcode), test_string)

    ## Tests that fault numbers haven't changed as this would constitute 
    #  breaking changes.
    def test__StandardPostcode__fault_numbers(self):

        test_list = [
            ( StandardPostcode.ExpectedSingleDigitDistrict, 201 ),
            ( StandardPostcode.ExpectedDoubleDigitDistrict, 202 ),
            ( StandardPostcode.NoZeroDistrict, 203 ),
            ( StandardPostcode.NoTenDistrict, 204 ),
            ( StandardPostcode.SubdistrictsUnsupported, 205 ),
            ( StandardPostcode.UnexpectedDistrictSubdivision, 206 ),
            ( StandardPostcode.UnusedCharacterInFirstPosition, 207 ),
            ( StandardPostcode.UnusedCharacterInSecondPosition, 208 ),
            ( StandardPostcode.UnusedSingleDigitAreaSubdistrict, 209 ),
            ( StandardPostcode.UnusedDoubleDigitAreaSubdistrict, 210 ),
            ( StandardPostcode.UnusedFirstCharacterInUnit, 211 ),
            ( StandardPostcode.UnusedSecondCharacterInUnit, 212 ),
        ]

        for error_object, expected_id in test_list:
            self.assertEqual(int(error_object), expected_id)

    ## Checks that the method we use to bind tests and faults is working
    def test__StandardPostcode_Validate__fault_assignment(self):
    
        test_list = [
            ("BR10 2XX", StandardPostcode.ExpectedSingleDigitDistrict),
            ("LL9 2XX", StandardPostcode.ExpectedDoubleDigitDistrict),
            ("LL0 2XX", StandardPostcode.NoZeroDistrict),
            ("BL10 2XX", StandardPostcode.NoTenDistrict),       
            ("XY7N 2XX", StandardPostcode.SubdistrictsUnsupported),         
            ("N1S 2XX", StandardPostcode.UnexpectedDistrictSubdivision),        
            ("X1 2XX", StandardPostcode.UnusedCharacterInFirstPosition),
            ("XI1 2XX", StandardPostcode.UnusedCharacterInSecondPosition),
            ("A1X 2XX", StandardPostcode.UnusedSingleDigitAreaSubdistrict),
            ("AA1Z 2XX", StandardPostcode.UnusedDoubleDigitAreaSubdistrict),
            ("AA1Z 2CX", StandardPostcode.UnusedFirstCharacterInUnit),
            ("AA1Z 2XC", StandardPostcode.UnusedSecondCharacterInUnit),
        ]

        for test_string, expected_fault in test_list:       
            postcode = self.createStandardPostcode(test_string)
            faults = StandardPostcode.Validate(postcode)
            self.assertTrue(expected_fault in faults)




if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ## 

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()