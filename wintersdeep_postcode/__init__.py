# Module Meta Information.
__author__      =    "Adam Williams"
__copyright__   =    "Copyright 2020, WintersDeep.com"

__license__     =    "MIT"
__version__     =    "0.0.0a1"
__credits__     =    [ ]

__maintainer__  =   "WintersDeep.com"
__email__       =   "admin@wintersdeep.com"
__status__      =   "Development"

# Import the most relevant classes up to the module scope.
from wintersdeep_postcode.postcode_parser import PostcodeParser
from wintersdeep_postcode.exceptions import (ValidationError, ParseError)

## Parses a postcode string using the default postcode parser.
#  @param postcode_string the postcode string that should be parsed.
#  @returns the postcode string as a postcode object.
#  @throws ParseError if the postcode cannot be parsed.
#  @throws ValidationError if the postcode cannot be parsed.
def parse_postcode(postcode_string):
    parser = PostcodeParser()
    return parser(postcode_string)

## Parses a postcode using the default postcode parser, in a more forgiving manner.
#  @param postcode_string the postcode string that should be parsed.
#  @param default_value the value to return in the event that the postcode cannot be parsed.
#  @param ignore_validation_error will still return a postcode object, even if it doesn't validate.
#  @returns the postcode object on success, or the default value on failure.
def try_parse_postcode(postcode_string, default_value=None, ignore_validation_error=False):
    try:
        return parse_postcode(postcode_string)
    except ValidationError as ex:
        return ex.postcode if ignore_validation_error else default_value
    except ParseError as ex:
        return default_value