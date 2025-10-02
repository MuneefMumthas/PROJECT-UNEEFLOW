import threading
from llama_cpp import Llama
import numpy as np
import config
import customtkinter as ctk
import pandas as pd
from sklearn.model_selection import train_test_split

#importing models
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

from sklearn.metrics import accuracy_score

class TrainingBackend:
    
    #class to manage the training backend
    
    def __init__(self):
        pass

    def train_model(self):

        #function to split the data into train and test sets

        #separating the input and target variables
        X = config.df_encoded.drop(columns=[config.selected_target_variable])
        y = config.df_encoded[config.selected_target_variable]

        #if classification stratify the split based on the target variable to maintain class distribution
        strat = y if config.task_type == "Classification" else None


        #splitting the data
        config.X_train, config.X_test, config.y_train, config.y_test = train_test_split(X, y, test_size=config.test_size, random_state=config.split_random_state, stratify=strat)
        print(np.shape(config.X_train), np.shape(config.X_test), np.shape(config.y_train), np.shape(config.y_test))


        #creating the model based on the selected model type
        model = None

        if config.task_type == "Classification":
            if config.selected_model == "Logistic Regression":
                model = LogisticRegression(max_iter=1000)
            elif config.selected_model == "Random Forest Classifier":
                model = RandomForestClassifier(n_estimators=100)
            elif config.selected_model == "Support Vector Classifier":
                model = SVC()
        
        elif config.task_type == "Regression":
            if config.selected_model == "Linear Regression":
                model = LinearRegression()
            elif config.selected_model == "Random Forest Regressor":
                model = RandomForestRegressor(n_estimators=100)
            elif config.selected_model == "Support Vector Regressor":
                model = SVR()

        if model is not None:
            #training the model
            model.fit(config.X_train, config.y_train)

            #saving the trained model to the config
            config.trained_model = model

            print(f"{config.selected_model} Model trained successfully.")

            predictions = model.predict(config.X_test)
            accuracy = accuracy_score(config.y_test, predictions)

            print(f"Model Accuracy on Test Set: {accuracy*100:.2f}%")

        from screens.model_evaluation_screen import EvaluationScreen
        EvaluationScreen().show_evaluation_screen()






    

        