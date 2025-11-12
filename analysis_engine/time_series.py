# analysis_engine/time_series.py

import os
import io
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA


# ------------------------
# Utilities
# ------------------------
def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def _save_fig(output_dir, filename_prefix):
    _ensure_dir(output_dir)
    filename = f"{filename_prefix}.png"
    outpath = os.path.join(output_dir, filename)
    plt.tight_layout()
    plt.savefig(outpath, bbox_inches="tight")
    plt.close()
    return filename

def prepare_series(df, date_col, value_col, freq=None, agg="mean"):
    """
    - Parses date column
    - Sorts by date
    - Groups duplicates (by agg)
    - Optional resampling to given freq ('D','M','Q','Y')
    Returns a clean pandas Series with DateTimeIndex
    """
    s = df[[date_col, value_col]].copy()
    # Parse dates
    s[date_col] = pd.to_datetime(s[date_col], errors="coerce")
    s = s.dropna(subset=[date_col, value_col])
    s = s.sort_values(by=date_col)
    # Aggregate duplicates on same date
    s = s.groupby(date_col)[value_col].agg(agg)

    if freq:
        # resample to target frequency with chosen aggregation
        if agg == "sum":
            s = s.resample(freq).sum()
        elif agg == "max":
            s = s.resample(freq).max()
        elif agg == "min":
            s = s.resample(freq).min()
        else:
            s = s.resample(freq).mean()

    # drop missing after resample
    s = s.dropna()
    return s


# ------------------------
# Moving Average
# ------------------------
def moving_average(series: pd.Series, window: int, output_dir: str, name_prefix: str):
    if window < 1:
        raise ValueError("Window must be >= 1.")
    if len(series) < window:
        raise ValueError(f"Not enough data points for a window of {window}.")

    ma = series.rolling(window=window, min_periods=1).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(series.index, series.values, label="Original")
    plt.plot(ma.index, ma.values, label=f"Moving Average (window={window})")
    plt.title("Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    filename = _save_fig(output_dir, f"{name_prefix}_moving_avg")

    return {
        "plot": filename,
        "window": window,
        "last_ma": float(ma.iloc[-1]) if len(ma) > 0 else None
    }


# ------------------------
# Exponential Smoothing (Holt-Winters)
# ------------------------
def run_exponential_smoothing(series: pd.Series, trend: str = "add", seasonal: str = None,
                              seasonal_periods: int = None, output_dir: str = "", name_prefix: str = ""):
    """
    trend: None | 'add' | 'mul'
    seasonal: None | 'add' | 'mul'
    """
    if seasonal and not seasonal_periods:
        raise ValueError("seasonal_periods is required when seasonal component is specified.")

    model = ExponentialSmoothing(
        series,
        trend=trend if trend != "none" else None,
        seasonal=seasonal if seasonal != "none" else None,
        seasonal_periods=seasonal_periods
    )
    fit = model.fit(optimized=True)
    fitted = fit.fittedvalues

    plt.figure(figsize=(10, 5))
    plt.plot(series.index, series.values, label="Original")
    plt.plot(fitted.index, fitted.values, label="Fitted (Exponential Smoothing)")
    plt.title("Exponential Smoothing (Holt-Winters)")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    filename = _save_fig(output_dir, f"{name_prefix}_exp_smoothing")

    aic = getattr(fit, "aic", None)
    return {
        "plot": filename,
        "aic": float(aic) if aic is not None else None
    }


# ------------------------
# ARIMA
# ------------------------
def run_arima(series: pd.Series, order=(1, 1, 1), forecast_steps: int = 12,
              output_dir: str = "", name_prefix: str = ""):
    if len(series) < (sum(order) + 3):
        raise ValueError("Not enough data points for the selected ARIMA order.")

    model = ARIMA(series, order=order)
    fit = model.fit()
    forecast = fit.get_forecast(steps=forecast_steps)
    pred = forecast.predicted_mean
    conf_int = forecast.conf_int()

    plt.figure(figsize=(10, 5))
    plt.plot(series.index, series.values, label="Observed")
    plt.plot(pred.index, pred.values, label=f"Forecast ({forecast_steps} steps)")
    # Confidence interval shading
    plt.fill_between(pred.index,
                     conf_int.iloc[:, 0],
                     conf_int.iloc[:, 1],
                     alpha=0.2, label="95% CI")
    plt.title(f"ARIMA{order} Forecast")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    filename = _save_fig(output_dir, f"{name_prefix}_arima")

    return {
        "plot": filename,
        "aic": float(fit.aic),
        "order": list(order),
        "forecast_steps": forecast_steps
    }


# ------------------------
# Seasonal Decomposition
# ------------------------
def run_seasonal_decomposition(series: pd.Series, model: str = "additive", period: int = None,
                               output_dir: str = "", name_prefix: str = ""):
    if period is None or period <= 1:
        raise ValueError("A valid seasonal period (>1) is required for decomposition.")

    result = seasonal_decompose(series, model=model, period=period)

    # Plot composite figure
    fig = result.plot()
    fig.set_size_inches(10, 7)
    filename = _save_fig(output_dir, f"{name_prefix}_decomposition")

    explained = {
        "model": model,
        "period": period
    }
    return {
        "plot": filename,
        "meta": explained
    }


# ------------------------
# Trend Analysis (simple linear trend using polyfit)
# ------------------------
def run_trend_analysis(series: pd.Series, output_dir: str = "", name_prefix: str = ""):
    # Convert the datetime index to an ordinal float for regression
    x = series.index.map(pd.Timestamp.toordinal).astype(float).values
    y = series.values.astype(float)

    # Fit linear trend y = a*x + b
    a, b = np.polyfit(x, y, deg=1)
    y_trend = a * x + b

    plt.figure(figsize=(10, 5))
    plt.plot(series.index, series.values, label="Original")
    plt.plot(series.index, y_trend, label="Linear Trend", linewidth=2)
    plt.title("Trend Analysis (Linear)")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    filename = _save_fig(output_dir, f"{name_prefix}_trend")

    slope = float(a)
    direction = "increasing" if slope > 0 else ("decreasing" if slope < 0 else "flat")
    return {
        "plot": filename,
        "slope": slope,
        "direction": direction
    }
