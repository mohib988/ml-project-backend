import pandas as pd
import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from typing import List, Union
from zenml import step

class HDBClustering:
  def __init__(self,df:pd.DataFrame,min_cluster:int,**kargs):
    self.df=df
    self.eps = 0.8  # Adjust the epsilon value based on your df2_scaled
    self.min_samples = 80
    self.hdbscan = HDBSCAN(cluster_selection_epsilon=1.5, min_cluster_size=min_cluster)

# Assuming 'self.df' is your DataFrame with the relevant data
# Feature engineering
  def run_hdb_scan(self,hour:bool=True)->Union[np.ndarray, List[int]]:
      if(hour):
        self.df['hour'] = self.df['created_date_time'].dt.hour
      self.df['day'] = self.df['created_date_time'].dt.day
      # self.df = self.df.reset_index(drop=True)

      # Select relevant features for prediction
      features = [  'sales_value', 'day', 'month',"location"]
      if (hour):
        features.append("hour")


      # Prepare input data
      X = self.df[features]
      # X["sales_value"] = np.log1p(np.abs(X["sales_value"]))
      # One-hot encode the 'location' column
      X=pd.get_dummies(X,columns=['location'])

      # Select relevant features for clustering
      # Standardize the selected features
      scaler = StandardScaler()
      df2_scaled = scaler.fit_transform(X)
      MinPts=5
      # # Apply DBSCAN
      outliers = self.hdbscan.fit_predict(df2_scaled)
      outliers =(outliers == -1).astype(int)*2

      # Filter rows marked as anomalies
      # self.df["sales_value"] = np.expm1(np.abs(self.df["sales_value"]))
      return outliers
@step
def run_hdb_clustering(df:pd.DataFrame,min_cluster:int=10,hour:bool=True)->Union[np.ndarray, List[int]]:
  HDB_clustering=HDBClustering(df,min_cluster)
  outliers=HDB_clustering.run_hdb_scan(hour=5)
  return outliers
