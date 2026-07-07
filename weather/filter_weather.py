import pandas as pd

mapping = pd.read_csv("data/processed/airport_weather_mapping.csv")

print(mapping["USAF"].head(10))

weather = pd.read_csv(
    "data/raw/weather/2024.csv",
    header=None,
    names=[
        "station_id",
        "date",
        "element",
        "value",
        "mflag",
        "qflag",
        "sflag",
        "obs_time"
    ],
    nrows=10
)

print("\nWeather station IDs:")
print(weather["station_id"])