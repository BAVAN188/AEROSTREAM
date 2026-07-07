import pandas as pd

# ==========================================
# Configuration
# ==========================================

WEATHER_PATH = "data/raw/weather/2024.csv"

# Weather elements we care about
REQUIRED_ELEMENTS = [
    "TMAX",   # Maximum Temperature
    "TMIN",   # Minimum Temperature
    "PRCP",   # Precipitation
    "SNOW",   # Snowfall
    "AWND"    # Average Wind Speed
]


# ==========================================
# Load Weather Dataset
# ==========================================

def load_weather():

    columns = [
        "station_id",
        "date",
        "element",
        "value",
        "mflag",
        "qflag",
        "sflag",
        "obs_time"
    ]

    print("Loading weather dataset...")

    weather = pd.read_csv(
        WEATHER_PATH,
        names=columns,
        header=None
    )

    print(f"\nLoaded {len(weather):,} rows.")

    return weather


# ==========================================
# Filter Required Weather Elements
# ==========================================

def filter_weather(weather):

    print("\nFiltering required weather elements...")

    weather = weather[
        weather["element"].isin(REQUIRED_ELEMENTS)
    ]

    print(f"Remaining rows: {len(weather):,}")

    print("\nWeather Element Counts:")
    print(weather["element"].value_counts())

    print("\nSample Data:")
    print(weather.head())

    return weather


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    weather = load_weather()

    weather = filter_weather(weather)