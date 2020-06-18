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
class TestSpecialCasePostcode(TestCase):
    
    ## Sets up the a special case we can use for testing various aspects of the parser.
    @classmethod
    def setUpClass(cls):
        cls.SpecialCaseLabel = "specialcase_unittest"
        cls.SpecialCase = SpecialCase.FromJsonString("""
            {{
                "identifier": "{label}",
                "patterns": [
                    [ "SCP", "XX(?:[0-9])" ],
                    [ "LHS", "RHS"],
                    [ "EXAMPLE" ],
                    [ "DOES", "NOT", "EXIST" ]
                ],
                "examples": [ "SCP XX0", "SCP XX8", "LHS RHS", "EXAMPLE", "DOES NOT EXIST" ]
            }}
        """.format(label=cls.SpecialCaseLabel))
        cls.NormalRegex = SpecialCasePostcode.GetParseRegex(r"\ ")

    ## tests that the function responsible for creating the parser regex, respects the
    #  whitespace delimiter that is passed to it.
    def test__SpecialCasePostcode_GetParseRegex__delimiter(self):

        from re import error

        test_A_delimiter = SpecialCasePostcode.GetParseRegex("A")
        self.assertIsNotNone ( test_A_delimiter.match("LHSARHS") )
        self.assertIsNone    ( test_A_delimiter.match("LHS RHS") )
        self.assertIsNone    ( test_A_delimiter.match("WHATEVR") )
        self.assertRaises(error, SpecialCasePostcode.GetParseRegex, '[')

    ## test that we can get the correct definition back from the special case postcode
    #  parser regex output.
    def test__SpecialCasePostcode_GetDefinitionFromRegex(self):
        for identifier, special_case in SpecialCase.Map.items():
            for example in special_case.examples:
                regex_match = self.NormalRegex.match(example)
                special_case_out = SpecialCasePostcode.GetDefinitionFromRegex(regex_match)
                self.assertEqual(special_case.identifier, identifier)
                self.assertIs(special_case_out, special_case)

        #
        # there isn't really a negative path for this function - as in normal use
        # it should never occur - this method is expected to be called from the 
        # constuctor - as such its has three failure modes - none of which should occur
        #   > being passed the wrong type
        #   > being passed None as the result of the match failing.
        #   > being passed a regex match from a different regex.
        #

    ## test that the method used for extracting postcode parts from the regex match
    #  work as expected. this is a bit more fragile as bad patterns from special
    #  cases might polute the results, and make everything fail - to help address
    #  this we'll add a "examples" field to the definition object.
    def test__SpecialCasePostcode_GetPostcodePartsFromRegex(self):

        for identifier, special_case in SpecialCase.Map.items():
            for example in special_case.examples:
                regex_match = self.NormalRegex.match(example)
                postcode_parts = SpecialCasePostcode.GetPostcodePartsFromRegex(identifier, regex_match)
                self.assertIsInstance(postcode_parts, list)
                self.assertGreater(len(postcode_parts), 0)

        exact_parse = [
            ("SCP XX0", ["SCP", "XX0"]),
            ("SCP XX9", ["SCP", "XX9"]),
            ("LHS RHS", ["LHS", "RHS"]),
            ("EXAMPLE", ["EXAMPLE"]),
            ("DOES NOT EXIST", ["DOES", "NOT", "EXIST"]),
        ]

        for test_pattern, expected_parts in exact_parse:
            regex_match = self.NormalRegex.match(test_pattern)
            postcode_parts = SpecialCasePostcode.GetPostcodePartsFromRegex(self.SpecialCaseLabel, regex_match)
            self.assertSequenceEqual(expected_parts, postcode_parts)

        #
        # there isn't really a negative path for this function - as in normal use
        # it should never occur - this method is expected to be called from the 
        # constuctor - as such its has three failure modes - none of which should occur
        #   > being passed the wrong type
        #   > being passed None as the result of the match failing.
        #   > being passed a regex match from a different regex.
        #

    ## test that we get the properties we expect from a postcode
    def test__SpecialCasePostcode_ctor(self):
        
        exact_parse = [
            ("SCP XX0", "SCP", "XX0"),
            ("SCP XX9", "SCP", "XX9"),
            ("LHS RHS", "LHS", "RHS"),
            ("EXAMPLE", "EXAMPLE", ""),
            ("DOES NOT EXIST", "DOES", "EXIST"),
        ]

        for postcode, outward_code, inward_code in exact_parse:
            regex_match = self.NormalRegex.match(postcode)
            postcode_obj = SpecialCasePostcode(regex_match)
            self.assertSequenceEqual(str(postcode_obj), postcode)
            self.assertSequenceEqual(postcode_obj.inward_code, inward_code)
            self.assertSequenceEqual(postcode_obj.outward_code, outward_code)

        for identifier, special_case in SpecialCase.Map.items():
            for example in special_case.examples:
                regex_match = self.NormalRegex.match(postcode)
                postcode_obj = SpecialCasePostcode(regex_match)
                self.assertEqual(str(postcode_obj), postcode)


if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()    
    
