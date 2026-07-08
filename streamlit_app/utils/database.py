from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

DATABASE_URL = "postgresql://bavanbaskar@localhost:5432/AEROSTREAM1"

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

@st.cache_data(ttl=300)
def query(sql):
    return pd.read_sql(sql, get_engine())