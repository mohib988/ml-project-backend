import json
import pandas as pd
from zenml import step
import logging

class Ingest:
    def __init__(self,path:str):
        self.path=path
    def get_data(self)->pd.DataFrame:
        return pd.read_csv(self.path)
@step
def ingest_data(path:str)->pd.DataFrame:
    try:
        logging.info("getting the data from path",path)
        return Ingest(path).get_data()
    except Exception as e:
        logging.error("Error in getting the data from path",path)
        logging.error(e)
        raise e
@step
def make_data(df_json_str)->pd.DataFrame:
    try:
        df_dict_list = json.loads(df_json_str)
        df = pd.DataFrame(df_dict_list)
        return df

    except Exception as e:
        logging.error("Error in getting the data ")
        logging.error(e)
        raise e