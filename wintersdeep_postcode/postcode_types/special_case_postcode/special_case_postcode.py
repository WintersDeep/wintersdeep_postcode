# python3 imports
from gettext import gettext as _


# project imports
from wintersdeep_postcode.postcode import Postcode
from wintersdeep_postcode.exceptions.validation_fault import ValidationFault
from wintersdeep_postcode.postcode_types.special_case_postcode.special_case import SpecialCase

## A postcode which doesn't follow any rules.
#  @remarks this represents a select few special cases which are create for a specific use. 
#  @remarks these postcodes do not follow any of the normal rules, and should just be accepted.
class SpecialCasePostcode(Postcode):

    ## The type of postcode this class represents.
    PostcodeType = 'special-case'

    ## The base number from which validation faults in this class start
    #  @remarks each class has 100 numbers allocated to it; SpecialCasePostcode - 300 -> 399
    ValidationFaultBase = 300

    #
    # No validation faults current raised or expected.
    # (We are running against a specific string at this point - theres nothing to validate)
    #

    ## Get a regular expression that can be used to parse postcodes of this type.
    #  @param whitespace_regex the regular expression used to parse any delimiting whitespace.
    #  @returns a compiled regular expression that can be used to parse a regeex of this type. 
    @staticmethod
    def GetParseRegex(whitespace_regex = r'\ '):
        special_cases = SpecialCase.Map
        regex_pattern = "|".join([ sc.get_detection_regex(whitespace_regex) \
            for sc in special_cases.values() ] )
        return Postcode.CompileRegex(regex_pattern)

    ## Determine if the given postcode appears to be valid.
    #  @param cls the class that is invoking this method.
    #  @param postcode the postcode to be checked.
    #  @returns a list of validation fault objects describing any problems with the postcode.
    @classmethod
    def Validate(cls, postcode):
        # these are special cases - they break the rules - if we ended up in this
        # object type, validation was the very act of parsing...
        return [ ]

    ## Creates a new instance of the standard postcode object.
    #  @param self the instance of the object that is invoking this method,
    #  @param regex_match regular expression match describing the postcode.
    def __init__(self, regex_match):
        super().__init__(regex_match)

        all_results = regex_match.groupdict()
        only_matches = filter( lambda kvp: kvp[1], all_results.items() )
        first_match = next(only_matches)[0]
        
        self.special_case = SpecialCase.Map[first_match]
        postcode_parts = list( regex_match.groups() )
        for index in reversed( list(regex_match.re.groupindex.values() )):
            postcode_parts.pop(index - 1)
        
        postcode_parts = filter(None, postcode_parts)
        self.postcode_parts = list(postcode_parts)


    ## Gets the postcodes outward code.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the postcodes outward code as a string.
    @property
    def outward_code(self):
        return  self.postcode_parts[0]

    ## Gets the postcodes inward code.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the postcodes outward code as s string.
    @property
    def inward_code(self):
        return  self.postcode_parts[-1] if len(self.postcode_parts) > 1 else ""

    ## Returns a simple string representation of the object.
    #  @param self the instance of the object that is invoking this method.
    #  @returns a string representation of this object suitable for user consumption.
    def __str__(self):
        return " ".join(self.postcode_parts)
