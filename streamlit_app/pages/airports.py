import streamlit as st
import plotly.express as px
from utils.database import query


def airports():

    st.title("🛫 Airport Analytics")
    st.caption("Airport Operations & Network Intelligence")

    # =====================================================
    # KPI QUERIES
    # =====================================================

    total_airports = query("""
    SELECT COUNT(*) total
    FROM dim_airport
    """).iloc[0]["total"]

    busiest = query("""
    SELECT
        airport_name,
        COUNT(*) flights
    FROM fact_flights f
    JOIN dim_airport a
        ON f.dest_id = a.airport_id
    GROUP BY airport_name
    ORDER BY flights DESC
    LIMIT 1
    """)

    highest_delay = query("""
    SELECT
        airport_name,
        ROUND(AVG(arr_delay)::numeric,2) delay
    FROM fact_flights f
    JOIN dim_airport a
        ON f.dest_id = a.airport_id
    GROUP BY airport_name
    ORDER BY delay DESC
    LIMIT 1
    """)

    avg_flights = query("""
    SELECT ROUND(
        COUNT(*)::numeric /
        (SELECT COUNT(*) FROM dim_airport),
        0
    ) avg_flights
    FROM fact_flights
    """).iloc[0]["avg_flights"]

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Airports",
        int(total_airports)
    )

    c2.metric(
        "Busiest Airport",
        busiest.iloc[0]["airport_name"]
    )

    c3.metric(
        "Highest Delay",
        highest_delay.iloc[0]["airport_name"]
    )

    c4.metric(
        "Avg Flights / Airport",
        int(avg_flights)
    )

    st.divider()

    # =====================================================
    # AIRPORT MAP
    # =====================================================

    st.subheader("🇺🇸 United States Airport Network")

    airport = query("""

    SELECT

    airport_name,

    city_name,

    state_name,

    latitude,

    longitude,

    COUNT(*) flights,

    ROUND(AVG(arr_delay)::numeric,2) avg_delay,

    ROUND((AVG(cancelled)*100)::numeric,2) cancel_rate

    FROM fact_flights f

    JOIN dim_airport a

    ON f.dest_id=a.airport_id

    GROUP BY

    airport_name,

    city_name,

    state_name,

    latitude,

    longitude

    ORDER BY flights DESC

    """)

    fig = px.scatter_map(

        airport,

        lat="latitude",

        lon="longitude",

        size="flights",

        color="avg_delay",

        hover_name="airport_name",

        hover_data={

            "city_name":True,

            "state_name":True,

            "flights":True,

            "avg_delay":True,

            "cancel_rate":True,

            "latitude":False,

            "longitude":False

        },

        size_max=30,

        zoom=3.2,

        height=650,

        color_continuous_scale="RdYlGn_r",

        map_style="carto-darkmatter"

    )

    fig.update_layout(

        paper_bgcolor="#0B0F17",

        plot_bgcolor="#0B0F17",

        font_color="white",

        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0

        )

    )

    fig.update_traces(
    marker=dict(
        opacity=0.85
    )
)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()
        # =====================================================
    # TOP AIRPORTS + HISTOGRAM
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("🏆 Top 10 Busiest Airports")

        top_airports = query("""

        SELECT

        airport_name,

        COUNT(*) flights

        FROM fact_flights f

        JOIN dim_airport a

        ON f.dest_id = a.airport_id

        GROUP BY airport_name

        ORDER BY flights DESC

        LIMIT 10

        """)

        fig2 = px.bar(

            top_airports,

            x="flights",

            y="airport_name",

            orientation="h",

            text="flights",

            color="flights",

            color_continuous_scale="Blues"

        )

        fig2.update_layout(

            height=420,

            yaxis_title="",

            xaxis_title="Flights",

            paper_bgcolor="#0B0F17",

            plot_bgcolor="#0B0F17",

            font_color="white"

        )

        st.plotly_chart(

            fig2,

            use_container_width=True

        )

    with right:

        st.subheader("📈 Airport Delay Distribution")

        histogram = query("""

        SELECT

        airport_name,

        ROUND(AVG(arr_delay)::numeric,2) avg_delay

        FROM fact_flights f

        JOIN dim_airport a

        ON f.dest_id = a.airport_id

        GROUP BY airport_name

        """)

        fig3 = px.histogram(

            histogram,

            x="avg_delay",

            nbins=25,

            color_discrete_sequence=["#3B82F6"]

        )

        fig3.update_layout(

            height=420,

            paper_bgcolor="#0B0F17",

            plot_bgcolor="#0B0F17",

            font_color="white",

            xaxis_title="Average Delay (Minutes)",

            yaxis_title="Number of Airports"

        )

        st.plotly_chart(

            fig3,

            use_container_width=True

        )

        st.divider()

    st.subheader("📋 Airport Performance Leaderboard")

    leaderboard = query("""

    SELECT

    airport_name,

    city_name,

    state_name,

    COUNT(*) AS flights,

    ROUND(AVG(arr_delay)::numeric,2) AS avg_delay,

    ROUND((AVG(cancelled)*100)::numeric,2) AS cancel_rate

    FROM fact_flights f

    JOIN dim_airport a

    ON f.dest_id = a.airport_id

    GROUP BY

    airport_name,

    city_name,

    state_name

    ORDER BY

    COUNT(*) DESC

    """)

    leaderboard.columns = [

        "Airport",

        "City",

        "State",

        "Flights",

        "Avg Delay (min)",

        "Cancellation %"

    ]

    st.dataframe(

        leaderboard,

        use_container_width=True,

        hide_index=True,

        height=500

    )