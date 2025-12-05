from typing import List, Dict, Any
from core.config import DATA_DIR
from core.utils import load_json
from validators.content_completion_validator import (
    validate_content_completion_user_id,
    validate_content_completion_user_ids,
)

DATA = load_json(DATA_DIR / "content_completion.json")

def get_single(user_id: str) -> Dict[str, Any]:
    user_id = validate_content_completion_user_id(user_id)
    item = DATA.get(user_id)
    if not item:
        return {"UserID": user_id, "message": "No data found"}
    return item

def get_bulk(user_ids: List[str]) -> List[Dict[str, Any]]:
    user_ids = validate_content_completion_user_ids(user_ids)
    return [get_single(uid) for uid in user_ids]
