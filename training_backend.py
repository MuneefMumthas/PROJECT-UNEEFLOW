import threading
from tkinter import messagebox
from llama_cpp import Llama
import numpy as np
import config
import customtkinter as ctk
import pandas as pd
import threading
from sklearn.model_selection import train_test_split

#importing models
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor




class TrainingBackend:
    
    #class to manage the training backend
    
    def __init__(self):
        pass

    def train_model(self):

        
        #creating the model based on the selected model type
        model = None

        if config.task_type == "Classification":

            if config.selected_model == "Logistic Regression":
                model = LogisticRegression(max_iter=1000)

            elif config.selected_model == "Random Forest Classifier":
                model = RandomForestClassifier(n_estimators=100)

            elif config.selected_model == "Gradient Boosting Classifier":
                model = GradientBoostingClassifier(n_estimators=100)
        
        elif config.task_type == "Regression":

            if config.selected_model == "Linear Regression":
                model = LinearRegression()

            elif config.selected_model == "Random Forest Regressor":
                model = RandomForestRegressor(n_estimators=100)

            elif config.selected_model == "Gradient Boosting Regressor":
                model = GradientBoostingRegressor(n_estimators=100)

        #function to train the model in a separate thread
        def train():

            #function to split the data into train and test sets

            #separating the input and target variables
            X = config.df_encoded.drop(columns=[config.selected_target_variable])
            y = config.df_encoded[config.selected_target_variable]

            #if classification stratify the split based on the target variable to maintain class distribution
            strat = y if config.task_type == "Classification" else None


            #splitting the data
            config.X_train, config.X_test, config.y_train, config.y_test = train_test_split(X, y, test_size=config.test_size, random_state=config.split_random_state, stratify=strat)
            print(np.shape(config.X_train), np.shape(config.X_test), np.shape(config.y_train), np.shape(config.y_test))

            #training the model
            model.fit(config.X_train, config.y_train)

            #saving the trained model to the config
            config.trained_model = model

            print(f"{config.selected_model} Model trained successfully.")

        #worker function to run the training in a separate thread
        def worker():

            training_successful = False

            try:
                train()
                training_successful = True

            except Exception as e:
                err_msg = str(e)

                def training_failed():
                    
                    #showing the training screen again to allow the user to retry
                    from screens.training_screen import TrainingScreen
                    TrainingScreen().show_training_screen()

                    #error message
                    messagebox.showerror("Training failed", err_msg)
                    
                config.main_window.after(0, training_failed())
                
                return

            #if the training is successfull moving onto evaluation
            if training_successful:
                config.main_window.after(0, predict_and_evaluate)


        #function to predict and evaluate the model and move to the evaluation screen
        def predict_and_evaluate():

            #evaluating the model on the test set
            config.predictions = model.predict(config.X_test)
            
            #stoping the progress bar and moving to the evaluation screen
            training_progess_bar.stop()

            from screens.model_evaluation_screen import EvaluationScreen
            EvaluationScreen().show_evaluation_screen()
            

        if model is not None:
            
            #clearing the screen
            for widget in config.main_window.winfo_children():
                widget.destroy()
            
            #creating a frame
            progress_frame = ctk.CTkFrame(config.main_window, fg_color="gray10")
            progress_frame.pack(fill="both", expand=True)

            progress_label = ctk.CTkLabel(progress_frame, text="Training the model, please wait...", font=("Arial", 20, "bold"), text_color="white")
            progress_label.place(relx=0.5, rely=0.44, anchor="center")
            
            #creating a progress bar to show the training progress
            training_progess_bar = ctk.CTkProgressBar(progress_frame, mode="indeterminate", width=350, height=15)
            training_progess_bar.place(relx=0.5, rely=0.50, anchor="center")
            training_progess_bar.start()

            #running the training in a separate thread to avoid blocking the UI
            threading.Thread(target=worker, daemon=True).start()

        


            

            
            
            

        






    

        