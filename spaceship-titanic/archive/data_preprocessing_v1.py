import pandas as pd
import numpy as np
def fill_planet_surname(df,cl,state):
    if state=='Train':
        df=cl.fit_transform(df)
    elif(state=='Validate')|(state=='Test'):
        df=cl.transform(df)
    else:
        print('please input proper State')
    return df
def fill_planets_deck(df):
    df[['deck','num','side']]=df['Cabin'].str.split('/',expand=True)
    df.drop(columns=['Cabin'], inplace=True)
    df.loc[(df['HomePlanet'].isna()) & (df['deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet']='Europa'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='G'), 'HomePlanet']='Earth'
    df.loc[(df['HomePlanet'].isna()) & ~(df['deck']=='D'), 'HomePlanet']='Earth'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='D'), 'HomePlanet']='Mars'
    return df
def fill_missing_homeplanets(df,cl,state,target_col=None):
    if target_col:
        removed_column = df[target_col].values
        df.drop(columns=[target_col], inplace=True)
        df[['First_name','Surname']] = df['Name'].str.split(' ', expand=True)
        df=fill_planet_surname(df,cl,state)
        df=fill_planets_deck(df)
        df[target_col]=removed_column
    else:
        df[['First_name','Surname']] = df['Name'].str.split(' ', expand=True)
        df=fill_planet_surname(df,cl,state)
        df=fill_planets_deck(df)
    return df
def fill_missing_cryo_sleep(df,col_to_fill):
    df['expenses'] = df[col_to_fill].sum(axis=1,skipna=False)
    df['expenses_w_o_na'] = df[col_to_fill].sum(axis=1,skipna=True)
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&((df['expenses']>0)|(df['expenses'].isnull()&(df['expenses_w_o_na']>0))),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0),True,df['CryoSleep'])
    df['CryoSleep']=df['CryoSleep'].fillna(False)
    df.drop(columns=['expenses','expenses_w_o_na'], inplace=True)
    return df
def fill_missing_destination(df):
    df['Destination']=np.where(df['Destination'].isnull(),'TRAPPIST-1e',df['Destination'])
    return df
def fill_missing_age(df,cl,state,target_col=None):
    if state=='Train':
        df=cl.fit_transform(df)
    elif(state=='Validate')|(state=='Test'):
        df=cl.transform(df)
    else:
        print('please input proper State')
    if target_col:
        removed_column = df[target_col].values
        df.drop(columns=[target_col], inplace=True)
        df[target_col]=removed_column
        return df
    else:
        return df
def fill_missing_vip(df):
    df.loc[df['VIP'].isna(),'VIP']=False
    # df['VIP']=np.where(df['VIP'].isnull()&((df['Age']<18)|(df['HomePlanet']=='Earth')),False,df['VIP'])
    # df['VIP']=np.where(df['VIP'].isnull()&(df['Age']<25)&(df['HomePlanet']=='Europa'),False,df['VIP'])
    # df['VIP']=np.where(df['VIP'].isnull()&(df['deck']=='T'),False,df['VIP'])
    # df['VIP']=np.where(df['VIP'].isnull()&(df['CryoSleep']==False)&(df['HomePlanet']=='Mars')&(df['Age']>18)&(df['Destination']!='55 Cancri e'),False,df['VIP'])
    # df['VIP']=np.where(df['VIP'].isnull()&(df['CryoSleep']==True),False,df['VIP'])
    return df
def fill_missing_expenses(df,expense_col,cl,state,target_col=None):
    for col in expense_col:
        df[col]=np.where(df[col].isnull()&((df['CryoSleep']==True)|(df['Age'] < 13)), 0, df[col])
    #return df
    # age_group column to be created 0~18, 18~38, and 38~
    if state=='Train':
        df=cl.fit_transform(df)
    elif(state=='Validate')|(state=='Test'):
        df=cl.transform(df)
    else:
        print('please input proper State')
    if target_col:
        removed_column = df[target_col].values
        df['expenses'] = df[expense_col].sum(axis=1,skipna=False)
        df.drop(columns=[target_col], inplace=True)
        df[target_col]=removed_column
        return df
    else:
        df['expenses'] = df[expense_col].sum(axis=1,skipna=False)
        return df
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_folder = os.path.join(current_dir, 'pre_imputer')
sys.path.append(modules_folder)
from homeplanet_surname_imputer import HS_Imputer
from HCD_Age_imputer import HCDA_Imputer
from Expense_Imputer import E_Imputer
def preprocess_data(train,test,valid=None):
    HS_cleaner=HS_Imputer()
    HCDA_cleaner=HCDA_Imputer()
    expense_col=['RoomService','FoodCourt','ShoppingMall','Spa','VRDeck']
    E_cleaner=E_Imputer(['HomePlanet','CryoSleep','VIP','Age Interval'],expense_col)
    if valid is None:
        train=fill_missing_homeplanets(train,HS_cleaner,'Train','Transported')
        train=fill_missing_destination(train)
        train=fill_missing_cryo_sleep(train,expense_col)
        train=fill_missing_age(train,HCDA_cleaner,'Train','Transported')
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col,E_cleaner,'Train','Transported')
        test=fill_missing_homeplanets(test,HS_cleaner,'Test')
        test=fill_missing_destination(test)
        test=fill_missing_cryo_sleep(test,expense_col)
        test=fill_missing_age(test,HCDA_cleaner,'Test')
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col,E_cleaner,'Test')
        return train,test
    else:
        train=fill_missing_homeplanets(train,HS_cleaner,'Train','Transported')
        train=fill_missing_destination(train)
        train=fill_missing_cryo_sleep(train,expense_col)
        train=fill_missing_age(train,HCDA_cleaner,'Train','Transported')
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col,E_cleaner,'Train','Transported')
        valid=fill_missing_homeplanets(valid,HS_cleaner,'Validate','Transported')
        valid=fill_missing_destination(valid)
        valid=fill_missing_cryo_sleep(valid,expense_col)
        valid=fill_missing_age(valid,HCDA_cleaner,'Validate','Transported')
        valid=fill_missing_vip(valid)
        valid=fill_missing_expenses(valid,expense_col,E_cleaner,'Validate','Transported')
        test=fill_missing_homeplanets(test,HS_cleaner,'Test')
        test=fill_missing_destination(test)
        test=fill_missing_cryo_sleep(test,expense_col)
        test=fill_missing_age(test,HCDA_cleaner,'Test')
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col,E_cleaner,'Test')
        E_cleaner.get_E_df().to_csv('expenses.csv',index=False)
        return train,valid,test
        