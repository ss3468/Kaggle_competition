import numpy as np
import pandas as pd
class MBH_Imputer:
    def __init__(self):
        self.df_group=None
    def fit(self,df):
        self.df_group=df[['Neighborhood','BldgType','HouseStyle','MSZoning']].groupby(['Neighborhood','BldgType','HouseStyle'])['MSZoning'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform(self,df):
        if(self.df_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_group, on=['Neighborhood','BldgType','HouseStyle'], how='left', suffixes=('', '_right'))
        df['MSZoning']=np.where(df['MSZoning'].isnull(),df['MSZoning_right'],df['MSZoning'])
        df.drop(columns=['MSZoning_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_enb_df(self):
        return self.df_group