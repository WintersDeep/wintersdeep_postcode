# python3 imports
from re import compile as compile_regex
from gettext import gettext as _

# project imports
from wintersdeep_postcode.postcode import Postcode
from wintersdeep_postcode.exceptions.validation_fault import ValidationFault

## A standard UK postcode.
#  @remarks this represents standard UK domestic/commercial postcode 
#  @remarks probably will service for > 99.99% of this libraries usage. 
class StandardPostcode(Postcode):

    ## The type of postcode this class represents.
    PostcodeType = 'standard'

    ## Regular expression pattern expressing the format of the "area" portion of a postcode.
    AreaRegex = r"(?P<area>[A-Z]{1,2})"

    ## Regular expression pattern expressing the format of a "normal district" string.
    StandardDistrict = r"(?P<district>[0-9]{1,2}?)"

    ## Regular expression pattern expressing the format of a "sub-divided district" string.
    SubdividedDistrict = r"((?P<district_m>[0-9])(?P<district_n>[A-Z]))"

    ## Regular expression pattern expressing the format of the "district" portion of a postcode.
    DistrictRegex = fr"({StandardDistrict}|{SubdividedDistrict})"

    ## Regular expression pattern expressing the format of the "sector" portion of a postcode.
    SectorRegex = r"(?P<sector>[0-9])"

    ## Regular expression pattern expressing the format of the "subsector" portion of a postcode.
    UnitRegex = r"(?P<unit>[A-Z]{2})"

    ## Areas that only have single digit districts (ignoring sub-divisions)
    AreasWithOnlySingleDigitDistricts = [ 
        "BR", "FY", "HA", "HD", "HG", "HR", "HS", "HX",
        "JE", "LD", "SM", "SR", "WC", "WN", "ZE" 
    ]

    ## Areas that only have double digit districts (ignoring sub-divisions)
    AreasWithOnlyDoubleDigitDistricts = [
        "AB", "LL", "SO"
    ]

    ## Areas that have a zero district.
    AreasWithAZeroDistrict = [ 
        "BL", "BS", "CM", "CR", "FY", "HA","PR", "SL", "SS"
    ]

    ## The base number from which validation faults in this class start
    #  @remarks each class has 100 numbers allocated to it; SimplePostcode - 200 -> 299
    ValidationFaultBase = 200

    ## Validation fault for when a postcode in an area with only single digit districts cites a 2-digit one.
    ExpectedSingleDigitDistrict = ValidationFault( ValidationFaultBase + 1, 
        _("Postcodes in this area are expected to only have single digit districts.") )

    ## Validation fault for when a postcode in an area with only double digit districts cites a 1-digit one.
    ExpectedDoubleDigitDistrict = ValidationFault( ValidationFaultBase + 2, 
        _("Postcodes in this area are expected to only have double digit districts.") )

    ## Validation fault for when a postcode has a zero district, but the area is not known to have this.
    NoZeroDistrict = ValidationFault( ValidationFaultBase + 3,
        _("Postcodes in this area are not known to have a district zero."))
    
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

    ## Determine if the given postcode appears to be valid.
    #  @param cls the class that is invoking this method.
    #  @param postcode the postcode to be checked.
    #  @returns a list of validation fault objects describing any problems with the postcode.
    @classmethod
    def Validate(cls, postcode):

        validation_faults = []

        # some areas only have single/double digit districts - we check the district first in this case
        # so we only have to perform the appropriate test.
        if postcode.outward_district <= 9:
            if postcode.outward_area in StandardPostcode.AreasWithOnlyDoubleDigitDistricts:
                validation_faults.append(StandardPostcode.ExpectedDoubleDigitDistrict)
        else: 
            if postcode.outward_area in StandardPostcode.AreasWithOnlySingleDigitDistricts:
                validation_faults.append(StandardPostcode.ExpectedSingleDigitDistrict)

        ## only some areas are known to have a district zero...
        if postcode.outward_district == 0:
            if not postcode.outward_area in StandardPostcode.AreasWithAZeroDistrict:
                validation_faults.append(StandardPostcode.NoZeroDistrict)

        return validation_faults

    ## Creates a new instance of the standard postcode object.
    #  @param self the instance of the object that is invoking this method,
    #  @param regex_match regular expression match describing the postcode.
    def __init__(self, regex_match):
        
        super().__init__(regex_match)

        self.outward_area        = regex_match.group("area")    
        self.outward_district    = int(regex_match.group("district") or \
                                        regex_match.group("district_m") )
        self.outward_subdistrict = regex_match.group("district_n") or ""
        self.inward_sector       = int(regex_match.group("sector"))
        self.inward_unit         = regex_match.group("unit")

    ## Gets the postcodes outward code.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the postcodes outward code as a string.
    @property
    def outward_code(self):
        return  self.outward_area           + \
                str(self.outward_district)  + \
                self.outward_subdistrict
    
    ## Gets the postcodes inward code.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the postcodes outward code as s string.
    @property
    def inward_code(self):
        return  str(self.inward_sector)     + \
                self.inward_unit

    ## Returns a simple string representation of the object.
    #  @param self the instance of the object that is invoking this method.
    #  @returns a string representation of this object suitable for user consumption.
    def __str__(self):
        return f"{self.outward_code} {self.inward_code}"   