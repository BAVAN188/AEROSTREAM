import pandas as pd

# -----------------------------
# Load airport codes
# -----------------------------
airports = pd.read_csv(
    "data/raw/weather/airport_codes.csv",
    header=None,
    names=["airport_code"]
)

airports["icao"] = "K" + airports["airport_code"]

# -----------------------------
# Load NOAA station metadata
# -----------------------------
stations = pd.read_csv("data/raw/weather/isd-history.csv")
stations = stations[stations["USAF"] != 999999]
stations = stations[stations["USAF"] != "999999"]

stations = stations[stations["ICAO"].notna()]

stations = stations[
    ["ICAO", "USAF", "WBAN", "STATION NAME", "LAT", "LON"]
]

# -----------------------------
# Merge airports with stations
# -----------------------------
mapping = airports.merge(
    stations,
    left_on="icao",
    right_on="ICAO",
    how="left"
)
# Keep only one weather station per airport
mapping = mapping.sort_values("USAF")
mapping = mapping.drop_duplicates(
    subset="airport_code",
    keep="first"
)

print("\n===== SAMPLE MAPPING =====")
print(mapping.head(20))

print(f"\nTotal Airports: {len(mapping)}")
print(f"Matched Airports: {mapping['USAF'].notna().sum()}")
print(f"Unmatched Airports: {mapping['USAF'].isna().sum()}")

# Save mapping
mapping.to_csv(
    "data/processed/airport_weather_mapping.csv",
    index=False
)

print("\n✅ airport_weather_mapping.csv created!")