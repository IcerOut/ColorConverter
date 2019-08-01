"""

ColorConverter
@author: Lung Alin-Sebastian

"""


class InvalidColorError(Exception):
    """
    Raised in the case of an invalid color being written in the input.
    Should be caught by the GUI and let the user know of the proper syntax
    """
    pass
