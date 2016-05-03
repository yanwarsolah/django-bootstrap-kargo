LOCAL_SETTINGS = True

from settings import *

CURRENT = os.path.dirname(__file__)

if LOCAL_SETTINGS:
    DEBUG = True

    # anything local changes, please put it here to overwrite main settings.py