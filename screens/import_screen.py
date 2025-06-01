import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter as ctk

from screens.df_preview_screen import DFPreviewScreen
import config

class ImportScreen:
    
    def __init__(self):
        
        pass

    #STEP 1: Importing the dataset
    #This function is used to import dataset files and display it
    def build_model_button_function(self):

        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()
        
        #step 1 label
        step1_label = ctk.CTkLabel(config.main_window, text="Step 1: Import Dataset", font=("Arial", 20, "bold"))
        step1_label.pack(pady=20)

        #import csv button
        import_csv_button = ctk.CTkButton(config.main_window, text="Import CSV", font=("Arial", 16), command=self.import_csv, width=180, height=40)
        import_csv_button.place(relx=0.5, rely=0.25, anchor="center")

        #import excel button
        import_excel_button = ctk.CTkButton(config.main_window, text="Import Excel", font=("Arial", 16), command=self.import_excel, width=180, height=40)
        import_excel_button.place(relx=0.5, rely=0.35, anchor="center")

        #import json button
        import_json_button = ctk.CTkButton(config.main_window, text="Import JSON", font=("Arial", 16), command=self.import_json, width=180, height=40)
        import_json_button.place(relx=0.5, rely=0.45, anchor="center")

        #back button
        from screens.main_menu_screen import MainMenuScreen
        back_button = ctk.CTkButton(config.main_window, text="Back", font=("Arial", 16), command=MainMenuScreen().back_to_main_menu, width=100, height=40)
        back_button.place(relx=0.5, rely=0.55, anchor="center")

    #saved actions dictionary for handling missing values
    config.saved_actions = {} 

    #Importing csv files
    def import_csv(self):

        config.current_step = "step 1"

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            #read CSV file
            config.df = pd.read_csv(file_path)

            #calling the function to display the dataframe
            DFPreviewScreen().show_dataframe(config.df)
            #clearing the saved actions as the dataframe has changed
            config.saved_actions.clear()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    #Importing excel files
    def import_excel(self):

        config.current_step = "step 1"

        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            #read excel file
            config.df = pd.read_excel(file_path, sheet_name=0, engine="openpyxl")

            #calling the function to display the dataframe
            DFPreviewScreen().show_dataframe(config.df)
            #clearing the saved actions as the dataframe has changed
            config.saved_actions.clear()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    #Importing json files
    def import_json(self):


        config.current_step = "step 1"

        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            #read json file
            config.df = pd.read_json(file_path, orient="records")

            #calling the function to display the dataframe
            DFPreviewScreen().show_dataframe(config.df)
            #clearing the saved actions as the dataframe has changed
            config.saved_actions.clear()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
