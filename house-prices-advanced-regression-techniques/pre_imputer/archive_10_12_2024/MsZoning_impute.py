import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
class MSZoning_rf:
    def __init__(self):
        self.nc= {
            'Neighborhood': ['Blmngtn', 'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'Names', 'NoRidge', 'NPkVill', 'NridgHt', 'NWAmes', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker'],
            'BldgType': ['1Fam', '2FmCon', 'Duplex', 'TwnhsE', 'Twnhs'],
            'HouseStyle':['1Story','1.5Fin','1.5Unf','2Story','2.5Fin','2.5Unf','SFoyer','SLvl']
        }
        self.od_cat={
            'LandContour':{'Lvl':0,'Bnk':1,'HLS':2,'Low':3}
        }
        self.target={
            'MSZoning':{'A':1, 'C (all)':2, 'FV':3, 'I':4, 'RH':5, 'RL':6, 'RP':7, 'RM':8}
            }
        self.encoder = OneHotEncoder(categories=[self.nc[cat] for cat in self.nc.keys()], handle_unknown='ignore', sparse=False)
        self.model = RandomForestClassifier(random_state=42)
    def expand_col(self,df):
        df_cat = df[list(self.nc.keys())]
        df_cat_transformed = self.encoder.fit_transform(df_cat)
        encoded_df = pd.DataFrame(df_cat_transformed, columns=self.encoder.get_feature_names_out(df_cat.columns))
        for col in self.nc.keys():
            last_category = self.nc[col][-1]
            col_to_drop = f"{col}_{last_category}"
            encoded_df = encoded_df.drop(columns=[col_to_drop])
        df_non_cat = df.loc[:, ~df.columns.isin(self.nc.keys())].reset_index(drop=True)
        new_df = pd.concat([encoded_df, df_non_cat], axis=1)
        return new_df
    def encode_col(self,df):
        for col in self.od_cat.keys():
            df[col]=df[col].map(self.od_cat[col])
        return df
    def encode_target(self,df):
        df['MSZoning']=df['MSZoning'].map(self.target['MSZoning'])
        return df
    
    def fit(self,df):
        df_train = df.loc[df['MSZoning'].notnull(),list(self.nc.keys())+list(self.od_cat.keys())+list(self.target.keys())]
        df_train_cat=self.expand_col(df_train)
        df_train_encode=self.encode_col(df_train_cat)
        df_train_encode=self.encode_target(df_train_cat)
        X_train = df_train_encode.loc[:,df_train_encode.columns!='MSZoning']
        y_train = df_train_encode['MSZoning']
        self.model.fit(X_train, y_train)
    def transform(self,df):
        reverse_replace_dict = {v: k for k, v in self.target['MSZoning'].items()}
        df_test = df.loc[df['MSZoning'].isnull(),list(self.nc.keys())+list(self.od_cat.keys())]
        if not df_test.empty:
            df_test_cat=self.expand_col(df_test)
            X_test=self.encode_col(df_test_cat)
            predicted = self.model.predict(X_test)
            fitted_pred= [reverse_replace_dict.get(value) for value in predicted]
            df.loc[df['MSZoning'].isnull(), 'MSZoning']=fitted_pred
        return df
    def fit_transform(self,x):
        self.fit(x)
        return self.transform(x)
    
    def get_model(self):
        return self.model
