---
name: init-wiki
description: Initialize an existing Obsidian vault as an LLM wiki. Use this skill whenever the user says `init-wiki`, asks to initialize or set up a vault as an LLM-maintained wiki, wants to prepare an existing Obsidian vault for Karpathy-style LLM wiki workflows, or asks for raw/todo/index/log/AGENTS operating files to be created while preserving existing notes.
---

# init-wiki

Initialize an existing Obsidian vault so future LLM agent sessions can maintain it as a wiki with a stable raw source layer, concise linked synthesis pages, and local operating rules.

## When To Use

Use this skill when the user wants to initialize an existing Obsidian vault as an LLM wiki, including command-style requests such as:

```text
init-wiki /path/to/vault
```

Also use it for natural language requests such as "set up this Obsidian vault as an LLM wiki", "prepare my notes vault for an LLM wiki workflow", or "create the raw folder, index, log, and AGENTS instructions for this vault."

This skill is for initialization only. Preserve existing folders and notes in place. Do not reorganize wiki content, ingest sources, answer research questions, or run lint passes unless the user explicitly asks for those workflows after initialization.

## Required Reading

Before editing the vault, read these bundled references:

- `skills/shared/wiki-conventions.md` for the vault layout, ownership rules, page conventions, and workflow boundaries.
- `skills/shared/obsidian-markdown.md` for Obsidian wikilinks, raw source links, and asset embeds.

When the target vault already contains `/AGENTS.md`, read it before making changes. Treat the local file as the vault-specific operating manual and preserve its guidance. If it conflicts with this initialization skill, pause and ask the user how to proceed.

## Workflow

1. Resolve the vault root.
   - If the user supplied a path, expand it, resolve it to an absolute path, and verify it is an existing directory.
   - If the user did not supply a path, ask whether to use the current folder as the vault root before editing anything.
   - If the resolved path is missing or is not a directory, stop and ask for a valid Obsidian vault path.

2. Inspect before editing.
   - Read `/AGENTS.md` when present.
   - List the vault root and identify existing root-level folders and standalone Markdown notes.
   - Preserve existing folders and notes in place.
   - Avoid editing `.obsidian` files or Obsidian plugin/workspace settings unless the user explicitly asks.

3. Create the raw source structure if missing.
   - Create `/raw`.
   - Create `/raw/todo`.
   - Create `/raw/assets`.
   - Do not move existing notes or sources into these folders during initialization unless the user separately asks.

4. Create `/index.md` if missing.
   - Build a concise content-oriented index from existing root-level knowledge folders and standalone Markdown notes.
   - Exclude `.obsidian`, hidden files, `/raw`, `/docs`, `/AGENTS.md`, `/index.md`, and `/log.md` from the topic catalog.
   - Use Obsidian wikilinks for standalone Markdown notes and clear section headings for folders.
   - If there is not enough content to catalog yet, create a short placeholder that explains the index will be maintained as pages are added.
   - If `/index.md` already exists, leave it unchanged.

5. Create `/log.md` if missing.
   - Add an initial setup entry using the current date.
   - Keep the log append-only in future workflows.
   - If `/log.md` already exists, leave it unchanged.

   Suggested initial entry:

   ```markdown
   # Log

   ## [YYYY-MM-DD] init | LLM wiki setup

   - Created: [[raw]], [[raw/todo]], [[raw/assets]], [[index]], [[AGENTS]]
   - Notes: Initialized this vault for LLM wiki workflows while preserving existing folders and notes in place.
   ```

6. Create `/AGENTS.md` if missing.
   - Base it on the operating rules below.
   - Keep it practical and vault-local so future agents can read it quickly before ingest, query, lint, or maintenance work.
   - If `/AGENTS.md` already exists, leave it unchanged unless the user explicitly asks to update it.

   Operating rules to include:

   ```markdown
   # AGENTS

   This Obsidian vault is maintained as an LLM wiki. The vault root is the wiki root.

   ## Layout

   - `/raw`: immutable archive for source records after approved ingest finalization.
   - `/raw/todo`: intake queue for new source records waiting to be ingested.
   - `/raw/assets`: local attachments and images associated with raw sources.
   - `/index.md`: content-oriented catalog of wiki pages, organized by topic.
   - `/log.md`: append-only chronological record of ingests, durable query edits, lint passes, and major maintenance.
   - `/AGENTS.md`: operating manual for future LLM agent sessions.

   Existing root-level folders and standalone Markdown notes are wiki content. Preserve them in place.

   ## Ownership Rules

   Read files in `/raw/todo` during ingest, but do not rewrite their contents. After a source is moved from `/raw/todo` to `/raw` through approved ingest briefing, treat `/raw` as immutable: do not edit, rename, or delete archived source files.

   The vault root is the synthesis layer. Agents may create, rewrite, split, merge, rename, and reorganize wiki content pages and topic folders at the root when the active workflow allows it. Preserve special system folders such as `/raw`, `/docs`, and `.obsidian`.

   Do not modify `.obsidian` plugin files or workspace settings unless the user explicitly asks.

   ## Page Conventions

   Write normal Markdown that works well in Obsidian. Each wiki page should be atomic: about one idea and complete enough to stand on its own. Start new pages with a 1-2 sentence executive summary.

   Keep pages concise. Aim for under 300 words and keep every page under 500 words. If a page wants to grow beyond that, split it into smaller linked pages.

   Use Obsidian wikilinks for internal references. Prefer short links when unique and vault-root paths when the path clarifies the target, especially for raw source links.

   ## Workflow Boundaries

   For ingest work, process one source from `/raw/todo` at a time, prepare a briefing, wait for approval before moving the source to `/raw` and editing pages, then wait for final approval before updating `/index.md` and `/log.md`.

   For query work, read `/index.md` first, search wiki pages before raw sources, and modify files only when the user wants durable synthesis captured in the vault.

   For lint work, scan wiki content while excluding `.obsidian`, `/docs`, `/raw`, hidden files, and system files. Present uncertain findings as recommendations and apply fixes after user approval.
   ```

7. Summarize initialization.
   - Tell the user which files and folders were created and which existing operating files were preserved.
   - Mention that existing folders and notes were left in place.
   - Mention if `.obsidian` was present and left untouched.

## Verification

After initialization, verify the vault state before reporting completion:

1. Confirm the raw folders exist, for example:

   ```bash
   find <vault-path> -maxdepth 2 -type d
   ```

   Check that `<vault-path>/raw`, `<vault-path>/raw/todo`, and `<vault-path>/raw/assets` are present.

2. Confirm the operating files exist:

   ```bash
   test -f <vault-path>/index.md && test -f <vault-path>/log.md && test -f <vault-path>/AGENTS.md
   ```

3. Confirm existing root-level knowledge folders and standalone Markdown notes were preserved in place.

4. Confirm `.obsidian` files were not edited unless the user explicitly asked for that.

If any verification step fails, fix the initialization if it is safe to do so. If fixing would require moving or rewriting existing content, stop and ask the user for direction.
