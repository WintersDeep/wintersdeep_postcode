# python3 imports
from re import compile as compile_regex

# project imports
from wintersdeep_postcode.postcode import Postcode

## A standard UK postcode.
#  @remarks this represents standard UK domestic/commercial postcode 
#  @remarks probably will service for > 99.99% of this libraries usage. 
class StandardPostcode(Postcode):

    ## The type of postcode this class represents.
    PostcodeType = 'standard'

    ## Regular expression pattern expressing the format of the "area" portion of a postcode.
    AreaRegex = r"(?P<area>[A-Z]{1,2})"

    ## Regular expression pattern expressing the format of the "district" portion of a postcode.
    DistrictRegex = r"(?P<district>([0-9]{1,2})|([0-9][A-Z]))"

    ## Regular expression pattern expressing the format of the "sector" portion of a postcode.
    SectorRegex = r"(?P<sector>[0-9])"

    ## Regular expression pattern expressing the format of the "subsector" portion of a postcode.
    UnitRegex = r"(?P<unit>[A-Z]{2})"

    ## Get a regular expression that can be used to parse postcodes of this type.
    #  @param whitespace_regex the regular expression used to parse any delimiting whitespace.
    #  @returns a compiled regular expression that can be used to parse a regeex of this type. 
    @staticmethod
    def GetParseRegex(whitespace_regex = r'\ '):
        return Postcode.CompileRegex(
            StandardPostcode.AreaRegex, 
            StandardPostcode.DistrictRegex, 
            whitespace_regex, 
            StandardPostcode.SectorRegex, 
            StandardPostcode.UnitRegex
        )

    ## Creates a new instance of the standard postcode object.
    #  @param self the instance of the object that is invoking this method,
    #  @param regex_match regular expression match describing the postcode.
    def __init__(self, regex_match):
        
        super().__init__(regex_match)

        self.outward_area        = regex_match.group("area")    
        self.outward_district    = regex_match.group("district")
        self.inward_sector       = regex_match.group("sector")
        self.inward_unit         = regex_match.group("unit")
