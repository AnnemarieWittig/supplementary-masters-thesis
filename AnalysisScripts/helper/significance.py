from scipy.stats import shapiro, ttest_rel, wilcoxon
import pandas as pd
import numpy as np
from numpy import std, mean, sqrt

def check_normality_of_buckets(commit_result_df, pre_columns, after_columns):
    # Initialize a list to store results
    results = []

    # Loop through each repository
    for repo_name in commit_result_df['repository'].unique():
        repo_df = commit_result_df[commit_result_df['repository'] == repo_name]
        
        # Extract pre and after values for the repository
        pre_values = commit_result_df[commit_result_df['repository'] == repo_name][pre_columns].values.flatten()
        after_values = commit_result_df[commit_result_df['repository'] == repo_name][after_columns].values.flatten()

        # Drop NaNs
        pre_values = pre_values[~np.isnan(pre_values)]
        after_values = after_values[~np.isnan(after_values)]

        # Shapiro-Wilk test for normality
        pre_stat, pre_p = shapiro(pre_values)
        after_stat, after_p = shapiro(after_values)

        # Append results
        results.append({
            'repository': repo_name,
            'pre_p_value': pre_p,
            'after_p_value': after_p,
            'pre_normal': pre_p > 0.05,
            'after_normal': after_p > 0.05
        })


    # Convert results to a DataFrame for easier analysis
    normality_results = pd.DataFrame(results)
    return normality_results


def use_normality_results_for_significance_dependent(normality_results, commit_result_df, pre_columns, after_columns, reverse=False):
    significance_results = []
    # Loop through each repository
    for _, row in normality_results.iterrows():
        repo_name = row['repository']
        pre_values = commit_result_df[commit_result_df['repository'] == repo_name][pre_columns].values.flatten()
        after_values = commit_result_df[commit_result_df['repository'] == repo_name][after_columns].values.flatten()

        if reverse:
            after_values = after_values[::-1]

        # Filter out pairs where either value is NaN
        valid_mask = ~np.isnan(pre_values) & ~np.isnan(after_values)
        pre_values = pre_values[valid_mask]
        after_values = after_values[valid_mask]
        
        print(f"{repo_name}: mean(pre)={np.mean(pre_values):.2f}, mean(after)={np.mean(after_values):.2f}")


        if len(pre_columns) != len(after_columns):
            print (repo_name)
            print(pre_values)
            print(after_values)

        # Perform the appropriate test based on normality
        if row['pre_normal'] and row['after_normal']:
            # Paired t-test for normal data
            stat, p_value = ttest_rel(pre_values, after_values)
            test_used = "t-test (ES Cohens d)"
            
            nx = len(pre_values)
            ny = len(after_values)
            dof = nx + ny - 2
            effect_size = (np.mean(pre_values) - np.mean(after_values)) / sqrt(((nx-1)*std(pre_values, ddof=1) ** 2 + (ny-1)*std(after_values, ddof=1) ** 2) / dof)

        else:
            # Wilcoxon Signed-Rank Test for non-normal data
            stat, p_value = wilcoxon(pre_values, after_values)
            test_used = "Wilcoxon (ES r)"

            # Calculate z-score and effect size (r)
            n = len(pre_values)
            mean_w = n * (n + 1) / 4
            std_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
            z = (stat - mean_w) / std_w
            effect_size = z / np.sqrt(n)

        # Append results
        significance_results.append({
            'repository': repo_name,
            'test_used': test_used,
            'statistic': stat,
            'p_value': p_value,
            'significant': p_value < 0.05,  # True if p-value < 0.05
            'effect_size': effect_size
        })

    # Convert significance results to a DataFrame
    significance_results_df = pd.DataFrame(significance_results)
    return significance_results_df

def calculate_cliffs_delta(commit_result_df, pre_columns, after_columns, reverse=False):
    significance_results = []
    # Loop through each repository
    for _, row in commit_result_df.iterrows():
        repo_name = row['repository']
        pre_values = commit_result_df[commit_result_df['repository'] == repo_name][pre_columns].values.flatten()
        after_values = commit_result_df[commit_result_df['repository'] == repo_name][after_columns].values.flatten()

            # Use Cliffs Delta as the effect size for all 
        def cliffs_delta(pre, post):
            """Calculate Cliff's Delta effect size."""
            n1 = len(pre)
            n2 = len(post)
            if n1 == 0 or n2 == 0:
                return np.nan
            higher_pre = sum(x > y for x in pre for y in post)
            higher_post = sum(x < y for x in pre for y in post)
            # Change order so  that effect 
            return (higher_post - higher_pre) / (n1 * n2)

        cliffs_delta_value = cliffs_delta(pre_values, after_values)
        
        significance_results.append({
            'repository': repo_name,
            'test_used': "Cliff's Delta",
            'effect_size': cliffs_delta_value
        })
        
    # Convert significance results to a DataFrame
    significance_results_df = pd.DataFrame(significance_results)
    return significance_results_df

