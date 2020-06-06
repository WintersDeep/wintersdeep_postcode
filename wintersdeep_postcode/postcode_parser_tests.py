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
from wintersdeep_postcode.postcode_parser import PostcodeParser

## Unit Test class for PostcodeParser
class TestPostcodeParser(TestCase):

    ## tests that the PostcodeParser::_get_whitespace_pattern raises an exception when 
    #  unrecognised type strings are provided to the method.
    def test_get_whitespace_pattern__unsupported(self):
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 'unsupported')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 'TOLERANT')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 'tolerant ')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, '')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, False)
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, None)
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 1)

    ## tests that the PostcodeParser::_get_whitespace_pattern creates a suitable pattern
    #  when created with the 'strict' keyword.
    def test_get_whitespace_pattern__strict(self):

        whitespace_pattern = PostcodeParser._get_whitespace_pattern('strict')
        test_regex = compile(f"^{whitespace_pattern}$")

        self.assertTrue( test_regex.match(" ") )
        self.assertFalse( test_regex.match("") )
        self.assertFalse( test_regex.match("  ") )
        self.assertFalse( test_regex.match("\t") )
        self.assertFalse( test_regex.match("\t ") )
        self.assertFalse( test_regex.match(" \t ") )
        self.assertFalse( test_regex.match("-") )
        self.assertFalse( test_regex.match("TEXT") )

    ## tests that the PostcodeParser::_get_whitespace_pattern creates a suitable pattern
    #  when created with the 'tolerant' keyword.
    def test_get_whitespace_pattern__tolerant(self):

        whitespace_pattern = PostcodeParser._get_whitespace_pattern('tolerant')
        test_regex = compile(f"^{whitespace_pattern}$")

        self.assertTrue( test_regex.match(" ") )
        self.assertTrue( test_regex.match("") )
        self.assertFalse( test_regex.match("  ") )
        self.assertFalse( test_regex.match("\t") )
        self.assertFalse( test_regex.match("\t ") )
        self.assertFalse( test_regex.match(" \t ") )
        self.assertFalse( test_regex.match("-") )
        self.assertFalse( test_regex.match("TEXT") )

    ## tests that the PostcodeParser::_get_whitespace_pattern creates a suitable pattern
    #  when created with the 'lenient' keyword.
    def test_get_whitespace_pattern__lenient(self):

        whitespace_pattern = PostcodeParser._get_whitespace_pattern('lenient')
        test_regex = compile(f"^{whitespace_pattern}$")

        self.assertTrue( test_regex.match(" ") )
        self.assertTrue( test_regex.match("") )
        self.assertTrue( test_regex.match("  ") )
        self.assertTrue( test_regex.match("\t") )
        self.assertTrue( test_regex.match("\t ") )
        self.assertTrue( test_regex.match(" \t ") )
        self.assertFalse( test_regex.match("-") )
        self.assertFalse( test_regex.match("TEXT") )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - no operation pipeline
    def test_build_input_translator__nop(self):

        pipeline = PostcodeParser._build_input_translater(trim=False, uppercase=False)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), " TRIM TEST\t " )
        self.assertEqual( pipeline("Uppercase Test"), "Uppercase Test" )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - trim only pipeline
    def test_build_input_translator__trim(self):

        pipeline = PostcodeParser._build_input_translater(trim=True, uppercase=False)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), "TRIM TEST" )
        self.assertEqual( pipeline("Uppercase Test"), "Uppercase Test" )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - uppercase only pipeline
    def test_build_input_translator__uppercase(self):

        pipeline = PostcodeParser._build_input_translater(trim=False, uppercase=True)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), " TRIM TEST\t " )
        self.assertEqual( pipeline("Uppercase Test"), "UPPERCASE TEST" )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - full pipeline
    def test_build_input_translator__full(self):

        pipeline = PostcodeParser._build_input_translater(trim=True, uppercase=True)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), "TRIM TEST" )
        self.assertEqual( pipeline("Uppercase Test"), "UPPERCASE TEST" )

    ## tests that the function responsible for creating the parser regex, produces a
    #  usable regular expression object - and behaves in a predictable way to bad input 
    def test_build_parser_regex(self):

        from re import error

        test_A_delimiter = PostcodeParser._build_parser_regex("A")
        self.assertIsNotNone ( test_A_delimiter.match("E20A2ST") )
        self.assertIsNone    ( test_A_delimiter.match("E20 2ST") )
        self.assertIsNone    ( test_A_delimiter.match("WHATEVR") )

        self.assertRaises(error, PostcodeParser._build_parser_regex, '[' )

    ## This test to make sure we throw if we try and create a parser with an unknown
    #  method of handling whitespace in a predicable manner
    def test_parse_with_bad_whitespace_handler(self):

        from wintersdeep_postcode.exceptions import ParseError
        self.assertRaises( ValueError, PostcodeParser, 
            trim_whitespace=False, 
            force_case=False, 
            whitespace='error'
        )
        

    ## This test is for the parser in its most strict configuration - strict whitepace
    #  handling, and no input translation. This is to ensure that in this mode, only 
    #  well formed postcodes are parsed. 
    def test_parse_with_no_translation(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=False, force_case=False, whitespace='strict')
        
        self.assertRaises(ParseError, postcode_parser, "aa0 0aa")
        self.assertRaises(ParseError, postcode_parser, "AA00AA")
        self.assertRaises(ParseError, postcode_parser, "AA0  0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t 0AA")
        self.assertRaises(ParseError, postcode_parser, " AA0 0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0 0AA ")
        self.assertRaises(ParseError, postcode_parser, " AA0 0AA ")
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A0 0AA") )
        self.assertIsNotNone( postcode_parser("A00 0AA") )
        self.assertIsNotNone( postcode_parser("A0A 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA00 0AA") )
        self.assertIsNotNone( postcode_parser("AA0A 0AA") )

    ## This test is for the parser in a strict configuration - strict whitepace
    #  handling, and only case correction enabled. This is to ensure that in 
    #  this mode, well formed postcodes of any case are parsed. 
    def test_parse_with_caps_correction(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=False, force_case=True, whitespace='strict')
        
        self.assertIsNotNone( postcode_parser("aa0 0aa") )
        self.assertRaises(ParseError, postcode_parser, "AA00AA")
        self.assertRaises(ParseError, postcode_parser, "AA0  0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t 0AA")
        self.assertRaises(ParseError, postcode_parser, " AA0 0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0 0AA ")
        self.assertRaises(ParseError, postcode_parser, " AA0 0AA ")
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A0 0AA") )
        self.assertIsNotNone( postcode_parser("A00 0AA") )
        self.assertIsNotNone( postcode_parser("A0A 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA00 0AA") )
        self.assertIsNotNone( postcode_parser("AA0A 0AA") )

    ## This test is for the parser in a strict configuration - strict whitepace
    #  handling, and ony whitepace trimming enabled. This is to ensure that in this 
    #  mode, well formed postcodes with whitespace padding are parsed correctly. 
    def test_parse_with_trimmed_whitespace(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=False, whitespace='strict')
        
        self.assertRaises(ParseError, postcode_parser, "aa0 0aa")
        self.assertRaises(ParseError, postcode_parser, "AA00AA")
        self.assertRaises(ParseError, postcode_parser, "AA0  0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t 0AA")
        self.assertIsNotNone( postcode_parser(" AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA ") )
        self.assertIsNotNone( postcode_parser(" AA0 0AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A0 0AA") )
        self.assertIsNotNone( postcode_parser("A00 0AA") )
        self.assertIsNotNone( postcode_parser("A0A 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA00 0AA") )
        self.assertIsNotNone( postcode_parser("AA0A 0AA") )

    ## This test is for the parser in a severe configuration - strict whitepace
    #  handling, but full pre-processing enabled. This is to ensure that in this 
    #  mode, well formed postcodes which may be slightly "dirty" are parsed. 
    def test_parse_with_full_translation(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=True, whitespace='strict')
        
        self.assertIsNotNone( postcode_parser("aa0 0aa") )
        self.assertRaises(ParseError, postcode_parser, "AA00AA")
        self.assertRaises(ParseError, postcode_parser, "AA0  0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t 0AA")
        self.assertIsNotNone( postcode_parser(" AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA ") )
        self.assertIsNotNone( postcode_parser(" AA0 0AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A0 0AA") )
        self.assertIsNotNone( postcode_parser("A00 0AA") )
        self.assertIsNotNone( postcode_parser("A0A 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA00 0AA") )
        self.assertIsNotNone( postcode_parser("AA0A 0AA") )

    ## This test is for the parser in a tolerant configuration - tolerant whitepace
    #  handling, and full pre-processing enabled. This is to ensure that in this 
    #  mode, well formed postcodes which may be slightly "dirty" are parsed. 
    def test_parse__tolerant(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=True, whitespace='tolerant')
        
        self.assertIsNotNone( postcode_parser("aa0 0aa") )
        self.assertIsNotNone( postcode_parser("AA00AA") )
        self.assertRaises(ParseError, postcode_parser, "AA0  0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t0AA")
        self.assertRaises(ParseError, postcode_parser, "AA0\t 0AA")
        self.assertIsNotNone( postcode_parser(" AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA ") )
        self.assertIsNotNone( postcode_parser(" AA0 0AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A0 0AA") )
        self.assertIsNotNone( postcode_parser("A00 0AA") )
        self.assertIsNotNone( postcode_parser("A0A 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA00 0AA") )
        self.assertIsNotNone( postcode_parser("AA0A 0AA") )

    ## This test is for the parser in a lenient configuration - lenient whitepace
    #  handling, and full pre-processing enabled. This is to ensure that in this 
    #  mode, well formed postcodes which may be slightly "dirty" are parsed. 
    def test_parse__lenient(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=True, whitespace='lenient')
        
        self.assertIsNotNone( postcode_parser("aa0 0aa") )
        self.assertIsNotNone( postcode_parser("AA00AA") )
        self.assertIsNotNone( postcode_parser("AA0  0AA") )
        self.assertIsNotNone( postcode_parser("AA0\t0AA") )
        self.assertIsNotNone( postcode_parser("AA0\t 0AA") )
        self.assertIsNotNone( postcode_parser(" AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA ") )
        self.assertIsNotNone( postcode_parser(" AA0 0AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A0 0AA") )
        self.assertIsNotNone( postcode_parser("A00 0AA") )
        self.assertIsNotNone( postcode_parser("A0A 0AA") )
        self.assertIsNotNone( postcode_parser("AA0 0AA") )
        self.assertIsNotNone( postcode_parser("AA00 0AA") )
        self.assertIsNotNone( postcode_parser("AA0A 0AA") )

        
if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()