import numpy as np
import pandas as pd
class MSZoning:
    def __init__(self):
        self.df_narrow_group=None
        self.df_broad_group=None
        self.df_group_narrow_cols=['Neighborhood','BldgType','HouseStyle']
        self.df_group_broad_cols=['Neighborhood']
    def fit(self,df):
        self.df_narrow_group=df[self.df_group_narrow_cols+['MSZoning']].groupby(self.df_group_narrow_cols)['MSZoning'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
        self.df_broad_group=df[self.df_group_broad_cols+['MSZoning']].groupby(self.df_group_broad_cols)['MSZoning'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform(self,df):
        if(self.df_narrow_group.empty)|(self.df_broad_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_narrow_group, on=self.df_group_narrow_cols, how='left', suffixes=('', '_1'))
            df=pd.merge(df, self.df_broad_group, on=self.df_group_broad_cols, how='left', suffixes=('', '_2'))
            df['MSZoning']=np.where(df['MSZoning'].isnull(),df['MSZoning_1'],df['MSZoning'])
            df['MSZoning']=np.where(df['MSZoning'].isnull(),df['MSZoning_2'],df['MSZoning'])
        df.drop(columns=['MSZoning_1','MSZoning_2'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_grouping_df(self,type):
        if type=='Narrow':
            return self.df_narrow_group
        else:
            return df_broad_group