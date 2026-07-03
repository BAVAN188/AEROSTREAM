# importing pandas library, nickname "pd"
# pandas lets Python work with tables of data like Excel
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
raw_file = project_root / 'data' / 'raw' / 'T_ONTIME_REPORTING.csv'

# reading the CSV file into a dataframe called "df"
# dataframe = a table stored in Python memory with rows and columns
df = pd.read_csv(raw_file)

# shape = (number of rows, number of columns)
print("Shape:", df.shape)

# shows all column names as a list
print("\nColumns:", df.columns.tolist())

# filters dataframe to only JFK rows
# df['ORIGIN'] == 'JFK' means keep only rows where ORIGIN column = JFK
jfk = df[df['ORIGIN'] == 'JFK']

# how many JFK flights after filtering
print("\nJFK shape:", jfk.shape)

# check if delay columns exist now
print("\nDelay columns:")
print(jfk[['FL_DATE', 'DEP_DELAY', 'ARR_DELAY']].head(10))