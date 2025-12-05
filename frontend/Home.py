import streamlit as st
from utils.auth_utils import logout
from pages import (
    LearningHistory,
    LearningHours,
    LoginIssue,
    ContentCompletion,
    WorkProfile,
    AnalyticsTable,
)

# Page setup
st.set_page_config(
    page_title="Support Automation Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove sidebar completely
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        .css-1d391kg {display: none !important;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


# ------------------------------------------------------
# Top-right Logout Button
# ------------------------------------------------------
def render_logout_button():
    st.markdown(
        """
        <style>
            .logout-button {
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 999;
            }
            .logout-button button {
                padding: 6px 12px;
                background-color: #ff4b4b !important;
                color: white !important;
                border-radius: 6px !important;
            }
        </style>
        <div class="logout-button">
        """,
        unsafe_allow_html=True
    )
    
    if st.button("Logout"):
        logout()
        st.session_state["current_page"] = None
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------
# Card/Tiles Configuration
# ------------------------------------------------------
MODULES = {
    "Learning History": {
        "page": LearningHistory,
        "icon": "📘",
        "color": "#4A90E2"
    },
    "Learning Hours": {
        "page": LearningHours,
        "icon": "⏱️",
        "color": "#50C878"
    },
    "Login Issue": {
        "page": LoginIssue,
        "icon": "⚠️",
        "color": "#F5A623"
    },
    "Content Completion": {
        "page": ContentCompletion,
        "icon": "📊",
        "color": "#9B59B6"
    },
    "Work Profile": {
        "page": WorkProfile,
        "icon": "👤",
        "color": "#E67E22"
    },
    "Analytics Table": {
        "page": AnalyticsTable,
        "icon": "📈",
        "color": "#2ECC71"
    },
}


# ------------------------------------------------------
# Render Tiles Homepage
# ------------------------------------------------------
def render_home():

    render_logout_button()

    # When module is selected, load module page
    if st.session_state.get("current_page"):
        selected = st.session_state["current_page"]
        MODULES[selected]["page"].render()
        return

    st.markdown(
        "<h1 style='text-align:center; color:#0066CC;'>Support Automation Dashboard</h1><br>",
        unsafe_allow_html=True
    )

    cols = st.columns(3, gap="large")

    index = 0
    for label, config in MODULES.items():
        col = cols[index % 3]
        index += 1

        # Tile card HTML
        tile_html = f"""
        <div style="
            background-color: {config['color']}20;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            border: 2px solid {config['color']};
            transition: 0.2s;
            height: 150px;
        "
        onmouseover="this.style.transform='scale(1.03)'"
        onmouseout="this.style.transform='scale(1)'"
        >
            <div style="font-size: 50px;">{config['icon']}</div>
            <h3 style="color:{config['color']}">{label}</h3>
        </div>
        """

        if col.button(label, key=f"btn_{label}", help=label):
            st.session_state["current_page"] = label
            st.rerun()

        col.markdown(tile_html, unsafe_allow_html=True)
