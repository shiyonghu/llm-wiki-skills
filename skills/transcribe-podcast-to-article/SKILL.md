---
name: transcribe-podcast-to-article
description: Use when Codex needs to transcribe podcast, interview, lecture, or long-form audio into readable article-style Markdown, especially Mandarin/Chinese podcasts, with headings, clean punctuation, filler cleanup, no timestamp clutter, and no background music lyrics.
---

# Podcast Article Transcription

## Overview

Create polished Markdown transcripts that read like lightly edited articles while preserving the speaker's original wording. The target is not raw ASR: it is a readable transcript with headings, punctuation, coherent paragraphs, removed non-semantic filler, and no background music transcription.

Before working, read [references/style-guide.md](references/style-guide.md).

## Standard Workflow

1. Resolve the audio source and metadata.
   - If the user provides a local audio file, use it directly.
   - If the user provides an Apple Podcasts link, use the show id with `https://itunes.apple.com/lookup?id=<id>` to find `feedUrl`, then locate the episode `<enclosure>` URL in the RSS feed.
   - Capture episode title, description, official chapters, and source URL before transcription.
   - Build a small glossary from metadata and show notes: host names, book/app names, English acronyms, recurring terms, and likely ASR trouble spots.
   - Save downloaded audio beside the requested output or in the user's target folder.

2. Reuse or create a durable ASR cache.
   - First look for a matching cached ASR JSON and metadata file for the same audio, model, language, skip length, max length, and prompt.
   - Prefer local `mlx-whisper` with `mlx-community/whisper-large-v3-turbo` on Apple Silicon when no matching cache exists.
   - Keep the ASR backend swappable, but do not switch to cloud ASR unless the user asks or local ASR is unavailable.
   - Use `language="zh"` for Mandarin-heavy Chinese podcasts.
   - Use an initial prompt/glossary that requests Simplified Chinese, original wording, filler cleanup, punctuation, no music lyrics, and known proper nouns.
   - Save ASR segment JSON and metadata permanently before article formatting. Do not delete these cache files during cleanup.
   - For long audio, chunk into 15-30 minute pieces only when needed for ASR stability, then save or merge the resulting checkpoint JSON.

3. Convert raw ASR into article-style Markdown.
   - Use `scripts/transcribe_podcast_article.py` as the first-pass helper when practical.
   - Start from cached ASR JSON when available; do not re-transcribe just to retry formatting or polish.
   - Then use Codex/cloud reasoning for the human-quality editorial pass following the style guide. Avoid a slow local LLM polish pass unless cloud reasoning is unavailable or the user asks for local-only processing.
   - Do not leave timestamps in the final article unless the user explicitly asks for them.
   - Prefer official episode chapters as the article-pass units. If chapters are absent, split by clear spoken signposts or topic shifts.
   - Add headings based on official episode chapters, RSS show notes, or topic shifts in the transcript.
   - Review paragraph and heading boundaries after placing headings. Do not let a heading split a sentence, separate a setup sentence from the section it introduces, or leave orphaned fragments before/after a heading.

4. Verify before finishing.
   - Confirm the Markdown exists in the requested folder.
   - Scan the first page and tail of the file.
   - Scan around each heading and adjust paragraph placement when the surrounding sentences belong more naturally to the previous or next section.
   - Search for timestamp markers like `[12:34]`, intro music lyrics, and raw filler.
   - Keep durable ASR cache JSON/metadata. Remove temporary chunks, virtualenvs, and scratch drafts unless the user asks to keep them.

## Tooling

Preferred local setup:

```bash
brew install ffmpeg
python3 -m venv .transcribe-venv
.transcribe-venv/bin/python -m pip install mlx-whisper
```

Use a local venv near the working folder for temporary transcription dependencies. Do not commit or preserve the venv as a deliverable.

Resolve the helper path relative to this `SKILL.md`; in examples, replace `<skill-dir>` with this skill's installed or repository directory.

Run a full transcription with durable ASR cache:

```bash
python <skill-dir>/scripts/transcribe_podcast_article.py \
  input.m4a \
  --output input_rough.md \
  --title "Episode title" \
  --chapters chapters.txt \
  --asr-cache-dir .transcription-cache/input \
  --skip-initial-seconds 20 \
  --language zh
```

The helper reuses a matching cache on later runs. Cache files are named from audio stem, model, language, skip/max settings, and prompt hash, with adjacent `.asr.json` and `.meta.json` files.

Format an existing Whisper JSON checkpoint:

```bash
python <skill-dir>/scripts/transcribe_podcast_article.py \
  --from-json raw_transcript.json \
  --output article.md \
  --title "Episode title" \
  --chapters chapters.txt
```

Chapter file format:

```text
00:00 开场：这一期讲什么
13:12 误解一：笔记是用来储存信息的
25:36 笔记也要符合刻意练习的规则
```

## Quality Rules

Use the style guide as the source of truth. The most important rules are:

- Preserve original wording unless removing meaningless filler or collapsing verbal spelling.
- Add punctuation and paragraph breaks so it reads like a written article.
- Do not paraphrase the speaker's ideas into summary prose.
- Use source metadata and a glossary to protect proper nouns and recurring technical terms.
- Use official chapters as preferred article-pass boundaries.
- Omit background music, song lyrics, applause-only sections, and outro humming.
- Remove timestamps from final output.
- Keep meaningful spoken style when it carries tone, such as rhetorical questions and emphatic repetition.
- Fix obvious ASR errors only when context or metadata makes the correction safe.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Dumping raw ASR with no punctuation | Do a section-by-section article pass before delivery. |
| Keeping `[00:00]` timestamps | Remove timestamps unless requested. |
| Transcribing intro music lyrics | Skip music and begin with host speech. |
| Over-editing into a summary | Preserve wording; clean delivery, not meaning. |
| Letting a heading split setup from content | Move transition/setup sentences into the section they introduce. |
| Re-transcribing when polishing failed | Reuse cached ASR JSON and redo only formatting/editorial passes. |
| Deleting ASR cache with scratch files | Keep durable `.asr.json`/`.meta.json`; clean only temp chunks, venvs, and drafts. |
| Ignoring official chapters | Use chapters as first-choice section boundaries, then adjust by transcript flow. |

## Test Prompts

Use these for future forward-testing when subagents are explicitly available:

- "Use this local Mandarin podcast audio to make a full Markdown transcript. I want it to read like an article, no timestamps, no music lyrics."
- "Here is an Apple Podcasts episode link. Download the audio and create an article-style transcript in the target folder."
- "Transcribe this interview into Markdown and make sure headings do not split paragraphs or setup sentences from the sections they introduce."
- "Retry formatting this podcast transcript from its ASR cache without running Whisper again."
