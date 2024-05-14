import pandas as pd
import numpy as np
def mod_passenger_id(df,target_col=None):
    if target_col:
        removed_column = df[target_col].values
        df.drop(columns=[target_col], inplace=True)
        df[['Group','pp']] = df['PassengerId'].str.split('_', expand=True)
        df['Group'] = df['Group'].apply(lambda x: int(x))
        df[target_col]=removed_column
    else:
        df[['Group','pp']] = df['PassengerId'].str.split('_', expand=True)
        df['Group'] = df['Group'].apply(lambda x: int(x))
    return df
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
    # df.loc[(df['HomePlanet'].isna()) & (df['deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet']='Europa'
    # df.loc[(df['HomePlanet'].isna()) & (df['deck']=='G'), 'HomePlanet']='Earth'
    # df.loc[(df['HomePlanet'].isna()) & (df['deck']=='D'), 'HomePlanet']='Mars'
    # df.loc[(df['HomePlanet'].isna()) & ~(df['deck']=='D'), 'HomePlanet']='Earth'
    return df
def fill_missing_homeplanets(df,cl,state,target_col=None):
    if target_col:
        removed_column = df[target_col].values
        df.drop(columns=[target_col], inplace=True)
        df['Surname'] = df['Name'].str.split(' ', expand=True)[1]
        df.drop(columns=['Name'], inplace=True)
        df=fill_planet_surname(df,cl,state)
        df=fill_planets_deck(df)
        df[target_col]=removed_column
    else:
        df['Surname'] = df['Name'].str.split(' ', expand=True)[1]
        df.drop(columns=['Name'], inplace=True)
        df=fill_planet_surname(df,cl,state)
        df=fill_planets_deck(df)
    return df
def fill_missing_cryo_sleep(df,col_to_fill):
    df['expenses'] = df[col_to_fill].sum(axis=1,skipna=False)
    df['expenses_w_o_na'] = df[col_to_fill].sum(axis=1,skipna=True)
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&((df['expenses']>0)|(df['expenses'].isnull()&(df['expenses_w_o_na']>0))),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['VIP']==True)&(df['HomePlanet']=='Mars'),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0),True,df['CryoSleep'])
    #df.loc[(df['CryoSleep'].isna()) & (df['deck']=='T'), 'CryoSleep']=False
    #df.drop(columns=['expenses','expenses_w_o_na'], inplace=True)
    return df
def fill_missing_vip(df):
    df['VIP']=np.where(df['VIP'].isnull()&((df['Age']<18)|(df['HomePlanet']=='Earth')),False,df['VIP'])
    df['VIP']=np.where(df['VIP'].isnull()&((df['Age']<25)&(df['HomePlanet']=='Europa')),False,df['VIP'])
    df.loc[(df['VIP'].isna() & (df['deck'].isin(['G', 'T']))), 'VIP'] = False
    return df
def fill_missing_expenses(df,expense_col):
    for col in expense_col:
        df[col]=np.where(df[col].isnull()&((df['CryoSleep']==True)|(df['Age'] < 13)), 0, df[col])
    return df
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_folder = os.path.join(current_dir, 'pre_imputer')
sys.path.append(modules_folder)
from homeplanet_surname_imputer import HS_Imputer
def preprocess_data(train,test,valid=None):
    HS_cleaner=HS_Imputer()
    expense_col=['RoomService','FoodCourt','ShoppingMall','Spa','VRDeck']
    if valid is None:
        train=mod_passenger_id(train,'Transported')
        train=fill_missing_homeplanets(train,HS_cleaner,'Train','Transported')
        train=fill_missing_cryo_sleep(train,expense_col)
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col)
        test=mod_passenger_id(test)
        test=fill_missing_homeplanets(test,HS_cleaner,'Test')
        test=fill_missing_cryo_sleep(test,expense_col)
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col)
        return train,test
    else:
        train=mod_passenger_id(train,'Transported')
        train=fill_missing_homeplanets(train,HS_cleaner,'Train','Transported')
        train=fill_missing_cryo_sleep(train,expense_col)
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col)
        valid=mod_passenger_id(valid,'Transported')
        valid=fill_missing_homeplanets(valid,HS_cleaner,'Validate','Transported')
        valid=fill_missing_cryo_sleep(valid,expense_col)
        valid=fill_missing_vip(valid)
        valid=fill_missing_expenses(valid,expense_col)
        test=mod_passenger_id(test)
        test=fill_missing_homeplanets(test,HS_cleaner,'Test')
        test=fill_missing_cryo_sleep(test,expense_col)
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col)
        HS_cleaner.get_hs_df().to_csv('s_name.csv',index=False)
        return train,valid,test