# LLM Wiki Skills

## Purpose

LLM Wiki Skills is a small skills package for maintaining an Obsidian vault as an LLM wiki: raw source material stays immutable, while the vault root becomes a concise, linked synthesis layer that an LLM can maintain over time.

It also includes a supplemental podcast transcription skill. That skill is not part of the core wiki maintenance model, but it is useful for turning podcast audio into readable Markdown source material before placing it in `/raw/todo` for ingestion.

The pattern is inspired by Karpathy's LLM wiki idea: the user curates sources and asks questions, and the LLM turns durable ideas into short atomic wiki pages, keeps cross-links current, records activity, and consults raw sources only when source-level detail or verification is needed.

## Vault Model

The vault root is the wiki root. Existing top-level knowledge folders and standalone Markdown notes stay in place and remain normal Obsidian wiki pages.

- `/raw/todo`: intake queue for new source records that have not been ingested yet. Agents may read files here during ingest, but should not rewrite them.
- `/raw`: immutable archive for source records after approved ingest finalization. Agents may read archived sources, but should not edit, rename, or delete them.
- `/raw/assets`: attachments and images associated with raw sources.
- Root-level wiki pages and topic folders: the synthesis layer. Agents may create, update, split, merge, rename, or move wiki pages when the active workflow allows it.
- `/index.md`: content-oriented catalog of wiki pages and topic folders, updated after ingests or major reorganizations.
- `/log.md`: append-only chronological record of ingests, durable query edits, lint passes, and major maintenance actions.
- `/AGENTS.md`: vault-local operating manual for future LLM agent sessions.

Wiki pages should be atomic, concise Markdown notes that work well in Obsidian. New pages start with a 1-2 sentence executive summary, aim for under 300 words, stay under 500 words, and use Obsidian wikilinks for internal references and source links.

## Skills

- `init-wiki`: initialize an existing Obsidian vault as an LLM wiki while preserving existing root-level notes and folders.
- `ingest-wiki`: process one source from `/raw/todo` into concise atomic wiki pages, with approval before source archiving and page edits, then again before finalization.
- `query-wiki`: answer questions from `/index.md` and wiki pages first, consulting `/raw` only when verification or extra source detail is useful.
- `lint-wiki`: run a wiki health pass for contradictions, stale claims, missing links, data gaps, atomic-page issues, and outdated index entries.
- `transcribe-podcast-to-article`: transcribe podcast, interview, lecture, or long-form audio into article-style Markdown with headings, punctuation, filler cleanup, durable ASR caching, and no timestamp clutter.

## Install

Requirements: Node.js 18 or newer, plus an agent environment that supports the Skills CLI package layout.

Preview the skills available in this repository:

```bash
npx skills add shiyonghu/llm-wiki-skills --list --full-depth
```

Install one skill from the public repository:

```bash
npx skills add shiyonghu/llm-wiki-skills --skill init-wiki
npx skills add shiyonghu/llm-wiki-skills --skill ingest-wiki
npx skills add shiyonghu/llm-wiki-skills --skill query-wiki
npx skills add shiyonghu/llm-wiki-skills --skill lint-wiki
npx skills add shiyonghu/llm-wiki-skills --skill transcribe-podcast-to-article
```

Install all skills:

```bash
npx skills add shiyonghu/llm-wiki-skills --all
```

Restart Codex or your agent app after installation so the newly installed skill descriptions are loaded.

## Usage

Command-style phrasing is convenient:

```text
init-wiki /path/to/vault
ingest-wiki raw/todo/example-source.md
query-wiki What does this vault say about growth mindset?
lint-wiki
transcribe-podcast-to-article raw/todo/example-podcast.m4a
```

The command-style prefix is not required. Each skill description is written to trigger from natural language too, such as "set up this Obsidian vault as an LLM wiki", "ingest this transcript from raw/todo", "what do my notes say about growth mindset?", "run a health check on this wiki", or "transcribe this podcast audio into a Markdown article."

## Development

This repository uses a local pinned `skills` CLI from `package.json` and `package-lock.json` for repeatable development checks. Run the npm scripts instead of relying on a globally installed CLI:

```bash
npm run skills:install-local
npm run skills:list
npm run skills:use:init
npm run skills:use:ingest
npm run skills:use:query
npm run skills:use:lint
npm run skills:use:transcribe
npm run test:install-local
```

- `npm run skills:install-local`: overwrites the local Codex installs of `init-wiki`, `ingest-wiki`, `query-wiki`, `lint-wiki`, and `transcribe-podcast-to-article` from this checkout. Use it after changing any `SKILL.md`, bundled script/reference, or any file under `skills/shared`.
- `npm run skills:list`: lists all skills discovered in this repository. It should include `init-wiki`, `ingest-wiki`, `query-wiki`, `lint-wiki`, and `transcribe-podcast-to-article`.
- `npm run skills:use:init`: previews the `init-wiki` skill prompt.
- `npm run skills:use:ingest`: previews the `ingest-wiki` skill prompt.
- `npm run skills:use:query`: previews the `query-wiki` skill prompt.
- `npm run skills:use:lint`: previews the `lint-wiki` skill prompt.
- `npm run skills:use:transcribe`: previews the `transcribe-podcast-to-article` skill prompt.
- `npm run test:install-local`: verifies the local installer against a temporary Codex skills directory and confirms stale installed content is overwritten.

### Codex refresh helper

For local Codex development, this repository also supports a personal helper skill named `refresh-wiki-skills`. After that helper is installed in Codex, ask Codex to "refresh wiki skills" and it will run `npm run skills:install-local` from this checkout.

The refresh command treats this repository as the source of truth. It overwrites the four wiki skills plus the supplemental `transcribe-podcast-to-article` skill under `${CODEX_HOME:-~/.codex}/skills`. It copies `skills/shared/wiki-conventions.md` and `skills/shared/obsidian-markdown.md` into each wiki skill so bundled reference paths resolve during testing; the transcribe skill does not receive wiki shared references.

Restart Codex after refreshing local installs, especially when changing frontmatter descriptions or shared reference files.

Public user-facing install examples can still use `npx skills add ...`; local repository development should use the npm scripts above.

### Publishing checklist

Before publishing changes for other people to install:

1. Run `npm run skills:list` and confirm all five skills are discovered.
2. Run `npm run test:install-local` to verify the bundled references and scripts install cleanly.
3. Push `main` to `https://github.com/shiyonghu/llm-wiki-skills`.
4. Verify a clean GitHub install path with a temporary Codex home:

```bash
tmp="$(mktemp -d)"
CODEX_HOME="$tmp/codex" npx skills add shiyonghu/llm-wiki-skills --all --full-depth
```

## Compatibility

The skills are plain Markdown instructions with bundled references, so they are intended to work across agents that understand the Skills CLI package layout. They are designed for Obsidian vaults that use Markdown files, folders, wikilinks, and local attachments.

The skills should not modify `.obsidian` files unless the user explicitly asks. They also preserve `/raw` as an immutable source archive after approved ingest finalization.

## License

MIT. See `LICENSE`.
