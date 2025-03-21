import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder
class feature_encoder:
    def __init__(self):
        self.nc_encode = ['MSSubClass','MSZoning','Street','Alley','LotShape','LandContour','Utilities','LotConfig','LandSlope','Neighborhood','Condition1','Condition2','BldgType','HouseStyle','RoofStyle','RoofMatl','Exterior1st','Exterior2nd','MasVnrType','Foundation','Heating','Electrical','GarageType','MiscFeature','MoSold','SaleType','SaleCondition','Vintage']
        self.bc_encode={'CentralAir':{'Y': 1, 'N': 0}}
        self.oc={
            'ExterQual':['Po','Fa','TA','Gd','Ex'],
            'ExterCond':['Po','Fa','TA','Gd','Ex'],
            'BsmtQual':['NA','Po','Fa','TA','Gd','Ex'],
            'BsmtCond':['NA','Po','Fa','TA','Gd','Ex'],
            'BsmtExposure':['NA','No','Mn','Av','Gd'],
            'BsmtFinType1':['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ'],
            'BsmtFinType2':['NA','Unf','LwQ','Rec','BLQ','ALQ','GLQ'],
            'HeatingQC':['Po','Fa','TA','Gd','Ex'],
            'KitchenQual':['Po','Fa','TA','Gd','Ex'],
            'Functional':['Typ','Min1','Min2','Mod','Maj1','Maj2','Sev','Sal'],
            'FireplaceQu':['NA','Po','Fa','TA','Gd','Ex'],
            'GarageFinish':['NA','Unf','RFn','Fin'],
            'GarageQual':['NA','Po','Fa','TA','Gd','Ex'],
            'GarageCond':['NA','Po','Fa','TA','Gd','Ex'],
            'PavedDrive':['N','P','Y'],
            'PoolQC':['NA','Fa','TA','Gd','Ex'],
            'Fence':['NA','MnWw','MnPrv','GdWo','GdPrv']
            }
        self.encoder_nc = OneHotEncoder(sparse_output=False,drop='first')
        self.encoder_oc= None
    def fit(self,df):
        self.encoder_nc.fit(df.loc[:,df.columns.isin(self.nc_encode)])
        categories =[self.oc[col] for col in df.loc[:,df.columns.isin(self.oc.keys())].columns]
        self.encoder_oc=OrdinalEncoder(categories=categories)
        self.encoder_oc.fit(df.loc[:,df.columns.isin(self.oc.keys())])
    def map_bc(self,df):
        for col in self.bc_encode.keys():
            df[col]=df[col].map(self.bc_encode[col])
        return df
    def map_oc(self,df):
        tem=df.loc[:,df.columns.isin(self.oc.keys())].columns
        for col in tem:
            df[col]=df[col].map(self.oc[col])
        return df
    def transform(self,df):
        num_df=df.loc[:,df.columns.isin(self.nc_encode)]
        oc_cols=df.loc[:,df.columns.isin(self.oc.keys())].columns.tolist()
        data_encoded=self.encoder_nc.transform(num_df)
        encoded_columns = self.encoder_nc.get_feature_names_out(num_df.columns)
        df_encoded=pd.DataFrame(data_encoded, columns=encoded_columns)
        for col in num_df.columns:
            col_idx = df.columns.get_loc(col)
            col_encoded = [c for c in encoded_columns if c.startswith(f"{col}_")]
            encoded_subset = df_encoded[col_encoded]
            for i, new_col in enumerate(col_encoded):
                df.insert(col_idx + i, new_col, encoded_subset[new_col])
        df.drop(columns=num_df.columns, inplace=True)
        df=self.map_bc(df)
        if self.encoder_oc is not None:
            df[oc_cols]=self.encoder_oc.transform(df.loc[:,oc_cols].values)
        #df=self.map_oc(df)
        return df
    def fit_transform(self,df):
        self.fit(df)
        return self.transform(df)