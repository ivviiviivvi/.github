# GitHub Copilot Enhancement Quick Start Guide

> **Get up and running with enhanced GitHub Copilot capabilities in 15 minutes**

## 🎯 What You'll Accomplish

By the end of this guide, you'll have:

- ✅ **Custom instructions** configured for consistent, high-quality code
  generation
- ✅ **MCP servers** set up for extended Copilot capabilities
- ✅ **Development environment** optimized for AI-assisted development
- ✅ **Custom agents** available for specialized tasks
- ✅ **Best practices** applied automatically

## ⏱️ Time Required

- **Minimal Setup**: 5 minutes (DevContainer)
- **Standard Setup**: 15 minutes (local installation)
- **Complete Setup**: 30 minutes (everything configured and customized)

---

## 🚀 Quick Start Paths

Choose your path based on your preferences and project needs:

### Path 1: DevContainer (Fastest) ⚡

**Best for**: Teams, complex projects, consistent environments

**Time**: 5 minutes setup + 5 minutes wait for first build

1. **Install prerequisites**:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

1. **Open project in container**:

   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   cd .github
   code .
   ```

1. **Reopen in container**:
   - Press `Cmd/Ctrl + Shift + P`
   - Select "Dev Containers: Reopen in Container"
   - Wait for build to complete

1. **Done!** Everything is pre-configured. Skip to [Verify Setup](#verify-setup)

### Path 2: Local Installation 🔧

**Best for**: Individual developers, existing setups, full control

**Time**: 15 minutes

1. **Install GitHub Copilot**:
   - Open VS Code Extensions (`Cmd/Ctrl + Shift + X`)
   - Install "GitHub Copilot" and "GitHub Copilot Chat"
   - Sign in when prompted

1. **Install custom instructions**:

   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   mkdir -p ~/.config/github-copilot-instructions
   cp .github/instructions/*.instructions.md ~/.config/github-copilot-instructions/
   ```

1. **Configure VS Code**:
   - Copy settings: `cp .github/.vscode/settings.json ~/.vscode/settings.json`
   - Restart VS Code

