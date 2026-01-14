# Prompt Frontmatter Schema

This document defines the expected YAML frontmatter for prompt templates in
`ai_framework/prompts/`.

## Required keys

- `name`: short display name
- `description`: one sentence, user-facing

## Optional keys

- `tags`: list of keywords
- `updated`: YYYY-MM-DD
- `model`: preferred model identifier
- `variables`: list of template variables

## Example

```yaml
---
name: Incident Summary Prompt
description: Summarize incident impact and remediation steps.
variables:
  - incident_id
  - owner
  - timeline
tags:
  - incident
  - reporting
updated: 2026-01-13
---
```

## Validation rules

- Frontmatter must be valid YAML and appear once at the top of the file.
- Use lowercase keys and list values for `tags` and `variables`.
- Avoid inline YAML on a single line for multi-value fields.
