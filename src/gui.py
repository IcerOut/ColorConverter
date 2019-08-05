"""

ColorConverter
@author: Lung Alin-Sebastian

"""
import tkinter as tk
from tkinter import messagebox

from src.exceptions import InvalidColorError
from src.globals import APP_TITLE, DISCORD_DARK, DISCORD_DARK_HOVER, DISCORD_LIGHT, \
    DISCORD_LIGHT_FADED, DISCORD_TEXTBOX, EMPTY_CONVERSION
from src.service import convert, random_color


class GUI:
    """
    The class responsible for the GUI and all of its associated functions
    """

    def __init__(self, master):
        self.master = master
        self.master.title(APP_TITLE)
        self.master.configure(bg=DISCORD_DARK)

        self.master.bind('<Button-1>', self._handle_left_click)
        self.master.bind('<F1>', self._handle_f1)

        #
        # Minimum size config
        for x in range(5):
            self.master.grid_rowconfigure(x, minsize=100, weight=1)

        self.master.grid_columnconfigure(0, minsize=110, weight=1)
        self.master.grid_columnconfigure(1, minsize=150, weight=1)
        self.master.grid_columnconfigure(2, minsize=300, weight=10)

        #
        # Input TextBox
        self.input_value = tk.StringVar(self.master, value='Enter a color...')
        self.input_textbox = tk.Entry(self.master, textvariable=self.input_value,
                                      font=('Verdana', 36), width=15, justify='center',
                                      fg=DISCORD_LIGHT_FADED, bg=DISCORD_TEXTBOX,
                                      insertbackground=DISCORD_LIGHT)
        self.input_textbox.grid(row=0, column=0, columnspan=2)
        self.old_input = 'Enter a color...'
        self.input_textbox.bind('<FocusIn>', self._on_entry_click)
        self.input_textbox.bind('<FocusOut>', self._on_focusout)

        #
        # Name output
        self.name_label = tk.Label(self.master, text='Name: ', font=('Verdana', 24),
                                   fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.name_label.grid(row=1, column=0)
        self.name_value = tk.StringVar(self.master, value=EMPTY_CONVERSION)
        self.name_output = tk.Label(self.master, textvariable=self.name_value,
                                    font=('Verdana', 36), width=15, justify='center',
                                    fg=DISCORD_LIGHT, bg=DISCORD_TEXTBOX)
        self.name_output.grid(row=1, column=1)

        #
        # Hex output
        self.hex_label = tk.Label(self.master, text='Hex: ', font=('Verdana', 24),
                                  fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.hex_label.grid(row=2, column=0)
        self.hex_value = tk.StringVar(self.master, value=EMPTY_CONVERSION)
        self.hex_output = tk.Label(self.master, textvariable=self.hex_value,
                                   font=('Verdana', 36), width=15, justify='center',
                                   fg=DISCORD_LIGHT, bg=DISCORD_TEXTBOX)
        self.hex_output.grid(row=2, column=1)

        #
        # RGB output
        self.rgb_label = tk.Label(self.master, text='RGB: ', font=('Verdana', 24),
                                  fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.rgb_label.grid(row=3, column=0)
        self.rgb_value = tk.StringVar(self.master, value=EMPTY_CONVERSION)
        self.rgb_output = tk.Label(self.master, textvariable=self.rgb_value,
                                   font=('Verdana', 36), width=15, justify='center',
                                   fg=DISCORD_LIGHT, bg=DISCORD_TEXTBOX)
        self.rgb_output.grid(row=3, column=1)

        #
        # HSL output
        self.hsl_label = tk.Label(self.master, text='HSL: ', font=('Verdana', 24),
                                  fg=DISCORD_LIGHT, bg=DISCORD_DARK)
        self.hsl_label.grid(row=4, column=0)
        self.hsl_value = tk.StringVar(self.master, value=EMPTY_CONVERSION)
        self.hsl_output = tk.Label(self.master, textvariable=self.hsl_value,
                                   font=('Verdana', 36), width=15, justify='center',
                                   fg=DISCORD_LIGHT, bg=DISCORD_TEXTBOX)

        self.hsl_output.grid(row=4, column=1)

        #
        # Color Display Box
        self.color_display = tk.Canvas(self.master, bg=DISCORD_DARK, highlightthickness=0)
        self.color_display.grid(row=0, rowspan=6, column=2, sticky='nsew')

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

    def _floating_notification(self, message: str, color: str) -> None:
        """
        Creates a floating notification on the color display for 2 seconds
        :param message: The message of the notification
        :param color: The notification's color
        """
        notification = tk.Label(self.color_display, font=('Verdana', 24), text=message, bg=color,
                                fg='white')
        self.color_display.grid_rowconfigure(0, weight=1)
        self.color_display.grid_columnconfigure(1, weight=1)
        notification.grid(row=1, column=0, sticky='s')
        notification.after(2000, lambda: notification.destroy())

    def _copy_result_to_clipboard(self, event) -> None:
        widget_to_clip = {self.name_output: self.name_value.get(),
                          self.hex_output: self.hex_value.get(),
                          self.rgb_output: f'rgb({self.rgb_value.get()})',
                          self.hsl_output: f'hsl({self.hsl_value.get()})'}
        widget_to_text = {self.name_output: 'Name', self.hex_output: 'Hex', self.rgb_output: 'RGB',
                          self.hsl_output: 'HSL'}
        if self.name_value.get() == EMPTY_CONVERSION:
            print('Nothing to copy!')
            self._floating_notification('Nothing to copy!', 'red')
        else:
            print(f"Text copied to clipboard from {widget_to_text[event.widget]} output.")
            self._floating_notification(
                    f"Text copied to clipboard\n from {widget_to_text[event.widget]} output.",
                    'blue')
            self.master.clipboard_clear()
            clip = widget_to_clip[event.widget]
            self.master.clipboard_append(clip)
            self.master.update()

    def _generate_random_color(self) -> None:
        """
        Gets a random color and places it in the input entry box
        """
        self.input_value.set(random_color())

    # <editor-fold desc="Event Handlers">
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

    def _handle_left_click(self, event):
        """
        Handles left click anywhere in the application, and calls the appropriate function
        :param event: The event returned by the bind
        """
        # Binded to <Mouse-1> for the entire window
        if event.widget == self.input_textbox:
            # We selected the input textbox, we leave the other event handlers to handle it
            pass
        else:
            # We selected something other than the input textbox, so we deselect it
            self.color_display.focus_set()

            if event.widget in [self.name_output, self.hex_output, self.rgb_output,
                                self.hsl_output]:
                # We selected one of the result labels, so we copy the result
                self._copy_result_to_clipboard(event)

    @staticmethod
    def _handle_f1(event):
        # Binded to <F1> for the entire window
        title = 'Help menu'
        content = 'Using the top textbox, simply enter the desired colour. \n' \
                  'The program will automatically detect the format and convert it to all ' \
                  'other options, and display the given colour.\n' \
                  '* For a normal colour, simply enter the name (with any case or formatting)\n' \
                  "* For a hex colour, enter the long form, with or without the '#'\n" \
                  '* For an RGB colour, enter the 3 numbers between 0 and 255, ' \
                  'separated by spaces or commas\n' \
                  '* For a HSL colour, enter the first number (between 0 and 360) and the two ' \
                  "percentages (with a '%' sign or as a number between 0 and 1)\n" \
                  'To copy one of the results, simply click on it.'
        messagebox.showinfo(title, content)

    # </editor-fold>

    def continuous_convert(self) -> None:
        """
        Continuously monitors the input textbox and dropdown for changes (every 0.5 seconds)
        When it detects a change, it updates the conversions
        """
        user_input = self.input_value.get()
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