1. **Continue to** [Language-Specific Setup](#language-specific-setup)

### Path 3: Organization-Wide 🏢

**Best for**: Enterprises, organizations with multiple repos

**Time**: 10 minutes (admin), instant for users

1. **Admin**: Ensure this repository is your organization's `.github` repository

1. **Admin**: Verify files are in correct locations:
   - Instructions: `instructions/*.instructions.md`
   - Agents: `agents/*.agent.md`
   - Chat modes: `chatmodes/*.chatmode.md`

1. **Users**: Install GitHub Copilot in VS Code

1. **Users**: Clone any org repository - instructions apply automatically

---

## 🔍 Verify Setup

### Test Custom Instructions

1. **Create a test file**:

   ```bash
   # For Python
   echo "# Test file" > test.py
   code test.py
   ```

1. **Start typing**:

   ```python
   def calculate_average(
   ```

1. **Verify**: Copilot should suggest code following your organization's
   standards

### Test GitHub Copilot Chat

1. **Open Copilot Chat**: `Cmd/Ctrl + I`

1. **Ask a question**:

   ```
   What custom instructions apply to this project?
   ```

1. **Verify**: Should list relevant instructions

### Test MCP Integration (Optional)

1. **Check if MCP servers are configured**:
   - Open VS Code Settings
   - Search for "copilot mcp"
   - Verify servers are listed

1. **Test with chat**:

   ```
   @workspace What MCP servers are available?
   ```

---

## 📚 Language-Specific Setup

### Python 🐍

**Quick install**:

```bash
pip install black flake8 pytest mypy
```

**Custom instructions**: Automatically applied to `**.py` files

**Collections to install**:

- [Python MCP Development](../ai_framework/collections/python-mcp-development.md)

**Test it**:

```python
# Ask Copilot to generate a typed function
# Should include type hints, docstrings, error handling
```

### TypeScript/JavaScript 📦

**Quick install**:

```bash
npm install -g typescript prettier eslint
```

**Custom instructions**: Automatically applied to `**.ts`, `**.tsx`, `**.js`
files

**Collections to install**:

- [TypeScript MCP Development](../ai_framework/collections/typescript-mcp-development.md)
- [Frontend Web Dev](../ai_framework/collections/frontend-web-dev.md)

**Test it**:

```typescript
// Ask Copilot to generate an async function
// Should include proper types, error handling, JSDoc
```

### Java ☕

**Quick install**:

```bash
# Via SDKMAN
sdk install java 17-tem
sdk install maven
```

**Custom instructions**: Automatically applied to `**.java` files

**Collections to install**:

- [Java MCP Development](../ai_framework/collections/java-mcp-development.md)
- [Java Development](../ai_framework/collections/java-development.md)

### C# / .NET 🔷

**Quick install**:

```bash
# Install .NET SDK
wget https://dot.net/v1/dotnet-install.sh
bash dotnet-install.sh --version latest
```

**Custom instructions**: Automatically applied to `**.cs` files

**Collections to install**:

- [C# MCP Development](../ai_framework/collections/csharp-mcp-development.md)
- [C#/.NET Development](../ai_framework/collections/csharp-dotnet-development.md)

### More Languages

**Available for**: Go, Rust, Ruby, PHP, Swift, Kotlin, and more

**See**:
[Language-specific documentation](DEVELOPMENT_ENVIRONMENT_SETUP.md#language-specific-setup)

---

## 🤖 Using Custom Agents

### What Are Custom Agents?

Specialized AI assistants that extend Copilot for specific domains:

- **CSharpExpert**: .NET and C# development
- **Terraform**: Infrastructure as code
- **Security Audit**: Security scanning and fixes
- **ADR Generator**: Architectural Decision Records
- **Data Forensics**: Data investigation and analysis

### How to Use Agents

**Method 1: Via Chat**

```
@agent-name Your request here
```

**Method 2: Via Inline Comments**

```typescript
// @terraform: create an S3 bucket with encryption
```

**Method 3: Via Workspace Commands**

```
/agent terraform Create infrastructure for a web app
```

### Available Agents

Browse all 26+ agents: [Agent Registry](AGENT_REGISTRY.md)

**Popular agents**:

- [`CSharpExpert`](../ai_framework/agents/CSharpExpert.agent.md) - C# and .NET
- [`terraform`](../ai_framework/agents/terraform.agent.md) - Infrastructure
- [`security-audit`](../ai_framework/agents/security-audit.agent.md) - Security
- [`adr-generator`](../ai_framework/agents/adr-generator.agent.md) - Documentation
- [`workflow-optimizer`](../ai_framework/agents/workflow-optimizer.agent.md) - CI/CD

---

## 🎨 Using Chat Modes

### What Are Chat Modes?

Specialized AI personas for different roles and contexts:

- **Python MCP Expert**: MCP server development in Python
- **TypeScript MCP Expert**: MCP server development in TypeScript
- **Database Architect**: Database design and optimization
- **Security Expert**: Security best practices

### How to Activate

```
@chat-mode Your question here
```

**Example**:

```
@python-mcp-expert How do I implement a tool with structured output?
```

### Available Chat Modes

Browse: [`chatmodes/`](../ai_framework/chatmodes/) directory

**Popular modes**:

- Language-specific MCP experts (Python, TypeScript, C#, Java, etc.)
- Role-specific modes (Architect, DBA, DevOps, Security)

---

## 📦 Using Collections

### What Are Collections?

Curated bundles of instructions, prompts, and chat modes organized by theme:

- **Python MCP Development**: Everything for building Python MCP servers
- **Azure Cloud Development**: Azure-specific tools and patterns
- **Frontend Web Dev**: React, Angular, Vue, and more
- **DevOps OnCall**: Tools for incident response

### How to Install

1. **Browse collections**: [`collections/`](../ai_framework/collections/) directory
1. **Open a collection file**: e.g., `python-mcp-development.md`
1. **Click install badges**: Each component has an "Install in VS Code" badge
1. **Or install manually**: Copy files to your project

### Available Collections

**Development**:

- Python MCP, TypeScript MCP, Java MCP, C# MCP, Go MCP, etc.
- Frontend Web Dev, Backend APIs, Full-stack

**Cloud & Infrastructure**:

- Azure Cloud Development
- DevOps OnCall
- Database Management

**Specialized**:

- Edge AI Tasks
- Clojure Interactive Programming
- Power Platform Development

---

## 🔧 Advanced Configuration

### MCP Server Setup

For advanced users who want to build or configure MCP servers:

**See**: [MCP Server Setup Guide](MCP_SERVER_SETUP.md)

**Quick start**:

1. Choose your language
1. Use the generator prompt: `/python-mcp-server-generator`
1. Implement your tools
1. Configure in VS Code settings

### Custom Instructions

To create organization-specific instructions:

**See**: [Custom Instructions Setup Guide](CUSTOM_INSTRUCTIONS_SETUP.md)

**Quick start**:

1. Create `.instructions.md` file
1. Add YAML frontmatter with `description` and `applyTo`
1. Write your conventions
1. Save to `.github/copilot-instructions/`

### Development Environment

For full environment customization:

**See**: [Development Environment Setup Guide](DEVELOPMENT_ENVIRONMENT_SETUP.md)

**Covers**:

- DevContainer customization
- VS Code configuration
- Language-specific tools
- Git and shell setup

---

## 📖 Learn More

### Core Documentation

| Guide                                                             | Purpose                                  | Time   |
| ----------------------------------------------------------------- | ---------------------------------------- | ------ |
| [MCP Server Setup](MCP_SERVER_SETUP.md)                           | Configure Model Context Protocol servers | 20 min |
| [Custom Instructions Setup](CUSTOM_INSTRUCTIONS_SETUP.md)         | Set up coding standards                  | 15 min |
| [Development Environment Setup](DEVELOPMENT_ENVIRONMENT_SETUP.md) | Optimize your dev environment            | 25 min |
| [Agent Architecture Guide](AGENT_ARCHITECTURE_GUIDE.md)           | Build custom agents                      | 30 min |

### Resource Directories

| Directory                           | Contents                                              |
| ----------------------------------- | ----------------------------------------------------- |
| [`agents/`](../ai_framework/agents/)             | 26+ custom agents for specialized tasks               |
| [`instructions/`](https://github.com/github/awesome-copilot/tree/main/instructions/) | 100+ custom instructions for languages and frameworks |
| [`prompts/`](https://github.com/github/awesome-copilot/tree/main/prompts/)           | Reusable prompts for common tasks                     |
| [`chatmodes/`](../ai_framework/chatmodes/)       | Specialized AI personas                               |
| [`collections/`](../ai_framework/collections/)   | Curated bundles by theme                              |

### Quick References

- [Agent Registry](AGENT_REGISTRY.md) - Complete catalog of agents
- [README.agents.md](README.agents.md) - Agent documentation
- [README.instructions.md](README.instructions.md) - Instructions documentation
- [README.prompts.md](README.prompts.md) - Prompts documentation
- [README.chatmodes.md](README.chatmodes.md) - Chat modes documentation

---

## 🆘 Troubleshooting

### Copilot Not Working

1. **Verify installation**: Check Extensions panel for GitHub Copilot
1. **Check license**: Ensure your Copilot subscription is active
1. **Restart VS Code**: Sometimes needed after configuration changes
1. **Check logs**: View > Output > GitHub Copilot

### Instructions Not Applying

1. **Check file patterns**: Ensure `applyTo` glob matches your files
1. **Verify location**: Instructions should be in
   `.github/copilot-instructions/`
1. **Check YAML frontmatter**: Must be valid YAML with `description` and
   `applyTo`
1. **Restart VS Code**: Reload window after adding instructions

### DevContainer Issues

1. **Docker running**: Verify with `docker ps`
1. **Clear cache**: `docker system prune -a`
1. **Rebuild container**: Cmd/Ctrl + Shift + P > "Rebuild Container"
1. **Check logs**: View > Output > Dev Containers

### MCP Server Not Connecting

1. **Check configuration**: VS Code Settings > search "copilot mcp"
1. **Verify server starts**: Test command manually in terminal
1. **Check logs**: Output panel for MCP-related errors
1. **Restart VS Code**: Reload window after configuration changes

**Still having issues?**

- Check detailed troubleshooting:
  [MCP Setup](MCP_SERVER_SETUP.md#troubleshooting) |
  [Custom Instructions](CUSTOM_INSTRUCTIONS_SETUP.md#troubleshooting) |
  [Dev Environment](DEVELOPMENT_ENVIRONMENT_SETUP.md#troubleshooting)
- Open an issue: [GitHub Issues](https://github.com/ivviiviivvi/.github/issues)
- Ask in discussions:
  [GitHub Discussions](https://github.com/orgs/ivviiviivvi/discussions)

---

## 🎓 Best Practices

### Getting the Most from Copilot

1. **Write clear comments**: Better context = better suggestions
1. **Use descriptive names**: Help Copilot understand intent
1. **Leverage chat**: Ask questions for complex problems
1. **Review suggestions**: Always verify generated code
1. **Provide examples**: Show patterns you want to follow

### Using Custom Instructions

1. **Start with essentials**: Don't over-constrain initially
1. **Iterate based on feedback**: Refine as you learn what works
1. **Be specific**: Clear rules are easier for Copilot to follow
1. **Include examples**: Show good and bad patterns
1. **Update regularly**: Keep instructions current

### Working with Agents

1. **Use the right agent**: Choose based on task domain
1. **Provide context**: Reference relevant files and goals
1. **Be specific**: Clear requests get better results
1. **Iterate**: Refine based on agent output
1. **Combine with chat**: Use both for complex tasks

---

## 🚀 Next Steps

### Immediate Actions

1. ✅ **Complete setup** using your chosen path above
1. ✅ **Verify everything works** with test examples
1. ✅ **Try an agent** for a real task
1. ✅ **Install collections** for your primary languages

### This Week

1. **Explore documentation** linked above
1. **Customize instructions** for your team's needs
1. **Build an MCP server** for a common task
1. **Share with team** and gather feedback

### This Month

1. **Create custom agents** for specialized domains
1. **Measure impact**: Track time saved and code quality
1. **Expand coverage**: Add more instructions and agents
1. **Contribute back**: Share improvements with the organization

---

## 🤝 Get Help

### Resources

- **Documentation**: [README.md](../README.md) - Complete repository overview
- **Agent Registry**: [AGENT_REGISTRY.md](AGENT_REGISTRY.md) - Catalog of all
  agents
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

### Community

- **Questions**:
  [GitHub Discussions](https://github.com/orgs/ivviiviivvi/discussions)
- **Issues**: [Issue Tracker](https://github.com/ivviiviivvi/.github/issues)
- **Feedback**: Open a discussion or issue

### Organization

- **Internal Wiki**: Check your organization's wiki for team-specific guides
- **Slack/Teams**: Join your organization's Copilot channel
- **Office Hours**: Attend Copilot Q&A sessions (if available)

---

**🎉 You're Ready to Go!**

Start coding with enhanced Copilot capabilities. Remember to:

- Review suggestions carefully
- Provide feedback when something doesn't work
- Share successes with your team
- Contribute improvements back

---

_Last Updated: 2025-12-31_
