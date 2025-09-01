"""Tests for blocking logic.

These tests mock out the ``requests.post`` call used by ``block_from_file`` so
no real network activity occurs.  They assert that the correct API endpoint is
called for each username and that the results mapping reports success.
"""

import io

from typing import List, Dict

import block


class DummyResponse:
    """Simple stand-in for :class:`requests.Response`."""

    def __init__(self, status_code: int = 200):
        self.status_code = status_code


def make_fake_post(collected: List[Dict]):
    """Return a ``requests.post`` replacement that records calls."""

    def fake_post(url, data=None, headers=None, cookies=None, timeout=None):
        collected.append(
            {
                "url": url,
                "data": data,
                "headers": headers,
                "cookies": cookies,
                "timeout": timeout,
            }
        )
        return DummyResponse()

    return fake_post


def test_block_from_text_stream(monkeypatch):
    calls: List[Dict] = []
    monkeypatch.setattr(block.requests, "post", make_fake_post(calls))


    file_obj = io.StringIO("alice\nbob\n")
    result = block.block_from_file(
        file_obj,
        "id",
        "token",
        ct0="csrf",
        bearer_token="bearer",
    )

    assert result == {"alice": "blocked", "bob": "blocked"}

    assert len(calls) == 2
    for call in calls:
        assert call["url"] == "https://api.twitter.com/1.1/blocks/create.json"
        assert call["cookies"] == {"auth_token": "token", "ct0": "csrf"}
        assert call["headers"]["Authorization"] == "Bearer bearer"
        assert call["headers"]["X-Csrf-Token"] == "csrf"
        assert call["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert call["data"]["source_id"] == "id"
        assert call["data"]["screen_name"] in {"alice", "bob"}


def test_block_from_binary_stream(monkeypatch):
    calls: List[Dict] = []
    monkeypatch.setattr(block.requests, "post", make_fake_post(calls))


    file_obj = io.BytesIO(b"alice\nbob\n")
    result = block.block_from_file(
        file_obj,
        "id",
        "token",
        ct0="csrf",
        bearer_token="bearer",
    )

    assert result == {"alice": "blocked", "bob": "blocked"}
    assert len(calls) == 2
    for call in calls:
        assert call["data"]["screen_name"] in {"alice", "bob"}


def test_block_sol_shills(monkeypatch):
    calls: List[Dict] = []
    monkeypatch.setattr(block.requests, "post", make_fake_post(calls))

    result = block.block_sol_shills("id", "token", ct0="csrf", bearer_token="bearer")

    assert set(result.keys()) == set(block.SOL_SHILLS)
    assert all(status == "blocked" for status in result.values())
    assert len(calls) == len(block.SOL_SHILLS)
    # Ensure usernames sent to the API are normalized without the '@' prefix.
    sent_usernames = {call["data"]["screen_name"] for call in calls}
    assert sent_usernames == {name.lstrip("@") for name in block.SOL_SHILLS}


def test_auth_error(monkeypatch):
    def fake_post(url, data=None, headers=None, cookies=None, timeout=None):
        return DummyResponse(401)

    monkeypatch.setattr(block.requests, "post", fake_post)
    file_obj = io.StringIO("alice\n")
    result = block.block_from_file(
        file_obj,
        "id",
        "token",
        ct0="csrf",
        bearer_token="bearer",
    )
    assert result == {"alice": "unauthorized"}


def test_rate_limit_retry(monkeypatch):
    responses = [DummyResponse(429), DummyResponse(200)]

    def fake_post(url, data=None, headers=None, cookies=None, timeout=None):
        return responses.pop(0)

    monkeypatch.setattr(block.requests, "post", fake_post)
    monkeypatch.setattr(block.time, "sleep", lambda s: None)
    file_obj = io.StringIO("alice\n")
    result = block.block_from_file(
        file_obj,
        "id",
        "token",
        ct0="csrf",
        bearer_token="bearer",
        max_retries=2,
        backoff=0,
    )
    assert result == {"alice": "blocked"}


def test_rate_limit_gives_up(monkeypatch):
    def fake_post(url, data=None, headers=None, cookies=None, timeout=None):
        return DummyResponse(429)

    monkeypatch.setattr(block.requests, "post", fake_post)
    monkeypatch.setattr(block.time, "sleep", lambda s: None)
    file_obj = io.StringIO("alice\n")
    result = block.block_from_file(
        file_obj,
        "id",
        "token",
        ct0="csrf",
        bearer_token="bearer",
        max_retries=2,
        backoff=0,
    )
    assert result == {"alice": "rate limited"}

