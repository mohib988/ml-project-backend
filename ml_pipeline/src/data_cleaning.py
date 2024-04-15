import logging
from abc import abstractmethod, ABC
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import Union

class DataStrategy(ABC):
    @abstractmethod
    def handle_data(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
class DataPreprocessingStrategy(DataStrategy):
    def handle_data(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Preprocessing the data")
            # df=df.drop("Unnamed: 0",axis=1)
            # Drop rows with missing values
            df['created_date_time']=pd.to_datetime(df['created_date_time'])
            df['invoice_date']=pd.to_datetime(df['created_date_time'])
            df["month"]=pd.DatetimeIndex(df['created_date_time']).month
            df['extra_info'] = df['extra_info'].replace(['N / A', 'N/A', "0", "0.0"], 0)
            df['consumer_name'] = df['consumer_name'].replace(['N / A', 'N/A', "0", "0.0"], 0)
            df['extra_info'] = df['extra_info'].replace(['test'], 1)
            df['extra_info'] = df['extra_info'].fillna(0)
            df['rate_value'] = df['rate_value'].fillna(0)
            df['consumer_address'] = df['consumer_address'].fillna(0)
            df['consumer_address'] = df['consumer_address'].fillna(0)
            df['consumer_address'] = df['consumer_address'].replace(['N / A', 'N/A', "0", "0.0"], 0)
            df['consumer_ntn'] = df['consumer_ntn'].fillna(0)
            df['consumer_ntn'] = df['consumer_ntn'].replace(['N / A', 'N/A', "0", "0.0"], 0)
            # df.loc[df['consumer_name'] != 0, 'consumer_name'] = 1
            df['consumer_name'] = df['consumer_name'].fillna(0)
            df['invoice_type'] = df['invoice_type'].fillna(0)
            
            # making every consumer_name=1
            df.loc[(df.consumer_name!="N / A") & (df.consumer_name!=0) & (df.consumer_name!=""),"consumer_name"]=1
            df.loc[(df.consumer_address!="N / A") & (df.consumer_address!=0) & (df.consumer_address!=""),"consumer_address"]=1
            df.loc[(df.consumer_ntn!="N / A") & (df.consumer_ntn!=0) & (df.consumer_ntn!=""),"consumer_ntn"]=1
            df["consumer_name"]=(df["consumer_name"]).astype(int)
            df["consumer_address"]=(df["consumer_address"]).astype(int)
            df["consumer_ntn"]=(df["consumer_ntn"]).astype(int)
            df["consumer_name"]=(df["consumer_name"]).astype(int)
            df["consumer_address"]=(df["consumer_address"]).astype(int)
            df["consumer_ntn"]=(df["consumer_ntn"]).astype(int)
            df["time"]=(df['created_date_time']).dt.time
            df["day"]=(df['created_date_time']).dt.day
            df["month"]=(df['created_date_time']).dt.month
            df['time_seconds'] = df['time'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second)
            df["delay"]=(df['created_date_time'] - df['invoice_date']).dt.total_seconds() / 60
            drop_cols=["name","pos_pass","pos_user","tariff_code","srb_invoice_id","time"]
            df.drop(drop_cols,axis=1,inplace=True)
            df2=df.copy()
            return df2
        except Exception as e:
            logging.error("Error in Data Preprocessing", e)
            raise e
class DataDivideStratedy(DataStrategy):
        def handle_data(self, df: pd.DataFrame)-> Union[pd.DataFrame,pd.Series] :
            try:
                logging.info("Dividing the data into train and test")
                X_train, X_test, y_train, y_test = train_test_split(df.drop(["anomaly"],axis=1),df["anomaly"], test_size=0.2, random_state=42)
                return X_train, X_test, y_train, y_test
            except Exception as e:
                logging.error("Error in dividing the data into train and test", e)
                raise e

class DataCleaner:
    def __init__(self, strategy: DataStrategy,df:pd.DataFrame):
        self.strategy = strategy
        self.df = df

    def handle_data(self)->Union[pd.DataFrame,pd.Series] :
        try:
            return self.strategy.handle_data(self.df)
        except Exception as e:
            logging.error("Error in handling the data", e)
            raise e
