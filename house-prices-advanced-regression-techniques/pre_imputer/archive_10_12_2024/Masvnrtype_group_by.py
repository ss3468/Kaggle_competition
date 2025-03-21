import numpy as np
import pandas as pd
class MNBHYE_Imputer:
    def __init__(self):
        self.df_group=None
    def fit(self,df):
        self.df_group=df[['Neighborhood','BldgType','HouseStyle','MasVnrType']].groupby(['Neighborhood','BldgType','HouseStyle'])['MasVnrType'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform(self,df):
        if(self.df_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_group, on=['Neighborhood','BldgType','HouseStyle'], how='left', suffixes=('', '_right'))
        df['MasVnrType']=np.where(df['MasVnrType'].isnull(),df['MasVnrType_right'],df['MasVnrType'])
        df.drop(columns=['MasVnrType_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_enb_df(self):
        return self.df_group