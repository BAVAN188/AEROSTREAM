# ✈️ AeroStream


# Enterprise Flight Operations Analytics Platform

**End-to-End Data Engineering \| PostgreSQL Data Warehouse \| Streamlit
Analytics \| Plotly Dashboards**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)
:::

------------------------------------------------------------------------

## 🚀 Overview

AeroStream is an end-to-end data engineering project that transforms raw
U.S. flight operations data into a modern analytics platform.

The project demonstrates the complete data lifecycle:

-   Data ingestion
-   Cleaning & transformation
-   Data quality validation
-   PostgreSQL star-schema warehouse
-   Business SQL analytics
-   Interactive Streamlit dashboards

**Dataset Scale**

  Metric                    Value
  ------------------ ------------
  Flight Records       2,240,464+
  Fact Tables                   1
  Dimension Tables              2
  Dashboard Pages               4
  Visualizations              15+

------------------------------------------------------------------------

# 🏗️ System Architecture

``` mermaid
flowchart LR

A[Raw Flight Data]
-->B[Ingestion]

B-->C[Cleaning]

C-->D[Validation]

D-->E[PostgreSQL Data Warehouse]

E-->F[Business SQL]

F-->G[Streamlit Analytics]

G-->H[Executive Dashboard]
```

------------------------------------------------------------------------

# ⭐ Star Schema

``` mermaid
erDiagram

FACT_FLIGHTS }o--|| DIM_AIRLINE : airline_id
FACT_FLIGHTS }o--|| DIM_AIRPORT : dest_id

FACT_FLIGHTS {
    bigint date_id
    int airline_id
    int dest_id
    float arr_delay
    float dep_delay
    boolean cancelled
    float weather_delay
    float carrier_delay
    float nas_delay
    float security_delay
    float late_aircraft_delay
    float distance
}

DIM_AIRLINE {
    int airline_id
    string airline_code
    string airline_name
}

DIM_AIRPORT {
    int airport_id
    string airport_name
    string city_name
    string state_name
    float latitude
    float longitude
}
```

------------------------------------------------------------------------

# 📊 Dashboard Modules

## 🏠 Executive Dashboard

-   Flight KPIs
-   Delay Analysis
-   Cancellation Rate
-   Weather Impact
-   USA Airport Operations Map
-   Delay Cause Analysis
-   Monthly Trends

📸 **Screenshot:** `assets/dashboard.png`

------------------------------------------------------------------------

## ✈️ Airline Analytics

-   Airline Rankings
-   Performance KPIs
-   Delay Comparison
-   Performance Leaderboard
-   Airline Analytics Table

📸 **Screenshot:** `assets/airlines.png`

------------------------------------------------------------------------

## 🛫 Airport Analytics

-   Interactive USA Airport Map
-   Airport KPIs
-   Airport Delay Distribution
-   Busiest Airports
-   Airport Leaderboard

📸 **Screenshot:** `assets/airports.png`

------------------------------------------------------------------------

## 🌦 Weather Analytics

-   Weather Impact KPIs
-   Weather vs Arrival Delay
-   Weather Distribution
-   Airlines Most Affected
-   Airports Most Affected

📸 **Screenshot:** `assets/weather.png`

------------------------------------------------------------------------

# 🛠 Tech Stack

  Layer             Technology
  ----------------- --------------
  Language          Python
  Data Processing   Pandas
  Database          PostgreSQL
  SQL               PostgreSQL
  ORM               SQLAlchemy
  Dashboard         Streamlit
  Visualization     Plotly
  Driver            psycopg2
  Version Control   Git & GitHub

------------------------------------------------------------------------

# 📂 Project Structure

``` text
AEROSTREAM/
│
├── analytics/
├── cleaning/
├── ingestion/
├── validation/
├── warehouse/
├── weather/
├── utils/
├── streamlit_app/
│   ├── app.py
│   ├── pages/
│   ├── utils/
│   └── assets/
├── data/
├── main.py
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# ▶️ Run Locally

``` bash
git clone https://github.com/BAVAN188/AEROSTREAM.git
cd AEROSTREAM

python -m venv .venv

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

python main.py

streamlit run streamlit_app/app.py
```

------------------------------------------------------------------------

# 📈 Key Engineering Highlights

-   Modular ETL pipeline
-   PostgreSQL warehouse using a star schema
-   Business-focused SQL analytics
-   Multi-page Streamlit application
-   Geospatial airport analytics
-   Weather impact analytics
-   Interactive Plotly visualizations

------------------------------------------------------------------------

# 🚀 Future Enhancements

-   Cloud PostgreSQL (Neon)
-   Streamlit Cloud deployment
-   Docker
-   Apache Airflow
-   CI/CD
-   AWS deployment

------------------------------------------------------------------------

# 👨‍💻 Author

**Bavan Baskar**

GitHub: https://github.com/BAVAN188

If you found this project useful, consider ⭐ starring the repository.
