import requests
import logging
import pandas as pd
from google.cloud import bigquery

CONFIG = {
    "latitude": 13.08,
    "longitude": 80.27,
    "location_name": "Chennai",
    "forecast_days": 7,
    "timezone": "Asia/Kolkata",
    "bq_project": "rapid-pottery-497706-n0",
    "bq_dataset": "weather_pipeline",
    "bq_table": "forecasts",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def fetch_weather(config):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": config["latitude"],
        "longitude": config["longitude"],
        "daily": ["temperature_2m_max","temperature_2m_min","precipitation_sum","windspeed_10m_max"],
        "forecast_days": config["forecast_days"],
        "timezone": config["timezone"],
    }
    logger.info(f"Fetching weather for {config['location_name']}")
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.info("API call successful")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        raise

def transform(raw, location_name):
    logger.info("Transforming data")
    daily = raw.get("daily", {})
    if not daily:
        raise ValueError("No daily data found")
    df = pd.DataFrame(daily)
    df.rename(columns={"time": "date"}, inplace=True)
    df.fillna(0, inplace=True)
    df["temp_range_c"] = df["temperature_2m_max"] - df["temperature_2m_min"]
    df["is_rainy_day"] = df["precipitation_sum"] > 1.0
    df["location"] = location_name
    df["date"] = pd.to_datetime(df["date"])
    df["is_rainy_day"] = df["is_rainy_day"].astype(bool)
    logger.info(f"Transformed {len(df)} rows")
    return df

def load_to_bigquery(df, config):
    table_id = f"{config['bq_project']}.{config['bq_dataset']}.{config['bq_table']}"
    logger.info(f"Loading {len(df)} rows to {table_id}")
    client = bigquery.Client(project=config["bq_project"])
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    logger.info("Successfully loaded data")

if __name__ == "__main__":
    raw_data = fetch_weather(CONFIG)
    df = transform(raw_data, CONFIG["location_name"])
    print(df.to_string())
    load_to_bigquery(df, CONFIG)