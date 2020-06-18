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
from wintersdeep_postcode.postcode_types.special_case_postcode.special_case_postcode import SpecialCasePostcode
from wintersdeep_postcode.postcode_types.special_case_postcode.special_case import SpecialCase

## Unit Test class for SpecialCase
class TestSpecialCase(TestCase):
    
    ## test that the default special cases map is being loading and appears to contain
    #  some expected items.
    def test__SpecialCase_Map__Loaded(self):
        self.assertGreater( len(SpecialCase.Map.items()), 0)
        self.assertIn( "santa", SpecialCase.Map )
        self.assertIn( "giro", SpecialCase.Map )

        for identifier, special_case in SpecialCase.Map.items():
            self.assertEqual(identifier, special_case.identifier)

    ## tests that we can load a special case from a JSON string - ensures the JSON loader
    #  is working in a predictable manner. Changes required to make this test pass should
    #  be considered potentially breaking.
    def test__SpecialCase_FromJsonString(self):
        
        SpecialCase.FromJsonString("""
            {
                "identifier": "unittest1",
                "patterns": [
                    [ "PAT", "RN(?:[0-9])" ],
                    [ "UN1", "TST"],
                    [ "SINGLE" ],
                    "STRING",
                    [ "THREE", "PARTS", "HERE" ]
                ],
                "examples": [ "PAT RN0", "PAT RN8", "SINGLE", "THREE PARTS HERE" ]
            }
        """)

        test_patterns = [  
            ("PAT RN0", "PAT", "RN0"),
            ("PAT RN1", "PAT", "RN1"),
            ("PAT RN5", "PAT", "RN5"),
            ("UN1 TST", "UN1", "TST"),
            ("SINGLE", "SINGLE", ""),
            ("STRING", "STRING", ""),
            ("THREE PARTS HERE", "THREE", "HERE") 
        ]

        regex_tester = SpecialCasePostcode.GetParseRegex(r"\ ")
        
        for pattern, outward, inward in test_patterns:
            pattern_match = regex_tester.match(pattern)
            postcode = SpecialCasePostcode(pattern_match)
            self.assertEqual(pattern, str(postcode))
            self.assertEqual(inward, postcode.inward_code)
            self.assertEqual(outward, postcode.outward_code)

    ## Tests the process of adding a special case identification regex using a string 
    #  pattern. This is not as reliable as the list approach as it relies on the 
    #  special case to split the pattern - and this might not be done properly.
    def test__SpecialCase_add_pattern__string(self):
        
        special_case = SpecialCase("unittest2")

        special_case.add_pattern("THIS")
        self.assertEqual(len(special_case.patterns), 1)
        self.assertIs(special_case.patterns[0].__class__, list)
        self.assertEqual(len(special_case.patterns[0]), 1)
        self.assertEqual(special_case.patterns[0][0], "THIS")
        
        special_case.add_pattern("THIS THAT")
        self.assertEqual(len(special_case.patterns), 2)
        self.assertIs(special_case.patterns[1].__class__, list)
        self.assertEqual(len(special_case.patterns[1]), 2)
        self.assertEqual(special_case.patterns[1][0], "THIS")
        self.assertEqual(special_case.patterns[1][1], "THAT")

        special_case.add_pattern("LARGE       SPACE")
        self.assertEqual(len(special_case.patterns), 3)
        self.assertIs(special_case.patterns[1].__class__, list)
        self.assertEqual(len(special_case.patterns[2]), 2)
        self.assertEqual(special_case.patterns[2][0], "LARGE")
        self.assertEqual(special_case.patterns[2][1], "SPACE")

        special_case.add_pattern(" ")
        self.assertEqual(len(special_case.patterns), 3)

    ## Tests the process of adding a special case identification regex using a list 
    #  pattern. This is the recommended syntax for adding patterns for special cases.
    def test__SpecialCase_add_pattern__list(self):
        
        special_case = SpecialCase("unittest3")

        special_case.add_pattern(["THIS"])
        self.assertEqual(len(special_case.patterns), 1)
        self.assertIs(special_case.patterns[0].__class__, list)
        self.assertEqual(len(special_case.patterns[0]), 1)
        self.assertEqual(special_case.patterns[0][0], "THIS")
        
        special_case.add_pattern(["THIS", "THAT"])
        self.assertEqual(len(special_case.patterns), 2)
        self.assertIs(special_case.patterns[1].__class__, list)
        self.assertEqual(len(special_case.patterns[1]), 2)
        self.assertEqual(special_case.patterns[1][0], "THIS")
        self.assertEqual(special_case.patterns[1][1], "THAT")

        special_case.add_pattern(["LARGE", "", " ", "SPACE"])
        self.assertEqual(len(special_case.patterns), 3)
        self.assertIs(special_case.patterns[1].__class__, list)
        self.assertEqual(len(special_case.patterns[2]), 2)
        self.assertEqual(special_case.patterns[2][0], "LARGE")
        self.assertEqual(special_case.patterns[2][1], "SPACE")

        special_case.add_pattern([])
        self.assertEqual(len(special_case.patterns), 3)

    ## Tests that we cannot create special case objects that have duplicate identifiers.
    #  this would cause issues with pattern creation, and definition identification.
    def test__SpecialCase_ctor__duplicate_id(self):
        special_case = SpecialCase("unittest4")
        self.assertRaises(ValueError, SpecialCase, "unittest4")
        

if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()