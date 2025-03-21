import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
def check_feature_bias(original_df,df,feature_name):
    contingency_table = pd.crosstab(original_df[feature_name], df[feature_name])
    print("Contingency Table:\n", contingency_table)
    chi2, p, dof, ex = chi2_contingency(contingency_table)
    print(f"Chi-Square Test p-value: {p:.4f}")
    return chi2, p, dof, ex
def chi_square_test_binary(imputed_data, feature_name, target):
    contingency_table = pd.crosstab(imputed_data[feature_name], imputed_data[target])
    print("Contingency Table:\n", contingency_table)
    chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)
    print(f"Chi-Square Test p-value: {p_val:.4f}")
    return chi2_stat,p_val
def bias_plot(original_df,df,feature_name):
    # Plot original vs imputed distributions
    plt.figure(figsize=(12, 6))
    sns.countplot(data=original_df, x=feature_name, label='Original', alpha=0.5, color='blue')
    sns.countplot(data=df, x=feature_name, label='Imputed', alpha=0.5, color='orange')
    plt.legend()
    plt.title('Comparison of Original and Imputed Category Distributions')
    plt.show()
def compare_statistics(original_data, imputed_data, feature_name):
    stats_original = original_data[feature_name].describe()
    stats_imputed = imputed_data[feature_name].describe()

    comparison = pd.DataFrame({
        'Original': stats_original,
        'Imputed': stats_imputed
    })

    return comparison