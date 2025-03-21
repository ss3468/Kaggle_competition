import numpy as np
import pandas as pd
class Global_Imputer:
    def __init__(self,imputation_target,impuation_mode='Mean'):
        self.impuation_mode=impuation_mode
        self.imputation_target=imputation_target
        self.imputation_val=None
    def fit(self,df):
        if self.impuation_mode=='Mode':
            self.imputation_val=df[self.imputation_target].mode()
        elif self.impuation_mode=='Median':
            self.imputation_val=df[self.imputation_target].median()
        else:
            self.imputation_val=df[self.imputation_target].mean()
    def transform(self,df):
        if(self.imputation_val is None):
            raise ValueError("Global Value not fitted")
        else:
            for col in self.imputation_target:
                df[col]=np.where(df[col].isnull(),self.imputation_val.iloc[0][col],df[col])
            #df[self.imputation_target]=np.where(df[self.imputation_target].isnull(),self.imputation_val,df[self.imputation_target])
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)