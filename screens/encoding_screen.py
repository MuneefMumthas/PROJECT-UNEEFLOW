import customtkinter as ctk
from tkinter import messagebox
from pandas.api.types import is_numeric_dtype
import config
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder
import pandas as pd

from sklearn.compose import ColumnTransformer


class EncodingScreen:
    def __init__(self):
        pass

    def show_encoding_screen(self):

        config.current_step = "step 5"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(expand=True)

        #creating a frame for the entire section
        
        entire_encoding_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_encoding_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_encoding_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.df_preview_screen import DFPreviewScreen
        def back_to_preview():
            config.current_step = "step 4"
            DFPreviewScreen().show_dataframe(config.df_handled_missing_values)

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=back_to_preview)
        back_button.pack(side="left",padx=10)

        #heading label
        heading_label = ctk.CTkLabel(top_frame, text="Step 5: Encoding", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_encoding_section, fg_color="gray10", height=600)
        middle_frame.pack(pady=0)


        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=500, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)

        

        #creating a copies of the dataframe to work with

        #this copy will be used to show the encoded dataframe in the preview screen
        config.df_encoded = config.df_handled_missing_values.copy()

        #this copy will be used to build piplines and train models without affecting the original dataframe
        config.df_not_encoded = config.df_handled_missing_values.copy() 

        target = config.selected_target_variable
        target_series = config.df_encoded[target]

        categorical_columns = [c for c in config.selected_input_variables if not is_numeric_dtype(config.df_encoded[c])]

        columns_to_encode = []

        #creating a list of columns to encode
        if not is_numeric_dtype(target_series):
            columns_to_encode.append(target)
        columns_to_encode.extend(categorical_columns)

        #hiding the scrollbar if there are 8 columns or less
        if len(columns_to_encode) > 8:
            scroll_frame._scrollbar.grid()
        else:
            scroll_frame._scrollbar.grid_remove()

        #dictionary to store actions for each option in the combo box
        actions = {}

        for i, col in enumerate(columns_to_encode):

            #creating border for each row using a lower height frame
            border_frame = ctk.CTkFrame(scroll_frame, fg_color="gray8", border_color="gray10", border_width=1)
            border_frame.grid(row=i, column=0, columnspan=3, sticky="ew")
            
            #making the columns equal width for better alignment
            for col_idx in (0, 1, 2):
                border_frame.grid_columnconfigure(col_idx, weight=1, uniform="cols")


            #column name label
            col_name_label = ctk.CTkLabel(border_frame, text=f"{col}: ", font=("Arial", 16), text_color="white", wraplength=180, bg_color="gray8")
            col_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(15,15))

            if col == target:
                options = ["Label Encoding"]
                col_name_label.configure(text=f"{col} (Target): ")

            else:
                options = ["One-Hot Encoding", "Ordinal Encoding"]
            
            #combo box for encoding
            combo = ctk.CTkComboBox(border_frame, values=options, state="readonly", width=250)
            combo.set("Choose Encoding Method")

            #setting the combo box to the previously selected value if exists
            if col in config.saved_categorical_encoding:
                combo.set(config.saved_categorical_encoding[col])

            elif col == target and col in config.saved_target_encoding:
                combo.set(config.saved_target_encoding[col])

            #saving the selected encoding method in the config
            if col == target:
                combo.configure(command=lambda val, t=target: config.saved_target_encoding.__setitem__(t, val))
            else:
                combo.configure(command=lambda val, c=col: config.saved_categorical_encoding.__setitem__(c, val))

            combo.grid(row=0, column=2, sticky="w", padx=10, pady=5)
            actions[col] = combo

        #print("category encoding: ", config.saved_categorical_encoding)
        #print("target encoding: ", config.saved_target_encoding)


        #message to show if there are no columns to encode
        no_columns_to_encode = not categorical_columns and is_numeric_dtype(target_series)

        if no_columns_to_encode:

            ctk.CTkLabel(scroll_frame, text="All Columns are numerical, click next to proceed to Training.", font=("Arial", 14, "bold"), text_color="green").pack(pady=20)
        
        def apply_encoding():

            #resetting the encoding selections at the start
            config.ohe_columns = []
            config.ordinal_encode_cols = []
            config.transformers = []
            config.col_transformer = None

            #validating the selection for each columns
            if no_columns_to_encode:
                from screens.training_screen import TrainingScreen
                TrainingScreen().show_training_screen()
                
            else:
                cols_without_selection = [
                    col
                    for col, combo in actions.items()
                    if combo.get() == "Choose Encoding Method"
                ]
                if cols_without_selection:
                    messagebox.showerror(
                        "Error",
                        "Please select an encoding method for the following columns:\n  "
                        + "\n  ".join(cols_without_selection)
                    )
                    return
                i
                # confirmation dialog before applying encoding
                if not messagebox.askyesno(
                    "Confirm",
                    "You’ve selected encoding for every column.\nProceed to apply them?"
                ):
                    return
                
                
                #encoding the target variable
                if not is_numeric_dtype(target_series):
                    choice = config.saved_target_encoding[target]
                    
                    #label encoding
                    if choice == "Label Encoding":
                        le = LabelEncoder()
                        config.df_encoded[target] = le.fit_transform(config.df_encoded[target])


                
                #encoding the categorical columns
                for col in categorical_columns:
                    choice = config.saved_categorical_encoding[col]

                    #one hot encoding
                    if choice == "One-Hot Encoding":


                        ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                        encoded_col = ohe.fit_transform(config.df_encoded[[col]])

                        #creating new meaningful column names
                        new_col_name = ohe.get_feature_names_out([col])

                        #creating a new dataframe with the encoded column
                        df_ohe = pd.DataFrame(encoded_col, columns=new_col_name, index=config.df_encoded.index)

                        #dropping the original column and concatenating the new dataframe
                        config.df_encoded = pd.concat([config.df_encoded.drop(columns=[col]), df_ohe], axis=1)

                        config.ohe_columns.append(col)

                        

                    elif choice == "Ordinal Encoding":
                        oe = OrdinalEncoder()
                        config.df_encoded[col] = oe.fit_transform(config.df_encoded[[col]]).astype(int)

                        config.ordinal_encode_cols.append(col)
                
                #creating the column transformer for the encoding steps
                ####
                #one hot enoding transformer
                if config.ohe_columns:
                    config.transformers.append(('OneHotEncoding', OneHotEncoder(handle_unknown='ignore'), config.ohe_columns))

                #ordinal encoding transformer
                if config.ordinal_encode_cols:
                    config.transformers.append(('OrdinalEncoding', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), config.ordinal_encode_cols))

                #creating the column transformer with both encoding methods
                config.col_transformer = ColumnTransformer(transformers=config.transformers, remainder='passthrough')
                print(config.col_transformer)
                ####

                #showing the encoded dataframe
                from screens.df_preview_screen import DFPreviewScreen
                DFPreviewScreen().show_dataframe(config.df_encoded)

                #debugging
                #print("category encoding: ", config.saved_categorical_encoding)
                #print("target encoding: ", config.saved_target_encoding)
                print("ohe columns: ", config.ohe_columns)
                print("ordinal encode columns: ", config.ordinal_encode_cols)
        
        next_button.configure(command=apply_encoding)

        #AI button and response frame
        ai_help_frame = ctk.CTkScrollableFrame(middle_frame, fg_color="gray10")
        ai_help_frame.pack(fill="both")
        ai_help_frame._scrollbar.grid_remove()

        def prompt():

            #showing the progress bar while waiting for the AI response
            ai_button.pack_forget()
            
            #progress bar
            progress_bar = ctk.CTkProgressBar(ai_help_frame, mode="indeterminate", width=100)
            progress_bar.pack(side="bottom", pady=10)
            progress_bar.start()

            #disabling the back and next buttons while waiting for the AI response
            back_button.configure(state="disabled")
            next_button.configure(state="disabled")

            response_label = ctk.CTkLabel(ai_help_frame, text="", text_color="#3a7ebf", wraplength=650, font=("Arial", 14), justify="left")

            response_label.pack(side="bottom", pady=10)

            #prompting the AI to answer the question
            config.chat_bot.ask(
                "You are a concise assistant."
                "Only output a single short paragraph that explains the concept in simple terms for someone with no coding knowledge.\n\n"
                "Explain when to use label encoding, ordinal encoding (rank), and one-hot encoding. (ALL in 1 paragraph please)\n\n", 
                response_label, progress_bar, back_button, next_button
            )

            ai_help_frame._scrollbar.grid()


        #Ask ai button
        ai_button = ctk.CTkButton(ai_help_frame, text="Whats the difference?, Ask UneePhi", font=("Arial", 14), command=lambda: prompt())
        ai_button.pack(side="bottom", pady=10)

        loading_frame.pack_forget()
        entire_encoding_section.pack(fill="both", expand=True)