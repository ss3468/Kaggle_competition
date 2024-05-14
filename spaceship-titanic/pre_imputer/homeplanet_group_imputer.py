import numpy as np
import pandas as pd
class HG_Imputer:
    def __init__(self):
        self.df_group=None
    def fit(self,df):
        self.df_group=df[['Group','HomePlanet']].groupby(['Group'])['HomePlanet'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform(self,df):
        if(self.df_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_group, on='Group', how='left', suffixes=('', '_right'))
        df['HomePlanet']=np.where(df['HomePlanet'].isnull(),df['HomePlanet_right'],df['HomePlanet'])
        df.drop(columns=['HomePlanet_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_hg_df(self):
        return self.df_group