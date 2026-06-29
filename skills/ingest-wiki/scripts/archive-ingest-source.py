#!/usr/bin/env python3
"""Move an ingested source from raw/todo to raw with safety checks."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def find_vault_root(source: Path) -> Path:
    parts = source.parts
    for index in range(len(parts) - 2, -1, -1):
        if parts[index] == "raw" and parts[index + 1] == "todo":
            return Path(*parts[:index]) if index else Path(source.anchor)
    fail(f"Source must be inside a raw/todo tree: {source}")


def archive_source(source_arg: str, archive_name: str | None = None) -> Path:
    source = Path(source_arg).expanduser().resolve()
    if not source.exists():
        fail(f"Source does not exist: {source}")
    if not source.is_file():
        fail(f"Source is not a file: {source}")

    vault_root = find_vault_root(source)
    raw_dir = vault_root / "raw"
    todo_dir = raw_dir / "todo"

    try:
        source.relative_to(todo_dir)
    except ValueError:
        fail(f"Source must be inside {todo_dir}: {source}")

    target_name = archive_name or source.name
    if target_name != Path(target_name).name or target_name in {"", ".", ".."}:
        fail(f"Archive name must be a filename, not a path: {target_name}")

    archive = raw_dir / target_name
    if archive.exists():
        fail(f"Archive already exists: {archive}")

    raw_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(archive))

    if source.exists():
        fail(f"Move verification failed; source still exists: {source}")
    if not archive.is_file():
        fail(f"Move verification failed; archive missing: {archive}")

    return archive


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Archive one ingested source from raw/todo to raw."
    )
    parser.add_argument("source", help="Path to the source file under raw/todo")
    parser.add_argument(
        "--archive-name",
        help="User-approved filename to use in raw when the original name collides",
    )
    args = parser.parse_args()

    archive = archive_source(args.source, args.archive_name)
    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
