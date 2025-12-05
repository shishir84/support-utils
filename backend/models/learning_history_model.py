from pydantic import BaseModel
from typing import List, Optional

class LearningHistoryItem(BaseModel):
    UserID: str
    LearningHistory: Optional[List[str]] = None
    message: Optional[str] = None

class BulkLearningHistoryResponse(BaseModel):
    data: List[LearningHistoryItem]
