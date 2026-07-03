import pandas as pd
from pathlib import Path


def run():

    # =====================
    # STEP 1: LOAD ALL 4 MONTHS
    # =====================

    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "data" / "raw"
    cleaned_output_path = project_root / "data" / "processed" / "jfk_clean.csv"

    files = [
        "T_ONTIME_REPORTING.csv",
        "T_ONTIME_REPORTING FEB.csv",
        "T_ONTIME_REPORTING MARCH.csv",
        "T_ONTIME_REPORTING APRIL.csv",
    ]

    all_months = []

    for file in files:
        path = raw_dir / file
        df_month = pd.read_csv(path)
        print(f"Loaded {file}: {df_month.shape}")
        all_months.append(df_month)

    raw = pd.concat(all_months, ignore_index=True)
    print("\nAll months combined:", raw.shape)

    # =====================
    # STEP 2: FILTER TO JFK
    # =====================

    jfk = raw[raw["ORIGIN"] == "JFK"]
    print("JFK flights:", jfk.shape)

    # =====================
    # STEP 3: KEEP USEFUL COLUMNS
    # =====================

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

    df = jfk[columns_we_need].copy()
    print("After column selection:", df.shape)

    # =====================
    # STEP 4: CLEAN DATA
    # =====================

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

    # =====================
    # STEP 5: SAVE CLEAN DATA
    # =====================

    cleaned_output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cleaned_output_path, index=False)

    print("\n✅ Clean data saved! Shape:", df.shape)


if __name__ == "__main__":
    run()