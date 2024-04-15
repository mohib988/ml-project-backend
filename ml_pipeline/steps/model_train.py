import logging
import pandas as pd
import numpy as np
from zenml import step
from src.models.random_forest import RandomForestModel 
from sklearn.base import ClassifierMixin
import mlflow
from zenml.client import Client
from typing import List, Union
experiment_tracker=Client().active_stack.experiment_tracker 


@step(experiment_tracker=experiment_tracker.name)
def train_model(X: pd.DataFrame) -> Union[np.ndarray, List[int]]:
    """Train the model
    Args:
        X_train: pd.DataFrame: Training data
        y_train: pd.Series: Training labels
    Returns:
        ClassifierMixin: Trained model
    """
    mlflow.sklearn.autolog()
    model=RandomForestModel()
    predict =model.train_random_forest(X)
    logging.info("Training the model")
    return predict
