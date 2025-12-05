import requests
from typing import Optional

API_BASE = "http://localhost:8000"  # adjust if needed

def login_api(username: str, password: str) -> Optional[str]:
    url = f"{API_BASE}/auth/login"
    resp = requests.post(url, json={"username": username, "password": password})
    if resp.status_code == 200:
        return resp.json().get("token")
    return None

def get_single(feature_slug: str, user_id: str):
    url = f"{API_BASE}/{feature_slug}/single/{user_id}"
    resp = requests.get(url)
    if resp.ok:
        return resp.json()
    return {"error": resp.text}

def get_bulk(feature_slug: str, uploaded_file):
    """
    uploaded_file: Streamlit UploadedFile
    """
    if uploaded_file is None:
        return {"data": []}

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
    }
    url = f"{API_BASE}/{feature_slug}/bulk"
    resp = requests.post(url, files=files)
    if resp.ok:
        return resp.json()
    return {"error": resp.text}
