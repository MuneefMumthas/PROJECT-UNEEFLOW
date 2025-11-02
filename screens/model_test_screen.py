import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter as ctk

from screens.df_preview_screen import DFPreviewScreen
import config

class ModelTestScreen:
    
    def __init__(self):
        
        pass

    def show_model_test_screen(self):

        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()
        
        #heading
        heading_label = ctk.CTkLabel(config.main_window, text="Model Deployment & Testing", font=("Arial", 20, "bold"))
        heading_label.pack(pady=20)

        #import model pkl button
        import_model_button = ctk.CTkButton(config.main_window, text="Load Model.pkl", font=("Arial", 16), command=None, width=180, height=40)
        import_model_button.place(relx=0.5, rely=0.40, anchor="center")



        #back button
        from screens.main_menu_screen import MainMenuScreen
        back_button = ctk.CTkButton(config.main_window, text="Back", font=("Arial", 16), command=lambda: MainMenuScreen().back_to_main_menu(), width=100, height=40)
        back_button.place(relx=0.5, rely=0.5, anchor="center")
