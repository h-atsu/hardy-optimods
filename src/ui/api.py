import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


def call_api(
    method: str,
    path: str,
    *,
    base_url: str,
    payload: dict[str, Any] | None = None,
    timeout: float = 10.0,
) -> Any:
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(
        url,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8")
        raise RuntimeError(f"API returned {error.code}: {details}") from error
    except URLError as error:
        raise RuntimeError(f"Could not connect to API: {error.reason}") from error
    except TimeoutError as error:
        raise RuntimeError("API request timed out") from error


def create_bmi_task(base_url: str, weight: float, height: float) -> dict[str, Any]:
    return call_api(
        "POST",
        "/bmi",
        base_url=base_url,
        payload={"weight": weight, "height": height},
    )


def fetch_bmi_task(base_url: str, task_id: str) -> dict[str, Any]:
    return call_api("GET", f"/bmi/{task_id}", base_url=base_url)


def fetch_bmi_tasks(base_url: str) -> list[dict[str, Any]]:
    return call_api("GET", "/bmi", base_url=base_url)
