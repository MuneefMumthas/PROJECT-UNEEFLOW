import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
from tkinter import ttk
from customtkinter import CTkImage
import customtkinter as ctk
from pandas.api.types import is_numeric_dtype
from tksheet import Sheet
from CTkScrollableDropdown import *
from tkinterweb import HtmlFrame
from ydata_profiling import ProfileReport
import tempfile
import os
from pathlib import Path
import webbrowser
import base64
import shutil
import threading
import config

from screens.main_menu_screen import MainMenuScreen

ctypes.windll.shcore.SetProcessDpiAwareness(2)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(config.uneeflow_ctk_theme)

#Method  to center a window as tkinter does not have a built-in method for this
def center_window(window, width, height):

    #getiing the wndow scaling
    scaling = window._get_window_scaling()
    
    #getting the window size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    #converting the width and height to scaled values
    scaled_width = int(width * scaling)
    scaled_height = int(height * scaling)

    #calculating the x and y position to center the window
    x_pos = (screen_width - scaled_width) // 2
    y_pos = (screen_height - scaled_height) // 2

    #adjusting the x and y position to get it right (i got adhd and i need it to be perfect)
    y_pos = y_pos - int(40 * scaling)
    x_pos = x_pos - int(15 * scaling)

    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    window.resizable(False, False)



if __name__ == "__main__":
    #creating the main window
    config.main_window = ctk.CTk()
    config.main_window.title("UNEEFLOW")
    center_window(config.main_window, 750, 750)

    #setting the logo
    config.main_window.iconbitmap(config.uneeflow_logo_icon)

    #Splash Screen- this will act as a loading screen before the main window
    ##########################################################################################

    #hiding the app at the start for the splash screen
    config.main_window.withdraw()

    splash = ctk.CTkToplevel()

    #centering the splash window
    center_window(splash, 500, 500)
    splash.overrideredirect(True)  

    #loading the uneeflow logo as splash
    splash_img = Image.open(config.uneeflow_logo)
    splash_img = splash_img.resize((500, 500), Image.LANCZOS)
    splash_bg = CTkImage(splash_img, size=(500, 500))

    splash_label = ctk.CTkLabel(splash, image=splash_bg, text="")
    splash_label.pack()

    #removing the splash and showing the main window
    def close_splash():
        splash.destroy()
        config.main_window.deiconify()

    splash.after(1500, close_splash)
    MainMenuScreen().main_menu()

    #deleting the temporary folders created for the profile reports once the app is closed to prevent cluttering the system
    def on_app_close():
        for d in config.profile_temp_dirs:
            shutil.rmtree(d, ignore_errors=True)
        config.main_window.destroy()

    config.main_window.protocol("WM_DELETE_WINDOW", on_app_close)

    #running the main window
    config.main_window.mainloop()
