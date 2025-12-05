from typing import List
from .common_validators import validate_user_id, validate_user_ids

def validate_learning_hours_user_id(user_id: str) -> str:
    return validate_user_id(user_id)

def validate_learning_hours_user_ids(user_ids: List[str]) -> List[str]:
    return validate_user_ids(user_ids)
