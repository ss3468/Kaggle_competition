import numpy as np
import pandas as pd
class Lfrontage:
    def __init__(self):
        self.df_group_1=None
        self.df_group_2=None
    def fit(self,df):
        data=df[['MSZoning','Neighborhood','LotShape','LotConfig','LotFrontage']].copy()
        Q1 = data['LotFrontage'].quantile(0.25)
        Q3 = data['LotFrontage'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3* IQR
        upper_bound = Q3 + 3* IQR
        data['LotFrontage']=data['LotFrontage'].clip(lower=lower_bound, upper=upper_bound)
        tem1=data.groupby(['Neighborhood','LotShape','LotConfig'])['LotFrontage'].agg(mean='mean',median='median',std='std',count='count').reset_index()
        #tem1['coefficient_of_variation'] = tem1['std'] / tem1['mean']
        self.df_group_1=tem1.drop(columns=['mean','count']).rename(columns={'median':'LotFrontage'})
        tem2=data.groupby(['Neighborhood'])['LotFrontage'].agg(mean='mean',median='median',std='std',count='count').reset_index()
        #tem2['coefficient_of_variation'] = tem2['std'] / tem2['mean']
        self.df_group_2=tem2.drop(columns=['mean','count']).rename(columns={'median':'LotFrontage'})
    def transform(self,df):
        if self.df_group_1.empty:
            raise ValueError("df_group not fitted")
        else:
            noise_mean = 0       # Centered at 0
            noise_std = 0.01      # Small standard deviation
            df=pd.merge(df, self.df_group_1, on=['Neighborhood','LotShape','LotConfig'], how='left', suffixes=('', '_1'))
            df['noise_1']=np.random.normal(noise_mean,df['std']*noise_std)
            df['noise_1']=np.where(df['noise_1'].isnull(),0,df['noise_1'])
            df['LotFrontage']=np.where(df['LotFrontage'].isnull(),df['LotFrontage_1']+df['noise_1'],df['LotFrontage'])
            df=pd.merge(df, self.df_group_2, on=['Neighborhood'], how='left', suffixes=('', '_2'))
            df['noise_2']=np.random.normal(noise_mean,df['std_2']*noise_std)
            df['noise_2']=np.where(df['noise_2'].isnull(),0,df['noise_2'])
            df['LotFrontage']=np.where(df['LotFrontage'].isnull(),df['LotFrontage_2']+df['noise_2'],df['LotFrontage'])
            df.drop(columns=['noise_1','std','LotFrontage_1','noise_2','std_2','LotFrontage_2'], inplace=True)
        return df
    
    def fit_transform(self,df):
        self.fit(df)
        return self.transform(df)