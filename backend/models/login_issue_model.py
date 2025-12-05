from pydantic import BaseModel
from typing import Optional, List

class LoginIssueItem(BaseModel):
    UserID: str
    Issues: Optional[List[str]] = None
    Status: Optional[str] = None
    message: Optional[str] = None

class BulkLoginIssueResponse(BaseModel):
    data: List[LoginIssueItem]
