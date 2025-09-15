import customtkinter as ctk
from tkinter import messagebox
import config
import pandas as pd


class TrainingScreen:
    def __init__(self):
        pass

    def show_training_screen(self):

        config.current_step = "step 6"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        
        entire_training_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_training_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_training_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.df_preview_screen import DFPreviewScreen
        def back_to_preview():
            config.current_step = "step 5"
            DFPreviewScreen().show_dataframe(config.df_encoded)

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=back_to_preview)
        back_button.pack(side="left",padx=10)

        #heading lable
        heading_label = ctk.CTkLabel(top_frame, text="Step 6: Training", font=("Arial", 16, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_training_section, fg_color="gray10", height=600)
        middle_frame.pack(pady=30)



        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=600, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)

        

    

        loading_frame.pack_forget()
        entire_training_section.pack(fill="both", expand=True)