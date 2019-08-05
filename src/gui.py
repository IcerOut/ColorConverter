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
        self.input_value = tk.StringVar(self.master, value='Enter a color...')
        self.input_textbox = tk.Entry(self.master, textvariable=self.input_value,
                                      font=('Verdana', 36), width=15, fg=DISCORD_LIGHT,
                                      bg=DISCORD_TEXTBOX, justify='center')
        self.input_textbox.grid(row=0, column=0, columnspan=2)
        self.old_input = 'Enter a color...'
        self.input_textbox.bind('<FocusIn>', self._on_entry_click)
        self.input_textbox.bind('<FocusOut>', self._on_focusout)

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
    def _on_entry_click(self, event):
        """
        Handles the entry click in the input entry box
        Clears the default text and sets the color to normal
        :param event: The event returned by the bind
        """
        # Binded to <FocusIn> for self.input_textbox
        if self.input_value.get() == 'Enter a color...':
            print('Faded out text.')
            self.input_value.set('')
            self.input_textbox.configure(fg=DISCORD_LIGHT)

    def _on_focusout(self, event):
        """
        Handles the click out of the input entry box
        Sets the default text and sets the color to faded out
        :param event: The event returned by the bind
        """
        # Binded to <FocusOut> for self.input_textbox
        if self.input_value.get() == '':
            print('Faded in text.')
            self.input_value.set('Enter a color...')
            self.input_textbox.configure(fg=DISCORD_LIGHT_FADED)
    def continuous_convert(self) -> None:
        """
        Continuously monitors the input textbox and dropdown for changes (every 0.5 seconds)
        When it detects a change, it updates the conversions
        """
        user_input = self.input_value.get()
        if user_input != self.old_input:
        if not user_input:
            self.name_value.set(EMPTY_CONVERSION)
            self.hex_value.set(EMPTY_CONVERSION)
            self.rgb_value.set(EMPTY_CONVERSION)
            self.hsl_value.set(EMPTY_CONVERSION)
            self.color_display.configure(bg=DISCORD_DARK)
        if user_input != self.old_input and user_input != 'Enter a color...' and user_input:
            self.old_input = user_input
            print('Change detected, attempting conversion...', end='')
            try:
                new_color = convert(user_input)
                self.name_value.set(new_color.name)
                self.hex_value.set(new_color.hex)
                self.rgb_value.set(new_color.rgb)
                self.hsl_value.set(new_color.hsl)
                self.color_display.configure(bg=new_color.hex)
            except ValueError:
                print(' Invalid number or decimal entered.')
            except InvalidColorError:
                print(' No format recognized.')
        self.master.after(500, self.continuous_convert)
