from pydantic import BaseModel
from typing import Optional, Dict, Any

class WorkProfileItem(BaseModel):
    UserID: str
    Profile: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class BulkWorkProfileResponse(BaseModel):
    data: list[WorkProfileItem]
