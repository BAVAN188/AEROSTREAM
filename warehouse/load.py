import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine


def run():

    engine = create_engine(
        "postgresql://bavanbaskar@localhost:5432/AEROSTREAM1"
    )

    with engine.connect() as conn:
        print("✅ Connected to PostgreSQL successfully!")

    project_root = Path(__file__).resolve().parents[1]
    cleaned_file = project_root / "data" / "processed" / "clean_flights.csv"

    df = pd.read_csv(cleaned_file)
    print("Clean data loaded:", df.shape)

    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

    # =====================
    # DIM_AIRLINE
    # =====================

    unique_airlines = df["OP_UNIQUE_CARRIER"].unique()

    dim_airline = pd.DataFrame({
        "airline_id": range(1, len(unique_airlines) + 1),
        "airline_code": unique_airlines,
        "airline_name": unique_airlines
    })

    print("\nAirlines to load:")
    print(dim_airline)

    dim_airline.to_sql(
        "dim_airline",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("✅ dim_airline loaded!")

        # =====================
    # DIM_AIRPORT
    # =====================

    # Origin airports
    origin_airports = df[["ORIGIN"]].copy()
    origin_airports.columns = ["airport_code"]
    origin_airports["city_name"] = None

    # Destination airports
    dest_airports = df[["DEST", "DEST_CITY_NAME"]].copy()
    dest_airports.columns = ["airport_code", "city_name"]

    # Combine origin + destination airports
    dim_airport = pd.concat(
        [origin_airports, dest_airports],
        ignore_index=True
    )

    # Remove duplicates
    dim_airport = (
        dim_airport
        .drop_duplicates(subset=["airport_code"])
        .reset_index(drop=True)
    )

    # Add IDs
    dim_airport.insert(
        0,
        "airport_id",
        range(1, len(dim_airport) + 1)
    )

    dim_airport["state_name"] = None

    print("\nAirports to load:", len(dim_airport))

    dim_airport.to_sql(
        "dim_airport",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("✅ dim_airport loaded!")

    

    # =====================
    # DIM_TIME
    # =====================

    unique_dates = (
        df["FL_DATE"]
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    dim_time = pd.DataFrame({
        "date_id": range(1, len(unique_dates) + 1),
        "full_date": unique_dates,
        "year": unique_dates.dt.year,
        "month": unique_dates.dt.month,
        "day": unique_dates.dt.day,
        "day_of_week": unique_dates.dt.day_name(),
        "is_weekend": unique_dates.dt.dayofweek >= 5
    })

    print("\nDates to load:", len(dim_time))

    dim_time.to_sql(
        "dim_time",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("✅ dim_time loaded!")

    # =====================
    # READ DIMENSION TABLES
    # =====================

    dim_airline_db = pd.read_sql(
        "SELECT * FROM dim_airline",
        con=engine
    )

    dim_airport_db = pd.read_sql(
        "SELECT * FROM dim_airport",
        con=engine
    )

    dim_time_db = pd.read_sql(
        "SELECT * FROM dim_time",
        con=engine
    )

    print("\nDimension tables loaded back from PostgreSQL")

    # =====================
    # MERGE KEYS
    # =====================

    fact = df.merge(
        dim_airline_db[["airline_id", "airline_code"]],
        left_on="OP_UNIQUE_CARRIER",
        right_on="airline_code",
        how="left"
    )

    print("After airline merge:", fact.shape)

    fact = fact.merge(
        dim_airport_db[["airport_id", "airport_code"]],
        left_on="DEST",
        right_on="airport_code",
        how="left"
    )

    print("After airport merge:", fact.shape)

    dim_time_db["full_date"] = pd.to_datetime(
        dim_time_db["full_date"]
    )

    fact = fact.merge(
        dim_time_db[["date_id", "full_date"]],
        left_on="FL_DATE",
        right_on="full_date",
        how="left"
    )

    print("After time merge:", fact.shape)

    # =====================
    # BUILD FACT TABLE
    # =====================

    fact_final = fact[
        [
            "date_id",
            "airline_id",
            "airport_id",
            "ORIGIN",
            "DEST",
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
    ].copy()

    fact_final = fact_final.rename(columns={
        "airport_id": "dest_id",
        "ORIGIN": "origin",
        "DEST": "dest",
        "DEP_DELAY": "dep_delay",
        "ARR_DELAY": "arr_delay",
        "CANCELLED": "cancelled",
        "CANCELLATION_CODE": "cancellation_code",
        "CARRIER_DELAY": "carrier_delay",
        "WEATHER_DELAY": "weather_delay",
        "NAS_DELAY": "nas_delay",
        "SECURITY_DELAY": "security_delay",
        "LATE_AIRCRAFT_DELAY": "late_aircraft_delay",
        "DISTANCE": "distance",
    })

    print("\nFact table shape:", fact_final.shape)

    fact_final.to_sql(
        "fact_flights",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("\n✅ fact_flights loaded successfully!")


if __name__ == "__main__":
    run()