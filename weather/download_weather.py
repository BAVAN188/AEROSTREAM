import os
import pandas as pd
import requests

# NOAA ISD-Lite base URL
BASE_URL = "https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/2024/"

# Output folder
OUTPUT_DIR = "data/raw/weather/isd"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading airport-weather mapping...")

mapping = pd.read_csv("data/processed/airport_weather_mapping.csv")

downloaded = 0
failed = 0

for _, row in mapping.iterrows():

    try:
        usaf = str(int(row["USAF"])).zfill(6)
        wban = str(int(row["WBAN"])).zfill(5)

        filename = f"{usaf}-{wban}-2024.gz"
        url = BASE_URL + filename

        output_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(output_path):
            print(f"✓ Exists: {filename}")
            continue

        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded: {filename}")
            downloaded += 1

        else:
            print(f"Missing: {filename}")
            failed += 1

    except Exception as e:
        print(f"Error: {e}")
        failed += 1

print("\n========================")
print(f"Downloaded : {downloaded}")
print(f"Failed     : {failed}")
print("========================")