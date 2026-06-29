#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill="${1:-$repo_root/skills/ingest-wiki/SKILL.md}"

python3 - "$skill" <<'PY'
import sys
from pathlib import Path

skill = Path(sys.argv[1])
text = skill.read_text()

required = {
    "archive_heading": "5. Archive the approved source before page edits.",
    "draft_heading": "6. Draft approved page changes.",
    "archive_command": "Run `python3 scripts/archive-ingest-source.py <absolute-source-path>`",
    "final_stdout": "Use the helper's stdout as the final archived source path",
    "page_change_approval": "Ask for page-change approval before finalization.",
}

positions = {}
for name, needle in required.items():
    index = text.find(needle)
    if index == -1:
        raise SystemExit(f"Missing required ingest workflow text: {needle}")
    positions[name] = index

if not positions["archive_heading"] < positions["draft_heading"]:
    raise SystemExit("The source archive step must come before drafting page changes.")

if not positions["archive_command"] < positions["draft_heading"]:
    raise SystemExit("The archive helper command must run before page changes are drafted.")

if not positions["final_stdout"] < positions["draft_heading"]:
    raise SystemExit("The final archive path must be known before source links are inserted.")

finalization_start = text.find("8. Finalize only after approval.")
if finalization_start == -1:
    raise SystemExit("Missing finalization step.")
finalization = text[finalization_start:]
for forbidden in ("Move the source", "archive-ingest-source.py", "--archive-name"):
    if forbidden in finalization:
        raise SystemExit(f"Finalization must not perform source movement: {forbidden}")

print("ingest workflow order test passed")
PY
