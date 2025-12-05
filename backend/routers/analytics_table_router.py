from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
from services.analytics_table_service import get_single, get_bulk
from models.analytics_table_model import (
    AnalyticsTableItem,
    BulkAnalyticsTableResponse,
)

router = APIRouter(
    prefix="/analytics-table",
    tags=["Learning Analytics Table"],
)

@router.get("/single/{user_id}", response_model=AnalyticsTableItem)
def get_single_analytics(user_id: str):
    return get_single(user_id)

@router.post("/bulk", response_model=BulkAnalyticsTableResponse)
async def bulk_analytics(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Excel file")

    if "UserID" not in df.columns:
        raise HTTPException(status_code=400, detail="Excel must contain 'UserID' column")

    user_ids: List[str] = [str(v) for v in df["UserID"].tolist()]
    data = get_bulk(user_ids)
    return {"data": data}
