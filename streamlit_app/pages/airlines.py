import streamlit as st
import plotly.express as px
from utils.database import query


def airlines():

    st.title("✈ Airline Analytics")
    st.caption("Operational Performance Across Airlines")

    # =====================================
    # KPIs
    # =====================================

    total_airlines = query("""
    SELECT COUNT(*) total
    FROM dim_airline
    """).iloc[0]["total"]

    avg_delay = query("""
    SELECT ROUND(AVG(arr_delay)::numeric,2) delay
    FROM fact_flights
    """).iloc[0]["delay"]

    best = query("""
    SELECT
        airline_name,
        ROUND(AVG(arr_delay)::numeric,2) delay
    FROM fact_flights f
    JOIN dim_airline a
        ON f.airline_id=a.airline_id
    GROUP BY airline_name
    ORDER BY delay ASC
    LIMIT 1
    """)

    worst = query("""
    SELECT
        airline_name,
        ROUND(AVG(arr_delay)::numeric,2) delay
    FROM fact_flights f
    JOIN dim_airline a
        ON f.airline_id=a.airline_id
    GROUP BY airline_name
    ORDER BY delay DESC
    LIMIT 1
    """)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Airlines",
        int(total_airlines)
    )

    c2.metric(
        "Average Delay",
        f"{avg_delay} min"
    )

    c3.metric(
        "Best Airline",
        best.iloc[0]["airline_name"]
    )

    c4.metric(
        "Worst Airline",
        worst.iloc[0]["airline_name"]
    )

    st.divider()
    st.subheader("Top Airlines by Average Delay")

    airlines = query("""

    SELECT

    airline_name,

    COUNT(*) flights,

    ROUND(AVG(arr_delay)::numeric,2) delay

    FROM fact_flights f

    JOIN dim_airline a

    ON f.airline_id=a.airline_id

    GROUP BY airline_name

    ORDER BY delay DESC

    """)

    fig = px.bar(

        airlines,

        x="delay",

        y="airline_name",

        orientation="h",

        text="delay",

        color="delay",

        color_continuous_scale="Reds"

    )

    fig.update_layout(

        height=500,

        yaxis_title="",

        xaxis_title="Average Arrival Delay (Minutes)",

        paper_bgcolor="#0B0F17",

        plot_bgcolor="#0B0F17",

        font_color="white"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )
    st.subheader("Airline Performance Table")

    table = query("""

    SELECT

    airline_name,

    COUNT(*) flights,

    ROUND(AVG(arr_delay)::numeric,2) avg_delay,

    ROUND((AVG(cancelled)*100)::numeric,2) cancel_rate,

    ROUND(AVG(carrier_delay)::numeric,2) carrier_delay,

    ROUND(AVG(weather_delay)::numeric,2) weather_delay,

    ROUND(AVG(nas_delay)::numeric,2) nas_delay,

    ROUND(AVG(late_aircraft_delay)::numeric,2) late_aircraft_delay

    FROM fact_flights f

    JOIN dim_airline a

    ON f.airline_id=a.airline_id

    GROUP BY airline_name

    ORDER BY avg_delay DESC

    """)

    st.dataframe(

        table,

        use_container_width=True,

        hide_index=True

    )