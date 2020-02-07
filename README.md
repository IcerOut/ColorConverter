
# ColorConverter

ColorConverter is a desktop application that converts between the various color formats (hex, RGB, HSL), providing the X11 color name when available and a sample of the given color.

![GUI Example](https://i.imgur.com/dWV6WQQ.png)
---

## Requirements

* Python >=3.6
* Python [colour module](https://pypi.org/project/colour/) >= 0.1.5
* Python [configparser module](https://pypi.org/project/configparser/) >= 4.0.2

---

## Usage

Run using the src/main.py file (python main.py from the CLI).
The input box takes input in one of the following formats:
* X11 standard color name (with or without spaces, any capitalization)
* Long hex code ( '#' is optional)
* RGB code (3 numbers 0-255, separated by comma or space)
* HSL code (1 number 0-360 and 2 percentages (35% or 0.35), separated by comma or space)

**These instructions are also available at any time by pressing F1 or entering the Help>Show Help menu.**

Clicking the 'Generate random color' button will produce various valid inputs (in any of the input formats).
![Example input](https://i.imgur.com/hEDHyY9.png)
Clicking on any of the output fields copies the content of that field to the clipboard (for the RGB and HSL outputs, it copies with the correct CSS function syntax, ready to use.
![Clipboard example](https://i.imgur.com/IUlgS6f.png)
The 'Generate complementary color' will generate the complement of the currently entered color.

---

The interface is available in English and Romanian (French coming soon). This can be changed from the File>Change Language menu, and requires a restart to take effect.

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE.md file for more details
