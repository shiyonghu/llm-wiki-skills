---
name: ingest-wiki
description: Process one source from an Obsidian LLM wiki's /raw/todo queue into concise atomic wiki pages. Use this skill whenever the user says `ingest-wiki`, provides a source path under raw/todo, asks to ingest/process/archive a new source into the wiki, or naturally asks to turn a raw note, transcript, article, PDF notes, or Chinese/English source from /raw/todo into linked Obsidian wiki pages.
---

# ingest-wiki

Process a single source from `/raw/todo` into the wiki's linked synthesis layer while keeping the source immutable, the pages concise, and the user involved at both approval gates.

## When To Use

Use this skill for command-style requests such as:

```text
ingest-wiki raw/todo/example-podcast-transcript.md
```

Also use it for natural language requests such as "process this source from raw/todo into the wiki", "ingest the new transcript", "turn this raw article into atomic Obsidian notes", or "archive this source after adding the useful ideas to my wiki."

This skill handles one source at a time. If the user supplies multiple sources, ask which one to process first and leave the others in `/raw/todo`. If the user does not name a source and `/raw/todo` contains exactly one note, ingest that note instead of asking the user to identify it. Do not use this skill for ordinary wiki questions, initialization, or broad lint passes unless the user explicitly asks to start an ingest workflow.

## Required Reading

Before proposing edits, read these bundled references:

- `skills/shared/wiki-conventions.md` for the vault layout, ownership rules, page conventions, ingest approval gates, log format, and source movement rules.
- `skills/shared/obsidian-markdown.md` for Obsidian wikilinks, raw source links, aliases, heading links, and asset embeds.

Then read these vault-local files when present:

- `/AGENTS.md` for the vault's operating manual and any local overrides.
- `/index.md` for the current topic map and likely homes for new or updated pages.
- Relevant existing notes before proposing page changes. Use `/index.md`, folder names, page titles, wikilinks, and text search to find pages that overlap the source's ideas.

If `/AGENTS.md` conflicts with this skill or the shared references, pause and ask the user how to proceed.

## Bundled Helper

Use `scripts/archive-ingest-source.py`, resolved relative to this `SKILL.md`, for the source archive move. It validates that the source is under `/raw/todo`, refuses archive collisions, moves the file to `/raw`, verifies the result, and prints the final archive path.

## Workflow

1. Resolve and validate the source.
   - Resolve the supplied path to an absolute path.
   - Verify that it exists, is a file, and is inside the vault's `/raw/todo` tree.
   - If no source path is supplied, inspect `/raw/todo`. If it contains exactly one note, use that note as the source. If it contains zero notes or multiple notes, ask the user for one source under `/raw/todo`.
   - If the path is outside `/raw/todo`, stop and ask for a valid intake source. Do not ingest archived `/raw` files or unrelated wiki pages through this workflow.
   - Read the source without rewriting it.

2. Establish wiki context before planning edits.
   - Read `/AGENTS.md` when present.
   - Read `/index.md`.
   - Inspect relevant topic folders and existing notes before recommending new pages or updates.
   - Prefer existing folder structure. Recommend a new folder only when the source clearly introduces a durable topic that does not fit the current wiki.

3. Prepare an ingest briefing before editing wiki pages.
   - Do not create, update, move, or archive wiki files while preparing the briefing.
   - Include this structure:

   ```markdown
   ## Ingest Briefing

   ### Executive Summary
   1-2 sentences describing what the source adds to the wiki.

   ### Key Takeaways
   - Durable ideas worth preserving.

   ### Candidate Atomic Pages
   - Proposed page title, folder, 1-sentence purpose, and whether it is new or an update.

   ### Relevant Existing Pages
   - Existing pages to link from, link to, strengthen, refine, or challenge.

   ### Illogical Claims
   - Claims in the source that seem unsupported, internally inconsistent, or conceptually confused.

   ### Contradictions
   - Claims that appear to conflict with existing wiki notes, with links to the relevant notes.

   ### Quote Restoration Opportunities
   - Paraphrased well-known quotes that may be worth restoring to original wording, with uncertainty noted.

   ### Useful English Names
   - Chinese academic concepts where an English name would clarify the core idea, used sparingly.
   ```

   - Include source links or short source location notes where they help the user evaluate the briefing.
   - Be explicit when a section has no findings, for example "No contradictions found in the notes reviewed."

