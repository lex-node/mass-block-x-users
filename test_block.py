import io
from block import block_from_file, block_sol_shills, SOL_SHILLS, BLOCK_URL

def test_block_from_text_stream():
    file_obj = io.StringIO("alice\nbob\n")
    result = block_from_file(file_obj, "id", "token")
    assert result == {"alice": "blocked", "bob": "blocked"}
    assert BLOCK_URL == "https://api.twitter.com/1.1/blocks/create.json"

def test_block_from_binary_stream():
    file_obj = io.BytesIO(b"alice\nbob\n")
    result = block_from_file(file_obj, "id", "token")
    assert result == {"alice": "blocked", "bob": "blocked"}


def test_block_sol_shills():
    result = block_sol_shills("id", "token")
    assert set(result.keys()) == set(SOL_SHILLS)
    assert all(status == "blocked" for status in result.values())
