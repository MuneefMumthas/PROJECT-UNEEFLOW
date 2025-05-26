import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
from tkinter import ttk
from customtkinter import CTkImage
import customtkinter as ctk
from pandas.api.types import is_numeric_dtype
from tksheet import Sheet
from CTkScrollableDropdown import *
from tkinterweb import HtmlFrame
from ydata_profiling import ProfileReport
import webview
import tempfile
import os
from pathlib import Path


ctypes.windll.shcore.SetProcessDpiAwareness(2)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("UneeFlow_theme.json")

#Method  to center a window as tkinter does not have a built-in method for this
def center_window(window, width, height):

    #getiing the wndow scaling
    scaling = window._get_window_scaling()
    
    #getting the window size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    #converting the width and height to scaled values
    scaled_width = int(width * scaling)
    scaled_height = int(height * scaling)

    #calculating the x and y position to center the window
    x_pos = (screen_width - scaled_width) // 2
    y_pos = (screen_height - scaled_height) // 2

    #adjusting the x and y position to get it right (i got adhd and i need it to be perfect)
    y_pos = y_pos - int(40 * scaling)
    x_pos = x_pos - int(15 * scaling)

    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    window.resizable(False, False)


#creating the main window
main_window = ctk.CTk()
main_window.title("UNEEFLOW")
center_window(main_window, 750, 750)

#setting the logo
main_window.iconbitmap("U Logo.ico")

#Splash Screen- this will act as a loading screen before the main window
##########################################################################################

#hiding the app at the start for the splash screen
main_window.withdraw()

splash = ctk.CTkToplevel()

#centering the splash window
center_window(splash, 500, 500)
splash.overrideredirect(True)  

#loading the uneeflow logo as splash
splash_img = Image.open("UNEE FLOW LOGO.png")
splash_img = splash_img.resize((500, 500), Image.LANCZOS)
splash_bg = CTkImage(splash_img, size=(500, 500))

splash_label = ctk.CTkLabel(splash, image=splash_bg, text="")
splash_label.pack()

#removing the splash and showing the main window
def close_splash():
    splash.destroy()
    main_window.deiconify()

splash.after(1500, close_splash)

##########################################################################################

#Method for main menu
def main_menu():
    
    #Buttons
    build_model_button = ctk.CTkButton(main_window, text="Build a Model", font=("Arial", 14), command=build_model_button_function, width=200, height=50)
    build_model_button.pack(pady=(250,30))

    test_model_button = ctk.CTkButton(main_window, text="Test a Model", font=("Arial", 14), command=None, width=200, height=50)
    test_model_button.pack(pady=10)


def back_to_main_menu():
    #removing all widgets from the window
    for widget in main_window.winfo_children():
        widget.destroy()
    
    #showing the main menu
    main_menu()


#function for the build model button


#STEP 1: Importing the dataset
#This function is used to import dataset files and display it
def build_model_button_function():

    #removing all widgets from the window
    for widget in main_window.winfo_children():
        widget.destroy()
    
    #step 1 label
    step1_label = ctk.CTkLabel(main_window, text="Step 1: Import Dataset", font=("Arial", 20, "bold"))
    step1_label.pack(pady=20)

    #import csv button
    import_csv_button = ctk.CTkButton(main_window, text="Import CSV", font=("Arial", 16), command=import_csv, width=180, height=40)
    import_csv_button.place(relx=0.5, rely=0.25, anchor="center")

    #import excel button
    import_excel_button = ctk.CTkButton(main_window, text="Import Excel", font=("Arial", 16), command=import_excel, width=180, height=40)
    import_excel_button.place(relx=0.5, rely=0.35, anchor="center")

    #import json button
    import_json_button = ctk.CTkButton(main_window, text="Import JSON", font=("Arial", 16), command=import_json, width=180, height=40)
    import_json_button.place(relx=0.5, rely=0.45, anchor="center")

    #back button
    back_button = ctk.CTkButton(main_window, text="Back", font=("Arial", 16), command=back_to_main_menu, width=100, height=40)
    back_button.place(relx=0.5, rely=0.55, anchor="center")



