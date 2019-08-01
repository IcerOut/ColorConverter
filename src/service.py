"""

ColorConverter
@author: Lung Alin-Sebastian

"""
import re
from collections import namedtuple

from colour import Color

from src.exceptions import InvalidColorError

ConvertedColor = namedtuple('ConvertedColor', 'name hex rgb hsl')

COLOR_NAMES = [['Black', 'Navy', 'DarkBlue', 'MediumBlue', 'Blue', 'DarkGreen', 'Green', 'DarkCyan',
                'DeepSkyBlue', 'DarkTurquoise', 'MediumSpringGreen', 'Lime', 'SpringGreen', 'Cyan',
                'MidnightBlue', 'DodgerBlue', 'LightSeaGreen', 'ForestGreen', 'SeaGreen',
                'DarkSlateGray', 'LimeGreen', 'MediumSeaGreen', 'Turquoise', 'RoyalBlue',
                'SteelBlue', 'DarkSlateBlue', 'MediumTurquoise', 'Indigo', 'DarkOliveGreen',
                'CadetBlue', 'CornflowerBlue', 'MediumAquamarine', 'DimGray', 'SlateBlue',
                'OliveDrab', 'SlateGray', 'LightSlateGray', 'MediumSlateBlue', 'LawnGreen',
                'Chartreuse', 'Aquamarine', 'Maroon', 'Purple', 'Olive', 'Gray', 'LightSlateBlue',
                'SkyBlue', 'LightSkyBlue', 'BlueViolet', 'DarkRed', 'DarkMagenta', 'SaddleBrown',
                'DarkSeaGreen', 'LightGreen', 'MediumPurple', 'DarkViolet', 'PaleGreen',
                'DarkOrchid', 'YellowGreen', 'Sienna', 'Brown', 'DarkGray', 'LightBlue',
                'GreenYellow', 'PaleTurquoise', 'LightSteelBlue', 'PowderBlue', 'Firebrick',
                'DarkGoldenrod', 'MediumOrchid', 'RosyBrown', 'DarkKhaki', 'Silver',
                'MediumVioletRed', 'IndianRed', 'Peru', 'VioletRed', 'Chocolate', 'Tan',
                'LightGray', 'Thistle', 'Orchid', 'Goldenrod', 'PaleVioletRed', 'Crimson',
                'Gainsboro', 'Plum', 'Burlywood', 'LightCyan', 'Lavender', 'DarkSalmon', 'Violet',
                'LightGoldenrod', 'PaleGoldenrod', 'LightCoral', 'Khaki', 'AliceBlue', 'Honeydew',
                'Azure', 'SandyBrown', 'Wheat', 'Beige', 'WhiteSmoke', 'MintCream', 'GhostWhite',
                'Salmon', 'AntiqueWhite', 'Linen', 'LightGoldenrodYellow', 'OldLace', 'Red',
                'Magenta', 'DeepPink', 'OrangeRed', 'Tomato', 'HotPink', 'Coral', 'DarkOrange',
                'LightSalmon', 'Orange', 'LightPink', 'Pink', 'Gold', 'PeachPuff', 'NavajoWhite',
                'Moccasin', 'Bisque', 'MistyRose', 'BlanchedAlmond', 'PapayaWhip', 'LavenderBlush',
                'Seashell', 'Cornsilk', 'LemonChiffon', 'FloralWhite', 'Snow', 'Yellow',
                'LightYellow', 'Ivory', 'White']]


def _replace_separators(string: str) -> str:
    """
    Replaces the separators ' ', ',' and ', ' with '*'
    :param string: The input string containing the separators
    :return: A string with the separators replaced by '*'
    """
    string.replace(', ', '*')
    string.replace(',', '*')
    string.replace(' ', '*')
    return string


def _transform_percentage(string: str) -> float:
    """
    Takes a percentage ('30%' or '0.3') and returns a float between 0.0 and 1.0
    :param string: The input string
    :return: A float between 0.0 and 1.0
    """
    if '%' in string:
        try:
            val = string[:-1]  # We cut the percent sign
            val = float(val)  # We convert to int
            val = val / 100  # We divide it (to obtain a number in the 0-1 range)
        except (ValueError, TypeError):
            raise ValueError('Not a valid percentage!')

    else:
        try:
            val = float(string)
        except ValueError:
            raise ValueError('Not a valid percentage!')

    return val


def identify_and_create_object(user_input: str) -> Color:
    """
    Identifies the data type of an input, converts it appropriately and creates the Color() object
    :param user_input: The input string from the input textbox
    :return: A Color object that corresponds to the user input
    :raises InvalidColorError: if the inputted color doesn't fit any of the available formats
    """
    result = Color()

    # Checks for literal color names
    if user_input in COLOR_NAMES:
        result = Color(user_input)
        return result

    # Matches a hex color without the '#' sign
    hex_without_pound_sign_pattern = re.compile(r'[A-Fa-f0-9]{6}')
    if hex_without_pound_sign_pattern.match(user_input) and len(user_input) == 6:
        result.hex_l = '#' + user_input.lower()
        return result

    # Matches a hex color with the '#' sign
    hex_with_pound_sign_pattern = re.compile(r'#[A-Fa-f0-9]{6}')
    if hex_with_pound_sign_pattern.match(user_input) and len(user_input) == 7:
        result.hex_l = user_input.lower()
        return result

    # Matches an RGB color (3x 1-3 digits numbers, separated by up to 2 of ',' and ' ')
    rgb_pattern = re.compile(r'(?:[0-9]{1,3}[, ]{1,2}){2}[0-9]{1,3}')
    if rgb_pattern.match(user_input):
        user_input = _replace_separators(user_input)
        r_value, g_value, b_value = [int(val) for val in user_input.split('*')]

        if not 0 <= r_value <= 255 or not 0 <= g_value <= 255 or not 0 <= b_value <= 255:
            raise InvalidColorError(
                    'This looks like an RGB color but the values are not in the 0-255 range!')
        result.rgb = (r_value / 255, g_value / 255, b_value / 255)
        return result

    # Matches a HSL color (1x 1-3 digits number, then 2x percentages or numbers in the range 0-1)
    hsl_pattern = re.compile(r'[0-9]{1,3}(?:[, ]{1,2}(?:[01]\.[0-9]{1,2}|[0-9]{1,3}%)){2}')
    if hsl_pattern.match(user_input):
        user_input = _replace_separators(user_input)
        h_value, s_value, l_value = user_input.split('*')

        h_value = int(h_value)
        if not 0 <= h_value <= 360:
            raise InvalidColorError(
                    'This looks like a HSL color but the Hue value is not in the 0-360 range!')

        try:
            s_value = _transform_percentage(s_value)
            l_value = _transform_percentage(l_value)
        except ValueError:
            raise InvalidColorError('This looks like a HSL color but the Saturation or Lightness '
                                    'are not valid percentages or in the 0.0-1.0 range!')

        if not 0 <= s_value <= 1 or not 0 <= l_value <= 1:
            raise InvalidColorError(
                    'This looks like a HSL color but the Saturation or Lightness values are not '
                    'percentages or in the 0-1 range!')
        result.hsl = (h_value, s_value, l_value)
        return result

    raise InvalidColorError("The input doesn't fit any of the known color patterns!")


def convert_color(color: Color) -> ConvertedColor:
    """
    Takes a Color object and converts it into a ConvertedColor namedtuple
    :param color: The color object
    :return: A ConvertedColor namedtuple
    """
    pass
