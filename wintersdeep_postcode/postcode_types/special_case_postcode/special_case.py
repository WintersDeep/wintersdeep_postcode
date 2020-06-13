# python3 imports
from json import loads

# project imports
from wintersdeep_postcode.postcode import Postcode

## Properties parsing for a special case postcode
class SpecialCase(object):

    ## A map of all the known special cases.
    Map = {}

    ## Loads all JSON files in the specified directory.
    #  @param directory_path the path to the directory with files that should be loaded.
    #  @param recursive indicates if we should recursively load from the given directory,
    @staticmethod
    def LoadFromDirectory(directory_path, recursive=True):
        from glob import iglob
        glob_path = fr"{directory_path}/**/*.json"
        for json_file in iglob(glob_path, recursive=recursive):
            SpecialCase.FromJsonFile(json_file)
        
    ## Loads a special case definition from a JSON string.
    #  @param json_string the json string that contains the definition of the special case.
    #  @returns a new special case object. 
    @staticmethod
    def FromJsonString(json_string):
        json = loads(json_string)

        special_case_id = json.pop("identifier")
        special_case = SpecialCase( special_case_id )

        for case_pattern in json.pop("regex-patterns"):
            special_case.add_pattern(case_pattern)
            
        return special_case

    ## Loads a special case definition from a JSON file.
    #  @param json_file the file to load the JSON content from.
    #  @returns a new special case from the loaded content.
    @staticmethod
    def FromJsonFile(json_file):
        with open(json_file, 'r') as file_handle:
            content_string = file_handle.read()
        return SpecialCase.FromJsonString(content_string)

    ## Creates a new instance of the special case definition
    #  @param self the instance of the object that is invoking this method.
    #  @param identifier the identifier of the special case being loaded.
    def __init__(self, identifier):

        if identifier in SpecialCase.Map:
            raise ValueError(f"Special case ID '{identifier}' is already allocated.")
        
        SpecialCase.Map[identifier] = self
        self.identifier = identifier
        self.patterns = []
        self.parsers = []

    ## Add a regex pattern which recognises this special case.
    #  @remarks the pattern is specified by array, each part is a chunk of the postcode seperated by whitespace
    #  @remarks we do this as whitespace handling/tolerance is defined by the parser.
    #  @param self the instance of the object that is invoking this method.
    #  @param pattern_parts the parts of the pattern seperated by whitespace.
    def add_pattern(self, pattern_parts):

        if pattern_parts.__class__ is str:
            pattern_parts = pattern_parts.split(" ")
        
        pattern_parts = [ s.strip() for s in pattern_parts ]
        pattern_parts = list( filter( None, pattern_parts ))

        if len(pattern_parts) > 0:
            self.patterns.append(pattern_parts)

    ## given the whitespace handling, compile a regular expression that can be
    #  used to identify this special case - it must follow these rules set out in the 
    #  comments in the function body.
    #  @param self the instance of the object invoking this method.
    #  @param whitespace the whitespace regex that should be used to join the parts.
    #  @returns a regular expression to detect this special case.
    def get_detection_regex(self, whitespace):

        #
        # ADDITIONAL RULES:
        # to extract each group from the postcode we extract all the postition matches.
        # as such the created regex must follow these additional rules:
        #   [*] each group/part must be encapsulated in a group (brackets).
        #   [*] the regex for each pattern must not result in additional groups - if they
        #       are needed they must be non-capture groups (these start with ?:).
        # if you dont follow these rules - this will break / not work

        regex_pattern_subpatterns = []
        
        for pattern in self.patterns:
            # encapsulate pattern parts in brackets
            pattern_parts = [ f"({part})" for part in pattern ]
            # join them together...
            pattern_regex = whitespace.join(pattern_parts)
            # wrap them in a group to prevent partial matches - but to ensure we don't
            # mess up the group logic described above - make it a non-capture group.
            wrapped_regex = f"(?:{pattern_regex})"
            # append to output regexes
            regex_pattern_subpatterns.append(wrapped_regex)
        
        full_regex_pattern = "|".join( regex_pattern_subpatterns )
        return fr"(?P<{self.identifier}>{full_regex_pattern})"    

## Loads special cases from the included special cases directory.
#  @remarks this is currently invoked just below - might want to change this?
def load_special_cases():    
    from os.path import dirname, join
    FILE_DIRECTORY = dirname(__file__)
    SPECIAL_CASE_DIRECTORY = join(FILE_DIRECTORY, "special_cases")
    SpecialCase.LoadFromDirectory(SPECIAL_CASE_DIRECTORY)

# load the default special cases.
load_special_cases()

if __name__ == "__main__":
    
    ##
    ##  If this class is the main entry point then we should run tests.
    ##

    from unittest import TextTestRunner, defaultTestLoader
    from special_case_tests import TestSpecialCase

    print("Running SpecialCase unit tests...")

    test_runner = TextTestRunner()
    test_loader_fn = defaultTestLoader.loadTestsFromTestCase
    unit_tests = test_loader_fn( TestSpecialCase )
    test_runner.run( unit_tests )