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

    def split_dataset(self):

        #function to split the data into train and test sets

        #separating the input and target variables
        X = config.df_encoded[config.selected_input_variables]
        y = config.df_encoded[config.selected_target_variable]


        #splitting the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.test_size, random_state=config.split_random_state)
        print(np.shape(X_train), np.shape(X_test), np.shape(y_train), np.shape(y_test))

        