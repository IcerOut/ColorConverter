"""

ColorConverter
@author: Lung Alin-Sebastian

"""
import tkinter as tk

from src.exceptions import InvalidColorError
from src.globals import APP_TITLE, DISCORD_DARK, DISCORD_LIGHT, DISCORD_TEXTBOX
from src.service import convert
from src.service import convert, random_color


class GUI:
    """
    The class responsible for the GUI and all of its associated functions
    """

    def __init__(self, master):
        self.master = master
        self.master.title(APP_TITLE)
        self.master.configure(bg=DISCORD_DARK)

        #
        # Minimum size config
        for x in range(5):
            self.master.grid_rowconfigure(x, minsize=70, weight=1)

        self.master.grid_columnconfigure(0, minsize=50, weight=1)
        self.master.grid_columnconfigure(1, minsize=150, weight=1)

        #
        # Input TextBox
        self.input_value = tk.StringVar(self.master)
        self.input_value.set('')
        self.input_textbox = tk.Entry(self.master, textvariable=self.input_value,
                                      font=('Verdana', 36), width=15, fg=DISCORD_LIGHT,
                                      bg=DISCORD_TEXTBOX, justify='center')
        self.input_textbox.grid(row=0, column=0, columnspan=2)
        self.old_input = ''

        #
        # Name output
        self.name_label = tk.Label(self.master, text='Name: ', font=('Verdana', 24),
                                   fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.name_label.grid(row=1, column=0)
        self.name_value = tk.StringVar(self.master)
        self.name_textbox = tk.Entry(self.master, textvariable=self.name_value,
                                     font=('Verdana', 24), width=15, fg=DISCORD_LIGHT,
                                     bg=DISCORD_TEXTBOX, justify='center')
        self.name_textbox.grid(row=1, column=1)

        #
        # Hex output
        self.hex_label = tk.Label(self.master, text='Hex: ', font=('Verdana', 24),
                                  fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.hex_label.grid(row=2, column=0)
        self.hex_value = tk.StringVar(self.master)
        self.hex_textbox = tk.Entry(self.master, textvariable=self.hex_value,
                                    font=('Verdana', 24), width=15, fg=DISCORD_LIGHT,
                                    bg=DISCORD_TEXTBOX, justify='center')
        self.hex_textbox.grid(row=2, column=1)

        #
        # RGB output
        self.rgb_label = tk.Label(self.master, text='RGB: ', font=('Verdana', 24),
                                  fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.rgb_label.grid(row=3, column=0)
        self.rgb_value = tk.StringVar(self.master)
        self.rgb_textbox = tk.Entry(self.master, textvariable=self.rgb_value,
                                    font=('Verdana', 24), width=15, fg=DISCORD_LIGHT,
                                    bg=DISCORD_TEXTBOX, justify='center')
        self.rgb_textbox.grid(row=3, column=1)

        #
        # HSL output
        self.hsl_label = tk.Label(self.master, text='HSL: ', font=('Verdana', 24),
                                  fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.hsl_label.grid(row=4, column=0)
        self.hsl_value = tk.StringVar(self.master)
        self.hsl_textbox = tk.Entry(self.master, textvariable=self.hsl_value,
                                    font=('Verdana', 24), width=15, fg=DISCORD_LIGHT,
                                    bg=DISCORD_TEXTBOX, justify='center')
        self.hsl_textbox.grid(row=4, column=1)
        #
        # Action buttons
        self.random_color_button = tk.Button(self.master, font=('Verdana', 24),
                                             text='Generate random color',
                                             command=self._generate_random_color, bg=DISCORD_DARK,
                                             fg=DISCORD_LIGHT, activeforeground='white',
                                             activebackground=DISCORD_DARK_HOVER)
        self.random_color_button.grid(row=5, column=1)

        # Initial call of the function. Afterwards it will keep calling itself every 0.5 seconds
        self.continuous_convert()

    def _generate_random_color(self) -> None:
        """
        Gets a random color and places it in the input entry box
        """
        self.input_value.set(random_color())
    def continuous_convert(self) -> None:
        """
        Continuously monitors the input textbox and dropdown for changes (every 0.5 seconds)
        When it detects a change, it updates the conversions
        """
        user_input = self.input_value.get()
        if user_input != self.old_input:
            self.old_input = user_input
            print('Change detected, attempting conversion...', end='')
            try:
                new_color = convert(user_input)
                self.name_value.set(new_color.name)
                self.hex_value.set(new_color.hex)
                self.rgb_value.set(new_color.rgb)
                self.hsl_value.set(new_color.hsl)
            except ValueError:
                print(' Invalid number or decimal entered.')
            except InvalidColorError:
                print(' No format recognized.')
        self.master.after(500, self.continuous_convert)
