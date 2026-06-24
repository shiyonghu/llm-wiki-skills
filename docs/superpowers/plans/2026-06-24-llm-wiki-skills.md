# LLM Wiki Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the current `obsidian-llm-wiki` project root into a public skills repository that ships four reusable skills for maintaining an Obsidian vault as an LLM wiki.

**Architecture:** The repository root is `/Users/shiyonghu/workspace/obsidian-llm-wiki`, not a nested `llm-wiki-skills` folder. Four skill folders contain `SKILL.md` files created through the personal Skill Creator workflow, with shared reference files for common wiki conventions and Obsidian Markdown syntax, plus eval prompts and CLI preview commands for installability checks.

**Tech Stack:** Markdown skills, YAML frontmatter, `npx skills` CLI, GitHub.

---

## Scope Check

The spec defines one cohesive skills repository. The four skills are separate entry points, but they share the same vault model, approval gates, page conventions, and raw-source ownership rules. Keep this as one repository and one plan.

Important user instructions for implementers:

- Use `/Users/shiyonghu/workspace/obsidian-llm-wiki` as the git repository root.
- Do not create a nested `llm-wiki-skills/` implementation directory.
- Do not copy concrete `SKILL.md` bodies from this plan. Use the personal Skill Creator skill at `/Users/shiyonghu/.agents/skills/skill-creator/SKILL.md` to author each skill from the spec and the acceptance criteria below.
- The updated spec no longer requires banning `/wiki`, `/tags.md`, or tags. Do not add those requirements unless the user reintroduces them.

## File Structure

```text
/Users/shiyonghu/workspace/obsidian-llm-wiki/
  .gitignore
  README.md
  LICENSE
  package.json
  docs/
    superpowers/
      specs/
        2026-06-23-llm-wiki-design.md
      plans/
        2026-06-24-llm-wiki-skills.md
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

- `.gitignore`: ignores local tooling output and OS files.
- `package.json`: provides repeatable Skills CLI discovery and preview commands.
- `skills/shared/wiki-conventions.md`: shared folder rules, ownership rules, page conventions, ingest approval gates, query rules, lint rules, and log formats.
- `skills/shared/obsidian-markdown.md`: concise reference for Obsidian wikilinks, aliases, embeds, source links, and asset references.
- `skills/init-wiki/SKILL.md`: initializes an existing Obsidian vault as an LLM wiki.
- `skills/ingest-wiki/SKILL.md`: processes one `/raw/todo` source into concise atomic wiki pages with user approval gates.
- `skills/query-wiki/SKILL.md`: answers questions using the wiki first, consulting `/raw` only when source verification or detail is needed.
- `skills/lint-wiki/SKILL.md`: runs wiki health checks and applies approved fixes.
- `evals/evals.json`: test prompts for all four skills.
- `README.md`: explains the LLM wiki pattern, install commands, usage examples, compatibility notes, and development checks.
- `LICENSE`: repository license.

## Shared Spec Requirements

Every skill and shared reference must preserve these rules from `docs/superpowers/specs/2026-06-23-llm-wiki-design.md`:

- The vault root is the wiki root.
- Existing top-level knowledge folders and standalone notes stay at the vault root.
- `/raw/todo` is the source intake queue; read files there but do not rewrite them.
- `/raw` is the immutable archive for ingested sources.
- `/raw/assets` stores source attachments and images.
- `AGENTS.md`, `/index.md`, and `/log.md` are wiki operating files.
- Do not edit `.obsidian` files unless explicitly asked.
- Wiki pages are atomic, concise, normal Markdown files for Obsidian.
- Created pages start with a 1-2 sentence executive summary.
- Aim for under 300 words and keep every page under 500 words.
- Use Obsidian wikilinks, including aliases and vault-root paths when useful.
- Add source sections when useful.
- Ingest must include a briefing and wait for approval before editing wiki pages.
- Ingest must ask for approval again before finalization.
- Ingest finalization updates `/index.md`, appends `/log.md`, moves the source from `/raw/todo` to `/raw`, and fixes source links to point at `/raw`.
- Ingest briefings check for illogical source claims, contradictions, well-known quote restoration, and useful English names for Chinese academic concepts.
- Query reads `/AGENTS.md` when present and `/index.md` first, searches wiki pages before raw sources, and appends `/log.md` only for durable wiki edits.
- Lint scans root wiki content while excluding `.obsidian`, `/docs`, `/raw`, hidden files, and system files.
- Lint checks contradictions, stale claims, missing cross-references, missing atomic pages, split/merge/rename/move candidates, data gaps, and outdated index entries.
- Lint applies clear fixes after user approval, keeps uncertain findings as recommendations, and logs changes.

## Task 1: Root Repository Bootstrap And CLI Helpers

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/.gitignore`
- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/package.json`

- [ ] **Step 1: Initialize git at the project root**

Run from `/Users/shiyonghu/workspace/obsidian-llm-wiki`:

```bash
git init
git config user.name >/dev/null || git config user.name "shiyonghu"
git config user.email >/dev/null || git config user.email "shiyonghu@users.noreply.github.com"
```

Expected: `git init` prints `Initialized empty Git repository` or `Reinitialized existing Git repository`.

- [ ] **Step 2: Create implementation directories**

Run:

```bash
mkdir -p evals skills/init-wiki skills/ingest-wiki skills/query-wiki skills/lint-wiki skills/shared
```

Expected: command exits 0.

- [ ] **Step 3: Create `.gitignore`**

Create `/Users/shiyonghu/workspace/obsidian-llm-wiki/.gitignore`:

```gitignore
node_modules/
.DS_Store
*.log
coverage/
.agents/
.codex/
.claude/
*-workspace/
```

- [ ] **Step 4: Create `package.json`**

Create `/Users/shiyonghu/workspace/obsidian-llm-wiki/package.json`:

```json
{
  "name": "llm-wiki-skills",
  "version": "0.1.0",
  "private": true,
  "description": "Reusable skills for maintaining an Obsidian vault as an LLM wiki.",
  "license": "MIT",
  "type": "module",
  "scripts": {
    "skills:list": "npx --yes skills add . --list --full-depth",
    "skills:use:init": "npx --yes skills use . --skill init-wiki --full-depth",
    "skills:use:ingest": "npx --yes skills use . --skill ingest-wiki --full-depth",
    "skills:use:query": "npx --yes skills use . --skill query-wiki --full-depth",
    "skills:use:lint": "npx --yes skills use . --skill lint-wiki --full-depth"
  },
  "engines": {
    "node": ">=18"
  }
}
```

- [ ] **Step 5: Verify package scripts are readable**

Run:

```bash
npm run
```

Expected: output lists `skills:list`, `skills:use:init`, `skills:use:ingest`, `skills:use:query`, and `skills:use:lint`.

- [ ] **Step 6: Commit bootstrap files**

```bash
git add .gitignore package.json
git commit -m "chore: bootstrap root skill repository"
```

Expected: commit succeeds.

## Task 2: Shared References And Evals

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/shared/wiki-conventions.md`
- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/shared/obsidian-markdown.md`
- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`

