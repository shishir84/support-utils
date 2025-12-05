from typing import List, Dict, Any
from core import settings
from core.config import DATA_DIR
from core.utils import load_json
from validators.work_profile_validator import (
    validate_work_profile_user_id,
    validate_work_profile_user_ids,
)
from db.neo4j_client import run_query

DATA = load_json(DATA_DIR / "work_profile.json")


def _get_single_dummy(user_id: str) -> Dict[str, Any]:
    item = DATA.get(user_id)
    if not item:
        return {"UserID": user_id, "message": "No data found"}
    return item


def _get_single_neo4j(user_id: str) -> Dict[str, Any]:
    q = """
    MATCH (u:User {id: $user_id})-[:HAS_PROFILE]->(p:Profile)
    RETURN u.id as UserID, p as Profile
    """
    results = run_query(q, {"user_id": user_id})
    if not results:
        return {"UserID": user_id, "message": "No profile found"}

    record = results[0]
    profile_node = record["Profile"]
    # neo4j Node -> dict
    profile_dict = dict(profile_node)

    return {
        "UserID": record["UserID"],
        "Profile": profile_dict,
    }


def get_single(user_id: str) -> Dict[str, Any]:
    user_id = validate_work_profile_user_id(user_id)

    if settings.USE_DUMMY_DATA:
        return _get_single_dummy(user_id)
    else:
        return _get_single_neo4j(user_id)


def get_bulk(user_ids: List[str]) -> List[Dict[str, Any]]:
    user_ids = validate_work_profile_user_ids(user_ids)
    return [get_single(uid) for uid in user_ids]
