# python3 imports
from gettext import gettext as _
from wintersdeep_postcode.exceptions.postcode_error import PostcodeError

## Postcode Validation error
#  Raised when a postcode fails to validate.
class ValidationError(PostcodeError):
    
    ## Creates a new instance of the validation error object.
    #  @param self the instance of the object that is invoking this method.
    #  @param postcode the postcode that failed validation.
    #  @param validation_faults a map of one or more reasons that the validation failed.
    #  @remarks the map should contain error_id => error_message pairs.
    def __init__(self, postcode, validation_faults = {}):
        localised_message = _(fr"'%s' failed validation with %i faults.")
        formatter_arguments = ( str(postcode), len(validation_faults.items())  )
        super().__init__( localised_message % formatter_arguments)
        self.faults = validation_faults
        self.postcode = postcode

    ## Converts this error message into a simple string.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the error message as a string suitable for user consumption.
    def __str__(self):
        return " ".join([ 
            super().__str__(), 
            *self.faults.values() 
    ])

if __name__ == "__main__":
    
    ##
    ##  If this is the main entry point - someone might be a little lost?
    ##

    print(f"{__file__} ran, but doesn't do anything on its own.")
    print(f"Check 'https://www.github.com/wintersdeep/wintersdeep_postcode' for usage.")