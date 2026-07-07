import os
import pandas as pd

GSOD_FOLDER = "data/raw/weather/gsod"
MAPPING_FILE = "data/processed/airport_weather_mapping.csv"
OUTPUT_FILE = "data/processed/weather_2024.csv"

print("Loading airport mapping...")

mapping = pd.read_csv(MAPPING_FILE)

# Create station ID
mapping["station_id"] = (
    mapping["USAF"].fillna(0).astype(int).astype(str).str.zfill(6)
    +
    mapping["WBAN"].fillna(0).astype(int).astype(str).str.zfill(5)
)

all_weather = []

files = [f for f in os.listdir(GSOD_FOLDER) if f.endswith(".csv")]

print(f"Found {len(files)} weather files")

for file in files:

    station_id = file.replace(".csv", "")

    try:
        df = pd.read_csv(os.path.join(GSOD_FOLDER, file))

        airport = mapping.loc[
            mapping["station_id"] == station_id,
            "airport_code"
        ]

        if len(airport) == 0:
            continue

        df["airport_code"] = airport.iloc[0]

        all_weather.append(df)

    except Exception as e:
        print(file, e)

print("\nMerging...")

weather = pd.concat(all_weather, ignore_index=True)

weather.to_csv(OUTPUT_FILE, index=False)

print("\n==========================")
print("Rows:", len(weather))
print("Airports:", weather["airport_code"].nunique())
print("==========================")

print("\nSample:")
print(weather.head())

print("\n✅ weather_2024.csv created!")
