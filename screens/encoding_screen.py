import customtkinter as ctk
from tkinter import messagebox
from pandas.api.types import is_numeric_dtype
import config
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder
import pandas as pd


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
        loading_label.pack(pady=40)

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

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 12), command=back_to_preview)
        back_button.pack(side="left",padx=10)

        #heading lable
        heading_label = ctk.CTkLabel(top_frame, text="Step 5: Encoding", font=("Arial", 16, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 12), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_encoding_section, fg_color="gray10")
        middle_frame.pack(pady=30)

        #bulk button to bulk select actions
        #self.bulk_button =ctk.CTkSegmentedButton(middle_frame, values=["Lable All", "Ordinal All"], command=None)
        #self.bulk_button.pack(pady=10)

        #AI button to decide the encoding methods

        #function to handle the AI response
        def handle_answer(answer: str):

            print("UneeSeek says:", answer)

            #stoping and hiding the progress bar
            progress_bar.stop()
            progress_bar.pack_forget()

            #enabling the back and next buttons after the AI response
            back_button.configure(state="normal")
            next_button.configure(state="normal")

            #showing the AI response in a label
            ctk.CTkLabel(middle_frame, text=f"UneeSeek: {answer}", text_color="#3a7ebf", font=("Arial", 14)).pack(side="bottom", pady=10)
    

        progress_bar = ctk.CTkProgressBar(middle_frame, mode="indeterminate", width=100)

        #function to prompt the AI
        def prompt():

            #showing the progress bar while waiting for the AI response
            ai_button.pack_forget()
            progress_bar.pack(side="bottom", pady=10)
            progress_bar.start()

            #disabling the back and next buttons while waiting for the AI response
            back_button.configure(state="disabled")
            next_button.configure(state="disabled")

            #prompting the AI to answer the question

            prompt =("You are a concise assistant. Never reveal your chain-of-thought"
                    "only output the single-sentence answer for someone with no coding knowledge.\n"
                    "how should we decide the encoding methods for the different columns between ordinal, label and one-hot encoding?\n\n"
                    "Keep it short, Do not include any extra commentary.\n")
            
            print(prompt)
            config.chat_bot.ask( prompt, handle_answer)

        #Ask ai button
        ai_button = ctk.CTkButton(middle_frame, text="Ask AI for Help", font=("Arial", 14), command=lambda: prompt())
        ai_button.pack(side="bottom", pady=10)


        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=500, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)

        

        #creating a copy of the dataframe to work with
        config.df_encoded = config.df_handled_missing_values.copy()

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
                options = ["Label Encoding", "Ordinal Encoding"]
                col_name_label.configure(text=f"{col} (Target): ")

            else:
                options = ["One-Hot Encoding", "Label Encoding", "Ordinal Encoding"]
            
            #combo box for encoding
            combo = ctk.CTkComboBox(border_frame, values=options, state="readonly", width=250)
            combo.set("Choose Encoding Method")

            #saving the selected encoding method in the config
            if col == target:
                combo.configure(command=lambda val, t=target: config.saved_target_encoding.__setitem__(t, val))
            else:
                combo.configure(command=lambda val, c=col: config.saved_categorical_encoding.__setitem__(c, val))

            combo.grid(row=0, column=2, sticky="w", padx=10, pady=5)


        #message to show if there are no columns to encode
        no_columns_to_encode = not categorical_columns and is_numeric_dtype(target_series)

        if no_columns_to_encode:

            ctk.CTkLabel(scroll_frame, text="All Columns are numerical, click next to proceed to scaling.", font=("Arial", 14), text_color="green").pack(pady=20)
        
        def apply_encoding():
            #validating the selection for each columns
            
            #validation for target variable
            if not is_numeric_dtype(target_series) and not config.saved_target_encoding.get(target):
                messagebox.showerror("Error", "Please select encoding for the target variable.")
                return
            
            #validation for categorical columns
            cat_cols_not_selected = [c for c in categorical_columns if not config.saved_categorical_encoding.get(c)]
            if cat_cols_not_selected:
                messagebox.showerror("Error", f"Select encoding for: {', '.join(cat_cols_not_selected)}")
                return

            # confirmation dialog before applying encoding
            if not messagebox.askyesno(
                "Confirm",
                "You’ve selected encoding for every column.\nProceed to apply them?"
            ):
                return
    
            #encoding the target variable
            if not is_numeric_dtype(target_series):
                choice = config.saved_target_encoding[target]
                
                #lable encoding
                if choice == "Label Encoding":
                    le = LabelEncoder()
                    config.df_encoded[target] = le.fit_transform(config.df_encoded[target])


                #ordinal encoding
                elif choice == "Ordinal Encoding":
                    oe = OrdinalEncoder()
                    config.df_encoded[target] = oe.fit_transform(config.df_encoded[[target]]).astype(int)

            
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
                    


                elif choice == "Label Encoding":
                    le = LabelEncoder()
                    config.df_encoded[col] = le.fit_transform(config.df_encoded[col])


                elif choice == "Ordinal Encoding":
                    oe = OrdinalEncoder()
                    config.df_encoded[col] = oe.fit_transform(config.df_encoded[[col]]).astype(int)

            
            #showing the encoded dataframe
            from screens.df_preview_screen import DFPreviewScreen
            DFPreviewScreen().show_dataframe(config.df_encoded)
        
        next_button.configure(command=apply_encoding)

        loading_frame.pack_forget()
        entire_encoding_section.pack(fill="both", expand=True)