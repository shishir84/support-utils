import pandas as pd
from io import BytesIO

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()