#Importing csv files
def import_csv():

    global df

    global current_step
    current_step = "step 1"

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        #read CSV file
        df = pd.read_csv(file_path)

        #calling the function to display the dataframe
        show_dataframe(df)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

#Importing excel files
def import_excel():

    global df

    global current_step
    current_step = "step 1"

    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    try:
        #read excel file
        df = pd.read_excel(file_path, sheet_name=0, engine="openpyxl")

        #calling the function to display the dataframe
        show_dataframe(df)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

#Importing json files
def import_json():

    global df

    global current_step
    current_step = "step 1"

    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not file_path:
        return

    try:
        #read json file
        df = pd.read_json(file_path, orient="records")

        #calling the function to display the dataframe
        show_dataframe(df)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")


#Dataset preview function

#methods to generalize the back and next buttons in the dataframe preview screen
def show_dataframe_back():
    global current_step

    if current_step == "step 1" or current_step == "step 2":
        build_model_button_function()
    elif current_step == "step 3":
        step_3_select_input_variables()
    elif current_step == "step 4":
        step_4_Missing_values()

def show_dataframe_next():
    global current_step
    if current_step == "step 1" or current_step == "step 2":
        step_2_select_target_variable()
    elif current_step == "step 3":
        step_4_Missing_values()


#This function is used to display dataframe in a table whenever needed to preview the updated dataframe
#################################################################################################################################### 
def show_dataframe(current_df):

    global df
    global df_selected
    #removing the existing widgets from the screen
    for widget in main_window.winfo_children():
        widget.destroy()

    #loading frame to show while the entire dataframe section is being created
    #this is done to avoid flickering of the screen
    loading_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    loading_frame.pack(fill="both", expand=True)

    loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
    loading_label.pack(pady=40)

    #creating a frame for the entire dataframe section
    entire_showdataframe_section = ctk.CTkFrame(main_window, fg_color="gray10")
    
    #forgetting the section to show only after all the widgets are created
    entire_showdataframe_section.pack_forget()

    top_frame = ctk.CTkFrame(entire_showdataframe_section, fg_color="gray10")
    top_frame.pack(fill="x", pady=10)

    #back button
    back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=show_dataframe_back)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = ctk.CTkLabel(top_frame, text="Dataset Preview", font=("Arial", 20, "bold"))
    table_label.pack(side="left", expand=True)

    #Next button
    next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=show_dataframe_next)
    next_button.pack(side="right", padx=10)

    #container for the table
    container = ctk.CTkFrame(entire_showdataframe_section, fg_color="gray10")
    container.pack(fill="both", expand=True, padx=10, pady=10)

    
    #creating the table view using tksheet
    sheet = Sheet(
        container,
        data=current_df.values.tolist(),
        headers=list(current_df.columns),
        height=400,
        width=700,
        show_x_scrollbar=True,
        show_y_scrollbar=True,
        row_select_mode="single",
        empty_horizontal=0,
        empty_vertical=0,
    )

    #featurs of the table
    sheet.enable_bindings((
        "single_select",
        "arrowkeys",
        "rc_select",
        "right_click_popup_menu",
        "copy",
    ))
    
    sheet.pack(fill="both", expand=True)

    #center aligning content in the table
    sheet.align(":", align="center")

    #setting the column width to fit the content in each column
    col_widths = []
    for col in current_df.columns:
        max_len = max(current_df[col].astype(str).map(len).max(), len(col))
        col_widths.append(max_len * 15)
    
    #applying width based on the content of the column first
    sheet.set_column_widths(col_widths)

    #dataset summary section
    summary_frame = ctk.CTkFrame(entire_showdataframe_section, fg_color="gray10")
    summary_frame.pack(fill="x", pady=10)

    #data profile report button
    data_profile_button = ctk.CTkButton(summary_frame, text="Profile Report", font=("Arial", 14), command=None)
    data_profile_button.pack()

    #calculating the statistics
    num_rows = current_df.shape[0] 
    num_columns = current_df.shape[1] 
    missing_values = current_df.isnull().sum().sum() 

    #displaying the summary
    #summary_text = f"📊 Rows: {num_rows}   |   📌 Columns: {num_columns}   |   ❗ Missing Values: {missing_values}"
    #summary_label = ctk.CTkLabel(summary_frame, text=summary_text, font=("Arial", 16), text_color="white", padx=10, pady=5)
    #summary_label.pack()

    
    ##############################################
    #ydata profiling report section

    #creating the profile report for the current dataframe
    profile = ProfileReport(current_df, explorative=True, title="UneeFlow Data Profile Report", progress_bar=False)
    

    #saving it to a temporary file as the size of the report can be large
    #and we don't want to keep it in memory
    tmp_dir  = tempfile.mkdtemp(prefix="uneeflow_profile_")

    html_path = os.path.join(tmp_dir, "report.html")


    profile.to_file(html_path)

    #creating a file URI for the HTML report to open in webview
    global uri
    uri = Path(html_path).absolute().as_uri()  

    #function to open the webview in a new window
    def open_webview():

        webview.create_window(
            "UneeFlow",
            url=uri,
            width=1920,
            height=1080,
        )


        webview.start()
    
    data_profile_button.configure(command=open_webview)

    ##############################################

    #forget
    loading_frame.pack_forget()
    #showing the entire dataframe section after all the widgets are created
    entire_showdataframe_section.pack(fill="both", expand=True)

    #updating the column tasks to get the available width of the container
    #and then distributing the extra width equally among all columns
    #this is done to make sure that the table fits the container and looks good
    #even if the content is not too long
    container.update_idletasks()
    avail = container.winfo_width()
    used  = sum(col_widths)
    extra = max(0, avail - used) // len(col_widths)
    if extra > 0:
        new_widths = [w + extra for w in col_widths]
        sheet.set_column_widths(new_widths)
