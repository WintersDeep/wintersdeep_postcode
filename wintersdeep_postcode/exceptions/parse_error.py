# python3 imports
from gettext import gettext as _

# project imports
from wintersdeep_postcode.exceptions.postcode_error import PostcodeError

## Postcode Parsing error
#  Raised when a value passed to PostCode parser object cannot be parsed.
class ParseError(PostcodeError):
    
    ## Creates a new instance of the parse error object.
    #  @param self the instance of the object that is invoking this method.
    #  @param input_string the string that could not be parsed.
    #  @param parser a reference to the parser that raised this exception.
    def __init__(self, input_string, parser):
        super().__init__( fr"Invalid postcode structure '{input_string}'.")
        self.source_input = input_string
        self.source_parser = parser
        
if __name__ == "__main__":
    
    ##
    ##  If this is the main entry point - someone might be a little lost?
    ##

    print(f"{__file__} ran, but doesn't do anything on its own.")
    print(f"Check 'https://www.github.com/wintersdeep/wintersdeep_postcode' for usage.")