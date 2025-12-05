import streamlit as st
import pandas as pd
from utils.file_utils import df_to_csv_bytes

def render_table_with_download(data_list, default_filename: str):
    if not data_list:
        st.info("No data to display.")
        return
    df = pd.DataFrame(data_list)
    st.dataframe(df, use_container_width=True)

    csv_bytes = df_to_csv_bytes(df)
    st.download_button(
        label="Download as CSV",
        data=csv_bytes,
        file_name=f"{default_filename}.csv",
        mime="text/csv",
    )
