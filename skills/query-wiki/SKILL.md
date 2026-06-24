---
name: query-wiki
description: Answer questions by reading an Obsidian LLM wiki before raw sources. Use this skill whenever the user says `query-wiki`, asks what the vault/wiki/notes say about a topic, asks for a synthesis from their Obsidian vault, or asks natural-language questions such as "what does my vault say about growth mindset?" even when they do not name the skill.
---

# query-wiki

Answer questions from the wiki's linked synthesis layer first, using raw source records only when the wiki needs verification, source-level detail, or support for a durable update.

## When To Use

Use this skill for command-style requests such as:

```text
query-wiki What does this vault say about growth mindset and mistakes?
```

Also use it for natural language requests such as "what do my notes say about this topic?", "summarize the vault's view on X", "find what the wiki says about X", or "answer this from my Obsidian vault."

This skill is primarily read-only. Use it to answer from existing wiki content. Create or update pages only when the user's wording implies durable synthesis, such as asking to "save this to the wiki", "make a page for this", "update the notes with this answer", or "turn this answer into a durable wiki page."

Do not use this skill for initializing a vault, ingesting a new `/raw/todo` source, or running a broad lint pass unless the user explicitly changes the task.

## Required Reading

Before answering, read these bundled references:

- `skills/shared/wiki-conventions.md` for vault layout, query workflow, ownership rules, page conventions, and logging boundaries.
- `skills/shared/obsidian-markdown.md` for Obsidian wikilinks, source links, aliases, and heading links.

Then read vault-local files in this order:

1. `/AGENTS.md` when present. Treat it as the vault-specific operating manual.
2. `/index.md` before searching elsewhere. Use it as the first map of topics, folders, and likely pages.

If `/AGENTS.md` conflicts with this skill or the bundled references, follow the local file for vault-specific conventions unless it would violate raw-source immutability or the user's explicit request. Ask the user before proceeding when the conflict affects what files may be edited.

## Workflow

1. Establish the query and vault root.
   - Restate the topic or question in your own working notes if it is broad or ambiguous.
   - If the user did not identify a vault and the current directory is unclear, ask for the vault root before reading files.
   - Treat the vault root as the wiki root.

2. Read the operating context first.
   - Read `/AGENTS.md` when present.
   - Read `/index.md` before opening topic pages or raw sources.
   - Use `/index.md` to identify likely root-level topic folders and standalone Markdown notes.

3. Search the wiki synthesis layer.
   - Search root-level topic folders and standalone Markdown notes using folder names, page titles, headings, body text, and Obsidian links.
   - Follow relevant `[[wikilinks]]` outward from promising pages to connected concepts.
   - Prefer root-level wiki pages over raw files when the wiki already contains a clear synthesis.
   - Avoid `.obsidian`, `/docs`, and `/raw/todo` unless the user's question directly concerns those areas.
   - Avoid `/raw` at this stage unless a wiki page points there and the answer needs source verification or source-level detail.

4. Consult raw sources only when useful.
   - Read `/raw` files when the wiki answer needs source verification, quoted support, date/source context, or details not preserved in the synthesis pages.
   - Do not edit, rename, move, or delete anything under `/raw`.
   - Do not treat `/raw/todo` as normal evidence for an ordinary query. Use it only when the user explicitly asks about pending intake items or the topic cannot be answered without a directly relevant pending source.

5. Answer with linked evidence.
   - Lead with the direct answer, then summarize the supporting wiki view.
   - Link relevant wiki pages using Obsidian wikilinks such as `[[Page Name]]` or `[[folder/page|alias]]`.
   - Include raw source links such as `[[raw/source-file|source-file]]` when they clarify provenance, resolve uncertainty, or support source-level detail.
   - Distinguish wiki synthesis from raw-source detail when they differ in certainty or emphasis.
   - Say what you checked when that helps the user trust the answer, especially if the topic was sparse or absent from the wiki.

6. Handle durable synthesis carefully.
   - Offer to create or update a wiki page when the answer reveals durable synthesis but the user has not clearly asked for a file change.
   - Directly create or update a page only when the user's intent implies the result should become part of the knowledge base.
   - Follow the page conventions in `skills/shared/wiki-conventions.md`: atomic page, 1-2 sentence executive summary for new pages, useful wikilinks, and under 500 words per page.
   - Update `/index.md` when a durable query creates, moves, renames, or meaningfully rehomes wiki pages.
   - Append `/log.md` only when the query creates or updates durable wiki content. Use the query log heading form from `skills/shared/wiki-conventions.md`.

7. Preserve read-only behavior for ordinary questions.
   - Do not modify source files, wiki pages, `/index.md`, or `/log.md` for ordinary question-answering.
   - If you accidentally discover a needed maintenance issue while answering, mention it as a recommendation instead of fixing it unless the user asks for the update.

## Verification

Before reporting completion, verify the result matches the query type:

1. For ordinary read-only questions:
   - Confirm relevant wiki pages were searched after `/index.md`.
   - Confirm the answer links to relevant wiki pages when they exist.
   - Confirm raw sources were used only when verification or source-level detail was needed.
   - Confirm no source files, wiki pages, `/index.md`, or `/log.md` were modified.

2. For queries that create or update durable wiki content:
   - Confirm each created or edited wiki page follows the page conventions and stays under 500 words.
   - Confirm new or edited pages use useful Obsidian links and stable raw source links when applicable.
   - Confirm `/index.md` was updated when page creation, movement, rename, or folder placement changed the topic map.
   - Confirm `/log.md` has one appended query entry and that no log entry was added for purely read-only answering.

3. If verification fails:
   - Fix safe formatting, link, or logging mistakes immediately.
   - Ask the user before changing ambiguous synthesis, overwriting existing page content, or using pending `/raw/todo` material as evidence.
