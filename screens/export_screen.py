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

                    'target_variable': config.selected_target_variable,
                    'target_label_encoder': config.label_encoder if config.label_encoder else None,
                    'label_encoded_target_labels': config.target_class_labels if config.target_class_labels else None,
                    'feature_columns': config.selected_input_variables,
                    'encoders_used_for_features': config.saved_categorical_encoding,
                    'column_transformers': config.col_transformer,
                    'model_pipeline': config.pipe    

                }

    
    #function to export the trained model as a pickle file
    def export_pkl(self):
        
        #validating if there is a trained model to export
        if config.pipe is None:
            messagebox.showerror("Error", "No trained model found to export.")
            return
        
        else:
            
            #asking the user to select the destination folder
            destination_parent = Path(filedialog.askdirectory(title="Select Folder to Save Model"))

            if not destination_parent:
                return
            
            #file name
            file_name = f"UNEEFLOW {config.file_name} Trained on {config.selected_model} Model"
            pkl_file_name = f"{file_name}.pkl"

            #creating the destination fild path
            destination_file_path = destination_parent / pkl_file_name

            #error handling
            try:
                #checking if the file already exists
                if destination_file_path.exists():
                    #if the file exists, asking the user if they want to overwrite it or create a copy
                    overwrite = messagebox.askyesnocancel(
                    "File Exists",
                    f"The file '{pkl_file_name}' already exists at the destination.\nDo you want to replace it?\n"
                    "Yes: Replace it\n"
                    "No: Save a copy with a numbered suffix\n"
                    "Cancel: Do nothing"
                    )

                    #overwriting the existing file
                    if overwrite is True:
                        joblib.dump(self.export_package, destination_file_path)
                        config.export_confirmation = True
                        messagebox.showinfo("Success", f"Model.pkl overwritten:\n{destination_file_path}")
                    
                    #creating a copy with numbered suffix
                    elif overwrite is False:
                        #creating copies with numbered suffixes
                        i = 1
                        while True:
                            #creating new file name with suffix
                            new_file_name_path = destination_parent / f"{file_name} ({i}).pkl"
                            if not new_file_name_path.exists():
                                joblib.dump(self.export_package, new_file_name_path)
                                config.export_confirmation = True
                                messagebox.showinfo("Success", f"Model.pkl saved as:\n{new_file_name_path}")
                                break
                            i += 1

                    #cancelling the save operation
                    else:
                        messagebox.showinfo("Cancelled", "Save operation was cancelled.")
                        
                #if the file does not exist creating it directly
                else:
                    joblib.dump(self.export_package, destination_file_path)
                    config.export_confirmation = True
                    messagebox.showinfo("Success", f"Model.pkl saved to:\n{destination_file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save profile report:\n{e}")
    
    
    #this function will be set to the next button to finish the flow
    def finish_flow(self):
        
        
        if config.export_confirmation == True:

            #confirmation if the model is exported
            if not messagebox.askyesno(
                "Flow Complete",
                "The model has been successfully exported.\nDo you want to go back to the main menu? (this cannot be undone)"
                ):
                return
            
            #removing all widgets from the window
            for widget in config.main_window.winfo_children():
                widget.destroy()
            
            #going back to the main menu
            from screens.main_menu_screen import MainMenuScreen
            MainMenuScreen().main_menu()
        
        elif config.export_confirmation == False:

            #confirmation if the model is not exported
            if not messagebox.askyesno(
                "Confirm Exit",
                "You have not exported your model.\nDo you still want to exit the flow? (this cannot be undone)"
                ):
                return
            
            #removing all widgets from the window
            for widget in config.main_window.winfo_children():
                widget.destroy()
            
            #going back to the main menu
            from screens.main_menu_screen import MainMenuScreen
            MainMenuScreen().main_menu()



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

        #heading label
        heading_label = ctk.CTkLabel(top_frame, text="Step 8: Export Model", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Finish button
        finish_button = ctk.CTkButton(top_frame, text="Finish", font=("Arial", 14), command=self.finish_flow)
        finish_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_export_section, fg_color="gray10")
        middle_frame.pack(fill="both",pady=(20,0))

        center_frame = ctk.CTkFrame(middle_frame, width=700, height=700, fg_color="gray10")
        center_frame.pack(padx=50, pady=10, fill="both", expand=True)

        #export section
        ################################
        export_section_frame = ctk.CTkScrollableFrame(center_frame, fg_color="gray8", height=550)
        export_section_frame.pack(anchor="center", pady=10, fill="both")

        #heading
        export_heading_label = ctk.CTkLabel(export_section_frame, text="Pickle (.pkl) File Contents", font=("Arial", 18, "bold"))
        export_heading_label.pack(pady=10)

        pkl_contents = "".join( f"- {col.capitalize()}: {content}\n\n" for col, content in self.export_package.items())
                            
        #label to show whats being exported
        export_contents_label = ctk.CTkLabel(export_section_frame, text=f"{pkl_contents}", font=("Arial", 16), wraplength=580, justify="left")
        export_contents_label.pack(pady=10)

        #export button
        export_button = ctk.CTkButton(center_frame, text="Export Model", font=("Arial", 16), width=150, height=35, command=self.export_pkl)
        export_button.pack(pady=20)

        loading_frame.pack_forget()
        entire_export_section.pack(fill="both", expand=True)