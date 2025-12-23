# CLAUDE.md - AI Assistant Guide for .github Repository

> **Comprehensive guide for AI assistants working with the ivviiviivvi organization's .github repository**

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Development Workflows](#development-workflows)
4. [Commit Conventions](#commit-conventions)
5. [Pull Request Process](#pull-request-process)
6. [GitHub Copilot Customizations](#github-copilot-customizations)
7. [Automation & CI/CD](#automation--cicd)
8. [Security & Compliance](#security--compliance)
9. [Key Conventions](#key-conventions)
10. [AI Assistant Guidelines](#ai-assistant-guidelines)
11. [Common Tasks](#common-tasks)

---

## Repository Overview

### Purpose

This is the **organization-level .github repository** for ivviiviivvi. It serves as the central hub for:

- **Default community health files** that apply to all repositories in the organization
- **Standardized templates** for issues and pull requests
- **Reusable workflow templates** for CI/CD and automation
- **Organization-wide configuration** and documentation standards
- **GitHub Copilot customizations** (300+ agents, instructions, prompts, chatmodes, collections)
- **Living Document System** - AI-driven governance and management protocols

When a repository in the organization doesn't have its own community health file, GitHub automatically uses the defaults from this repository.

### Key Principles

- **Openness**: Transparent development and documentation
- **Automation-First**: 59 active workflows plus 14 reusable templates covering all aspects of development
- **Security-by-Default**: Multi-layered security scanning (CodeQL, Semgrep, dependency review)
- **AI-Driven**: Deep integration with AI tools (Claude, GitHub Copilot, OpenAI, Gemini, Grok)
- **Community-Focused**: Welcoming to contributors with clear guidelines and templates
- **Quality-Enforced**: Automated quality checks on all PRs

---

## Codebase Structure

### Directory Tree

```
/home/user/.github/
├── .github/                          # Organization's own automation
│   ├── workflows/                    # 59 active GitHub Actions workflows
│   │   ├── Security & Compliance
│   │   │   ├── codeql-analysis.yml
│   │   │   ├── semgrep.yml
│   │   │   ├── dependency-review.yml
│   │   │   └── sbom-generation.yml
│   │   ├── Quality & Automation
│   │   │   ├── auto-labeler.yml
│   │   │   ├── auto-assign.yml
│   │   │   ├── pr-quality-checks.yml
│   │   │   ├── link-checker.yml
│   │   │   └── community-health.yml
│   │   ├── AI & Code Intelligence
│   │   │   ├── claude-code-review.yml
│   │   │   ├── openai_workflow.yml
│   │   │   ├── gemini_workflow.yml
│   │   │   ├── grok_workflow.yml
│   │   │   └── perplexity_workflow.yml
│   │   ├── Metrics & Analytics
│   │   │   ├── commit-tracking.yml
│   │   │   ├── weekly-commit-report.yml
│   │   │   ├── repo-metrics.yml
│   │   │   └── accessibility-testing.yml
│   │   └── Release & Deployment
│   │       ├── release.yml
│   │       ├── version-bump.yml
│   │       └── semantic-release.yml
│   ├── copilot-instructions.md       # Code review checklist
│   ├── labeler.yml                   # Path-based auto-labeling config
│   ├── markdown-link-check-config.json
│   └── spellcheck-config.yml
│
├── GitHub Copilot Customizations/    # 300+ AI customizations
│   ├── agents/                       # 25 MCP-integrated specialized agents
│   │   ├── terraform.agent.md
│   │   ├── CSharpExpert.agent.md
│   │   ├── dynatrace-expert.agent.md
│   │   └── [21 more agents]
│   ├── instructions/                 # 110 file pattern-based coding standards
│   │   ├── angular.instructions.md
│   │   ├── bicep-code-best-practices.md
│   │   ├── terraform-azure.instructions.md
│   │   └── [106 more instructions]
│   ├── prompts/                      # 119 task-specific automation prompts
│   │   ├── conventional-commit.prompt.md
│   │   ├── architecture-blueprint.prompt.md
│   │   └── [116 more prompts]
│   ├── chatmodes/                    # 88 specialized AI personas
│   │   ├── azure-principal-architect.md
│   │   ├── Ultimate-Transparent-Thinking-Beast-Mode.md
│   │   └── [85 more modes]
│   └── collections/                  # 27 collections (55 files w/ .yml+.md)
│       ├── azure-cloud-development.yml
│       ├── typescript-mcp-development.yml
│       ├── python-mcp-development.yml
│       ├── clojure.collection.yml
│       ├── edge-ai-tasks.collection.yml
│       └── [22 more collections]
│
├── chaos-zone/                       # Temporary holding area for unorganized content
│   ├── README.md                     # Chaos zone documentation
│   ├── chats/                        # AI chat transcripts
│   ├── drafts/                       # Work-in-progress documents
│   ├── ideas/                        # Brainstorming notes
│   └── misc/                         # Miscellaneous files
│
├── ISSUE_TEMPLATE/                   # Issue templates
│   ├── config.yml
│   ├── bug_report.md
│   ├── bug_report_form.yml
│   ├── feature_request.md
│   ├── feature_request_form.yml
│   ├── documentation.md
│   └── question.md
│
├── PULL_REQUEST_TEMPLATE/            # PR templates
│   ├── bug_fix.md
│   ├── feature.md
│   ├── documentation.md
│   ├── refactoring.md
│   └── performance.md
│
├── workflow-templates/               # Reusable org-wide workflows
│   ├── ci.yml
│   ├── security-scan.yml
│   ├── deployment.yml
│   ├── stale-management.yml
│   ├── dependency-updates.yml
│   └── *.properties.json
│
├── docs/                             # Documentation & guides
│   ├── README.agents.md              # Agent documentation (23KB)
│   ├── README.instructions.md        # Instructions catalog (104KB)
│   ├── README.prompts.md             # Prompts catalog (110KB)
│   ├── README.chatmodes.md           # Chat modes catalog (81KB)
│   ├── README.collections.md         # Collections guide
│   ├── AI_IMPLEMENTATION_GUIDE.md
│   ├── BRANCH_PROTECTION.md
│   ├── REPOSITORY_SETUP_CHECKLIST.md
│   ├── LABELS.md
│   ├── TESTING.md
│   ├── GOVERNANCE.md
│   ├── MANIFESTO.md
│   ├── CODE_OF_CONDUCT.md            # Community code of conduct
│   ├── CONTRIBUTING.md               # Contribution guidelines
│   ├── SECURITY.md                   # Security policy
│   ├── SUPPORT.md                    # Support information
│   ├── PULL_REQUEST_TEMPLATE.md      # Default PR template
│   ├── LOGICAL_EXPANSIONS.md
│   ├── ORG_HEALTH_REPORT.md
│   ├── REPOSITORY_PURPOSE_ANALYSIS.md
│   ├── QUICK_START.md
│   ├── AI_CODE_INTELLIGENCE.md       # AI tools integration guide
│   ├── AUTOMATION_MASTER_GUIDE.md    # Automation documentation
│   ├── BEST_PRACTICES.md             # Comprehensive best practices
│   ├── DOCKER_BEST_PRACTICES.md
│   ├── GIT_WORKFLOW.md
│   ├── SEMANTIC_VERSIONING.md
│   ├── SECURITY_ADVANCED.md
│   └── CHANGELOG.md
│
├── Configuration/
│   ├── dependabot.yml                # 6 ecosystems (npm, pip, actions, etc.)
│   ├── renovate.json                 # Advanced dependency management
│   ├── .semgrep/rules.yml            # Custom security rules (1511 lines)
│   ├── .pre-commit-config.yaml
│   └── observability/prometheus-example.yml
│
├── Scripts/
│   ├── commit_changes.sh             # Automated commits
│   ├── manage_lock.sh                # Lock management
│   └── quota_manager.py              # API quota tracking
│
├── Infrastructure/
│   ├── .devcontainer/                # Development containers
│   │   ├── devcontainer.json
│   │   ├── docker-compose.yml
│   │   └── post-create.sh
│   └── profile/README.md             # Organization profile page
│
└── reports/                          # Auto-generated activity reports
    └── commit-report-*.md
```

### Key Files Reference

| File                          | Purpose                                | Location          |
| ----------------------------- | -------------------------------------- | ----------------- |
| `README.md`                   | Organization overview                  | Root              |
| `BEST_PRACTICES.md`           | Gold standard practices                | `docs/guides/`    |
| `GIT_WORKFLOW.md`             | Git conventions and branching          | `docs/workflows/` |
| `AI_IMPLEMENTATION_NOTES.txt` | Complete AI GitHub management protocol | `docs/guides/`    |
| `copilot-instructions.md`     | Code review checklist for PRs          | `.github/`        |
| `labeler.yml`                 | Path-based auto-labeling rules         | `.github/`        |
| `dependabot.yml`              | Dependency update configuration        | `.github/`        |
| `renovate.json`               | Advanced dependency management         | `.config/`        |
| `.semgrep/rules.yml`          | Custom security scanning rules         | `.semgrep/`       |

---

## Development Workflows

### Branch Strategy (Modified Git Flow)

```
main (production)
  ├── develop (integration)
  │   ├── feature/user-authentication
  │   ├── feature/payment-integration
  │   └── bugfix/fix-login-error
  ├── release/v1.2.0
  └── hotfix/critical-security-fix
```

#### Branch Types

1. **`main`** - Production-ready code

   - Highest protection level
   - No direct commits
   - Requires PR approval
   - All checks must pass
   - Signed commits required

2. **`develop`** - Integration branch

   - High protection level
   - Auto-deploys to staging
   - Merges from feature branches

3. **`feature/*`** - New features or enhancements

   - Naming: `feature/short-description` or `feature/TICKET-123-description`
   - Base: `develop`
   - Merge to: `develop`
   - Delete after merging

4. **`release/*`** - Prepare for production

   - Naming: `release/v1.2.0`
   - Base: `develop`
   - Merge to: Both `main` and `develop`
   - Only version bumps, final testing, bug fixes

5. **`hotfix/*`** - Urgent production fixes

   - Naming: `hotfix/critical-fix-description`
   - Base: `main`
   - Merge to: Both `main` and `develop`
   - Highest priority

6. **`bugfix/*`** - Non-critical bug fixes
   - Naming: `bugfix/fix-login-error`
   - Base: `develop`
   - Merge to: `develop`

#### Claude-Created Branches

When Claude creates branches, they follow the pattern:

```
claude/claude-md-<hash>-<model-id>
```

Example: `claude/claude-md-mi3ttr1cgn2h0j04-015VPcZYnRno1ergLmxSZAPL`

---

## Commit Conventions

### Conventional Commits Format

**STRICTLY ENFORCED** via `pr-quality-checks.yml` workflow.

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Commit Types

| Type       | Description             | Use When                                |
| ---------- | ----------------------- | --------------------------------------- |
| `feat`     | New feature             | Adding new functionality                |
| `fix`      | Bug fix                 | Fixing a bug                            |
| `docs`     | Documentation           | Updating docs only                      |
| `style`    | Code style              | Formatting, missing semicolons, etc.    |
| `refactor` | Code refactoring        | Restructuring without changing behavior |
| `perf`     | Performance improvement | Optimizing performance                  |
| `test`     | Adding/updating tests   | Test-related changes                    |
| `build`    | Build system            | Changes to build process                |
| `ci`       | CI/CD changes           | Workflow or pipeline changes            |
| `chore`    | Maintenance             | Routine tasks, dependency updates       |

### Examples

```bash
# Good commits
feat: add user authentication
feat(api): implement JWT token validation
fix: resolve memory leak in data processor
fix(login): correct password validation logic
docs: update API documentation
refactor: simplify database query logic
perf(images): optimize image loading strategy
test: add unit tests for payment module
ci: update deployment workflow
chore: upgrade dependencies

# Bad commits (will fail CI)
Add authentication
Fixed bug
Update code
WIP
```

### Commit Validation

The `commit-tracking.yml` workflow validates:

- Conventional commit format
- Message length (>10 characters)
- Type validity
- Generates statistics by author

Weekly reports are auto-generated every Monday and stored in `reports/`.

---

## Pull Request Process

### PR Quality Checks

All PRs must pass automated quality checks defined in `.github/workflows/pr-quality-checks.yml`:

#### 1. Conventional Commit Title

- PR title must follow conventional commit format
- Example: `feat(auth): add OAuth2 support`

#### 2. Description Requirements

- Minimum 50 characters
- Should explain WHAT and WHY
- Reference related issues

#### 3. Linked Issues

- PRs should reference issues with keywords:
  - `Closes #123`, `Fixes #456`, `Resolves #789`
  - `Related to #234`, `Part of #567`

#### 4. Checklist Completion

- Review checklist in PR template
- Check applicable items before requesting review

#### 5. All CI Checks Must Pass

- CodeQL security scan
- Semgrep security audit
- Dependency review
- Link checker
- Code coverage
- Any project-specific tests

### Auto-Labeling

PRs are automatically labeled based on:

**By Path** (`.github/labeler.yml`):

- `frontend` - Changes to UI/client code
- `backend` - Changes to server/API code
- `docs` - Changes to documentation
- `ci/cd` - Changes to workflows
- `security` - Changes to security-related files

**By Size**:

- `size/XS` - <10 lines
- `size/S` - 10-99 lines
- `size/M` - 100-499 lines
- `size/L` - 500-999 lines
- `size/XL` - 1000+ lines

### Auto-Assignment

The `auto-assign.yml` workflow automatically:

- Assigns PR to the author
- Requests reviews from CODEOWNERS
- Adds team-based reviewers

### PR Templates

Use specialized templates via `?template=<name>.md`:

- `bug_fix.md` - Bug fixes with reproduction steps
- `feature.md` - New features with use cases
- `documentation.md` - Documentation updates
- `refactoring.md` - Code refactoring
- `performance.md` - Performance improvements

**Default**: `PULL_REQUEST_TEMPLATE.md`

---

## GitHub Copilot Customizations

This repository includes **300+ GitHub Copilot customizations** from [github/awesome-copilot](https://github.com/github/awesome-copilot).

### 1. Agents (14 files)

**Purpose**: MCP-integrated specialists that connect to external services

**Structure**:

```yaml
---
name: Agent Name
description: Detailed capabilities
tools: ["read", "edit", "search", "shell", "mcp-tool/*"]
mcp-servers:
  service-name:
    type: "local"
    command: "docker"
    args: [...]
---
# Agent instructions follow
```

**Key Agents**:

- **Terraform Agent** (`terraform.agent.md`) - IaC automation with Terraform MCP server integration
- **C# Expert** (`CSharpExpert.agent.md`) - .NET development specialist
- **Dynatrace Expert** (`dynatrace-expert.agent.md`) - Observability and monitoring
- **PagerDuty Incident Responder** - Incident management automation
- **LaunchDarkly Flag Cleanup** - Feature flag lifecycle management

**Documentation**: `docs/README.agents.md` (23KB)

### 2. Instructions (109 files)

**Purpose**: Auto-apply based on file patterns to enforce coding standards

**Structure**:

```yaml
---
description: "What this instruction does"
applyTo: "**/*.ts, **/*.html"
---
# Instructions follow
```

**Key Instructions**:

- **Angular** (`angular.instructions.md`) - Angular 19+ with Signals, standalone components, OnPush strategy
- **Terraform** (`terraform-azure.instructions.md`) - 2-space indentation, alphabetical vars, HCP backend
- **Python FastAPI** (`python-fastapi.instructions.md`) - Type hints, async/await, best practices
- **Bicep** (`bicep-code-best-practices.md`) - Azure IaC standards
- **React** - Modern hooks, TypeScript, component patterns

**Documentation**: `docs/README.instructions.md` (104KB)

**File Naming Convention**: `lowercase-with-hyphens.instructions.md`

### 3. Prompts (114 files)

**Purpose**: Task-specific automation accessible via `/` commands

**Structure**:

```yaml
---
mode: 'agent' or 'ask'
description: 'What this prompt does'
tools: ['read', 'edit', 'search']  # Optional but encouraged
model: 'claude-sonnet-4.5'          # Strongly encouraged
---
# Prompt content
```

**Usage**: `/awesome-copilot <prompt-name>` in GitHub Copilot Chat

**Key Prompts**:

- **Architecture**:
  - `architecture-blueprint.prompt.md` - Generate system architecture
  - `adr-generator.prompt.md` - Create Architecture Decision Records
  - `breakdown-epic-arch.prompt.md` - Decompose epics into tasks
- **Development**:
  - `conventional-commit.prompt.md` - Generate commit messages
  - `code-review.prompt.md` - Perform code reviews
  - `test-generation.prompt.md` - Generate test cases
- **DevOps**:
  - `dockerfile-creation.prompt.md` - Containerization
  - `cost-optimization.prompt.md` - Cloud cost analysis
- **Documentation**:
  - `create-readme.prompt.md` - Generate README files
  - `api-documentation.prompt.md` - API docs

**Documentation**: `docs/README.prompts.md` (110KB)

**File Naming Convention**: `lowercase-with-hyphens.prompt.md`

### 4. Chat Modes (87 files)

**Purpose**: Specialized AI personas for different development contexts

**Structure**:

```yaml
---
description: "Role and capabilities"
tools: ["read", "edit"] # Optional but encouraged
model: "claude-sonnet-4.5" # Strongly encouraged
---
# Persona instructions
```

**Key Chat Modes**:

- **Architecture**:
  - `azure-principal-architect.md` - WAF-based architecture with MCP docs integration
  - `solution-architect.md` - System design expert
- **Development**:
  - `expert-rust-software-engineer.md` - Rust expertise
  - `expert-react-software-engineer.md` - React/TypeScript expertise
  - `expert-dotnet-software-engineer.md` - .NET/C# expertise
- **Specialized**:
  - `Ultimate-Transparent-Thinking-Beast-Mode.md` - Extended reasoning with full transparency
  - `power-bi-dax-expert.md` - BI development
  - `postgresql-dba.md`, `ms-sql-dba.md` - Database specialists
- **Maintenance**:
  - `csharp-dotnet-janitor.md` - Code cleanup specialist
  - `typescript-react-janitor.md` - React code cleanup

**Documentation**: `docs/README.chatmodes.md` (81KB)

**File Naming Convention**: `lowercase-with-hyphens.chatmode.md` or `PascalCase.md`

### 5. Collections (27 collections, 55 files)

**Purpose**: Curated bundles of related prompts, instructions, chat modes

**Key Collections**:

- **Cloud**:
  - `azure-cloud-development.yml` - IaC (Bicep/Terraform), Functions, Logic Apps, Architecture
- **MCP Development**:
  - `typescript-mcp-development.yml`, `python-mcp-development.yml`
  - Language-specific: Go, Rust, C#, Java, Kotlin, Swift, Ruby, PHP, Clojure
- **Domains**:
  - `security-best-practices.yml` - Security-focused tools
  - `testing-and-automation.yml` - QA and test automation
  - `frontend-web-dev.yml` - React, Angular, Vue
  - `database-data-management.yml` - Database and data management
  - `edge-ai-tasks.collection.yml` - Edge AI and machine learning tasks
- **Microsoft Power Platform**:
  - `power-platform.yml` - Power Platform development
  - `power-apps.yml` - Power Apps customizations
  - `power-bi.yml` - Power BI and analytics
- **Project Management**:
  - `project-planning.yml` - Project planning and management
  - `technical-spike.yml` - Technical spike exploration
  - `partners.yml` - Partner integrations

**Documentation**: `docs/README.collections.md`

### Copilot Code Review Checklist

File: `.github/copilot-instructions.md`

Applied during code reviews, checks for:

**Prompt Files** (`.prompt.md`):

- Has markdown front matter
- Has `mode` field (`agent` or `ask`)
- Has `description` field (in single quotes)
- File name is lowercase with hyphens
- Encouraged: `tools` field
- Strongly encouraged: `model` field

**Instruction Files** (`.instructions.md`):

- Has markdown front matter
- Has `description` field (in single quotes)
- Has `applyTo` field with file patterns
- File name is lowercase with hyphens

**Chat Mode Files** (`.chatmode.md`):

- Has markdown front matter
- Has `description` field (in single quotes)
- File name is lowercase with hyphens
- Encouraged: `tools` field
- Strongly encouraged: `model` field

**README Updates**:

- New files added to `README.md`

### 6. Chaos Zone

**Location**: `chaos-zone/` directory

**Purpose**: Temporary holding area for unorganized, unstructured, or work-in-progress content. Think of it as the repository's "inbox" for quickly uploading content without worrying about structure.

**Structure**:

```
chaos-zone/
├── README.md         # Usage guidelines
├── chats/            # AI chat transcripts and conversation logs
├── drafts/           # Work-in-progress documents before refinement
├── ideas/            # Brainstorming notes and quick ideas
└── misc/             # Everything else that doesn't fit elsewhere
```

**What Goes Here**:

- Raw chat transcripts from AI conversations
- Draft documents before they're refined
- Brainstorming notes and ideas
- Screenshots and temporary files
- Anything that doesn't have a clear home yet
- Content that needs to be reviewed and organized later

**Best Practices**:

- ✅ Use descriptive filenames with dates (YYYY-MM-DD format)
- ✅ Dump content quickly without worrying about formatting
- ✅ Review and organize periodically (suggested: monthly)
- ❌ Don't let content sit here indefinitely
- ❌ Don't upload sensitive information (API keys, passwords, etc.)
- ❌ Don't store large binary files (use Git LFS or external storage)

**Maintenance**: The chaos zone should be reviewed monthly to move relevant content to appropriate directories, archive outdated material, and extract useful insights into proper documentation.

---

## Automation & CI/CD

### Workflow Categories

#### Security & Compliance (6 workflows)

1. **CodeQL Analysis** (`codeql-analysis.yml`)

   - **Languages**: Go, Python, Ruby, JavaScript/TypeScript
   - **Triggers**: Push, PR, weekly schedule
   - **Output**: SARIF to GitHub Security tab
   - **Queries**: Security and quality

2. **Semgrep** (`semgrep.yml`)

   - **Jobs**: 4 parallel jobs
     - Security audit (OWASP Top 10, CWE Top 25)
     - Secrets detection
     - Supply chain analysis
     - Diff scanning with PR comments
   - **Custom Rules**: `.semgrep/rules.yml` (1511 lines)
   - **Output**: SARIF, inline PR comments

3. **Dependency Review** (`dependency-review.yml`)

   - **Triggers**: Pull requests
   - **Checks**: Vulnerabilities, license compliance
   - **Blocks**: GPL-3.0, AGPL-3.0
   - **Allows**: MIT, Apache-2.0, BSD

4. **SBOM Generation** (`sbom-generation.yml`)

   - **Formats**: SPDX, CycloneDX
   - **Purpose**: Supply chain transparency

5. **Dependency Updates** (`dependabot.yml`)

   - **Ecosystems**: npm, pip, GitHub Actions, Docker, Go, Composer
   - **Schedule**: Weekly Monday 3 AM UTC
   - **Limits**: 5 PRs max per ecosystem
   - **Auto-labeling**: `dependencies` tag

6. **Renovate** (`renovate.json`)
   - **Features**: Dependency dashboard, smart grouping
   - **Schedule**: Before 4 AM Monday
   - **Limits**: 10 concurrent PRs, 5/hour
   - **Pin Strategy**: Reproducible builds

#### Quality Assurance (8 workflows)

1. **Auto-Labeler** (`auto-labeler.yml`)

   - Path-based labels: `frontend`, `backend`, `docs`, `ci/cd`, `security`
   - Size labels: `size/XS`, `size/S`, `size/M`, `size/L`, `size/XL`

2. **Auto-Assign** (`auto-assign.yml`)

   - Assigns PR to author
   - Requests reviews from CODEOWNERS
   - Team-based reviewers

3. **PR Quality Checks** (`pr-quality-checks.yml`)

   - Conventional commit title
   - Description length >50 characters
   - Linked issues check
   - Checklist completion

4. **Link Checker** (`link-checker.yml`)

   - Weekly validation of markdown links
   - Runs on PRs modifying documentation

5. **Community Health** (`community-health.yml`)

   - Stale issue management
   - 60 days inactive → 7 days warning → close
   - Labels: `stale`, `no-issue-activity`

6. **Welcome Bot** (`welcome.yml`)

   - Greets first-time contributors
   - Links to CONTRIBUTING.md, CODE_OF_CONDUCT.md

7. **Code Coverage** - Tracks test coverage metrics

8. **Accessibility Testing** - WCAG 2.1 compliance validation

#### AI & Code Intelligence (9 workflows)

1. **Claude Code Review** (`claude-code-review.yml`)

   - AI-powered PR reviews
   - Analyzes: security, performance, best practices
   - Posts review comments

2. **OpenAI Workflow** (`openai_workflow.yml`)

   - OpenAI API integration for code analysis
   - Configurable for various AI tasks

3. **Gemini Workflow** (`gemini_workflow.yml`)

   - Google Gemini integration
   - Multi-modal AI capabilities

4. **Grok Workflow** (`grok_workflow.yml`)

   - xAI Grok integration
   - Real-time AI assistance

5. **Perplexity Workflow** (`perplexity_workflow.yml`)

   - Perplexity AI integration
   - Research and code understanding

6. **Jules** (`jules.yml`)

   - AI-powered development assistant
   - Automated task execution

7. **Orchestrator** (`orchestrator.yml`)

   - Coordinates multi-AI workflows
   - Task distribution and management

8. **Process Queue** (`process_queue.yml`)

   - Async task processing
   - Quota management integration

9. **CI Advanced** (`ci-advanced.yml`)
   - Advanced continuous integration
   - AI-enhanced build and test automation

#### Metrics & Reporting (5 workflows)

1. **Commit Tracking** (`commit-tracking.yml`)

   - Validates commit messages
   - Generates statistics by author
   - Tracks activity patterns

2. **Weekly Commit Report** (`weekly-commit-report.yml`)

   - Auto-generated every Monday
   - 7-day activity summary
   - Stored in `reports/commit-report-YYYY-MM-DD.md`

3. **Repository Metrics** (`repo-metrics.yml`)

   - Monthly analytics
   - Issue/PR timing
   - Contributor stats
   - Language breakdown

4. **Performance Benchmarking** - Performance regression detection

5. **Mutation Testing** - Test effectiveness validation

#### Release Management (3 workflows)

1. **Semantic Release** (`semantic-release.yml`)

   - Automated releases based on conventional commits
   - Changelog generation
   - Version bumping
   - GitHub release creation

2. **Version Bump** (`version-bump.yml`)

   - Supports: major.minor.patch
   - Ecosystems: npm, Python, Rust

3. **Release** (`release.yml`)
   - Changelog generation
   - Asset uploads
   - Release notes

#### Orchestration & Quota Management (4 workflows)

1. **Orchestrator** (`orchestrator.yml`)

   - Coordinates multi-AI workflows
   - Manages task distribution across AI providers

2. **Process Queue** (`process_queue.yml`)

   - Async task processing with quota management
   - Handles background job execution

3. **Reset Quotas** (`reset_quotas.yml`)

   - Automated quota reset on schedule
   - Manages API rate limits

4. **Manual Reset** (`manual_reset.yml`)
   - Manual quota reset trigger
   - Emergency quota management

---

## Security & Compliance

### Multi-Layered Security

1. **SAST Scanning**:

   - CodeQL for multiple languages
   - Semgrep with custom rules (1511 lines)
   - Scheduled and event-driven

2. **Dependency Security**:

   - Dependency review on PRs
   - Dependabot weekly updates
   - Renovate advanced management
   - License compliance enforcement

3. **Secrets Detection**:

   - Semgrep secrets scanning
   - GitHub secret scanning (where enabled)
   - Pre-commit hooks

4. **Supply Chain**:
   - SBOM generation (SPDX, CycloneDX)
   - Supply chain analysis via Semgrep
   - Dependency provenance

### Compliance Features

- **License Validation**: Blocks GPL-3.0, AGPL-3.0; allows MIT, Apache-2.0, BSD
- **Security Policy**: `SECURITY.md` with vulnerability reporting process
- **Branch Protection**: Enforced via `BRANCH_PROTECTION.md`
- **Signed Commits**: Supported and encouraged
- **CODEOWNERS**: Code ownership and review requirements

### Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets or environment variables
2. **Review dependency updates** - Don't auto-merge security updates without review
3. **Respond to security alerts** - Within 24-48 hours
4. **Keep dependencies updated** - Weekly reviews via Dependabot/Renovate
5. **Enable branch protection** - On all production and integration branches

---

## Key Conventions

### File Naming Conventions

#### General

- Use `lowercase-with-hyphens.md` for documentation
- Use `UPPERCASE.md` for root-level important files (README, LICENSE, etc.)
- Use `.yml` (not `.yaml`) for GitHub Actions workflows

#### Copilot Customizations

- Agents: `lowercase-name.agent.md`
- Instructions: `lowercase-name.instructions.md`
- Prompts: `lowercase-name.prompt.md`
- Chat Modes: `lowercase-name.chatmode.md` or `PascalCase.md`
- Collections: `lowercase-name.yml`

### Code Organization

#### Terraform/IaC

- **Files**: `main.tf`, `variables.tf`, `outputs.tf`, `README.md`
- **Indentation**: 2 spaces
- **Ordering**: Alphabetical for variables and outputs
- **Separation**: `network.tf`, `compute.tf`, `security.tf`

#### Python

- **Type hints**: Always use
- **Async/await**: Prefer for I/O operations
- **Imports**: Grouped and sorted (stdlib, third-party, local)

#### JavaScript/TypeScript

- **Indentation**: 2 spaces
- **Quotes**: Single quotes for strings
- **Semicolons**: Required

### Documentation Standards

1. **README.md** - Must have:

   - Title and description
   - Table of contents (if >200 lines)
   - Installation instructions
   - Usage examples
   - Contributing section
   - License

2. **Code Comments**:

   - Use docstrings/JSDoc for functions
   - Explain WHY, not WHAT
   - Keep comments up-to-date

3. **Markdown**:
   - Use ATX-style headers (`#` not `===`)
   - Fenced code blocks with language
   - Reference-style links for readability

---

## AI Assistant Guidelines

### When Working with This Repository

#### DO:

1. **Use Conventional Commits** - ALWAYS format commits as `type(scope): description`

2. **Leverage Existing Workflows** - Don't recreate automation that already exists

3. **Follow Established Patterns**:

   - Use appropriate Copilot agents for specialized tasks
   - Apply instructions based on file types
   - Reference existing prompts for common tasks

4. **Respect Security Constraints**:

   - Never hardcode secrets
   - Don't bypass security checks
   - Always run security scans

5. **Update Documentation**:

   - When adding features, update relevant docs
   - Add new Copilot customizations to README files
   - Keep CHANGELOG.md current

6. **Use Auto-Labeling**:

   - Understand that PRs will be auto-labeled
   - Don't manually add labels that auto-labeler handles

7. **Reference Issues**:

   - Link PRs to issues with `Closes #123`, `Fixes #456`
   - Provide context in PR descriptions

8. **Test Thoroughly**:
   - Run all checks locally before pushing
   - Verify CI passes before requesting review

#### DON'T:

1. **Don't Bypass Quality Checks**:

   - Don't use `--no-verify` on commits
   - Don't push without running tests
   - Don't merge with failing CI

2. **Don't Create Duplicate Automation**:

   - Check existing workflows first
   - Reuse workflow templates where possible

3. **Don't Ignore Security Alerts**:

   - Always address CodeQL findings
   - Review Semgrep warnings
   - Update vulnerable dependencies

4. **Don't Commit Generated Files** (unless necessary):

   - Build artifacts
   - Lock files (if not needed)
   - IDE-specific files

5. **Don't Use Non-Standard Formats**:
   - Follow conventional commits strictly
   - Use established branch naming
   - Match existing code style

### Recommended Workflow for AI Assistants

1. **Understand the Task**:

   - Read relevant documentation
   - Check existing implementations
   - Identify applicable Copilot customizations

2. **Plan the Changes**:

   - Use TodoWrite tool to track tasks
   - Break down complex changes
   - Identify potential issues

3. **Implement**:

   - Follow established conventions
   - Use appropriate tools and agents
   - Write clean, documented code

4. **Test**:

   - Run local tests
   - Verify security scans pass
   - Check documentation builds

5. **Commit**:

   - Use conventional commit format
   - Write descriptive messages
   - Reference related issues

6. **Create PR**:

   - Use appropriate template
   - Write clear description
   - Link to issues
   - Complete checklist

7. **Respond to Feedback**:
   - Address review comments
   - Update based on CI failures
   - Keep PR up-to-date with base branch

### Leveraging Copilot Customizations

#### For Architecture Tasks

- Use **Azure Principal Architect** chat mode
- Apply `/awesome-copilot architecture-blueprint` prompt
- Reference architecture-related instructions

#### For Terraform/IaC

- Use **Terraform Agent** with MCP server
- Apply `terraform-azure.instructions.md`
- Follow 2-space indentation, alphabetical ordering

#### For Code Cleanup

- Use **Janitor chat modes** (C#, TypeScript, React)
- Focus on technical debt reduction
- Improve code quality metrics

#### For Documentation

- Use `/awesome-copilot create-readme` prompt
- Follow existing documentation patterns
- Ensure all new features are documented

#### For Security Reviews

- Use security-focused chat modes
- Apply security best practices instructions
- Run Semgrep with custom rules

---

## Common Tasks

### Task 1: Adding a New Copilot Instruction

```bash
# 1. Create the instruction file
touch instructions/my-framework.instructions.md

# 2. Add front matter and content
---
description: 'Instructions for my-framework development'
applyTo: '**/*.myext, **/my-framework/**'
---

# Instructions content here

# 3. Document in README
# Update docs/README.instructions.md

# 4. Commit with conventional format
git add instructions/my-framework.instructions.md docs/README.instructions.md
git commit -m "feat(copilot): add instructions for my-framework"

# 5. Create PR
git push -u origin feature/add-my-framework-instructions
# Create PR via GitHub UI or gh CLI
```

### Task 2: Adding a New Workflow

```bash
# 1. Create workflow file
touch .github/workflows/my-workflow.yml

# 2. Define workflow (see existing workflows for patterns)

# 3. Test locally (if possible)

# 4. Document in AUTOMATION_MASTER_GUIDE.md

# 5. Commit
git add .github/workflows/my-workflow.yml AUTOMATION_MASTER_GUIDE.md
git commit -m "ci: add workflow for my automation"

# 6. Create PR
git push -u origin feature/add-my-workflow
```

### Task 3: Updating Dependencies

```bash
# Option 1: Let Dependabot/Renovate handle it
# - PRs are created automatically every Monday
# - Review and merge

# Option 2: Manual update
# 1. Update package.json / requirements.txt / go.mod

# 2. Test changes
npm test  # or appropriate test command

# 3. Commit
git commit -m "chore(deps): update dependencies"

# 4. Create PR
git push -u origin chore/update-dependencies
```

### Task 4: Responding to Security Alert

```bash
# 1. Review alert in GitHub Security tab

# 2. Update vulnerable dependency
npm update vulnerable-package
# or
pip install --upgrade vulnerable-package

# 3. Test thoroughly
npm test

# 4. Commit
git commit -m "fix(security): update vulnerable-package to vX.Y.Z"

# 5. Create PR with security context
git push -u origin fix/security-vulnerable-package

# PR description should reference:
# - Security alert number
# - CVE (if applicable)
# - Testing performed
```

### Task 5: Creating a Release

```bash
# Releases are mostly automated via semantic-release.yml

# 1. Ensure all commits follow conventional commits
# - feat: triggers minor version bump
# - fix: triggers patch version bump
# - BREAKING CHANGE: triggers major version bump

# 2. Merge PR to main

# 3. semantic-release workflow runs automatically:
# - Analyzes commits since last release
# - Determines version bump
# - Generates CHANGELOG
# - Creates GitHub release
# - Tags commit

# Manual release (if needed):
# 1. Use version-bump.yml workflow
# 2. Or manually:
git tag v1.2.3
git push origin v1.2.3
```

### Task 6: Adding a New Repository to Organization

```bash
# Follow REPOSITORY_SETUP_CHECKLIST.md

# 1. Create repository via GitHub UI

# 2. Clone locally
git clone https://github.com/ivviiviivvi/new-repo.git
cd new-repo

# 3. Initialize with standard files (optional - inherited from .github)
# - Can override by creating local versions

# 4. Copy desired workflow templates
cp ../.github/workflow-templates/ci.yml .github/workflows/ci.yml

# 5. Configure Dependabot (optional - inherits from org)
cp ../.github/dependabot.yml .github/dependabot.yml

# 6. Apply labels from LABELS.md

# 7. Enable branch protection per BRANCH_PROTECTION.md

# 8. Initial commit
git add .
git commit -m "chore: initialize repository structure"
git push origin main
```

### Task 7: Fixing a Failing CI Check

```bash
# 1. Identify which check failed
# - View PR checks on GitHub
# - Click "Details" for failed check

# 2. Common failures:

# CodeQL failure:
# - Review security finding
# - Fix vulnerable code
# - Retest locally if possible

# Semgrep failure:
# - Review inline PR comment
# - Address security issue
# - May need to update .semgrep/rules.yml if false positive

# PR Quality Check failure:
# - Conventional commit title
# - Description length
# - Linked issues
# - Fix PR title/description

# Link Checker failure:
# - Fix broken links in markdown
# - Update or remove dead links

# 3. Push fix
git commit -m "fix(ci): address failing check"
git push

# 4. CI re-runs automatically
```

### Task 8: Using GitHub Copilot Customizations

#### In GitHub Copilot Chat:

```
# Use a prompt
/awesome-copilot architecture-blueprint

# Activate a chat mode
@workspace /mode azure-principal-architect

# Reference a collection
# Collections are automatically available based on your workspace
```

#### Instructions Apply Automatically:

- When editing `*.tf` files → Terraform instructions apply
- When editing `*.component.ts` → Angular instructions apply
- When editing `*.py` → Python instructions apply

#### Using an Agent:

Agents are configured in individual repositories that need them. See `docs/README.agents.md` for setup instructions.

---

## Quick Reference

### Essential Commands

```bash
# Start a new feature
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add my feature"

# Push and create PR
git push -u origin feature/my-feature
gh pr create --title "feat: add my feature" --body "Description"

# Update branch with latest develop
git checkout develop
git pull origin develop
git checkout feature/my-feature
git merge develop

# Squash commits (if needed)
git rebase -i develop
```

### Useful GitHub CLI Commands

```bash
# View PR status
gh pr status

# View PR checks
gh pr checks

# View PR diff
gh pr diff

# Merge PR
gh pr merge --squash

# View repository metrics
gh repo view --json name,description,stargazerCount,forkCount
```

### Documentation Quick Links

- **Getting Started**: `README.md`, `QUICK_START.md`
- **Best Practices**: `BEST_PRACTICES.md`
- **Git Workflow**: `GIT_WORKFLOW.md`
- **Contributing**: `CONTRIBUTING.md`
- **Security**: `SECURITY.md`, `SECURITY_ADVANCED.md`
- **AI Implementation**: `AI_CODE_INTELLIGENCE.md`, `for-ai-implementation.txt`
- **Automation**: `AUTOMATION_MASTER_GUIDE.md`
- **Copilot**:
  - Agents: `docs/README.agents.md`
  - Instructions: `docs/README.instructions.md`
  - Prompts: `docs/README.prompts.md`
  - Chat Modes: `docs/README.chatmodes.md`
  - Collections: `docs/README.collections.md`

---

## Summary

This `.github` repository represents a **comprehensive reference implementation** for organization-level GitHub management with:

- **300+ AI customizations** for GitHub Copilot
- **59 automated workflows** plus 14 reusable templates covering security, quality, metrics, and releases
- **Multi-layered security** scanning with CodeQL, Semgrep, and dependency review
- **Comprehensive documentation** (300KB+ of Copilot docs alone)
- **Strict quality enforcement** via automated PR checks
- **Conventional commits** strictly enforced
- **Community-focused** with templates and welcoming automation
- **AI-first development** with Claude, GitHub Copilot, and multiple AI providers

### Key Takeaways for AI Assistants

1. **Always use conventional commits** - This is strictly enforced
2. **Leverage existing automation** - Don't recreate what exists
3. **Follow security best practices** - Multiple layers of scanning
4. **Use Copilot customizations** - 300+ agents, instructions, prompts, modes
5. **Document everything** - Update docs with every change
6. **Test thoroughly** - All CI checks must pass
7. **Respect conventions** - File naming, code organization, branching

### Getting Help

- **Documentation**: Check `docs/` directory first
- **Support**: See `SUPPORT.md`
- **Contributing**: See `CONTRIBUTING.md`
- **Security**: See `SECURITY.md`
- **Issues**: Use issue templates in `ISSUE_TEMPLATE/`

---

**Last Updated**: 2025-11-18
**Maintained by**: ivviiviivvi organization
**License**: MIT
