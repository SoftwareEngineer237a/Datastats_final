# app/utils.py

import os
from app.models import Dataset

UPLOAD_FOLDER = 'uploads'

def load_dataset_by_id(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    if dataset:
        filepath = os.path.join(UPLOAD_FOLDER, dataset.filename)
        return filepath if os.path.exists(filepath) else None
    return None

def save_cleaned_dataframe(df, original_path):
    df.to_csv(original_path, index=False)
