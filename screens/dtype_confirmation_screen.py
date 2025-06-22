import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import config

class DtypeScreen:
    def __init__(self):
        pass

    #Confirming the data types of the selected columns before proceeding to the next step
    #################################################################################################################################### 
    def step_4_confirm_dtypes(self):

        
        config.current_step = "step 4"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        entire_dtype_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_dtype_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_dtype_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)


        #back button
        from screens.input_var_screen import InputVarScreen
        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=InputVarScreen().step_3_select_input_variables)
        back_button.pack(side="left",padx=10)

        #heading lable
        table_label = ctk.CTkLabel(top_frame, text="Step 4: Confirm Data types", font=("Arial", 16, "bold"))
        table_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
        next_button.pack(side="right", padx=10)

        #displaying the columns in the new dataframe
        columns = config.df_selected.columns

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_dtype_section, fg_color="gray10")
        middle_frame.pack(pady=40)

        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=600, fg_color="gray10")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #turning on the visibility of the scrollbar if there are more than 13 columns
        if len(columns) > 13:
            scroll_frame._scrollbar.grid()
        else:
            scroll_frame._scrollbar.grid_remove()

        scroll_frame.columnconfigure(0, weight=1)

        
        from screens.df_preview_screen import DFPreviewScreen
        next_button.configure(command=lambda: DFPreviewScreen().show_dataframe(config.df_selected))

        loading_frame.pack_forget()
        entire_dtype_section.pack(fill="both", expand=True)
    #################################################################################################################################### 
