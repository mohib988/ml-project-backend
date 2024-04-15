import logging
import pandas as pd
from zenml import step
from src.data_cleaning import DataCleaner, DataDivideStratedy,DataPreprocessingStrategy
from typing import Union,Tuple,Annotated
@step
def clean_data(df: pd.DataFrame)->pd.DataFrame :
    try:
        process_strategy=DataPreprocessingStrategy()
        data_cleaner=DataCleaner(process_strategy,df)
        processed_data=data_cleaner.handle_data()
        logging.info("Data Preprocessing Done")
        return processed_data
    except Exception as e:
        logging.error("Error in Data Preprocessing", e)
        raise e
@step
def split_data(df: pd.DataFrame)->Tuple[Annotated[pd.DataFrame, "X_train"],Annotated[pd.DataFrame, "X_test"],Annotated[pd.Series, "y_train"],Annotated[pd.Series, "y_test"]]:
    try:
        divide_strategy=DataDivideStratedy()
        data_cleaner=DataCleaner(divide_strategy,df)
        X_train, X_test, y_train, y_test=data_cleaner.handle_data()
        logging.info("Data Preprocessing Done")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error("Error in Data Preprocessing", e)
        raise e

    # logging.info("Cleaning the data")
    # # Drop rows with missing values
    # df = df.dropna()
    # return df