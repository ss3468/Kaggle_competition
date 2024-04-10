import pandas as pd
import numpy as np
def fill_planets_groups(df):
    df['Group'] = df['PassengerId'].apply(lambda x: x.split('_')[0]).astype(int)
    group_size = df['Group'].value_counts().to_dict()
    df['Group_Size'] = df['Group'].map(group_size)
    df['Solo']=df['Group_Size'].apply(lambda x: x == 1)
    tem=df[['Group','HomePlanet']].groupby(['Group'])['HomePlanet'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    df = pd.merge(df, tem, on='Group', how='left', suffixes=('', '_right'))
    df['HomePlanet']=np.where(df['HomePlanet'].isnull(),df['HomePlanet_right'],df['HomePlanet'])
    df.drop(columns=['HomePlanet_right'], inplace=True)
    return df
def fill_planets_surnames(df):
    df[['First_name','Surname']] = df['Name'].str.split(' ', expand=True)
    tem=df[['Surname','HomePlanet']].groupby(['Surname'])['HomePlanet'].apply(lambda x: x.mode().iloc[0] if len(x.dropna()) > 0 else None).reset_index()
    df = pd.merge(df, tem, on='Surname', how='left', suffixes=('', '_right'))
    df['HomePlanet']=np.where(df['HomePlanet'].isnull(),df['HomePlanet_right'],df['HomePlanet'])
    df.drop(columns=['HomePlanet_right'], inplace=True)
    return df
def fill_planets_deck(df):
    df[['deck','num','side']]=df['Cabin'].str.split('/',expand=True)
    df.loc[(df['HomePlanet'].isna()) & (df['deck'].isin(['A', 'B', 'C', 'T'])), 'HomePlanet']='Europa'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='G'), 'HomePlanet']='Earth'
    df.loc[(df['HomePlanet'].isna()) & ~(df['deck']=='D'), 'HomePlanet']='Earth'
    df.loc[(df['HomePlanet'].isna()) & (df['deck']=='D'), 'HomePlanet']='Mars'
    return df
def fill_missing_planets_merge(train,test):
    train_id=train['PassengerId'].values
    test_id=test['PassengerId'].values
    removed_column = train['Transported']
    train.drop(columns=['Transported'], inplace=True)
    df=pd.concat([train, test],ignore_index=True)
    df.to_csv('data_merge_pre.csv',index=False)
    df=fill_planets_groups(df)
    df=fill_planets_surnames(df)
    df=fill_planets_deck(df)
    train=df[df['PassengerId'].isin(train_id)]
    test=df[df['PassengerId'].isin(test_id)]
    train['Transported']=removed_column
    return train,test
def fill_expense_cryo_sleep(df):
    col_to_fill=['RoomService','FoodCourt','ShoppingMall','Spa','VRDeck']
    df['expenses'] = df[col_to_fill].sum(axis=1,skipna=False)
    df['expenses_w_o_na'] = df[col_to_fill].sum(axis=1,skipna=True)
    df['CryoSleep']=np.where(df['CryoSleep'].isnull()&((df['expenses']>0)|(df['expenses'].isnull()&(df['expenses_w_o_na']>0))),False,df['CryoSleep'])
    for col in col_to_fill:
        df[col]=np.where(df[col].isnull()&((df['CryoSleep']==True)|(df['Age'] < 13)), 0, df[col])
    #df.drop(columns=['expenses','expenses_w_o_na'], inplace=True)
    return df
def fill_missing_vip(df):
    df['VIP']=np.where(df['VIP'].isnull()&((df['Age']<18)|(df['HomePlanet']=='Earth')),False,df['VIP'])
    return df
def fill_missing_destination(df):
    df['Destination']=np.where(df['Destination'].isnull(),'TRAPPIST-1e',df['Destination'])
    return df