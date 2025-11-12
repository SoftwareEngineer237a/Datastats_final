# analysis_engine/clustering.py
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import seaborn as sns

def run_kmeans(df, selected_columns, n_clusters, output_dir):
    if len(selected_columns) < 2:
        raise ValueError("Select at least two columns for clustering.")

    X = df[selected_columns].dropna()
    X_scaled = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_scaled)

    # Plotting
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X_scaled[:, 0], y=X_scaled[:, 1], hue=labels, palette='Set2', edgecolor='w', s=100)
    plt.title("KMeans Clustering")
    plt.xlabel(selected_columns[0])
    plt.ylabel(selected_columns[1])
    plt.grid(True)
    plt.tight_layout()

    filename = "kmeans_plot.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()

    return {'kmeans_plot': filename, 'labels': labels.tolist()}

def run_hac(df, selected_columns, output_dir, method='ward'):
    if len(selected_columns) < 2:
        raise ValueError("Select at least two columns for clustering.")

    X = df[selected_columns].dropna()
    X_scaled = StandardScaler().fit_transform(X)

    plt.figure(figsize=(10, 6))
    linked = linkage(X_scaled, method=method)
    dendrogram(linked,
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.tight_layout()

    filename = "hac_dendrogram.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()

    return {'hac_plot': filename}
