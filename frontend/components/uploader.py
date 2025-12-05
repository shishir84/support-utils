import streamlit as st

def excel_uploader(key: str):
    return st.file_uploader(
        "Upload Excel with 'UserID' column",
        type=["xls", "xlsx"],
        key=key
    )
