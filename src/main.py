"""

ColorConverter
@author: Lung Alin-Sebastian

"""
import tkinter as tk

import src.globals as global_var
from src.gui import GUI
from src.startup import read_config, get_language_func

if __name__ == '__main__':
    read_config()
    lang_func = get_language_func(global_var.LANGUAGE)

    root = tk.Tk()
    my_gui = GUI(root, lang_func)
    my_gui.master.mainloop()
