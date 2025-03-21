import pandas as pd
import numpy as np
from scipy.stats import f_oneway,spearmanr
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
def get_cat_feat(df,features,target_col,p_stat):
    best_cat=[]
    for col in features:
        categories = df[col].unique()
        if len(categories) <= 1:  # Skip columns with one or zero categories
            print(f"Skipping column '{col}' as it has {len(categories)} unique category(s).")
            continue
        groups = [df[df[col] == cat][target_col] for cat in categories]
        f_stat, p_value = f_oneway(*groups)
        # print("Feature: ",col)
        # print("F-statistic:", f_stat)
        # print("P-value:", p_value)
        if p_value<p_stat:
            best_cat.append(col)
    return best_cat
def select_best_continuous_features(data, features, target, corr_threshold=0.5,mi_threshold=0.1):
    results = []
    scaler = StandardScaler()
    # Iterate through each continuous feature and calculate statistics
    data[features] = scaler.fit_transform(data[features])
    for feature in features:
        # Pearson Correlation
        pearson_corr = data[feature].corr(data[target])
        
        # Spearman Correlation (non-linear relationships)
        spearman_corr, _ = spearmanr(data[feature], data[target])

        mi_score = mutual_info_regression(data[[feature]], data[target])[0]

        # Collect results
        results.append({
            'Feature': feature,
            'Pearson Corr': pearson_corr,
            'Spearman Corr': spearman_corr,
            'Mutual Info': mi_score
        })

    # Convert results to DataFrame
    stats_df = pd.DataFrame(results)
    
    # Apply selection criteria (e.g., Corr > threshold)
    selected_features = stats_df[
        (stats_df['Pearson Corr'].abs() > corr_threshold) |
        (stats_df['Spearman Corr'].abs() > corr_threshold)|
        (stats_df['Mutual Info'] > mi_threshold)
    ]['Feature'].tolist()
    
    return stats_df.sort_values(by='Pearson Corr', ascending=False), selected_features