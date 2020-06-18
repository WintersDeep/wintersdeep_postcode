# project imports
from wintersdeep_postcode.postcode import Postcode
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
        return Postcode.CompileRegex(f"(?:{regex_pattern})")

    ## Determine if the given postcode appears to be valid.
    #  @param cls the class that is invoking this method.
    #  @param postcode the postcode to be checked.
    #  @returns a list of validation fault objects describing any problems with the postcode.
    @classmethod
    def Validate(cls, postcode):
        # these are special cases - they break the rules - if we ended up in this
        # object type, validation was the very act of parsing...
        return [ ]

    ## Gets the special case definition from a regex match. Does this by working out
    #  which regex matched (by looking at named groups), and using the label to map
    #  back to the definition class.
    #  @param regex_match the regex that matched the special case regeular expression
    #  @returns the special case definition object
    @staticmethod
    def GetDefinitionFromRegex(regex_match):

        # gets all the named matches as a group - this will include results for
        # all special cases - but one or more may have a value.
        all_results = regex_match.groupdict()

        # next we convert the dict into (key,value) tuples, and remove any that
        # did not get a match - this should leave us with one or more tuples
        only_matches = filter( lambda kvp: kvp[1], all_results.items() )

        # we might have more than one result, but should have at least one.
        # we might have more if the same pattern is used in multiple special cases.
        # this isn't actually expected to happen - but its worth noting it could.

        # pop off the first (and hopefully only) match, and take its key value
        first_match = next(only_matches)[0]
        
        # return the special case definition from the special cases map.
        return SpecialCase.Map[first_match]

    ## Get a list of the postcode parts / blocks from the entire regex match
    #  @param case_type the type of regex that matched; used to prevent having to be recursive.
    #  @param regex_match the regex match that was used to parse the query.
    #  @returns the postcode block as a list, this may be one or more items (usually 2, but not certain)
    @staticmethod
    def GetPostcodePartsFromRegex(case_type, regex_match):

        # the rules of the regex state that there should be no groups other than those
        # that wrap the postcode parts, or an entire postocde. Those that wrap the 
        # entire postcode should be named. Therefor to this match should be, a lot of 
        # None's from the failed matches, the actual named match, and its part groups.
        # To get our list of parts therefor we need to pop off the named match, and 
        # filter the Nones...
        
        # get an ordered list of all the matches.
        postcode_parts = list( regex_match.groups() )

        # work out where the full match is (so we can remove it)
        original_regex = regex_match.re
        named_groups_map = original_regex.groupindex
        target_group_index = named_groups_map[case_type]

        # this always seems to be +1 of the actual index?
        postcode_parts.pop(target_group_index -1)
        postcode_parts = filter(None, postcode_parts)
        
        return list(postcode_parts)


    ## Creates a new instance of the standard postcode object.
    #  @param self the instance of the object that is invoking this method,
    #  @param regex_match regular expression match describing the postcode.
    def __init__(self, regex_match):
        super().__init__(regex_match)
        self.special_case = SpecialCasePostcode.GetDefinitionFromRegex(regex_match)
        self.postcode_parts = SpecialCasePostcode.GetPostcodePartsFromRegex(
            self.special_case.identifier, regex_match
        )


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


if __name__ == "__main__":
    
    ##
    ##  If this class is the main entry point then we should run tests.
    ##

    from unittest import TextTestRunner, defaultTestLoader
    from special_case_postcode_tests import TestSpecialCasePostcode

    print("Running SpecialCasePostcode unit tests...")

    test_runner = TextTestRunner()
    test_loader_fn = defaultTestLoader.loadTestsFromTestCase
    unit_tests = test_loader_fn( TestSpecialCasePostcode )
    test_runner.run( unit_tests )