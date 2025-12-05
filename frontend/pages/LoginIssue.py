import streamlit as st
from components.uploader import excel_uploader
from components.table_renderer import render_table_with_download
from utils.api_client import get_single, get_bulk

FEATURE_SLUG = "login-issue"

def go_home():
    st.session_state["current_page"] = None
    st.rerun()

def render():
    if st.button("⬅ Back to Home"):
        go_home()

    st.header("Login Issues")

    st.subheader("Single User Lookup")
    user_id = st.text_input("Enter WID/UserID", key="li_single_user")
    if st.button("Get Login Issues", key="li_single_btn"):
        if user_id.strip():
            resp = get_single(FEATURE_SLUG, user_id.strip())
            if "error" in resp:
                st.error(resp["error"])
            else:
                render_table_with_download([resp], f"login_issue_{user_id}")
        else:
            st.warning("Please enter a UserID.")

    st.markdown("---")

    st.subheader("Bulk Lookup")
    uploaded = excel_uploader("li_bulk_upload")
    if st.button("Process Bulk", key="li_bulk_btn"):
        if uploaded is None:
            st.warning("Please upload an Excel file.")
        else:
            resp = get_bulk(FEATURE_SLUG, uploaded)
            if "error" in resp:
                st.error(resp["error"])
            else:
                render_table_with_download(resp.get("data", []), "login_issue_bulk")
