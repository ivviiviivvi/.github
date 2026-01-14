# Agent Frontmatter Schema

This document defines the expected YAML frontmatter for agents in
`ai_framework/agents/`.

## Required keys

- `name`: short display name
- `description`: one sentence, user-facing

## Optional keys

- `tools`: list of tool identifiers
- `tags`: list of keywords
- `updated`: YYYY-MM-DD

## Example

```yaml
---
name: ADR Generator
description: Agent for creating Architectural Decision Records (ADRs).
tools: []
tags:
  - architecture
updated: 2026-01-13
---
```

## Validation rules

- Frontmatter must be valid YAML and appear once at the top of the file.
- Use lowercase keys and list values for `tools` and `tags`.
- Avoid inline YAML on a single line for multi-value fields.
