"""

ColorConverter
@author: Lung Alin-Sebastian

"""

import configparser
import gettext
from collections import Callable

import globals as global_var
from globals import CONFIG_FILE


def read_config() -> None:
    """
    Reads the config file and sets the LANGUAGE global variable
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    print('Loading language...', end=' ')
    try:
        global_var.LANGUAGE = config['APPLICATION_SETTINGS']['language']
        print(f'Language set to {global_var.LANGUAGE}.')
    except KeyError:
        global_var.LANGUAGE = 'en'
        print('Config file missing or misconfigured! Defaulting to English.')


def get_language_func(lang: str) -> Callable:
    """
    Sets the application to the given language
    :param lang: the language code. Can be 'en', 'ro' or 'fr'
    """
    if lang == 'en':
        return lambda s: s
    lang_file = gettext.translation('gui', localedir='locale', languages=[lang])
    lang_file.install()
    return lang_file.gettext
