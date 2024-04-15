import pandas as pd
import numpy as np
import logging
from zenml import step
from typing import Union,List

@step
def merge_anomaly(anomaly1: Union[np.ndarray, List[int]],anomaly2:Union[np.ndarray, List[int]],anomaly3:Union[np.ndarray, List[int]]) -> Union[np.ndarray, List[int]]:
    try:
        anomaly = anomaly1 + anomaly2+anomaly3
        logging.info("Merging the anomalies",anomaly[0:10])
        return anomaly
    except Exception as e:
        logging.error("Error in merging the anomalies")
        raise e