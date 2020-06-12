# python3 imports
from logging import getLogger, INFO, DEBUG, ERROR, WARN
from argparse import ArgumentParser
from gettext import gettext as _

# project imports
from wintersdeep_postcode.postcode_parser import PostcodeParser
from wintersdeep_postcode.exceptions import ParseError, ValidationError

## Simple CLI interface for the library.
#  @remarks this is useful for testing, debugging and demonstrating how to use the library.
class PostcodeCliApp(object):

    ## Exit code used to return a successful run.
    ExitSuccess = 0

    ## The description of the binary presented on the CLI help message
    Description = _("Simple CLI tool to inspect UK postcodes and test the wintersdeep_postcode library.")

    ## Log levels that can be used when running this application in a meaningful way
    LogLevels = {
        'debug': DEBUG,
        'info': INFO,
        'warn': WARN,
        'error': ERROR
    }

    ## Creates a new instance of the CLI object.
    #  @param self the instance of the object that is invoking this method.
    def __init__(self):
        self.log = getLogger("postcode-cli")
        self.parser = PostcodeParser()

    ## Parses any arguments supplied by the command line interface and returns
    #  them so they can be actioned.
    #  @param argument_list list of arguments to parse, defaults to sys.argv
    #  @returns arguments parsed from the command line.
    @staticmethod
    def GetCliArguments(argument_list=None):
        parser = ArgumentParser(description=PostcodeCliApp.Description)
        parser.add_argument("-l", "--log-level", type=str, choices=PostcodeCliApp.LogLevels.keys(),
            help=_("The log level used for console messages."), default="info")
        parser.add_argument("postcodes", metavar='POSTCODE',  type=str, nargs="+", 
            help=_("The postcode object(s) to attempt to parse and examine."))
        return vars( parser.parse_args(argument_list) )

    ## Main entry point for the application.
    #  @param self the instance of the object that is invoking this method.
    #  @returns exit code returned from the main method.
    def main(self, postcodes):
        
        for postcode in postcodes:
            self.handle_postcode(postcode)

        return PostcodeCliApp.ExitSuccess

    ## Handles inspecting a postcode.
    #  @param self the instance of the object that is invoking this method.
    #  @param postcode the postcode that should be parsed.
    def handle_postcode(self, postcode):
        
        self.log.debug(f"Inspecting input string '{postcode}'...")

        try:
            self.log.info( self.parser(postcode) )
        except ParseError as ex:
            self.log.warning(f"Failed to parse '{postcode}': {ex}")
        except ValidationError as ex:
            self.log.warning(f"Failed to vaidate '{postcode}': {ex}")
        except Exception as ex:
            self.log.error(f"Internal Error handling '{postcode}: {ex}")

if __name__ == "__main__":
    
    # if this is the main entry point (which in this case we generally expect to be the 
    # case) - then we want to run the application.

    from sys import exit
    from logging import basicConfig

    arguments = PostcodeCliApp.GetCliArguments()

    log_level = arguments.pop('log_level')
    postcodes = arguments.pop('postcodes')

    basicConfig(level=PostcodeCliApp.LogLevels[log_level])
    application = PostcodeCliApp(**arguments)
    return_code = application.main(postcodes)

    exit(return_code)