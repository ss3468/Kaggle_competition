import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
class MNBHYE_rf:
    def __init__(self,random_state=42):
        self.model = RandomForestClassifier(random_state=random_state)
        self.features=['Neighborhood','BldgType','HouseStyle','YearBuilt', 'Exterior1st']
        self.is_fitted = False
    def fit(self,df):
        train_df=df[df['MasVnrType'].notnull()]
        self.model.fit(train_df[self.features], train_df['MasVnrType'])
        self.is_fitted = True
    def transform(self,df):
       if not self.is_fitted:
            raise ValueError("The model is not fitted yet. Please call 'fit' before 'transform'.")
       missing_data = df[df['MasVnrType'].isnull()]
       missing_indices = df[df['MasVnrType'].isnull()].index
       if missing_data.empty:
            return df
       predicted_values = self.model.predict(missing_data[self.features])
       df.iloc[missing_indices, 'MasVnrType'] = predicted_values
       return df
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    def get_model(self):
        return self.model