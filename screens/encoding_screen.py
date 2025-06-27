import customtkinter as ctk
from tkinter import messagebox
from pandas.api.types import is_numeric_dtype
import config


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



        loading_frame.pack_forget()
        entire_encoding_section.pack(fill="both", expand=True)