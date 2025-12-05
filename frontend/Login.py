import streamlit as st
from utils.api_client import login_api
from utils.auth_utils import is_logged_in, set_logged_in
import Home

# Page config (no sidebar)
st.set_page_config(page_title="Support Automation Login", layout="wide")

# Remove sidebar
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        .css-1d391kg {display: none !important;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


def main():
    if is_logged_in():
        Home.render_home()
        return

    # ---------- Banner ----------
    st.markdown(
        """
        <h1 style='text-align: center; color: #0066CC; font-size: 42px; 
        font-weight: bold; margin-top: 20px;'>
            Support Automation
        </h1>
        """,
        unsafe_allow_html=True
    )

    # spacing
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- Centered Login Box ----------
    left, center, right = st.columns([2, 1, 2])

    with center:
        st.markdown("<h3 style='text-align:center;'>Login</h3>", unsafe_allow_html=True)

        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")

        if st.button("Login", use_container_width=True):
            token = login_api(username, password)
            if token:
                set_logged_in(token)
                st.session_state["current_page"] = None
                st.rerun()
            else:
                st.error("Invalid credentials")


if __name__ == "__main__":
    main()
