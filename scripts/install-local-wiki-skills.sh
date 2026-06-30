#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest_root="${CODEX_HOME:-$HOME/.codex}/skills"
skills=(init-wiki ingest-wiki lint-wiki query-wiki transcribe-podcast-to-article)
wiki_skills=(init-wiki ingest-wiki lint-wiki query-wiki)

usage() {
  cat <<'USAGE'
Usage: scripts/install-local-wiki-skills.sh [--dest PATH]

Overwrites the local Codex installs for init-wiki, ingest-wiki, lint-wiki,
query-wiki, and transcribe-podcast-to-article from this repository's skills/
directory.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      if [[ $# -lt 2 ]]; then
        echo "--dest requires a path" >&2
        exit 2
      fi
      dest_root="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for skill in "${skills[@]}"; do
  if [[ ! -f "$repo_root/skills/$skill/SKILL.md" ]]; then
    echo "Missing source skill: $repo_root/skills/$skill/SKILL.md" >&2
    exit 1
  fi
done

for ref in wiki-conventions.md obsidian-markdown.md; do
  if [[ ! -f "$repo_root/skills/shared/$ref" ]]; then
    echo "Missing shared reference: $repo_root/skills/shared/$ref" >&2
    exit 1
  fi
done

mkdir -p "$dest_root"

for skill in "${skills[@]}"; do
  dest="$dest_root/$skill"
  rm -rf "$dest"
  mkdir -p "$dest"
  cp -R "$repo_root/skills/$skill"/. "$dest"/
  for wiki_skill in "${wiki_skills[@]}"; do
    if [[ "$skill" == "$wiki_skill" ]]; then
      mkdir -p "$dest/skills/shared"
      cp "$repo_root/skills/shared/wiki-conventions.md" "$dest/skills/shared/"
      cp "$repo_root/skills/shared/obsidian-markdown.md" "$dest/skills/shared/"
      break
    fi
  done
  echo "installed $skill -> $dest"
done

echo "Restart Codex to pick up refreshed skill definitions."
