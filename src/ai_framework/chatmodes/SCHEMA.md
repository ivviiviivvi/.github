# Chatmode Frontmatter Schema

This document defines the expected YAML frontmatter for chatmodes in
`ai_framework/chatmodes/`.

## Required keys

- `name`: short display name
- `description`: one sentence, user-facing
- `tools`: list of tool identifiers

## Optional keys

- `tags`: list of keywords
- `version`: semantic version or date
- `owner`: team or handle
- `updated`: YYYY-MM-DD

## Example

```yaml
---
name: Plan Mode
description: Strategic planning and architecture assistant focused on analysis.
tools:
  - codebase
  - search
  - findTestFiles
tags:
  - planning
  - architecture
version: 1.0.0
owner: ai-framework
updated: 2026-01-13
---
```

## Validation rules

- Frontmatter must be valid YAML and appear once at the top of the file.
- Use lowercase keys and list values for `tools` and `tags`.
- Avoid inline YAML on a single line for multi-value fields.
- Do not insert extra `---` blocks inside the body.

## Known divergence

Some chatmodes use `## description:` lines and inline `tools:` lists inside the
body. These should be migrated to the YAML frontmatter format above.
