import numpy as np
import pandas as pd
class Exterior_n:
    def __init__(self):
        self.exterior1_df=None
        self.exterior2_df=None
    def fit(self,df):
        data=df[['Neighborhood','MSZoning', 'HouseStyle','Exterior1st','Exterior2nd']].copy()
        self.exterior1_df=data.groupby(['Neighborhood','MSZoning', 'HouseStyle'])['Exterior1st'].apply(lambda x: x.mode().iloc[0]).reset_index()
        self.exterior2_df=data.groupby(['Neighborhood','MSZoning', 'HouseStyle'])['Exterior2nd'].apply(lambda x: x.mode().iloc[0]).reset_index()
    def transform(self,df):
        if(self.exterior1_df.empty)|(self.exterior2_df.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.exterior1_df, on=['Neighborhood','MSZoning', 'HouseStyle'], how='left', suffixes=('', '_mod'))
            df['Exterior1st']=np.where(df['Exterior1st'].isnull(),df['Exterior1st_mod'],df['Exterior1st'])
            df=pd.merge(df, self.exterior2_df, on=['Neighborhood','MSZoning', 'HouseStyle'], how='left', suffixes=('', '_mod'))
            df['Exterior2nd']=np.where(df['Exterior2nd'].isnull(),df['Exterior2nd_mod'],df['Exterior2nd'])
            df.drop(columns=['Exterior1st_mod','Exterior2nd_mod'], inplace=True)
        return df
    def fit_transform(self,df):
        self.fit(df)
        return self.transform(df)