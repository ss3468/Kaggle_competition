import numpy as np
import pandas as pd
class ENB_Imputer:
    def __init__(self):
        self.df_group=None
    def fit(self,df):
        self.df_group=df[['Neighborhood','BldgType','Electrical']].groupby(['Neighborhood','BldgType'])['Electrical'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform(self,df):
        if(self.df_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_group, on=['Neighborhood','BldgType'], how='left', suffixes=('', '_right'))
        df['Electrical']=np.where(df['Electrical'].isnull(),df['Electrical_right'],df['Electrical'])
        df.drop(columns=['Electrical_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_enb_df(self):
        return self.df_group