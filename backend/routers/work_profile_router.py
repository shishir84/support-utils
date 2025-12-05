from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
from services.work_profile_service import get_single, get_bulk
from models.work_profile_model import WorkProfileItem, BulkWorkProfileResponse

router = APIRouter(
    prefix="/work-profile",
    tags=["Work Profile"],
)

@router.get("/single/{user_id}", response_model=WorkProfileItem)
def get_single_profile(user_id: str):
    return get_single(user_id)

@router.post("/bulk", response_model=BulkWorkProfileResponse)
async def bulk_profile(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Excel file")

    if "UserID" not in df.columns:
        raise HTTPException(status_code=400, detail="Excel must contain 'UserID' column")

    user_ids: List[str] = [str(v) for v in df["UserID"].tolist()]
    data = get_bulk(user_ids)
    return {"data": data}
