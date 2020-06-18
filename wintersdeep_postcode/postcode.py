#  python3 imports
from re import compile as compile_regex

## UK Postcode Class
#  @summary This class represents the parsed form of a UK postcode.
class Postcode(object):

    ## The type of postcode represented by this object
    #  @param this should be overriden in derived classes.
    PostcodeType = 'unspecified'

    ## Helper method used to compile regular expressions.
    #  @param args parts of the regular expression to join and compile.
    #  @remarks prevents having to specifically import re imto implementations, 
    #    and standardises join logic
    @staticmethod
    def CompileRegex(*args):
        return compile_regex( "".join(
            [ r'^' ] + [ *args ] + [ r'$' ]
        ))

    ## Given a postcode, should validate it conforms to any rules.
    #  Raises an error when an implementor forgets to implement this function.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode that should be validated.
    #  @returns a list of validation faults observed with the postcode.
    @classmethod
    def Validate(cls, postcode):
        invoking_class = cls.__name__
        raise NotImplementedError(f"{invoking_class} does not implement validate; cannot validate '{postcode}'.")

    ## Creates a new instance of the postcode class.
    #  @param self the instance of the object that is invoking this method.
    #  @param regex_match the regular expression that triggered building this object.
    def __init__(self, regex_match):
        self._original_regex_match = regex_match
        self.validation_faults = {}
        self.is_validated = False
    
    ## The type of postcode that this represents.
    #  @param self the instance of the object that is invoking this method
    #  @retuns a string identifying this postcode type. 
    @property
    def postcode_type(self):
        return self.__class__.PostcodeType

if __name__ == "__main__":
    
    ##
    ##  If this is the main entry point - someone might be a little lost?
    ##

    print(f"{__file__} ran, but doesn't do anything on its own.")
    print(f"Check 'https://www.github.com/wintersdeep/wintersdeep_postcode' for usage.")