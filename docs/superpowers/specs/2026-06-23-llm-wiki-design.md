# LLM Wiki Design

## Purpose

Build an Obsidian vault into an LLM-maintained wiki following [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The user curates source material and asks questions. The LLM reads immutable raw sources, maintains the wiki, updates cross-links, records activity, and keeps synthesis current over time.

## Obsidian Vault Directory Structure

```text
/
  Wiki root. Existing top-level knowledge folders and standalone notes live here directly.

/raw/
  Immutable source records that have already been ingested into wiki pages. The LLM may read these files but must not edit, rename, or delete them.

/raw/todo/
  Intake queue for new source records that have not been ingested yet. The LLM may read these files during ingest and may move an ingested source to /raw only after the user approves finalization.

/raw/assets/
  Local attachments and images associated with raw sources.

/index.md
  Content-oriented catalog of wiki pages, organized by topic and updated after ingests or major reorganizations.

/log.md
  Append-only chronological record of ingests, queries, lint passes, and major maintenance actions.

/AGENTS.md
  Operating manual for future LLM agent sessions.
```

Existing folders are wiki content and should stay at the vault root. 

## Ownership Rules

- `/raw/todo` is the source intake queue. Files in this tree are source-of-truth records waiting to be processed. The LLM may read them but must not rewrite their contents.
- `/raw` is the ingested source archive. Files in this tree are immutable once moved there after an approved ingest.
- The vault root is the synthesis layer. The LLM may create, rewrite, split, merge, rename, and reorganize wiki content pages and topic folders at the root, while preserving special system folders such as `/raw`, `/docs`, and `.obsidian`.
- `AGENTS.md`, `/index.md`, and `/log.md` are part of the operating system for the wiki and should be updated when conventions or workflows change.
- The LLM should not modify Obsidian plugin files or workspace settings unless explicitly asked.

## Page Conventions

Wiki pages are normal Markdown files that should work well in Obsidian.

Each wiki page should be atomic: about one idea, and complete enough to stand on its own. The page title should be the concise name of that idea. A book, podcast, article, or other broad source may have a page, but its important sub-ideas should usually become separate linked concept pages rather than being packed into the source page.

When creating a page, always write a 1~2 sentence executive summary first.

Pages should stay concise. Aim for under 300 words, and keep every page under 500 words. If a page wants to grow beyond that, check whether it contains more than one idea and split it into smaller linked pages.

Use Obsidian wiki links for internal references. Prefer short links when unique; use vault-root paths when a path makes the target clearer:

```markdown
[[心理学/阿德勒：个体心理学|阿德勒：个体心理学]]
```

When useful, add a short source section near the bottom:

```markdown
## Sources

- [[raw/example-source|example-source]]
```

Use clear titles and topic folders as each note's primary home. 

## Ingest Workflow

Ingest is the most important workflow. It has the following purposes:
- **Organize** the new idea(s) into the most appropriate folders
- **Distill** key takeaways and summarize the content
- **Connect** relevant ideas in other pages

### Rules for Ingest
- Keep the user involved in the process
- Follow the Page Conventions above
- Identify relevant pages, add links in them using Obsidian's link feature.
- If the source have paraphrased a well-known quote (this is common in podcast transcription), search for the original quote and add it
- If the source is Chinese and talked about a key academic concept, add the English name of this concept. For example 成长型思维 (Growth Mindset). Be judicious whether it adds value to do it. Don't do it too much in a page -- my suggestion would be only do it for the main concept of the page if it adds value. I don't need this in the page title because it makes the title verbose. It's helpful to do it in the executive summary.

### Ingest steps

1. Find the source the user wants to ingest in `/raw/todo`.
2. Decide which topic folder should contain the new page. Use the existing folder structure when possible; create a folder only when the topic clearly needs one.
3. Read the source and prepare an ingest briefing before editing wiki pages:
   - an executive summary
   - suggested key takeaways
   - candidate new atomic pages
   - relevant existing pages that may need outbound links or updates
   - anything illogical in the source itself
   - claims that contradict existing notes
   - paraphrased well-known quotes that should be restored to the original wording when useful
   - Chinese academic concepts where adding the English name would clarify the page, used judiciously and usually only for the page's core concept
4. Discuss the briefing with the user and wait for approval before creating or updating wiki pages.
5. Create the new page with the approved executive summary and key takeaways in concise writing. Link to the source.
6. Add outbound Obsidian links from edited pages to other relevant wiki pages.
7. Update relevant existing atomic wiki pages when the source strengthens, refines, or contradicts prior synthesis, keeping changes focused and concise.
8. After the user approves the page changes, finalize the ingest:
   - update `/index.md` when pages or folder placement changed
   - append an entry to `/log.md`
   - move the ingested source from `/raw/todo` to `/raw`
   - ensure wiki source links point to the final `/raw` archive path

Use this log format:

```markdown
## [YYYY-MM-DD] ingest | Source title

- Source: [[raw/source-file|source-file]]
- Updated: [[folder/page-a|page-a]], [[folder/page-b|page-b]]
- Created: [[folder/page-c|page-c]]
- Notes: brief summary of the integration
```

## Query Workflow

When answering questions against the vault:

1. Read `/index.md` first.
2. Use folder structure, page titles, and Obsidian links to search and read relevant wiki pages.
3. Consult `/raw` only when the answer needs source verification or more detail than the wiki contains.
4. Answer with links to relevant wiki pages and raw sources when useful.
5. If the answer produces durable synthesis, offer or directly create a new page when the user's intent implies that the answer should become part of the knowledge base.
6. Append important query-driven additions to `/log.md`.

## Lint Workflow

Periodic wiki health checks should look for:

- contradictions between pages
- stale claims that newer sources have superseded
- important concepts mentioned but lacking their own page
- missing cross-references. Ideas that can interconnect but are not linked.
- data gaps that could be filled with a web search.
- Pages that should be split, merged, renamed, or moved.
- Index entries that are missing or outdated.

Lint passes should update the wiki directly when fixes are clear and log what changed.

## Skill Implementation Plan

Create four reusable, standalone skills in a public GitHub repository so they can be installed by other agents through Find Skills / the Skills CLI. Codex, Claude, Gemini, and other LLM agents should all be able to use the skills because each skill is plain Markdown instructions plus optional bundled reference files or scripts.

Recommended repository name: `llm-wiki-skills`.

### Repository files to create

```text
llm-wiki-skills/
  README.md
  LICENSE
  skills/
    init-wiki/
      SKILL.md
    ingest-wiki/
      SKILL.md
    query-wiki/
      SKILL.md
    lint-wiki/
      SKILL.md
    shared/
      wiki-conventions.md
      obsidian-markdown.md
  evals/
    evals.json
```

- `skills/init-wiki/SKILL.md`: initializes an existing Obsidian vault as an LLM wiki.
- `skills/ingest-wiki/SKILL.md`: processes one source from `/raw/todo` into concise atomic wiki pages.
- `skills/query-wiki/SKILL.md`: answers questions using the wiki first.
- `skills/lint-wiki/SKILL.md`: runs wiki health checks and proposes or applies approved fixes.
- `skills/shared/wiki-conventions.md`: shared folder rules, page conventions, ingest approval gates, query rules, and lint rules.
- `skills/shared/obsidian-markdown.md`: concise Obsidian Markdown reference focused on wikilinks, embeds, and source links.
- `README.md`: explains the LLM wiki pattern, skill list, examples, install commands, and compatibility notes.
- `evals/evals.json`: test prompts for the four skills.

The skill names must be:

- `init-wiki`
- `ingest-wiki`
- `query-wiki`
- `lint-wiki`

Each skill description should trigger on both the skill name and natural language. Command-style phrasing can be documented as a convenient user convention, but the skills should not depend on Codex-specific slash-command registration. Example invocations:

- `init-wiki /path/to/vault`
- `ingest-wiki raw/todo/example-source.md`
- `query-wiki What does this vault say about growth mindset?`
- `lint-wiki`

If the public Skills CLI supports the repository as expected, users should be able to install individual skills with commands like:

```bash
npx skills add <owner>/llm-wiki-skills@init-wiki
npx skills add <owner>/llm-wiki-skills@ingest-wiki
npx skills add <owner>/llm-wiki-skills@query-wiki
npx skills add <owner>/llm-wiki-skills@lint-wiki
```

Before publishing, verify the final repository layout against the current Skills CLI expectations and adjust only packaging metadata or folder placement as needed. Do not change the four skill names.

### Vault files created or maintained by the skills

- `/AGENTS.md`: vault-local operating manual created by `init-wiki`; documents the four skills, folder rules, page conventions, and approval gates.
- `/index.md`: root-level wiki index created by `init-wiki` and maintained by `ingest-wiki` and `lint-wiki`.
- `/log.md`: root-level chronological activity log created by `init-wiki` and appended by `ingest-wiki`, `query-wiki` when it creates durable synthesis, and `lint-wiki`.

Each skill should read `/AGENTS.md` when present. All skills must preserve the current vault structure: the vault root is the wiki root, `/raw/todo` is the source intake queue, `/raw` is the ingested source archive.

### `init-wiki <path>`

Purpose: initialize an existing Obsidian vault so future sessions can operate it as an LLM wiki without moving existing knowledge folders.

Implementation behavior:

1. Resolve `<path>` to the vault root and verify it is a directory. If user doesn't give a path, ask if user want to use the current folder as vault root. 
2. Create `/raw`, `/raw/todo`, and `/raw/assets` if they do not exist.
3. Create `/index.md` if missing, with a concise topic index based on existing root-level knowledge folders and standalone Markdown notes.
4. Create `/log.md` if missing, with an initial setup entry.
5. Create `/AGENTS.md` if missing, copying the operating rules from this spec.
6. Preserve existing folders and notes in place.
7. Do not edit `.obsidian` files.

Verification:

- Run `find <path> -maxdepth 2 -type d` and confirm `/raw`, `/raw/todo`, and `/raw/assets` exist.
- Run `test -f <path>/index.md && test -f <path>/log.md && test -f <path>/AGENTS.md`.

### `ingest-wiki <specific source under /raw/todo>`

Purpose: process one source at a time into concise, atomic Obsidian wiki pages while keeping the user involved.

Implementation behavior:

1. Resolve the supplied source path and verify it is inside `/raw/todo`.
2. Read `/AGENTS.md`, `/index.md`, and relevant existing notes before proposing edits.
3. Prepare an ingest briefing with the folder recommendation, executive summary, key takeaways, candidate pages, relevant existing pages, illogical source claims, contradictions with existing notes, quote restoration opportunities, and useful English names for Chinese academic concepts.
4. Discuss the briefing with the user and wait for approval before editing wiki pages.
5. Create or update pages using Obsidian wikilinks, concise writing, a 1-2 sentence executive summary, and the page length limits from Page Conventions.
6. Add outbound links from edited pages to relevant existing pages.
7. Update existing atomic pages only when the new source strengthens, refines, or contradicts prior synthesis.
8. Ask the user to approve the page changes before finalization.
9. After approval, update `/index.md`, append `/log.md`, move the source from `/raw/todo` to `/raw`, and ensure source links point to the final `/raw` path.

Verification:

- Confirm every created or edited wiki page is under 500 words.
- Confirm the source file no longer exists under `/raw/todo` and exists under `/raw` only after final approval.
- Confirm the log entry lists source, created pages, updated pages, and a short integration note.

### `query-wiki <question>`

Purpose: answer questions using the wiki first, with raw sources used only when the wiki needs verification or more detail.

Implementation behavior:

1. Read `/AGENTS.md` and `/index.md` first.
2. Search root-level topic folders and standalone notes using folder names, page titles, and wikilinks.
3. Avoid `.obsidian`, `/docs`, and `/raw/todo` unless directly relevant.
4. Consult `/raw` only when the answer needs source verification or source-level detail.
5. Answer with links to relevant wiki pages and raw sources when useful.
6. If the answer creates durable synthesis, ask whether to create or update a wiki page unless the user's wording clearly requests it.
7. Append `/log.md` only when the query creates or updates durable wiki content.

Verification:

- Confirm the answer cites relevant wiki pages when they exist.
- Confirm no source files or wiki pages are modified for ordinary read-only questions.
- Confirm durable query-driven edits follow Page Conventions.

### `lint-wiki`

Purpose: run a wiki health pass that finds structural and synthesis issues across the root-level wiki.

Implementation behavior:

1. Read `/AGENTS.md` and `/index.md`.
2. Scan root-level Markdown notes and topic folders, excluding `.obsidian`, `/docs`, `/raw`, and hidden/system files.
3. Look for contradictions, stale claims, missing cross-references, important concepts without their own page, pages that should be split or merged, and outdated index entries.
4. Present a lint briefing grouped by severity and proposed action.
5. Apply clear fixes after user approval; keep uncertain findings as recommendations.
6. Append `/log.md` with the lint pass summary and pages changed.

Verification:

- Confirm lint does not modify `/raw` contents.
- Confirm every page edit preserves atomicity and the 500-word limit.
- Confirm `/index.md` is updated when pages are created, renamed, moved, split, or merged.

### Skill test prompts

Use these prompts to test the first version of the skills:

1. `init-wiki /Users/shiyonghu/workspace/Obsidian Vault`
2. `ingest-wiki raw/todo/example-podcast-transcript.md`
3. `query-wiki What does this vault say about growth mindset and mistakes?`
4. `lint-wiki`

The skill tests should verify that the skills follow approval gates, use Obsidian wikilinks, preserve `/raw` immutability, and keep pages concise and atomic.

## Success Criteria

- The vault has a clear raw/source layer and root-level wiki content layer.
- Existing notes are preserved in their root-level topic folders.
- Future LLM agent sessions can read `AGENTS.md` and know how to ingest, query, and lint the wiki.
- `/raw/todo` contains new sources waiting for ingest, and `/raw` remains the immutable archive for ingested sources.
