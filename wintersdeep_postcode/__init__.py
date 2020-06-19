# Module Meta Information.
__author__      =    "WintersDeep"
__copyright__   =    "Copyright 2020, WintersDeep.com"

__license__     =    "MIT"
__version__     =    "1.0.0"
__credits__     =    [ ]

__maintainer__  =   "WintersDeep.com"
__email__       =   "admin@wintersdeep.com"
__status__      =   "Production"

## Defines the modules that will be imported when someone uses *
__all__ = [
    "PostcodeParser",
    "PostcodeError",
    "ValidationError",
    "ParseError",
    "parse_postcode",
    "try_parse_postcode"
]

# Import the most relevant classes up to the module scope.
from wintersdeep_postcode.postcode_parser import PostcodeParser
from wintersdeep_postcode.exceptions import (PostcodeError, ValidationError, ParseError)

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
#  @param ignore_validation_errors will still return a postcode object, even if it doesn't validate.
#  @returns the postcode object on success, or the default value on failure.
def try_parse_postcode(postcode_string, default_value=None, ignore_validation_errors=False):
    try:
        return parse_postcode(postcode_string)
    except ValidationError as ex:
        return ex.postcode if ignore_validation_errors else default_value
    except ParseError as ex:
        return default_value