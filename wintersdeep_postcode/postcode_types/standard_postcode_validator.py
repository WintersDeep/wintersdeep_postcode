# python3 imports
from re import compile as compile_regex
from gettext import gettext as _

# project imports
from wintersdeep_postcode.postcode import Postcode
from wintersdeep_postcode.exceptions.validation_fault import ValidationFault

## A wrapper for validation of standard postcodes
#  @remarks see \ref wintersdeep_postcode.postcode_types.standard_postcode 
class StandardPostcodeValidator(object):



    ## Areas that only have single digit districts (ignoring sub-divisions)
    #  @remarks loaded from JSON file 'standard_postcode_validator.json'
    AreasWithOnlySingleDigitDistricts = []

    ## Checks if a postcode is in an area with only single digit districts and if 
    #  so - that the district specified is only a single digit.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckAreasWithOnlySingleDigitDistricts(cls, postcode):
        impacted_by_rule = False
        if postcode.outward_district >= 10:
            single_digit_districts = cls.AreasWithOnlySingleDigitDistricts
            impacted_by_rule = postcode.outward_area in single_digit_districts
        return impacted_by_rule
                


    ## Areas that only have double digit districts (ignoring sub-divisions)
    #  @remarks loaded from JSON file 'standard_postcode_validator.json'
    AreasWithOnlyDoubleDigitDistricts = []
        
    ## Checks if a postcode is in an area with only double digit districts and 
    #  if so - that the district specified has two digits as required.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckAreasWithOnlyDoubleDigitDistricts(cls, postcode):
        impacted_by_rule = False
        if postcode.outward_district <= 9:
            double_digit_districts = cls.AreasWithOnlyDoubleDigitDistricts
            impacted_by_rule = postcode.outward_area in double_digit_districts
        return impacted_by_rule
                


    ## Areas that have a district zero.
    #  @remarks loaded from JSON file 'standard_postcode_validator.json'
    AreasWithDistrictZero = []
        
    ## Checks if a postcode has a district zero if it specified one.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckAreasWithDistrictZero(cls, postcode):
        impacted_by_rule = False
        if postcode.outward_district == 0:
            areas_with_district_zero = cls.AreasWithDistrictZero
            impacted_by_rule = not postcode.outward_area in areas_with_district_zero
        return impacted_by_rule



    ## Areas that do not have a district 10
    #  @remarks loaded from JSON file 'standard_postcode_validator.json'
    AreasWithoutDistrictTen = []
        
    ## Checks if a postcode has a district ten if it specified one.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckAreasWithoutDistrictTen(cls, postcode):
        impacted_by_rule = False
        if postcode.outward_district == 10:
            areas_without_district_ten = cls.AreasWithoutDistrictTen
            impacted_by_rule = postcode.outward_area in areas_without_district_ten
        return impacted_by_rule



    ## Only a few areas have subdivided districts
    #  @remarks loaded from JSON file 'standard_postcode_validator.json'
    AreasWithSubdistricts = {}

    ## If a postcode has subdistricts, check its supposed to.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckAreasWithSubdistricts(cls, postcode):
        impacted_by_rule = False
        if postcode.outward_subdistrict:
            areas_with_subdistricts = cls.AreasWithSubdistricts
            impacted_by_rule = not postcode.outward_area in areas_with_subdistricts
            if not impacted_by_rule:
                subdivided_districts_in_area = areas_with_subdistricts[postcode.outward_area]
                if subdivided_districts_in_area:
                    impacted_by_rule = not postcode.outward_district in subdivided_districts_in_area
        return impacted_by_rule

    ## If a postcode has a limited selection of subdistricts, makes sure any set are in scope.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckAreasWithSpecificSubdistricts(cls, postcode):
        impacted_by_rule = False
        if postcode.outward_subdistrict:
            areas_with_subdistricts = cls.AreasWithSubdistricts
            subdivided_districts_in_area = areas_with_subdistricts.get(postcode.outward_area, {})
            specific_subdistrict_codes = subdivided_districts_in_area.get(postcode.outward_district, None)
            impacted_by_rule = specific_subdistrict_codes and \
                not postcode.outward_subdistrict in specific_subdistrict_codes
        return impacted_by_rule



    #  @remarks loaded from JSON file 'standard_postcode_validator.json'
    FirstPositionExcludes = []
    
    ## Checks that a postcode does not include reserved characters in the first postition.
    #  @param cls the type of class that is invoking this method.
    #  @param postcode the postcode to check for conformance to this rule.
    #  @returns True if the postcode violates this rule, else False.
    @classmethod
    def CheckFirstPositionExcludes(cls, postcode):
        first_postion_char = postcode.outward_area[0]
        impacted_by_rule = first_postion_char in cls.FirstPositionExcludes
        return impacted_by_rule


## Loads various static members used for validation of standard postcodes from
#  a JSON file - this is expected to be co-located with this class.
def load_validator_params_from_json():
    
    from json import load
    from os.path import dirname, join
    
    json_configuration_file = join( dirname(__file__), "standard_postcode_validator.json" )
    
    with open(json_configuration_file, 'r') as file_handle:
        config_json = load(file_handle)

    subdivision_map = config_json["subdivided-districts"]

    StandardPostcodeValidator.AreasWithOnlySingleDigitDistricts = config_json['single-digit-districts']
    StandardPostcodeValidator.AreasWithOnlyDoubleDigitDistricts = config_json['double-digit-districts']
    StandardPostcodeValidator.AreasWithDistrictZero = config_json['has-district-zero']
    StandardPostcodeValidator.AreasWithoutDistrictTen = config_json['no-district-ten']
    StandardPostcodeValidator.AreasWithSubdistricts = {  k: { 
        int(k1): v1 for k1, v1 in v.items()
    } for k, v in subdivision_map.items() }
    StandardPostcodeValidator.FirstPositionExcludes = config_json['first-position-excludes']


load_validator_params_from_json()