- [ ] **Step 1: Read the source spec**

Run:

```bash
sed -n '1,360p' docs/superpowers/specs/2026-06-23-llm-wiki-design.md
```

Expected: output includes sections for vault structure, ownership rules, page conventions, ingest workflow, query workflow, lint workflow, skill implementation plan, and success criteria.

- [ ] **Step 2: Create shared reference files from the spec**

Use the spec to create:

```text
skills/shared/wiki-conventions.md
skills/shared/obsidian-markdown.md
```

Acceptance criteria for `skills/shared/wiki-conventions.md`:

- Explains that the vault root is the wiki root.
- Lists `/raw`, `/raw/todo`, `/raw/assets`, `/index.md`, `/log.md`, and `/AGENTS.md`.
- States existing root-level knowledge folders and standalone notes stay in place.
- States `/raw/todo` can be read during ingest but not rewritten.
- States `/raw` is immutable after approved ingest finalization.
- States `.obsidian` files must not be modified unless explicitly asked.
- Includes atomic page rules, executive summaries, 300-word target, 500-word hard limit, and source sections.
- Includes the ingest briefing requirements, approval before page edits, final approval before archival, and log format.
- Includes query and lint workflows from the spec.
- Includes the exact ingest log heading form `## [YYYY-MM-DD] ingest | Source title`.
- Includes query and lint log heading forms.

Acceptance criteria for `skills/shared/obsidian-markdown.md`:

- Shows `[[Page Name]]`.
- Shows `[[folder/page|alias]]`.
- Shows heading links when useful.
- Shows `[[raw/source-file|source-file]]`.
- Shows an embed from `/raw/assets`.
- Explains when to prefer short links versus vault-root paths.

