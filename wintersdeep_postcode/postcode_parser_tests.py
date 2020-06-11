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

    ## test that we throw an error if excess / unrecognised keywords are recevied.
    def test__PostcodeParser_ctor_excess_keywords(self):
        self.assertRaises(TypeError, PostcodeParser, unused="value")
        self.assertRaises(TypeError, PostcodeParser, whitespace="tolerant", unused="value")

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
        postcode_parser = PostcodeParser(trim_whitespace=False, force_case=False, whitespace='strict', validate=False)
        
        self.assertRaises(ParseError, postcode_parser, "aa1 1aa")
        self.assertRaises(ParseError, postcode_parser, "AA11AA")
        self.assertRaises(ParseError, postcode_parser, "AA1  1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t 1AA")
        self.assertRaises(ParseError, postcode_parser, " AA1 1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1 1AA ")
        self.assertRaises(ParseError, postcode_parser, " AA1 1AA ")
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A1 1AA") )
        self.assertIsNotNone( postcode_parser("A11 1AA") )
        self.assertIsNotNone( postcode_parser("A1A 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA11 1AA") )
        self.assertIsNotNone( postcode_parser("AA1A 1AA") )

    ## This test is for the parser in a strict configuration - strict whitepace
    #  handling, and only case correction enabled. This is to ensure that in 
    #  this mode, well formed postcodes of any case are parsed. 
    def test__PostcodeParser_parse__with_caps_correction(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=False, force_case=True, whitespace='strict', validate=False)
        
        self.assertIsNotNone( postcode_parser("aa1 1aa") )
        self.assertRaises(ParseError, postcode_parser, "AA11AA")
        self.assertRaises(ParseError, postcode_parser, "AA1  1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t 1AA")
        self.assertRaises(ParseError, postcode_parser, " AA1 1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1 1AA ")
        self.assertRaises(ParseError, postcode_parser, " AA1 1AA ")
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A1 1AA") )
        self.assertIsNotNone( postcode_parser("A11 1AA") )
        self.assertIsNotNone( postcode_parser("A1A 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA11 1AA") )
        self.assertIsNotNone( postcode_parser("AA1A 1AA") )

    ## This test is for the parser in a strict configuration - strict whitepace
    #  handling, and ony whitepace trimming enabled. This is to ensure that in this 
    #  mode, well formed postcodes with whitespace padding are parsed correctly. 
    def test__PostcodeParser_parse__with_trimmed_whitespace(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=False, whitespace='strict', validate=False)
        
        self.assertRaises(ParseError, postcode_parser, "aa1 1aa")
        self.assertRaises(ParseError, postcode_parser, "AA11AA")
        self.assertRaises(ParseError, postcode_parser, "AA1  1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t 1AA")
        self.assertIsNotNone( postcode_parser(" AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA ") )
        self.assertIsNotNone( postcode_parser(" AA1 1AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A1 1AA") )
        self.assertIsNotNone( postcode_parser("A11 1AA") )
        self.assertIsNotNone( postcode_parser("A1A 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA11 1AA") )
        self.assertIsNotNone( postcode_parser("AA1A 1AA") )

    ## This test is for the parser in a severe configuration - strict whitepace
    #  handling, but full pre-processing enabled. This is to ensure that in this 
    #  mode, well formed postcodes which may be slightly "dirty" are parsed. 
    def test__PostcodeParser_parse__with_full_translation(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=True, whitespace='strict', validate=False)
        
        self.assertIsNotNone( postcode_parser("aa1 1aa") )
        self.assertRaises(ParseError, postcode_parser, "AA11AA")
        self.assertRaises(ParseError, postcode_parser, "AA1  1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t 1AA")
        self.assertIsNotNone( postcode_parser(" AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA ") )
        self.assertIsNotNone( postcode_parser(" AA1 1AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A1 1AA") )
        self.assertIsNotNone( postcode_parser("A11 1AA") )
        self.assertIsNotNone( postcode_parser("A1A 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA11 1AA") )
        self.assertIsNotNone( postcode_parser("AA1A 1AA") )

    ## This test is for the parser in a tolerant configuration - tolerant whitepace
    #  handling, and full pre-processing enabled. This is to ensure that in this 
    #  mode, well formed postcodes which may be slightly "dirty" are parsed. 
    def test__PostcodeParser_parse__tolerant(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=True, whitespace='tolerant', validate=False)
        
        self.assertIsNotNone( postcode_parser("aa1 1aa") )
        self.assertIsNotNone( postcode_parser("AA11AA") )
        self.assertRaises(ParseError, postcode_parser, "AA1  1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t1AA")
        self.assertRaises(ParseError, postcode_parser, "AA1\t 1AA")
        self.assertIsNotNone( postcode_parser(" AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA ") )
        self.assertIsNotNone( postcode_parser(" AA1 1AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A1 1AA") )
        self.assertIsNotNone( postcode_parser("A11 1AA") )
        self.assertIsNotNone( postcode_parser("A1A 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA11 1AA") )
        self.assertIsNotNone( postcode_parser("AA1A 1AA") )

    ## This test is for the parser in a lenient configuration - lenient whitepace
    #  handling, and full pre-processing enabled. This is to ensure that in this 
    #  mode, well formed postcodes which may be slightly "dirty" are parsed. 
    def test__PostcodeParser_parse__lenient(self):

        from wintersdeep_postcode.exceptions import ParseError
        postcode_parser = PostcodeParser(trim_whitespace=True, force_case=True, whitespace='lenient', validate=False)
        
        self.assertIsNotNone( postcode_parser("aa1 1aa") )
        self.assertIsNotNone( postcode_parser("AA11AA") )
        self.assertIsNotNone( postcode_parser("AA1  1AA") )
        self.assertIsNotNone( postcode_parser("AA1\t1AA") )
        self.assertIsNotNone( postcode_parser("AA1\t 1AA") )
        self.assertIsNotNone( postcode_parser(" AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA ") )
        self.assertIsNotNone( postcode_parser(" AA1 1AA ") )
        self.assertRaises(ParseError, postcode_parser, 1)
        self.assertRaises(ParseError, postcode_parser, False)
    
        self.assertIsNotNone( postcode_parser("A1 1AA") )
        self.assertIsNotNone( postcode_parser("A11 1AA") )
        self.assertIsNotNone( postcode_parser("A1A 1AA") )
        self.assertIsNotNone( postcode_parser("AA1 1AA") )
        self.assertIsNotNone( postcode_parser("AA11 1AA") )
        self.assertIsNotNone( postcode_parser("AA1A 1AA") )

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

    ## tests that the postcode parser respects the validate keyword argument
    def test__PostcodeParser_ctor__validate_keyword(self):
        
        from wintersdeep_postcode.postcode_types import StandardPostcode
        from wintersdeep_postcode.exceptions import ParseError, ValidationError

        # one postcode to check that validation errors are thrown, and another for parser errors
        postcode_invalid = "LL9 2XX"
        postcode_valid = "LL20 2XX"
        postcode_malformed = "LL20 XXX"

        postcode_parser = PostcodeParser(validate=True)
        self.assertRaises(ParseError, postcode_parser.parse, postcode_malformed)
        self.assertRaises(ValidationError, postcode_parser.parse, postcode_invalid)

        postcode = postcode_parser.parse(postcode_valid)
        self.assertIsInstance(postcode, StandardPostcode)
        self.assertFalse(postcode.validation_faults)
        self.assertTrue(postcode.is_validated)

        postcode_parser = PostcodeParser(validate=False)
        self.assertRaises(ParseError, postcode_parser.parse, postcode_malformed)

        postcode = postcode_parser.parse(postcode_invalid)
        self.assertIsInstance(postcode, StandardPostcode)
        self.assertFalse(postcode.validation_faults)
        self.assertFalse(postcode.is_validated)

    ## tests that the ignore faults keyword allows people to mask postcode faults they
    # wish to supress (future troubleshooting, errors, or to be more forgiving)
    def test__PostcodeParser_ctor__ignore_faults(self):
        
        from wintersdeep_postcode.postcode_types import StandardPostcode
        from wintersdeep_postcode.exceptions import ParseError, ValidationError

        # one postcode to check that validation errors are thrown, and another for parser errors
        postcode_invalid_but_ignored = "LL9 2XX"
        postcode_invalid_not_ignored = "HX10 2XX"
        postcode_valid = "LL20 2XX"
        postcode_malformed = "LL20 XXX"

        supress_error = StandardPostcode.ExpectedDoubleDigitDistrict
        
        for test_error in [ supress_error, int(supress_error) ]:

            postcode_parser = PostcodeParser(validate=True, ignored_faults=[ test_error ])

            self.assertRaises(ParseError, postcode_parser.parse, postcode_malformed)

            postcode = postcode_parser.parse(postcode_valid)
            self.assertIsInstance(postcode, StandardPostcode)
            self.assertFalse(postcode.validation_faults)
            self.assertTrue(postcode.is_validated)

            postcode = postcode_parser.parse(postcode_invalid_but_ignored)
            self.assertIsInstance(postcode, StandardPostcode)
            self.assertEqual( len(postcode.validation_faults), 1)
            self.assertTrue(postcode.is_validated)
            
            try:
                postcode_parser.parse(postcode_invalid_not_ignored)
                self.fail(f"Parsing '{postcode_invalid_not_ignored}' was expected to trigger an exception.")
            except ValidationError as ex:
                self.assertTrue( int(StandardPostcode.ExpectedSingleDigitDistrict) in ex.postcode.validation_faults)
                self.assertEqual( len(ex.postcode.validation_faults), 1)
                self.assertFalse(ex.postcode.is_validated)

    ## attempts to parse every postcode in the UK to check we are good.
    #  @remarks will only do this if the relevant file is available.
    def test_parse_all_current_uk_postocodes__if_available(self):
        
        from os.path import exists
        
        root_relative_file_path = join("reference", "current-uk-postcodes.txt")
        file_path = join(PROJECT_ROOT_DIRECTORY, root_relative_file_path)
        
        if not exists(file_path):
            error_major = f"Can't run test without {root_relative_file_path}"
            error_minor = "this may not be checked-in/available for licencing or file size reasons."
            self.skipTest(f"{error_major}; {error_minor}")
        
        from wintersdeep_postcode.exceptions import ParseError

        with open(file_path, 'r') as file_handle:
            parser = PostcodeParser()
            postcode_string = file_handle.readline()
            while postcode_string:
                try:
                    postcode = parser(postcode_string)
                    self.assertTrue(postcode.is_validated)
                except ParseError as ex:
                    print(str(ex))
                postcode_string = file_handle.readline()



if __name__ ==  "__main__":

    ##
    ## if this file is the main entry point, run the contained tests.
    ##

    from unittest import main as unit_test_entry_point
    unit_test_entry_point()