4. Discuss the briefing and wait for approval.
   - Ask the user to approve, revise, or reject the proposed page plan before editing any wiki pages.
   - Tell the user that approving the page plan also approves archiving the source from `/raw/todo` to `/raw` before page edits begin.
   - If the user asks for changes to the plan, revise the briefing and wait again.
   - Do not proceed from briefing to source archiving or page edits without clear user approval.

5. Archive the approved source before page edits.
   - Run `python3 scripts/archive-ingest-source.py <absolute-source-path>` from this skill directory, preserving the filename.
   - If the helper reports `Archive already exists`, pause and ask the user for a safe archive filename. After approval, rerun the helper with `--archive-name <approved-filename>`.
   - Use the helper's stdout as the final archived source path.
   - Do not create or update wiki pages until the helper succeeds and the final archived source path is known.

6. Draft approved page changes.
   - Create or update concise atomic pages in the vault root's topic folders.
   - Start each newly created page with a 1-2 sentence executive summary.
   - Use Obsidian wikilinks for internal references and source sections when useful.
   - Link to the source using the helper-reported final archive path under `/raw`, not `/raw/todo`.
   - Add outbound links from edited pages to relevant existing pages.
   - Update existing pages only when the source strengthens, refines, or contradicts prior synthesis. Keep updates focused; do not rewrite unrelated material.
   - When part of the source is already concise and suitable for a wiki page, copy that concise wording directly into the page. Never paraphrase concise source material into more verbose prose just to make it sound synthesized.
   - Preserve page atomicity, aim for under 300 words per page, and keep every created or edited page under 500 words.
   - When a Chinese academic concept is central and useful to clarify, include the English name in prose, usually in the executive summary rather than the title.
   - Restore well-known quotes only when the original wording can be identified reliably; otherwise note the paraphrase without presenting uncertain wording as exact.

7. Ask for page-change approval before finalization.
   - Summarize created pages, updated pages, source links, and any notable unresolved contradictions or uncertainties.
   - Ask the user to approve the page changes before updating `/index.md` or appending `/log.md`.
   - If the user requests revisions, make the revisions and ask again.

8. Finalize only after approval.
   - Update `/index.md` when pages were created, moved, renamed, or their folder placement changed.
   - Append `/log.md` using the ingest log format from `skills/shared/wiki-conventions.md`.
   - Ensure all source links in created or edited pages point to the helper-reported `/raw` archive path.
   - Do not edit, rename, or delete any file already archived under `/raw`.

9. Report the completed ingest.
   - List created pages, updated pages, the archived source path, and the log entry heading.
   - Mention any pages intentionally left unchanged because the source did not strengthen, refine, or contradict them.

## Verification

Before reporting completion, verify the ingest state:

1. Page length and structure:
   - Check every created or edited wiki page is under 500 words.
   - Confirm newly created pages begin with a 1-2 sentence executive summary.
   - Confirm edited pages include useful outbound Obsidian links to relevant existing pages.

2. Source links and movement:
   - Confirm no created or edited page links to `/raw/todo` for the ingested source.
   - Confirm source links point to the helper-reported `/raw` archive path.
   - Confirm the helper-reported archive path exists and the original `/raw/todo` source path no longer exists after briefing approval and before page edits.

3. Operating files:
   - Confirm `/index.md` reflects created or relocated pages when applicable.
   - Confirm `/log.md` has one appended ingest entry listing the source, created pages, updated pages, and a short integration note.

4. Approval gates:
   - Confirm the user approved the ingest briefing before page edits.
   - Confirm the user approved source archiving before the helper ran.
   - Confirm the user approved the page changes before finalization.

If any verification step fails, fix the issue when safe. If fixing would require changing the approved page plan, moving a source unexpectedly, overwriting an archived file, or changing ambiguous synthesis, pause and ask the user for direction.
