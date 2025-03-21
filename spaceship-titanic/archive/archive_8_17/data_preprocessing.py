import pandas as pd
import numpy as np
import sys
import os
def feature_expansion(df,target_col=None):
    if target_col:
        removed_column = df[target_col].values
        df.drop(columns=[target_col], inplace=True)
        df['Surname'] = df['Name'].str.split(' ', expand=True)[1]
        df[['Group','pp']] = df['PassengerId'].str.split('_', expand=True)
        df['Group'] = df['Group'].apply(lambda x: int(x))
        df['pp'] = df['pp'].apply(lambda x: int(x))
        df[['deck','num','side']]=df['Cabin'].str.split('/',expand=True)
        df.drop(columns=['Name','Cabin'], inplace=True)
        df[target_col]=removed_column
    else:
        df['Surname'] = df['Name'].str.split(' ', expand=True)[1]
        df[['Group','pp']] = df['PassengerId'].str.split('_', expand=True)
        df['Group'] = df['Group'].apply(lambda x: int(x))
        df['pp'] = df['pp'].apply(lambda x: int(x))
        df[['deck','num','side']]=df['Cabin'].str.split('/',expand=True)
        df.drop(columns=['Name','Cabin'], inplace=True)
    return df
# def fill_planet_surname(df,cl,state):
#     if state=='Train':
#         df=cl.fit_transform(df)
#     elif(state=='Validate')|(state=='Test'):
#         df=cl.transform(df)
#     else:
#         print('please input proper State')
#     return df
# def fill_planet_group(df,cl,state):
#     if state=='Train':
#         df=cl.fit_transform(df)
#     elif(state=='Validate')|(state=='Test'):
#         df=cl.transform(df)
#     else:
#         print('please input proper State')
#     return df
def g_imputer(df,cl,state):
    if state=='Train':
        df=cl.fit_transform(df)
    elif(state=='Validate')|(state=='Test'):
        df=cl.transform(df)
    else:
        print('please input proper State')
    return df
def fill_planets_deck(df,cl,state):
    df.loc[(df['HomePlanet'].isna()) & (df['deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet']='Europa'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='G'), 'HomePlanet']='Earth'
    df=g_imputer(df,cl,state)
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='D'), 'HomePlanet']='Mars'
    df.loc[(df['HomePlanet'].isna()) & ~(df['deck']=='D'), 'HomePlanet']='Earth'
    return df
def fill_missing_homeplanets(df,cl1,cl2,cl3,state):
    df=g_imputer(df,cl1,state)#fill_planet_surname(df,cl1,state)
    df=g_imputer(df,cl2,state)#fill_planet_group(df,cl2,state)
    df=fill_planets_deck(df,cl3,state)
    return df
def fill_missing_destination(df):
    df['Destination']=np.where(df['Destination'].isnull(),'TRAPPIST-1e',df['Destination'])
    return df
def fill_missing_cryo_sleep(df,col_to_fill):
    df['expenses'] = df[col_to_fill].sum(axis=1,skipna=False)
    df['expenses_w_o_na'] = df[col_to_fill].sum(axis=1,skipna=True)
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&((df['expenses']>0)|(df['expenses'].isnull()&(df['expenses_w_o_na']>0))),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['VIP']==True)&(df['HomePlanet']=='Mars'),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0),True,df['CryoSleep'])
    df['CryoSleep']=df['CryoSleep'].fillna(False)
    df.drop(columns=['expenses','expenses_w_o_na'], inplace=True)
    return df
def fill_missing_vip(df):
    df['VIP']=np.where(df['VIP'].isnull()&((df['Age']<18)|(df['HomePlanet']=='Earth')),False,df['VIP'])
    df['VIP']=np.where(df['VIP'].isnull()&((df['Age']<25)&(df['HomePlanet']=='Europa')),False,df['VIP'])
    df.loc[(df['VIP'].isna() & (df['deck'].isin(['G', 'T']))), 'VIP'] = False
    # df.loc[df['VIP'].isna(), 'VIP'] = False
    return df
def fill_missing_expenses(df,expense_col):
    for col in expense_col:
        df[col]=np.where(df[col].isnull()&((df['CryoSleep']==True)|(df['Age'] < 13)), 0, df[col])
    return df
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_folder = os.path.join(current_dir, 'pre_imputer')
sys.path.append(modules_folder)
from homeplanet_surname_imputer import HS_Imputer
from homeplanet_group_imputer import HG_Imputer
from homeplanet_ddc_imputer import HDDC_Imputer
def preprocess_data(train,test,valid=None):
    HS_cleaner=HS_Imputer()
    HG_cleaner=HG_Imputer()
    HDDC_cleaner=HDDC_Imputer()
    expense_col=['RoomService','FoodCourt','ShoppingMall','Spa','VRDeck']
    if valid is None:
        train=feature_expansion(train,'Transported')
        train=fill_missing_homeplanets(train,HS_cleaner,HG_cleaner,HDDC_cleaner,'Train')
        train=fill_missing_destination(train)
        train=fill_missing_cryo_sleep(train,expense_col)
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col)
        test=feature_expansion(test)
        test=fill_missing_homeplanets(test,HS_cleaner,HG_cleaner,HDDC_cleaner,'Test')
        test=fill_missing_destination(test)
        test=fill_missing_cryo_sleep(test,expense_col)
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col)
        return train,test
    else:
        train=feature_expansion(train,'Transported')
        train=fill_missing_homeplanets(train,HS_cleaner,HG_cleaner,HDDC_cleaner,'Train')
        train=fill_missing_destination(train)
        train=fill_missing_cryo_sleep(train,expense_col)
        # train=fill_missing_vip(train)
        # train=fill_missing_expenses(train,expense_col)
        valid=feature_expansion(valid,'Transported')
        valid=fill_missing_homeplanets(valid,HS_cleaner,HG_cleaner,HDDC_cleaner,'Validate')
        valid=fill_missing_destination(valid)
        valid=fill_missing_cryo_sleep(valid,expense_col)
        # valid=fill_missing_vip(valid)
        # valid=fill_missing_expenses(valid,expense_col)
        test=feature_expansion(test)
        test=fill_missing_homeplanets(test,HS_cleaner,HG_cleaner,HDDC_cleaner,'Test')
        test=fill_missing_destination(test)
        test=fill_missing_cryo_sleep(test,expense_col)
        # test=fill_missing_vip(test)
        # test=fill_missing_expenses(test,expense_col)
        HS_cleaner.get_hs_df().to_csv('s_name.csv',index=False)
        return train,valid,test