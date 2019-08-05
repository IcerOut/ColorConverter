"""

ColorConverter
@author: Lung Alin-Sebastian

"""
import random
import re
from collections import namedtuple

from colour import Color

from src.exceptions import InvalidColorError

ConvertedColor = namedtuple('ConvertedColor', 'name hex rgb hsl')

# noinspection SpellCheckingInspection
COLOR_NAMES = ('black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'darkcyan',
               'deepskyblue', 'darkturquoise', 'mediumspringgreen', 'lime', 'springgreen', 'cyan',
               'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen',
               'darkslategray', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue',
               'steelblue', 'darkslateblue', 'mediumturquoise', 'indigo', 'darkolivegreen',
               'cadetblue', 'cornflowerblue', 'mediumaquamarine', 'dimgray', 'slateblue',
               'olivedrab', 'slategray', 'lightslategray', 'mediumslateblue', 'lawngreen',
               'chartreuse', 'aquamarine', 'maroon', 'purple', 'olive', 'gray', 'lightslateblue',
               'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown',
               'darkseagreen', 'lightgreen', 'mediumpurple', 'darkviolet', 'palegreen',
               'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'lightblue',
               'greenyellow', 'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick',
               'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver',
               'mediumvioletred', 'indianred', 'peru', 'violetred', 'chocolate', 'tan', 'lightgray',
               'thistle', 'orchid', 'goldenrod', 'palevioletred', 'crimson', 'gainsboro', 'plum',
               'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'lightgoldenrod',
               'palegoldenrod', 'lightcoral', 'khaki', 'aliceblue', 'honeydew', 'azure',
               'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon',
               'antiquewhite', 'linen', 'lightgoldenrodyellow', 'oldlace', 'red', 'magenta',
               'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 'lightsalmon',
               'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin',
               'bisque', 'mistyrose', 'blanchedalmond', 'papayawhip', 'lavenderblush', 'seashell',
               'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory',
               'white')


def _replace_separators(string: str) -> str:
    """
    Replaces the separators ' ', ',' and ', ' with '*'
    :param string: The input string containing the separators
    :return: A string with the separators replaced by '*'
    """
    return string.replace(', ', '*').replace(',', '*').replace(' ', '*')


def _format_name(name: str) -> str:
    """
    Formats the color name to start with capital letters and have spaces where necessary
    :param name: The original name color
    :return: The formatted name color
    """
    name = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
    return name.title()


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


def _identify_and_create_object(user_input: str) -> Color:
    """
    Identifies the data type of an input, converts it appropriately and creates the Color() object
    :param user_input: The input string from the input textbox
    :return: A Color object that corresponds to the user input
    :raises InvalidColorError: if the inputted color doesn't fit any of the available formats
    """
    result = Color()

    # Checks for literal color names
    tmp = re.sub(r"[^a-zA-Z]+", "", user_input.lower())
    if tmp in COLOR_NAMES:
        result = Color(tmp)
        print(f'\nDetected literal: {tmp}')
        return result

    # Matches a hex color without the '#' sign
    hex_without_pound_sign_pattern = re.compile(r'[A-Fa-f0-9]{6}')
    if hex_without_pound_sign_pattern.match(user_input) and len(user_input) == 6:
        result.set_hex_l('#' + user_input.lower())
        print("\nDetected hex without '#'...")
        return result

    # Matches a hex color with the '#' sign
    hex_with_pound_sign_pattern = re.compile(r'#[A-Fa-f0-9]{6}')
    if hex_with_pound_sign_pattern.match(user_input) and len(user_input) == 7:
        result.set_hex_l(user_input.lower())
        print("\nDetected hex with '#'...")
        return result

    # Matches an RGB color (3x 1-3 digits numbers, separated by up to 2 of ',' and ' ')
    rgb_pattern = re.compile(r'(?:[0-9]{1,3}[, ]{1,2}){2}[0-9]{1,3}')
    if rgb_pattern.match(user_input):
        user_input = _replace_separators(user_input)
        r_value, g_value, b_value = [int(val) for val in user_input.split('*')]

        if not 0 <= r_value <= 255 or not 0 <= g_value <= 255 or not 0 <= b_value <= 255:
            raise InvalidColorError(
                    'This looks like an RGB color but the values are not in the 0-255 range!')
        result.set_rgb((r_value / 255, g_value / 255, b_value / 255))
        print(f"\nDetected rgb: {user_input}")
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
        result.set_hsl((h_value / 360, s_value, l_value))
        print(f"\nDetected hsl: {user_input}")
        return result

    raise InvalidColorError("The input doesn't fit any of the known color patterns!")


def convert(user_input: str) -> ConvertedColor:
    """
    Takes a the user input and converts it into a ConvertedColor namedtuple
    :param user_input: The input string from the input textbox
    :return: A ConvertedColor namedtuple
    """

    # Strips left and right spacing from the user input
    user_input = user_input.lstrip().rstrip()

    color = _identify_and_create_object(user_input)

    name_value = _format_name(color.get_web()) if not color.get_web().startswith('#') else None
    hex_value = color.get_hex_l().upper()
    rgb_value = ', '.join([str(int(nr * 255)) for nr in color.get_rgb()])
    hsl_value = ', '.join([str(int(color.get_hsl()[0] * 360)),
                           str(int(round(color.get_hsl()[1], 2) * 100)) + '%',
                           str(int(round(color.get_hsl()[2], 2) * 100)) + '%'])

    return ConvertedColor(name_value, hex_value, rgb_value, hsl_value)


def random_color() -> str:
    """
    Returns a random color (in any of the 4 formats)
    :return: A random color as a string
    """
    color_format = random.choice(('name', 'hex', 'rgb', 'hsl'))
    if color_format == 'name':
        return random.choice(COLOR_NAMES)
    elif color_format == 'hex':
        return '#' + ''.join((random.choice("0123456789ABCDEF") for _ in range(6)))
    elif color_format == 'rgb':
        return ', '.join(str(random.randrange(0, 255)) for _ in range(3))
    else:
        return f'{str(random.randrange(0, 360))}, {str(random.randrange(0, 100))}%,' \
               f' {str(random.randrange(0, 100))}%'
