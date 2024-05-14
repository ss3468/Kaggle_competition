import numpy as np
import pandas as pd
class HDDC_Imputer:
    def __init__(self):
        self.df_ddc=None
    def fit(self,df):
        self.df_ddc=df[['deck','Destination','CryoSleep','HomePlanet']].groupby(['deck','Destination','CryoSleep'])['HomePlanet'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform(self,df):
        if(self.df_ddc.empty):
            raise ValueError("df_ddcnot fitted")
        else:
            df=pd.merge(df, self.df_ddc, on=['deck','Destination','CryoSleep'], how='left', suffixes=('', '_right'))
        df['HomePlanet']=np.where(df['HomePlanet'].isnull(),df['HomePlanet_right'],df['HomePlanet'])
        df.drop(columns=['HomePlanet_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_h_ddc(self):
        return self.df_ddc