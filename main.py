import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
import time
from PIL import Image, ImageTk
import pandas as pd
from tkinter import ttk
from customtkinter import CTkImage
import customtkinter as ctk
from pandas.api.types import is_numeric_dtype

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
    import_csv_button = ctk.CTkButton(main_window, text="Import CSV", font=("Arial", 14), command=import_csv)
    import_csv_button.place(relx=0.5, rely=0.15, anchor="center")

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


#Dataset preview function

#methods to generalize the back and next buttons in the dataframe preview screen
def show_dataframe_back():
    global current_step

    if current_step == "step 1" or current_step == "step 2":
        build_model_button_function()
    elif current_step == "step 3":
        step_3_select_input_variables()

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

    top_frame = ctk.CTkFrame(main_window, fg_color="gray10")
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

    #creating a frame for the table
    frame = ctk.CTkFrame(main_window, fg_color="gray10")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    #adding the scrollbars
    tree_scroll_vertical = ctk.CTkScrollbar(frame, orientation="vertical")
    tree_scroll_horizontal = ctk.CTkScrollbar(frame, orientation="horizontal")
    
    #placing the scrollbars
    tree_scroll_vertical.pack(side="right", fill="y")
    tree_scroll_horizontal.pack(fill="x", side="bottom")

    #using the Treeview widget inside the frame to display the dataframe from the CSV
    tree = ttk.Treeview(frame, yscrollcommand=tree_scroll_vertical.set, xscrollcommand=tree_scroll_horizontal.set, selectmode="browse")
    tree_scroll_vertical.configure(command=tree.yview)
    tree_scroll_horizontal.configure(command=tree.xview)

    #adding the dataframe columns to the treeview and hiding the first empty columns created by default
    tree["columns"] = list(current_df.columns)
    tree["show"] = "headings"  

    for col in current_df.columns:
        #assigning the column names
        tree.heading(col, text=col)

        #adjusting the column width based on the longest content in a column 
        max_content_length = max(current_df[col].astype(str).apply(len).max(), len(col))
        tree.column(col, anchor="center", stretch=True, width=(max_content_length * 13))

    #adding the rows to the treeview one by one
    for _, row in current_df.iterrows():
        tree.insert("", "end", values=list(row))

    #method to block clicks on the column header and separator to avoid resizing by the user
    def block_column_resize(event):
        
        #geting the region where the click occurred
        region = tree.identify_region(event.x, event.y)
        if region == "separator" or region == "heading":
            return "break"  

    tree.bind("<Button-1>", block_column_resize)

    #packing the treeview
    tree.pack(fill="both", expand=True)

    #creating a style for the treeview
    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("Treeview.Heading",
                    foreground="black",
                    font=("Arial", 9, "bold"))
    
    style.configure("Treeview",
                    background="#707070",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#707070",
                    font=("Arial", 9))
    

    style.map("Treeview", background=[("selected", "#4B4B4B")])

    #dataset summary section
    summary_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    summary_frame.pack(fill="x", pady=10)

    #calculating the statistics
    num_rows = current_df.shape[0] 
    num_columns = current_df.shape[1] 
    missing_values = current_df.isnull().sum().sum() 

    #displaying the summary
    summary_text = f"📊 Rows: {num_rows}   |   📌 Columns: {num_columns}   |   ❗ Missing Values: {missing_values}"
    summary_label = ctk.CTkLabel(summary_frame, text=summary_text, font=("Arial", 16), text_color="white", padx=10, pady=5)
    summary_label.pack()
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

    top_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    top_frame.pack(fill="x", pady=10)

    #back button to return to Step 1
    back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=lambda: show_dataframe(df))
    back_button.pack(side="left", padx=10)

    #label for Step 2
    step2_label = ctk.CTkLabel(top_frame, text="Step 2: Select Target Variable", font=("Arial", 16, "bold"))
    step2_label.pack(side="left", expand=True)

    #dropdown selection for the target variable
    dropdown_frame = ctk.CTkFrame(main_window)
    dropdown_frame.pack(pady=20)

    ctk.CTkLabel(dropdown_frame, text="Select Target Variable:", font=("Arial", 12)).pack(side="left", padx=10)

    target_variable = ctk.StringVar()
    target_dropdown = ctk.CTkComboBox(dropdown_frame, variable=target_variable, values=list(df.columns), state="readonly")
    target_dropdown.pack(side="left")

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

    #next button
    next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=save_selected_target_var)
    next_button.pack(side="right", padx=10)
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

    top_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    top_frame.pack(fill="x", pady=10)


    #back button
    back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=step_2_select_target_variable)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = ctk.CTkLabel(top_frame, text="Step 3: Select Input Variables", font=("Arial", 16, "bold"))
    table_label.pack(side="left", expand=True)

    #displaying the columns except the target variable

    selected_columns = {col: tk.BooleanVar(value=True) for col in df.columns if col != selected_target_variable}

    
    #middle fram for content
    middle_frame = ctk.CTkFrame(main_window, fg_color="gray10")
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
        
    #Next button
    next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=save_selected_columns_df)
    next_button.pack(side="right", padx=10)
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

    num_cols = [c for c in df.columns if is_numeric_dtype(df[c])] 
    non_num_cols = [c for c in df.columns if c not in num_cols] 
    #removing the existing widgets from the screen
    for widget in main_window.winfo_children():
        widget.destroy()

    top_frame = ctk.CTkFrame(main_window, fg_color="gray10")
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
    middle_frame = ctk.CTkFrame(main_window, fg_color="gray10")
    middle_frame.pack(pady=40)

    #getting the height to adjust scroll frame dynamically
    scrollable_frame_height = len(df_selected.columns) * 30

    scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=scrollable_frame_height, fg_color="gray8")
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    #creating 3 columns in the scrollable frame
    scroll_frame.columnconfigure((0,1,2), weight=1)
    
    for i, col in enumerate(df_selected.columns):

        #counting the missing values in each column
        missing_count = df_selected[col].isnull().sum()

        #configuring the rows for each column
        scroll_frame.rowconfigure(i, weight=1)


        #column name label
        col_name_label = ctk.CTkLabel(scroll_frame, text=f"{col}: ", font=("Arial", 16), text_color="white", wraplength=180)
        col_name_label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        
        if missing_count == 0:

            #label for no missing values
            no_missing_label = ctk.CTkLabel(scroll_frame, text="No Missing Values", text_color="green", font=("Arial", 16))
            no_missing_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        else:

            #missing count label
            missing_count_label = ctk.CTkLabel(scroll_frame, text=f"{missing_count} missing values", text_color="red", font=("Arial", 16))
            missing_count_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            
            #combo box for handling missing values
            options = ["Fill with Mean", "Fill with Median", "Fill with Mode", "Remove Rows", "Remove Column"]
            combo = ctk.CTkComboBox(scroll_frame, values=options, state="readonly")
            combo.set("Choose Action")
            combo.grid(row=i, column=2, sticky="w", padx=10, pady=5)
        
    total_missing = df_selected.isnull().sum().sum()
    total_missing_label = ctk.CTkLabel(middle_frame, text=f"Total Missing Values: {total_missing}", font=("Arial", 16), text_color="white")
    total_missing_label.pack(pady=10)


#################################################################################################################################### 
    
    

#Buttons
build_model_button = ctk.CTkButton(main_window, text="Build a Model", font=("Arial", 14), command=build_model_button_function)
build_model_button.pack(pady=10)

test_model_button = ctk.CTkButton(main_window, text="Test a Model", font=("Arial", 14), command=None)
test_model_button.pack(pady=10)


#running the main window
main_window.mainloop()
