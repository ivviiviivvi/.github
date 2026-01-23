# MCP Collection Standardization Guide

> **Status**: ✅ Completed - January 20, 2026

This document describes the standardization implemented for Model Context Protocol (MCP) collections in the repository.

## Overview

MCP collections provide complete development toolkits for building MCP servers across 11+ programming languages. This standardization ensures consistency, validation, and maintainability across all MCP-related resources.

## What Was Standardized

### 1. Frontmatter Format

**Before (Incorrect):**
```yaml
---

## name: Python MCP Development description: Collection for Python MCP Development. tags: \[\] updated: 2026-01-13

# Python MCP Server Development
```

**After (Correct):**
```yaml
---
name: Python MCP Development
description: Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP. Includes instructions for best practices, a prompt for generating servers, and an expert chat mode for guidance.
tags: []
updated: 2026-01-13
---

# Python MCP Server Development
```

### 2. Collection Files Standardized

All 27 collection files were updated:

#### MCP Collections (11)
1. `python-mcp-development.md`
2. `typescript-mcp-development.md`
3. `java-mcp-development.md`
4. `csharp-mcp-development.md`
5. `go-mcp-development.md`
6. `rust-mcp-development.md`
7. `ruby-mcp-development.md`
8. `php-mcp-development.md`
9. `swift-mcp-development.md`
10. `kotlin-mcp-development.md`
11. `power-platform-mcp-connector-development.md`

#### Other Collections (16)
- `awesome-copilot.md`
- `azure-cloud-development.md`
- `clojure-interactive-programming.md`
- `csharp-dotnet-development.md`
- `database-data-management.md`
- `devops-oncall.md`
- `edge-ai-tasks.md`
- `frontend-web-dev.md`
- `java-development.md`
- `partners.md`
- `power-apps-code-apps.md`
- `power-bi-development.md`
- `project-planning.md`
- `security-best-practices.md`
- `technical-spike.md`
- `testing-automation.md`

#### Meta Files
- `TEMPLATE.md`

### 3. Documentation Updates

1. **SCHEMA.md**: Enhanced with:
   - Clear standardization requirements
   - Correct vs incorrect examples
   - MCP-specific standards
   - Validation instructions
   - Standardization script reference

2. **README.md**: Added:
   - Collection standards section
   - Validation instructions
   - MCP collections overview table
   - Component descriptions

3. **MCP_STANDARDIZATION_GUIDE.md** (this file): Complete reference

## Standardization Rules

### Required Frontmatter Fields

```yaml
name: string          # Display name (Title Case)
description: string   # One-sentence description
```

### Optional Frontmatter Fields

```yaml
tags: array          # List of discovery keywords (can be empty: [])
updated: string      # Date in YYYY-MM-DD format
```

### MCP Collection Naming Convention

Format: `{language}-mcp-development`

Examples:
- `python-mcp-development`
- `typescript-mcp-development`
- `csharp-mcp-development`

### MCP Collection Description Pattern

Follow this template:
```
"Complete toolkit for building Model Context Protocol (MCP) servers in {Language} using the official SDK..."
```

### MCP Collection Tags

Must include at minimum:
- Language identifier: `python`, `typescript`, `java`, etc.
- `mcp`
- `model-context-protocol`
- `server-development`

Optional tags:
- Framework: `fastmcp`, `nodejs`, `dotnet`, etc.
- SDK: `sdk`, `rmcp`, etc.

## Validation

### Running Validation

```bash
# From repository root
python3 automation/scripts/validate_collection_frontmatter.py
```

Expected output:
```
Collection frontmatter validation passed.
```

### What Gets Validated

1. ✅ Proper YAML frontmatter format
2. ✅ Required fields present (`name`, `description`)
3. ✅ Frontmatter at top of file
4. ✅ Correct delimiter placement (`---`)
5. ✅ No inline comment format

## Automated Standardization

### Standardization Script

Location: `scripts/standardize-mcp-collections.py`

#### What It Does