#################################################################################################################################### 



#Step 2: Selecting the target variable
#This function is used to select the target variable from the dataframe
#################################################################################################################################### 
def step_2_select_target_variable():

    global df
    global current_step
    current_step = "step 2"

    #removing the existing widgets from the screen
    for widget in main_window.winfo_children():
        widget.destroy()
    
    #loading frame to show while the section is being created
    #this is done to avoid flickering of the screen/ delay
    loading_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    loading_frame.pack(fill="both", expand=True)

    loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
    loading_label.pack(pady=40)

    #creating a frame for the entire dataframe section
    entire_targetvar_section = ctk.CTkFrame(main_window, fg_color="gray10")
    
    #forgetting the section to show only after all the widgets are created
    entire_targetvar_section.pack_forget()

    top_frame = ctk.CTkFrame(entire_targetvar_section, fg_color="gray10")
    top_frame.pack(fill="x", pady=10)

    #back button to return to Step 1
    back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=lambda: show_dataframe(df))
    back_button.pack(side="left", padx=10)

    #label for Step 2
    step2_label = ctk.CTkLabel(top_frame, text="Step 2: Select Target Variable", font=("Arial", 16, "bold"))
    step2_label.pack(side="left", expand=True)

    #next button
    next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
    next_button.pack(side="right", padx=10)

    #dropdown selection for the target variable
    dropdown_frame = ctk.CTkFrame(entire_targetvar_section, fg_color="gray10")
    dropdown_frame.pack(pady=50)

    ctk.CTkLabel(dropdown_frame, text="Select Target Variable:", font=("Arial", 16), text_color="white").pack(side="left", padx=10)

    values=list(df.columns)
    target_variable = ctk.StringVar()
    target_dropdown = ctk.CTkComboBox(dropdown_frame, variable=target_variable, state="readonly", corner_radius=30, font=("Arial", 14), justify="center", width=180)
    target_dropdown.pack(side="left")

    #attaching the scrollable dropdown to the combo box
    CTkScrollableDropdown(target_dropdown, values=values, justify="left", button_color="transparent")

    #adjusting the internal entry’s grid padding
    target_dropdown._entry.grid_configure(padx=(10,45))

    #function to store selection when "Next" is clicked
    def save_selected_target_var():

        global selected_target_variable
        selected_target_variable = target_variable.get()

        if not selected_target_variable:
            #showing an error message if next button clicked without selecting a target variable
            messagebox.showerror("Error", "Please select a target variable!")
            return
        
        #printting the selected target variable for debugging
        print(f"Selected Target Variable: {selected_target_variable}")
        step_3_select_input_variables()

    next_button.configure(command=save_selected_target_var)

    #forget
    loading_frame.pack_forget()
    #showing the entire section after all the widgets are created
    entire_targetvar_section.pack(fill="both", expand=True)
