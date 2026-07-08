import streamlit as st


def show_kpis(total_flights, avg_delay, cancel_rate):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="✈️ Total Flights",
            value=f"{int(total_flights):,}"
        )

    with col2:
        st.metric(
            label="⏱ Average Arrival Delay",
            value=f"{avg_delay} min"
        )

    with col3:
        st.metric(
            label="❌ Cancellation Rate",
            value=f"{cancel_rate}%"
        )