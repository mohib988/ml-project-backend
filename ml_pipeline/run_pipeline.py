from .pipelines.training_pipeline import training_pipeline
import json
from typing import List, Dict, Any
import mlflow
import pandas as pd
from zenml.client import Client

def main(df,**kwargs):
    df_dict_list = df.to_dict(orient='records')
    df_json_str = json.dumps(df_dict_list)
    contanimation=kwargs.get('contanimation',0.05)
    min_cluster=kwargs.get('min_cluster',10)
    print(Client().active_stack.experiment_tracker.get_tracking_uri())
    return training_pipeline(df_json_str,**kwargs)

if __name__ == '__main__':
    df=pd.read_csv("./data/AnomalyDetection.csv")
    df_dict_list = df.to_dict(orient='records')
    df_json_str = json.dumps(df_dict_list)
    contanimation=0.05
    min_cluster=0.05
    main(df,contanimation=contanimation,min_cluster=min_cluster)
    # Run the training pipeline
 