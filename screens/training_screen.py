import customtkinter as ctk
from tkinter import messagebox
import config
import pandas as pd
from pandas.api.types import is_numeric_dtype


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
        loading_label.pack(expand=True)

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
        middle_frame = ctk.CTkFrame(entire_training_section, fg_color="gray10")
        middle_frame.pack(fill="x",pady=30)


        center_frame = ctk.CTkFrame(middle_frame, width=700, height=600, fg_color="transparent")
        center_frame.pack(padx=50, pady=10, fill="both", expand=True)


        #train test split section
        ###############################################################
        
        train_test_split_section_frame = ctk.CTkFrame(center_frame, fg_color="gray8", height=100, width=700, corner_radius=10)
        train_test_split_section_frame.pack(anchor="center", pady=10, fill="x")

        train_test_split_label = ctk.CTkLabel(train_test_split_section_frame, text="Train Test Split", font=("Arial", 15, "bold"))
        train_test_split_label.pack(pady=10)

        #this frame will hold all the widgets to keep them in the center
        train_test_frame = ctk.CTkFrame(train_test_split_section_frame, fg_color="gray8")
        train_test_frame.pack(anchor="center")

        test_size_lable = ctk.CTkLabel(train_test_frame, text="Test Size: ", font=("Arial", 14))
        test_size_lable.pack(side="left", padx=5, pady=10)

        test_size_combo = ctk.CTkComboBox(train_test_frame, values=["10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%"], font=("Arial", 14), width=100, state="readonly")
        test_size_combo.set("20%")
        test_size_combo.pack(side="left", padx=5, pady=10)

        #default values for train test split
        config.test_size = 0.2
        config.train_size = 0.8

        config.test_size = int(test_size_combo.get().replace("%", "")) / 100
        config.train_size = 1 - config.test_size 

        train_size_lable = ctk.CTkLabel(train_test_frame, text="Train Size: ", font=("Arial", 14))
        train_size_lable.pack(side="left", padx=10, pady=10)

        train_size_value_lable = ctk.CTkLabel(train_test_frame, text=f"{round(config.train_size * 100)}%", font=("Arial", 14), text_color="gray")
        train_size_value_lable.pack(side="left", padx=5, pady=10)


        def update_sizes(choice):
            config.test_size = int(choice.replace("%", "")) / 100
            config.train_size = 1 - config.test_size 
            train_size_value_lable.configure(text=f"{round(config.train_size * 100)}%")

            #debugging
            print(f"Test Size: {config.test_size}, Train Size: {config.train_size}")

        test_size_combo.configure(command=update_sizes)
        print(f"Test Size: {config.test_size}, Train Size: {config.train_size}")



        #combo box for random state
        ###############################################################

        random_state_combo = ctk.CTkComboBox(train_test_frame, values=["None", "0", "1", "21", "42", "99", "123", "2025"], font=("Arial", 14), width=180, state="readonly")
        random_state_combo.set("Random State: None")
        random_state_combo.pack(side="left", padx=10, pady=10)
        
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

        
        #Task and Model Selection Section
        ###############################################################

        task_model_selection_frame = ctk.CTkFrame(center_frame, fg_color="gray8", height=100, width=700, corner_radius=10)
        task_model_selection_frame.pack(anchor="center", pady=10, fill="x")

        model_selection_label = ctk.CTkLabel(task_model_selection_frame, text="Model Selection", font=("Arial", 15, "bold"))
        model_selection_label.pack(pady=10)

        #Task type selection
        ####################################

        #this frame will hold all the widgets to keep them in the center
        task_selection_frame = ctk.CTkFrame(task_model_selection_frame, fg_color="gray8")
        task_selection_frame.pack(anchor="center")

        task_type_combo_box = ctk.CTkComboBox(task_selection_frame, values=["Regression", "Classification"], font=("Arial", 14), width=150, state="readonly")
        task_type_combo_box.pack(side="left", pady=10, padx=10)

        #finding the task type based on the target variable using sklearn type_of_target
        from sklearn.utils.multiclass import type_of_target

        target_type = type_of_target(config.df_handled_missing_values[config.selected_target_variable])

        def set_task_type():
            if  target_type in ['binary', 'multiclass', 'multilabel-indicator']:
                task_type_combo_box.set("Classification")
                config.task_type = "Classification"

            elif target_type in ['continuous']:
                task_type_combo_box.set("Regression")
                config.task_type = "Regression"

            task_type_combo_box.configure(state="disabled")
        
        #running it when the screen loads
        set_task_type()
        
        #debugging
        print(f"Task Type: {config.task_type}")

        #checkbox to overide and the function to enable/disable the combo box
        overide_task_var = ctk.BooleanVar(value=False)

        def overide_task_command():
            if overide_task_var.get():
                task_type_combo_box.configure(state="readonly")

            else:
                
                #setting the task type based on the target variable
                set_task_type()

                #updating the model options based on the task type
                update_model_options()

            #debugging
            print(f"Task Type: {config.task_type}")

        overide_task_check_box = ctk.CTkCheckBox(task_selection_frame, text="Overide", variable=overide_task_var, command=overide_task_command, font=("Arial", 14))
        overide_task_check_box.pack(padx=10, pady=15)

        #function to update the task type when selected from the combo box
        def update_task_type(choice):
            config.task_type = choice

            #debugging
            print(f"Task Type: {config.task_type}")

            update_model_options()
        
        task_type_combo_box.configure(command=update_task_type)

        ####################################

        #model selection section
        ####################################
        
        #this frame will hold all the widgets to keep them in the center
        model_selection_frame = ctk.CTkFrame(task_model_selection_frame, fg_color="gray8")
        model_selection_frame.pack(anchor="center")


        model_combo_box = ctk.CTkComboBox(model_selection_frame, values=[], font=("Arial", 14), width=300, state="readonly")
        model_combo_box.pack(side="left", padx=10, pady=10)

        #function to update the model options based on the task type
        def update_model_options():

            if config.task_type == "Classification":
                model_combo_box.configure(values=["Logistic Regression", "Random Forest Classifier", "Gradient Boosting Classifier"])
                model_combo_box.set("Select Model")
                config.selected_model = None
                print(f"Selected Model: {config.selected_model}")
            
            elif config.task_type == "Regression":
                model_combo_box.configure(values=["Linear Regression", "Random Forest Regressor", "Gradient Boosting Regressor"])
                model_combo_box.set("Select Model")
                config.selected_model = None
                print(f"Selected Model: {config.selected_model}")

        
        #running it when the screen loads
        update_model_options()

        #saving the selected model to config
        def save_selected_model(choice):
            config.selected_model = choice

            #debugging
            print(f"Selected Model: {config.selected_model}")
        
        model_combo_box.configure(command=save_selected_model)

        config.trained_model = None

        ###############################################################

        
        def next_button_command():

            #checking if a model is selected before proceeding
            if config.selected_model is None:
                messagebox.showerror("Error", "Please select a model before proceeding.")
                return
            
            #validating if the selected target var is categorical but the task type is regression
            #selected df_handled_missing_values to check as it has the missing values handled and doesn't get affected by encoding
            elif not is_numeric_dtype(config.df_handled_missing_values[config.selected_target_variable]) and config.task_type == "Regression":
                messagebox.showerror(
                    "Invalid Selection",
                    "The target variable is categorical. Please select 'Classification' instead."
                )
                return
            
            else:
                from training_backend import TrainingBackend
                TrainingBackend().train_model()


        #linking the next button to the model training then to evaluation screen

        next_button.configure(command=next_button_command)

        

        loading_frame.pack_forget()
        entire_training_section.pack(fill="both", expand=True)