Do not include concrete `SKILL.md` content in the plan or copy old plan skill bodies. The implementer may write these shared references directly because they are bundled references, not the skill bodies.

- [ ] **Step 3: Create `evals/evals.json`**

Create `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`:

```json
{
  "name": "llm-wiki-skills",
  "version": "0.1.0",
  "evals": [
    {
      "skill": "init-wiki",
      "prompt": "init-wiki /Users/shiyonghu/workspace/Obsidian Vault",
      "expected_output": "Initializes the supplied Obsidian vault as an LLM wiki while preserving existing root-level notes and folders.",
      "checks": [
        "Resolves the supplied path and verifies it is a directory.",
        "Creates raw, raw/todo, raw/assets, index.md, log.md, and AGENTS.md when missing.",
        "Preserves existing root-level knowledge folders and standalone Markdown notes.",
        "Does not edit .obsidian files."
      ]
    },
    {
      "skill": "ingest-wiki",
      "prompt": "ingest-wiki raw/todo/example-podcast-transcript.md",
      "expected_output": "Produces a briefing, waits for approval, creates concise linked pages, waits for final approval, then updates index/log and archives the source.",
      "checks": [
        "Verifies the source is inside raw/todo.",
        "Reads AGENTS.md, index.md, and relevant existing notes before proposing edits.",
        "Briefing includes takeaways, candidate pages, existing pages, contradictions, quote restoration, and Chinese academic concept checks.",
        "Waits for approval before editing and again before finalization.",
        "Moves the source to raw only after final approval."
      ]
    },
    {
      "skill": "query-wiki",
      "prompt": "query-wiki What does this vault say about growth mindset and mistakes?",
      "expected_output": "Answers from index.md and wiki pages first, consulting raw sources only when needed for verification or detail.",
      "checks": [
        "Reads AGENTS.md when present and reads index.md first.",
        "Searches root-level topic folders and standalone notes before raw sources.",
        "Cites relevant wiki pages and raw sources when useful.",
        "Does not modify files for ordinary read-only questions.",
        "Logs only durable query-driven wiki edits."
      ]
    },
    {
      "skill": "lint-wiki",
      "prompt": "lint-wiki",
      "expected_output": "Runs a wiki health pass, presents findings by severity, applies approved clear fixes, and logs the maintenance pass.",
      "checks": [
        "Reads AGENTS.md when present and reads index.md.",
        "Excludes .obsidian, docs, raw, hidden files, and system files.",
        "Checks contradictions, stale claims, missing cross-references, data gaps, page split/merge/rename/move candidates, and outdated index entries.",
        "Asks for approval before applying fixes unless explicitly told to apply clear fixes.",
        "Does not modify raw source contents."
      ]
    }
  ]
}
```

- [ ] **Step 4: Review shared references and eval prompts against the spec**

Run:

```bash
sed -n '1,260p' skills/shared/wiki-conventions.md
sed -n '1,220p' skills/shared/obsidian-markdown.md
sed -n '1,220p' evals/evals.json
```

Expected: the shared references cover the acceptance criteria in Step 2, and `evals/evals.json` contains one prompt for each of `init-wiki`, `ingest-wiki`, `query-wiki`, and `lint-wiki`.

- [ ] **Step 5: Commit shared references and eval prompts**

```bash
git add skills/shared/wiki-conventions.md skills/shared/obsidian-markdown.md evals/evals.json
git commit -m "docs: add shared wiki references and eval prompts"
```

Expected: commit succeeds.

## Task 3: Create `init-wiki` With Personal Skill Creator

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/init-wiki/SKILL.md`
- Modify if needed: `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`

- [ ] **Step 1: Read the personal Skill Creator instructions**

Run:

```bash
sed -n '1,700p' /Users/shiyonghu/.agents/skills/skill-creator/SKILL.md
```

Expected: output includes Capture Intent, Write the SKILL.md, Test Cases, Running and evaluating test cases, and Description Optimization.

- [ ] **Step 2: Use Skill Creator to author `init-wiki`**

Invoke the personal Skill Creator workflow for this skill. Use this handoff prompt:

```text
Use the personal Skill Creator skill at /Users/shiyonghu/.agents/skills/skill-creator/SKILL.md to create skills/init-wiki/SKILL.md from docs/superpowers/specs/2026-06-23-llm-wiki-design.md.

