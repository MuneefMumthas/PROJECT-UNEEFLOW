import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
import time
from PIL import Image, ImageTk
import pandas as pd
from tkinter import ttk

ctypes.windll.shcore.SetProcessDpiAwareness(2)


#Method  to center a window as tkinter does not have a built-in method for this
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width - width) // 2
    y_pos = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    window.resizable(False, False)


#creating the main window
root = tk.Tk()
root.title("UNEEFLOW")
center_window(root, 900, 900)

#setting the logo
root.iconbitmap("U Logo.ico")

#Splash Screen- this will act as a loading screen before the main window
##########################################################################################

#hiding the app at the start for the splash screen
root.withdraw()

splash = tk.Toplevel()

#centering the splash window
center_window(splash, 500, 500)
splash.overrideredirect(True)  

#loading the uneeflow logo as splash
splash_img = Image.open("UNEE FLOW LOGO.png")
splash_img = splash_img.resize((500, 500), Image.LANCZOS)
splash_bg = ImageTk.PhotoImage(splash_img)

splash_label = tk.Label(splash, image=splash_bg)
splash_label.pack()

#waiting time before the main window
splash.update()
time.sleep(1.5)

#removing the splash and showing the main window
splash.destroy()
root.deiconify()

##########################################################################################


#function for the build model button



#STEP 1: Importing the dataset
#This function is used to import dataset files and display it
def build_model_button_function():

    #removing all widgets from the window
    for widget in root.winfo_children():
        widget.destroy()
    
    #step 1 label
    step1_label = tk.Label(root, text="Step 1: Import Dataset", font=("Arial", 16, "bold"))
    step1_label.pack(pady=20)

    #import csv button
    import_csv_button = tk.Button(root, text="Import CSV", font=("Arial", 12), command=import_csv)
    import_csv_button.pack()

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
        step_4_data_preprocessing()

#This function is used to display dataframe in a table whenever needed to preview the updated dataframe
def show_dataframe(current_df):

    global df
    global df_selected
    #removing the existing widgets from the screen
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", pady=10)


    #back button
    back_button = tk.Button(top_frame, text="Back", font=("Arial", 12), command=show_dataframe_back)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = tk.Label(top_frame, text="Dataset Preview", font=("Arial", 16, "bold"))
    table_label.pack(side="left", expand=True)

    #Next button
    next_button = tk.Button(top_frame, text="Next", font=("Arial", 12), command=show_dataframe_next)
    next_button.pack(side="right", padx=10)


    #creating a frame for the table
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    #adding the scrollbars
    tree_scroll_vertical = ttk.Scrollbar(frame, orient="vertical")
    tree_scroll_horizontal = ttk.Scrollbar(frame, orient="horizontal")

    #using the Treeview widget inside the frame to display the dataframe from the CSV
    tree = ttk.Treeview(frame, yscrollcommand=tree_scroll_vertical.set, xscrollcommand=tree_scroll_horizontal.set)
    tree_scroll_vertical.config(command=tree.yview)
    tree_scroll_horizontal.config(command=tree.xview)

    #placing the scrollbars
    tree_scroll_vertical.pack(side="right", fill="y")
    tree_scroll_horizontal.pack(side="bottom", fill="x")

    #adding the dataframe columns to the treeview and hiding the first empty columns created by default
    tree["columns"] = list(current_df.columns)
    tree["show"] = "headings"  

    
    for col in current_df.columns:
        #assigning the column names
        tree.heading(col, text=col)

        #adjusting the column width based on the longest content in a column 
        max_content_length = max(current_df[col].astype(str).apply(len).max(), len(col))
        tree.column(col, anchor="center", width=max_content_length * 13, stretch=False)

    #adding the rows to the treeview one by one
    for _, row in current_df.iterrows():
        tree.insert("", "end", values=list(row))

    #unbinding the left click event on the treeview to stop adjusting the column width manually
    tree.bind("<Button-1>", lambda event: "break")
    
    #packing the treeview
    tree.pack(fill="both", expand=True)


    #dataset summary section
    summary_frame = tk.Frame(root)
    summary_frame.pack(fill="x", pady=10)

    #calculating the statistics
    num_rows = current_df.shape[0] 
    num_columns = current_df.shape[1] 
    missing_values = current_df.isnull().sum().sum() 

    #displaying the summary
    summary_text = f"📊 Rows: {num_rows}   |   📌 Columns: {num_columns}   |   ❗ Missing Values: {missing_values}"
    summary_label = tk.Label(summary_frame, text=summary_text, font=("Arial", 12), fg="black", padx=10, pady=5)
    summary_label.pack()



