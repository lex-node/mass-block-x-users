import re
import time
from unittest.mock import patch

import pytest

import web_app


@pytest.fixture
def client():
    web_app.app.config['TESTING'] = True
    with web_app.app.test_client() as client:
        yield client


def test_block_sol_shills_background(client):
    fake_users = ['user1', 'user2']

    def fake_block(
        file_obj,
        source_id,
        token,
        *,
        ct0=None,
        bearer_token=None,
    ):
        username = next(iter(file_obj))
        assert ct0 == 'c'
        assert bearer_token == 'b'
        return {username: 'blocked'}

    with patch.object(web_app, 'SOL_SHILLS', fake_users), \
         patch.object(web_app, 'block_from_file', side_effect=fake_block):
        resp = client.post(
            '/block-sol-shills',
            data={'source_id': '1', 'token': 't', 'ct0': 'c', 'bearer_token': 'b'},
        )
        assert resp.status_code == 200
        match = re.search(r'Task ID: ([\w-]+)', resp.data.decode())
        assert match
        task_id = match.group(1)
        status_url = f'/tasks/{task_id}'
        for _ in range(20):
            status_resp = client.get(status_url)
            data = status_resp.get_json()
            if data['status'] == 'finished':
                break
            time.sleep(0.1)
        assert data['status'] == 'finished'
        assert data['result'] == {u: 'blocked' for u in fake_users}
