import numpy as np
import pandas as pd
class Lfrontage:
    def __init__(self):
        self.df_group_1=None
        self.df_group_2=None
        self.df_group_3=None
        self.df_group_4=None
        self.df_group_broad=None
        self.bin_edges=None
        self.lotfrontage_std=0
    def fit(self,df):
        data=df[['LotArea','MSZoning','Neighborhood','BldgType','LotShape','LotConfig','Alley','LotFrontage']].copy()
        data['LotArea_transformed']=np.sqrt(data['LotArea'])
        data['LotFrontage_mod']=np.log1p(data['LotFrontage'])
        n = len(data['LotArea_transformed'])
        Q1 = data['LotFrontage'].quantile(0.25)
        Q3 = data['LotFrontage'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        filtered_df = data[(data['LotFrontage'] >= lower_bound) & (data['LotFrontage'] <= upper_bound)]
        self.lotfrontage_std=filtered_df['LotFrontage'].std()
        IQR = np.percentile(data['LotArea_transformed'], 75) - np.percentile(data['LotArea_transformed'], 25)
        bin_width_sqrt = 2 * IQR / (n ** (1 / 3))
        num_bins_sqrt = int(np.ceil((data['LotArea_transformed'].max() - data['LotArea_transformed'].min()) / bin_width_sqrt))
        self.bin_edges = np.linspace(data['LotArea_transformed'].min(), data['LotArea_transformed'].max(), num_bins_sqrt + 1).tolist()
        self.bin_edges=np.append([-np.inf],self.bin_edges).tolist()
        self.bin_edges.append(np.inf)
        data['LotArea_Bins'] = pd.cut(data['LotArea_transformed'], bins=self.bin_edges,labels=[f"Bin {i}" for i in range(len(self.bin_edges) - 1)],right=False)
        tem1=data.groupby(['Neighborhood','MSZoning','LotShape','LotConfig'])['LotFrontage'].agg(['median', 'var']).reset_index()
        tem1=tem1[tem1['var']==0]
        print(tem1)
        tem2=data.groupby(['Neighborhood','Alley','LotShape','LotConfig'])['LotFrontage_mod'].agg(['median', 'var']).reset_index()
        tem2=tem2[tem2['var']<0.01]
        print(tem2)
        self.df_group_1=tem1.drop(columns=['var']).rename(columns={'median': 'LotFrontage'})
        self.df_group_2=tem2.drop(columns=['var']).rename(columns={'median': 'LotFrontage'})
        self.df_group_3=data.groupby(['Neighborhood','LotShape'])['LotFrontage'].median().reset_index()
        self.df_group_4=data.groupby(['Neighborhood','LotConfig'])['LotFrontage'].median().reset_index()
        self.df_group_broad=data.groupby(['Neighborhood'])['LotFrontage'].median().reset_index()
        upper_bound_original = (self.bin_edges[-2]) ** 2
        # print(f"Upper bound for last bin (original scale): {upper_bound_original}")
    def transform(self,df):
        if(self.df_group_1.empty)|(self.df_group_2.empty)|(self.df_group_3.empty):
            raise ValueError("df_group not fitted")
        else:
            df['LotArea_transformed']=np.sqrt(df['LotArea'])
            df['LotArea_Bins'] = pd.cut(df['LotArea_transformed'], bins=self.bin_edges,labels=[f"Bin {i}" for i in range(len(self.bin_edges) - 1)],right=False)
            noise_mean = 0       # Centered at 0
            noise_std = 0.01      # Small standard deviation
            print(noise_std)
            print(self.lotfrontage_std)
            noise = np.random.normal(noise_mean, noise_std, size=len(df))
            df=pd.merge(df, self.df_group_1, on=['Neighborhood','MSZoning','LotShape','LotConfig'], how='left', suffixes=('', '_1'))
            df['LotFrontage']=np.where(df['LotFrontage'].isnull(),df['LotFrontage_1'],df['LotFrontage'])
            df=pd.merge(df, self.df_group_2, on=['Neighborhood','Alley','LotShape','LotConfig'], how='left', suffixes=('', '_2'))
            df['LotFrontage']=np.where(df['LotFrontage'].isnull(),np.expm1(df['LotFrontage_2'])+noise,df['LotFrontage'])
            df['LotFrontage']=np.where(df['LotFrontage'].isnull(),(df['LotArea_transformed'] * 0.448)+noise,df['LotFrontage'])
            # df=pd.merge(df, self.df_group_3, on=['Neighborhood','LotShape'], how='left', suffixes=('', '_3'))
            # df['LotFrontage']=np.where(df['LotFrontage'].isnull(),round(df['LotFrontage_3']+noise,2),df['LotFrontage'])
            # df=pd.merge(df, self.df_group_4, on=['Neighborhood','LotConfig'], how='left', suffixes=('', '_4'))
            # df['LotFrontage']=np.where(df['LotFrontage'].isnull(),round(df['LotFrontage_4']+noise,2),df['LotFrontage'])
            # df=pd.merge(df, self.df_group_broad, on=['Neighborhood'], how='left', suffixes=('', '_broad'))
            # df['LotFrontage']=np.where(df['LotFrontage'].isnull(),round(df['LotFrontage_broad']+noise,2),df['LotFrontage'])
            #df.drop(columns=['LotArea_transformed','LotArea_Bins','LotFrontage_1'], inplace=True)
        return df
    def fit_transform(self,df):
        self.fit(df)
        return self.transform(df)