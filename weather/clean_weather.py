

import pandas as pd
import numpy as np

INPUT_FILE = "data/processed/weather_2024.csv"
OUTPUT_FILE = "data/processed/weather_final.csv"

print("Loading weather dataset...")

weather = pd.read_csv(INPUT_FILE)

# Keep only useful columns
weather = weather[
    [
        "airport_code",
        "DATE",
        "TEMP",
        "MAX",
        "MIN",
        "WDSP",
        "PRCP",
        "SNDP",
    ]
]

# Replace NOAA missing values
weather.replace({
    9999.9: np.nan,
    999.9: np.nan,
    99.99: np.nan,
}, inplace=True)

# Convert date
weather["DATE"] = pd.to_datetime(weather["DATE"])

# Rename columns
weather.rename(columns={
    "DATE": "date",
    "TEMP": "avg_temp",
    "MAX": "max_temp",
    "MIN": "min_temp",
    "WDSP": "wind_speed",
    "PRCP": "precipitation",
    "SNDP": "snow_depth"
}, inplace=True)

weather.to_csv(OUTPUT_FILE, index=False)

print("\n======================")
print(f"Rows     : {len(weather)}")
print(f"Airports : {weather['airport_code'].nunique()}")
print(weather.head())
print("======================")

print("\n✅ weather_final.csv created!")