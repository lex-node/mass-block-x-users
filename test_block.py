import io
from block import block_from_file

def test_block_from_text_stream():
    file_obj = io.StringIO("alice\nbob\n")
    result = block_from_file(file_obj, "id", "token")
    assert result == {"alice": "blocked", "bob": "blocked"}

def test_block_from_binary_stream():
    file_obj = io.BytesIO(b"alice\nbob\n")
    result = block_from_file(file_obj, "id", "token")
    assert result == {"alice": "blocked", "bob": "blocked"}
