import requests
from datetime import datetime
from typing import Dict, Any, Optional
from config import HEADERS, MAX_REQUESTS, WINDOW_SECONDS

REQUEST_HISTORY = []  # timestamps


def limited_get(url: str, timeout: int = 10) -> requests.Response:
    """Rate-limited GET with NBA headers."""
    global REQUEST_HISTORY
    now = datetime.now().timestamp()
    REQUEST_HISTORY = [t for t in REQUEST_HISTORY if now - t < WINDOW_SECONDS]

    if len(REQUEST_HISTORY) >= MAX_REQUESTS:
        raise Exception("Rate limit reached")

    REQUEST_HISTORY.append(now)
    return requests.get(url, headers=HEADERS, timeout=timeout)


def safe_json(resp: requests.Response, log_prefix: str = "") -> Dict[str, Any]:
    """
    Parse JSON safely. If NBA returns AccessDenied XML/HTML, return {}.
    """
    try:
        return resp.json()
    except ValueError:
        if log_prefix:
            print(f"[{log_prefix}] Non-JSON response (status {resp.status_code}). First 300 chars:\n{resp.text[:300]}")
        return {}
