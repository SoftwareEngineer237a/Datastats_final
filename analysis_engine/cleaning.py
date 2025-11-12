import pandas as pd
from sklearn.preprocessing import StandardScaler

def clean_and_transform_data(df, form_data):
    # 🔹 Handle Missing Values
    strategy = form_data.get('missing_strategy')
    if strategy == 'drop':
        df = df.dropna()
    elif strategy == 'fill_mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif strategy == 'fill_median':
        df = df.fillna(df.median(numeric_only=True))
    elif strategy == 'fill_zero':
        df = df.fillna(0)

    # 🔹 Rename Columns
    for col in df.columns:
        new_name = form_data.get(f'rename_{col}')
        if new_name and new_name.strip() != '':
            df = df.rename(columns={col: new_name})

    # 🔹 Filter
    filter_col = form_data.get('filter_column')
    filter_val = form_data.get('filter_value')
    if filter_col and filter_val:
        df = df[df[filter_col] == filter_val]

    # 🔹 Sort
    sort_col = form_data.get('sort_column')
    sort_order = form_data.get('sort_order')
    if sort_col:
        df = df.sort_values(by=sort_col, ascending=(sort_order == 'asc'))

    # 🔹 Normalize/Standardize
    norm_cols = form_data.get('normalize_columns')
    if norm_cols:
        cols = [c.strip() for c in norm_cols.split(',') if c.strip() in df.columns]
        scaler = StandardScaler()
        df[cols] = scaler.fit_transform(df[cols])

    # 🔹 Group By & Aggregate
    group_col = form_data.get('group_by')
    agg_col = form_data.get('agg_column')
    agg_func = form_data.get('agg_func')
    if group_col and agg_col and agg_func:
        if group_col in df.columns and agg_col in df.columns:
            df = df.groupby(group_col)[agg_col].agg(agg_func).reset_index()

    return df
