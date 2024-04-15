from sklearn.neighbors import LocalOutlierFactor
from pandas import DataFrame
from zenml import step
import logging

class LocalOutlierDetection:
    def __init__(self,**kargs):
        self.clf = LocalOutlierFactor(**kargs)
        
    def fit_predict(self,df) -> DataFrame:
        try:
            df_numeric =df.select_dtypes(include=['float64', 'int64'])

            y_pred = (self.clf).fit_predict(df_numeric)
            df["anomaly"] = (y_pred == -1).astype(int)
            return df
        except Exception as e:
            logging.error("Error in LocalOutlierDetection")
            raise e

@step
def run_loc(df: DataFrame) -> DataFrame:
    loc = LocalOutlierDetection()
    df = loc.fit_predict(df)
    return df