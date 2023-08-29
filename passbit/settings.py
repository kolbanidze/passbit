from locale import getlocale, windows_locale
from os import name


def get_os_language() -> str:
    if name == 'posix':
        language = getlocale()[0]
        if language[:2] == 'ru':
            return 'ru'
        else:
            return 'en'
    else:
        import ctypes
        windll = ctypes.windll.kernel32
        if windows_locale[windll.GetUserDefaultUILanguage()][:2] == 'ru':
            return 'ru'
        else:
            return 'en'


VERSION = "0.1.0"
NAME = "PassBit"

# PassBit DataBase
FILE_EXTENSION = ".pbdb"
# PassBit EXport
EXPORT_FILE_EXTENSION = ".pbex"

# Supported languages: 'ru', 'en'
# Values: get_os_language(), ru, en
LANGUAGE = get_os_language()

# Database viewer screen size constants
DB_VIEWER_MIN_WIDTH = 800
DB_VIEWER_MIN_HEIGHT = 400

# Default KDF parameters
DEFAULT_ARGON2ID_TIME_COST = 3
DEFAULT_ARGON2ID_MEMORY_COST = 65536
DEFAULT_ARGON2ID_PARALLELISM = 4
DEFAULT_SALT_SIZE = 8

# Key File Generator URL
THE_CAT_API_URL = "https://api.thecatapi.com/v1/images/search"

# Show 'Update' button in 'Database viewer'
SHOW_UPDATE_BUTTON = False
