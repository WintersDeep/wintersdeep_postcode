# python3 imports
from re import compile as compile_regex
from gettext import gettext as _

# project imports
from wintersdeep_postcode.postcode import Postcode
from wintersdeep_postcode.exceptions.validation_fault import ValidationFault

## A British Forces Postcode Office postcode.
#  @remarks this represents postcode destined for the BFPO service. 
class ForcesPostcode(Postcode):

    ## The type of postcode this class represents.
    PostcodeType = 'forces'

    ## Regular expression pattern expressing the BFPO outward code string. 
    BfpoRegex = r"(?:BFPO)"

    ## Traditional BFPO postcode - inward area regex match numeric value between 1 and 4 digits. 
    BfpoNumberRegex = r"(?P<bfpo>[0-9]{1,4})"

    ## UK postcode compatible BFPO address - technically the district can only be 1 or 2, but we'll accept
    #  double digits, as all BF is allocated to BFPO and it might be used in the future. We'll handle 
    #  actual validation in Validate() - we'll ignore subdistrcts for now however.
    DistrictRegex = r"(?:BF)(?P<district>[0-9]{1,2})"

    ## Regular expression pattern expressing the format of the "sector" portion of a postcode.
    SectorRegex = r"(?P<sector>[0-9])"

    ## Regular expression pattern expressing the format of the "subsector" portion of a postcode.
    UnitRegex = r"(?P<unit>[A-Z]{2})"

    ## The base number from which validation faults in this class start
    #  @remarks each class has 100 numbers allocated to it; ForcesPostcode - 400 -> 499
    ValidationFaultBase = 400 
    
    ## Validation fault raised when the district is not valid for a forces postcode.
    InvalidDistrict = ValidationFault( ValidationFaultBase + 1, 
        _("{district} is not a valid district for BF postcodes."))

    ## Get a regular expression that can be used to parse postcodes of this type.
    #  @param whitespace_regex the regular expression used to parse any delimiting whitespace.
    #  @returns a compiled regular expression that can be used to parse a regeex of this type. 
    @staticmethod
    def GetParseRegex(whitespace_regex = r'\ '):

        bfpo_regex = "".join([
            ForcesPostcode.BfpoRegex,
            whitespace_regex,
            ForcesPostcode.BfpoNumberRegex
        ])

        bf_regex = "".join([
            ForcesPostcode.DistrictRegex,
            whitespace_regex,
            ForcesPostcode.SectorRegex,
            ForcesPostcode.UnitRegex
        ])

        return Postcode.CompileRegex(fr"^({bfpo_regex}|{bf_regex})$")

    ## Determine if the given postcode appears to be valid.
    #  @param cls the class that is invoking this method.
    #  @param postcode the postcode to be checked.
    #  @returns a list of validation fault objects describing any problems with the postcode.
    @classmethod
    def Validate(cls, postcode):

        faults = []

        if not postcode.is_bfpo_format:
            if postcode.outward_district > 2:
                faults.append(ForcesPostcode.InvalidDistrict)

        return faults

    ## Creates a new instance of the forces postcode object.
    #  @param self the instance of the object that is invoking this method,
    #  @param regex_match regular expression match describing the postcode.
    def __init__(self, regex_match):
        
        super().__init__(regex_match)
        
        bfpo = regex_match.group("bfpo")
        
        self.is_bfpo_format = bool(bfpo)

        if self.is_bfpo_format:
            self.bfpo = int(bfpo)
            self.outward_area = None
            self.outward_district = None
            self.inward_sector = None
            self.inward_unit = None
        else:
            self.bfpo = None
            self.outward_area = "BF"
            self.outward_district = int(regex_match.group("district"))
            self.inward_sector = int(regex_match.group("sector"))
            self.inward_unit = regex_match.group("unit")

    ## Gets the postcodes outward code.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the postcodes outward code as a string.
    @property
    def outward_code(self):
        return  "BFPO" if self.is_bfpo_format else f"{self.outward_area}{self.outward_district}"
    
    ## Gets the postcodes inward code.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the postcodes outward code as s string.
    @property
    def inward_code(self):
        return  str(self.bfpo) if self.is_bfpo_format else f"{self.inward_sector}{self.inward_unit}"

    ## Returns a simple string representation of the object.
    #  @param self the instance of the object that is invoking this method.
    #  @returns a string representation of this object suitable for user consumption.
    def __str__(self):
        return f"{self.outward_code} {self.inward_code}"
        
if __name__ == "__main__":
    
    ##
    ##  If this is the main entry point - someone might be a little lost?
    ##

    print(f"{__file__} ran, but doesn't do anything on its own.")
    print(f"Check 'https://www.github.com/wintersdeep/wintersdeep_postcode' for usage.")