#Step 2: Selecting the target variable
#This function is used to select the target variable from the dataframe
def step_2_select_target_variable():

    global df
    global current_step
    current_step = "step 2"

    #removing the existing widgets from the screen
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", pady=10)

    #back button to return to Step 1
    back_button = tk.Button(top_frame, text="Back", font=("Arial", 12), command=lambda: show_dataframe(df))
    back_button.pack(side="left", padx=10)

    #label for Step 2
    step2_label = tk.Label(top_frame, text="Step 2: Select Target Variable", font=("Arial", 16, "bold"))
    step2_label.pack(side="left", expand=True)

    #dropdown selection for the target variable
    dropdown_frame = tk.Frame(root)
    dropdown_frame.pack(pady=20)

    tk.Label(dropdown_frame, text="Select Target Variable:", font=("Arial", 12)).pack(side="left", padx=10)

    target_variable = tk.StringVar()
    target_dropdown = ttk.Combobox(dropdown_frame, textvariable=target_variable, values=list(df.columns), state="readonly")
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
    next_button = tk.Button(top_frame, text="Next", font=("Arial", 12), command=save_selected_target_var)
    next_button.pack(side="right", padx=10)



#Step 3: Select Input Variables
#This function is used to select the input variables from the dataframe
def step_3_select_input_variables():

    global df
    global selected_target_variable

    global current_step
    current_step = "step 3"

    #removing the existing widgets from the screen
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", pady=10)


    #back button
    back_button = tk.Button(top_frame, text="Back", font=("Arial", 12), command=step_2_select_target_variable)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = tk.Label(top_frame, text="Step 3: Select Input Variables", font=("Arial", 16, "bold"))
    table_label.pack(side="left", expand=True)

    #displaying the columns except the target variable

    selected_columns = {col: tk.BooleanVar(value=True) for col in df.columns if col != selected_target_variable}

    #checkbox for each column
    checkbox_frame = tk.Frame(root)
    checkbox_frame.pack(pady=20)

    for col, var in selected_columns.items():
        checkbox = tk.Checkbutton(checkbox_frame, text=col, variable=var)
        checkbox.pack(anchor="w")

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
    next_button = tk.Button(top_frame, text="Next", font=("Arial", 12), command=save_selected_columns_df)
    next_button.pack(side="right", padx=10)


#Step 4 - Preprocessing the data
#This function will be used to preprocess the data 
def step_4_data_preprocessing():
    
    global df
    global selected_target_variable

    global current_step
    current_step = "step 4"

    #removing the existing widgets from the screen
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", pady=10)


    #back button
    back_button = tk.Button(top_frame, text="Back", font=("Arial", 12), command=step_3_select_input_variables)
    back_button.pack(side="left",padx=10)

    #heading lable
    table_label = tk.Label(top_frame, text="Step 4: Data Preprocessing", font=("Arial", 16, "bold"))
    table_label.pack(side="left", expand=True)

    #Next button
    next_button = tk.Button(top_frame, text="Next", font=("Arial", 12), command=None)
    next_button.pack(side="right", padx=10)

    

#Buttons
build_model_button = tk.Button(root, text="Build a Model", font=("Arial", 14), command=build_model_button_function)
build_model_button.pack(pady=10)

test_model_button = tk.Button(root, text="Test a Model", font=("Arial", 14), command=None)
test_model_button.pack(pady=10)


#running the main window
root.mainloop()
