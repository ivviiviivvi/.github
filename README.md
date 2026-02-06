# ivviiviivvi Organization Hub

<!-- BADGES:START -->
[![CI](https://img.shields.io/github/actions/workflow/status/ivviiviivvi/.github/ci.yml?style=flat-square&label=CI)](https://github.com/ivviiviivvi/.github/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/ivviiviivvi/.github?style=flat-square)](LICENSE) [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](#) [![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](#) [![Stars](https://img.shields.io/github/stars/ivviiviivvi/.github?style=flat-square)](https://github.com/ivviiviivvi/.github/stargazers) [![Issues](https://img.shields.io/github/issues/ivviiviivvi/.github?style=flat-square)](https://github.com/ivviiviivvi/.github/issues) [![Pull Requests](https://img.shields.io/github/issues-pr/ivviiviivvi/.github?style=flat-square)](https://github.com/ivviiviivvi/.github/pulls) [![Last Commit](https://img.shields.io/github/last-commit/ivviiviivvi/.github?style=flat-square)](https://github.com/ivviiviivvi/.github/commits) [![Contributors](https://img.shields.io/github/contributors/ivviiviivvi/.github?style=flat-square)](https://github.com/ivviiviivvi/.github/graphs/contributors) 
<!-- BADGES:END -->

[![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)](VERSION)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-129%20workflows-blue?logo=github-actions)](https://github.com/ivviiviivvi/.github/actions)
[![Security Scanning](https://img.shields.io/badge/security-bandit%20%7C%20gitleaks-green?logo=security)](https://github.com/ivviiviivvi/.github)
[![Documentation](https://img.shields.io/badge/docs-comprehensive-blue?logo=markdown)](docs/INDEX.md)

> **AI-Driven Development Infrastructure for the Modern Organization**

______________________________________________________________________

## The Problem

Scaling AI-assisted development across multiple repositories creates fragmented
tooling, inconsistent policies, and duplicated effort that grows exponentially
with team size.

## Our Approach

A centralized `.github` repository providing organization-wide defaults:

- Standardized governance that inherits automatically
- Production-ready AI agents for common development tasks
- Comprehensive workflow automation

## The Outcome

- **Zero-config inheritance** for new repositories
- **129 workflows** handling CI/CD, security, and maintenance
- **32 AI agents** ready for deployment
- **Clean state**: 0 open issues, 0 open PRs

______________________________________________________________________

## Overview

A centralized `.github` repository providing organization-wide infrastructure:

- **32 Production AI Agents** - Ready-to-deploy development assistants
- **129 GitHub Actions Workflows** - Comprehensive automation coverage
- **MCP Server Framework** - Extended AI capabilities across 11 languages
- **Comprehensive Documentation** - Guides and references

______________________________________________________________________

## Quick Start

**Get started in 5 minutes:**

1. **Read the basics:** [CONTRIBUTING.md](CONTRIBUTING.md) +
   [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
1. **Browse documentation:** [Documentation Index](docs/INDEX.md)
1. **Set up environment:**
   [Development Environment Setup](docs/DEVELOPMENT_ENVIRONMENT_SETUP.md)
1. **Clone and explore:**
   ```bash
   git clone https://github.com/ivviiviivvi/.github.git
   cd .github
   pip install -e ".[dev]"
   pre-commit install
   ```
1. **Find issues:**
   [Good first issues](https://github.com/ivviiviivvi/.github/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

**Need help?** Check [SUPPORT.md](SUPPORT.md) or
[start a discussion](https://github.com/orgs/ivviiviivvi/discussions).

______________________________________________________________________

## Repository Structure

```
.github/
├── .config/               # Configuration files (devcontainer, vscode, pre-commit)
├── .github/workflows/     # GitHub Actions workflows
│   └── reusable/          # Reusable workflow templates
├── docs/                  # Documentation files
│   ├── archive/           # Historical reports
│   ├── guides/            # How-to guides
│   ├── reference/         # Reference documentation
│   └── reports/           # Health reports & roadmaps
├── src/
│   ├── ai_framework/      # AI infrastructure
│   │   ├── agents/        # Production AI agents
│   │   ├── chatmodes/     # Copilot chat modes
│   │   ├── instructions/  # Coding instructions
│   │   └── prompts/       # Task-specific prompts
│   └── automation/        # Python automation scripts
│       ├── scripts/       # Python scripts
│       └── project_meta/  # Project metadata
├── tests/                 # Test suites
├── .github/workflow-templates/  # Starter workflow templates for org repos
├── pyproject.toml         # Python config
└── package.json           # npm config (version scripts)
```

______________________________________________________________________

## Key Features

### AI Framework

**Production Agents** across 5 categories:

- Security, Infrastructure, Development, Languages, Documentation
- See [Agent Registry](docs/AGENT_REGISTRY.md) for complete catalog

**GitHub Copilot Customizations:**

- [Quick Start Guide](docs/COPILOT_QUICK_START.md) - Setup guide
- [Custom Instructions](docs/CUSTOM_INSTRUCTIONS_SETUP.md) - Coding standards
- [MCP Server Setup](docs/MCP_SERVER_SETUP.md) - Language support

### Workflow Automation

**Workflows** covering:

- CI/CD pipelines
- Security scanning (CodeQL, Gitleaks, TruffleHog)
- Stale issue management
- PR automation and batch operations
- Health monitoring

**Key Workflows:**

- `health-check.yml` - Repository health monitoring
- `auto-merge.yml` - Automated PR merging
- `batch-onboarding.yml` - Multi-repo onboarding
- `org-wide-workflow-dispatch.yml` - Org-wide workflow triggers

### Security

- **SHA-Pinned Actions** - All actions pinned to specific commits
- **Secret Scanning** - Multi-tool detection (TruffleHog, Gitleaks,
  detect-secrets)
- **CodeQL Analysis** - Continuous vulnerability scanning
- **Branch Protection** - Enforced rules on production branches

### Version Management

```bash
# Check version
grep "^version" pyproject.toml  # 1.0.0

# Bump and sync versions
npm run version:bump:minor
npm run version:sync
```

______________________________________________________________________

## Documentation

**[Complete Documentation Index](docs/INDEX.md)** - Browse all docs

### Core Documentation

| Document                                 | Purpose                 |
| ---------------------------------------- | ----------------------- |
| [CONTRIBUTING.md](CONTRIBUTING.md)       | Contribution guidelines |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards     |
| [SECURITY.md](SECURITY.md)               | Security policy         |
| [SUPPORT.md](SUPPORT.md)                 | Getting help            |

### Guides

| Guide                                                       | Description              |
| ----------------------------------------------------------- | ------------------------ |
| [COPILOT_QUICK_START.md](docs/COPILOT_QUICK_START.md)       | GitHub Copilot setup     |
| [BATCH_ONBOARDING_GUIDE.md](docs/BATCH_ONBOARDING_GUIDE.md) | Multi-repo onboarding    |
| [WORKFLOW_DESIGN.md](docs/WORKFLOW_DESIGN.md)               | Workflow architecture    |
| [docs/guides/CLAUDE.md](docs/guides/CLAUDE.md)              | Working with Claude Code |

______________________________________________________________________

## Templates

### Issue Templates

- Bug Reports (form-based)
- Feature Requests
- Documentation improvements
- Security vulnerabilities
- Tasks

### Pull Request Templates

- Default template
- Bug fix, Feature, Documentation, Refactoring, Performance variants

### Workflow Templates

Located in `workflow-templates/`:

- `ci.yml` - Basic CI pipeline
- `security-scan.yml` - CodeQL analysis
- `stale-management.yml` - Stale issue management
- `deployment.yml` - Deployment pipeline
- `repository-bootstrap.yml` - Repository setup automation

______________________________________________________________________

## GitHub Projects

**Organization Projects** at
[github.com/orgs/ivviiviivvi/projects](https://github.com/orgs/ivviiviivvi/projects):

- AI Framework Development
- Documentation & Knowledge
- Workflow & Automation
- Security & Compliance
- Infrastructure & DevOps
- Community & Engagement
- Product Roadmap

______________________________________________________________________

## Development

### Prerequisites

- Python >= 3.9 (prefer 3.12)
- Node.js >= 20.0.0
- Pre-commit hooks enabled

### Setup

```bash
# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
python -m pytest --cov=src/automation

# Run linting
ruff check . && ruff format .
```

### Commit Convention

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
```

______________________________________________________________________

## Security

**Found a security vulnerability?**

**DO NOT create a public issue.** Follow our [Security Policy](SECURITY.md):

- Email: security@ivviiviivvi.com
- [GitHub Security Advisory](https://github.com/ivviiviivvi/.github/security/advisories/new)

**Response Timeline:**

- 24 hours: Acknowledgment
- 72 hours: Initial assessment
- 7 days: Detailed response

______________________________________________________________________

## Automation

### Dependabot

Configured for: GitHub Actions, pip, npm, Docker, Go modules, Terraform

### Stale Management

- Issues/PRs marked stale after 60 days
- Closed 14 days after stale marking
- Exemptions: security, critical priority, pinned

______________________________________________________________________

## Community

- **Questions:**
  [GitHub Discussions](https://github.com/ivviiviivvi/.github/discussions)
- **Issues:** [Issue Tracker](https://github.com/ivviiviivvi/.github/issues)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

______________________________________________________________________

## License

[MIT License](LICENSE)

______________________________________________________________________

## Contact

- **General:** info@ivviiviivvi.com
- **Security:** security@ivviiviivvi.com
- **Support:** support@ivviiviivvi.com

______________________________________________________________________

**Maintained by:** @ivviiviivvi/leadership
