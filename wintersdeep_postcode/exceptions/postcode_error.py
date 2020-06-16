## A simple class to act as a base for all postcode related errors
#  @remarks this is to allow users to "catch" all generic postcode exceptions.
class PostcodeError(ValueError):

    ## Creates a new instance of the postcode error
    #  @param self the instance of the object invoking this method.
    #  @param args the postional arguments supplied to this method.
    #  @param kwargs the keyword arguments supplied to this method.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)