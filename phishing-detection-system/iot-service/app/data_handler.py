# IoT Data Handler
import pandas as pd
from datetime import datetime

def process_iot_data(raw_data):
    """Process raw IoT data for ML features"""
    df = pd.DataFrame([raw_data])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df

def store_data(df, path='data/iot_data.parquet'):
    df.to_parquet(path)
    print(f"Data stored to {path}")

