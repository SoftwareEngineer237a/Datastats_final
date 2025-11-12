from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score
import numpy as np
import pandas as pd
import os

def run_regression(df, x_col, y_cols, model_type='linear', degree=2, output_dir="static/results", prefix="regression"):
    try:
        if isinstance(y_cols, str):
            y_cols = [y_cols]

        filtered_df = df[[x_col] + y_cols].dropna()
        X = filtered_df[[x_col]].values
        Y = filtered_df[y_cols].values

        model = None
        result = {}

        # ✅ Logistic regression
        if model_type == 'logistic':
            if len(y_cols) > 1:
                raise ValueError("Logistic Regression supports only one dependent variable.")

            y = filtered_df[y_cols[0]].values
            y_unique = np.unique(y)

            if len(y_unique) != 2:
                raise ValueError("Logistic Regression requires binary target values (0/1).")

            if set(y_unique) != {0, 1}:
                le = LabelEncoder()
                y = le.fit_transform(y)

            model = LogisticRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            y_proba = model.predict_proba(X)[:, 1]
            accuracy = accuracy_score(y, y_pred)

            predictions_df = pd.DataFrame({
                x_col: X.flatten(),
                "Predicted": y_pred,
                "Probability": y_proba
            })

            result['metric'] = f"Accuracy: {accuracy:.4f}"

        else:
            # ✅ Other regression models
            if model_type == 'linear':
                model = LinearRegression()
            elif model_type == 'polynomial':
                model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
            elif model_type == 'ridge':
                model = Ridge()
            elif model_type == 'lasso':
                model = Lasso()
            elif model_type == 'multiple_linear':
                model = LinearRegression()
            else:
                raise ValueError("Invalid regression model type")

            model.fit(X, Y)
            Y_pred = model.predict(X)

            metrics = []
            for i, col in enumerate(y_cols):
                r2 = r2_score(Y[:, i], Y_pred[:, i])
                mse = mean_squared_error(Y[:, i], Y_pred[:, i])
                metrics.append(f"{col} → R²: {r2:.4f}, MSE: {mse:.4f}")

            result['metric'] = " | ".join(metrics)

            # ✅ Build prediction table w/ column names
            predictions_df = pd.DataFrame({x_col: X.flatten()})
            for i, col in enumerate(y_cols):
                predictions_df[f"Predicted {col}"] = Y_pred[:, i]

        # ✅ Save CSV
        os.makedirs(output_dir, exist_ok=True)
        csv_file = f"{prefix}_{model_type}.csv"
        predictions_df.to_csv(os.path.join(output_dir, csv_file), index=False)

        result["csv"] = csv_file
        result["y_columns"] = [f"Predicted {col}" for col in y_cols]
        result["predictions"] = predictions_df.values.tolist()

        return result

    except Exception as e:
        return {'metric': f'Error: {str(e)}', 'predictions': [], 'csv': None}
