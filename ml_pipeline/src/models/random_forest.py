from sklearn.model_selection import train_test_split
import pickle
import joblib
import logging
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
from typing import List, Union

# Load the model
import matplotlib.pyplot as plt
class RandomForestModel:
    def train_random_forest(self,X)->Union[np.ndarray, List[int]]:
        # Create the training and testing sets

        # Fit a random forest classifier model to our data
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the pickle file
            pickle_file_path = os.path.join(current_directory, 'rf_model.joblib')

        # Load the model from the pickle file
            model = joblib.load(pickle_file_path)

            X["inv_len"]=len(X["invoice_no"].astype(str))
            X["sales_tax"]=X['rate_value'] * (1 + X['sales_tax']) - X['sales_value']
            X=X[[ 'rate_value', 'sales_value',
            'sales_tax',"inv_len",
            "delay"]]
            logging.info("Training the model",X)
            X.fillna(0)
            predict=model.predict(X[[ 'rate_value', 'sales_value',
            'sales_tax',"inv_len",
            "delay"]])
            return predict
        except Exception as e:
            logging.error("error in Random Forest",e)
            raise e

    
        # Obtain model predictions
    