1. Detects malformed frontmatter (inline comment format)
2. Extracts metadata from corresponding `.yml` files
3. Rewrites frontmatter in proper YAML format
4. Preserves all file content below frontmatter

#### Running the Script

```bash
# From repository root
python3 scripts/standardize-mcp-collections.py
```

#### Output Example

```
Processing python-mcp-development.md...
  ✓ Fixed frontmatter in python-mcp-development.md
Processing typescript-mcp-development.md...
  ✓ Fixed frontmatter in typescript-mcp-development.md
...
Fixed 27 collection files
```

## MCP Collections Structure

Each MCP collection includes three components:

### 1. Instructions File
**Path**: `ai_framework/instructions/{language}-mcp-server.instructions.md`
**Purpose**: Best practices and coding standards for MCP development in that language

### 2. Prompt File
**Path**: `ai_framework/prompts/{language}-mcp-server-generator.prompt.md`
**Purpose**: Project scaffolding generator for new MCP server projects

### 3. Chat Mode File
**Path**: `ai_framework/chatmodes/{language}-mcp-expert.chatmode.md`
**Purpose**: Expert assistant for implementation guidance and troubleshooting

## Consistency Between .yml and .md Files

Each collection exists in two formats:
- `.collection.yml` - Machine-readable YAML
- `.md` - Human-readable Markdown

### Requirements

1. Both files must have **identical frontmatter**
2. The `.md` file contains additional formatted content
3. The `.yml` file contains structured collection data

### Example Alignment

**python-mcp-development.collection.yml:**
```yaml
---
name: Python MCP Development
description: Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP. Includes instructions for best practices, a prompt for generating servers, and an expert chat mode for guidance.
tags: []
updated: 2026-01-13
---
```

**python-mcp-development.md:**
```yaml
---
name: Python MCP Development
description: Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP. Includes instructions for best practices, a prompt for generating servers, and an expert chat mode for guidance.
tags: []
updated: 2026-01-13
---
```

## Benefits of Standardization

1. **Validation**: Automated checking ensures all collections meet requirements
2. **Consistency**: Uniform format across all 11 MCP collections
3. **Maintainability**: Easy to update and manage collections
4. **Discoverability**: Standard structure helps with search and navigation
5. **Quality**: Clear guidelines prevent formatting errors
6. **Automation**: Enables scripted updates and validation

## Future Enhancements

Potential improvements for MCP collections:

1. **Tag Enforcement**: Add allowed tags list to validation
2. **Description Validation**: Check for MCP-specific terminology
3. **Component Validation**: Ensure all three files exist for each MCP collection
4. **Version Tracking**: Add version fields for SDK compatibility
5. **Automated Updates**: Script to update multiple collections at once

## Related Documentation

- [SCHEMA.md](../ai_framework/collections/SCHEMA.md) - Frontmatter schema specification
- [README.md](../ai_framework/collections/README.md) - Collections overview
- [MCP_SERVER_SETUP.md](MCP_SERVER_SETUP.md) - MCP server configuration guide
- [CUSTOM_INSTRUCTIONS_SETUP.md](CUSTOM_INSTRUCTIONS_SETUP.md) - Instructions setup guide

## Maintenance

### Adding New MCP Collections

When adding a new MCP collection:

1. Create all three component files (instructions, prompt, chat mode)
2. Create both `.yml` and `.md` versions
3. Use proper frontmatter format
4. Follow naming conventions
5. Include required tags
6. Run validation script
7. Update README.md table

### Updating Existing Collections

When updating:

1. Maintain frontmatter format
2. Keep `.yml` and `.md` versions in sync
3. Update `updated` field with current date
4. Run validation after changes
5. Test with validation script

## Support

For questions or issues:

1. Check [SCHEMA.md](../ai_framework/collections/SCHEMA.md) for format details
2. Review validation error messages
3. Run standardization script if needed
4. Open an issue if validation rules need adjustment

---

**Last Updated**: January 20, 2026  
**Status**: Active  
**Maintained By**: Organization Maintainers
