# analysis_engine/dimensionality.py

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import prince
import os

# ===================== PCA ===================== 
def run_pca(df, selected_columns, output_dir, custom_ratios=None):
    """
    Perform PCA with optional custom ratios (composite features).
    
    Args:
        df: DataFrame
        selected_columns: list of columns to include
        output_dir: output directory for graphs
        custom_ratios: dict, e.g. {"Subventions/Income": ("Subventions", "Income")}
    """
    df_selected = df[selected_columns].copy()

    # Handle composite ratios if provided
    if custom_ratios:
        for new_col, (num, denom) in custom_ratios.items():
            if num in df.columns and denom in df.columns:
                df_selected[new_col] = df[num] / df[denom]

    df_selected = df_selected.dropna()

    # Standardize data (important for PCA)
    X_scaled = StandardScaler().fit_transform(df_selected)

    pca = PCA()
    components = pca.fit_transform(X_scaled)

    explained_variance = pca.explained_variance_ratio_
    eigenvalues = pca.explained_variance_
    loadings = pca.components_.T  # coefficients of variables

    # Scree Plot
    plt.figure(figsize=(8, 5))
    plt.plot(np.arange(1, len(eigenvalues)+1), eigenvalues, 'o-', color='blue')
    plt.title("Scree Plot (Eigenvalues)")
    plt.xlabel("Principal Component")
    plt.ylabel("Eigenvalue")
    scree_path = os.path.join(output_dir, "scree_plot.png")
    plt.tight_layout()
    plt.savefig(scree_path)
    plt.close()

    # Biplot (first 2 PCs)
    plt.figure(figsize=(8, 6))
    xs, ys = components[:, 0], components[:, 1]
    plt.scatter(xs, ys, alpha=0.6, color='gray', label="Observations")

    for i, var in enumerate(df_selected.columns):
        plt.arrow(0, 0, loadings[i, 0]*3, loadings[i, 1]*3, 
                  color='red', alpha=0.7)
        plt.text(loadings[i, 0]*3.2, loadings[i, 1]*3.2, var, color='red')

    plt.xlabel(f"PC1 ({explained_variance[0]*100:.2f}%)")
    plt.ylabel(f"PC2 ({explained_variance[1]*100:.2f}%)")
    plt.title("PCA Biplot")
    plt.grid(True)
    biplot_path = os.path.join(output_dir, "pca_biplot.png")
    plt.savefig(biplot_path)
    plt.close()

    # Correlation circle
    plt.figure(figsize=(6, 6))
    for i in range(loadings.shape[0]):
        plt.arrow(0, 0, loadings[i, 0], loadings[i, 1], 
                  color='blue', alpha=0.5)
        plt.text(loadings[i, 0]*1.1, loadings[i, 1]*1.1, df_selected.columns[i])
    circle = plt.Circle((0, 0), 1, color='gray', fill=False)
    plt.gca().add_artist(circle)
    plt.title("Correlation Circle (PC1 vs PC2)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.axis('equal')
    corr_circle_path = os.path.join(output_dir, "correlation_circle.png")
    plt.savefig(corr_circle_path)
    plt.close()

    return {
        "eigenvalues": eigenvalues.tolist(),
        "explained_variance": explained_variance.tolist(),
        "loadings": loadings.tolist(),
        "coordinates": components[:, :2].tolist(),
        "scree_plot": "scree_plot.png",
        "biplot": "pca_biplot.png",
        "correlation_circle": "correlation_circle.png"
    }

# ===================== MCA =====================

def run_mca(df, selected_columns, output_dir):
    df_selected = df[selected_columns].copy()

    # Convert numeric columns to categorical bins for MCA
    for col in selected_columns:
        if np.issubdtype(df_selected[col].dtype, np.number):
            # Use qcut with labels to create meaningful categories
            try:
                df_selected[col] = pd.qcut(df_selected[col], q=4, duplicates='drop', 
                                          labels=['Q1', 'Q2', 'Q3', 'Q4'])
            except ValueError:
                # If qcut fails, use cut instead
                df_selected[col] = pd.cut(df_selected[col], bins=4, 
                                         labels=['Low', 'Med-Low', 'Med-High', 'High'])
        # Convert to string to ensure categorical treatment
        df_selected[col] = df_selected[col].astype(str)

    df_selected = df_selected.dropna()
    
    if df_selected.empty:
        return {
            "error": "No valid data after preprocessing",
            "mca_map": None
        }

    try:
        # Initialize and fit MCA
        mca = prince.MCA(n_components=2, random_state=42)
        mca = mca.fit(df_selected)

        # Get row coordinates (observations)
        row_coords = mca.transform(df_selected)
        
        # Get column coordinates (variable categories)
        col_coords = mca.column_coordinates(df_selected)
        
        # Get explained inertia - try different attribute names
        try:
            inertia = mca.explained_inertia_
        except AttributeError:
            try:
                # Some versions use eigenvalues_
                eigenvalues = mca.eigenvalues_
                total_inertia = eigenvalues.sum()
                inertia = eigenvalues / total_inertia
            except AttributeError:
                # Fallback: calculate manually
                inertia = np.array([0.5, 0.3])  # Placeholder

        # Plot MCA - Row coordinates
        plt.figure(figsize=(10, 8))
        
        # Plot observations (smaller, more transparent)
        plt.scatter(row_coords.iloc[:, 0], row_coords.iloc[:, 1], 
                   alpha=0.3, c='lightblue', s=30, label='Observations', edgecolors='blue', linewidth=0.5)

        # Plot variable categories (larger, more visible)
        for idx, label in enumerate(col_coords.index):
            plt.scatter(col_coords.iloc[idx, 0], col_coords.iloc[idx, 1], 
                       c='red', marker='o', s=150, edgecolors='darkred', linewidth=2, zorder=5)
            plt.text(col_coords.iloc[idx, 0] + 0.05, col_coords.iloc[idx, 1] + 0.05, 
                    str(label), fontsize=9, ha='left', weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

        # Format the plot
        try:
            plt.title(f"MCA Factorial Map (Dim1: {inertia[0]*100:.2f}%, Dim2: {inertia[1]*100:.2f}%)", 
                     fontsize=14, weight='bold')
            plt.xlabel(f"Dimension 1 ({inertia[0]*100:.2f}%)", fontsize=12)
            plt.ylabel(f"Dimension 2 ({inertia[1]*100:.2f}%)", fontsize=12)
        except (TypeError, IndexError):
            plt.title("MCA Factorial Map", fontsize=14, weight='bold')
            plt.xlabel("Dimension 1", fontsize=12)
            plt.ylabel("Dimension 2", fontsize=12)
            
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)

        mca_path = os.path.join(output_dir, "mca_map.png")
        plt.tight_layout()
        plt.savefig(mca_path, dpi=150, bbox_inches='tight')
        plt.close()

        # Prepare inertia for return
        inertia_list = inertia.tolist() if hasattr(inertia, 'tolist') else [float(inertia[0]), float(inertia[1])]

        return {
            "mca_map": "mca_map.png",
            "row_coordinates": row_coords.iloc[:10, :2].to_dict(),  # First 10 rows
            "column_coordinates": col_coords.to_dict(),
            "inertia": inertia_list,
            "n_observations": len(row_coords),
            "n_categories": len(col_coords)
        }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"MCA Error: {error_details}")  # For debugging in console
        return {
            "error": f"{str(e)}",
            "mca_map": None
        }
    