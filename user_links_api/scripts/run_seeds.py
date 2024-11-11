import sys
sys.path = ["", ".."] + sys.path[1:]
import django
django.setup()
from core.loggers import logger
from core.scripts import perform


script_names = ('admins',)

PERFORM_FUNC_NAME = "perform"
SCRIPTS_PATH = "scripts.seeds"


if __name__ == "__main__":
    try:
        perform(sys.argv, SCRIPTS_PATH, script_names, PERFORM_FUNC_NAME, True)
    except IndexError:
        logger.error("Pass script name to to arguments")
