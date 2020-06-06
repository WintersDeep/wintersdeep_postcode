# https://en.m.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom
# The structure of a postcode is two alphanumeric codes, the first having between two 
# and four characters and the second, three characters. First, one or two letters 
# indicate the postcode area, followed by one or two digits signifying a district 
# within that area. This is followed by a space and then a number denoting a sector 
# within said district, and finally by two letters which are allocated to streets or 
# sides of a street.

# python3 imports
from re import compile

## Class responsible for parsing a postcode object.
#  @remarks will parse a string into a Postcode object.
class PostcodeParser(object):

    ## Regular expression pattern expressing the format of the "area" portion of a postcode.
    AreaRegex = r"(?P<area>[A-Z]{1,2})"

    ## Regular expression pattern expressing the format of the "district" portion of a postcode.
    DistrictRegex = r"(?P<district>([0-9]{1,2})|([0-9][A-Z]))"

    ## Regular expression pattern expressing the format of the "sector" portion of a postcode.
    SectorRegex = r"(?P<sector>[0-9])"

    ## Regular expression pattern expressing the format of the "subsector" portion of a postcode.
    SubsectorRegex = r"(?P<unit>[A-Z]{2})"

    ## Regular expression used if the parser is using strict whitespace rules.
    #  @remarks postcodes must use a single space character in this mode.
    #  @remarks use 'whitespace': 'strict' to use this option - see PostcodeParser._get_whitepsace_pattern
    StrictWhitespace = r"(\ )"

    ## Regular expression used if the parser is using tolerant whitespace.
    #  @remarks postcodes can use zero or one whitespace character in this mode. 
    #  @remarks use 'whitespace': 'tolerant' to use this option - see PostcodeParser._get_whitepsace_pattern
    TolerantWhitespace = r"(\ ?)"

    ## Regular expression used if the parser is using lenient whitespace rules.
    #  @remarks postcodes can use zero or more whitespace characters as in this mode.
    #  @remarks use 'whitespace': 'lenient' to use this option - see PostcodeParser._get_whitepsace_pattern
    LenientWhitespace = r"(\s*)"

    ## Creates a new instance of the postcode parser object.
    #  @param self the instance of the object that is invoking this method.
    #  @param kwargs the keyword arguments that are being applied to this object.
    #  @remarks see local 'keyword_arguments' for arguments, and what they achieve.
    def __init__(self, **kwargs):

        keyword_arguments = {
            ## indicates how the postcodes whitespace seperator is be handled.
            #  @remarks available options are 'strict', 'tolerant', and 'lenient'.
            #  @remarks see static members StrictWhitespace, TolerantWhitespace and LenientWhitespace respectively.  
            'whitespace': 'tolerant',

            ## determines if parser input should be forced to uppercase.
            #  defaults to True; if False and lower case input is provided, the element will fail to parse.
            'force_case': True,

            ## determines if parser input should be trimmed before its parsed.
            #  defaults to True; if False and padded input is provided, the element will fail to parse. 
            'trim_whitespace': True
        }

        keyword_arguments.update(kwargs)
        
        # actually do the initialisation here.
        self._configure_from_kwargs(keyword_arguments)

        if len(keyword_arguments):
            invalid_keys = ", ".join( keyword_arguments.keys() )
            error_message = f"Invalid keyword argument(s): {invalid_keys}"
            raise TypeError(error_message)

    ## Determines the regular expression pattern used when parsing postcode whitespace.
    #  @param whitespace the whitespace configuration to apply, see local supported_whitespace_patterns.
    #  @returns a regular expression string that can be used to parse postcode whitespace.
    #  @throws ValueError when whitespace isn't a recognised type string.
    @staticmethod
    def _get_whitespace_pattern(whitespace):

        supported_whitespace_patterns = {
            'strict':   PostcodeParser.StrictWhitespace,
            'tolerant': PostcodeParser.TolerantWhitespace,
            'lenient':  PostcodeParser.LenientWhitespace
        }

        whitespace_pattern = supported_whitespace_patterns.get(whitespace, None)

        if not whitespace_pattern:
            supported_types = ", ".join( supported_whitespace_patterns.keys() )
            error_message = f"whitespace is expected to be one of - {supported_types}; actually got '{whitespace}''"
            raise ValueError(error_message) 

        return whitespace_pattern

    ## creates a pipeline to translate parser input.
    #  @param trim_input when true input will be trimmed of leading/tailing whitespace
    #  @param uppercase_input when true input will be converted to uppercase.
    #  @returns a function that can be used to translate input into a parsable form.
    @staticmethod
    def _build_input_translater(trim=True, uppercase=True):
        
        translation_pipeline = [ str ]

        if trim:        translation_pipeline.append( str.strip )
        if uppercase:   translation_pipeline.append( str.upper )

        if len(translation_pipeline) == 1:
            return translation_pipeline[0]
        else:
            def compose(lhs, rhs):
                return lambda input_: rhs( lhs(input_) )
            from functools import reduce
            return reduce( compose, translation_pipeline)

    ## Creates the regular expression used to parse postcode strings.
    #  @param whitespace_regex the regex pattern used to handle whitespace.
    @staticmethod
    def _build_parser_regex(whitespace_regex):

        return compile("".join([
            r"^",
            PostcodeParser.AreaRegex,
            PostcodeParser.DistrictRegex,
            whitespace_regex,
            PostcodeParser.SectorRegex,
            PostcodeParser.SubsectorRegex,
            r"$"
        ]))

    ## Configures the object using keyword arguments
    #  @param self the instance of the object that is invoking this method.
    #  @param kwargs the keyword arguments dict to load configuration from.
    #  @throws TypeError when an argument is provided, but has an unsupported type. 
    def _configure_from_kwargs(self, kwargs):

        # sort out whitespace handling
        whitespace_stratergy = kwargs.pop('whitespace', 'tolerant')
        whitespace_translate = PostcodeParser._get_whitespace_pattern
        self.whitespace_regex = whitespace_translate(whitespace_stratergy)

        # load other options
        self.translate_input = PostcodeParser._build_input_translater(
            uppercase = bool( kwargs.pop('force_case', True) ),
            trim = bool( kwargs.pop('trim_whitespace', True) )
        ) 

        # create the core regex parser.
        self.postcode_regex = PostcodeParser._build_parser_regex(
            whitespace_regex = self.whitespace_regex
        )

    ## Parses an input string into a postcode.
    #  @param self the instance of the object that is invoking this method
    #  @param input_string the input string to be parsed into a postcode.
    #  @returns a Postcode object that was parsed from the input string.
    def parse(self, input_string):

        transformed_string = self.translate_input(input_string)
        postcode_match = self.postcode_regex.match(transformed_string)

        if postcode_match:
            return True
        else:
            # we are unable to parse the given input - raise a parse error
            from wintersdeep_postcode.exceptions import ParseError
            raise ParseError(input_string, self)

    ## allows directly invoking the class to parse input
    #  @param self the instance of the object that is invoking this method.
    #  @param input_string the string that was provided by the user.
    def __call__(self, input_string):
        return self.parse(input_string)       


if __name__ == "__main__":
    
    ##
    ##  If this class is the main entry point then we should run tests.
    ##

    from unittest import TextTestRunner, defaultTestLoader
    from postcode_parser_tests import TestPostcodeParser

    print("Running postcode parser unit tests...")

    test_runner = TextTestRunner()
    test_loader_fn = defaultTestLoader.loadTestsFromTestCase
    unit_tests = test_loader_fn( TestPostcodeParser )
    test_runner.run( unit_tests )