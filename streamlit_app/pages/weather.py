import streamlit as st
import plotly.express as px
from utils.database import query


def weather():

    st.title("🌦 Weather Analytics")
    st.caption("Weather Impact on Flight Operations")

    # ======================================
    # KPIs
    # ======================================

    weather_impacted = query("""

    SELECT

    COUNT(*) impacted

    FROM fact_flights

    WHERE weather_delay > 0

    """).iloc[0]["impacted"]

    avg_weather = query("""

    SELECT

    ROUND(AVG(weather_delay)::numeric,2) avg_weather

    FROM fact_flights

    WHERE weather_delay > 0

    """).iloc[0]["avg_weather"]

    max_weather = query("""

    SELECT

    ROUND(MAX(weather_delay)::numeric,2) worst

    FROM fact_flights

    """).iloc[0]["worst"]

    weather_percent = query("""

    SELECT

    ROUND(

    (SUM(CASE WHEN weather_delay>0 THEN 1 ELSE 0 END)

    *100.0

    /COUNT(*))::numeric

    ,2)

    weather

    FROM fact_flights

    """).iloc[0]["weather"]

    c1,c2,c3,c4=st.columns(4)

    c1.metric(

        "Weather Impacted Flights",

        f"{int(weather_impacted):,}"

    )

    c2.metric(

        "Average Weather Delay",

        f"{avg_weather} min"

    )

    c3.metric(

        "Worst Weather Delay",

        f"{max_weather} min"

    )

    c4.metric(

        "Weather Impact",

        f"{weather_percent}%"

    )

    st.divider()

    # ======================================
    # WEATHER SCATTER
    # ======================================

    st.subheader("🌧 Weather Delay vs Arrival Delay")

    scatter=query("""

    SELECT

    weather_delay,

    arr_delay,

    distance

    FROM fact_flights

    WHERE weather_delay>0

    LIMIT 15000

    """)

    fig=px.scatter(

        scatter,

        x="weather_delay",

        y="arr_delay",

        size="distance",

        opacity=.6,

        color="arr_delay",

        color_continuous_scale="Turbo",

        height=600

    )

    fig.update_layout(

        paper_bgcolor="#0B0F17",

        plot_bgcolor="#0B0F17",

        font_color="white",

        xaxis_title="Weather Delay (Minutes)",

        yaxis_title="Arrival Delay (Minutes)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ======================================
    # HISTOGRAM + TOP AIRLINES
    # ======================================

    left, right = st.columns(2)

    with left:

        st.subheader("📈 Weather Delay Distribution")

        hist = query("""

        SELECT

        weather_delay

        FROM fact_flights

        WHERE weather_delay > 0

        """)

        fig2 = px.histogram(

            hist,

            x="weather_delay",

            nbins=30,

            color_discrete_sequence=["#3B82F6"]

        )

        fig2.update_layout(

            height=420,

            paper_bgcolor="#0B0F17",

            plot_bgcolor="#0B0F17",

            font_color="white",

            xaxis_title="Weather Delay (Minutes)",

            yaxis_title="Flights"

        )

        st.plotly_chart(

            fig2,

            use_container_width=True

        )

    with right:

        st.subheader("✈ Airlines Most Affected")

        airline = query("""

        SELECT

        a.airline_name,

        ROUND(AVG(weather_delay)::numeric,2) avg_weather,

        COUNT(*) flights

        FROM fact_flights f

        JOIN dim_airline a

        ON f.airline_id=a.airline_id

        WHERE weather_delay>0

        GROUP BY a.airline_name

        ORDER BY avg_weather DESC

        """)

        fig3 = px.bar(

            airline,

            x="avg_weather",

            y="airline_name",

            orientation="h",

            text="avg_weather",

            color="avg_weather",

            color_continuous_scale="Oranges"

        )

        fig3.update_layout(

            height=420,

            yaxis_title="",

            xaxis_title="Average Weather Delay",

            paper_bgcolor="#0B0F17",

            plot_bgcolor="#0B0F17",

            font_color="white"

        )

        st.plotly_chart(

            fig3,

            use_container_width=True

        )

    st.divider()

    # ======================================
    # TOP WEATHER AFFECTED AIRPORTS
    # ======================================

    st.subheader("🌩 Airports Most Affected by Weather")

    airports = query("""

    SELECT

    airport_name,

    city_name,

    state_name,

    COUNT(*) flights,

    ROUND(AVG(weather_delay)::numeric,2) avg_weather,

    ROUND(AVG(arr_delay)::numeric,2) avg_arrival

    FROM fact_flights f

    JOIN dim_airport a

    ON f.dest_id=a.airport_id

    WHERE weather_delay>0

    GROUP BY

    airport_name,

    city_name,

    state_name

    ORDER BY avg_weather DESC

    """)

    airports.columns = [

        "Airport",

        "City",

        "State",

        "Flights",

        "Weather Delay",

        "Arrival Delay"

    ]

    st.dataframe(

        airports,

        use_container_width=True,

        hide_index=True,

        height=500

    )

    st.caption(

        "Weather analytics generated from the AeroStream PostgreSQL warehouse."

    )