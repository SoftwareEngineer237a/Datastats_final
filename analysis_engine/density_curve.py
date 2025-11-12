# analysis_engine/density_curve.py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io, base64, numpy as np
from datetime import datetime
from app import db
from app.models import Graph


def run_density_curve(df, column, color, dataset_id, user_id):
    """
    Generates a density curve for a numeric column and saves it to DB.
    """
    # Ensure column exists
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset.")

    data = df[column].dropna()

    if len(data) < 2:
        raise ValueError(f"Not enough valid data in column '{column}'.")

    # Compute stats
    mean_val = data.mean()
    median_val = data.median()
    std_val = data.std()
    n = len(data)

    # Create figure
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data, fill=True, color=color, alpha=0.6, linewidth=2)
    plt.title(f"Courbe de densité - {column}", fontsize=16, fontweight='bold')
    plt.xlabel(column)
    plt.ylabel("Densité")

    # Mean & median lines
    plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f"Moyenne: {mean_val:.2f}")
    plt.axvline(median_val, color='blue', linestyle='--', linewidth=2, label=f"Médiane: {median_val:.2f}")
    plt.legend()

    # Stats box
    stats_text = (
        f"Moyenne: {mean_val:.2f}\n"
        f"Médiane: {median_val:.2f}\n"
        f"Écart-type: {std_val:.2f}\n"
        f"N: {n}"
    )
    plt.text(
        0.02, 0.98, stats_text,
        transform=plt.gca().transAxes,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    )

    plt.tight_layout()

    # Save figure to memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    buffer.seek(0)

    # Encode to Base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Save to DB
    new_graph = Graph(
        name=f"Density Curve - {column}",
        graph_type="Density Curve",
        dataset_id=dataset_id,
        analysis_type="density_curve",
        file_path=img_base64,   # store encoded image
        created_by=user_id,
        created_at=datetime.utcnow()
    )
    db.session.add(new_graph)
    db.session.commit()

    return {
        "column": column,
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "std": round(std_val, 2),
        "n": n,
        "image_base64": img_base64
    }
