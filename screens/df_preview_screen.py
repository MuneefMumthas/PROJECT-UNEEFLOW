import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tksheet import Sheet
from pandas.api.types import is_numeric_dtype
from ydata_profiling import ProfileReport
import threading
import tempfile
import os
import shutil
import webbrowser
from pathlib import Path
import customtkinter as ctk
import pandas as pd
import hashlib

import base64
import config

class DFPreviewScreen:
    def __init__(self):
        pass

    #Dataset preview function

    #methods to generalize the back and next buttons in the dataframe preview screen
    def show_dataframe_back(self):
        
        from screens.import_screen import ImportScreen
        from screens.input_var_screen import InputVarScreen 
        from screens.missing_val_screen import MissingValScreen

        if config.current_step == "step 1" or config.current_step == "step 2":
            ImportScreen().show_import_screen()

        elif config.current_step == "step 3":
            InputVarScreen().show_input_var_screen()
               
        elif config.current_step == "step 4":
            MissingValScreen().show_missing_val_screen()

        elif config.current_step == "step 5":
            from screens.encoding_screen import EncodingScreen
            EncodingScreen().show_encoding_screen()

    def show_dataframe_next(self):
        
        from screens.target_var_screen import TargetVarScreen
        from screens.missing_val_screen import MissingValScreen

        if config.current_step == "step 1" or config.current_step == "step 2":
            TargetVarScreen().show_target_var_screen()

        elif config.current_step == "step 3":
            MissingValScreen().show_missing_val_screen()
        
        elif config.current_step == "step 4":
            from screens.encoding_screen import EncodingScreen
            EncodingScreen().show_encoding_screen()
        
        elif config.current_step == "step 5":
            from screens.training_screen import TrainingScreen
            TrainingScreen().show_training_screen()


    #This function is used to display dataframe in a table whenever needed to preview the updated dataframe
    #################################################################################################################################### 
    def show_dataframe(self, current_df):

        row_hashes = pd.util.hash_pandas_object(current_df, index=True).values
        df_hash    = hashlib.sha256(row_hashes.tobytes()).hexdigest()
        self._df_hash = df_hash

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame to show while the entire dataframe section is being created
        #this is done to avoid flickering of the screen
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(expand=True)

        #creating a frame for the entire dataframe section
        entire_showdataframe_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_showdataframe_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_showdataframe_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=self.show_dataframe_back)
        back_button.pack(side="left",padx=10)

        #setting the name to differentiate between different dataframe previews
        if config.current_step == "step 1":
            current_dataset = "Dataset"

        elif config.current_step == "step 2":
            current_dataset = "Dataset"

        elif config.current_step == "step 3":
            current_dataset = "Refined Dataset"

        elif config.current_step == "step 4":
            current_dataset = "Cleaned Dataset"

        elif config.current_step == "step 5":
            current_dataset = "Encoded Dataset"
        
        else:
            current_dataset = "Dataset"

        #heading label
        heading_label = ctk.CTkLabel(top_frame, text=f"{current_dataset} Preview", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=self.show_dataframe_next)
        next_button.pack(side="right", padx=10)

        #container for the table
        container = ctk.CTkFrame(entire_showdataframe_section, fg_color="gray10")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        #disabling the pack propagation to avoid resizing issues
        container.pack_propagate(False)
        
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

        #calculating the statistics
        num_rows = current_df.shape[0] 
        num_columns = current_df.shape[1] 
        missing_values = current_df.isnull().sum().sum() 

        #displaying the summary
        summary_text = f"📊 Rows: {num_rows}   |   📌 Columns: {num_columns}   |   ❗ Missing Values: {missing_values}"
        summary_label = ctk.CTkLabel(summary_frame, text=summary_text, font=("Arial", 16), text_color="white", padx=10, pady=5)
        summary_label.pack()

        #data profile report button
        data_profile_button = ctk.CTkButton(summary_frame, text="Generate Profile Report", font=("Arial", 14), command=None)
        

        

        progress_bar = ctk.CTkProgressBar(summary_frame, mode="indeterminate", width=200)
        
        ##############################################
        #ydata profiling report section
        
        def create_profile_report():
            #creating the profile report for the current dataframe
            profile = ProfileReport(current_df, title="Data Profile Report", explorative=True, progress_bar=False, config_file=config.uneeflow_data_profile_config)
            
            
            #saving it to a temporary file as the size of the report can be large
            #and we don't want to keep it in memory
            tmp_dir  = tempfile.mkdtemp(prefix="uneeflow_profile_")

            #storing the temporary directory in the config for cleaning up later
            config.profile_temp_dirs.append(tmp_dir)

            html_path = os.path.join(tmp_dir, "report.html")

            profile.to_widgets
            profile.to_file(html_path)
            
            #copying the logo to the temporary directory to display it in the report
            #logo_src_path = config.uneeflow_logo
            #logo_filename = Path(logo_src_path).name
            #logo_dst_path = os.path.join(tmp_dir, logo_filename)
            #shutil.copy2(logo_src_path, logo_dst_path)


            html_path = Path(tmp_dir) / "report.html"
            logo_path = Path(config.uneeflow_logo)

            #reading the HTML file and encoding the logo to base64
            #this is done to embed the logo in the HTML report
            html = html_path.read_text(encoding="utf-8")
            b64  = base64.b64encode(logo_path.read_bytes()).decode("ascii")
            data_uri = f"data:image/png;base64,{b64}"

            #replacing the logo path in the HTML with the base64 encoded data URI
            html = html.replace(f'src="{logo_path.name}"', f'src="{data_uri}"')

            inlined_html = Path(tmp_dir) / "report_inlined.html"
            inlined_html.write_text(html, encoding="utf-8")

            #creating a file URI for the HTML report
            config.uri = Path(inlined_html).absolute().as_uri()  
            config.profile_cache[self._df_hash] = config.uri


        #function to open the html report in a web browser
        def open_profile_report():
            
            webbrowser.open(config.uri)
        

        def profile_report_button():
            
            #hiding the button and showing the progress bar
            data_profile_button.pack_forget()
            progress_bar.pack(pady=(20,20))
            progress_bar.start()

            #disabling navigation buttons to avoid glitching
            back_button.configure(state="disabled")
            next_button.configure(state="disabled")

            #creating a new thread to run the profiling report generation
            #this is done to avoid blocking the main thread and keep the UI responsive
            def report_generator():
                try:
                    create_profile_report()
                finally:
                    #back on the main thread
                    config.main_window.after(0, profile_done)

            threading.Thread(target=report_generator, daemon=True).start()

        def save_profile_report():
            
            #deriving the temporary folder path from the saved URI
            tmp_html_path = Path(config.uri.replace("file:///", ""))

            #letting user choose a destination directory
            destination_parent = Path(filedialog.askdirectory(title="Select folder to save the profile report"))
            if not destination_parent:
                return

            #file name
            file_name= f"UNEEFLOW {config.file_name} {current_dataset} Profile Report"
            html_file_name = f"{file_name}.html"
            
            #creating the destination file path
            destination_file_path = destination_parent / html_file_name

            #error handling
            try:
                #checking if the file already exists
                if destination_file_path.exists():
                    #if the file exists, asking the user if they want to overwrite it or create a copy
                    overwrite = messagebox.askyesnocancel(
                    "File Exists",
                    f"The file '{html_file_name}' already exists at the destination.\nDo you want to replace it?\n"
                    "Yes: Replace it\n"
                    "No: Save a copy with a numbered suffix\n"
                    "Cancel: Do nothing"
                    )

                    #overwriting the existing file
                    if overwrite is True:
                        shutil.copy2(tmp_html_path, destination_file_path)
                        messagebox.showinfo("Success", f"Profile report overwritten:\n{destination_file_path}")
                    
                    #creating a copy with numbered suffix
                    elif overwrite is False:
                        #creating copies with numbered suffixes
                        i = 1
                        while True:
                            #creating new file name with suffix
                            new_file_name_path = destination_parent / f"{file_name} ({i}).html"
                            if not new_file_name_path.exists():
                                shutil.copy2(tmp_html_path, new_file_name_path)
                                messagebox.showinfo("Success", f"Profile report saved as:\n{new_file_name_path}")
                                break
                            i += 1

                    #cancelling the save operation
                    else:
                        messagebox.showinfo("Cancelled", "Save operation was cancelled.")
                        
                #if the file does not exist creating it directly
                else:
                    shutil.copy2(tmp_html_path, destination_file_path)
                    messagebox.showinfo("Success", f"Profile report saved to:\n{destination_file_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save profile report:\n{e}")

        def profile_done():

            #stopping and hiding the progress bar
            progress_bar.stop()
            progress_bar.pack_forget()

            #changing the button text and command to open the report
            #data_profile_button.configure(text="View Profile Report", command=open_profile_report)
            #data_profile_button.pack(pady=(10,10))

            #save or view button
            save_view_profile_button = ctk.CTkSegmentedButton(summary_frame, values=["Save Profile Report", "View Profile Report"], command=None, font=("Arial", 14), width=150)
            save_view_profile_button.pack(pady=(10,10))

            def save_view_selection_command(value):
                if value == "View Profile Report":
                    open_profile_report()
                    save_view_profile_button.set(None)

                elif value == "Save Profile Report":
                    save_profile_report()
                    save_view_profile_button.set(None)

            #re-enabling the navigation buttons
            back_button.configure(state="normal")
            next_button.configure(state="normal")

            save_view_profile_button.configure(command=save_view_selection_command)
        
        if self._df_hash in config.profile_cache:
            #if the profile report is already generated for this dataframe, we can skip the generation
            #and directly show the report
            config.uri = config.profile_cache[self._df_hash]
            profile_done()

        else:
            data_profile_button.configure(text="Generate Profile Report", command=profile_report_button)
            data_profile_button.pack(pady=(10,10))
        

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
