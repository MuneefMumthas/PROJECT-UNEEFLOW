import customtkinter as ctk
from tkinter import messagebox
from pandas.api.types import is_numeric_dtype
import config
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder
import pandas as pd


class EncodingScreen:
    def __init__(self):
        pass

    def show_encoding_screen(self):

        config.current_step = "step 5"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        
        entire_encoding_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_encoding_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_encoding_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.df_preview_screen import DFPreviewScreen
        def back_to_preview():
            config.current_step = "step 4"
            DFPreviewScreen().show_dataframe(config.df_handled_missing_values)

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=back_to_preview)
        back_button.pack(side="left",padx=10)

        #heading lable
        table_label = ctk.CTkLabel(top_frame, text="Step 5: Encoding", font=("Arial", 16, "bold"))
        table_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_encoding_section, fg_color="gray10")
        middle_frame.pack(pady=30)

        #creating a copy of the dataframe to work with

        config.df_encoded = config.df_handled_missing_values.copy()

        target = config.selected_target_variable
        target_series = config.df_encoded[config.selected_target_variable]

        #encoding the target variable if it is categorical
        if not is_numeric_dtype(target_series):
            target_encoding_frame = ctk.CTkFrame(middle_frame, fg_color="gray10")
            target_encoding_frame.pack(pady=20)
            ctk.CTkLabel(target_encoding_frame, text=f"Encoding for {target} Target", font=("Arial", 16, "bold"), text_color="white").pack(pady=10)

            #creating a combo box for selecting the encoding method
            target_encoding_options = ["Label Encoding", "Ordinal Encoding"]

            target_encoding_combo = ctk.CTkComboBox(target_encoding_frame, values=target_encoding_options, state="readonly")
            target_encoding_combo.set("Select Encoding Method")
            
            #saving the selected encoding method in the config
            target_encoding_combo.configure(command=lambda val, t=target: config.saved_target_encoding.__setitem__(t, val))
            target_encoding_combo.pack(pady=10)


        categorical_columns = [c for c in config.selected_input_variables if not is_numeric_dtype(config.df_encoded[c])]

        if categorical_columns:
            #encoding the categorical input variables
            categorical_encoding_frame = ctk.CTkFrame(middle_frame, fg_color="gray10")
            categorical_encoding_frame.pack(pady=20)
            ctk.CTkLabel(categorical_encoding_frame, text="Encoding for Categorical Variables", font=("Arial", 16, "bold"), text_color="white").pack(pady=10)

            #creating a combo box for selecting the encoding method
            categorical_encoding_options = ["One-Hot Encoding", "Ordinal Encoding"]

            for col in categorical_columns:
                col_frame = ctk.CTkFrame(categorical_encoding_frame, fg_color="gray10")
                col_frame.pack(pady=5)

                ctk.CTkLabel(col_frame, text=f"Encoding for {col}", font=("Arial", 14), text_color="white").pack(side="left", padx=10)

                encoding_combo = ctk.CTkComboBox(col_frame, values=categorical_encoding_options, state="readonly")
                encoding_combo.set("Select Encoding Method")

                #saving the selected encoding method in the config
                encoding_combo.configure(command=lambda val, c=col: config.saved_categorical_encoding.__setitem__(c, val))
                encoding_combo.pack(side="left", padx=10)

        
        

        loading_frame.pack_forget()
        entire_encoding_section.pack(fill="both", expand=True)