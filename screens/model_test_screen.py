import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter as ctk

import config
import joblib

class ModelTestScreen:
    
    def __init__(self):
        
        pass

    def show_model_test_screen(self):

        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()

        center_frame = ctk.CTkFrame(config.main_window, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.40, anchor="center")
        
        #heading
        heading_label = ctk.CTkLabel(center_frame, text="Model Deployment & Testing", font=("Arial", 20, "bold"))
        heading_label.pack(pady=(0, 50)) 

        #import model pkl button
        import_model_button = ctk.CTkButton(center_frame, text="Load Model.pkl", font=("Arial", 16), command=self.load_model_and_test, width=180, height=40)
        import_model_button.pack(pady=(0, 25))


        #back button
        from screens.main_menu_screen import MainMenuScreen
        back_button = ctk.CTkButton(center_frame, text="Back", font=("Arial", 16), command=lambda: MainMenuScreen().back_to_main_menu(), width=100, height=40)
        back_button.pack(pady=(10,0))

    def load_model_and_test(self):

        #loading the model pkl

        pkl_path = filedialog.askopenfilename(title="Select model (.pkl)", filetypes=[("Pickle files", "*.pkl")])
        
        if not pkl_path:
            return
        
        try:
            #loading the pkl via joblib and saving it inside the config
            config.model_package = joblib.load(pkl_path)
            print(config.model_package)

        #error handling
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            return


        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(expand=True)

        #creating a frame for the entire section
        entire_test_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_test_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_test_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=self.show_model_test_screen)
        back_button.pack(side="left",padx=10)

        #heading label
        heading_label = ctk.CTkLabel(top_frame, text="Enter Data to Predict", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_test_section, fg_color="gray10")
        middle_frame.pack(fill="both",pady=(20,0))


        #scroll frame
        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=500, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)


        #features from the model pkl
        feature_cols = config.model_package.get("feature_columns", [])

        #hiding the scrollbar if there are 8 columns or less
        if len(feature_cols) > 8:
            scroll_frame._scrollbar.grid()
        else:
            scroll_frame._scrollbar.grid_remove()

        for i, col in enumerate(feature_cols):

            #creating border for each row using a lower height frame
            border_frame = ctk.CTkFrame(scroll_frame, fg_color="gray8", border_color="gray10", border_width=1)
            border_frame.grid(row=i, column=0, columnspan=3, sticky="ew")
            
            #making the columns equal width for better alignment
            for col_idx in (0, 1, 2):
                border_frame.grid_columnconfigure(col_idx, weight=1, uniform="cols")


            #column name label
            col_name_label = ctk.CTkLabel(border_frame, text=f"{col}: ", font=("Arial", 16), text_color="white", wraplength=180, bg_color="gray8")
            col_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(15,15))

            #entry box
            col_entry = ctk.CTkEntry(border_frame, width=250, placeholder_text=f"Enter {col}")
            col_entry.grid(row=0, column=2, sticky="w", padx=10, pady=5)





        loading_frame.pack_forget()
        entire_test_section.pack(fill="both", expand=True)