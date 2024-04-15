import logging

import pandas as pd
from steps.clean_data import clean_data


def get_data_for_test():
    try:
        df = pd.read_csv("../data/AnomalyDetection.csv")
        df = df.sample(n=100)
        df=clean_data(df)
        result = df.to_json(orient="split")
        return result
    except Exception as e:
        logging.error(e)
        raise e