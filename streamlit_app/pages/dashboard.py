import streamlit as st
import plotly.express as px
from utils.database import query


def dashboard():
    st.title("✈ Executive Dashboard")
    st.caption("Enterprise Aviation Intelligence Platform")

    # ================= KPIs ================= #

    total_flights = query("""
        SELECT COUNT(*) total
        FROM fact_flights
    """).iloc[0]["total"]

    avg_delay = query("""
        SELECT ROUND(AVG(arr_delay)::numeric, 2) avg_delay
        FROM fact_flights
    """).iloc[0]["avg_delay"]

    cancel_rate = query("""
        SELECT ROUND((AVG(cancelled) * 100)::numeric, 2) cancel_rate
        FROM fact_flights
    """).iloc[0]["cancel_rate"]

    weather_delay = query("""
        SELECT ROUND(
            (SUM(CASE WHEN weather_delay > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*))::numeric,
            2
        ) weather
        FROM fact_flights
    """).iloc[0]["weather"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Flights", f"{int(total_flights):,}")
    c2.metric("Avg Delay", f"{avg_delay} min")
    c3.metric("Cancelled", f"{cancel_rate}%")
    c4.metric("Weather Delay", f"{weather_delay}%")

    st.divider()

    left, right = st.columns([2, 1])

    # ===========================================================
    # MAP
    # ===========================================================
    with left:
        st.subheader("USA Airport Operations")

        airport = query("""
            SELECT
                airport_name,
                latitude,
                longitude,
                COUNT(*) flights,
                ROUND(AVG(arr_delay)::numeric, 2) delay
            FROM fact_flights f
            JOIN dim_airport a ON f.dest_id = a.airport_id
            GROUP BY airport_name, latitude, longitude
        """)

        fig = px.scatter_mapbox(
            airport,
            lat="latitude",
            lon="longitude",
            size="flights",
            color="delay",
            hover_name="airport_name",
            zoom=3,
            height=500,
            color_continuous_scale="RdYlGn_r"
        )

        fig.update_layout(
            mapbox_style="carto-darkmatter",
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ===========================================================
    with right:
        st.subheader("Top Airlines")

        airline = query("""
            SELECT
                airline_name,
                ROUND(AVG(arr_delay)::numeric, 2) delay
            FROM fact_flights f
            JOIN dim_airline a ON f.airline_id = a.airline_id
            GROUP BY airline_name
            ORDER BY delay DESC
            LIMIT 10
        """)

        fig2 = px.bar(
            airline,
            x="delay",
            y="airline_name",
            orientation="h",
            color="delay",
            color_continuous_scale="Reds"
        )

        fig2.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Delay Cause")

        cause = query("""
            SELECT
                SUM(weather_delay) weather,
                SUM(carrier_delay) carrier,
                SUM(nas_delay) nas,
                SUM(late_aircraft_delay) late,
                SUM(security_delay) security
            FROM fact_flights
        """)

        pie = px.pie(
            names=[
                "Weather",
                "Carrier",
                "NAS",
                "Late Aircraft",
                "Security"
            ],
            values=[
                cause.weather[0],
                cause.carrier[0],
                cause.nas[0],
                cause.late[0],
                cause.security[0]
            ],
            hole=.65
        )

        pie.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(pie, use_container_width=True)

    # ===========================================================

    st.divider()

    st.subheader("Monthly Delay Trend")

    trend = query("""
        SELECT
            EXTRACT(MONTH FROM flight_date) AS flight_month,
            ROUND(AVG(arr_delay)::numeric, 2) AS delay
        FROM fact_flights
        GROUP BY flight_month
        ORDER BY flight_month
    """)

    line = px.line(
        trend,
        x="flight_month",
        y="delay",
        markers=True
    )

    line.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(line, use_container_width=True)