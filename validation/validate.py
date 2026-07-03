import pandas as pd
from pathlib import Path
import sys
from utils.logger import logger


def run():

    # =====================
    # LOAD CLEANED DATA
    # =====================

    project_root = Path(__file__).resolve().parents[1]
    cleaned_file = project_root / "data" / "processed" / "jfk_clean.csv"

    df = pd.read_csv(cleaned_file)

    # =====================
    # DATA VALIDATION REPORT
    # =====================

    logger.info("=" * 35)
    logger.info("DATA VALIDATION REPORT")
    logger.info("=" * 35)

    # 1. Missing Flight Dates
    missing_dates = df["FL_DATE"].isnull().sum()
    logger.info(f"Missing Flight Dates : {missing_dates}")

    # 2. Missing Airline Codes
    missing_airlines = df["OP_UNIQUE_CARRIER"].isnull().sum()
    logger.info(f"Missing Airline Codes : {missing_airlines}")

    # 3. Missing Origin Airports
    missing_origin = df["ORIGIN"].isnull().sum()
    logger.info(f"Missing Origin : {missing_origin}")

    # 4. Missing Destination Airports
    missing_dest = df["DEST"].isnull().sum()
    logger.info(f"Missing Destination : {missing_dest}")

    # 5. Negative Distance
    negative_distance = (df["DISTANCE"] < 0).sum()
    logger.info(f"Negative Distance : {negative_distance}")

    # 6. Duplicate Rows
    duplicates = df.duplicated().sum()
    logger.info(f"Duplicate Rows : {duplicates}")

    logger.info("=" * 35)

    # =====================
    # VALIDATION RESULT
    # =====================

    if (
        missing_dates == 0
        and missing_airlines == 0
        and missing_origin == 0
        and missing_dest == 0
        and negative_distance == 0
        and duplicates == 0
    ):
        logger.info("✅ Validation Passed")
    else:
        logger.error("❌ Validation Failed")
        logger.error("Stopping pipeline...")
        sys.exit(1)


if __name__ == "__main__":
    run()