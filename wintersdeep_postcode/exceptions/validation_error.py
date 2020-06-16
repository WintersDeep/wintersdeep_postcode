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
    ## If this file is the main entry point - run tests
    ##

    from unittest import TextTestRunner, defaultTestLoader
    from validation_error_tests import TestValidationError

    print( f"Running ValidationError unit tests...")

    test_runner = TextTestRunner()
    test_loader_fn = defaultTestLoader.loadTestsFromTestCase
    unit_tests = test_loader_fn(TestValidationError)
    test_runner.run( unit_tests)