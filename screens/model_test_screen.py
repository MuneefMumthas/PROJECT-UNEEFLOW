import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter as ctk

import config
import joblib

class ModelTestScreen:
    
    def __init__(self):
        
        pass

    def show_model_test_screen(self):

        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()

        center_frame = ctk.CTkFrame(config.main_window, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.40, anchor="center")
        
        #heading
        heading_label = ctk.CTkLabel(center_frame, text="Model Deployment & Testing", font=("Arial", 20, "bold"))
        heading_label.pack(pady=(0, 50)) 

        #import model pkl button
        import_model_button = ctk.CTkButton(center_frame, text="Load Model.pkl", font=("Arial", 16), command=self.load_model_and_test, width=180, height=40)
        import_model_button.pack(pady=(0, 25))


        #back button
        from screens.main_menu_screen import MainMenuScreen
        back_button = ctk.CTkButton(center_frame, text="Back", font=("Arial", 16), command=lambda: MainMenuScreen().back_to_main_menu(), width=100, height=40)
        back_button.pack(pady=(10,0))

    def load_model_and_test(self):

        #loading the model pkl

        pkl_path = filedialog.askopenfilename(title="Select model (.pkl)", filetypes=[("Pickle files", "*.pkl")])
        
        if not pkl_path:
            return
        
        try:
            #loading the pkl via joblib and saving it inside the config
            config.model_package = joblib.load(pkl_path)
            print(config.model_package)

            #checking if the file loaded is from uneeflow to avoid bug if unknown files are imported
            uneeflow_pkl = config.model_package.get("uneeflow_pkl", False)

            if not uneeflow_pkl:
                messagebox.showerror(
                    "Invalid File",
                    "This file is not a valid UNEEFLOW model.\n"
                    "Please select a .pkl exported from UNEEFLOW."
                )
                return
            
            #assigning the objects of the pkl file to self variables
            self.pipe = config.model_package.get("model_pipeline", None)
            self.features = config.model_package.get("feature_columns", [])
            self.target_lable_encoder = config.model_package.get("target_label_encoder", None)
            self.saved_categorical_encoding = config.model_package.get("encoders_used_for_features", {})


        #error handling
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            return


        #removing all widgets from the window
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(expand=True)

        #creating a frame for the entire section
        entire_test_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_test_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_test_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=self.show_model_test_screen)
        back_button.pack(side="left",padx=10)

        #heading label
        heading_label = ctk.CTkLabel(top_frame, text="Enter Data to Predict", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_test_section, fg_color="gray10", height=600)
        middle_frame.pack(pady=0)


        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=500, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)


        #hiding the scrollbar if there are 8 columns or less
        if len(self.features) > 8:
            scroll_frame._scrollbar.grid()
        else:
            scroll_frame._scrollbar.grid_remove()

        #dictionary to save the entry boxes for each column
        self.entry_boxes = {}

        #iterating through each features from the model pkl
        for i, col in enumerate(self.features):

            #creating border for each row using a lower height frame
            border_frame = ctk.CTkFrame(scroll_frame, fg_color="gray8", border_color="gray10", border_width=1)
            border_frame.grid(row=i, column=0, columnspan=3, sticky="ew")
            
            #making the columns equal width for better alignment
            for col_idx in (0, 1, 2):
                border_frame.grid_columnconfigure(col_idx, weight=1, uniform="cols")


            #column name label
            col_name_label = ctk.CTkLabel(border_frame, text=f"{col}: ", font=("Arial", 16), text_color="white", wraplength=180, bg_color="gray8")
            col_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(15,15))

            #entry box
            col_entry = ctk.CTkEntry(border_frame, width=250, placeholder_text=f"Enter {col}")
            col_entry.grid(row=0, column=2, sticky="w", padx=10, pady=5)
            self.entry_boxes[col] = col_entry

        #frame for prediction section
        prediction_frame = ctk.CTkFrame(middle_frame, fg_color="gray10")
        prediction_frame.pack(fill="both")
        
        #prediction button
        predict_button = ctk.CTkButton(prediction_frame, text="Predict", font=("Arial", 14), command=lambda: self.predict(prediction_lable))
        predict_button.pack(side="bottom", pady=(15,20))

        #lable for prediction
        prediction_lable = ctk.CTkLabel(prediction_frame, text="Answer", font=("Arial", 20, "bold"), text_color= "#3a7ebf")
        prediction_lable.pack(side="bottom", pady=(20,10))


        loading_frame.pack_forget()
        entire_test_section.pack(fill="both", expand=True)

    def predict(self, result_label: ctk.CTkLabel):
        

        #dictionary to store user input for each features
        data_dict = {}

        for col in self.features:
            entry_box = self.entry_boxes.get(col)
            value = entry_box.get().strip()


            #checking if the column is encoded to keep the value as a string
            #lower casing as the model was trained on lowercased values
            if col in self.saved_categorical_encoding:
                data_dict[col] = value.lower()

            #converting str to numerical if the col is numerical and not encoded before
            else:
                try:
                    data_dict[col] = float(value)

                except Exception as e:
                    messagebox.showerror("Invalid Input", f"{e}\nPlease enter a numeric value for {col}")
                    return

        df = pd.DataFrame([data_dict], columns=self.features)

        #predicting
        try:
            prediction = self.pipe.predict(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict:\n{e}")
            return

        #inverse transforming if there is a label encoder
        final_pred = prediction[0]

        if self.target_lable_encoder is not None:
            try:
                final_pred = self.target_lable_encoder.inverse_transform(prediction)[0]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to predict:\n{e}")
                return

        result_label.configure(text=f"{final_pred}")
