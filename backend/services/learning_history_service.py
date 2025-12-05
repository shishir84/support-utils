from typing import List, Dict, Any
from core import settings
from core.config import DATA_DIR
from core.utils import load_json
from validators.learning_history_validator import (
    validate_learning_history_user_id,
    validate_learning_history_user_ids,
)
from db.rds_client import fetch_all  # real RDS


# Dummy data still loaded from JSON
DATA = load_json(DATA_DIR / "learning_history.json")


def _get_single_dummy(user_id: str) -> Dict[str, Any]:
    item = DATA.get(user_id)
    if not item:
        return {"UserID": user_id, "message": "No data found"}
    return item


def _get_single_rds(user_id: str) -> Dict[str, Any]:
    # Adjust query to your real schema
    query = """
        SELECT user_id, course_name
        FROM learning_history
        WHERE user_id = %s
        ORDER BY completion_date DESC
    """
    rows = fetch_all(query, (user_id,))
    if not rows:
        return {"UserID": user_id, "message": "No data found"}

    courses = [r["course_name"] for r in rows]
    return {
        "UserID": user_id,
        "LearningHistory": courses,
    }


def get_single(user_id: str) -> Dict[str, Any]:
    user_id = validate_learning_history_user_id(user_id)

    if settings.USE_DUMMY_DATA:
        return _get_single_dummy(user_id)
    else:
        return _get_single_rds(user_id)


def get_bulk(user_ids: List[str]) -> List[Dict[str, Any]]:
    user_ids = validate_learning_history_user_ids(user_ids)
    return [get_single(uid) for uid in user_ids]
