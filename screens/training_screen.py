import customtkinter as ctk
from tkinter import messagebox
import config
import pandas as pd


class TrainingScreen:
    def __init__(self):
        pass

    def show_training_screen(self):

        config.current_step = "step 6"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        
        entire_training_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_training_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_training_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.df_preview_screen import DFPreviewScreen
        def back_to_preview():
            config.current_step = "step 5"
            DFPreviewScreen().show_dataframe(config.df_encoded)

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=back_to_preview)
        back_button.pack(side="left",padx=10)

        #heading lable
        heading_label = ctk.CTkLabel(top_frame, text="Step 6: Training", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_training_section, fg_color="gray9")
        middle_frame.pack(fill="x",pady=30)



        scroll_frame = ctk.CTkScrollableFrame(middle_frame, width=700, height=600, fg_color="transparent")
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #creating 3 columns in the scrollable frame
        scroll_frame.columnconfigure(0, weight=1)


        #train test split section
        ######################################
        train_test_split_label = ctk.CTkLabel(scroll_frame, text="Train Test Split", font=("Arial", 15,))
        train_test_split_label.pack(pady=10)

        train_test_split_frame = ctk.CTkFrame(scroll_frame, fg_color="gray10", height=100, width=600)
        train_test_split_frame.pack(side ="left", pady=10)

        test_size_lable = ctk.CTkLabel(train_test_split_frame, text="Test Size: ", font=("Arial", 14))
        test_size_lable.pack(side="left", padx=10, pady=10)

        test_size_combo = ctk.CTkComboBox(train_test_split_frame, values=["10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%"], font=("Arial", 14), width=100)
        test_size_combo.set("20%")
        test_size_combo.pack(side="left", padx=0, pady=10)

        #default values for train test split
        config.test_size = 0.2
        config.train_size = 0.8

        config.test_size = int(test_size_combo.get().replace("%", "")) / 100
        config.train_size = 1 - config.test_size 

        train_size_lable = ctk.CTkLabel(train_test_split_frame, text="Train Size: ", font=("Arial", 14))
        train_size_lable.pack(side="left", padx=10, pady=10)

        train_size_value_lable = ctk.CTkLabel(train_test_split_frame, text=f"{round(config.train_size * 100)}%", font=("Arial", 14), text_color="gray")
        train_size_value_lable.pack(side="left", padx=0, pady=10)


        def update_sizes(choice):
            config.test_size = int(choice.replace("%", "")) / 100
            config.train_size = 1 - config.test_size 
            train_size_value_lable.configure(text=f"{round(config.train_size * 100)}%")

            #debugging
            print(f"Test Size: {config.test_size}, Train Size: {config.train_size}")

        test_size_combo.configure(command=update_sizes)
        print(f"Test Size: {config.test_size}, Train Size: {config.train_size}")



        #combo box for random state
        ##############################
        # random_state_lable = ctk.CTkLabel(train_test_split_frame, text="Random State: ", font=("Arial", 14), text_color="white")
        # random_state_lable.pack(side="left", padx=10, pady=10)

        random_state_combo = ctk.CTkComboBox(train_test_split_frame, values=["None", "0", "1", "21", "42", "99", "123", "2025"], font=("Arial", 14), width=180)
        random_state_combo.set("Random State: None")
        random_state_combo.pack(side="left", padx=20, pady=10)
        
        #default random state
        config.split_random_state = None
        
        def update_random_state(choice):
            if choice == "None":
                random_state_combo.set("Random State: None")
                config.split_random_state = None
            else:
                random_state_combo.set(f"Random State: {choice}")
                config.split_random_state = int(choice)

            #debugging
            print(f"Random State: {config.split_random_state}")

        random_state_combo.configure(command=update_random_state)
        print(f"Random State: {config.split_random_state}")

        






    

        loading_frame.pack_forget()
        entire_training_section.pack(fill="both", expand=True)