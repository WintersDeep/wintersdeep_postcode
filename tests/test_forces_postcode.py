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
from wintersdeep_postcode.postcode_types.forces_postcode.forces_postcode import ForcesPostcode

## Unit Test class for the ForcesPostcode class
class TestForcesPostcode(TestCase):

    ## Sets up static memebers that are reused over tests.
    #  @param cls the class that is invoking this method.
    @classmethod
    def setUpClass(cls):
        cls.NormalRegex = ForcesPostcode.GetParseRegex(r"\ ")

    ## Creates a forces postcode from an string.
    #  @param cls the class that is invoking this method.
    #  @param postcode_string the postcode string to convert.
    #  @returns the forces postcode object
    def createForcesPostcode(cls, postcode_string):
        regex_match = cls.NormalRegex.match(postcode_string)
        result_postcode = ForcesPostcode(regex_match)
        return result_postcode

    ## tests that the function responsible for creating the parser regex, respects the
    #  whitespace delimiter that is passed to it.
    def test__ForcesPostcode_GetParseRegex__delimiter(self):

        from re import error

        test_A_delimiter = ForcesPostcode.GetParseRegex("A")
        self.assertIsNotNone ( test_A_delimiter.match("BFPOA1234") )
        self.assertIsNotNone ( test_A_delimiter.match("BF11A2XX") )
        self.assertIsNone    ( test_A_delimiter.match("BFPO 1234") )
        self.assertIsNone    ( test_A_delimiter.match("BF1 2XX") )
        self.assertIsNone    ( test_A_delimiter.match("WHATEVR") )
        self.assertRaises(error, ForcesPostcode.GetParseRegex, '[')

    ## tests that, at a glance, the regular expression being returned by the factory
    #  appears to able to successfully parse good values.
    def test__ForcesPostcode_GetParseRegex__regex(self):
        
        test_regex = ForcesPostcode.GetParseRegex(r"\ ")

        test_list = [
            "BFPO 1",
            "BFPO 12",
            "BFPO 123",
            "BFPO 1234",
            "BF1 1AA",
            "BF11 1AA" # techincally not in use but still captured for future and validation.
        ]

        for test_string in test_list:
            self.assertIsNotNone( test_regex.match(test_string) )

    ## tests that the BFPO postcode object allocates local members as expected.
    def test__ForcesPostcode_ctor(self):

        test_list = [
            (r"BFPO 1",     1,      True,  None, None, None, None),
            (r"BFPO 12",    12,     True,  None, None, None, None),
            (r"BFPO 123",   123,    True,  None, None, None, None),
            (r"BFPO 1234",  1234,   True,  None, None, None, None),
            (r"BF1 2XX",    None,   False, "BF", 1,    2,    "XX"),
            (r"BF12 3XX",   None,   False, "BF", 12,   3,    "XX"),

        ]
        
        for postcode, bfpo, is_bfpo, area, district, sector, unit in test_list:
            test_postcode = self.createForcesPostcode(postcode)
            self.assertEqual(test_postcode.bfpo, bfpo)
            self.assertEqual(test_postcode.outward_district, district)
            self.assertEqual(test_postcode.is_bfpo_format, is_bfpo)
            self.assertEqual(test_postcode.outward_area, area)
            self.assertEqual(test_postcode.outward_district, district)
            self.assertEqual(test_postcode.inward_sector, sector)
            self.assertEqual(test_postcode.inward_unit, unit)
            self.assertEqual(test_postcode.postcode_type, "forces")
            self.assertFalse(test_postcode.is_validated)

    ## Test that the BFPO postcodes outward code property words as expected.
    def test__ForcesPostcode_outward_code(self):

        test_list = [
            ("BFPO 1", "BFPO"),
            ("BFPO 12", "BFPO"),
            ("BFPO 123", "BFPO"),
            ("BFPO 1234", "BFPO"),
            ("BF1 1AA", "BF1"),
            ("BF11 1AA", "BF11")
        ]

        for postcode, outward_code in test_list:
            postcode = self.createForcesPostcode(postcode)
            self.assertEqual(postcode.outward_code, outward_code)

    ## Test that the BFPO postcodes inward code property words as expected.
    def test__ForcesPostcode_inward_code(self):

        test_list = [
            ("BFPO 1", "1"),
            ("BFPO 12", "12"),
            ("BFPO 123", "123"),
            ("BFPO 1234", "1234"),
            ("BF1 1AA", "1AA"),
            ("BF11 1AA", "1AA")
        ]

        for postcode, inward_code in test_list:
            postcode = self.createForcesPostcode(postcode)
            self.assertEqual(postcode.inward_code, inward_code)

    ## Tests the the BFPO postcode object __str__ method works as expected.
    def test__ForcesPostcode_str(self):

        test_list = [
            "BFPO 1", "BFPO 12", "BFPO 123", "BFPO 1234", "BF1 1AA", "BF11 1AA"  
        ]

        for test_string in test_list:
            postcode = self.createForcesPostcode(test_string)
            self.assertEqual( str(postcode), test_string)

    ## Tests that fault numbers haven't changed as this would constitute 
    #  breaking changes.
    def test__ForcesPostcode__fault_numbers(self):

        test_list = [
            ( ForcesPostcode.InvalidDistrict, 401 ),
        ]

        for error_object, expected_id in test_list:
            self.assertEqual(int(error_object), expected_id)

    ## Checks that the method we use to bind tests and faults is working
    def test__ForcesPostcode_Validate__fault_assignment(self):
    
        test_list = [
            ("BF3 2XX", ForcesPostcode.InvalidDistrict)
        ]

        for test_string, expected_fault in test_list:       
            postcode = self.createForcesPostcode(test_string)
            faults = ForcesPostcode.Validate(postcode)
            self.assertTrue(expected_fault in faults)




if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ## 

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()