Do not reuse concrete SKILL.md bodies from old plans. Author a fresh skill.

The skill name must be init-wiki.

The description must trigger on both "init-wiki" and natural language requests to initialize an existing Obsidian vault as an LLM wiki.

The skill must instruct the agent to:
- resolve the supplied vault path and verify it is a directory
- ask whether to use the current folder if no path is supplied
- create /raw, /raw/todo, and /raw/assets if missing
- create /index.md if missing from existing root-level folders and standalone Markdown notes
- create /log.md if missing with an initial setup entry
- create /AGENTS.md if missing from the operating rules in the spec
- preserve existing folders and notes in place
- avoid editing .obsidian files unless explicitly asked
- read /AGENTS.md when present
- verify raw folders and operating files after initialization

The SKILL.md must include sections named:
- ## When To Use
- ## Required Reading
- ## Workflow
- ## Verification

Use skills/shared/wiki-conventions.md and skills/shared/obsidian-markdown.md as bundled references.
```

Expected: `skills/init-wiki/SKILL.md` exists and follows Skill Creator guidance.

- [ ] **Step 3: Review `init-wiki` against the handoff criteria**

Run:

```bash
sed -n '1,260p' skills/init-wiki/SKILL.md
```

Expected: output shows YAML frontmatter with `name: init-wiki`, a description that triggers on command-style and natural-language initialization requests, the required section headings, references to the shared files, and the workflow requirements from the handoff prompt.

- [ ] **Step 4: Preview the skill through the Skills CLI**

Run:

```bash
npm run skills:use:init
```

Expected: command exits 0 and output contains `init-wiki`.

- [ ] **Step 5: Commit `init-wiki`**

```bash
git add skills/init-wiki/SKILL.md evals/evals.json
git commit -m "feat: add init wiki skill"
```

Expected: commit succeeds.

## Task 4: Create `ingest-wiki` With Personal Skill Creator

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/ingest-wiki/SKILL.md`
- Modify if needed: `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`

- [ ] **Step 1: Use Skill Creator to author `ingest-wiki`**

Invoke the personal Skill Creator workflow with this handoff prompt:

```text
Use the personal Skill Creator skill at /Users/shiyonghu/.agents/skills/skill-creator/SKILL.md to create skills/ingest-wiki/SKILL.md from docs/superpowers/specs/2026-06-23-llm-wiki-design.md.

Do not reuse concrete SKILL.md bodies from old plans. Author a fresh skill.

The skill name must be ingest-wiki.

The description must trigger on both "ingest-wiki" and natural language requests to process a source from /raw/todo into the wiki.

The skill must instruct the agent to:
- process one source at a time
- resolve the supplied source path and verify it is inside /raw/todo
- read /AGENTS.md, /index.md, and relevant existing notes before proposing edits
- prepare an ingest briefing before editing pages
- include executive summary, key takeaways, candidate atomic pages, relevant existing pages, illogical claims, contradictions, quote restoration opportunities, and useful English names for Chinese academic concepts in the briefing
- discuss the briefing and wait for user approval before editing wiki pages
- create or update concise atomic pages with 1-2 sentence executive summaries, Obsidian wikilinks, and source links
- add outbound links from edited pages to relevant existing pages
- update existing pages only when the source strengthens, refines, or contradicts prior synthesis
- ask the user to approve page changes before finalization
- after approval, update /index.md, append /log.md, move the source from /raw/todo to /raw, and ensure source links point to /raw
- verify page word counts, source movement, and log contents

The SKILL.md must include sections named:
- ## When To Use
- ## Required Reading
- ## Workflow
- ## Verification

Use skills/shared/wiki-conventions.md and skills/shared/obsidian-markdown.md as bundled references.
```

Expected: `skills/ingest-wiki/SKILL.md` exists and follows Skill Creator guidance.

- [ ] **Step 2: Review `ingest-wiki` against the handoff criteria**

Run:

```bash
sed -n '1,320p' skills/ingest-wiki/SKILL.md
```

Expected: output shows YAML frontmatter with `name: ingest-wiki`, a description that triggers on command-style and natural-language ingest requests, the required section headings, references to the shared files, both approval gates, the ingest briefing requirements, and finalization rules.

- [ ] **Step 3: Preview the skill through the Skills CLI**

Run:

```bash
npm run skills:use:ingest
```

Expected: command exits 0 and output contains `ingest-wiki`.

- [ ] **Step 4: Commit `ingest-wiki`**

