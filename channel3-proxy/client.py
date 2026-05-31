import httpx
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = "https://api.trychannel3.com"

_client: httpx.AsyncClient | None = None


def _get_api_key() -> str:
    key = os.getenv("CHANNEL3_API_KEY")
    if not key:
        raise RuntimeError("CHANNEL3_API_KEY is not set in your .env file")
    return key


def _get_headers() -> dict:
    return {
        "x-api-key": _get_api_key(),
        "Content-Type": "application/json",
    }


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=httpx.Timeout(20.0, connect=5.0),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
    return _client


async def close_client():
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


def _handle_error(response: httpx.Response):
    try:
        detail = response.json()
    except Exception:
        detail = response.text

    status = response.status_code

    if status == 401:
        raise PermissionError(f"Auth failed — check your API key. Detail: {detail}")
    elif status == 402:
        raise PermissionError(f"Credits exhausted. Detail: {detail}")
    elif status == 422:
        raise ValueError(f"Invalid request. Detail: {detail}")
    elif status == 404:
        raise LookupError(f"Not found. Detail: {detail}")
    elif status >= 500:
        raise ConnectionError(f"Channel3 server error ({status}). Detail: {detail}")
    else:
        raise httpx.HTTPStatusError(
            f"Unexpected status {status}",
            request=response.request,
            response=response,
        )


async def c3_post(path: str, body: dict) -> dict:
    client = await get_client()
    logger.debug("POST %s | body=%s", path, body)
    try:
        response = await client.post(path, json=body, headers=_get_headers())
        if response.is_error:
            _handle_error(response)
        return response.json()
    except (PermissionError, ValueError, LookupError, ConnectionError):
        raise
    except httpx.TimeoutException:
        raise TimeoutError(f"Request timed out: POST {path}")
    except httpx.RequestError as e:
        raise ConnectionError(f"Network error: {e}")


async def c3_get(path: str, params: dict | None = None) -> dict:
    client = await get_client()
    logger.debug("GET %s | params=%s", path, params)
    try:
        response = await client.get(path, params=params, headers=_get_headers())
        if response.is_error:
            _handle_error(response)
        return response.json()
    except (PermissionError, ValueError, LookupError, ConnectionError):
        raise
    except httpx.TimeoutException:
        raise TimeoutError(f"Request timed out: GET {path}")
    except httpx.RequestError as e:
        raise ConnectionError(f"Network error: {e}")
