import customtkinter as ctk
from tkinter import messagebox
import config
import pandas as pd

#classification metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#regression metrics
from sklearn.metrics import r2_score, mean_squared_error, root_mean_squared_error, mean_absolute_error


class EvaluationScreen:
    def __init__(self):
        pass


    def show_evaluation_screen(self):

        config.current_step = "step 7"

        #removing the existing widgets from the screen
        for widget in config.main_window.winfo_children():
            widget.destroy()

        #loading frame
        loading_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
        loading_frame.pack(fill="both", expand=True)

        loading_label = ctk.CTkLabel(loading_frame, text="Loading...", font=("Arial", 20, "bold"), text_color="white")
        loading_label.pack(pady=40)

        #creating a frame for the entire section
        
        entire_evaluation_section = ctk.CTkFrame(config.main_window, fg_color="gray10")
        
        #forgetting the section to show only after all the widgets are created
        entire_evaluation_section.pack_forget()

        top_frame = ctk.CTkFrame(entire_evaluation_section, fg_color="gray10")
        top_frame.pack(fill="x", pady=10)

        #back button
        from screens.training_screen import TrainingScreen

        back_button = ctk.CTkButton(top_frame, text="Back", font=("Arial", 14), command=TrainingScreen().show_training_screen)
        back_button.pack(side="left",padx=10)

        #heading lable
        heading_label = ctk.CTkLabel(top_frame, text="Step 7: Model Evaluation", font=("Arial", 20, "bold"))
        heading_label.pack(side="left", expand=True)

        #Next button
        next_button = ctk.CTkButton(top_frame, text="Next", font=("Arial", 14), command=None)
        next_button.pack(side="right", padx=10)

        #middle frame for content
        middle_frame = ctk.CTkFrame(entire_evaluation_section, fg_color="gray10")
        middle_frame.pack(fill="both",pady=(20,0))

        center_frame = ctk.CTkFrame(middle_frame, width=700, height=700, fg_color="gray10")
        center_frame.pack(padx=50, pady=10, fill="both", expand=True)

        #model configuration details
        #####################################
        model_config_frame = ctk.CTkScrollableFrame(center_frame, fg_color="gray8", height=220)
        model_config_frame.pack(anchor="center", pady=10, fill="both")

        model_config_label = ctk.CTkLabel(model_config_frame, text="Model Config Summary", font=("Arial", 15, "bold"),  text_color="white")
        model_config_label.pack(pady=(5, 10))

        #creating a dictionary to hold the model details
        model_details = {
            
            "Target Variable": config.selected_target_variable,
            "Features/Input Variables": ", ".join(config.selected_input_variables),
            "Task Type":config.task_type,
            "Selected Model": config.selected_model,
            "Train Size": f"{round(config.train_size * 100)}%",
            "Test Size": f"{round(config.test_size * 100)}%",
            "Random State for Data Split": config.split_random_state if config.split_random_state is not None else "None"
        }

        #displaying the model details in the frame
        for name, value in model_details.items():
            row = ctk.CTkFrame(model_config_frame, fg_color="transparent")
            row.pack(anchor="w", pady=4)

            name_label = ctk.CTkLabel(row, text=f"{name}:", font=("Arial", 13, "bold"))
            name_label.pack(side="left", padx=(20,10))

            value_label = ctk.CTkLabel(row, text=value, font=("Arial", 13), text_color="gray", wraplength=400, justify="left")
            value_label.pack(side="left")


        #model Performance Metrics
        #####################################
        evaluation_metrics_frame = ctk.CTkFrame(center_frame, fg_color="gray8", height=220)
        evaluation_metrics_frame.pack(anchor="center", pady=10, fill="x")

        evaluation_label = ctk.CTkLabel(evaluation_metrics_frame, text="Model Performance Metrics", font=("Arial", 15, "bold"),  text_color="white")
        evaluation_label.pack(pady=10)
        
        #calculating the evaluation metrics
        if config.trained_model is not None:
            if config.task_type == "Classification":

                #calculating the metrics
                accuracy = accuracy_score(config.y_test, config.predictions)
                precision = precision_score(config.y_test, config.predictions, average='weighted')
                recall = recall_score(config.y_test, config.predictions, average='weighted')
                f1 = f1_score(config.y_test, config.predictions, average='weighted')
                
                #dictionary to hold the metrics and their values
                metrics = {
                    "Accuracy": f"{accuracy*100:.2f}%",
                    "Precision": f"{precision*100:.2f}%",
                    "Recall": f"{recall*100:.2f}%",
                    "F1 Score": f"{f1*100:.2f}%"
                }

            elif config.task_type == "Regression":
                
                #calculating the metrics
                r2score = r2_score(config.y_test, config.predictions)
                mse = mean_squared_error(config.y_test, config.predictions)
                rmse = root_mean_squared_error(config.y_test, config.predictions)
                mae = mean_absolute_error(config.y_test, config.predictions)

                #dictionary to hold the metrics and their values
                metrics = {
                    "R² Score": f"{r2score*100:.2f}%",
                    "Mean Squared Error (MSE)": f"{mse:,.2f}",
                    "Root Mean Squared Error (RMSE)": f"{rmse:,.2f}",
                    "Mean Absolute Error (MAE)": f"{mae:,.2f}"
                }
            
            #displaying the metrics in the frame
            for name, value in metrics.items():
                row = ctk.CTkFrame(evaluation_metrics_frame, fg_color="transparent")
                row.pack(anchor="w", pady=4)

                name_label = ctk.CTkLabel(row, text=f"{name}:", font=("Arial", 13, "bold"),)
                name_label.pack(side="left", padx=(20,10))

                value_label = ctk.CTkLabel(row, text=value, font=("Arial", 13), text_color="#50DF9C")
                value_label.pack(side="left")
            
        #ai review section
        ai_review_frame = ctk.CTkFrame(center_frame, fg_color="gray8", height=220)
        ai_review_frame.pack(anchor="center", pady=10, fill="x")

        
        #Ask ai button
        ai_button = ctk.CTkButton(ai_review_frame, text="Get Insights with UneeSeek AI", font=("Arial", 14), command=None)
        ai_button.pack(side="bottom", pady=10)


        loading_frame.pack_forget()
        entire_evaluation_section.pack(fill="both", expand=True)