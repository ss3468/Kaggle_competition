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
def get_total_expense(df,col_to_fill,target_col=None):
    if target_col:
        removed_column = df[target_col].values
        df.drop(columns=[target_col], inplace=True)
        df['expenses'] = df[col_to_fill].sum(axis=1,skipna=False)
        df['expenses_w_o_na'] = df[col_to_fill].sum(axis=1,skipna=True)
        df[target_col]=removed_column
    else:
        df['expenses'] = df[col_to_fill].sum(axis=1,skipna=False)
        df['expenses_w_o_na'] = df[col_to_fill].sum(axis=1,skipna=True)
    return df
def engineer_data(col_to_fill,train,test,valid=None):
    if valid is None:
        train=feature_expansion(train,'Transported')
        train=get_total_expense(train,col_to_fill,'Transported')
        test=feature_expansion(test)
        test=get_total_expense(test,col_to_fill)
        return train,test
    else:
        train=feature_expansion(train,'Transported')
        train=get_total_expense(train,col_to_fill,'Transported')
        valid=feature_expansion(valid,'Transported')
        valid=get_total_expense(valid,col_to_fill,'Transported')
        test=feature_expansion(test)
        test=get_total_expense(test,col_to_fill)
        return train,valid,test
    # create way to fill homeplanet using features not strongly related to target
def g_imputer(df,cl,state):
    if state=='Train':
        df=cl.fit_transform(df)
    elif(state=='Validate')|(state=='Test'):
        df=cl.transform(df)
    else:
        print('please input proper State')
    return df
def fill_missing_homeplanets(df,cl1,cl2,state):
    df=g_imputer(df,cl1,state)#group number
    df=g_imputer(df,cl2,state)#Surname number
    df.loc[(df['HomePlanet'].isna()) & (df['deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet']='Europa'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='G'), 'HomePlanet']='Earth'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='D'), 'HomePlanet']='Mars'
    df.loc[(df['HomePlanet'].isna()) & ~(df['deck']=='D'), 'HomePlanet']='Earth'
    return df
def fill_missing_cryo_sleep(df):
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&((df['expenses']>0)|(df['expenses'].isnull()&(df['expenses_w_o_na']>0))),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='A')&(df['Destination']=='55 Cancri e'),True,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='G')&(df['Age']>56),True,df['CryoSleep'])# fill cryosleep for mars if age>56 and expenses are 0
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='G')&(df['Age']>12)&((df['Destination']=='PSO J318.5-22')|(df['Destination']=='55 Cancri e')),True,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='B')&(df['Age']>=13)&(df['Age']<=68)&(df['Destination']=='55 Cancri e'),True,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='C')&(df['Age']>=13)&(df['Age']<=64)&(df['Destination']=='55 Cancri e'),True,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='F')&(df['Age']>20)&(df['HomePlanet']=='Mars'),True,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='F')&(df['Age']>9)&(df['HomePlanet']=='Earth'),True,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses']==0)&(df['deck']=='F')&(df['Age']<2)&(df['HomePlanet']=='Earth'),False,df['CryoSleep'])
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&(df['expenses_w_o_na']==0),True,df['CryoSleep'])
    return df
def fill_missing_vip(df):
    df['VIP']=np.where((df['VIP'].isnull())&(df['HomePlanet']=='Earth'),False,df['VIP'])
    df['VIP']=np.where((df['VIP'].isnull())&(df['HomePlanet']=='Europa')&(df['Age']<25),False,df['VIP'])
    df['VIP']=np.where((df['VIP'].isnull())&(df['HomePlanet']=='Mars')&((df['CryoSleep'])|(df['Age']<18)|(df['Destination']=='55 Cancri e')),False,df['VIP'])
    #df['VIP']=np.where((df['VIP'].isnull())&(df['HomePlanet']=='Europa')&(df['Age']>=25),False,df['VIP'])
    #df['VIP']=np.where((df['VIP'].isnull())&(df['HomePlanet']=='Mars')&(df['Age']>=18)&((df['Destination']!='55 Cancri e')&(df['Destination'].isna())),False,df['VIP'])
    #df['VIP']=np.where((df['VIP'].isnull())&(df['Age']<=12),False,df['VIP'])
    return df
def fill_zero_expense_col(df,expense_col):
    df.drop(columns=['expenses','expenses_w_o_na'], inplace=True)
    for col in expense_col:
        df[col]=np.where(df[col].isnull()&((df['CryoSleep']==True)|(df['Age'] < 13)), 0, df[col])
    df['expenses'] = df[expense_col].sum(axis=1,skipna=False)
    df['expenses_w_o_na'] = df[expense_col].sum(axis=1,skipna=True)
    return df
def fill_missing_expenses(df,expense_col):
    # add function for filling in 0 expenses
    df=fill_zero_expense_col(df,expense_col)
    # find way to fill missing expenses based on VIP,Cryosleep, HomePlanet pending with noise to reduce bias
    return df
def fill_missing_dest(df):
    df['Destination']=np.where((df['Destination'].isnull())&(df['expenses']==0)&(df['Age']>12)&(df['CryoSleep']==False),"TRAPPIST-1e",df['Destination'])
    return df
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_folder = os.path.join(current_dir, 'pre_imputer')
sys.path.append(modules_folder)
from homeplanet_group_imputer import HG_Imputer
from homeplanet_surname_imputer import HS_Imputer
def fill_missing_values(train,test,valid=None):
    HG_cleaner=HG_Imputer()
    HS_cleaner=HS_Imputer()
    expense_col=['RoomService','FoodCourt','ShoppingMall','Spa','VRDeck']
    if valid is None:
        train=fill_missing_homeplanets(train,HG_cleaner,HS_cleaner,'Train')
        train=fill_missing_cryo_sleep(train)
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col)
        train=fill_missing_dest(train)
        test=fill_missing_homeplanets(test,HG_cleaner,HS_cleaner,'Test')
        test=fill_missing_cryo_sleep(test)
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col)
        test=fill_missing_dest(test)
        return train,test
    else:
        train=fill_missing_homeplanets(train,HG_cleaner,HS_cleaner,'Train')
        train=fill_missing_cryo_sleep(train)
        train=fill_missing_vip(train)
        train=fill_missing_expenses(train,expense_col)
        train=fill_missing_dest(train)
        valid=fill_missing_homeplanets(valid,HG_cleaner,HS_cleaner,'Validate')
        valid=fill_missing_cryo_sleep(valid)
        valid=fill_missing_vip(valid)
        valid=fill_missing_expenses(valid,expense_col)
        valid=fill_missing_dest(valid)
        test=fill_missing_homeplanets(test,HG_cleaner,HS_cleaner,'Test')
        test=fill_missing_cryo_sleep(test)
        test=fill_missing_vip(test)
        test=fill_missing_expenses(test,expense_col)
        test=fill_missing_dest(test)
        return train,valid,test