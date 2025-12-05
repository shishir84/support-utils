import streamlit as st

PAGES = [
    "Learning History",
    "Learning Hours",
    "Login Issue",
    "Content Completion",
    "Work Profile",
    "Analytics Table",
]

def render_sidebar() -> str:
    with st.sidebar:
        st.header("Navigation")
        selected = st.radio("Go to", PAGES, key="sidebar_selection")
        st.markdown("---")
        if st.button("Logout"):
            st.session_state["logout_clicked"] = True
        return selected
