import pandas as pd
import numpy as np
import sys
import os
def fill_missing_bsmt_sf(df):
    df['BsmtFinSF1']=np.where(df['BsmtFinSF1'].isna()&(df['BsmtFinType1']=='NA'),0,df['BsmtFinSF1'])
    df['BsmtFinSF2']=np.where(df['BsmtFinSF2'].isna()&(df['BsmtFinType2']=='NA'),0,df['BsmtFinSF2'])
    df['BsmtUnfSF']=np.where(df['BsmtUnfSF'].isna()&(df['BsmtFinType1']=='NA')&(df['BsmtFinType2']=='NA'),0,df['BsmtUnfSF'])
    df['TotalBsmtSF']=np.where(df['TotalBsmtSF'].isna(),df['BsmtFinSF1']+df['BsmtFinSF2']+df['BsmtUnfSF'],df['BsmtUnfSF'])
    df['BsmtFullBath']=np.where(df['BsmtFullBath'].isna()&(df['BsmtFinType1']=='NA')&(df['BsmtFinType2']=='NA'),0,df['BsmtFullBath'])
    df['BsmtHalfBath']=np.where(df['BsmtHalfBath'].isna()&(df['BsmtFinType1']=='NA')&(df['BsmtFinType2']=='NA'),0,df['BsmtHalfBath'])
    return df
def g_imputer(df,cl,state):
    if state=='Train':
        df=cl.fit_transform(df)
    elif(state=='Validate')|(state=='Test'):
        df=cl.transform(df)
    else:
        print('please input proper State')
    return df
def fill_missing_MSZoning(df,cl,state):
    df=g_imputer(df,cl,state)
    return df
def fill_missing_LotFrontage(df,cl,state):
    df=g_imputer(df,cl,state)
    return df
def fill_missing_exterior(df,cl,state):
    df=g_imputer(df,cl,state)
    return df
def fill_missing_MasVnr(df,cl,state):
    df=g_imputer(df,cl,state)
    df['MasVnrArea']=np.where(df['MasVnrArea'].isnull()&(df['MasVnrType']=='None'),0,df['MasVnrArea'])
    return df
def fill_missing_garage_yr_blt(df):
    df['GarageYrBlt']=np.where((df['GarageType']=='NA')&(df['GarageYrBlt'].isnull()),0,df['GarageYrBlt'])
    df['GarageYrBlt']=np.where((df['GarageType'].isin(['Attchd', 'Detchd', 'CarPort', 'BuiltIn', 'Basment'])) & (df['GarageYrBlt'].isnull()),df['YearBuilt'],df['GarageYrBlt'])
    df['GarageYrBlt']=np.where((df['GarageType']=='2Types')&(df['GarageYrBlt'].isnull()),df['YearRemodAdd'],df['GarageYrBlt'])
    return df
def fill_missing_garage_details(df,cl,state):
    df=fill_missing_garage_yr_blt(df)#impute year garageyrblt
    df=g_imputer(df,cl,state)#impute number of cars in garage using MSSubclass,neighborhood and garagetype
    #impute garagearea using garagetype and number of cars
    return df
def fill_missing_kitchen_qual(df,cl,state):
    df=g_imputer(df,cl,state)
    return df
def fill_missing_saletype(df,cl,state):
    df=g_imputer(df,cl,state)# use Neighborhood and Salecondition
    return df
