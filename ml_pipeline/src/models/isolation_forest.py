import pandas as pd
from zenml import step
from typing import Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame
import numpy as np
from typing import List, Union
class Isolation_Forest:
    def __init__(self,contamination):
        """
        Initialize the IsolationForest class.

        Parameters:
        - contamination: float, the proportion of outliers in the data.
        """
        self.isolation_forest = IsolationForest(contamination=contamination)
    def apply_isolation_forest(self,df:pd.DataFrame) -> Union[np.ndarray, List[int]]:
        """
        Parameters:
        - df: DataFrame, the input DataFrame containing numeric columns.

        Returns:
        - DataFrame
        """
        # Selecting only numeric columns
        df_numeric =df.select_dtypes(include=['float64', 'int64'])
        # Handling missing values (filling with mean for example)
        # Normalize the data if needed (using StandardScaler)
        # scaler = StandardScaler()
        # df_normalized = scaler.fit_transform(df_numeric)

        # Applying Isolation Forest
        outliers = self.isolation_forest.fit_predict(df_numeric)

        # Add 'anomaly' column to the original DataFrame
        outliers = (outliers == -1).astype(int)*5

        return outliers

# Example usage:
# Initialize IsolationForest object
@step
def run_isolation_forest(df: pd.DataFrame,contamination:float=0.05) -> Union[np.ndarray, List[int]]:
    isolationForest = Isolation_Forest(contamination)
    # Apply Isolation Forest to the input DataFrame
    predict = isolationForest.apply_isolation_forest(df)
    return predict



