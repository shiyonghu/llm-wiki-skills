# Article-Style Podcast Transcript Guide

## Goal

Turn spoken podcast audio into a readable article transcript. Preserve what the speaker said, but remove delivery artifacts that only exist because speech is improvised.

## Keep

- The speaker's original wording and order of ideas.
- Rhetorical questions, first-person phrasing, emphasis, and repeated keywords when they carry meaning.
- English terms, book titles, acronyms, app names, and proper nouns.
- Casual tone when it is part of the podcast voice.

## Clean

- Add punctuation: `，。？！：；、（）《》“”`.
- Split long ASR runs into short paragraphs.
- Add Markdown headings for topic changes.
- Review heading boundaries after drafting: headings should not split a sentence, detach transition/setup sentences from the section they introduce, or leave orphaned fragments before or after the heading.
- Collapse verbal spelling and word explanations:
  - `PARA, P, A, R, A` -> `PARA`
  - `他姓吴，口天吴` -> `吴`
- Remove non-semantic filler:
  - `嗯`, `呃`, `uh`, `um`, `well`
  - repeated `那个那个`, `这个这个`
  - false starts that do not add meaning
- Remove repeated oral scaffolding when it is purely mechanical, but keep wording around it.

## Metadata and Glossary

Before the article pass, read available episode metadata: title, description, RSS notes, official chapters, and source URL. Extract a short glossary for names, book titles, app names, acronyms, and repeated technical terms.

Use the glossary to fix safe ASR errors, but do not invent terms that are not supported by metadata or transcript context.

## Do Not

- Do not summarize or paraphrase.
- Do not translate unless the user asks.
- Do not include timestamps unless requested.
- Do not transcribe background music, intro song lyrics, outro humming, applause-only moments, or non-speech ambience.
- Do not "improve" the argument by adding ideas the speaker did not say.
- Do not overcorrect into formal essay prose. It should still sound like the speaker.

## Headings

Prefer meaningful headings over timestamp headings. Sources for headings, in order:

1. Official chapter list or RSS show notes.
2. Clear spoken signposts such as "第一个误解", "第二步", "总结来说".
3. Topic shifts inferred from the transcript.

Use `##` for major sections and `###` only for genuine subsections.

After placing headings, read the paragraph before and after each heading. Move lead-in sentences into the new section when they introduce that section's topic, and keep the previous section ending as a complete thought.

When official chapters exist, use them as the default article-pass units. Polish each chapter as a coherent section, then do a final boundary pass across adjacent chapters to catch misplaced setup sentences.

## Punctuation Heuristics for Mandarin ASR

- Use `。` when a complete thought ends.
- Use `？` for rhetorical and explicit questions.
- Use `：` before examples, lists, and quoted internal thoughts.
- Use `；` to separate long parallel clauses.
- Use commas to restore breathing points, not after every phrase.
- Use quotes for remembered or imagined speech:
  - `大家就会想：“我明明记得它在这里，怎么找不到？”`

## Final Review

Before delivery, scan the opening, tail, every heading boundary, and glossary-sensitive terms. Confirm the transcript has no timestamps, no background music lyrics, useful headings, complete paragraphs, and wording that is preserved rather than summarized.
