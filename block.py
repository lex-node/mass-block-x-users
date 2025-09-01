from typing import Dict, Iterable
from io import StringIO


# TODO: Fill this list with the usernames from the provided images
SOL_SHILLS = [
    # Example placeholders
    "exampleuser1",
    "exampleuser2",
]


def block_from_file(
    file_obj: Iterable[str], source_id: str, token: str
) -> Dict[str, str]:
    """Block users listed in ``file_obj``.

    This stub function reads each line from the provided file-like object and
    returns a mapping of username to a message indicating the user was blocked.
    The ``file_obj`` may yield either strings or bytes; bytes are decoded using
    UTF-8. In a real implementation this would call the X API using
    ``source_id`` and ``token``.
    """
    results: Dict[str, str] = {}
    for line in file_obj:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        username = line.strip()
        if not username:
            continue
        # Placeholder: real blocking logic would go here
        results[username] = "blocked"
    return results


def block_sol_shills(source_id: str, token: str) -> Dict[str, str]:
    """Block the preset list of SOL shill usernames."""

    buffer = StringIO("\n".join(SOL_SHILLS))
    return block_from_file(buffer, source_id, token)
