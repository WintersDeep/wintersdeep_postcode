## A reason that a postcode is invalid.
class ValidationFault(object):

    ## A map of identifier to validation fault
    #  @remarks ID's are loaded into this map when they are instanciated.
    Map = {}
    
    ## Creates a new instance of the validation fault object.
    #  @param self the instance of the object that is invoking this method.
    #  @param fault_id the unique identifier this validation fault.
    #  @param description_string a string that describes the fault.
    def __init__(self, fault_id, description_string):

        if fault_id in ValidationFault.Map:
            other_description = ValidationFault.Map[fault_id].description
            fault_message = fr"Validation fault #{fault_id} is already allocated to '{other_description}'."
            raise ValueError(fault_message)

        ValidationFault.Map[fault_id] = self

        self.description = description_string
        self.id = fault_id

    ## Gets the integer equivolent of this object.
    #  @param self the instance of the object that is invoking this method.
    #  @returns the fault identifier assigned to this object.
    def __int__(self):
        return self.id

    ## Returns a simple string representation of this object.
    #  @param self the instance of the object that is invoking this method.
    #  @returns a string representation of the object suitable for user consumption.
    def __str__(self):
        return self.description

if __name__ == "__main__":

    ##
    ## If this file is the main entry point - run tests
    ##

    from unittest import TextTestRunner, defaultTestLoader
    from validation_fault_tests import TestValidationFault

    print( f"Running ValidationFault unit tests...")

    test_runner = TextTestRunner()
    test_loader_fn = defaultTestLoader.loadTestsFromTestCase
    unit_tests = test_loader_fn(TestValidationFault)
    test_runner.run( unit_tests)