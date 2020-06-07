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
    def test__PostcodeParser_get_whitespace_pattern__unsupported(self):
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 'unsupported')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 'TOLERANT')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 'tolerant ')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, '')
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, False)
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, None)
        self.assertRaises(ValueError, PostcodeParser._get_whitespace_pattern, 1)

    ## tests that the PostcodeParser::_get_whitespace_pattern creates a suitable pattern
    #  when created with the 'strict' keyword.
    def test__PostcodeParser_get_whitespace_pattern__strict(self):

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
    def test__PostcodeParser_get_whitespace_pattern__tolerant(self):

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
    def test__PostcodeParser_get_whitespace_pattern__lenient(self):

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
    def test__PostcodeParser_build_input_translator__nop(self):

        pipeline = PostcodeParser._build_input_translater(trim=False, uppercase=False)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), " TRIM TEST\t " )
        self.assertEqual( pipeline("Uppercase Test"), "Uppercase Test" )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - trim only pipeline
    def test__PostcodeParser_build_input_translator__trim(self):

        pipeline = PostcodeParser._build_input_translater(trim=True, uppercase=False)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), "TRIM TEST" )
        self.assertEqual( pipeline("Uppercase Test"), "Uppercase Test" )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - uppercase only pipeline
    def test__PostcodeParser_build_input_translator__uppercase(self):

        pipeline = PostcodeParser._build_input_translater(trim=False, uppercase=True)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), " TRIM TEST\t " )
        self.assertEqual( pipeline("Uppercase Test"), "UPPERCASE TEST" )

    ## tests that the PostcodeParser::_build_input_translater method creates functions
    #  that perform the expected actions - full pipeline
    def test__PostcodeParser_build_input_translator__full(self):

        pipeline = PostcodeParser._build_input_translater(trim=True, uppercase=True)

        self.assertEqual( pipeline("NO CHANGE"), "NO CHANGE" )
        self.assertEqual( pipeline(" TRIM TEST\t "), "TRIM TEST" )
        self.assertEqual( pipeline("Uppercase Test"), "UPPERCASE TEST" )

    ## This test to make sure we throw if we try and create a parser with an unknown
    #  method of handling whitespace in a predicable manner
    def test__PostcodeParser_ctor__with_bad_whitespace_handler(self):

        from wintersdeep_postcode.exceptions import ParseError
        self.assertRaises( ValueError, PostcodeParser, 
            trim_whitespace=False, 
            force_case=False, 
            whitespace='error'
        )
        

    ## This test is for the parser in its most strict configuration - strict whitepace
    #  handling, and no input translation. This is to ensure that in this mode, only 
    #  well formed postcodes are parsed. 
    def test__PostcodeParser_parse__with_no_translation(self):

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
    def test__PostcodeParser_parse__with_caps_correction(self):

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
    def test__PostcodeParser_parse__with_trimmed_whitespace(self):

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
    def test__PostcodeParser_parse__with_full_translation(self):

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
    def test__PostcodeParser_parse__tolerant(self):

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
    def test__PostcodeParser_parse__lenient(self):

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

    ## tests that the _get_parser_regex_list throws as expected when given bad params
    def test__PostcodeParser_get_parser_regex_list__bad_args(self):
        self.assertRaises(ValueError, PostcodeParser._get_parser_regex_list, type_list=[])

    ## tests that when we ask for the default parser (passing None, or ommiting) we 
    #  get back a parser that loads all postcode types.
    def test__PostcodeParser_get_parser_regex_list__all_types(self):
        
        from re import Pattern
        from wintersdeep_postcode.postcode_types import postcode_type_objects

        parser_list = PostcodeParser._get_parser_regex_list(type_list=None)
        
        # make sure it appears we loaded all types (basic count check only)
        self.assertEqual( len(postcode_type_objects), len(parser_list) )
        
        # and that the returned list appears usable
        for regex, factory in parser_list:
            self.assertIsInstance(regex, Pattern)
            self.assertTrue( callable(factory) )

        # and that the default list, is still the same as the None call.
        self.assertListEqual( parser_list, PostcodeParser._get_parser_regex_list() )
        
    ## tests that when we ask for a selective parser (passing a specific list) we 
    #  get back a parser that is loaded correctly
    def test__PostcodeParser_get_parser_regex_list__specific_type(self):
        
        from wintersdeep_postcode.postcode_types import postcode_type_objects

        test_type = postcode_type_objects[0]
        parser_list = PostcodeParser._get_parser_regex_list(
            type_list=[ test_type.PostcodeType ]
        )
        
        # make sure it appears we loaded all types (basic count check only)
        self.assertEqual( len(parser_list), 1 )
        self.assertIs( parser_list[0][1], test_type)
        
if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()