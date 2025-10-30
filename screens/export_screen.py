import customtkinter as ctk
from tkinter import messagebox
import config
import pandas as pd
from tkinter import filedialog
import joblib
import numpy as np
from pathlib import Path


class ExportScreen:
    def __init__(self):

        #creating the export package at the initialization of the screen
        self.export_package = {
                    'model_pipeline': config.pipe,
                    'feature_columns': config.selected_input_variables,
                    'encoders_used_for_features': config.saved_categorical_encoding,
                    'target_variable': config.selected_target_variable,
                    'target_label_encoder': config.label_encoder if config.label_encoder else None,
                    'encoded_labels': config.target_class_labels if config.target_class_labels else None
                    
                }

    def export_pkl(self):
        
        #validating if there is a trained model to export
        if config.pipe is None:
            messagebox.showerror("Error", "No trained model found to export.")
            return
        
        else:
            
            #file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")], title="Save Trained Model")
            file_path = Path(filedialog.askdirectory(title="Select Folder to Save Model")) / f"UNEEFLOW {config.file_name} Trained on {config.selected_model} Model.pkl"
            if not file_path:
                return

            try:
                
                #exporting the model using joblib
                joblib.dump(self.export_package, file_path)
                messagebox.showinfo("Success", f"Model exported successfully to {file_path}")

            
            #error handling
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export model: {str(e)}")


    def show_export_screen(self):

        config.current_step = "step 8"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(expand=True)

        #creating a frame for the entire section
        
        entire_export_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_export_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_export_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.model_evaluation_screen import EvaluationScreen
        

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=lambda: EvaluationScreen().show_evaluation_screen())
        back_button.pack(side="left",padx=10)

        #heading lable
        heading_label = ctk.CTkLabel(top_frame, text="Step 8: Export Model", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_export_section, fg_color="gray10")
        middle_frame.pack(fill="both",pady=(20,0))

        center_frame = ctk.CTkFrame(middle_frame, width=700, height=700, fg_color="gray9")
        center_frame.pack(padx=50, pady=10, fill="both", expand=True)

        #export section
        ################################
        export_section_frame = ctk.CTkFrame(center_frame, fg_color="gray8", height=220)
        export_section_frame.pack(anchor="center", pady=10, fill="both")

        export_button = ctk.CTkButton(export_section_frame, text="Export Model", font=("Arial", 16), width=200, height=40, command=self.export_pkl)
        export_button.pack(pady=20)

        loading_frame.pack_forget()
        entire_export_section.pack(fill="both", expand=True)