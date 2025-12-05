from pydantic import BaseModel
from typing import Optional, List

class ContentCompletionItem(BaseModel):
    UserID: str
    CompletedContents: Optional[List[str]] = None
    CompletionRate: Optional[float] = None
    message: Optional[str] = None

class BulkContentCompletionResponse(BaseModel):
    data: List[ContentCompletionItem]
