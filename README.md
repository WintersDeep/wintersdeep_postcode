# WintersDeep Postcode
[![Build Status](https://travis-ci.org/WintersDeep/wintersdeep_postcode.svg?branch=development)](https://travis-ci.org/WintersDeep/wintersdeep_postcode)

This is a Python3.6+ library for parsing, heuristically validating, and formatting a British postcode. The library makes use of information, rules and observations detailed on the “[Postcodes in the United Kingdom](https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom)” Wikipedia page. The validation offered by this library is never going to give 100% certainty as this would require checking input against a definitive database of all active postcodes. This is currently not supported by the library. However it does provide a good  *“at a glance”* check.

The library provides the following features:

 - Parses a string into an postcode object.
 - Performs heuristic validation of a postcode object.
 - Supports standard postcodes, BFPO postcodes, and “special cases”.
 - Is flexible in its operation, tolerances, and configuration.
 - Is extensible to future use cases.
 - Is dependency free.

## Table of Contents
 - [Library Usage](#library-usage)
   - [The Quick and Ugly (parse_postcode)](#the-quick-and-ugly-parse-postcode)
   - [The Quick and Dirty (try_parse_postcode)](#the-quick-and-dirty-try-parse-postcode)
   - [The "Right" Way](#the-right-way) 
 - [PostcodeParser Options](#postcodeparser-options)
 - [Parsing Bad or Tainted Input](#parsing-bad-or-tainted-input) 
   - [Parsing Errors (ParseError)](#parsing-errors-parseerror) 
   - [Validation Errors (ValidationError)](#validation-errors-validationerror)
   - [Having Validation Problems?](#having-validation-problems)
 - [Custom Special Cases](#custom-special-cases)
 - [Licence and Farewell](#licence-and-farewell)
  
## Library Usage
 This library can be used in your code using a number of interfaces; the best choice will dependion your use case and requirements.

### The Quick and Ugly (parse_postcode)
 This is the libraries simplist interface. You just need to import the function and pass it the postcode string you want to parse. It takes no other arguments and will throw a `PostcodeError` is something isn't right.
 
**NOTE**: This example does not implement any error handling, you might want to.
 
 ```python
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
```

### The Quick and Dirty (try_parse_postcode)
If you don’t want the hassle of dealing with error handling; we won't judge you. Use `try_parse_postcode` instead. This method accepts two additional, optional arguments:

 - `default_value` *(default; None)*. The value to return when the postcode string either does not parse, or (optionally) does not validate.
 - `ignore_validation_errors` *(default; False)*. When `True`, a postcode which parsed, but didn’t validate, will still be returned - you can check the returned objects `validation_faults` property for more details if you really care. Otherwise, when `False`, postcode strings that parse, but dont validate, will return the value specified by the `default_value` argument.

A quick example of this might look like:
```python
# import the library into your script.
from wintersdeep_postcode import try_parse_postcode
    
# parse your objects.
postcode_obj = try_parse_postcode(“N1C 4DN”, None, False)
    
# use your postcode object...
```

### The "Right" Way 
The final example demonstrates an implementation of with the library used as it was anticipated. You instance the `PostcodeParser` object and invoke it. This gives the advantage of being able to configure the way in which the parser operates. More details on the exact options available are provided below the code sample, which for simplicity will just use the defaults.

```python
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
```

## PostcodeParser Options
You can configure the behaviour of the `PostcodeParser` object by passing arguments to its constructor when you create it. This should allow you to ensure the parser behaves in a manner that best suits your use case. 

It accepts the following keyword arguments:

|Keyword|Default|Description|
|--|--|--|
|whitespace  |”tolerant”  | Determines how the parser handles the whitespace which separates the outward and inward codes (the two groups of alpha-numeric strings in a normal postcode). Options are “*lenient*” (zero or more characters of any whitespace type), “*tolerant*” (either no whitespace, or a single space character), and “*strict*” (a single space character only).|
|force_case| `True` |When `True`, input will be converted to uppercase, otherwise the input case will not be altered. Postcodes are expected to be uppercase else they will not parse.|
|trim_whitespace|`True`|When `True` leading or following whitespace will be removed from the input, otherwise the input will not be altered. Postcodes with leading or trailing whitespace will not parse.|
|postcode_types|`None`|A list/array of strings identifying the types of postcode the parser should support in priority order. If two postcodes types would recognise an input, the first in this list will be the one selected to handle the input. If `None` (the default) all postcode types will be parsed in the following order “special”, “forces”, “standard”. Supported types are “*standard*” (Standard UK postcodes), “*forces*” (BFPO postcodes, including mail sent to the BF area), and “*special*” (Special cases).|
|validate|`True`|When `True` the parser may attempt to use heuristic validation rules to determine whether or not the given postcode appears to be genuine. If a postcode fails validation, then the parser will raise a `ValidationError`, which will detail why the postcode is being rejected. If `False`, then the parser will only attempt to extract a postcode, but will not attempt to validate it. |
|ignore_faults|`[]`|A list/array, containing the integer identifiers of any validation faults that you want to ignore. By default this is empty (the parser is ignoring no faults); if an ID value is added to this, and a fault of the corresponding type is noted when validating a postcode then the parser will not throw an exception (unless of course, other faults are noted which are not ignored). The fault ID/description will still however appear in the returned postcodes `validation_faults` member. If the parse is not set to validate postcodes, this setting has no effect.|

## Parsing Bad or Tainted Input 
This library has been designed with bad input in mind. It offers a number of options such as auto-casing, trimming, and varying whitespace tolerance to handle adverse input. That said some things just don’t work out. This library communicates bad input using exceptions.

The library throws two types of error in response to bad input: 

- The library will raise a `ParseError`  when the given input does not parse; it structurally does not match any supported and loaded postcode type.
- The library will raise a `ValidationError` when input does parse, but fails validation. This exception will not occur if validation is disabled, or the validation rule was added to the parsers ignored faults list (`ignore_faults`).
 
Both of these error types derive from `PostcodeError`, which itself is a simple wrapper for `ValueError`. Either of these can therefor be used if you want to catch both faults in a single exception handler using a simple generic type.

All error messages and validation fault string use `gettext` so should support localisation (although this has not been tested, or actually used so...)

### Parsing Errors (ParseError) 
`ParseError` does not tell you a lot; all it knows is that the input does not appear to match any of the postcode types loaded, using the current whitespace rules. Fundamentally this is saying “*the postcode didn’t match any of the regular expressions I am looking for.*”

The `ParseError` object has two additional properties; `source_input`, which contains the input we tried to match (this may differ from the original input as it may have been transformed in accordance with the casing and trimming rules of the parser); and `source_parser`, the parser that is raising the exception.


### Validation Errors (ValidationError)
`ValidationError` objects tells you a postcode isn’t considered valid - and it'll tell you exactly why the parser rejected it.

A `ValidationError` object has two additional properties; `postcode`, which is the actual postcode object that was parsed, and is failing validation; and `faults`, which is a `dict` of all the reasons it is suspected to not be valid.

Keys in the `faults` map are an ID number associated with the given type of validation fault, and values are a human readable description of what that fault code means in relation to the parsed postcode.

### Having Validation Problems?
Hopefully this shouldn’t happen. However, perhaps you don't agree with a rule, or a postcode you know is valid isn't being accepted. The rules implemented in this library are based on observations of a the real data, and the real data just isn't static, so this might happen. For example Wikipedia currently lists SR as an area that only has single digit districts, but SR43 was allocated in 2019.

So what are your options if you are in this position?

 - **Fix the rules** - while the rules are defined and handled in code, most are configured in JSON. For example, the configuration for each standard postcodes validation rule is stored in [`standard_postcode_validator.json`](https://github.com/WintersDeep/wintersdeep_postcode/blob/development/wintersdeep_postcode/postcode_types/standard_postcode/standard_postcode_validator.json). You don’t need to understand Python or this library to tinker there.
 - **Ignore the validation fault** - grab the ID number of the validation fault that is troubling you and add it to the `ignore_faults` argument passed to the `PostcodeParser` constructor. The fault will still appear in the objects `validation_faults` member, but it will not raise a `ValidationError` when parsing any more.
 - **Disable validation** - the option for the all or nothing guys/girls. Disable validation entirely; but seriously, use one of the above options.
## Custom Special Cases
Whether its one that was missed, or you need to implement your own one - its not a problem. Special cases don’t need to follow any rules (don’t want an inward code, or want to use three alpha-numeric groups instead of two... fine)

You have two options for creating a custom special case:

 - You can programmatically create one; take a look at the [`SpecialCase`](https://github.com/WintersDeep/wintersdeep_postcode/blob/development/wintersdeep_postcode/postcode_types/special_case_postcode/special_case.py) object. Creating one will automatically add it to the list of known special cases - you just need to set some properties, which are described below.
 - You can create one from a JSON string; either directly in your software using `SpecialCase.FromJsonString` or from a file via `SpecialCase.FromJsonFile`. If you are able to load it from file, the recommendation would be to add your JSON to the [special_cases directory](https://github.com/WintersDeep/wintersdeep_postcode/tree/development/wintersdeep_postcode/postcode_types/special_case_postcode/special_cases) as it will then be automatically loaded when the library starts without any other code changes. 

The following properties need to be defined in either JSON file or object:

|Property| Type | Description |
|--|--|--|
| `identifier`| `str` | a unique string that identifies this special case. it must be alpha-numeric (basically be suitable for a regular expression group label). |
| `patterns` | `list` | A list of patterns used to match this special case. Each pattern can itself either be a raw string, explicitly setting the postcode string in its strict form - or an array, describing each part of the postcode (example: “GIR 0AA” and [“GIR”, “0AA”] are equivalent). When using the array syntax it is safe to use regular expression syntax, however care must be taken that any group expression used is non-capturing. This list must have at least one value.|
|`examples`|`list`|A list of strings that give valid examples of this special case. This is used for testing purposes.

## Licence and Farewell
You are free to use this library in any capacity that is in accordance with the [MIT licence](https://github.com/WintersDeep/wintersdeep_postcode/blob/development/LICENSE) that accompanies the project. That should cover most use cases.

If you have a cool use-case, or application, I’m always glad to hear about it - its always interesting to hear where your code ends up. If you need some help adapting the library to your use case, feel free to drop me an email. I cant promise I’ll be able to get back to you quickly - life’s busy, you know the deal, but I’ll try.