```bash
git add skills/ingest-wiki/SKILL.md evals/evals.json
git commit -m "feat: add ingest wiki skill"
```

Expected: commit succeeds.

## Task 5: Create `query-wiki` With Personal Skill Creator

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/query-wiki/SKILL.md`
- Modify if needed: `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`

- [ ] **Step 1: Use Skill Creator to author `query-wiki`**

Invoke the personal Skill Creator workflow with this handoff prompt:

```text
Use the personal Skill Creator skill at /Users/shiyonghu/.agents/skills/skill-creator/SKILL.md to create skills/query-wiki/SKILL.md from docs/superpowers/specs/2026-06-23-llm-wiki-design.md.

Do not reuse concrete SKILL.md bodies from old plans. Author a fresh skill.

The skill name must be query-wiki.

The description must trigger on both "query-wiki" and natural language requests asking what the vault says about a topic.

The skill must instruct the agent to:
- read /AGENTS.md when present
- read /index.md first
- search root-level topic folders and standalone Markdown notes using folder names, page titles, and Obsidian links
- avoid .obsidian, /docs, and /raw/todo unless directly relevant
- consult /raw only when the answer needs source verification or source-level detail
- answer with links to relevant wiki pages and raw sources when useful
- offer or directly create a new page only when the user's intent implies durable synthesis
- append /log.md only when the query creates or updates durable wiki content
- verify ordinary read-only questions did not modify source files or wiki pages

The SKILL.md must include sections named:
- ## When To Use
- ## Required Reading
- ## Workflow
- ## Verification

Use skills/shared/wiki-conventions.md and skills/shared/obsidian-markdown.md as bundled references.
```

Expected: `skills/query-wiki/SKILL.md` exists and follows Skill Creator guidance.

- [ ] **Step 2: Review `query-wiki` against the handoff criteria**

Run:

```bash
sed -n '1,260p' skills/query-wiki/SKILL.md
```

Expected: output shows YAML frontmatter with `name: query-wiki`, a description that triggers on command-style and natural-language wiki questions, the required section headings, references to the shared files, wiki-first search rules, raw-source limits, and durable synthesis logging rules.

- [ ] **Step 3: Preview the skill through the Skills CLI**

Run:

```bash
npm run skills:use:query
```

Expected: command exits 0 and output contains `query-wiki`.

- [ ] **Step 4: Commit `query-wiki`**

```bash
git add skills/query-wiki/SKILL.md evals/evals.json
git commit -m "feat: add query wiki skill"
```

Expected: commit succeeds.

## Task 6: Create `lint-wiki` With Personal Skill Creator

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/lint-wiki/SKILL.md`
- Modify if needed: `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`

- [ ] **Step 1: Use Skill Creator to author `lint-wiki`**

Invoke the personal Skill Creator workflow with this handoff prompt:

```text
Use the personal Skill Creator skill at /Users/shiyonghu/.agents/skills/skill-creator/SKILL.md to create skills/lint-wiki/SKILL.md from docs/superpowers/specs/2026-06-23-llm-wiki-design.md.

Do not reuse concrete SKILL.md bodies from old plans. Author a fresh skill.

The skill name must be lint-wiki.

The description must trigger on both "lint-wiki" and natural language requests for an Obsidian LLM wiki health check.

The skill must instruct the agent to:
- read /AGENTS.md when present
- read /index.md
- scan root-level Markdown notes and topic folders
- exclude .obsidian, /docs, /raw, hidden files, and system files
- look for contradictions, stale claims, missing cross-references, data gaps, important concepts without their own page, split candidates, merge candidates, rename/move candidates, and outdated index entries
- present a lint briefing grouped by severity and proposed action
- apply clear fixes after user approval
- keep uncertain findings as recommendations
- avoid modifying /raw contents
- preserve page atomicity and the 500-word limit
- update /index.md when pages are created, renamed, moved, split, or merged
- append /log.md with the lint pass summary and pages changed

The SKILL.md must include sections named:
- ## When To Use
- ## Required Reading
- ## Workflow
- ## Verification

Use skills/shared/wiki-conventions.md and skills/shared/obsidian-markdown.md as bundled references.
```

Expected: `skills/lint-wiki/SKILL.md` exists and follows Skill Creator guidance.

- [ ] **Step 2: Review `lint-wiki` against the handoff criteria**

Run:

