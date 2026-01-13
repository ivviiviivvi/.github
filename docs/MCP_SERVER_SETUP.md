# Model Context Protocol (MCP) Server Setup Guide

> **Comprehensive guide to configuring and using MCP servers with GitHub Copilot**

## Table of Contents

- [Overview](#overview)
- [What is MCP?](#what-is-mcp)
- [MCP Servers in This Organization](#mcp-servers-in-this-organization)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Available MCP Development Resources](#available-mcp-development-resources)
  - [By Language](#by-language)
  - [Chat Modes](#chat-modes)
  - [Prompts](#prompts)
  - [Instructions](#instructions)
  - [Collections](#collections)
- [Using MCP Servers with Agents](#using-mcp-servers-with-agents)
- [Building Your Own MCP Server](#building-your-own-mcp-server)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

---

## Overview

Model Context Protocol (MCP) is an open standard that enables seamless integration between AI applications and data sources. MCP servers extend GitHub Copilot's capabilities by providing specialized tools, resources, and prompts that can be invoked during AI-assisted development.

This guide covers:
- Understanding MCP and its benefits
- Configuring MCP servers for use with GitHub Copilot
- Leveraging existing MCP development resources in this organization
- Building custom MCP servers for your specific needs

---

## What is MCP?

**Model Context Protocol (MCP)** is a universal, open protocol that standardizes how applications provide context to Large Language Models (LLMs). Think of MCP servers as plugins that give AI assistants like GitHub Copilot access to:

- **Tools**: Execute functions and operations (e.g., search databases, call APIs, run scripts)
- **Resources**: Access data and content (e.g., files, documentation, metrics)
- **Prompts**: Reusable prompt templates for common tasks

### Why Use MCP?

- **Extend Capabilities**: Give Copilot access to your organization's tools and data
- **Standardization**: Use a unified protocol across different AI tools
- **Flexibility**: Connect to any service or data source through custom servers
- **Reusability**: Build once, use across multiple AI applications
- **Open Source**: Built on open standards with community-driven development

### Key Concepts

- **MCP Client**: The AI application (GitHub Copilot, Claude Desktop, etc.)
- **MCP Server**: Provides tools, resources, and prompts to the client
- **Transport**: Communication layer (stdio for local, HTTP/SSE for remote)
- **Schema**: Type definitions for tools and resources using JSON Schema

---

## MCP Servers in This Organization

This organization provides comprehensive support for MCP development across **11 programming languages**:

| Language | Chat Mode | Prompt | Instructions | Collection |
|----------|-----------|--------|--------------|------------|
| **Python** | ✅ | ✅ | ✅ | ✅ |
| **TypeScript** | ✅ | ✅ | ✅ | ✅ |
| **Java** | ✅ | ✅ | ✅ | ✅ |
| **C#** | ✅ | ✅ | ✅ | ✅ |
| **Go** | ✅ | ✅ | ✅ | ✅ |
| **Rust** | ✅ | ✅ | ✅ | ✅ |
| **Ruby** | ✅ | ✅ | ✅ | ✅ |
| **PHP** | ✅ | ✅ | ✅ | ✅ |
| **Swift** | ✅ | ✅ | ✅ | ✅ |
| **Kotlin** | ✅ | ✅ | ✅ | ✅ |
| **Power Platform** | ✅ | ✅ | ✅ | ✅ |

---

## Getting Started

### Prerequisites

Before setting up MCP servers, ensure you have:

1. **GitHub Copilot** installed and activated in VS Code
2. **VS Code** or **VS Code Insiders** (version 1.80 or later)
3. **Development tools** for your chosen language (Python 3.10+, Node.js 18+, etc.)
4. **Git** for cloning repositories

### Installation

MCP servers can be installed in two ways:

#### Option 1: Quick Install (Recommended)

Use the provided installation badges to automatically install MCP resources:

1. Navigate to the language-specific collection (e.g., `collections/python-mcp-development.md`)
2. Click the **"Install in VS Code"** badge for each component
3. Follow the prompts in VS Code to complete installation

#### Option 2: Manual Installation

1. **Clone this repository** (or copy the relevant files):
   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   ```

2. **Copy MCP resources** to your project or VS Code settings directory:
   - **Instructions**: Copy to `.github/copilot-instructions/` in your project
   - **Chat Modes**: Install via VS Code's chat mode settings
   - **Prompts**: Install via VS Code's prompt settings

3. **Configure VS Code** to recognize the custom resources:
   - Open VS Code Settings (`Cmd/Ctrl + ,`)
   - Search for "Copilot"
   - Ensure custom instructions and chat modes are enabled

### Configuration

#### For Local Development (stdio transport)

MCP servers using stdio transport run as separate processes and communicate through standard input/output.

**Example: Python MCP Server Configuration**

Create or edit your VS Code settings (`settings.json`):

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "servers": {
        "my-python-server": {
          "command": "python",
          "args": ["/path/to/your/server.py"],
          "env": {
            "PYTHONPATH": "/path/to/dependencies"
          }
        }
      }
    }
  }
}
```

#### For Remote Services (HTTP/SSE transport)

For MCP servers hosted as web services:

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "servers": {
        "my-remote-server": {
          "url": "https://your-server.example.com/mcp",
          "transport": "sse"
        }
      }
    }
  }
}
```

---

## Available MCP Development Resources

### By Language

Each language has a complete development toolkit including:

#### Python
- **Collection**: [`collections/python-mcp-development.md`](../collections/python-mcp-development.md)
- **Chat Mode**: [`chatmodes/python-mcp-expert.chatmode.md`](../chatmodes/python-mcp-expert.chatmode.md)
- **Instructions**: [`instructions/python-mcp-server.instructions.md`](../instructions/python-mcp-server.instructions.md)
- **Prompt**: [`prompts/python-mcp-server-generator.prompt.md`](../prompts/python-mcp-server-generator.prompt.md)
- **SDK**: `mcp` package with FastMCP for rapid development
- **Transport**: stdio (local) or streamable HTTP (remote)

**Quick Start:**
```bash
# Install dependencies
pip install mcp fastmcp

# Generate a new server
# Use the prompt: /python-mcp-server-generator

# Test the server
uv run mcp dev server.py
```

#### TypeScript
- **Collection**: [`collections/typescript-mcp-development.md`](../collections/typescript-mcp-development.md)
- **Chat Mode**: [`chatmodes/typescript-mcp-expert.chatmode.md`](../chatmodes/typescript-mcp-expert.chatmode.md)
- **Instructions**: [`instructions/typescript-mcp-server.instructions.md`](../instructions/typescript-mcp-server.instructions.md)
- **Prompt**: [`prompts/typescript-mcp-server-generator.prompt.md`](../prompts/typescript-mcp-server-generator.prompt.md)
- **SDK**: `@modelcontextprotocol/sdk`
- **Transport**: stdio or SSE

**Quick Start:**
```bash
# Install dependencies
npm install @modelcontextprotocol/sdk zod

# Generate a new server
# Use the prompt: /typescript-mcp-server-generator

# Build and test
npm run build
node build/index.js
```

#### Java
- **Collection**: [`collections/java-mcp-development.md`](../collections/java-mcp-development.md)
- **Chat Mode**: [`chatmodes/java-mcp-expert.chatmode.md`](../chatmodes/java-mcp-expert.chatmode.md)
- **Instructions**: [`instructions/java-mcp-server.instructions.md`](../instructions/java-mcp-server.instructions.md)
- **Prompt**: [`prompts/java-mcp-server-generator.prompt.md`](../prompts/java-mcp-server-generator.prompt.md)
- **SDK**: Maven/Gradle MCP SDK
- **Transport**: stdio or SSE

#### C# (.NET)
- **Collection**: [`collections/csharp-mcp-development.md`](../collections/csharp-mcp-development.md)
- **Chat Mode**: [`chatmodes/csharp-mcp-expert.chatmode.md`](../chatmodes/csharp-mcp-expert.chatmode.md)
- **Instructions**: [`instructions/csharp-mcp-server.instructions.md`](../instructions/csharp-mcp-server.instructions.md)
- **Prompt**: [`prompts/csharp-mcp-server-generator.prompt.md`](../prompts/csharp-mcp-server-generator.prompt.md)
- **SDK**: `ModelContextProtocol` NuGet packages
- **Transport**: stdio or HTTP

**Quick Start:**
```bash
# Install SDK
dotnet add package ModelContextProtocol.SDK

# Generate a new server
# Use the prompt: /csharp-mcp-server-generator

# Build and run
dotnet build
dotnet run
```

#### Go
- **Collection**: [`collections/go-mcp-development.md`](../collections/go-mcp-development.md)
- **Chat Mode**: [`chatmodes/go-mcp-expert.chatmode.md`](../chatmodes/go-mcp-expert.chatmode.md)
- **Instructions**: [`instructions/go-mcp-server.instructions.md`](../instructions/go-mcp-server.instructions.md)
- **Prompt**: [`prompts/go-mcp-server-generator.prompt.md`](../prompts/go-mcp-server-generator.prompt.md)

#### Additional Languages
- **Rust**: Full toolkit with cargo integration
- **Ruby**: Rails-friendly MCP servers
- **PHP**: PSR-compliant MCP implementation
- **Swift**: iOS/macOS MCP integration
- **Kotlin**: Android and JVM support
- **Power Platform**: Low-code MCP connectors

### Chat Modes

Chat modes provide expert assistance for MCP development:

- Activate by typing `@<mode-name>` in GitHub Copilot Chat
- Each mode specializes in a specific language and MCP SDK
- Provides best practices, debugging help, and code generation
- Understands the nuances of each MCP implementation

**Example Usage:**
```
@python-mcp-expert How do I implement a tool with structured output?
@typescript-mcp-expert What's the best way to handle errors in MCP servers?
@csharp-mcp-expert How do I configure dependency injection for my MCP server?
```

### Prompts

Prompts are reusable commands for generating MCP server code:

- Access via `/` commands in Copilot Chat
- Generate complete MCP server projects with proper structure
- Include testing setup and documentation
- Follow language-specific best practices

**Example Usage:**
```
/python-mcp-server-generator Create a server for managing GitHub issues
/typescript-mcp-server-generator Build a server that connects to Slack
/csharp-mcp-server-generator Generate a server for Azure DevOps integration
```

### Instructions

Instructions provide coding standards and best practices:

- Automatically apply to MCP server files based on file patterns
- Ensure consistency across your codebase
- Include type safety guidelines, error handling patterns, and testing approaches
- Language-specific optimizations and idioms

**File Patterns:**
- Python: `**/*mcp*server*.py`, `**/mcp/*.py`
- TypeScript: `**/*mcp*server*.ts`, `**/mcp/*.ts`
- C#: `**/*Mcp*Server*.cs`, `**/Mcp/*.cs`
- etc.

### Collections

Collections bundle related MCP resources by language:

- Complete development toolkit in one place
- Easy installation with one-click badges
- Curated for optimal developer experience
- Regularly updated with new patterns and examples

**Available Collections:**
- `python-mcp-development.collection.yml`
- `typescript-mcp-development.collection.yml`
- `java-mcp-development.collection.yml`
- `csharp-mcp-development.collection.yml`
- `go-mcp-development.collection.yml`
- `rust-mcp-development.collection.yml`
- `ruby-mcp-development.collection.yml`
- `php-mcp-development.collection.yml`
- `swift-mcp-development.collection.yml`
- `kotlin-mcp-development.collection.yml`
- `power-platform-mcp-connector-development.collection.yml`

---

## Using MCP Servers with Agents

Custom agents in this organization can leverage MCP servers for enhanced capabilities:

### Agent + MCP Integration Pattern

```yaml
---
name: DataAnalysisAgent
description: Analyzes data using specialized MCP servers
tools:
  - github/*
  - shell
mcp-servers:
  - postgres-mcp-server  # Database access
  - analytics-mcp-server # Analytics tools
  - visualization-mcp    # Chart generation
---

# Agent implementation
This agent uses MCP servers to:
1. Query databases through postgres-mcp-server
2. Perform analysis using analytics-mcp-server
3. Generate visualizations via visualization-mcp
```

### Example: Agent with MCP Server

See [`agents/octopus-deploy-release-notes-mcp.agent.md`](../agents/octopus-deploy-release-notes-mcp.agent.md) for a real-world example of an agent that integrates with an MCP server.

**Architecture:**
```
┌─────────────────┐
│  GitHub Copilot │
└────────┬────────┘
         │ invokes
         ▼
┌─────────────────┐
│  Custom Agent   │
└────────┬────────┘
         │ calls
         ▼
┌─────────────────┐
│   MCP Server    │──► External APIs/Data
└─────────────────┘
```

---

## Building Your Own MCP Server

### Step-by-Step Guide

#### 1. Choose Your Language

Select a language based on:
- **Team expertise**: Use what your team knows
- **Performance needs**: Go/Rust for high-performance, Python for rapid development
- **Integration requirements**: TypeScript for Node.js ecosystems, C# for .NET, etc.
- **Transport needs**: stdio for local tools, HTTP for remote services

#### 2. Generate Server Scaffold

Use the language-specific prompt to generate a starting point:

```
/python-mcp-server-generator Create a server named "github-metrics" that provides tools for analyzing GitHub repository statistics
```

This will create:
- Server entry point with proper configuration
- Example tool implementations
- Type definitions and schemas
- Testing setup
- README with usage instructions

#### 3. Implement Your Tools

Add tools that your AI assistant can invoke:

**Python Example:**
```python
from mcp import FastMCP
from typing import TypedDict

mcp = FastMCP("github-metrics")

class RepoStats(TypedDict):
    stars: int
    forks: int
    issues: int
    pull_requests: int

@mcp.tool()
async def get_repo_stats(owner: str, repo: str) -> RepoStats:
    """
    Get statistics for a GitHub repository.
    
    Args:
        owner: Repository owner username
        repo: Repository name
    
    Returns:
        Repository statistics including stars, forks, issues, and PRs
    """
    # Implementation here
    return {
        "stars": 1234,
        "forks": 567,
        "issues": 89,
        "pull_requests": 45
    }
```

#### 4. Add Resources

Resources provide read-only access to data:

**Python Example:**
```python
@mcp.resource("github://repos/{owner}/{repo}/readme")
async def get_readme(owner: str, repo: str) -> str:
    """Get repository README content."""
    # Implementation here
    return "# Repository README\n..."
```

#### 5. Define Prompts (Optional)

Reusable prompt templates for common tasks:

**Python Example:**
```python
@mcp.prompt()
async def analyze_repo_prompt(owner: str, repo: str) -> str:
    """Generate a prompt for analyzing a repository."""
    stats = await get_repo_stats(owner, repo)
    return f"""
Analyze the GitHub repository {owner}/{repo} with the following statistics:
- Stars: {stats['stars']}
- Forks: {stats['forks']}
- Open Issues: {stats['issues']}
- Open PRs: {stats['pull_requests']}

Provide insights on the repository's health and activity.
"""
```

#### 6. Test Your Server

**Local Testing (stdio):**
```bash
# Python
uv run mcp dev server.py

# TypeScript
npx @modelcontextprotocol/inspector node build/index.js

# C#
dotnet run --project YourServer.csproj
```

**Integration Testing:**
Configure in VS Code settings and test with GitHub Copilot Chat.

#### 7. Deploy Your Server

**For Local Use:**
- Keep server on developer machines
- Configure via VS Code settings
- Use stdio transport

**For Team Use:**
- Host as a web service
- Use HTTP/SSE transport
- Add authentication and rate limiting
- Document API endpoints

---

## Troubleshooting

### Common Issues

#### Server Not Connecting

**Symptom:** GitHub Copilot doesn't recognize your MCP server

**Solutions:**
1. Check VS Code settings for correct server configuration
2. Verify the server process starts without errors
3. Check logs in Output panel (View > Output > GitHub Copilot)
4. Ensure the command path is absolute and correct
5. Restart VS Code after configuration changes

#### Type/Schema Errors

**Symptom:** Tools don't work or show incorrect parameters

**Solutions:**
1. Ensure all function parameters have type hints (Python) or type annotations (TypeScript/Java/C#)
2. Verify return types are properly defined
3. Use Pydantic models, TypedDicts, or dataclasses for complex types
4. Check that schemas are properly generated and exposed
5. Test schema validation with sample inputs

#### Transport Issues

**Symptom:** Server times out or communication fails

**Solutions:**
1. For stdio: Ensure the server isn't writing to stdout except MCP messages
2. For HTTP: Check CORS configuration and port accessibility
3. Verify firewall rules allow communication
4. Check for conflicting environment variables
5. Enable debug logging in the MCP SDK

#### Performance Problems

**Symptom:** Server responds slowly or times out

**Solutions:**
1. Use async/await for I/O operations
2. Implement caching for expensive operations
3. Add timeouts to external API calls
4. Use connection pooling for databases
5. Profile your code to identify bottlenecks
6. Consider implementing pagination for large datasets

---

## Best Practices

### Security

- **Never expose secrets**: Use environment variables or secure vaults
- **Validate inputs**: Sanitize all parameters before processing
- **Rate limiting**: Implement limits to prevent abuse
- **Authentication**: Secure remote MCP servers with tokens
- **Least privilege**: Grant minimal necessary permissions
- **Audit logging**: Log all sensitive operations

### Performance

- **Async by default**: Use async/await for all I/O operations
- **Connection pooling**: Reuse database and HTTP connections
- **Caching**: Cache expensive computations and API responses
- **Lazy loading**: Only load resources when needed
- **Timeouts**: Set reasonable timeouts for all operations
- **Resource cleanup**: Properly close connections and files

### Maintainability

- **Type safety**: Use comprehensive type hints/annotations
- **Documentation**: Write clear docstrings for all tools and resources
- **Testing**: Include unit tests and integration tests
- **Error handling**: Provide helpful error messages
- **Logging**: Use structured logging for debugging
- **Versioning**: Version your MCP server API

### Developer Experience

- **Clear naming**: Use descriptive tool and parameter names
- **Good descriptions**: Write helpful documentation strings
- **Sensible defaults**: Provide default values where appropriate
- **Examples**: Include usage examples in documentation
- **Validation**: Return clear validation errors
- **Progress reporting**: Use progress updates for long operations

---

## Additional Resources

### Official Documentation

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK Documentation](https://github.com/modelcontextprotocol/typescript-sdk)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)

### Organization Resources

- [Agent Architecture Guide](AGENT_ARCHITECTURE_GUIDE.md) - Building custom agents
- [Agent Registry](AGENT_REGISTRY.md) - Catalog of available agents
- [Custom Instructions Guide](CUSTOM_INSTRUCTIONS_SETUP.md) - Setting up coding standards
- [Development Environment Setup](DEVELOPMENT_ENVIRONMENT_SETUP.md) - Configuring your dev environment

### Language-Specific Guides

Each language collection includes:
- SDK installation instructions
- Best practices for that language
- Common patterns and examples
- Debugging tips
- Performance optimization guides

### Community

- [GitHub Discussions](https://github.com/orgs/ivviiviivvi/discussions) - Ask questions and share ideas
- [Issue Tracker](https://github.com/ivviiviivvi/.github/issues) - Report bugs or request features
- [Contributing Guide](CONTRIBUTING.md) - Contribute to this documentation

---

## Next Steps

1. **Choose a language** from the [Available MCP Development Resources](#available-mcp-development-resources)
2. **Install the collection** using the one-click install badges
3. **Generate a server** using the language-specific prompt
4. **Test locally** with the MCP inspector or dev tools
5. **Configure in VS Code** to use with GitHub Copilot
6. **Build your first tool** that solves a real problem
7. **Share with your team** and iterate based on feedback

---

**Questions or Issues?**
- Check the [Troubleshooting](#troubleshooting) section
- Review [GitHub Copilot Actions Setup](GITHUB_COPILOT_ACTIONS_SETUP.md) for CI/CD integration
- Open an issue in this repository
- Ask in GitHub Discussions

---

*Last Updated: 2025-12-31*
