from __future__ import annotations

import hashlib
from pathlib import Path


BUFFER_SIZE = 65_536


def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 digest of a file."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(BUFFER_SIZE):
            sha256.update(chunk)

    return sha256.hexdigest()