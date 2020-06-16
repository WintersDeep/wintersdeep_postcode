# WintersDeep Postcode
This is a Python3 library for parsing, heuristically validating, and formatting a postcode from, or associated with, the United Kingdom. The library makes use of information, rules and observations detailed on the “[Postcodes in the United Kingdom](https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom)” Wikipedia page. The results of using this library are never going to be 100% conclusive as this would require checking input against a definitive database of all active postcodes, but does act as a good 	*“at a glance”* check.

The library provides the following features:

 - Parses a string into an postcode object.
 - Performs heuristic validation of a postcode object.
 - Supports standard postcodes, british forces post office (BFPO) postcodes, and “special cases”.
 - Is flexible in its operation, tolerance, and configuration.
 - Is extensible to future use cases.
 - Dependency free.
  
 ## Library Usage
 This library can be used in a number of ways, with the most common being presented below.
  ### The Quick and Ugly (parse_postcode)
 This is just two lines, including the import - its the simplist interface to the library and takes no other arguments than the postcode that needs to be converted. 
 
**NOTE**: This method will throw if the postcode does not parse or validate, so you might want some error handling in there.  
 
    # import the library into your script.
    from wintersdeep_postcode import parse_postcode
    
    # parse your objects.
    postcode_obj = parse_postcode(“N1C 4DN”)
    
    # use your object...
    print( postcode_obj )          # ‘N1C 4DN’
	print( postcode.outward_code ) # ‘N1C’
	print( postcode.inward_code)   # ‘4DN’
	print( postcode.area )         # ‘N’
	print( postcode.district )     # 1
	print( postcode.subdistrict )  # ‘C’
	print( postcode.sector )       # 4
	print( postcode.unit)          # ‘DN’
	print( postcode.is_validated)  # True
	print( postcode.postcode_type) # ‘standard’

### The Quick and Dirty (try_parse_postcode)
Don’t want the hassle of dealing with error handling? No judgements. Use `try_parse_postcode` instead. This method accepts two additional, optional arguments:

 - `default_value` *(default; None)*. The value to return when the postcode string either does not parse, or (optionally) does not validate.
 - `ignore_validation_errors` *(default; False)*. When True, a postcode which parsed, but didn’t validate, will still be returned - you can check the returned objects `validation_faults` map/dict for more details if you care. Otherwise, when False, postcode strings that parse, but dont validate, will return the `default_value`.

This would look a little like this:

    # import the library into your script.
    from wintersdeep_postcode import try_parse_postcode
    
    # parse your objects.
    postcode_obj = try_parse_postcode(“N1C 4DN”, None, False)
    
    # use your postcode object...
    
### The Right Way 
The final example demonstrates an implementation of with the library used as it was anticipated. In this setup, you instance the parser object and invoke it. This gives the advantage of being able to configure the way in which the parser operates. More details on this are provided below.

    # import the parser and base error
    from wintersdeep_postcode import PostcodeParser, PostcodeError
    
    # set an parser options you want to set, and create a parser instance
    parser_options = {}
    parser_obj = PostcodeParser(**parser_options)
    
    try:
        # parse the postcode, and do your thing...
        postcode_obj = parser_obj(postcode_string)
    except PostcodeError as ex:
        # handle any errors 
        print( str(ex) )

As mentioned, this is preferred as it allows you to configure how the parser behaves to best meet your use case. This is done by passing keyword arguments to the `PostcodeParser` constructor. It accepts the following keyword arguments:
|Keyword|Default|Description|
|--|--|--|
|whitespace  |”tolerant”  | Determines how the parser handles the whitespace which separates the outward and inward codes (the two groups of alpha-numeric strings in a normal postcode). Options are “*lenient*” (zero or more characters of any whitespace type), “*tolerant*” (either no whitespace, or a single space character), and “*strict*” (a single space character only).|
|force_case| `True` |When `True`, input will be converted to uppercase, otherwise the input case will not be altered. Postcodes are expected to be uppercase else they will not parse.|
|trim_whitespace|`True`|When `True` leading or following whitespace will be removed from the input, otherwise the input will not be altered. Postcodes with leading or trailing whitespace will not parse.|
|postcode_types|`None`|A list/array of strings identifying the types of postcode the parser should support in priority order. If two postcodes types would recognise an input, the first in this list will be the one selected to handle the input. If `None` (the default) all postcode types will be parsed in the following order “special”, “forces”, “standard”. Supported types are “*standard*” (Standard UK postcodes), “*forces*” (British Forces Post Office), and “*special*” (Special cases).|
|validate|`True`|When `True` the parser may attempt to use heuristic validation rules to determine whether or not the given postcode appears to be genuine. If a postcode fails validation, then the parser will raise a `ValidationError`, which will detail why the postcode is being rejected. If `False`, then the parser will only attempt to extract a postcode, but will not attempt to validate it. |
|ignore_faults|`[]`|A list/array, containing the integer identifiers of any validation faults that you want to ignore. By default this is empty (the parser is ignoring no faults); if an ID value is added to this, and a fault of the corresponding type is noted when validating a postcode then the parser will not throw an exception (unless of course, other faults are noted which are not ignored). The fault ID/description will still however appear in the returned postcodes `validation_faults` member. If the parse is not set to validate postcodes, this setting has no effect.|

