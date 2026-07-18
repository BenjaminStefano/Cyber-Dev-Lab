from __future__ import annotations

import json
from pathlib import Path
from typing import TypeAlias

from monitor.hashing import calculate_sha256


Baseline: TypeAlias = dict[str, str]

IGNORED_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "baseline.json",
}


def should_ignore(path: Path) -> bool:
    """Return True when a path belongs to an ignored directory or file."""
    return any(part in IGNORED_NAMES for part in path.parts)


def build_baseline(directory: Path) -> Baseline:
    """Create a mapping between relative file paths and SHA-256 hashes."""
    baseline: Baseline = {}

    for file_path in directory.rglob("*"):
        if not file_path.is_file() or should_ignore(file_path):
            continue

        relative_path = file_path.relative_to(directory).as_posix()

        try:
            baseline[relative_path] = calculate_sha256(file_path)
        except (PermissionError, OSError):
            continue

    return baseline


def save_baseline(baseline: Baseline, output_path: Path) -> None:
    """Save a baseline as formatted JSON."""
    output_path.write_text(
        json.dumps(baseline, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def load_baseline(input_path: Path) -> Baseline:
    """Load a baseline from a JSON file."""
    try:
        content = input_path.read_text(encoding="utf-8")
        data = json.loads(content)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            "No existe una línea base. Ejecuta primero el comando init."
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError(
            "El archivo de línea base está dañado o no contiene JSON válido."
        ) from error

    if not isinstance(data, dict):
        raise ValueError("La línea base no tiene el formato esperado.")

    return {
        str(file_path): str(file_hash)
        for file_path, file_hash in data.items()
    }