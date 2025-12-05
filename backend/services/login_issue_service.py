from typing import List, Dict, Any
from core import settings
from core.config import DATA_DIR
from core.utils import load_json
from validators.login_issue_validator import (
    validate_login_issue_user_id,
    validate_login_issue_user_ids,
)
from db.es_client import search_index

DATA = load_json(DATA_DIR / "login_issue.json")


def _get_single_dummy(user_id: str) -> Dict[str, Any]:
    item = DATA.get(user_id)
    if not item:
        return {"UserID": user_id, "message": "No data found"}
    return item


def _get_single_es(user_id: str) -> Dict[str, Any]:
    body = {
        "query": {
            "term": {"user_id.keyword": user_id}
        }
    }
    res = search_index("login_issues", body)
    hits = res["hits"]["hits"]

    if not hits:
        return {"UserID": user_id, "message": "No login issues found"}

    issues = [h["_source"]["issue"] for h in hits]
    status = hits[0]["_source"].get("status", "Unknown")

    return {
        "UserID": user_id,
        "Issues": issues,
        "Status": status,
    }


def get_single(user_id: str) -> Dict[str, Any]:
    user_id = validate_login_issue_user_id(user_id)

    if settings.USE_DUMMY_DATA:
        return _get_single_dummy(user_id)
    else:
        return _get_single_es(user_id)


def get_bulk(user_ids: List[str]) -> List[Dict[str, Any]]:
    user_ids = validate_login_issue_user_ids(user_ids)
    return [get_single(uid) for uid in user_ids]
