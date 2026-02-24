______________________________________________________________________

## name: Readme description: Collection for Readme. tags: \[\] updated: 2026-01-20

# Collections

Curated sets of prompts, instructions, and chat modes organized by theme or use
case.

## 📚 Collection Standards

All collections in this directory follow standardized formatting rules. See
[SCHEMA.md](SCHEMA.md) for complete details.

### ✅ Quick Standards Checklist

- **Frontmatter Format**: Proper YAML frontmatter (not inline comments)
- **Required Fields**: `name`, `description`
- **Optional Fields**: `tags`, `updated`
- **File Formats**: Both `.yml` (machine-readable) and `.md` (human-readable)
  versions

### 🔍 Validation

Check all collections for compliance:

```bash
python3 automation/scripts/validate_collection_frontmatter.py
```

## 🤖 MCP Collections

Model Context Protocol (MCP) collections provide complete toolkits for building
MCP servers across 11+ programming languages.

### MCP Collection Standards

All MCP collections follow these standards:

1. **Naming**: `{language}-mcp-development`
1. **Components**: Include instruction, prompt, and chat-mode resources
1. **Tags**: Must include `mcp`, `model-context-protocol`, and language-specific
   tags
1. **Description**: Follow standard format mentioning "Model Context Protocol"
   and SDK details

### Available MCP Collections

| Collection                                 | Language       | SDK                           |
| ------------------------------------------ | -------------- | ----------------------------- |
| `python-mcp-development`                   | Python         | `mcp` with FastMCP            |
| `typescript-mcp-development`               | TypeScript     | `@modelcontextprotocol/sdk`   |
| `java-mcp-development`                     | Java           | Official MCP Java SDK         |
| `csharp-mcp-development`                   | C#             | Official MCP .NET SDK         |
| `go-mcp-development`                       | Go             | `modelcontextprotocol/go-sdk` |
| `rust-mcp-development`                     | Rust           | `rmcp` SDK                    |
| `ruby-mcp-development`                     | Ruby           | Official MCP Ruby SDK gem     |
| `php-mcp-development`                      | PHP            | Official PHP SDK              |
| `swift-mcp-development`                    | Swift          | Official MCP Swift SDK        |
| `kotlin-mcp-development`                   | Kotlin         | `io.modelcontextprotocol:sdk` |
| `power-platform-mcp-connector-development` | Power Platform | Copilot Studio integration    |

Each MCP collection includes:

- 📋 **Instructions**: Best practices for that language/SDK
- 🎯 **Prompt**: Project generator for scaffolding new MCP servers
- 💬 **Chat Mode**: Expert assistant for implementation guidance

## 📦 All Collections

- **Count**: 55 files
- **Schema**: [SCHEMA.md](SCHEMA.md)
- **Inventory**: [INVENTORY.md](INVENTORY.md) (auto-generated)
- **Full catalog**:
  [docs/README.collections.md](../../docs/README.collections.md)

## 📝 Notes

- Prefer `.collection.yml` for structured bundles
- Both `.yml` and `.md` versions should have matching frontmatter
- Run validation before committing changes
