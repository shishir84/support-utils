from typing import List

def validate_user_id(user_id: str) -> str:
    user_id = str(user_id).strip()
    if not user_id:
        raise ValueError("UserID cannot be empty")
    return user_id

def validate_user_ids(user_ids: List[str]) -> List[str]:
    return [validate_user_id(uid) for uid in user_ids]
