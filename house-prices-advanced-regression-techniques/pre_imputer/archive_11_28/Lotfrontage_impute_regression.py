import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
class Lfrontage_lr:
    def __init__(self):
        self.categorical_features = ['LotShape', 'Neighborhood', 'BldgType', 'MSZoning']
        self.numerical_features=['LotArea']
        self.possible_categories = {
            'LotShape': ['Reg', 'IR1', 'IR2', 'IR3'],
            'Neighborhood': ['Blmngtn', 'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'Names', 'NoRidge', 'NPkVill', 'NridgHt', 'NWAmes', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker'],
            'BldgType': ['1Fam', '2FmCon', 'Duplex', 'TwnhsE', 'Twnhs'],
            'MSZoning': ['A', 'C (all)', 'FV', 'I', 'RH', 'RL', 'RP', 'RM']
            }
        self.encoder = OneHotEncoder(categories=[self.possible_categories[cat] for cat in self.categorical_features], handle_unknown='ignore', sparse=False)
        self.model = LinearRegression()
    def fit(self,df):
        df_train = df[df['LotFrontage'].notnull()]
        X_train_cat = self.encoder.fit_transform(df_train[self.categorical_features])
        X_train = pd.concat([pd.DataFrame(X_train_cat, columns=self.encoder.get_feature_names_out(self.categorical_features)),df_train[self.numerical_features].reset_index(drop=True)], axis=1)
        y_train = df_train['LotFrontage']
        self.model.fit(X_train, y_train)
    def transform(self,df):
        df_test = df[df['LotFrontage'].isnull()]
        X_test_cat = self.encoder.transform(df_test[self.categorical_features])
        X_test = pd.concat([pd.DataFrame(X_test_cat, columns=self.encoder.get_feature_names_out(self.categorical_features)),df_test[self.numerical_features].reset_index(drop=True)], axis=1)
        df.loc[df['LotFrontage'].isnull(), 'LotFrontage'] = self.model.predict(X_test).round()
        return df
    def fit_transform(self,X):
        self.fit(X)
        return self.transform(X)
    def get_model(self):
        return self.model

