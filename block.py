from typing import Dict, Iterable
from io import StringIO
from pathlib import Path
import os
import time

import requests

BLOCK_URL = "https://api.twitter.com/1.1/blocks/create.json"
SOL_SHILLS_PATH = Path(__file__).with_name("sol_shills.txt")
try:
    with SOL_SHILLS_PATH.open() as f:
        SOL_SHILLS = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    SOL_SHILLS = []


def block_from_file(
    file_obj: Iterable[str],
    source_id: str | None = None,
    token: str | None = None,
    *,
    ct0: str | None = None,
    bearer_token: str | None = None,
    max_retries: int = 3,
    backoff: float = 1.0,
) -> Dict[str, str]:
    """Block users listed in ``file_obj`` using the X web API.

    Parameters
    ----------
    file_obj:
        Iterable yielding usernames, one per line. Each line may be ``str`` or ``bytes``.
    source_id:
        Numeric X user id of the account performing the block. If ``None``, value is
        read from the ``SOURCE_ID`` environment variable.
    token:
        ``auth_token`` cookie from the user's X session. If ``None``, value is read
        from the ``AUTH_TOKEN`` environment variable.
    ct0:
        ``ct0`` cookie paired with the ``X-Csrf-Token`` header. If ``None``, value is
        read from the ``CT0`` environment variable.
    bearer_token:
        OAuth2 bearer token used in the ``Authorization`` header. If ``None``, value
        is read from the ``BEARER_TOKEN`` environment variable.
    max_retries:
        Number of attempts for a request when rate limited (HTTP 429).
    backoff:
        Base time in seconds to wait between retry attempts when rate limited.

    Returns
    -------
    dict
        Mapping of the original username lines to ``"blocked"`` or an error message.

    Notes
    -----
    The real X API requires many headers and cookies. This function performs a minimal
    request using ``requests`` so that it can be easily mocked during tests. It posts
    to ``https://api.twitter.com/1.1/blocks/create.json`` for each username. Specific
    HTTP statuses are reported with clearer messages and HTTP 429 responses are
    retried.
    """

    source_id = source_id or os.getenv("SOURCE_ID", "")
    token = token or os.getenv("AUTH_TOKEN", "")
    ct0 = ct0 or os.getenv("CT0", "")
    bearer_token = bearer_token or os.getenv("BEARER_TOKEN", "")
    results: Dict[str, str] = {}
    headers = {
        "User-Agent": "mass-block-x-users",
        "Authorization": f"Bearer {bearer_token}",
        "X-Csrf-Token": ct0,
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    cookies = {"auth_token": token, "ct0": ct0}

    for line in file_obj:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        raw_username = line.strip()
        if not raw_username:
            continue

        screen_name = raw_username.lstrip("@")
        payload = {"screen_name": screen_name, "source_id": source_id}

        attempts = 0
        while True:
            try:
                response = requests.post(
                    BLOCK_URL, data=payload, headers=headers, cookies=cookies, timeout=10
                )
            except requests.RequestException as exc:  # pragma: no cover - network
                results[raw_username] = f"error: {exc}"
                break

            if response.status_code == 200:
                results[raw_username] = "blocked"
                break
            if response.status_code in {401, 403}:
                results[raw_username] = "unauthorized"
                break
            if response.status_code == 429:
                attempts += 1
                if attempts >= max_retries:
                    results[raw_username] = "rate limited"
                    break
                time.sleep(backoff * attempts)
                continue
            results[raw_username] = f"error: {response.status_code}"
            break

    return results


def block_sol_shills(
    source_id: str | None = None,
    token: str | None = None,
    *,
    ct0: str | None = None,
    bearer_token: str | None = None,
) -> Dict[str, str]:
    """Block the preset list of SOL shill usernames."""

    buffer = StringIO("\n".join(SOL_SHILLS))
    return block_from_file(
        buffer,
        source_id,
        token,
        ct0=ct0,
        bearer_token=bearer_token,
    )
