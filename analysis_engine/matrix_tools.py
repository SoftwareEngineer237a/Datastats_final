# analysis_engine/matrix_tools.py

import os
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # for server-side rendering
import matplotlib.pyplot as plt
import seaborn as sns


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def _save_fig(output_dir, filename_prefix):
    _ensure_dir(output_dir)
    filename = f"{filename_prefix}.png"
    outpath = os.path.join(output_dir, filename)
    plt.tight_layout()
    plt.savefig(outpath, bbox_inches="tight", dpi=140)
    plt.close()
    return filename


def _save_csv(output_dir, filename_prefix, df):
    _ensure_dir(output_dir)
    filename = f"{filename_prefix}.csv"
    outpath = os.path.join(output_dir, filename)
    df.to_csv(outpath, index=True, encoding="utf-8")
    return filename


def compute_correlation(df, columns, method="pearson", handle_na="pairwise", output_dir="", name_prefix=""):
    """
    method: 'pearson' | 'spearman' | 'kendall'
    handle_na: 'pairwise' (default) or 'complete' (drop rows with any NA in selected cols)
    """
    data = df[columns].copy()

    if handle_na == "complete":
        data = data.dropna()
    else:
        # pairwise handled by pandas corr itself
        pass

    # Compute correlation matrix
    corr = data.corr(method=method)

    # Heatmap
    plt.figure(figsize=(min(1.1*len(columns), 14), min(1.1*len(columns), 14)))
    mask = np.triu(np.ones_like(corr, dtype=bool))  # show lower triangle
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
                square=True, annot=len(columns) <= 15, fmt=".2f",
                linewidths=.5, cbar_kws={"shrink": .8})
    plt.title(f"Correlation Matrix ({method.title()})")
    plot_file = _save_fig(output_dir, f"{name_prefix}_corr_{method}")

    # Save CSV
    csv_file = _save_csv(output_dir, f"{name_prefix}_corr_{method}", corr)

    # Top pairs (absolute value)
    pairs = []
    for i in range(len(columns)):
        for j in range(i+1, len(columns)):
            pairs.append((columns[i], columns[j], float(corr.iloc[i, j])))
    # sort by absolute correlation desc
    pairs_sorted = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)
    top_pairs = pairs_sorted[:10]

    return {
        "matrix": corr,
        "matrix_html": corr.to_html(classes="table table-striped table-sm", float_format=lambda x: f"{x:.4f}"),
        "plot": plot_file,
        "csv": csv_file,
        "top_pairs": top_pairs,
        "method": method,
        "na_policy": handle_na
    }


def compute_covariance(df, columns, ddof=1, handle_na="complete", output_dir="", name_prefix=""):
    """
    ddof: 0 for population, 1 for sample (default)
    handle_na: 'complete' (drop rows with any NA) or 'pairwise' (cov with pairwise NA handling)
    Note: pandas cov already uses pairwise complete observations by default.
    """
    data = df[columns].copy()

    if handle_na == "complete":
        data = data.dropna()

    cov = data.cov(ddof=ddof)

    # Heatmap (no diverging cmap; covariance not bounded)
    plt.figure(figsize=(min(1.1*len(columns), 14), min(1.1*len(columns), 14)))
    sns.heatmap(cov, cmap="YlGnBu", annot=len(columns) <= 15, fmt=".2f",
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title(f"Covariance Matrix (ddof={ddof})")
    plot_file = _save_fig(output_dir, f"{name_prefix}_cov_ddof{ddof}")

    # Save CSV
    csv_file = _save_csv(output_dir, f"{name_prefix}_cov_ddof{ddof}", cov)

    return {
        "matrix": cov,
        "matrix_html": cov.to_html(classes="table table-striped table-sm", float_format=lambda x: f"{x:.4f}"),
        "plot": plot_file,
        "csv": csv_file,
        "ddof": ddof,
        "na_policy": handle_na
    }
