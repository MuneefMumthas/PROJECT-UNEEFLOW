import customtkinter as ctk
from tkinter import messagebox
from pandas.api.types import is_numeric_dtype
import config


class MissingValScreen:
    def __init__(self):
        pass

    #Step 4 - Handling Missing Values

    #this function is used to handle the change in the combo box selection
    # it saves the selected action for each column in the saved_actions dictionary
    def on_combo_change(self, col_name: str, combo: ctk.CTkComboBox):
        config.saved_actions[col_name] = combo.get()

    #this function is used to bulk select actions for all columns in the missing values section
    def apply_bulk(self, option: str, actions: dict[str, ctk.CTkComboBox]):

        for col, combo in actions.items():

            if option == "Remove All Rows":
                combo.set("Remove Rows")
                

            elif option == "Fill Median/Mode":
                column_data = config.df_selected[col]
                nunique  = column_data.nunique(dropna=True)
                frac_nunique   = nunique / len(column_data)

                #continuous numeric data
                if is_numeric_dtype(column_data) and nunique > 10 and frac_nunique > 0.05:
                    combo.set("Fill with Median")
                
                #categorical numeric data
                else:
                    combo.set("Fill with Mode")

            #saving the selected action in the saved_actions dictionary
            config.saved_actions[col] = combo.get()

            if self.bulk_button is not None:
                #resetting the bulk button to None to reuse it
                self.bulk_button.set(None)


    #This function is used to handle missing values in the dataset for both numerical and categorical data
    #################################################################################################################################### 
    def show_missing_val_screen(self):
        

        config.current_step = "step 4"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #removing the saved actions if the columns have changed
        #this is done to avoid issues with the saved actions not matching the current columns
        current_columns = list(config.df_selected.columns)
        if config.prev_columns is None or set(current_columns) != set(config.prev_columns):
            config.saved_actions.clear()

        config.prev_columns = current_columns.copy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(expand=True)

        #creating a frame for the entire section
        
        entire_missingvalues_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_missingvalues_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_missingvalues_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.input_var_screen import InputVarScreen
        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=lambda: InputVarScreen().show_input_var_screen())
        back_button.pack(side="left",padx=10)

        #heading label
        heading_label = ctk.CTkLabel(top_frame, text="Step 4: Handling Missing Values", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle fram for content
        middle_frame = ctk.CTkFrame(entire_missingvalues_section, fg_color="gray10")
        middle_frame.pack(pady=30)

        #bulk button to bulk select actions
        self.bulk_button =ctk.CTkSegmentedButton(middle_frame, values=["Remove All Rows", "Fill Median/Mode"], command=lambda opt: self.apply_bulk(opt, actions))
        self.bulk_button.pack(pady=10)

        #scrollable frame for the content
        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=500, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)

        #hiding the scrollbar if there are 8 columns or less
        if len(config.df_selected.columns) > 8:
            scroll_frame._scrollbar.grid()
        else:
            scroll_frame._scrollbar.grid_remove()

        
        #dictionary to store actions for each option in the combo box
        actions = {}

        for i, col in enumerate(config.df_selected.columns):

            #counting the missing values in each column
            missing_count = config.df_selected[col].isnull().sum()

            #creating border for each row using a lower height frame
            border_frame = ctk.CTkFrame(scroll_frame, fg_color="gray8", border_color="gray10", border_width=1)
            border_frame.grid(row=i, column=0, columnspan=3, sticky="ew")
            
            #making the columns equal width for better alignment
            for col_idx in (0, 1, 2):
                border_frame.grid_columnconfigure(col_idx, weight=1, uniform="cols")


            #column name label
            col_name_label = ctk.CTkLabel(border_frame, text=f"{col}: ", font=("Arial", 16), text_color="white", wraplength=180, bg_color="gray8")
            col_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(15,15))

            
            if missing_count == 0:

                #label for no missing values
                no_missing_label = ctk.CTkLabel(border_frame, text="No Missing Values", text_color="green", font=("Arial", 16), bg_color="gray8")
                no_missing_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

                #label for no action needed
                no_action_label = ctk.CTkLabel(border_frame, text="No Action Needed", text_color="gray50", font=("Arial", 16), bg_color="gray8")
                no_action_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)
            
            else:

                #missing count label
                missing_count_label = ctk.CTkLabel(border_frame, text=f"{missing_count} missing values", text_color="red", font=("Arial", 16), bg_color="gray8")
                missing_count_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
                
                #actions for handling missing values by data type
                column_data = config.df_selected[col]
                nunique  = column_data.nunique(dropna=True)
                frac_nunique   = nunique / len(column_data)


                #continuous numeric data
                if is_numeric_dtype(column_data) and nunique > 10 and frac_nunique > 0.05:
                    options = [ 
                        "Fill with Mean/Average",
                        "Fill with Median",
                        "Remove Rows",
                        "Remove Column"
                    ]

                #categorical numeric data
                elif is_numeric_dtype(column_data):
                    options = [
                        "Fill with Mode",
                        "Remove Rows",
                        "Remove Column"
                    ]
                

                #object or string dtype
                else:
                    options = [
                        "Fill with Mode",      
                        "Remove Rows",
                        "Remove Column"
                    ]

                #combo box for handling missing values
                combo = ctk.CTkComboBox(border_frame, values=options, state="readonly")
                combo.set("Choose Action")

                if col in config.saved_actions and config.saved_actions[col] in options:
                    combo.set(config.saved_actions[col])

                combo.configure(command=lambda val, c=col, cb=combo: self.on_combo_change(c, cb))

                combo.grid(row=0, column=2, sticky="w", padx=10, pady=5)
                actions[col] = combo
        
 
        config.total_missing = config.df_selected.isnull().sum().sum()
    
        #showcasing the missing values only if there are any
        if config.total_missing == 0:
            
            total_missing_label = ctk.CTkLabel(middle_frame, text="Click Next to continue, this will also remove any duplicate rows", font=("Arial", 18), text_color="white")
            total_missing_label.pack(pady=10)

            #hiding the bulk button if there are no missing values
            self.bulk_button.pack_forget()

        else:
            total_missing_label = ctk.CTkLabel(middle_frame, text=f"The actions will also remove duplicate rows after handling the Total Missing Values: {config.total_missing}", font=("Arial", 18), text_color="white", wraplength=500)
            total_missing_label.pack(pady=10)

        def apply_actions():

            from screens.df_preview_screen import DFPreviewScreen

            #creating a copy of the selected DataFrame to avoid modifying the original
            config.df_handled_missing_values = config.df_selected.copy()

            if config.total_missing == 0:
                config.selected_input_variables = list(config.df_handled_missing_values.columns.drop(config.selected_target_variable))
                print(f"Updated Input Variables: {config.selected_input_variables}")
                
                #removing duplicates
                config.df_handled_missing_values.drop_duplicates(inplace=True)

                DFPreviewScreen().show_dataframe(config.df_handled_missing_values)
            else:
                #checking if any action is selected for columns with missing values
                missing_cols = [
                    col
                    for col, combo in actions.items()
                    if combo.get() == "Choose Action"
                ]
                if missing_cols:
                    messagebox.showerror(
                        "Error",
                        "Please select an action for the following columns:\n  "
                        + "\n  ".join(missing_cols)
                    )
                    return

                #confirmation dialog for applying actions
                if not messagebox.askyesno(
                    "Confirm",
                    "You’ve selected actions for every column.\nProceed to apply them?"
                    ):
                    return

                

                #dropping rows with missing values first
                to_drop_rows = [
                    c for c, combo in actions.items()
                    if combo.get().startswith("Remove Rows")
                ]
                if to_drop_rows:
                    config.df_handled_missing_values.dropna(subset=to_drop_rows, inplace=True)

                #filling missing values based on selected actions
                for col, combo in actions.items():
                    act = combo.get()
                    if act == "Fill with Mean/Average":
                        config.df_handled_missing_values[col].fillna(config.df_handled_missing_values[col].mean(), inplace=True)
                    elif act == "Fill with Median":
                        config.df_handled_missing_values[col].fillna(config.df_handled_missing_values[col].median(), inplace=True)
                    elif act == "Fill with Mode":
                        config.df_handled_missing_values[col].fillna(config.df_handled_missing_values[col].mode()[0], inplace=True)

                #droppin columns last to avoid issues with missing values in other columns
                to_drop_cols = [
                    c for c, combo in actions.items()
                    if combo.get().startswith("Remove Column")
                ]
                if to_drop_cols:
                    config.df_handled_missing_values.drop(columns=to_drop_cols, inplace=True)

                #removing duplicate rows
                config.df_handled_missing_values.drop_duplicates(inplace=True)

                #storing the final input variables after handling missing values
                config.selected_input_variables = list(config.df_handled_missing_values.columns.drop(config.selected_target_variable))
                print(f"Updated Input Variables: {config.selected_input_variables}")

                #showing the dataset preview after handling missing values
                DFPreviewScreen().show_dataframe(config.df_handled_missing_values)
        
        next_button.configure(command=apply_actions)

        loading_frame.pack_forget()
        entire_missingvalues_section.pack(fill="both", expand=True)
    #################################################################################################################################### 
