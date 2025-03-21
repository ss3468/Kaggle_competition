import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
class MSZoning_rf:
    def __init__(self):
        self.od_num=['OverallQual']
        self.nc= {
            'Neighborhood': ['Blmngtn', 'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NoRidge', 'NPkVill', 'NridgHt', 'NWAmes', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker'],
            'HouseStyle':['1Story','1.5Fin','1.5Unf','2Story','2.5Fin','2.5Unf','SFoyer','SLvl'],
            'SaleCondition':['Normal','Abnorml','AdjLand','Alloca','Family','Partial']
            #'LandContour':['Lvl','Bnk','HLS','Low']
            #'BldgType': ['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs']
        }
        self.od_cat={
            #'LandContour':{'Lvl':0,'Bnk':1,'HLS':2,'Low':3}
        }
        self.cont=['LotArea']
        self.target={
            'MSZoning':{'A':0, 'C (all)':1, 'FV':2, 'I':3, 'RH':4, 'RL':5, 'RP':6, 'RM':7}
            }
        self.best_features=['LotArea', 'Neighborhood_Somerst', 'Neighborhood_IDOTRR', 'Neighborhood_OldTown', 'Neighborhood_SWISU', 'Neighborhood_SawyerW', 'SaleCondition_Abnorml', 'HouseStyle_2Story', 'HouseStyle_1.5Fin']
        #['LotArea', 'Neighborhood_Somerst', 'Neighborhood_IDOTRR', 'Neighborhood_OldTown', 'LandContour', 'Neighborhood_SawyerW', 'Neighborhood_SWISU', 'HouseStyle_2Story', 'HouseStyle_1.5Fin']
        #['Neighborhood_SWISU', 'Neighborhood_IDOTRR','Neighborhood_SawyerW', 'Neighborhood_OldTown','Neighborhood_Somerst', 'Neighborhood_NAmes', 'LandContour','LotArea', 'BldgType_1Fam', 'OverallQual']
        #['LotArea','Neighborhood_OldTown','Neighborhood_Somerst','Neighborhood_IDOTRR','Neighborhood_BrkSide','Neighborhood_MeadowV','LandContour','HouseStyle_2Story','Neighborhood_BrDale','Neighborhood_CollgCr','BldgType_TwnhsE','Neighborhood_NAmes','HouseStyle_1.5Fin']
        self.encoder = OneHotEncoder(categories=[self.nc[cat] for cat in self.nc.keys()], handle_unknown='ignore', sparse=False)
        self.model = RandomForestClassifier(class_weight='balanced',random_state=42)
    def expand_col(self,df):
        df_cat = df[list(self.nc.keys())]
        df_cat_transformed = self.encoder.fit_transform(df_cat)
        encoded_df = pd.DataFrame(df_cat_transformed, columns=self.encoder.get_feature_names_out(df_cat.columns))
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
        df_train = df.loc[df['MSZoning'].notnull(),list(self.nc.keys())+self.od_num+self.cont+list(self.od_cat.keys())+list(self.target.keys())]
        df_train_cat=self.expand_col(df_train)
        df_train_encode=self.encode_col(df_train_cat)
        df_train_encode=self.encode_target(df_train_cat)
        X_train = df_train_encode.loc[:,self.best_features]
        y_train = df_train_encode['MSZoning']
        self.model.fit(X_train, y_train)
    def transform(self,df):
        reverse_replace_dict = {v: k for k, v in self.target['MSZoning'].items()}
        df_test = df.loc[df['MSZoning'].isnull(),list(self.nc.keys())+self.od_num+self.cont+list(self.od_cat.keys())]
        if not df_test.empty:
            df_test_cat=self.expand_col(df_test)
            X_test=self.encode_col(df_test_cat)
            X_test=X_test.loc[:,self.best_features]
            predicted = self.model.predict(X_test)
            fitted_pred= [reverse_replace_dict.get(value) for value in predicted]
            df.loc[df['MSZoning'].isnull(), 'MSZoning']=fitted_pred
        return df
    def fit_transform(self,x):
        self.fit(x)
        return self.transform(x)
    
    def get_model(self):
        return self.model
    def plot_tree(self):
        tree=self.get_model().estimators_[0]
        plt.figure(figsize=(20, 10))
        plot_tree(tree, feature_names=self.best_features, filled=True, rounded=True, max_depth=3)
        plt.title("Visualization of a Single Tree from Random Forest")
        plt.show()