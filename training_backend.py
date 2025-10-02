import threading
from llama_cpp import Llama
import numpy as np
import config
import customtkinter as ctk
import pandas as pd
from sklearn.model_selection import train_test_split

class TrainingBackend:
    
    #class to manage the training backend
    
    def __init__(self):
        pass

    def train_model(self):

        #function to split the data into train and test sets

        #separating the input and target variables
        X = config.df_encoded[config.selected_input_variables]
        y = config.df_encoded[config.selected_target_variable]

        #if classification stratify the split based on the target variable to maintain class distribution
        strat = y if config.task_type == "Classification" else None


        #splitting the data
        config.X_train, config.X_test, config.y_train, config.y_test = train_test_split(X, y, test_size=config.test_size, random_state=config.split_random_state, stratify=strat)
        print(np.shape(config.X_train), np.shape(config.X_test), np.shape(config.y_train), np.shape(config.y_test))





    

        