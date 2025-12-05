from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AnalyticsTableItem(BaseModel):
    UserID: str
    Metrics: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class BulkAnalyticsTableResponse(BaseModel):
    data: List[AnalyticsTableItem]
