---
name: lint-wiki
description: Run an Obsidian LLM wiki health check and maintenance pass. Use this skill whenever the user says `lint-wiki`, asks to lint/audit/check/clean up an Obsidian LLM wiki, wants a vault health check, asks for stale notes or missing links to be found, or naturally requests a review of wiki structure, contradictions, index drift, or concepts that should be split, merged, renamed, moved, or turned into their own pages.
---

# lint-wiki

Run a cautious health pass over an Obsidian LLM wiki: inspect the synthesis layer, surface structural and content issues, get user approval for edits, then apply clear maintenance fixes while preserving raw sources and concise atomic pages.

## When To Use

Use this skill for command-style requests such as:

```text
lint-wiki
```

Also use it for natural language requests such as "run a health check on this Obsidian LLM wiki", "find stale or contradictory notes", "check whether my wiki needs more links", "audit the index", or "look for pages that should be split, merged, renamed, or moved."

This skill is for periodic maintenance of an already initialized wiki. Do not use it to initialize a vault, ingest a new `/raw/todo` source, or answer a narrow knowledge question unless the user explicitly asks to turn that work into a wiki health pass.

## Required Reading

Before scanning or editing the vault, read these bundled references:

- `skills/shared/wiki-conventions.md` for vault layout, ownership rules, page conventions, lint expectations, index/log maintenance, and raw-source immutability.
- `skills/shared/obsidian-markdown.md` for Obsidian wikilinks, source links, aliases, heading links, and asset embeds.

Then read these vault-local files:

1. `/AGENTS.md` when present. Treat it as the local operating manual for the vault.
2. `/index.md` before scanning topic folders. Use it as the expected topic map and compare it with the actual pages.

If `/AGENTS.md` conflicts with this skill or the bundled references, follow the local rule when it is more specific and does not violate raw-source immutability. Ask the user before proceeding when the conflict affects what may be edited.

## Workflow

1. Establish the lint scope.
   - Treat the current working directory as the vault root unless the user supplied another path.
   - If the vault root is unclear, ask the user to identify it before scanning.
   - Read `/AGENTS.md` when present and `/index.md` before opening topic pages.
   - Decide whether the user requested a full-vault lint pass or a focused pass over specific topics.

2. Build the scan set.
   - Scan root-level Markdown notes and root-level topic folders that contain wiki pages.
   - Include nested Markdown files inside topic folders when they are part of the wiki content.
   - Exclude `.obsidian`, `/docs`, `/raw`, hidden files, hidden folders, operating-system files, dependency folders, generated files, and other system files.
   - Do not modify anything under `/raw`; archived and pending source records are evidence only when needed to verify a lint finding.

3. Inspect content and structure.
   - Compare `/index.md` with the actual root notes and topic folders to find missing, stale, misplaced, or outdated index entries.
   - Follow existing `[[wikilinks]]` to detect related ideas that lack cross-references.
   - Look for contradictions between pages, especially where one page appears to supersede or challenge another.
   - Identify stale claims that newer pages or sources appear to have replaced.
   - Note data gaps that would benefit from a web search or additional source ingestion.
   - Identify important concepts mentioned in pages that do not have their own atomic page.
   - Identify pages that exceed or strain the atomic-page model and should be split.
   - Identify pages that overlap heavily and may be merge candidates.
   - Identify pages or folders that should be renamed or moved for clearer topic placement.
   - Preserve the hard 500-word limit for every wiki page; flag pages that are already over the limit or would exceed it after a proposed edit.

4. Prepare a lint briefing before editing.
   - Do not create, rewrite, move, rename, merge, split, or delete wiki pages while preparing the briefing.
   - Group findings by severity and proposed action.
   - Keep uncertain findings as recommendations instead of presenting them as facts.
   - Include enough page links or paths for the user to inspect each finding.
   - Use this structure:

   ```markdown
   ## Lint Briefing

   ### High Severity
   - Finding, evidence, impact, proposed action, and whether approval is needed.

   ### Medium Severity
   - Finding, evidence, impact, proposed action, and whether approval is needed.

   ### Low Severity
   - Finding, evidence, impact, proposed action, and whether approval is needed.

   ### Recommendations
   - Uncertain findings, possible research/data gaps, and optional improvements.

   ### Proposed Fix Plan
   - Clear fixes to apply after approval.
   - Items to leave as recommendations.
   ```

5. Get approval before applying fixes.
   - Ask the user to approve the proposed fix plan, revise it, or choose specific findings to apply.
   - Apply only approved fixes unless the user has explicitly granted permission to apply clear lint fixes in the original request.
   - When a finding is uncertain, keep it as a recommendation or ask the user for direction before editing.

6. Apply approved maintenance fixes.
   - Use focused edits that preserve each page's atomic idea and keep every edited page under 500 words.
   - Add missing Obsidian cross-references where the relationship is clear.
   - Update stale claims only when the newer or more reliable wiki evidence is clear; otherwise record the uncertainty.
   - Create a new page for an important concept only when the concept is durable, recurring, and distinct enough to stand alone.
   - Split pages that combine multiple durable ideas, leaving clear wikilinks between the resulting pages.
   - Merge pages only when they duplicate the same idea and the combined page can remain concise.
   - Rename or move pages only when the new title or location is clearly more accurate and useful.
   - Update `/index.md` whenever pages are created, renamed, moved, split, merged, or meaningfully rehomed.
   - Never edit, rename, move, delete, or reorganize `/raw` contents.

7. Log the lint pass.
   - Append `/log.md` after approved fixes are applied.
   - Include the date, lint scope, pages changed, and a short summary of what the pass resolved.
   - Use this heading form:

   ```markdown
   ## [YYYY-MM-DD] lint | Scope or pass summary

   - Checked: brief scope description
   - Changed: [[folder/page-a|page-a]], [[folder/page-b|page-b]]
   - Notes: summary of contradictions, links, index updates, splits, merges, or recommendations handled
   ```

   - If the user requested a read-only lint briefing and no files changed, do not append `/log.md` unless the user asks to record the pass.

8. Report the outcome.
   - Summarize the lint findings that were fixed, the recommendations left open, and any data gaps that need user-provided sources or web research.
   - List pages created, updated, renamed, moved, split, or merged.
   - Mention whether `/index.md` and `/log.md` were updated.

## Verification

Before reporting completion, verify the lint pass against the approved scope:

1. Confirm `/AGENTS.md` was read when present and `/index.md` was read before scanning topic folders.
2. Confirm the scan excluded `.obsidian`, `/docs`, `/raw`, hidden files, hidden folders, and system files.
3. Confirm the briefing covered contradictions, stale claims, missing cross-references, data gaps, important concepts without their own page, split candidates, merge candidates, rename/move candidates, and outdated index entries.
4. Confirm all uncertain findings remained recommendations or were explicitly approved by the user before editing.
5. Confirm no `/raw` contents were modified.
6. Confirm every created or edited wiki page remains atomic and under 500 words.
7. Confirm `/index.md` was updated when pages were created, renamed, moved, split, merged, or rehomed.
8. Confirm `/log.md` was appended with the lint pass summary and pages changed when approved fixes were applied.
9. If verification finds a safe formatting, link, index, or log mistake, fix it before final reporting. Ask the user before changing ambiguous synthesis or making unapproved structural edits.
