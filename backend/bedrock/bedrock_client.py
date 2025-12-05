import requests
from core import settings


def call_bedrock_model(prompt: str, extra_payload: dict | None = None) -> dict:
    """
    Calls your API Gateway URL which triggers Lambda -> Bedrock.
    Assumes JSON payload => { "prompt": "...", ... } and JSON response.
    """
    if not settings.BEDROCK_API_URL:
        raise RuntimeError("BEDROCK_API_URL not configured")

    payload = {"prompt": prompt}
    if extra_payload:
        payload.update(extra_payload)

    headers = {
        "Content-Type": "application/json",
    }
    if settings.BEDROCK_API_KEY:
        headers["x-api-key"] = settings.BEDROCK_API_KEY

    resp = requests.post(settings.BEDROCK_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()
