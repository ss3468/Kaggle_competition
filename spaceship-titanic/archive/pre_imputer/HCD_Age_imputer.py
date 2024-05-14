import numpy as np
import pandas as pd
import math
class HCDA_Imputer:
    def __init__(self):
        self.df_HCD=None
        self.min_age=0
        self.max_age=0
        self.n_rows=0
    def fit(self,df):
        self.df_HCD=df[['HomePlanet','CryoSleep','Destination','Age']].groupby(['HomePlanet','CryoSleep','Destination'])['Age'].mean().reset_index()
        self.min_age = df['Age'].min()
        self.max_age = df['Age'].max()
        self.n_rows=len(df)
    def transform(self,df):
        if(self.df_HCD.empty):
            raise ValueError("df_HCD not fitted")
        else:
            df=pd.merge(df, self.df_HCD, on=['HomePlanet','CryoSleep','Destination'], how='left', suffixes=('', '_right'))
        df['Age']=np.where(df['Age'].isnull(),np.floor(df['Age_right']),df['Age'])
        k=math.ceil(1 + np.log2(self.n_rows))
        interval_width = math.ceil((self.max_age - self.min_age) / k)
        bins = [self.min_age + i * interval_width for i in range(k+1)]
        bins.append(np.inf)
        print(bins)
        labels = [f'{int(bins[i])}-{int(bins[i+1])}' for i in range(k)]
        labels.append(f'{int(bins[-2])}+')
        print(labels)
        df['Age Interval'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
        df.drop(columns=['Age_right'], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_HCD_df(self):
        return self.df_HCD