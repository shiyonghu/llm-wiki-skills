#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script="$repo_root/skills/ingest-wiki/scripts/archive-ingest-source.py"
tmp_root="$(mktemp -d)"
trap 'rm -rf "$tmp_root"' EXIT

vault="$(cd "$tmp_root" && pwd -P)/vault"
mkdir -p "$vault/raw/todo" "$vault/raw"
printf 'source body\n' > "$vault/raw/todo/example.md"

archive_path="$(python3 "$script" "$vault/raw/todo/example.md")"

test "$archive_path" = "$vault/raw/example.md"
test ! -e "$vault/raw/todo/example.md"
test -f "$vault/raw/example.md"
grep -q 'source body' "$vault/raw/example.md"

printf 'new body\n' > "$vault/raw/todo/collision.md"
printf 'old body\n' > "$vault/raw/collision.md"
if python3 "$script" "$vault/raw/todo/collision.md" >"$tmp_root/collision.out" 2>"$tmp_root/collision.err"; then
  echo "expected collision to fail" >&2
  exit 1
fi
grep -q 'Archive already exists' "$tmp_root/collision.err"
test -f "$vault/raw/todo/collision.md"
grep -q 'old body' "$vault/raw/collision.md"

renamed_archive="$(python3 "$script" "$vault/raw/todo/collision.md" --archive-name collision-2.md)"
test "$renamed_archive" = "$vault/raw/collision-2.md"
test ! -e "$vault/raw/todo/collision.md"
grep -q 'new body' "$vault/raw/collision-2.md"
grep -q 'old body' "$vault/raw/collision.md"

mkdir -p "$vault/notes"
printf 'note body\n' > "$vault/notes/not-raw.md"
if python3 "$script" "$vault/notes/not-raw.md" >"$tmp_root/invalid.out" 2>"$tmp_root/invalid.err"; then
  echo "expected non-raw/todo source to fail" >&2
  exit 1
fi
grep -q 'Source must be inside' "$tmp_root/invalid.err"
test -f "$vault/notes/not-raw.md"

echo "archive-ingest-source test passed"
