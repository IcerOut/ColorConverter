"""

ColorConverter
@author: Lung Alin-Sebastian

"""
import colour
import tkinter as tk

from src.globals import APP_TITLE


class GUI:
    """
    The class responsible for the GUI and all of its associated functions
    """

    def __init__(self, master):
        self.master = master
        self.master.title(APP_TITLE)

        #
        # Input TextBox
        self.input_value = tk.StringVar(self.master)
        self.input_textbox = tk.Entry(self.master, textvariable=self.input_value)
        self.input_textbox.grid(row=0, column=0, columnspan=3)

        #
        # Hex output
        self.hex_label = tk.Label(self.master, text="Hex: ")
        self.hex_label.grid(row=1, column=0)
        self.hex_value = tk.StringVar(self.master)
        self.hex_textbox = tk.Entry(self.master, textvariable=self.hex_value)
        self.hex_textbox.grid(row=1, column=1)

        #
        # RGB/RGBA output
        self.rgb_label = tk.Label(self.master, text="RGB/RGBA: ")
        self.rgb_label.grid(row=2, column=0)
        self.rgb_value = tk.StringVar(self.master)
        self.rgb_textbox = tk.Entry(self.master, textvariable=self.rgb_value)
        self.rgb_textbox.grid(row=2, column=1)

        #
        # HSL/HSLA output
        self.hsl_label = tk.Label(self.master, text="HSL/HSLA: ")
        self.hsl_label.grid(row=3, column=0)
        self.hsl_value = tk.StringVar(self.master)
        self.hsl_textbox = tk.Entry(self.master, textvariable=self.hsl_value)
        self.hsl_textbox.grid(row=3, column=1)

    def continuous_convert(self):
        pass