import numpy as np
import pandas as pd
from sklearn.utils import resample

def calculate_cliffs_delta_with_confidence(commit_result_df, pre_columns, after_columns, reverse=False, n_boot=1000, alpha=0.05):
    significance_results = []

    for _, row in commit_result_df.iterrows():
        repo_name = row['repository']
        pre_values = commit_result_df[commit_result_df['repository'] == repo_name][pre_columns].values.flatten()
        after_values = commit_result_df[commit_result_df['repository'] == repo_name][after_columns].values.flatten()

        if len(pre_values) == 0 or len(after_values) == 0:
            significance_results.append({
                'repository': repo_name,
                'test_used': "Cliff's Delta",
                'effect_size': np.nan,
                'ci_lower': np.nan,
                'ci_upper': np.nan
            })
            continue

        def cliffs_delta(pre, post):
            n1 = len(pre)
            n2 = len(post)
            higher_pre = sum(x > y for x in pre for y in post)
            higher_post = sum(x < y for x in pre for y in post)
            return (higher_post - higher_pre) / (n1 * n2)

        # Compute original delta
        delta = cliffs_delta(pre_values, after_values)

        # Bootstrap
        deltas = []
        for _ in range(n_boot):
            boot_pre = resample(pre_values)
            boot_post = resample(after_values)
            try:
                boot_delta = cliffs_delta(boot_pre, boot_post)
                deltas.append(boot_delta)
            except:
                continue

        if deltas:
            lower = np.percentile(deltas, 100 * alpha / 2)
            upper = np.percentile(deltas, 100 * (1 - alpha / 2))
        else:
            lower = upper = np.nan

        significance_results.append({
            'repository': repo_name,
            'test_used': "Cliff's Delta",
            'effect_size': delta,
            'ci_lower': lower,
            'ci_upper': upper
        })

    return pd.DataFrame(significance_results)


from scipy.stats import ttest_ind, mannwhitneyu
from math import sqrt, isnan

def use_normality_results_for_significance_independent(normality_results, commit_result_df, pre_columns, after_columns):
    significance_results = []
    
    # Loop through each repository
    for _, row in normality_results.iterrows():
        repo_name = row['repository']
        pre_values = commit_result_df[commit_result_df['repository'] == repo_name][pre_columns].values.flatten()
        after_values = commit_result_df[commit_result_df['repository'] == repo_name][after_columns].values.flatten()

        # Filter out NaNs independently (since samples are independent)
        pre_values = pre_values[~np.isnan(pre_values)]
        after_values = after_values[~np.isnan(after_values)]

        print(f"{repo_name}: mean(pre)={np.mean(pre_values):.2f}, mean(after)={np.mean(after_values):.2f}, len(pre)={len(pre_values)}, len(after)={len(after_values)}")

        if len(pre_values) == 0 or len(after_values) == 0:
            print(f"Skipping {repo_name} due to insufficient data.")
            continue

        # if row['pre_normal'] and row['after_normal']:
        #     # Independent t-test for normal data
        #     stat, p_value = ttest_ind(pre_values, after_values, equal_var=False)  # Welch's t-test for safety
        #     test_used = "t-test (independent, ES Cohens d)"
            
        #     nx = len(pre_values)
        #     ny = len(after_values)
        #     s1 = np.std(pre_values, ddof=1)
        #     s2 = np.std(after_values, ddof=1)
            
        #     # Pooled standard deviation
        #     s_pooled = sqrt(((nx - 1) * s1 ** 2 + (ny - 1) * s2 ** 2) / (nx + ny - 2))
            
        #     effect_size = (np.mean(after_values) - np.mean(pre_values)) / s_pooled if s_pooled > 0 else np.nan

        # else:
            # Mann-Whitney U test for non-normal data
        stat, p_value = mannwhitneyu(pre_values, after_values, alternative='two-sided', method='auto')
        
        test_used = "Mann-Whitney U (ES rank-biserial)"
        
        n1 = len(after_values)
        n2 = len(pre_values)
        U = stat
        rank_biserial = 1 - (2 * U) / (n1 * n2)
        
                # Approximate z from U
        # n = n1 + n2
        # mean_u = n1 * n2 / 2
        # std_u = np.sqrt(n1 * n2 * (n + 1) / 12)
        # z = (stat - mean_u) / std_u

        # r = z / np.sqrt(n)
        
        effect_size = rank_biserial

        # Append results
        significance_results.append({
            'repository': repo_name,
            'test_used': test_used,
            'statistic': stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'effect_size': effect_size
        })

    significance_results_df = pd.DataFrame(significance_results)
    return significance_results_df
