import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="AEROSTREAM",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- SIDEBAR ----------

with st.sidebar:

    st.markdown("# ✈️ AEROSTREAM")
    st.caption("Enterprise Aviation Intelligence")

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Airlines",
            "Airports",
            "Weather"
        ],
        icons=[
            "speedometer2",
            "airplane",
            "geo-alt",
            "cloud-rain"
        ],
        default_index=0
    )

st.markdown(
"""
<style>

.block-container{
padding-top:1rem;
padding-bottom:1rem;
padding-left:2rem;
padding-right:2rem;
}

</style>
""",
unsafe_allow_html=True
)

if selected=="Dashboard":
    from pages.dashboard import dashboard
    dashboard()

elif selected=="Airlines":
    from pages.airlines import airlines
    airlines()

elif selected=="Airports":
    from pages.airports import airports
    airports()

elif selected=="Weather":
    from pages.weather import weather
    weather()