def fill_global_vals(df,cl,state):
    df=g_imputer(df,cl,state)
    return df
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_folder = os.path.join(current_dir, 'pre_imputer')
sys.path.append(modules_folder)
from dynamic_multi_imputer import value_mod_Imputer
from MSZoning_impute import MSZoning
from Lotfrontage_impute import Lfrontage
from Exterior_impute import Exterior_n
from Masvnr_impute import Masvnr
from Garage_impute import Garage_detail
from Global_imputer import Global_Imputer
def fill_missing_values(train,test,valid=None):
    MBH_cleaner=MSZoning()
    LF_cleaner=Lfrontage()
    Exterior_cleaner=Exterior_n()
    Masvnr_cleaner=Masvnr()
    Garage_impute=Garage_detail()
    Kitchen_impute=value_mod_Imputer(group_cols=['Neighborhood','MSSubClass'],imputation_target=['KitchenQual'],impuation_mode='Mode')
    Saletype_impute=value_mod_Imputer(group_cols=['Neighborhood','SaleCondition'],imputation_target=['SaleType'],impuation_mode='Mode')
    Global_impute=Global_Imputer(imputation_target=['Electrical','Utilities','Functional'],impuation_mode='Mode')
    if valid is None:
        train=fill_missing_bsmt_sf(train)
        train=fill_missing_MSZoning(train,MBH_cleaner,'Train')
        train=fill_missing_LotFrontage(train,LF_cleaner,'Train')
        train=fill_missing_exterior(train,Exterior_cleaner,'Train')
        train=fill_missing_MasVnr(train,Masvnr_cleaner,'Train')
        train=fill_missing_garage_details(train,Garage_impute,'Train')#fill_missing_garage_yr_blt(train)
        train=fill_missing_kitchen_qual(train,Kitchen_impute,'Train')
        train=fill_missing_saletype(train,Saletype_impute,'Train')
        train=fill_global_vals(train,Global_impute,'Train')
        test=fill_missing_bsmt_sf(test)
        test=fill_missing_exterior(test,Exterior_cleaner,'Test')
        test=fill_missing_MasVnr(test,Masvnr_cleaner,'Test')
        test=fill_missing_garage_details(test,Garage_impute,'Test')#fill_missing_garage_yr_blt(test)
        test=fill_missing_kitchen_qual(test,Kitchen_impute,'Test')
        test=fill_missing_saletype(test,Saletype_impute,'Test')
        test=fill_global_vals(test,Global_impute,'Test')
        return train,test
    else:
        train=fill_missing_bsmt_sf(train)
        train=fill_missing_MSZoning(train,MBH_cleaner,'Train')
        train=fill_missing_LotFrontage(train,LF_cleaner,'Train')
        train=fill_missing_exterior(train,Exterior_cleaner,'Train')
        train=fill_missing_MasVnr(train,Masvnr_cleaner,'Train')
        train=fill_missing_garage_details(train,Garage_impute,'Train')#fill_missing_garage_yr_blt(train)
        train=fill_missing_kitchen_qual(train,Kitchen_impute,'Train')
        train=fill_missing_saletype(train,Saletype_impute,'Train')
        train=fill_global_vals(train,Global_impute,'Train')
        valid=fill_missing_bsmt_sf(valid)
        valid=fill_missing_MSZoning(valid,MBH_cleaner,'Validate')
        valid=fill_missing_LotFrontage(valid,LF_cleaner,'Validate')
        valid=fill_missing_exterior(valid,Exterior_cleaner,'Validate')
        valid=fill_missing_MasVnr(valid,Masvnr_cleaner,'Validate')
        valid=fill_missing_garage_details(valid,Garage_impute,'Validate')#fill_missing_garage_yr_blt(valid)
        valid=fill_missing_kitchen_qual(valid,Kitchen_impute,'Validate')
        valid=fill_missing_saletype(valid,Saletype_impute,'Validate')
        valid=fill_missing_saletype(valid,Saletype_impute,'Validate')
        valid=fill_global_vals(valid,Global_impute,'Validate')
        test=fill_missing_bsmt_sf(test)
        test=fill_missing_MSZoning(test,MBH_cleaner,'Test')
        test=fill_missing_LotFrontage(test,LF_cleaner,'Test')
        test=fill_missing_exterior(test,Exterior_cleaner,'Test')
        test=fill_missing_MasVnr(test,Masvnr_cleaner,'Test')
        test=fill_missing_garage_details(test,Garage_impute,'Test')#fill_missing_garage_yr_blt(test)
        test=fill_missing_kitchen_qual(test,Kitchen_impute,'Test')
        test=fill_missing_saletype(test,Saletype_impute,'Test')
        test=fill_global_vals(test,Global_impute,'Test')
        return train,valid,test