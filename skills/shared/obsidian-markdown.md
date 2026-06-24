# Obsidian Markdown Reference

Use normal Markdown plus Obsidian wiki links for internal wiki references.

## Wiki Links

Link to a page by title when the target is unique:

```markdown
[[Page Name]]
```

Use a vault-root path and alias when the folder disambiguates the target or the displayed text should be shorter:

```markdown
[[folder/page|alias]]
```

Use heading links when pointing readers to a specific section is more useful than linking the whole page:

```markdown
[[Page Name#Heading]]
[[folder/page#Heading|alias]]
```

Prefer short links for well-named unique pages because they survive folder moves better and are easier to read. Prefer vault-root paths when multiple pages share a title, when a source link should clearly point into `/raw`, or when folder context is part of the meaning.

## Source Links

Link raw source files from page source sections with a vault-root path and readable alias:

```markdown
[[raw/source-file|source-file]]
```

## Asset Embeds

Embed images or attachments from `/raw/assets` when they are part of the source record:

```markdown
![[raw/assets/example-image.png]]
```

Keep source and asset references stable after ingest finalization by pointing them at `/raw` and `/raw/assets`, not `/raw/todo`.
