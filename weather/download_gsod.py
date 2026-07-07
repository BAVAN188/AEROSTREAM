import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# -----------------------------
# Configuration
# -----------------------------
BASE_URL = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/"
OUTPUT_DIR = "data/raw/weather/gsod"
MAPPING_FILE = "data/processed/airport_weather_mapping.csv"

MAX_WORKERS = 10
TIMEOUT = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading airport-weather mapping...")

mapping = pd.read_csv(MAPPING_FILE)

# Remove rows with missing station IDs
mapping = mapping.dropna(subset=["USAF", "WBAN"])

# Remove duplicate weather stations
mapping = mapping.drop_duplicates(subset=["USAF", "WBAN"])

print(f"Stations to download: {len(mapping)}")

# Reuse HTTP connections
session = requests.Session()


def download_station(row):
    usaf = str(int(row["USAF"])).zfill(6)
    wban = str(int(row["WBAN"])).zfill(5)

    filename = f"{usaf}{wban}.csv"
    url = BASE_URL + filename

    output_path = os.path.join(OUTPUT_DIR, filename)

    # Already downloaded
    if os.path.exists(output_path):
        return ("exists", filename)

    try:
        response = session.get(url, timeout=TIMEOUT)

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)

            return ("downloaded", filename)

        elif response.status_code == 404:
            return ("missing", filename)

        else:
            return ("error", filename)

    except Exception:
        return ("error", filename)


downloaded = 0
exists = 0
missing = 0
errors = 0

print("\nStarting downloads...\n")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = [
        executor.submit(download_station, row)
        for _, row in mapping.iterrows()
    ]

    for future in as_completed(futures):

        status, filename = future.result()

        if status == "downloaded":
            downloaded += 1
            print(f"✅ {filename}")

        elif status == "exists":
            exists += 1

        elif status == "missing":
            missing += 1
            print(f"❌ {filename}")

        else:
            errors += 1
            print(f"⚠️ {filename}")

print("\n==============================")
print(f"Downloaded : {downloaded}")
print(f"Already    : {exists}")
print(f"Missing    : {missing}")
print(f"Errors     : {errors}")
print("==============================")