import streamlit as st

def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)

def set_logged_in(token: str):
    st.session_state["logged_in"] = True
    st.session_state["auth_token"] = token

def logout():
    st.session_state.clear()
