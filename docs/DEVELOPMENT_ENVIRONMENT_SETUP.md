# Development Environment Setup Guide

> **Complete guide to configuring your development environment for optimal GitHub Copilot integration**

## Table of Contents

- [Overview](#overview)
- [Benefits of a Standardized Environment](#benefits-of-a-standardized-environment)
- [Quick Start](#quick-start)
- [Development Container (DevContainer)](#development-container-devcontainer)
  - [What is a DevContainer?](#what-is-a-devcontainer)
  - [Features Included](#features-included)
  - [Getting Started with DevContainers](#getting-started-with-devcontainers)
  - [Customizing Your DevContainer](#customizing-your-devcontainer)
- [VS Code Configuration](#vs-code-configuration)
  - [Extensions](#extensions)
  - [Settings](#settings)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
- [GitHub Copilot Configuration](#github-copilot-configuration)
  - [Basic Setup](#basic-setup)
  - [Advanced Settings](#advanced-settings)
  - [Chat Configuration](#chat-configuration)
- [Language-Specific Setup](#language-specific-setup)
  - [Python](#python)
  - [TypeScript/JavaScript](#typescriptjavascript)
  - [Java](#java)
  - [C#/.NET](#cnet)
  - [Go](#go)
  - [Rust](#rust)
- [Git Configuration](#git-configuration)
- [Shell Configuration](#shell-configuration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

---

## Overview

This guide helps you set up a consistent, optimized development environment that maximizes GitHub Copilot's effectiveness. Whether you're using DevContainers, local development, or a hybrid approach, you'll find comprehensive instructions for creating an environment that:

- **Enhances Copilot suggestions** through proper tooling and configuration
- **Standardizes team setups** for consistency across projects
- **Automates environment creation** with infrastructure-as-code
- **Supports multiple languages** in a single environment
- **Integrates seamlessly** with GitHub workflows

---

## Benefits of a Standardized Environment

### For Developers

- **Instant setup**: Get productive immediately without configuration headaches
- **Consistency**: Same environment across local, container, and CI/CD
- **Better Copilot**: Properly configured tools improve AI suggestions
- **Fewer errors**: Pre-configured linting, formatting, and testing
- **Easy switching**: Move between projects without reconfiguration

### For Teams

- **Reduced onboarding time**: New developers productive in minutes
- **Eliminate "works on my machine"**: Identical environments for all
- **Shared tooling**: Everyone uses the same versions and configurations
- **Better collaboration**: Consistent code style and quality
- **Documented standards**: Configuration as documentation

### For Organizations

- **Compliance**: Enforce security and quality standards
- **Cost reduction**: Less time on environment issues
- **Scalability**: Easy to add new projects and teams
- **Knowledge preservation**: Infrastructure-as-code captures decisions
- **Integration**: Seamless CI/CD pipeline alignment

---

## Quick Start

### Option 1: Use the DevContainer (Recommended)

For the fastest, most consistent setup:

1. **Install prerequisites**:
   - [VS Code](https://code.visualstudio.com/) or [VS Code Insiders](https://code.visualstudio.com/insiders/)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in container**:
   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   cd .github
   code .
   ```

3. **Reopen in container**:
   - Press `Cmd/Ctrl + Shift + P`
   - Select "Dev Containers: Reopen in Container"
   - Wait for container to build (first time only)

4. **Start coding**: Everything is pre-configured and ready!

### Option 2: Local Setup

For developers who prefer local development:

1. **Clone and copy configurations**:
   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   
   # Copy VS Code settings
   cp .github/.vscode/settings.json ~/.vscode/settings.json
   
   # Copy Git configuration (review before using)
   # cat .github/.gitconfig >> ~/.gitconfig
   ```

2. **Install extensions** (see [VS Code Configuration](#vs-code-configuration))

3. **Configure languages** (see [Language-Specific Setup](#language-specific-setup))

---

## Development Container (DevContainer)

### What is a DevContainer?

A **Development Container** (DevContainer) is a fully configured development environment running in a Docker container. It provides:

- **Consistent environment**: Same tools, versions, and settings for everyone
- **Isolated workspace**: No conflicts with other projects or system tools
- **Reproducible**: Defined in code, version controlled
- **Pre-configured**: Extensions, settings, and tools ready to use
- **Portable**: Works on any machine with Docker

### Features Included

Our DevContainer (`.devcontainer/devcontainer.json`) includes:

#### Language Runtimes

- **Node.js 20**: JavaScript/TypeScript development
- **Python 3.11**: With pip, setuptools, and build tools
- **Go 1.21**: Go development and tools
- **Rust**: Latest stable Rust toolchain
- **Git**: Latest version for source control
- **GitHub CLI**: `gh` command-line tool

#### VS Code Extensions

##### Core Development
- **GitHub Copilot**: AI-powered code completion
- **GitHub Copilot Chat**: Conversational AI assistance
- **GitLens**: Enhanced Git integration
- **GitHub Pull Requests**: PR management in VS Code

##### Language Support
- **Python** (Pylance, Black formatter, Flake8)
- **ESLint** (JavaScript/TypeScript linting)
- **Prettier** (Code formatting)
- **Go** (Official Go extension)
- **Rust Analyzer** (Rust language support)

##### Infrastructure & DevOps
- **Docker**: Container management
- **Terraform**: Infrastructure as code
- **YAML**: YAML language support
- **Makefile Tools**: Makefile support

##### Additional AI Tools
- **Sourcegraph Cody**: Alternative AI assistant
- **TabNine**: AI code completion

#### Pre-configured Settings

- **Format on save**: Automatic code formatting
- **ESLint auto-fix**: Fix issues on save
- **Organize imports**: Automatic import sorting
- **Python linting**: Flake8 with sensible defaults
- **Git auto-fetch**: Stay synchronized with remotes
- **Smart commit**: Convenient Git workflows

#### Ports Configured

- **3000**: Application (auto-notify on forward)
- **5000**: API backend
- **8000**: Alternative app port
- **8080**: Alt HTTP server
- **9090**: Prometheus (silent forwarding)
- **3001**: Additional app port

### Getting Started with DevContainers

#### Prerequisites

1. **Docker Desktop** (or compatible container runtime)
   ```bash
   # Verify Docker is running
   docker --version
   docker ps
   ```

2. **VS Code** with **Dev Containers** extension
   ```bash
   # Install extension (or use VS Code marketplace)
   code --install-extension ms-vscode-remote.remote-containers
   ```

#### Opening a Project in a Container

**Method 1: From VS Code**
1. Open the project folder in VS Code
2. Press `Cmd/Ctrl + Shift + P`
3. Select "Dev Containers: Reopen in Container"
4. Wait for build to complete

**Method 2: From Command Line**
```bash
# Open project in container directly
code --folder-uri vscode-remote://dev-container+$(pwd | sed 's/\//%2F/g')/workspace
```

**Method 3: Using GitHub Codespaces**
```bash
# Create a codespace (uses the same devcontainer.json)
gh codespace create --repo ivviiviivvi/.github
```

#### First-Time Setup

On first run, the container will:

1. **Pull base images** (Ubuntu with VS Code Server)
2. **Install features** (Node, Python, Go, Rust, etc.)
3. **Install extensions** (Copilot, language support, tools)
4. **Run post-create script** (`.devcontainer/post-create.sh`):
   - Install additional dependencies
   - Configure Git settings
   - Set up pre-commit hooks
   - Initialize language-specific tools

**Post-create script includes:**
```bash
#!/bin/bash
# Install global npm packages
npm install -g typescript ts-node @types/node

# Install Python packages
pip install --user black flake8 pytest

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Configure Git
git config --global --add safe.directory /workspace
```

### Customizing Your DevContainer

#### Adding Language Features

Edit `.devcontainer/devcontainer.json`:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/java:1": {
      "version": "17"
    },
    "ghcr.io/devcontainers/features/php:1": {
      "version": "8.2"
    }
  }
}
```

#### Adding VS Code Extensions

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "svelte.svelte-vscode",
        "prisma.prisma"
      ]
    }
  }
}
```

#### Mounting Local Files

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.aws,target=/home/vscode/.aws,type=bind,consistency=cached"
  ]
}
```

#### Adding Environment Variables

```json
{
  "containerEnv": {
    "API_KEY": "${localEnv:API_KEY}",
    "NODE_ENV": "development"
  }
}
```

#### Customizing Post-Create Commands

Edit `.devcontainer/post-create.sh`:

```bash
#!/bin/bash
set -e

echo "Installing project dependencies..."
npm install

echo "Setting up database..."
docker-compose up -d db
npm run db:migrate

echo "Environment ready!"
```

---

## VS Code Configuration

### Extensions

Our recommended extensions (automatically installed in DevContainer):

#### Essential

| Extension | Purpose |
|-----------|---------|
| **GitHub Copilot** | AI code completion |
| **GitHub Copilot Chat** | Conversational AI assistant |
| **GitLens** | Enhanced Git capabilities |
| **Prettier** | Code formatting |
| **ESLint** | JavaScript/TypeScript linting |

#### Language-Specific

| Extension | Language |
|-----------|----------|
| **Python** | Python development |
| **Pylance** | Python language server |
| **Black Formatter** | Python formatting |
| **Rust Analyzer** | Rust development |
| **Go** | Go development |

#### Infrastructure

| Extension | Purpose |
|-----------|---------|
| **Docker** | Container management |
| **Terraform** | Infrastructure as code |
| **YAML** | YAML editing |
| **Remote Containers** | DevContainer support |

### Settings

Key VS Code settings (`.vscode/settings.json`):

```json
{
  // Editor
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "editor.rulers": [80, 120],
  "editor.bracketPairColorization.enabled": true,

  // Python
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": ["--max-line-length=88"],

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,

  // GitHub Copilot
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "markdown": true
  }
}
```

### Keyboard Shortcuts

Recommended shortcuts for GitHub Copilot:

| Action | Shortcut (Mac) | Shortcut (Windows/Linux) |
|--------|----------------|--------------------------|
| Accept suggestion | `Tab` | `Tab` |
| Reject suggestion | `Esc` | `Esc` |
| Next suggestion | `Option + ]` | `Alt + ]` |
| Previous suggestion | `Option + [` | `Alt + [` |
| Open Copilot Chat | `Cmd + I` | `Ctrl + I` |
| Trigger inline suggestions | `Option + \` | `Alt + \` |

---

## GitHub Copilot Configuration

### Basic Setup

1. **Install GitHub Copilot**:
   - Open VS Code
   - Go to Extensions (`Cmd/Ctrl + Shift + X`)
   - Search "GitHub Copilot"
   - Install both "GitHub Copilot" and "GitHub Copilot Chat"

2. **Sign in**:
   - Click "Sign in to GitHub" in the status bar
   - Authorize VS Code in your browser
   - Verify Copilot icon appears in status bar

3. **Verify installation**:
   - Open a code file
   - Start typing - you should see suggestions
   - Press `Cmd/Ctrl + I` to open Copilot Chat

### Advanced Settings

Configure Copilot behavior in `settings.json`:

```json
{
  // Enable/disable by language
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "markdown": true,
    "plaintext": false
  },

  // Advanced features
  "github.copilot.advanced": {
    "debug.overrideEngine": "gpt-4",
    "debug.testOverrideProxyUrl": "",
    "authProvider": "github"
  }
}
```

### Chat Configuration

Optimize Copilot Chat:

```json
{
  // Chat behavior
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": ".github/copilot-instructions.md"
    }
  ],
  "github.copilot.chat.followUps": "always",
  "github.copilot.chat.localeOverride": "en"
}
```

---

## Language-Specific Setup

### Python

**Tools to install:**
```bash
# Core tools
pip install black flake8 pytest mypy

# Type stubs
pip install types-requests types-PyYAML

# Development tools
pip install ipython jupyter pre-commit
```

**VS Code settings:**
```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.testing.pytestEnabled": true
}
```

### TypeScript/JavaScript

**Tools to install:**
```bash
# Core tools
npm install -g typescript ts-node
npm install -g eslint prettier

# Type definitions
npm install -D @types/node @types/jest

# Development tools
npm install -D jest ts-jest @types/jest
```

**VS Code settings:**
```json
{
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "typescript.updateImportsOnFileMove.enabled": "always",
  "javascript.updateImportsOnFileMove.enabled": "always"
}
```

### Java

**Tools to install:**
```bash
# Via SDKMAN (recommended)
curl -s "https://get.sdkman.io" | bash
sdk install java 17.0.2-tem
sdk install maven
sdk install gradle
```

**VS Code extensions:**
- Extension Pack for Java
- Spring Boot Extension Pack
- Lombok

### C#/.NET

**Tools to install:**
```bash
# .NET SDK
wget https://dot.net/v1/dotnet-install.sh
bash dotnet-install.sh --version latest

# Global tools
dotnet tool install -g dotnet-format
dotnet tool install -g dotnet-ef
```

**VS Code extensions:**
- C# (Official)
- C# Dev Kit
- .NET Core Test Explorer

### Go

**Tools to install:**
```bash
# Via Go install
go install golang.org/x/tools/gopls@latest
go install github.com/go-delve/delve/cmd/dlv@latest
go install honnef.co/go/tools/cmd/staticcheck@latest
```

**VS Code settings:**
```json
{
  "[go]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "go.formatTool": "goimports",
  "go.lintTool": "staticcheck"
}
```

### Rust

**Tools to install:**
```bash
# Via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Components
rustup component add rust-analyzer
rustup component add rustfmt
rustup component add clippy
```

**VS Code extensions:**
- rust-analyzer (Official)

---

## Git Configuration

### Basic Configuration

```bash
# Identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Editor
git config --global core.editor "code --wait"

# Default branch
git config --global init.defaultBranch main

# Pull strategy
git config --global pull.rebase false
```

### Aliases

```bash
# Shortcuts
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

# Advanced
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
```

### GitHub CLI Configuration

```bash
# Install gh (if not already installed)
# macOS: brew install gh
# Linux: See https://github.com/cli/cli#installation

# Authenticate
gh auth login

# Set default editor
gh config set editor "code --wait"

# Enable Copilot in CLI
gh extension install github/gh-copilot
```

---

## Shell Configuration

### Bash Configuration

Add to `~/.bashrc` or `~/.bash_profile`:

```bash
# GitHub CLI completion
eval "$(gh completion -s bash)"

# Node version manager
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Python virtual environments
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

# Go workspace
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Rust
source $HOME/.cargo/env

# Aliases
alias g="git"
alias dc="docker-compose"
alias k="kubectl"
```

### Zsh Configuration

Add to `~/.zshrc`:

```zsh
# Oh My Zsh plugins
plugins=(git docker docker-compose kubectl python npm)

# GitHub CLI completion
eval "$(gh completion -s zsh)"

# Starship prompt (optional)
eval "$(starship init zsh)"
```

---

## Troubleshooting

### DevContainer Issues

**Problem**: Container fails to build

**Solutions**:
1. Check Docker is running: `docker ps`
2. Clear Docker cache: `docker system prune -a`
3. Rebuild without cache: `Cmd/Ctrl + Shift + P` > "Dev Containers: Rebuild Container"
4. Check logs: View > Output > Dev Containers

**Problem**: Extensions not installing

**Solutions**:
1. Verify internet connection
2. Check VS Code extension marketplace status
3. Install extensions manually in container
4. Check `devcontainer.json` for syntax errors

### GitHub Copilot Issues

**Problem**: Copilot not providing suggestions

**Solutions**:
1. Verify Copilot is enabled (check status bar icon)
2. Check file type is supported
3. Ensure GitHub Copilot license is active
4. Restart VS Code
5. Check output logs: View > Output > GitHub Copilot

**Problem**: Poor suggestion quality

**Solutions**:
1. Install custom instructions for your language
2. Provide more context in comments
3. Use Copilot Chat for complex tasks
4. Check language server is working

---

## Best Practices

### Environment

- **Use DevContainers** for complex projects with multiple dependencies
- **Keep DevContainer lightweight**: Only install what you need
- **Version lock dependencies**: Pin versions for reproducibility
- **Document customizations**: Comment non-obvious configurations
- **Regular updates**: Keep base images and tools up to date

### VS Code

- **Install recommended extensions**: Use workspace recommendations
- **Configure formatters**: Ensure consistent code style
- **Use workspace settings**: Project-specific settings in `.vscode/`
- **Leverage snippets**: Create custom snippets for common patterns
- **Keyboard shortcuts**: Learn and customize for efficiency

### GitHub Copilot

- **Write clear comments**: Better comments = better suggestions
- **Use descriptive names**: Help Copilot understand intent
- **Leverage chat**: Ask questions for complex problems
- **Review suggestions**: Always verify generated code
- **Provide context**: Reference related files and functions

---

## Additional Resources

### Documentation

- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [Docker Documentation](https://docs.docker.com/)

### Organization Resources

- [Custom Instructions Setup](CUSTOM_INSTRUCTIONS_SETUP.md) - Configure coding standards
- [MCP Server Setup](MCP_SERVER_SETUP.md) - Integrate MCP servers
- [Agent Architecture Guide](AGENT_ARCHITECTURE_GUIDE.md) - Build custom agents
- [Contributing Guide](CONTRIBUTING.md) - Contribute to this repository

### Templates

- [DevContainer Template](../.devcontainer/devcontainer.json) - Base configuration
- [VS Code Settings Template](../.vscode/settings.json) - Recommended settings
- [Git Configuration Template](../.gitconfig) - Git setup examples

---

## Next Steps

1. **Choose your setup method**: DevContainer or local installation
2. **Follow the Quick Start** for your chosen method
3. **Install GitHub Copilot** and verify it's working
4. **Add custom instructions** for your languages
5. **Configure MCP servers** if needed
6. **Customize to your needs** based on your workflow
7. **Share with your team** and iterate based on feedback

---

**Questions or Issues?**
- Check the [Troubleshooting](#troubleshooting) section
- Review related guides: [Custom Instructions](CUSTOM_INSTRUCTIONS_SETUP.md) | [MCP Servers](MCP_SERVER_SETUP.md)
- Open an issue in this repository
- Ask in GitHub Discussions

---

*Last Updated: 2025-12-31*
