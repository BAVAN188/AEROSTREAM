import pandas as pd
import os

# =====================
# STEP 1: LOAD ALL 4 MONTHS
# =====================

# List all CSV files in the ingestion folder
# Each file is one month of flight data
ingestion_path = 'C:/Users/bavan/AeroStream/ingestion/'

files = [
    'T_ONTIME_REPORTING.csv',        # January
    'T_ONTIME_REPORTING FEB.csv',    # February
    'T_ONTIME_REPORTING MARCH.csv',  # March
    'T_ONTIME_REPORTING APRIL.csv'   # April
]

# Empty list to store each month's dataframe
# Think of it like an empty box we'll fill with 4 tables
all_months = []

# Loop through each file, load it, add to the list
for file in files:
    path = ingestion_path + file
    df_month = pd.read_csv(path)
    print(f"Loaded {file}: {df_month.shape}")
    all_months.append(df_month)

# Combine all 4 months into one big dataframe
# pd.concat() stacks dataframes on top of each other like stacking papers
# ignore_index=True resets row numbers from 0 to end
raw = pd.concat(all_months, ignore_index=True)
print("\nAll months combined:", raw.shape)

# =====================
# STEP 2: FILTER TO JFK
# =====================

jfk = raw[raw['ORIGIN'] == 'JFK']
print("JFK flights:", jfk.shape)

# =====================
# STEP 3: KEEP USEFUL COLUMNS
# =====================

columns_we_need = [
    'FL_DATE',
    'OP_UNIQUE_CARRIER',
    'ORIGIN',
    'DEST',
    'DEST_CITY_NAME',
    'CRS_DEP_TIME',
    'DEP_TIME',
    'DEP_DELAY',
    'ARR_DELAY',
    'CANCELLED',
    'CANCELLATION_CODE',
    'CARRIER_DELAY',
    'WEATHER_DELAY',
    'NAS_DELAY',
    'SECURITY_DELAY',
    'LATE_AIRCRAFT_DELAY',
    'DISTANCE'
]

df = jfk[columns_we_need].copy()
print("After column selection:", df.shape)

# =====================
# STEP 4: CLEAN DATA
# =====================

df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='mixed')

delay_columns = [
    'CARRIER_DELAY',
    'WEATHER_DELAY',
    'NAS_DELAY',
    'SECURITY_DELAY',
    'LATE_AIRCRAFT_DELAY'
]

for col in delay_columns:
    df[col] = df[col].fillna(0)

df['CANCELLATION_CODE'] = df['CANCELLATION_CODE'].fillna('N')
df['DEP_DELAY'] = df['DEP_DELAY'].fillna(0)
df['ARR_DELAY'] = df['ARR_DELAY'].fillna(0)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# =====================
# STEP 5: SAVE CLEAN DATA
# =====================

df.to_csv('C:/Users/bavan/AeroStream/cleaning/jfk_clean.csv', index=False)
print("\n✅ Clean data saved! Shape:", df.shape)