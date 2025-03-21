import numpy as np
import pandas as pd
class Garage_detail:
    def __init__(self):
        self.gcars_df=None
        self.garea_df=None
    def fit(self,df):
        data=df[['Neighborhood','MSSubClass','GarageType','GarageCars','GarageArea']].copy()
        self.gcars_df=data.groupby(['Neighborhood','MSSubClass','GarageType'])['GarageCars'].apply(lambda x: x.mode().iloc[0]).reset_index()
        self.garea_df=data.groupby(['Neighborhood','MSSubClass','GarageType','GarageCars'])['GarageArea'].median().reset_index()
    def transform(self,df):
        if(self.gcars_df.empty)|(self.garea_df.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.gcars_df, on=['Neighborhood','MSSubClass','GarageType'], how='left', suffixes=('', '_mod'))
            df['GarageCars']=np.where(df['GarageCars'].isnull(),df['GarageCars_mod'],df['GarageCars'])
            df=pd.merge(df, self.garea_df, on=['Neighborhood','MSSubClass','GarageType','GarageCars'], how='left', suffixes=('', '_mod'))
            df['GarageArea']=np.where(df['GarageArea'].isnull(),df['GarageArea_mod'],df['GarageArea'])
            df.drop(columns=['GarageCars_mod','GarageArea_mod'], inplace=True)
        return df
    def fit_transform(self,df):
        self.fit(df)
        return self.transform(df)