```bash
sed -n '1,300p' skills/lint-wiki/SKILL.md
```

Expected: output shows YAML frontmatter with `name: lint-wiki`, a description that triggers on command-style and natural-language health-check requests, the required section headings, references to the shared files, exclusions, severity briefing, approval rules, raw immutability, and logging rules.

- [ ] **Step 3: Preview the skill through the Skills CLI**

Run:

```bash
npm run skills:use:lint
```

Expected: command exits 0 and output contains `lint-wiki`.

- [ ] **Step 4: Commit `lint-wiki`**

```bash
git add skills/lint-wiki/SKILL.md evals/evals.json
git commit -m "feat: add lint wiki skill"
```

Expected: commit succeeds.

## Task 7: README, License, And Package Documentation

**Files:**

- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/README.md`
- Create: `/Users/shiyonghu/workspace/obsidian-llm-wiki/LICENSE`

- [ ] **Step 1: Create README**

Create `/Users/shiyonghu/workspace/obsidian-llm-wiki/README.md` with these sections:

```text
# LLM Wiki Skills
## Purpose
## Vault Model
## Skills
## Install
## Usage
## Development
## Compatibility
## License
```

README acceptance criteria:

- Explains the LLM wiki pattern.
- Explains `/raw/todo`, `/raw`, `/raw/assets`, root-level wiki pages, `/index.md`, `/log.md`, and `/AGENTS.md`.
- Lists `init-wiki`, `ingest-wiki`, `query-wiki`, and `lint-wiki`.
- Includes usage examples from the spec.
- Uses current Skills CLI syntax verified by `npx --yes skills --help`: `npx skills add <owner>/llm-wiki-skills --skill init-wiki`, `--skill ingest-wiki`, `--skill query-wiki`, `--skill lint-wiki`, and `--all`.
- Notes that command-style phrasing is convenient but not required because descriptions also trigger on natural language.
- Explains `npm run skills:list` and the `npm run skills:use:*` commands.

- [ ] **Step 2: Create MIT license**

Create `/Users/shiyonghu/workspace/obsidian-llm-wiki/LICENSE`:

```text
MIT License

Copyright (c) 2026 shiyonghu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Verify local Skills CLI discovery**

Run:

```bash
npm run skills:list
```

Expected: output lists all four skill names:

```text
init-wiki
ingest-wiki
query-wiki
lint-wiki
```

- [ ] **Step 4: Preview all skills through the Skills CLI**

Run:

```bash
npm run skills:use:init
npm run skills:use:ingest
npm run skills:use:query
npm run skills:use:lint
```

Expected: all commands exit 0 and each preview contains the matching skill name.

- [ ] **Step 5: Commit docs**

```bash
git add README.md LICENSE
git commit -m "docs: add readme and license"
```

Expected: commit succeeds.

## Task 8: Skill Creator Evaluation Loop

**Files:**

- Modify if needed: `/Users/shiyonghu/workspace/obsidian-llm-wiki/skills/*/SKILL.md`
- Modify if needed: `/Users/shiyonghu/workspace/obsidian-llm-wiki/evals/evals.json`
- Create during evaluation: `/Users/shiyonghu/workspace/obsidian-llm-wiki/*-workspace/`

- [ ] **Step 1: Create Skill Creator evaluation todo**

Create a local execution checklist for the current implementer:

```text
- Run with-skill and baseline evaluations for init-wiki.
- Run with-skill and baseline evaluations for ingest-wiki.
- Run with-skill and baseline evaluations for query-wiki.
- Run with-skill and baseline evaluations for lint-wiki.
- Create evals JSON and run eval-viewer/generate_review.py so the human can review test cases.
- Capture timing.json as subagent notifications arrive.
- Grade outputs and aggregate benchmark results.
- Incorporate human feedback into SKILL.md revisions.
```

Expected: checklist exists in the implementer's task tracker or notes.

- [ ] **Step 2: Run evaluations using the personal Skill Creator workflow**

For each skill, follow the "Running and evaluating test cases" section in `/Users/shiyonghu/.agents/skills/skill-creator/SKILL.md`:

```text
Spawn with-skill and baseline runs in the same turn.
Save outputs under <skill-name>-workspace/iteration-1/.
Create eval_metadata.json for each eval.
Draft assertions while runs are in progress.
Capture timing.json from task notifications.
Grade outputs.
Aggregate benchmark results.
Run eval-viewer/generate_review.py.
Ask the user to review results.
Read feedback.json.
Revise the skill if feedback identifies issues.
Repeat until the user is satisfied or feedback is empty.
```

