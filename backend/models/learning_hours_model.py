from pydantic import BaseModel
from typing import Optional, List

class LearningHoursItem(BaseModel):
    UserID: str
    TotalHours: Optional[float] = None
    Breakdown: Optional[List[str]] = None
    message: Optional[str] = None

class BulkLearningHoursResponse(BaseModel):
    data: List[LearningHoursItem]
