# LLM Wiki Skills

## Purpose

LLM Wiki Skills is a small skills package for maintaining an Obsidian vault as an LLM wiki: raw source material stays immutable, while the vault root becomes a concise, linked synthesis layer that an LLM can maintain over time.

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
- `ingest-wiki`: process one source from `/raw/todo` into concise atomic wiki pages, with approval before page edits and again before finalization.
- `query-wiki`: answer questions from `/index.md` and wiki pages first, consulting `/raw` only when verification or extra source detail is useful.
- `lint-wiki`: run a wiki health pass for contradictions, stale claims, missing links, data gaps, atomic-page issues, and outdated index entries.

## Install

Install one skill from the public repository:

```bash
npx skills add <owner>/llm-wiki-skills --skill init-wiki
npx skills add <owner>/llm-wiki-skills --skill ingest-wiki
npx skills add <owner>/llm-wiki-skills --skill query-wiki
npx skills add <owner>/llm-wiki-skills --skill lint-wiki
```

Install all skills:

```bash
npx skills add <owner>/llm-wiki-skills --all
```

Replace `<owner>` with the GitHub owner that publishes this repository.

## Usage

Command-style phrasing is convenient:

```text
init-wiki /path/to/vault
ingest-wiki raw/todo/example-source.md
query-wiki What does this vault say about growth mindset?
lint-wiki
```

The command-style prefix is not required. Each skill description is written to trigger from natural language too, such as "set up this Obsidian vault as an LLM wiki", "ingest this transcript from raw/todo", "what do my notes say about growth mindset?", or "run a health check on this wiki".

## Development

This repository uses a local pinned `skills` CLI from `package.json` and `package-lock.json` for repeatable development checks. Run the npm scripts instead of relying on a globally installed CLI:

```bash
npm run skills:list
npm run skills:use:init
npm run skills:use:ingest
npm run skills:use:query
npm run skills:use:lint
```

- `npm run skills:list`: lists all skills discovered in this repository. It should include `init-wiki`, `ingest-wiki`, `query-wiki`, and `lint-wiki`.
- `npm run skills:use:init`: previews the `init-wiki` skill prompt.
- `npm run skills:use:ingest`: previews the `ingest-wiki` skill prompt.
- `npm run skills:use:query`: previews the `query-wiki` skill prompt.
- `npm run skills:use:lint`: previews the `lint-wiki` skill prompt.

Public user-facing install examples can still use `npx skills add ...`; local repository development should use the npm scripts above.

## Compatibility

The skills are plain Markdown instructions with bundled references, so they are intended to work across agents that understand the Skills CLI package layout. They are designed for Obsidian vaults that use Markdown files, folders, wikilinks, and local attachments.

The skills should not modify `.obsidian` files unless the user explicitly asks. They also preserve `/raw` as an immutable source archive after approved ingest finalization.

## License

MIT. See `LICENSE`.
