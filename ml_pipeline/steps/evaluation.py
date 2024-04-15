import matplotlib.pyplot as plt
from sklearn.base import ClassifierMixin
import pandas as pd
import numpy as np
from typing import Tuple,Annotated
from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from zenml import step
import mlflow
from zenml.client import Client

experiment_tracker=Client().active_stack.experiment_tracker 


class ClassificationEvaluator:
    def __init__(self, model:ClassifierMixin, X_test:pd.DataFrame, y_test:pd.Series):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.y_predicted = self.model.predict(self.X_test)
    def matrix(self)->Tuple[
        Annotated[float, "average_precision"],
        Annotated[np.ndarray, "false_positive_rate"],
        Annotated[np.ndarray, "true_positive_rate"],
        Annotated[float, "accuracy"],]:   
        average_precision = average_precision_score(self.y_test, self.y_predicted)
        precision, recall, _ = precision_recall_curve(self.y_test, self.y_predicted)
        probs = self.model.predict_proba(self.X_test)
        false_positive_rate, true_positive_rate, _ = roc_curve(self.y_test, probs[:, 1])
        roc_auc = roc_auc_score(self.y_test, probs[:, 1])
        accuracy = accuracy_score(self.y_test, self.y_predicted)
        probs = self.model.predict_proba(self.X_test)
        auc_roc_score = roc_auc_score(self.y_test, probs[:, 1])
        return average_precision,false_positive_rate,true_positive_rate,accuracy



@step(experiment_tracker=experiment_tracker.name)
def evaluate(model:ClassifierMixin, X_test:pd.DataFrame, y_test:pd.Series)->Tuple[
        Annotated[float, "average_precision"],
        Annotated[np.ndarray, "false_positive_rate"],
        Annotated[np.ndarray, "true_positive_rate"],
        Annotated[float, "accuracy"],]:
    '''Evaluate the model
    Args:
        model: trained model
        X_test: test features
        y_test: test target
    Return:
        Tuple: average_precision,precision,recall,false_positive_rate,true_positive_rate,accuracy'''
    try:
        classifier = ClassificationEvaluator(model, X_test, y_test)
        average_precision,false_positive_rate,true_positive_rate,accuracy=classifier.matrix()
        
        metrics = {"average_precision": average_precision, "false_positive_rate":np.mean(false_positive_rate)
        , "true_positive_rate":np.mean(true_positive_rate)
        , "accuracy":accuracy}
        mlflow.log_metrics(metrics)
        return average_precision,false_positive_rate,true_positive_rate,accuracy
    except Exception as e:
        raise e
    
