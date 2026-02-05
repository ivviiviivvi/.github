______________________________________________________________________

## name: Schema description: Collection frontmatter schema and validation rules for ai_framework/collections/. tags: \[\] updated: 2026-01-20

# Collection Frontmatter Schema

This document defines the expected YAML frontmatter for collections in
`ai_framework/collections/`.

## Standardization Requirements

All collection files (both `.md` and `.yml` formats) **MUST** have valid YAML
frontmatter at the top of the file following this exact format:

```yaml
---
name: Collection Name
description: Brief description of the collection purpose.
tags: []
updated: YYYY-MM-DD
---
```

### Important Notes

- **Do NOT use inline comment format**:
  `## name: X description: Y tags: [] updated: Z`
- **Do use proper YAML frontmatter**: Multi-line YAML block enclosed in `---`
  delimiters
- Frontmatter must appear at the **top** of the file (first line must be `---`)
- All keys must be lowercase
- Tags must be a proper YAML list (either `[]` for empty or multi-line list
  format)

## Required Keys

- `name`: Short display name (string)

  - Example: `"Python MCP Development"`
  - Format: Title case, concise

- `description`: One-sentence user-facing description (string)

  - Example:
    `"Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP."`
  - Format: Should be clear and informative
  - Length: Typically 50-200 characters

## Optional Keys

- `tags`: List of discovery keywords (array)

  - Example:
    `[python, mcp, model-context-protocol, fastmcp, server-development]`
  - Format: Lowercase, hyphen-separated for multi-word tags
  - Can be empty: `[]`

- `updated`: Last update date (string)

  - Format: `YYYY-MM-DD`
  - Example: `"2026-01-20"`

## Complete Example

### Correct Format ✓

```yaml
---
name: Python MCP Development
description: Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP. Includes instructions for best practices, a prompt for generating servers, and an expert chat mode for guidance.
tags: []
updated: 2026-01-13
---

# Python MCP Server Development

Rest of the content...
```

### Incorrect Format ✗

```yaml
---

## name: Python MCP Development description: Collection for Python MCP Development. tags: \[\] updated: 2026-01-13

# Python MCP Server Development
```

## Validation

Run the validation script to check all collections:

```bash
python3 automation/scripts/validate_collection_frontmatter.py
```

### Validation Rules

1. Frontmatter must be valid YAML
1. Frontmatter must appear at the top of the file (first line: `---`)
1. All required keys must be present (`name`, `description`)
1. Keys must be lowercase
1. Tags must be a proper YAML list (not a string)
1. No inline YAML on a single line for multi-value fields

## MCP Collection Standards

For MCP (Model Context Protocol) collections specifically:

### Naming Convention

- Format: `{language}-mcp-development`
- Examples: `python-mcp-development`, `typescript-mcp-development`

### Required Tags

MCP collections should include relevant tags such as:

- Language: `python`, `typescript`, `java`, `csharp`, `go`, `rust`, `ruby`,
  `php`, `swift`, `kotlin`
- Core tag: `mcp`
- Standard: `model-context-protocol`
- Type: `server-development`
- Framework-specific: `fastmcp`, `nodejs`, `dotnet`, etc.

### Description Pattern

Descriptions should follow this pattern:

```
"Complete toolkit for building Model Context Protocol (MCP) servers in {Language} using the official SDK..."
```

## Standardization Script

To automatically fix malformed frontmatter, run:

```bash
python3 scripts/standardize-mcp-collections.py
```

This script:

1. Detects inline comment format frontmatter
1. Extracts metadata from corresponding `.yml` files
1. Rewrites frontmatter in proper YAML format
1. Preserves the rest of the file content
