# script calls on validation script which then runs the scope parser

from validate import validation
import sys

from colorama import Fore
from colorama import Style

# call validator, which then calls scope parser
# stop everything (crawls), raise an error
# ask the user to try again

if len(sys.argv) == 1:
    print("no file arguements passed")
    raise Exception(Fore.RED + "no file arguments passed" + Style.RESET_ALL)
    # sys.exit()
else:
    try:
        validation(sys.argv[1])  # pass into the validation function
    except Exception:
        raise
