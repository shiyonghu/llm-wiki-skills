# LLM Wiki Conventions

Use these conventions when maintaining an Obsidian vault as an LLM wiki.

## Vault Layout

The vault root is the wiki root. Existing root-level knowledge folders and standalone Markdown notes are wiki content and stay in place.

- `/raw`: immutable archive for source records after approved ingest finalization.
- `/raw/todo`: intake queue for new source records. Read files during ingest, but do not rewrite their contents.
- `/raw/assets`: local attachments and images associated with raw sources.
- `/index.md`: content-oriented catalog of wiki pages, organized by topic.
- `/log.md`: append-only chronological record of ingests, durable query edits, lint passes, and major maintenance.
- `/AGENTS.md`: operating manual for future LLM agent sessions.

The vault root is the synthesis layer. Agents may create, rewrite, split, merge, rename, and reorganize wiki content pages and topic folders at the root when the workflow allows it. Preserve special system folders such as `/raw`, `/docs`, and `.obsidian`. Do not modify `.obsidian` plugin files or workspace settings unless explicitly asked.

After a source is moved from `/raw/todo` to `/raw` through approved ingest finalization, `/raw` is immutable: do not edit, rename, or delete archived source files.

## Page Conventions

Wiki pages are normal Markdown files that work well in Obsidian.

Each page should be atomic: about one idea, and complete enough to stand on its own. A broad source such as a book, podcast, or article may have a page, but important sub-ideas should usually become separate linked concept pages.

When creating a page, start with a 1-2 sentence executive summary.

Keep pages concise. Aim for under 300 words. Keep every page under 500 words as a hard limit. If a page wants to grow beyond that, check whether it contains more than one idea and split it into smaller linked pages.

Use Obsidian wiki links for internal references. Prefer short links when the target is unique; use vault-root paths when the path makes the target clearer.

When useful, add a short source section near the bottom:

```markdown
## Sources

- [[raw/example-source|example-source]]
```

## Ingest Workflow

Ingest processes one source from `/raw/todo` into concise, linked wiki pages while keeping the user involved.

1. Find the source the user wants to ingest in `/raw/todo`.
2. Decide which topic folder should contain the new page. Use the existing folder structure when possible; create a folder only when the topic clearly needs one.
3. Read the source and prepare an ingest briefing before editing wiki pages.
4. Discuss the briefing with the user and wait for approval before archiving the source or editing wiki pages.
5. After briefing approval, move the source from `/raw/todo` to `/raw` so page source links can point to the stable archive path.
6. Create the new page with the approved executive summary and key takeaways in concise writing. Link to the archived source.
7. Add outbound Obsidian links from edited pages to other relevant wiki pages.
8. Update relevant existing atomic wiki pages when the source strengthens, refines, or contradicts prior synthesis, keeping changes focused and concise.
9. Ask the user to approve the page changes before finalization.
10. After final approval, update `/index.md`, append `/log.md`, and ensure source links point to the final `/raw` archive path.

The ingest briefing must include:

- executive summary
- suggested key takeaways
- candidate new atomic pages
- relevant existing pages that may need outbound links or updates
- anything illogical in the source itself
- claims that contradict existing notes
- paraphrased well-known quotes that should be restored to original wording when useful
- Chinese academic concepts where adding the English name would clarify the page, used judiciously and usually only for the core concept

Use this ingest log format:

```markdown
## [YYYY-MM-DD] ingest | Source title

- Source: [[raw/source-file|source-file]]
- Updated: [[folder/page-a|page-a]], [[folder/page-b|page-b]]
- Created: [[folder/page-c|page-c]]
- Notes: brief summary of the integration
```

## Query Workflow

When answering questions against the vault:

1. Read `/AGENTS.md` when present and `/index.md` first.
2. Use folder structure, page titles, and Obsidian links to search and read relevant wiki pages.
3. Consult `/raw` only when the answer needs source verification or more detail than the wiki contains.
4. Answer with links to relevant wiki pages and raw sources when useful.
5. If the answer produces durable synthesis, offer or directly create a new page when the user's intent implies that the answer should become part of the knowledge base.
6. Append important query-driven additions to `/log.md`.

Use this query log heading form when a query creates or updates durable wiki content:

```markdown
## [YYYY-MM-DD] query | Question or synthesis title
```

## Lint Workflow

Periodic wiki health checks should scan root wiki content while excluding `.obsidian`, `/docs`, `/raw`, hidden files, and system files.

Look for:

- contradictions between pages
- stale claims that newer sources have superseded
- important concepts mentioned but lacking their own page
- missing cross-references between related ideas
- data gaps that could be filled with a web search
- pages that should be split, merged, renamed, or moved
- index entries that are missing or outdated

Present uncertain findings as recommendations. Apply clear fixes after user approval, preserve atomicity and the 500-word hard limit, update `/index.md` when pages are created, renamed, moved, split, or merged, and never modify `/raw` contents.

Use this lint log heading form:

```markdown
## [YYYY-MM-DD] lint | Scope or pass summary
```
