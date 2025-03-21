import numpy as np
import pandas as pd
class value_mod_Imputer:
    def __init__(self,group_cols,imputation_target,impuation_mode='Mean'):
        self.df_group=None
        self.impuation_mode=impuation_mode
        self.df_group_cols=group_cols
        self.imputation_target=imputation_target
    def fit(self,df):
        total_col_list=self.df_group_cols+self.imputation_target
        if self.impuation_mode=='Mode':
            self.df_group=df[total_col_list].groupby(self.df_group_cols)[self.imputation_target].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
        else:
            self.df_group=df[total_col_list].groupby(self.df_group_cols)[self.imputation_target].mean().reset_index()
    def transform(self,df):
        if(self.df_group.empty):
            raise ValueError("df_group not fitted")
        else:
            df=pd.merge(df, self.df_group, on=self.df_group_cols, how='left', suffixes=('', '_right'))
        for col in self.imputation_target:
            df[col]=np.where(df[col].isnull(),df[f'''{col}_right'''],df[col])
        df.drop(columns=[f'''{col}_right''' for col in self.imputation_target], inplace=True)
        return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_grouping_df(self):
        return self.df_group