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

    ## Add a pattern to recognise this special case.
    #  @param self the instance of the object that is invoking this method.
    #  @param pattern_parts the parts of the pattern seperated by whitespace.
    def add_pattern(self, pattern_parts):

        if pattern_parts.__class__ is str:
            pattern_parts = [ pattern_parts ]
        elif not pattern_parts.__class__ is list:
            bad_type_name = pattern_parts.__class__.__name__
            raise TypeError(fr"pattern_parts is {bad_type_name}; expected str or list.")
        
        pattern_parts = [ s.strip() for s in pattern_parts ]
        pattern_parts = list( filter( None, pattern_parts ))

        if len(pattern_parts) == 0:
            raise ValueError("pattern_parts is an empty, or contained only empty strings - this won't work.")
        elif len(pattern_parts) == 1:
            pattern_parts.append("")

        self.patterns.append(pattern_parts)

    def get_detection_regex(self, whitespace):

        #
        # pattern parts arriving at this point should not be in any encapsulating
        # brackets - any internal brackets should be non-capture groups (i.e they
        # should start with "?:", otherwise they might mess up some logic).
        #

        regex_pattern_subpatterns = [ whitespace.join([
            fr"({s})" for s in p
        ]) for p in self.patterns ]
        regex_pattern = "|".join( fr"(?:{s})" for s in regex_pattern_subpatterns )
        return fr"(?P<{self.identifier}>{regex_pattern})"    
    
    def get_internal_parsers(self):
        
        outward_code = [ fr"(?P<outward_code>{pattern_parts[0]})" ]
        inward_code  = [ fr"(?P<inward_code>{pattern_parts[-1]})" ]
        other_code   = pattern_parts[1:-1]

        regex_string = Postcode.LenientWhitespace.join(
            outward_code + other_code + inward_code)
        
        parser_regex = Postcode.GetParseRegex(regex_string)

        self.parsers.append(parser_regex)

# Load all the special cases from directory
from os.path import dirname, join
FILE_DIRECTORY = dirname(__file__)
SPECIAL_CASE_DIRECTORY = join(FILE_DIRECTORY, "special_cases")
SpecialCase.LoadFromDirectory(SPECIAL_CASE_DIRECTORY)