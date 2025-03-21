import numpy as np
import pandas as pd
class Lfrontage:
    def __init__(self):
        self.df_group_1=None
        self.df_group_2=None
        self.df_group_3=None
        self.bin_edges=None
    def fit(self,df):
        def skewness(x):
            return x.skew() if len(x) > 2 else np.nan
        data=df[['LotArea','MSZoning','Neighborhood','LotShape','BldgType','LotConfig','Alley','LotFrontage']].copy()
        data['LotArea_transformed']=np.sqrt(data['LotArea'])
        n = len(data['LotArea_transformed'])
        IQR = np.percentile(data['LotArea_transformed'], 75) - np.percentile(data['LotArea_transformed'], 25)
        bin_width_sqrt = 2 * IQR / (n ** (1 / 3))
        num_bins_sqrt = int(np.ceil((data['LotArea_transformed'].max() - data['LotArea_transformed'].min()) / bin_width_sqrt))
        self.bin_edges = np.linspace(data['LotArea_transformed'].min(), data['LotArea_transformed'].max(), num_bins_sqrt + 1).tolist()
        self.bin_edges=np.append([-np.inf],self.bin_edges).tolist()
        self.bin_edges.append(np.inf)
        data['LotArea_Bins'] = pd.cut(data['LotArea_transformed'], bins=self.bin_edges,labels=[f"Bin {i}" for i in range(len(self.bin_edges) - 1)],right=False)
        Q1 = data['LotFrontage'].quantile(0.25)
        Q3 = data['LotFrontage'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5* IQR
        upper_bound = Q3 + 1.5* IQR
        data['LotFrontage']=data['LotFrontage'].clip(lower=lower_bound, upper=upper_bound)
        tem1=data.groupby(['Neighborhood','LotArea_Bins','LotShape','LotConfig'])['LotFrontage'].agg(mean='mean',median='median',std='std',count='count',skew=skewness).reset_index()
        tem1['coefficient_of_variation'] = tem1['std'] / tem1['mean']
        tem1.to_csv('tem_1.csv')
        print(tem1[((tem1['std']<3)&(tem1['count']>10))|((tem1['coefficient_of_variation']<0.4)&(tem1['count']>10))|(tem1['coefficient_of_variation']==0)])
        self.df_group_1=tem1[((tem1['std']<3))|((tem1['coefficient_of_variation']<0.4)&(tem1['count']>10))|(tem1['coefficient_of_variation']==0)].drop(columns=['mean','count','skew','coefficient_of_variation']).rename(columns={'median':'LotFrontage'})
        tem2=data.groupby(['Neighborhood','LotShape','LotConfig','BldgType'])['LotFrontage'].agg(mean='mean',median='median',std='std',count='count',skew=skewness).reset_index()
        tem2['coefficient_of_variation'] = tem2['std'] / tem2['mean']
        tem2.to_csv('tem_2.csv')
        self.df_group_2=tem2.drop(columns=['mean','count','skew','coefficient_of_variation']).rename(columns={'median':'LotFrontage'})
        tem3=data.groupby(['Neighborhood'])['LotFrontage'].agg(mean='mean',median='median',std='std',count='count',skew=skewness).reset_index()
        tem3['coefficient_of_variation'] = tem3['std'] / tem3['mean']
        tem3.to_csv('tem_3.csv')
        self.df_group_3=tem3[((tem3['std']<3))|(tem3['coefficient_of_variation']==0)].drop(columns=['mean','count','skew','coefficient_of_variation']).rename(columns={'median':'LotFrontage'})

    def transform(self,df):
        if self.df_group_1.empty:
            raise ValueError("df_group not fitted")
        else:
            noise_mean = 0       # Centered at 0
            noise_std = 0.01      # Small standard deviation
            noise = np.random.normal(noise_mean, noise_std, size=len(df))
            df['LotArea_transformed']=np.sqrt(df['LotArea'])
            df['LotArea_Bins'] = pd.cut(df['LotArea_transformed'], bins=self.bin_edges,labels=[f"Bin {i}" for i in range(len(self.bin_edges) - 1)],right=False)
            df=pd.merge(df, self.df_group_1, on=['Neighborhood','LotArea_Bins','LotShape','LotConfig'], how='left', suffixes=('', '_1'))
            df['noise']=np.random.normal(noise_mean,df['std']*noise_std)
            df['noise']=np.where(df['noise'].isnull(),0,df['noise'])
            df['LotFrontage']=np.where(df['LotFrontage'].isnull(),df['LotFrontage_1']+df['noise'],df['LotFrontage'])
            # df=pd.merge(df, self.df_group_2, on=['Neighborhood','LotShape','LotConfig'], how='left', suffixes=('', '_2'))
            # df['noise_2']=np.random.normal(noise_mean,df['std_2']*noise_std)
            # df['noise_2']=np.where(df['noise_2'].isnull(),0,df['noise_2'])
            # df['LotFrontage']=np.where(df['LotFrontage'].isnull(),df['LotFrontage_2']+df['noise_2'],df['LotFrontage'])
            # df=pd.merge(df, self.df_group_3, on=['Neighborhood'], how='left', suffixes=('', '_3'))
            # df['noise_3']=np.random.normal(noise_mean,df['std_3']*noise_std)
            # df['noise_3']=np.where(df['noise_3'].isnull(),0,df['noise_3'])
            # df['LotFrontage']=np.where(df['LotFrontage'].isnull(),df['LotFrontage_3']+df['noise_3'],df['LotFrontage'])
        return df
    
    def fit_transform(self,df):
        self.fit(df)
        return self.transform(df)