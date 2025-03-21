import pandas as pd
import numpy as np
from sklearn.utils import resample
def synthetic_data(df,seed_val=45):
    np.random.seed(seed_val)
    n_augmented_samples = len(df)
    print(f"""Generating {n_augmented_samples} samples for augmentation: """)
    X_train_bootstrap, y_train_bootstrap = resample(df.loc[:,df.columns!='SalePrice'],df.loc[:,'SalePrice'], n_samples=n_augmented_samples, replace=True, random_state=42)
    synthetic_data=pd.concat([X_train_bootstrap, y_train_bootstrap], axis=1)
    synthetic_data['Id']=(synthetic_data['Id'].astype(str) + '_' + (synthetic_data.groupby('Id').cumcount() + 1).astype(str))
    synthetic_data['BsmtFinSF1'] = np.where(
    synthetic_data['BsmtFinType1'].isin(['NA', 'Unf']),  # Condition
    synthetic_data['BsmtFinSF1'],  # Keep as is
    np.expm1(np.log1p(synthetic_data['BsmtFinSF1'])+np.random.normal(0,np.log1p(df[~df['BsmtFinType1'].isin(['NA', 'Unf'])]['BsmtFinSF1']).std()*0.01,size=len(synthetic_data)))
    )
    # synthetic_data['BsmtFinSF2'] = np.where(
    #     synthetic_data['BsmtFinType2'].isin(['NA', 'Unf']),  # Condition
    #     synthetic_data['BsmtFinSF2'],  # Keep as is
    #     np.power((np.sqrt(synthetic_data['BsmtFinSF2'])+np.random.normal(0,np.sqrt(df[~df['BsmtFinType2'].isin(['Unf','NA'])]['BsmtFinSF2']).std()*0.01,size=len(synthetic_data))),2)
    #     )
    synthetic_data['BsmtUnfSF'] = np.where(
        synthetic_data['BsmtQual']=='NA',  # Condition
        synthetic_data['BsmtUnfSF'],  # Keep as is
        np.power((np.sqrt(synthetic_data['BsmtUnfSF'])+np.random.normal(0,np.sqrt(df[df['BsmtQual']!='NA']['BsmtUnfSF']).std()*0.01,size=len(synthetic_data))),2)
        )
    # synthetic_data['BsmtUnfSF']=np.power((np.sqrt(synthetic_data['BsmtUnfSF'])+np.random.normal(0,np.sqrt(df['BsmtUnfSF']).std()*0.01,size=len(synthetic_data))),2)
    synthetic_data['TotalBsmtSF']=synthetic_data[['BsmtFinSF1','BsmtFinSF2','BsmtUnfSF']].sum(axis=1, skipna=True)
    synthetic_data['GarageArea']=np.where(
        synthetic_data['GarageType']=='NA',
        synthetic_data['GarageArea'],
        np.power((np.sqrt(synthetic_data['GarageArea'])+np.random.normal(0,np.sqrt(df[df['GarageType']!='NA']['GarageArea']).std()*0.01,size=len(synthetic_data))),2)
    )
    synthetic_data['WoodDeckSF']=np.where(
        synthetic_data['WoodDeckSF']==0,
        0,
        np.power((np.sqrt(synthetic_data['WoodDeckSF'])+np.random.normal(0,np.sqrt(df[df['WoodDeckSF']!=0]['WoodDeckSF']).std()*0.01,size=len(synthetic_data))),2)
    )
    synthetic_data['OpenPorchSF'] = np.where(
    synthetic_data['OpenPorchSF']==0,  # Condition
    0,  # Keep as is
    np.expm1(np.log1p(synthetic_data['OpenPorchSF'])+np.random.normal(0,np.log1p(df[df['OpenPorchSF']!=0]['OpenPorchSF']).std()*0.01,size=len(synthetic_data)))
    )
    synthetic_data['EnclosedPorch']=np.where(synthetic_data['EnclosedPorch']==0,0,synthetic_data['EnclosedPorch']+np.random.normal(0,df[df['EnclosedPorch']!=0]['EnclosedPorch'].std()*0.01,size=len(synthetic_data)))
    # synthetic_data['3SsnPorch']=np.where(
    #     synthetic_data['3SsnPorch']==0,
    #     0,
    #     np.power((np.sqrt(synthetic_data['3SsnPorch'])+np.random.normal(0,np.sqrt(df[df['3SsnPorch']!=0]['3SsnPorch']).std()*0.01,size=len(synthetic_data))),2)
    # )
    # synthetic_data['ScreenPorch']=np.where(
    #     synthetic_data['ScreenPorch']==0,
    #     0,
    #     np.power((np.sqrt(synthetic_data['ScreenPorch'])+np.random.normal(0,np.sqrt(df[df['ScreenPorch']!=0]['ScreenPorch']).std()*0.01,size=len(synthetic_data))),2)
    # )
    synthetic_data['1stFlrSF']=np.expm1(np.log1p(synthetic_data['1stFlrSF'])+np.random.normal(0,np.log1p(df['1stFlrSF']).std()*0.01,size=len(synthetic_data)))
    synthetic_data['2ndFlrSF']=np.where(synthetic_data['2ndFlrSF']==0,0,np.power((np.sqrt(synthetic_data['2ndFlrSF'])+np.random.normal(0,np.sqrt(df['2ndFlrSF']).std()*0.01,size=len(synthetic_data))),2))
    synthetic_data['GrLivArea']=synthetic_data[['1stFlrSF','2ndFlrSF','LowQualFinSF']].sum(axis=1, skipna=True)#np.power((np.sqrt(synthetic_data['GrLivArea'])+np.random.normal(0,np.sqrt(df['GrLivArea']).std()*0.01,size=len(synthetic_data))),2)
    synthetic_data['MasVnrArea']=np.where(synthetic_data['MasVnrType']=='None',
                                          0,
                                          np.power((np.sqrt(synthetic_data['MasVnrArea'])+np.random.normal(0,np.sqrt(df[df['MasVnrType']!='None']['MasVnrArea']).std()*0.01,size=len(synthetic_data))),2))    #np.expm1(np.log1p(synthetic_data['MasVnrArea'])+np.random.normal(0,np.log1p(df['MasVnrArea']).std()*0.01,size=len(synthetic_data)))
    synthetic_data['LotArea']=np.expm1(np.log1p(synthetic_data['LotArea'])+np.random.normal(0,np.log1p(df['LotArea']).std()*0.01,size=len(synthetic_data)))
    synthetic_data['LotFrontage']=np.power((np.sqrt(synthetic_data['LotFrontage'])+np.random.normal(0,np.sqrt(df['LotFrontage']).std()*0.01,size=len(synthetic_data))),2)
    synthetic_data['SalePrice']=synthetic_data['SalePrice']*np.exp(np.random.normal(0,(np.log(df['SalePrice']/100000)).std() * 0.01, size=len(synthetic_data)))
    synthetic_data.to_csv('synthetic_data.csv',index=False)
    return synthetic_data
def augment_data(df,new_data=None,seed_val=45):
    df_augmented=df.copy()
    if new_data is None:
        synthetic_df=synthetic_data(df_augmented,seed_val)
        df_aug = pd.concat([df_augmented, synthetic_df], axis=0, ignore_index=True)
    else:
        df_aug = pd.concat([df_augmented, new_data], axis=0, ignore_index=True)
    print(f"""Data set size increased from {len(df)} to {len(df_aug)} samples following augmentation""")
    return df_aug