## Parsing Bad or Tainted Input 
This library has been designed with bad input in mind. It offers a number of options (such as auto-casing, trimming and varying whitespace tolerance) to handle adverse input. That said some things just don’t work out, and this library communicates bad input using exceptions. This will come in one of two scenarios: 

- The given input does not parse; it structurally does not match any supported and loaded postcode type. In this scenario the library will raise a `ParseError`.
 - The given input did parse, and was passed onto a postcode type handler where it failed validation. If validation is enabled, and the validation rule is not ignored, in this scenario the library will raise a `ValidationError`.
 
Both of these error types derive from `PostcodeError`, which itself is a simple wrapper for `ValueError` (if you wanted a more generic exception type to catch).

All errors use `gettext` so should support localisation (although this has not been tested, or actually used so...)

### Parsing Errors (ParseError) 
`ParseError` does not tell you a lot; all it knows is that the input does not appear to match any of the postcode types loaded, and using the current whitespace rules. Fundamentally this is says “*the postcode didn’t match any of the regular expressions I am looking for.*”

The `ParseError` object has two useful properties; `source_input`, which contains the input we tried to match (this may differ from the original input as it will have been transformed in line with the casing and trimming rules of the parser); and `source_parser`, the parser that is raising the exception.

### Validation Errors (ValidationError)
`ValidationErrors` tell you why a postcode isn’t considered valid - and it tells you exactly why it thinks the a given postcode is not valid.

`ValidationErrors` have two useful properties; `postcode`, the actual postcode object that was parsed (and is failing validation), in case you still want to use or examine it; and `faults`, a map/dict of all the reasons it is suspected to not be valid.

Keys in the `faults` map are the error ID numbers associated with the given fault, and values are a human readable description of the fault.

### Having Validation Problems?
Hopefully this shouldn’t happen (one of the tests, if you have the file, literally runs every standard UK postcode through the parser, and several special cases / BFPO). However, the rules we have are based on observations of the real data; just because area LL only has double digit districts today, doesn’t mean district LL2 wont be allocated tomorrow. A good example of this is that Wikipedia currently lists SR as a single digit district area, but SR43 was allocated in 2019.

You have options:

 - **Fix the rules** - while the rules are defined and handled in code, most are configured in JSON. For example, the configuration for each standard postcodes validation rule is stored in `./postcode_types/standard_postcode/standard_postcode.json`. You don’t need to understand Python or this library to tinker there.
 - **Ignore the validation fault** - grab the ID of the validation fault that is troubling you and add it to the ignore_faults PostcodeParser keyword arguments.
 - **Disable validation** - for the all or nothing guys/girls. Disable validation entirely. But seriously, use one of the above options.

## Custom Special Cases
Whether its one that was missed, or you need to implement your own one - its not a problem. Special cases don’t need to follow any rules (don’t want an inward code, or want to use three blocks... fine)

You’ll need to use `SpecialCase` from `./postcode_types/special_case_postcode/special_case.py`

You have two options for creating a custom special case:

 - You can programmatically create one; take a look at you just need to instance a `SpecialCase` object and fill out its members.
 - You can create one from a JSON string; either directly loaded in the software using `SpecialCase.FromJsonString` or from a file via `SpecialCase.FromJsonFile`. The recommendation would be to add your special case to the default special case directory `./postcode_types/special_case_postcode/special_cases` as it will then be automatically loaded without any other changes. 

The following properties need to be defined in either JSON or the object:
|Property| Type | Description |
|--|--|--|
| identifier| str | a unique string that identifies this special case. it must be alpha-numeric (basically be suitable for a regular expression group label). |
| patterns | list | A list of patterns used to match this special case. Each pattern can itself either be a raw string, explicitly setting the postcode string in its strict form - or an array, describing each part of the postcode (example: “GIR 0AA” and [“GIR”, “0AA”] are equivalent). When using the array syntax it is safe to use regular expression syntax, however care must be taken that any group expression used is non-capturing. This list must have at least one value.|
|examples|list|A list of strings that give valid examples of this special case. This is used for testing purposes.

## Donations, Licence and Farewell.
If this library saved you some time, or makes you some pennies and you are so inclined any donation is obviously gratefully received, but you are under absolutely no obligation to do so.

You are free to use this library in any capacity that is in accordance with the MIT licence that accompanies the project. That should cover most use cases.

If you have a cool use-case, or application, I’m always glad to hear about it - its always interesting to hear where your code ends up. If you need some help adapting the library to your use case, feel free to drop me an email. I cant promise I’ll be able to get back to you quickly - life’s busy, you know the deal, but I’ll try.