#################################################################################################################################### 



#Step 3: Select Input Variables
#This function is used to select the input variables from the dataframe
#################################################################################################################################### 
def step_3_select_input_variables():

    global df
    global selected_target_variable

    global current_step
    current_step = "step 3"

    #removing the existing widgets from the screen
    for widget in main_window.winfo_children():
        widget.destroy()

    #loading frame
    loading_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    loading_frame.pack(fill="both", expand=True)

    loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
    loading_label.pack(pady=40)

    #creating a frame for the entire section
    entire_inputvariables_section = ctk.CTkFrame(main_window, fg_color="gray10")
    
    #forgetting the section to show only after all the widgets are created
    entire_inputvariables_section.pack_forget()

    top_frame = ctk.CTkFrame(entire_inputvariables_section, fg_color="gray10")
    top_frame.pack(fill="x", pady=10)


    #back button
    back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=step_2_select_target_variable)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = ctk.CTkLabel(top_frame, text="Step 3: Select Input Variables", font=("Arial", 16, "bold"))
    table_label.pack(side="left", expand=True)

    #Next button
    next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
    next_button.pack(side="right", padx=10)

    #displaying the columns except the target variable
    selected_columns = {col: tk.BooleanVar(value=True) for col in df.columns if col != selected_target_variable}

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

        global df
        global df_selected
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
            df_selected = df[selected + [selected_target_variable]]
            #show updated dataframe
            show_dataframe(df_selected)
        else:
            #allow user to modify selection
            return
        
    next_button.configure(command=save_selected_columns_df)

    loading_frame.pack_forget()
    entire_inputvariables_section.pack(fill="both", expand=True)
#################################################################################################################################### 



