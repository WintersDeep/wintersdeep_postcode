# python3 imports
from gettext import gettext as _

## Postcode Parsing error
#  Raised when a value passed to PostCode parser object cannot be parsed.
class ParseError(ValueError):
    
    ## Creates a new instance of the parse error object.
    #  @param self the instance of the object that is invoking this method.
    #  @param input_string the string that could not be parsed.
    #  @param parser a reference to the parser that raised this exception.
    def __init__(self, input_string, parser):
        super().__init__( _(fr"Invalid postcode structure '%s'.") % input_string )
        self.source_input = input_string
        self.source_parser = parser

if __name__ == "__main__":

    ##
    ## If this file is the main entry point - run tests
    ##

    from unittest import TextTestRunner, defaultTestLoader
    from parse_error_tests import TestParseError

    print( f"Running ParseError unit tests...")

    test_runner = TextTestRunner()
    test_loader_fn = defaultTestLoader.loadTestsFromTestCase
    unit_tests = test_loader_fn(TestParseError)
    test_runner.run( unit_tests)