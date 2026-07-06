import pandas as pd
from pathlib import Path

# =====================================================
# CONFIGURATION
# =====================================================

# None = Process all airports
# "JFK" = Only JFK
# "LAX" = Only LAX
# etc.

AIRPORT_FILTER = None


def run():

    # =====================================================
    # STEP 1: LOAD ALL CSV FILES
    # =====================================================

    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "data" / "raw"
    cleaned_output_path = project_root / "data" / "processed" / "clean_flights.csv"

    csv_files = sorted(raw_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("❌ No CSV files found inside data/raw")

    all_months = []

    for file in csv_files:
        df_month = pd.read_csv(file)
        print(f"Loaded {file.name}: {df_month.shape}")
        all_months.append(df_month)

    raw = pd.concat(all_months, ignore_index=True)

    print(f"\nCombined Dataset Shape: {raw.shape}")

    # =====================================================
    # STEP 2: FILTER AIRPORT (OPTIONAL)
    # =====================================================

    if AIRPORT_FILTER:
        filtered = raw[raw["ORIGIN"] == AIRPORT_FILTER]
        print(f"{AIRPORT_FILTER} flights: {filtered.shape}")
    else:
        filtered = raw
        print(f"Processing ALL airports: {filtered.shape}")

    # =====================================================
    # STEP 3: KEEP REQUIRED COLUMNS
    # =====================================================

    columns_we_need = [
        "FL_DATE",
        "OP_UNIQUE_CARRIER",
        "ORIGIN",
        "DEST",
        "DEST_CITY_NAME",
        "CRS_DEP_TIME",
        "DEP_TIME",
        "DEP_DELAY",
        "ARR_DELAY",
        "CANCELLED",
        "CANCELLATION_CODE",
        "CARRIER_DELAY",
        "WEATHER_DELAY",
        "NAS_DELAY",
        "SECURITY_DELAY",
        "LATE_AIRCRAFT_DELAY",
        "DISTANCE",
    ]

    df = filtered[columns_we_need].copy()

    print(f"After column selection: {df.shape}")

    # =====================================================
    # STEP 4: CLEAN DATA
    # =====================================================

    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"], format="mixed")

    delay_columns = [
        "CARRIER_DELAY",
        "WEATHER_DELAY",
        "NAS_DELAY",
        "SECURITY_DELAY",
        "LATE_AIRCRAFT_DELAY",
    ]

    for col in delay_columns:
        df[col] = df[col].fillna(0)

    df["CANCELLATION_CODE"] = df["CANCELLATION_CODE"].fillna("N")
    df["DEP_DELAY"] = df["DEP_DELAY"].fillna(0)
    df["ARR_DELAY"] = df["ARR_DELAY"].fillna(0)

    print("\nMissing values after cleaning:")

    print(df.isnull().sum())

    # =====================================================
    # STEP 5: SAVE CLEAN DATA
    # =====================================================

    cleaned_output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(cleaned_output_path, index=False)

    print(f"\n✅ Clean data saved to: {cleaned_output_path}")
    print(f"Final Shape: {df.shape}")


if __name__ == "__main__":
    run()