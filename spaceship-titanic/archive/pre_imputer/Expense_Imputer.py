import numpy as np
import pandas as pd
class E_Imputer:
    def __init__(self,x,y):
        self.df_E=None
        self.g_col=x
        self.expense_col=y
    def fit(self,df):
        self.df_E=df[self.g_col+self.expense_col].groupby(self.g_col,dropna=False)[self.expense_col].mean().reset_index()
    def transform(self,df):
        if(self.df_E.empty):
            raise ValueError("df_E not fitted")
        else:
            df=pd.merge(df, self.df_E, on=self.g_col, how='left', suffixes=('', '_right'))
        for item in self.expense_col:
            df[item]=np.where(df[item].isnull(),df[item+'_right'],df[item])
        df.drop(columns=list(map(lambda x: x + '_right', self.expense_col)), inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_E_df(self):
        return self.df_E