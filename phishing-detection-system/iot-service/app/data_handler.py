import pandas as pd
from datetime import datetime

def process_iot_data(raw_data):
    """Process raw IoT data for ML features"""

    # Convert to DataFrame
    df = pd.DataFrame([raw_data])

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Rename for consistency (IMPORTANT)
    if 'Device' in df.columns:
        df.rename(columns={'Device': 'device_id'}, inplace=True)

    # -------- Feature Engineering -------- #

    # Temperature anomaly
    df['temp_anomaly'] = df['temperature'].apply(
        lambda x: 1 if x > 32 or x < 18 else 0
    )

    # CPU anomaly
    df['cpu_anomaly'] = df['cpu_usage'].apply(
        lambda x: 1 if x > 85 else 0
    )

    # Network anomaly
    df['network_anomaly'] = df['packet_rate'].apply(
        lambda x: 1 if x > 300 else 0
    )

    # Login anomaly
    df['login_anomaly'] = df['failed_logins'].apply(
        lambda x: 1 if x > 10 else 0
    )

    # Battery health
    df['low_battery'] = df['battery'].apply(
        lambda x: 1 if x < 25 else 0
    )

    # Combined anomaly score
    df['anomaly_score'] = (
        df['temp_anomaly'] +
        df['cpu_anomaly'] +
        df['network_anomaly'] +
        df['login_anomaly']
    )

    # Final label (optional ML target)
    df['is_suspicious'] = df['anomaly_score'].apply(
        lambda x: 1 if x >= 2 else 0
    )

    return df


def store_data(df, path='data/iot_data.parquet'):
    """Store processed data"""

    # Ensure folder exists
    import os
    os.makedirs('data', exist_ok=True)

    df.to_parquet(path)
    print(f"Data stored to {path}")