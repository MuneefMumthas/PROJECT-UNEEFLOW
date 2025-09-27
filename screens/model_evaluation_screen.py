import customtkinter as ctk
from tkinter import messagebox
import config
import pandas as pd


class EvaluationScreen:
    def __init__(self):
        pass


    def show_evaluation_screen(self):

        config.current_step = "step 7"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        
        entire_evaluation_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_evaluation_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_evaluation_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.training_screen import TrainingScreen

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=TrainingScreen().show_training_screen)
        back_button.pack(side="left",padx=10)

        #heading lable
        heading_label = ctk.CTkLabel(top_frame, text="Step 7: Model Evaluation", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_evaluation_section, fg_color="gray10")
        middle_frame.pack(fill="x",pady=30)


        center_frame = ctk.CTkFrame(middle_frame, width=700, height=600, fg_color="gray11")
        center_frame.pack(padx=50, pady=10, fill="both", expand=True)



        loading_frame.pack_forget()
        entire_evaluation_section.pack(fill="both", expand=True)