import numpy as np
import pandas as pd
class CustomSimpleImputer:
    def __init__(self):
        self.df_surname=None
    def fit_surname_planet(self,df):
        self.df_surname=df[['Surname','HomePlanet']].groupby(['Surname'])['HomePlanet'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    def transform_surname(self,df):
        if(self.df_surname.empty):
            raise ValueError("df_surname not fitted")
        else:
            df=pd.merge(df, self.df_surname, on='Surname', how='left', suffixes=('', '_right'))
        df['HomePlanet']=np.where(df['HomePlanet'].isnull(),df['HomePlanet_right'],df['HomePlanet'])
        df.drop(columns=['HomePlanet_right'], inplace=True)
        return df
    def fit_transform(self, X):
        X[['First_name','Surname']] = X['Name'].str.split(' ', expand=True)
        self.fit_surname_planet(X)
        return self.transform_surname(X)