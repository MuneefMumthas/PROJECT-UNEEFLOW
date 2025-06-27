import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from screens.df_preview_screen import DFPreviewScreen
from screens.target_var_screen import TargetVarScreen
import config

class InputVarScreen:
    def __init__(self):
        pass

    #Step 3: Select Input Variables
    #This function is used to select the input variables from the dataframe
    #################################################################################################################################### 
    def step_3_select_input_variables(self):

        
        config.current_step = "step 3"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        entire_inputvariables_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_inputvariables_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_inputvariables_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)


        #back button
        from screens.target_var_screen import TargetVarScreen
        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=TargetVarScreen().step_2_select_target_variable)
        back_button.pack(side="left",padx=10)

        #heading lable
        table_label = ctk.CTkLabel(top_frame, text="Step 3: Select Input Variables", font=("Arial", 16, "bold"))
        table_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
        next_button.pack(side="right", padx=10)

        #displaying the columns except the target variable
        selected_columns = {col: tk.BooleanVar(value=True) for col in config.df.columns if col != config.selected_target_variable}

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_inputvariables_section, fg_color="gray10")
        middle_frame.pack(pady=40)

        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=600, fg_color="gray10")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #turning on the visibility of the scrollbar if there are more than 13 columns
        if len(selected_columns) > 13:
            scroll_frame._scrollbar.grid()
        else:
            scroll_frame._scrollbar.grid_remove()

        scroll_frame.columnconfigure(0, weight=1)

        #checkbox for each column
        for col, var in selected_columns.items():
            checkbox = ctk.CTkCheckBox(scroll_frame, text=col, variable=var)
            checkbox.grid(column=0, sticky="w", pady=10, padx=50)

        #creatting a segmented button for select all and deselect all
        select_all_button = ctk.CTkSegmentedButton(scroll_frame, values=["✅", "❎"], command=None)
        select_all_button.grid(row=0, column=1, padx=10, pady=10)

        #function for selecting/deselecting all checkboxes
        def selection_command(value):
            
            if value == "✅":
                #select all checkboxes
                for var in selected_columns.values():
                    var.set(True)

                #setting the segmented button to None to reuse it
                select_all_button.set(None)

            elif value == "❎":
                #deselect all checkboxes
                for var in selected_columns.values():
                    var.set(False)

                select_all_button.set(None)

        select_all_button.configure(command=selection_command)

        def save_selected_columns_df():

            #from screens.df_preview_screen import DFPreviewScreen
            from screens.dtype_confirmation_screen import DtypeScreen

            #get the selected columns
            selected = [col for col, var in selected_columns.items() if var.get()]
            
            #check if at least one column is selected
            if len(selected) == 0:
                #show error message if no column is selected
                messagebox.showerror("Error", "Please select at least one column.")
                return

            #show confirmation dialog 
            confirmation = messagebox.askyesno("Confirm", f"You have selected: {', '.join(selected)}\nDo you want to proceed?")
            if confirmation:
                #drop unselected columns 
                config.df_selected = config.df[selected + [config.selected_target_variable]]
                print("Selected columns:", config.df_selected.columns.tolist())
                #show updated dataframe
                #DFPreviewScreen().show_dataframe(config.df_selected)
                
                DtypeScreen().step_4_confirm_dtypes()

            else:
                #allow user to modify selection
                return
            
        next_button.configure(command=save_selected_columns_df)

        loading_frame.pack_forget()
        entire_inputvariables_section.pack(fill="both", expand=True)
    #################################################################################################################################### 
