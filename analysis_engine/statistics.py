import pandas as pd
from scipy.stats import skew, kurtosis
from scipy import stats
import numpy as np
import os

def compute_descriptive_stats(df, output_dir="static/results", filename_prefix="descriptive_stats"):
    numeric_df = df.select_dtypes(include='number').copy()

    stats = pd.DataFrame()
    stats["Mean"] = numeric_df.mean()
    stats["Median"] = numeric_df.median()
    stats["Mode"] = numeric_df.mode().iloc[0]
    stats["Standard Deviation"] = numeric_df.std()
    stats["Variance"] = numeric_df.var()
    stats["Skewness"] = numeric_df.apply(skew)
    stats["Kurtosis"] = numeric_df.apply(kurtosis)

    stats = stats.round(3)

    # ✅ Ensure folder exists
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Save to CSV
    csv_file = f"{filename_prefix}.csv"
    stats.to_csv(os.path.join(output_dir, csv_file), index=True)

    return stats, csv_file

def calculate_confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)  # standard error of the mean
    margin = sem * stats.t.ppf((1 + confidence) / 2., n-1)
    return {
        "mean": mean,
        "margin_of_error": margin,
        "confidence_level": confidence,
        "ci_lower": mean - margin,
        "ci_upper": mean + margin
    }

def one_sample_ttest(data, popmean):
    t_stat, p_value = stats.ttest_1samp(data, popmean)
    return {
        "t_statistic": t_stat,
        "p_value": p_value,
        "reject_null": p_value < 0.05
    }
