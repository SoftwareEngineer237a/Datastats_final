import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import numpy as np

def run_ml_model(df, x_col, y_col, model_type='random_forest', task_type='classification', n_neighbors=3, output_dir=None, filename_prefix=None):
    df = df[[x_col, y_col]].dropna()

    X = df[[x_col]].values
    y = df[y_col].values

    result = {}

    # Encode y if classification and not numeric
    if task_type == 'classification' and not np.issubdtype(y.dtype, np.number):
        le = LabelEncoder()
        y = le.fit_transform(y)
        label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        result['label_mapping'] = label_mapping

    # Select model
    if model_type == 'random_forest':
        model = RandomForestClassifier() if task_type == 'classification' else RandomForestRegressor()
    elif model_type == 'knn':
        model = KNeighborsClassifier(n_neighbors=n_neighbors) if task_type == 'classification' else KNeighborsRegressor(n_neighbors=n_neighbors)
    else:
        raise ValueError("Invalid model type")

    model.fit(X, y)
    y_pred = model.predict(X)

    # Metrics
    if task_type == 'classification':
        accuracy = accuracy_score(y, y_pred)
        result['metric'] = f'Accuracy: {accuracy:.4f}'
    else:
        r2 = r2_score(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        result['metric'] = f'R²: {r2:.4f}, MSE: {mse:.4f}'

    result['predictions'] = list(zip(X.flatten(), y_pred))

    # ✅ Save results to CSV
    if output_dir and filename_prefix:
        os.makedirs(output_dir, exist_ok=True)
        out_df = pd.DataFrame(result['predictions'], columns=[x_col, f"Predicted_{y_col}"])
        csv_file = f"{filename_prefix}_ml_results.csv"
        out_df.to_csv(os.path.join(output_dir, csv_file), index=False)
        result['csv'] = csv_file

    return result
