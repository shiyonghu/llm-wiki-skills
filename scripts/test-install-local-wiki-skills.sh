#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp_root="$(mktemp -d)"
trap 'rm -rf "$tmp_root"' EXIT

dest_root="$tmp_root/codex-skills"
mkdir -p "$dest_root/init-wiki"
printf 'stale install\n' > "$dest_root/init-wiki/SKILL.md"

"$repo_root/scripts/install-local-wiki-skills.sh" --dest "$dest_root"

for skill in init-wiki ingest-wiki lint-wiki query-wiki; do
  test -f "$dest_root/$skill/SKILL.md"
  test -f "$dest_root/$skill/skills/shared/wiki-conventions.md"
  test -f "$dest_root/$skill/skills/shared/obsidian-markdown.md"
  cmp "$repo_root/skills/$skill/SKILL.md" "$dest_root/$skill/SKILL.md"
  cmp "$repo_root/skills/shared/wiki-conventions.md" "$dest_root/$skill/skills/shared/wiki-conventions.md"
  cmp "$repo_root/skills/shared/obsidian-markdown.md" "$dest_root/$skill/skills/shared/obsidian-markdown.md"
done

test -f "$dest_root/ingest-wiki/scripts/archive-ingest-source.py"
cmp "$repo_root/skills/ingest-wiki/scripts/archive-ingest-source.py" "$dest_root/ingest-wiki/scripts/archive-ingest-source.py"

if grep -q 'stale install' "$dest_root/init-wiki/SKILL.md"; then
  echo "stale installed content was not overwritten" >&2
  exit 1
fi

echo "install-local-wiki-skills test passed"
