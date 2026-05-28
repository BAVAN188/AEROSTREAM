# We import pandas as pd - our main tool for working with data
import pandas as pd

# =====================
# STEP 1: LOAD RAW DATA
# =====================

# Loading the raw CSV file into a dataframe called "raw"
# We call it "raw" because this is the unprocessed original data
raw = pd.read_csv('C:/Users/bavan/AeroStream/ingestion/T_ONTIME_REPORTING.csv')

# Printing shape so we know what we started with
print("Raw data shape:", raw.shape)


# =====================
# STEP 2: FILTER TO JFK
# =====================

# Keep only rows where the flight originated from JFK
# We learned this in explore.py - inner df checks, outer df filters
jfk = raw[raw['ORIGIN'] == 'JFK']

print("JFK flights:", jfk.shape)


# =====================
# STEP 3: KEEP ONLY USEFUL COLUMNS
# =====================

# Out of 64 columns we only need these for our project
# This is called "column selection" - we drop junk we don't need
columns_we_need = [
    'FL_DATE',              # flight date
    'OP_UNIQUE_CARRIER',    # airline code
    'ORIGIN',               # origin airport (all JFK)
    'DEST',                 # destination airport
    'DEST_CITY_NAME',       # destination city name
    'CRS_DEP_TIME',         # scheduled departure time
    'DEP_TIME',             # actual departure time
    'DEP_DELAY',            # departure delay in minutes
    'ARR_DELAY',            # arrival delay in minutes
    'CANCELLED',            # was flight cancelled? 1=yes 0=no
    'CANCELLATION_CODE',    # reason for cancellation
    'CARRIER_DELAY',        # delay caused by airline
    'WEATHER_DELAY',        # delay caused by weather
    'NAS_DELAY',            # delay caused by air traffic control
    'SECURITY_DELAY',       # delay caused by security
    'LATE_AIRCRAFT_DELAY',  # delay caused by late incoming plane
    'DISTANCE'              # distance of flight in miles
]

# Here we create a new dataframe with only our needed columns
# .copy() makes a fresh independent copy so we don't accidentally
# modify the original jfk dataframe
df = jfk[columns_we_need].copy()

print("After column selection:", df.shape)


# =====================
# STEP 4: CHECK MISSING VALUES
# =====================

# .isnull() checks every cell - True if empty, False if has value
# .sum() counts how many True values (empty cells) per column
print("\nMissing values per column:")
print(df.isnull().sum())
# =====================
# STEP 5: HANDLE MISSING VALUES
# =====================

# FL_DATE needs to be converted to a proper date format
# Right now it's a string like "1/1/2025 12:00:00 AM"
# pd.to_datetime() converts it to a real date Python understands
df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='mixed')

# For delay cause columns - if they're empty it means no delay
# So we fill empty cells with 0 (zero minutes of that type of delay)
# .fillna(0) replaces every NaN (empty) with 0
delay_columns = [
    'CARRIER_DELAY',
    'WEATHER_DELAY', 
    'NAS_DELAY',
    'SECURITY_DELAY',
    'LATE_AIRCRAFT_DELAY'
]

# This loops through each delay column and fills empty values with 0
# "for col in delay_columns" means: go through each column name one by one
# df[col].fillna(0) fills that column's empty cells with 0
for col in delay_columns:
    df[col] = df[col].fillna(0)

# For CANCELLATION_CODE - empty means flight operated normally
# We fill with 'N' meaning "Not Cancelled"
df['CANCELLATION_CODE'] = df['CANCELLATION_CODE'].fillna('N')

# For DEP_DELAY and ARR_DELAY - cancelled flights have no delay value
# We fill with 0 because technically delay doesnt apply
df['DEP_DELAY'] = df['DEP_DELAY'].fillna(0)
df['ARR_DELAY'] = df['ARR_DELAY'].fillna(0)

# Check missing values again - should be 0 for everything now
print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nData types after cleaning:")
print(df.dtypes)
# =====================
# STEP 6: SAVE CLEAN DATA
# =====================

# We save the cleaned dataframe as a new CSV file
# This goes into the cleaning folder as "jfk_clean.csv"
# index=False means don't save the row numbers as a column
df.to_csv('C:/Users/bavan/AeroStream/cleaning/jfk_clean.csv', index=False)

print("\n✅ Clean data saved! Shape:", df.shape)
print("File saved to: cleaning/jfk_clean.csv")