#Step 4 - Handling Missing Values
#This function is used to handle missing values in the dataset for both numerical and categorical data
#################################################################################################################################### 
def step_4_Missing_values():
    
    global df
    global df_selected
    global selected_target_variable

    global current_step
    current_step = "step 4"

    #removing the existing widgets from the screen
    for widget in main_window.winfo_children():
        widget.destroy()

    #loading frame
    loading_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    loading_frame.pack(fill="both", expand=True)

    loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
    loading_label.pack(pady=40)

    #creating a frame for the entire section
    
    entire_missingvalues_section = ctk.CTkFrame(main_window, fg_color="gray10")
    
    #forgetting the section to show only after all the widgets are created
    entire_missingvalues_section.pack_forget()

    top_frame = ctk.CTkFrame(entire_missingvalues_section, fg_color="gray10")
    top_frame.pack(fill="x", pady=10)

    #back button
    back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=step_3_select_input_variables)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = ctk.CTkLabel(top_frame, text="Step 4: Handling Missing Values", font=("Arial", 16, "bold"))
    table_label.pack(side="left", expand=True)

    #Next button
    next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
    next_button.pack(side="right", padx=10)

    #middle fram for content
    middle_frame = ctk.CTkFrame(entire_missingvalues_section, fg_color="gray10")
    middle_frame.pack(pady=30)

    scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=500, fg_color="transparent")
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    #creating 3 columns in the scrollable frame
    scroll_frame.columnconfigure(0, weight=1)

    #hiding the scrollbar if there are 8 columns or less
    if len(df_selected.columns) > 8:
        scroll_frame._scrollbar.grid()
    else:
        scroll_frame._scrollbar.grid_remove()
    
    #dictionary to store actions for each option in the combo box
    actions = {}

    for i, col in enumerate(df_selected.columns):

        #counting the missing values in each column
        missing_count = df_selected[col].isnull().sum()

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

            #lable for no action needed
            no_action_label = ctk.CTkLabel(border_frame, text="No Action Needed", text_color="gray50", font=("Arial", 16), bg_color="gray8")
            no_action_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        
        else:

            #missing count label
            missing_count_label = ctk.CTkLabel(border_frame, text=f"{missing_count} missing values", text_color="red", font=("Arial", 16), bg_color="gray8")
            missing_count_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
            
            #actions for handling missing values by data type
            column_data = df_selected[col]
            
            #continuous numeric data
            if is_numeric_dtype(column_data) and column_data.nunique() > 10:
                options = [ "ContinuousN debug",
                    "Fill with Mean/Average",
                    "Fill with Median",
                    "Remove Rows",
                    "Remove Column"
                ]

            #categorical numeric data
            elif is_numeric_dtype(column_data):
                options = ["CategoricalN debug",
                    "Fill with Mode",
                    "Remove Rows",
                    "Remove Column"
                ]

            #object or string dtype
            else:
                options = ["object or string debug",
                    "Fill with Mode",      
                    "Remove Rows",
                    "Remove Column"
                ]

            #combo box for handling missing values
            combo = ctk.CTkComboBox(border_frame, values=options, state="readonly")
            combo.set("Choose Action")
            combo.grid(row=0, column=2, sticky="w", padx=10, pady=5)
            actions[col] = combo
    
    global total_missing   
    total_missing = df_selected.isnull().sum().sum()

    #showcasing the missing values only if there are any
    if total_missing == 0:
        total_missing_label = ctk.CTkLabel(middle_frame, text="Click Next to continue", font=("Arial", 18), text_color="white")
        total_missing_label.pack(pady=10)
    else:
        total_missing_label = ctk.CTkLabel(middle_frame, text=f"Total Missing Values: {total_missing}", font=("Arial", 18), text_color="white")
        total_missing_label.pack(pady=10)

    def apply_actions():

        global df_selected, df_handled_missing_values, total_missing
        #creating a copy of the selected DataFrame to avoid modifying the original
        df_handled_missing_values = df_selected.copy()

        if total_missing == 0:
            show_dataframe(df_handled_missing_values)
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
                df_handled_missing_values.dropna(subset=to_drop_rows, inplace=True)

            #filling missing values based on selected actions
            for col, combo in actions.items():
                act = combo.get()
                if act == "Fill with Mean/Average":
                    df_handled_missing_values[col].fillna(df_handled_missing_values[col].mean(), inplace=True)
                elif act == "Fill with Median":
                    df_handled_missing_values[col].fillna(df_handled_missing_values[col].median(), inplace=True)
                elif act == "Fill with Mode":
                    df_handled_missing_values[col].fillna(df_handled_missing_values[col].mode()[0], inplace=True)

            #droppin columns last to avoid issues with missing values in other columns
            to_drop_cols = [
                c for c, combo in actions.items()
                if combo.get().startswith("Remove Column")
            ]
            if to_drop_cols:
                df_handled_missing_values.drop(columns=to_drop_cols, inplace=True)

            #showing the dataset preview after handling missing values
            show_dataframe(df_handled_missing_values)
    
    next_button.configure(command=apply_actions)

    loading_frame.pack_forget()
    entire_missingvalues_section.pack(fill="both", expand=True)
#################################################################################################################################### 
    

main_menu()
#running the main window
main_window.mainloop()
