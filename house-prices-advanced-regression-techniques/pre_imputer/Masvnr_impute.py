import numpy as np
import pandas as pd
class Masvnr:
    def __init__(self):
        self.df_narrow_group=None
        self.df_broad_group=None
        self.df_msvnr_area=None
        self.df_group_narrow_cols=['Neighborhood','BldgType','HouseStyle']
        self.df_group_broad_cols=['Neighborhood']
        self.df_group_area_cols=['Neighborhood','BldgType','HouseStyle','MasVnrType']
    def fit(self,df):
        self.df_narrow_group=df[self.df_group_narrow_cols+['MasVnrType']].groupby(self.df_group_narrow_cols)['MasVnrType'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
        self.df_broad_group=df[self.df_group_broad_cols+['MasVnrType']].groupby(self.df_group_broad_cols)['MasVnrType'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
        self.df_msvnr_area=df.loc[df['MasVnrType']!='None',self.df_group_area_cols+['MasVnrArea']].groupby(self.df_group_area_cols)['MasVnrArea'].median().reset_index()
    def transform(self,df):
        if(self.df_narrow_group.empty)|(self.df_broad_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_narrow_group, on=self.df_group_narrow_cols, how='left', suffixes=('', '_1'))
            df=pd.merge(df, self.df_broad_group, on=self.df_group_broad_cols, how='left', suffixes=('', '_2'))
            df['MasVnrType']=np.where(df['MasVnrType'].isnull(),df['MasVnrType_1'],df['MasVnrType'])
            df['MasVnrType']=np.where(df['MasVnrType'].isnull(),df['MasVnrType_2'],df['MasVnrType'])
            df=pd.merge(df, self.df_msvnr_area, on=self.df_group_area_cols, how='left',suffixes=('', '_3'))
            df['MasVnrArea']=np.where(df['MasVnrArea'].isnull(),df['MasVnrArea_3'],df['MasVnrArea'])
        df.drop(columns=['MasVnrType_1','MasVnrType_2','MasVnrArea_3'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_grouping_df(self,type):
        if type=='Narrow':
            return self.df_narrow_group
        else:
            return self.df_broad_group