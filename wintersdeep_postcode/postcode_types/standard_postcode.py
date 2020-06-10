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
    #  @remarks loaded from JSON file 'standard_postcode.json'
    AreasWithOnlySingleDigitDistricts = []

    ## Areas that only have double digit districts (ignoring sub-divisions)
    #  @remarks loaded from JSON file 'standard_postcode.json'
    AreasWithOnlyDoubleDigitDistricts = []

    ## Areas that have a zero district.
    AreasWithAZeroDistrict = []

    ## Areas that do not have a district 10
    AreasWithNoDistrictTen = []

    ## Only a few areas have subdivided districts
    DistrictsWithSubdivision = {}

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
    
    ## Validation fault for when a postcode has a 10 district, but the area is not known to have this.
    NoTenDistrict = ValidationFault( ValidationFaultBase + 4,
        _("Postcodes in this area are not known to have a district ten."))
    
    ## Validation fault for when a postcode has a 10 district, but the area is not known to have this.
    SubdistrictsUnsupported = ValidationFault( ValidationFaultBase + 5,
        _("Postcodes in this area/district are not known to have subdivisions."))
    
    ## Validation fault when the postcode supports subdivisions, but no the one used.
    UnexpectedDistrictSubdivision = ValidationFault( ValidationFaultBase + 6, 
        _("Postcodes in this area/district have one or more sub-districts, but not the one used."))

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

        # only some areas are known to have a district zero...
        if postcode.outward_district == 0:
            if not postcode.outward_area in StandardPostcode.AreasWithAZeroDistrict:
                validation_faults.append(StandardPostcode.NoZeroDistrict)
        elif postcode.outward_district == 10:
            if postcode.outward_area in StandardPostcode.AreasWithNoDistrictTen:
                validation_faults.append(StandardPostcode.NoTenDistrict)

        # only a handful of postcode areas have subdistricts
        if postcode.outward_subdistrict:
            areas_with_subdistricts = StandardPostcode.DistrictsWithSubdivision
            if postcode.outward_area in areas_with_subdistricts:
                districts_with_divisions = areas_with_subdistricts[postcode.outward_area]
                if districts_with_divisions:
                    if postcode.outward_district in districts_with_divisions:
                        allowed_divisions = districts_with_divisions[postcode.outward_district]
                        if allowed_divisions:
                            if not postcode.outward_subdistrict in allowed_divisions:
                                validation_faults.append(StandardPostcode.UnexpectedDistrictSubdivision)
                    else:
                        # the district specified isn't in the map of districts that have divisions
                        validation_faults.append(StandardPostcode.SubdistrictsUnsupported)
            else:
                # the postcode is in an area not known to have sub-districting
                validation_faults.append(StandardPostcode.SubdistrictsUnsupported)
                

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


## Loads various static members used for validation of standard JSON postcodes from
#  a JSON file - this is expected to be the one that is co-located with this class.
def load_standard_postcode_static_variables_from_json():
    
    from json import load
    from os.path import dirname, join
    
    json_configuration_file = join( dirname(__file__), "standard_postcode.json" )
    
    with open(json_configuration_file, 'r') as file_handle:
        config_json = load(file_handle)

    StandardPostcode.AreasWithOnlySingleDigitDistricts = config_json['single-digit-districts']
    StandardPostcode.AreasWithOnlyDoubleDigitDistricts = config_json['double-digit-districts']
    StandardPostcode.AreasWithAZeroDistrict = config_json['has-zero-district']
    StandardPostcode.AreasWithNoDistrictTen = config_json['no-ten-district']

    subdivision_map = config_json["subdivided-districts"]
    StandardPostcode.DistrictsWithSubdivision = {  k: { 
        int(k1): v1 for k1, v1 in v.items()
    } for k, v in subdivision_map.items() }


load_standard_postcode_static_variables_from_json()