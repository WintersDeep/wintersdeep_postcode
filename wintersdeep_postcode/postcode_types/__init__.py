# project imports
from wintersdeep_postcode.postcode_types.standard_postcode.standard_postcode import StandardPostcode

## a list of all supported parsers in order of priority
#  @remarks parser results should be issued from the first parser to both parse, and validate.
postcode_type_objects = [
    StandardPostcode
]

## a list of postcode type identifiers in order of priority.
#  @remarks auto generated from the object list - for reference only.
#  @remarks to translate to an implementation use \ref postcode_type_map
postcode_type_keys = [ cls_.PostcodeType for cls_ in postcode_type_objects ]

## a map for translating a postcode type identifier to an implementation object.
#  @remarks auto generated from the object list - for reference only.
postcode_type_map = { cls_.PostcodeType: cls_ for cls_ in postcode_type_objects }