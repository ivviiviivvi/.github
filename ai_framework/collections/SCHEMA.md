---
name: Schema
description: Collection for MCP server development in Python.
tags: []
updated: 2026-01-13
---

# Collection Frontmatter Schema

This document defines the expected YAML frontmatter for collections in
`ai_framework/collections/`.

## Required keys

- `name`: short display name
- `description`: one sentence, user-facing

## Optional keys

- `tags`: list of keywords
- `updated`: YYYY-MM-DD

## Example

```yaml
---
name: Python MCP Development
description: Collection for MCP server development in Python.
tags:
  - python
  - mcp
updated: 2026-01-13
---
```

## Validation rules

- Frontmatter must be valid YAML and appear once at the top of the file.
- Use lowercase keys and list values for `tags`.
- Avoid inline YAML on a single line for multi-value fields.

## Allowed tags

Currently none. Add tags here before using them in collections.