Expected: each skill has an evaluation workspace with iteration output, metadata, grading, benchmark files, and human-review artifacts.

- [ ] **Step 3: Preview skills after any Skill Creator revisions**

Run:

```bash
npm run skills:list
npm run skills:use:init
npm run skills:use:ingest
npm run skills:use:query
npm run skills:use:lint
```

Expected: all commands exit 0 and each skill preview contains the matching skill name.

- [ ] **Step 4: Commit evaluated skill revisions**

```bash
git add skills evals
git commit -m "test: evaluate wiki skills"
```

Expected: commit succeeds if evaluation produced file changes. If no files changed, skip the commit and record that evaluation required no revisions.

## Task 9: Publish Readiness And GitHub Push

**Files:**

- No required file changes.

- [ ] **Step 1: Confirm root repository status**

Run from `/Users/shiyonghu/workspace/obsidian-llm-wiki`:

```bash
git status --short
```

Expected: no output.

- [ ] **Step 2: Verify current Skills CLI command surface**

Run:

```bash
npx --yes skills --help
```

Expected: output includes:

```text
add <package>
use <package>@<skill>
--skill <skills>
--list
--full-depth
```

- [ ] **Step 3: Verify local install preview**

Run:

```bash
npx --yes skills add . --list --full-depth
```

Expected: output lists:

```text
init-wiki
ingest-wiki
query-wiki
lint-wiki
```

- [ ] **Step 4: Ask before public publishing**

Ask the user:

```text
Ready to publish this root repository to GitHub as shiyonghu/llm-wiki-skills?
```

Expected: user explicitly approves.

- [ ] **Step 5: Create or connect the GitHub repository**

If the remote does not exist, run after approval:

```bash
gh repo create shiyonghu/llm-wiki-skills --public --source=. --remote=origin --push
```

If the remote already exists, run after approval:

```bash
git remote add origin git@github.com:shiyonghu/llm-wiki-skills.git 2>/dev/null || true
git push -u origin main
```

Expected: push succeeds and GitHub shows `shiyonghu/llm-wiki-skills`.

- [ ] **Step 6: Verify remote Skills CLI discovery**

Run:

```bash
npx --yes skills add shiyonghu/llm-wiki-skills --list --full-depth
```

Expected: output lists:

```text
init-wiki
ingest-wiki
query-wiki
lint-wiki
```

## Self-Review

Spec coverage:

- Repository layout: covered with root-level `skills/`, `skills/shared/`, `evals/`, `README.md`, and `LICENSE`.
- User repo-root note: covered by using `/Users/shiyonghu/workspace/obsidian-llm-wiki` as the git root.
- User no concrete skill-body note: covered by Skill Creator handoff prompts and no embedded `SKILL.md` bodies.
- Four exact skill names: covered in file structure, tasks, evals, Skill Creator handoff prompts, and CLI checks.
- Vault structure: covered in shared requirements, shared references, and Skill Creator handoff prompts.
- Ownership rules: covered for `/raw/todo`, `/raw`, `.obsidian`, root synthesis layer, and operating files.
- Page conventions: covered for atomicity, executive summaries, word limits, wikilinks, paths, and source sections.
- Ingest workflow: covered for briefing, approval gates, page creation/update, outbound links, contradictions, quotes, Chinese concept English names, finalization, index/log/source archival.
- Query workflow: covered for reading index first, wiki-first search, raw source limits, durable synthesis, and logging.
- Lint workflow: covered for exclusions, health checks, severity briefing, approved fixes, recommendations, logging, and raw immutability.
- Skill tests: covered in `evals/evals.json` and Skill Creator evaluation loop.
- Success criteria: covered by root wiki model, `AGENTS.md`, `/index.md`, `/log.md`, `/raw/todo`, and `/raw` archive rules.

Placeholder scan:

- No forbidden placeholder markers or vague test instructions remain.
- Skill body details are intentionally delegated to Skill Creator because the user explicitly requested that the plan not contain concrete `SKILL.md` file contents.

Type and name consistency:

- Paths consistently use `/Users/shiyonghu/workspace/obsidian-llm-wiki` as root.
- Skill names consistently use `init-wiki`, `ingest-wiki`, `query-wiki`, and `lint-wiki`.
- CLI preview commands match the planned file structure.

