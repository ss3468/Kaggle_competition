import numpy as np
import pandas as pd
class Mas_area_Imputer:
    def __init__(self):
        self.df_group=None
    def fit(self,df):
        self.df_group=df[['Neighborhood','BldgType','HouseStyle','MasVnrType','MasVnrArea']].groupby(['Neighborhood','BldgType','HouseStyle','MasVnrType'])['MasVnrArea'].mean().reset_index()
    def transform(self,df):
        if(self.df_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_group, on=['Neighborhood','BldgType','HouseStyle','MasVnrType'], how='left', suffixes=('', '_right'))
        df['MasVnrArea']=np.where(df['MasVnrArea'].isnull(),df['MasVnrArea_right'],df['MasVnrArea'])
        df.drop(columns=['MasVnrArea_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_enb_df(self):
        return self.df_group