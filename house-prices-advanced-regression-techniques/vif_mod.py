from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
def calculate_vif(X):
    vif_df = pd.DataFrame()
    vif_df["Feature"] = X.columns
    vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif_df = vif_df.sort_values(by="VIF", ascending=False).reset_index(drop=True)
    return vif_df
def vif_selection(df, threshold=5,redundancies=None):
    """Iteratively remove features with VIF above the threshold."""
    X=df.copy()
    if redundancies:
        redundancies = [col for col in redundancies if col in X.columns]
        X=X.drop(columns=redundancies)
    while True:
        vif_data = calculate_vif(X)
        max_vif = vif_data["VIF"].max()
        if max_vif < threshold:
            break
        else:
            # Drop the feature with the highest VIF
            drop_feature = vif_data.sort_values("VIF", ascending=False)["Feature"].iloc[0]
            X.drop(columns=[drop_feature], inplace=True)
            print(f"Dropped '{drop_feature}' with VIF: {max_vif:.2f}")
    final_vif_df = calculate_vif(X)
    best_features = final_vif_df["Feature"].values
    return final_vif_df,best_features