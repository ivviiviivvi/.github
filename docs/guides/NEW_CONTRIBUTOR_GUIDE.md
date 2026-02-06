# New Contributor Guide

> **Welcome! This guide will help you get started contributing to the
> {{ORG_NAME}}/.github organization repository**

**Estimated Time to Setup**: 30-45 minutes

______________________________________________________________________

## Table of Contents

- [Welcome](#welcome)
- [Quick Start](#quick-start)
- [Development Environment Setup](#development-environment-setup)
- [Repository Structure](#repository-structure)
- [Making Your First Contribution](#making-your-first-contribution)
- [Testing Your Changes](#testing-your-changes)
- [Documentation Guidelines](#documentation-guidelines)
- [Workflow Development](#workflow-development)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Getting Help](#getting-help)

______________________________________________________________________

## Welcome

Thank you for your interest in contributing to our organization's shared GitHub
configuration repository! This repository contains:

- **Workflow templates** for GitHub Actions across all organization repositories
- **Custom agents** for specialized AI-assisted development tasks
- **Documentation** for organizational standards and best practices
- **Automation scripts** for repository management and maintenance
- **Testing infrastructure** to ensure quality and reliability

### What You'll Learn

By following this guide, you'll learn how to:

1. Set up your development environment (local or DevContainer)
1. Navigate the repository structure
1. Make changes following our standards
1. Test your changes before submitting
1. Submit pull requests that get merged quickly

______________________________________________________________________

## Quick Start

**TL;DR - Get coding in 5 minutes:**

```bash
# 1. Fork and clone
gh repo fork {{ORG_NAME}}/.github --clone

# 2. Open in VS Code with DevContainer (recommended)
cd .github
code .
# Press Cmd/Ctrl+Shift+P → "Dev Containers: Reopen in Container"

# 3. Create a branch
git checkout -b feature/my-contribution

# 4. Make changes, test, commit
pytest tests/
git add -A
git commit -m "feat: your change description"

# 5. Push and create PR
git push origin feature/my-contribution
gh pr create --fill
```

**Done!** Continue reading for detailed explanations.

______________________________________________________________________

## Development Environment Setup

### Prerequisites

Install these tools before starting:

| Tool               | Purpose              | Installation                                                                                                          |
| ------------------ | -------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Git**            | Version control      | [git-scm.com](https://git-scm.com/)                                                                                   |
| **GitHub CLI**     | GitHub operations    | `brew install gh` or [cli.github.com](https://cli.github.com/)                                                        |
| **VS Code**        | Code editor          | [code.visualstudio.com](https://code.visualstudio.com/)<!-- link:docs.vscode -->                                      |
| **Docker Desktop** | DevContainer support | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)<!-- link:docs.docker_desktop --> |

### Option 1: DevContainer Setup (Recommended)

**Why DevContainer?**

- Instant environment with all tools pre-installed
- Consistent across all contributors
- No conflicts with your local system

**Steps:**

1. **Install Prerequisites**:

   - VS Code +
     [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)<!-- link:docs.vscode_remote_containers -->
   - Docker Desktop (running)

1. **Clone and Open**:

   ```bash
   git clone https://github.com/{{ORG_NAME}}/.github.git
   cd .github
   code .
   ```

1. **Reopen in Container**:

   - VS Code will prompt: "Reopen in Container"
   - Or manually: `Cmd/Ctrl + Shift + P` → "Dev Containers: Reopen in Container"
   - Wait 5-10 minutes for first-time build

1. **Verify Setup**:

   ```bash
   # Check tools are available
   python --version  # Should show 3.11+
   node --version    # Should show 20+
   pytest --version  # Should show 7.4+
   gh --version      # Should show 2.40+
   ```

**What's Included:**

- Python 3.11, Node.js 20, Go 1.21, Rust latest
- pytest, black, flake8, mypy (Python tools)
- ESLint, Prettier (JavaScript tools)
- GitHub CLI, Docker CLI
- All VS Code extensions (Copilot, GitLens, Python, etc.)

### Option 2: Local Setup

**For developers who prefer local development:**

1. **Clone Repository**:

   ```bash
   git clone https://github.com/{{ORG_NAME}}/.github.git
   cd .github
   ```

1. **Install Python Dependencies**:

   ```bash
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt  # If exists
   pip install pytest black flake8 mypy pytest-cov
   ```

1. **Install Node.js Dependencies** (if working with workflows):

   ```bash
   npm install -g @actions/toolkit @actions/core
   ```

1. **Configure Git**:

   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

1. **Install Pre-commit Hooks**:

   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Verify Your Setup

Run these commands to ensure everything works:

```bash
# Python tests
pytest tests/ -v

# Python linting
flake8 automation/scripts/

# Git status
git status

# GitHub CLI
gh auth status
```

**Expected Output**: All commands should complete without errors.

______________________________________________________________________

## Repository Structure

Understanding the repository layout helps you find what you need:

```
.github/
├── workflows/              # GitHub Actions workflows (99 files)
│   ├── reusable/          # Reusable workflow components
│   ├── safeguard-*.yml    # Security safeguard workflows
│   ├── test-*.yml         # Testing workflows
│   └── *.yml              # Various automation workflows
│
├── copilot-instructions/   # GitHub Copilot custom instructions (100+ files)
│   └── *.instructions.md  # Language and framework standards
│
├── DISCUSSION_TEMPLATE/    # GitHub Discussions templates
│   ├── announcements.yml
│   ├── ideas.yml
│   └── q-and-a.yml
│
├── ISSUE_TEMPLATE/         # GitHub Issues templates
│   ├── bug_report.yml
│   ├── feature_request.yml
│   └── documentation.yml
│
└── PULL_REQUEST_TEMPLATE.md

ai_framework/              # AI agent system
├── agents/               # Custom agents (26+ agents)
│   ├── *.agent.md        # Agent definitions
│   └── README.md
├── chatmodes/            # AI chat modes (85+ modes)
│   ├── *.chatmode.md     # Chat mode definitions
│   └── README.md
├── prompts/              # Reusable prompts
│   ├── *.prompt.md       # Prompt templates
│   └── README.md
├── collections/          # Curated bundles
│   └── *.collection.yml  # Resource collections
└── INDEX.md              # Navigation for 188 files

automation/
├── scripts/              # Python automation scripts
│   ├── web_crawler.py           # Security-critical web crawler
│   ├── org_health_visualizer.py  # Workflow visualization
│   ├── sync_labels_gh.py        # Label synchronization
│   ├── natural_language_prompt_filter.py     # Content filtering
│   └── update_agent_docs.py     # Agent documentation
└── workflow-templates/   # Workflow templates for copy

docs/
├── guides/              # User guides
│   ├── monitoring.md            # Monitoring & observability
│   ├── testing-best-practices.md # Testing standards
│   └── NEW_CONTRIBUTOR_GUIDE.md  # This file!
├── AGENT_REGISTRY.md           # Catalog of all agents
├── CONTRIBUTING.md             # Contribution guidelines
├── COPILOT_QUICK_START.md      # GitHub Copilot setup
└── INDEX.md                    # Documentation index

tests/
├── unit/                # Unit tests (4 files, 989 lines)
│   ├── test_web_crawler.py
│   ├── test_org_health_visualizer.py
│   ├── test_sync_labels.py
│   └── test_natural_language_prompt_filter.py
├── integration/         # Integration tests
│   └── test_agent_tracking.py
├── conftest.py          # Shared fixtures
└── pytest.ini           # Test configuration

project_meta/           # Project metadata and tracking
├── context-handoff/   # Context generation for AI
└── reports/           # Analysis reports
```

### Key Files

| File                      | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| `CLEANUP_ROADMAP.md`      | Project roadmap (10 phases, 90% complete)     |
| `CONTRIBUTING.md`         | Contribution guidelines                       |
| `pytest.ini`              | Test configuration (80% coverage target)      |
| `.pre-commit-config.yaml` | Pre-commit hooks (formatting, linting, tests) |
| `README.md`               | Repository overview                           |

______________________________________________________________________

## Making Your First Contribution

Follow this workflow for all contributions:

### 1. Find or Create an Issue

**Before starting work:**

```bash
# Search for existing issues
gh issue list --search "keyword"

# Create a new issue if none exists
gh issue create --title "Add feature X" --body "Description of feature"
```

**Issue Labels**:

- `good first issue` - Great for new contributors
- `documentation` - Documentation improvements
- `bug` - Something isn't working
- `enhancement` - New feature or request

### 2. Create a Branch

**Naming Convention**: `type/short-description`

```bash
# Feature branch
git checkout -b feature/add-monitoring-dashboard

# Bug fix branch
git checkout -b fix/workflow-failure-alert

# Documentation branch
git checkout -b docs/update-contributor-guide
```

**Branch Types**:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Adding tests
- `chore/` - Maintenance tasks

### 3. Make Your Changes

**Follow Our Standards**:

- **Python**: Follow PEP 8, use type hints, add docstrings
- **Markdown**: Use proper formatting, check with linters
- **Workflows**: Use reusable workflows, pin actions to SHAs
- **Documentation**: Update relevant docs with your changes

**Example - Adding a Python Script**:

```python
"""
Module docstring explaining purpose.

This module provides functionality for X.
"""
from typing import List, Optional

def process_data(items: List[str], threshold: Optional[int] = None) -> dict:
    """
    Process a list of items with an optional threshold.

    Args:
        items: List of strings to process
        threshold: Optional integer threshold (default: None)

    Returns:
        Dictionary with processing results

    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")

    # Implementation here
    return {"processed": len(items)}
```

### 4. Test Your Changes

**Run Tests Locally**:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_web_crawler.py -v

# Run specific test
pytest tests/unit/test_web_crawler.py::TestSSRFProtection::test_blocks_localhost -v
```

**Expected Results**:

- All tests pass (green)
- Coverage ≥70% (enforced by CI)
- No new warnings or errors

**Run Linters**:

```bash
# Python linting
flake8 automation/scripts/
black --check automation/scripts/
mypy automation/scripts/

# Auto-fix Python formatting
black automation/scripts/

# Markdown linting (if mdformat available)
mdformat --check docs/
```

### 5. Commit Your Changes

**Commit Message Format**:

```
type(scope): brief description

Detailed explanation of what and why (optional).

Fixes #123
```

**Commit Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding tests
- `refactor`: Code refactoring
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples**:

```bash
# Feature commit
git commit -m "feat(monitoring): add workflow health dashboard

Implements real-time dashboard showing workflow success rates,
average durations, and resource consumption.

Closes #456"

# Bug fix commit
git commit -m "fix(crawler): prevent SSRF attacks on private IPs

Adds validation to block access to 127.0.0.1, 10.0.0.0/8,
192.168.0.0/16, and 169.254.169.254 (AWS metadata).

Fixes #789"

# Documentation commit
git commit -m "docs: update contribution guidelines

Adds section on DevContainer setup and testing requirements."
```

### 6. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/add-monitoring-dashboard

# Create pull request
gh pr create --title "feat(monitoring): add workflow health dashboard" \
  --body "## Description

This PR adds a real-time dashboard for monitoring workflow health.

## Changes
- Added metrics-dashboard.yml workflow
- Created dashboard HTML template
- Updated monitoring.md documentation

## Testing
- ✅ All unit tests pass
- ✅ Dashboard generates correctly
- ✅ Coverage at 85%

Closes #456"
```

**PR Checklist**:

- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] Linked to relevant issue(s)

### 7. Respond to Review Feedback

**When reviewers request changes:**

```bash
# Make the requested changes
# ... edit files ...

# Commit changes
git add -A
git commit -m "address review feedback: improve error handling"

# Push updates
git push origin feature/add-monitoring-dashboard
```

**Tips for Good PRs**:

- Keep PRs focused (one feature/fix per PR)
- Respond to feedback promptly
- Ask questions if feedback is unclear
- Be open to suggestions
- Thank reviewers for their time

______________________________________________________________________

## Testing Your Changes

### Running Tests

**Basic Test Commands**:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific directory
pytest tests/unit/

# Run with coverage report
pytest --cov --cov-report=html
open htmlcov/index.html  # View coverage report
```

**Using Test Markers**:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only security tests
pytest -m security

# Skip slow tests
pytest -m "not slow"
```

### Writing Tests

**Test File Structure**:

```python
# tests/unit/test_my_feature.py
"""Tests for my_feature module."""
import pytest
from automation.scripts.my_feature import process_data


class TestProcessData:
    """Test suite for process_data function."""

    def test_basic_functionality(self):
        """Test basic data processing."""
        result = process_data(["item1", "item2"])
        assert result["processed"] == 2

    def test_empty_input_raises_error(self):
        """Test that empty input raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            process_data([])

    @pytest.mark.parametrize("items,expected", [
        (["a"], 1),
        (["a", "b"], 2),
        (["a", "b", "c"], 3),
    ])
    def test_various_input_sizes(self, items, expected):
        """Test processing different input sizes."""
        result = process_data(items)
        assert result["processed"] == expected
```

**Using Fixtures**:

```python
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return ["item1", "item2", "item3"]


def test_with_fixture(sample_data):
    """Test using the fixture."""
    result = process_data(sample_data)
    assert result["processed"] == 3
```

### Test Coverage Requirements

| Code Type          | Coverage Required     |
| ------------------ | --------------------- |
| Security-critical  | 100%                  |
| Core functionality | 80%+                  |
| Utility functions  | 70%+                  |
| Scripts            | 70%+ (enforced by CI) |

**Check Coverage**:

```bash
# Generate coverage report
pytest --cov --cov-report=term-missing

# View detailed HTML report
pytest --cov --cov-report=html
open htmlcov/index.html
```

______________________________________________________________________

## Documentation Guidelines

### When to Update Documentation

Update documentation when you:

- Add new features
- Change existing behavior
- Add new workflows or scripts
- Fix bugs that affect user experience
- Add new best practices

### Documentation Types

| Type          | Location       | Purpose                       |
| ------------- | -------------- | ----------------------------- |
| **Guides**    | `docs/guides/` | Step-by-step instructions     |
| **Reference** | `docs/`        | API docs, registries, indexes |
| **README**    | Various        | Quick overview of directories |
| **Inline**    | Code           | Docstrings, comments          |

### Writing Good Documentation

**Do:**

- ✅ Use clear, simple language
- ✅ Include code examples
- ✅ Add screenshots/diagrams where helpful
- ✅ Keep it up to date
- ✅ Link to related documentation
- ✅ Include troubleshooting tips

**Don't:**

- ❌ Assume prior knowledge
- ❌ Use jargon without explanation
- ❌ Write overly long paragraphs
- ❌ Forget to update dates
- ❌ Leave broken links

### Markdown Standards

```markdown
# Main Title (H1 - only one per file)

> **Brief description with emphasis**

## Section (H2)

### Subsection (H3)

**Bold for emphasis**
_Italic for subtle emphasis_

- Bullet lists for items
- Use hyphens consistently

1. Numbered lists for steps
2. In sequential order

`inline code` for commands and filenames

\`\`\`bash

# Code blocks with language specified

command --flag value
\`\`\`

[Link text](relative/path/to/file.md)

| Column 1 | Column 2 |
| -------- | -------- |
| Data 1   | Data 2   |
```

### Adding to Documentation Index

When creating new documentation, add it to `docs/INDEX.md`:

```markdown
### [Category]

- [Your New Doc](path/to/your-doc.md) - Brief description
```

______________________________________________________________________

## Workflow Development

### Creating a New Workflow

**1. Start with a Template**:

```yaml
name: My New Workflow

on:
  workflow_dispatch: # Start with manual trigger
  push:
    branches: [main]
    paths:
      - "relevant/path/**"

permissions:
  contents: read # Minimal permissions

jobs:
  my-job:
    runs-on: ubuntu-latest
    timeout-minutes: 10 # Always set timeout

    steps:
      - name: Checkout code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4

      - name: Your step
        run: |
          echo "Do something"
```

**2. Follow Best Practices**:

- ✅ Pin actions to full commit SHAs (not tags)
- ✅ Set explicit `permissions`
- ✅ Add `timeout-minutes` to all jobs
- ✅ Use `concurrency` to prevent duplicate runs
- ✅ Add meaningful descriptions
- ✅ Test with `workflow_dispatch` first

**3. Security Checklist**:

- [ ] Actions pinned to SHAs
- [ ] Minimal permissions used
- [ ] No secrets in logs
- [ ] Input validation added
- [ ] Timeout set
- [ ] Concurrency configured

**4. Test Your Workflow**:

```bash
# Push workflow to branch
git add .github/workflows/my-workflow.yml
git commit -m "feat(ci): add my new workflow"
git push origin feature/my-workflow

# Manually trigger workflow
gh workflow run my-workflow.yml --ref feature/my-workflow

# Check run status
gh run list --workflow my-workflow.yml --limit 1

# View logs
gh run view $(gh run list -w my-workflow.yml --limit 1 --json databaseId -q '.[0].databaseId') --log
```

### Reusable Workflows

**When to Create Reusable Workflows**:

- Logic used by 3+ workflows
- Complex multi-step processes
- Standardized patterns (build, test, deploy)

**Example**:

```yaml
# .github/workflows/reusable/test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pytest tests/
```

**Using Reusable Workflows**:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push]

jobs:
  test:
    uses: ./.github/workflows/reusable/test.yml
    with:
      python-version: "3.11"
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

______________________________________________________________________

## Troubleshooting

### Common Issues

#### 1. Pre-commit Hooks Failing

**Symptom**: `git commit` fails with pre-commit errors

**Solutions**:

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Auto-fix issues
pre-commit run --all-files

# Stage fixed files
git add -A

# Try commit again
git commit -m "your message"

# Skip pre-commit (use sparingly)
git commit --no-verify -m "your message"
```

#### 2. Tests Failing Locally

**Symptom**: `pytest` shows failures

**Solutions**:

```bash
# Install test dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run verbose to see details
pytest -v

# Run single failing test
pytest tests/unit/test_file.py::test_name -v

# Clear pytest cache
pytest --cache-clear
rm -rf .pytest_cache __pycache__

# Check Python version
python --version  # Should be 3.10+
```

#### 3. Import Errors in Tests

**Symptom**: `ModuleNotFoundError` when running tests

**Solutions**:

```bash
# Ensure you're in the repository root
cd /workspace

# Install package in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# In DevContainer, this should be automatic
```

#### 4. DevContainer Won't Build

**Symptom**: DevContainer build fails or hangs

**Solutions**:

```bash
# Rebuild without cache
Cmd/Ctrl+Shift+P → "Dev Containers: Rebuild Container Without Cache"

# Check Docker is running
docker ps

# Clear Docker cache
docker system prune -a

# Check logs
Cmd/Ctrl+Shift+P → "Dev Containers: Show Log"
```

#### 5. GitHub CLI Not Authenticated

**Symptom**: `gh` commands fail with authentication error

**Solutions**:

```bash
# Authenticate
gh auth login

# Check status
gh auth status

# Refresh token
gh auth refresh
```

#### 6. Workflow Not Triggering

**Symptom**: Pushed changes but workflow didn't run

**Causes & Solutions**:

```bash
# Check workflow syntax
actionlint .github/workflows/my-workflow.yml

# Verify file paths in triggers
git diff --name-only HEAD~1 HEAD

# Check if workflow is disabled
gh workflow list

# Enable workflow
gh workflow enable my-workflow.yml

# Manually trigger
gh workflow run my-workflow.yml
```

### Getting Unstuck

**When you're stuck**:

1. **Read error messages carefully** - They usually tell you what's wrong
1. **Check documentation** - Guides are comprehensive and searchable
1. **Search existing issues** - Someone may have solved it already
1. **Ask in Discussions** - Team is happy to help
1. **Pair with a mentor** - Reach out to experienced contributors

______________________________________________________________________

## FAQ

### General Questions

**Q: How long does it take to get a PR merged?**

A: Typically 1-3 business days. Simple documentation PRs may be faster, complex
features may take longer for thorough review.

**Q: Can I work on multiple issues at once?**

A: Yes, but use separate branches for each issue. This keeps PRs focused and
easier to review.

**Q: What if I can't finish a contribution?**

A: No problem! Just comment on the issue letting us know. Someone else may pick
it up, or you can return to it later.

### Setup Questions

**Q: Do I need to use DevContainer?**

A: No, but it's recommended. Local setup works fine if you prefer it.

**Q: What if I don't have Docker?**

A: Follow the [Local Setup](#option-2-local-setup) instructions instead. You'll
need Python 3.10+ and Node.js 20+.

**Q: Can I use GitHub Codespaces?**

A: Yes! Codespaces uses the same DevContainer configuration. Just click "Code" →
"Create codespace on main".

### Contribution Questions

**Q: How do I find good first issues?**

A: Use the `good first issue` label:

```bash
gh issue list --label "good first issue"
```

**Q: Can I suggest new features?**

A: Absolutely! Create an issue with the `enhancement` label describing your
idea.

**Q: What if my PR gets rejected?**

A: Don't be discouraged! Reviewers will explain why and may suggest
alternatives. Learn from the feedback and try again.

### Testing Questions

**Q: Do I need to write tests for documentation changes?**

A: No, tests are not required for pure documentation changes. But you should
verify all links work.

**Q: What coverage percentage should I aim for?**

A: Minimum 70% for CI to pass, but aim for 80%+ for core functionality.

**Q: How do I mock external APIs in tests?**

A: Use pytest fixtures with mocked responses. See `tests/conftest.py` for
examples:

```python
def test_api_call(mock_requests_session):
    # mock_requests_session is a fixture
    result = call_api()
    assert result.status_code == 200
```

### Workflow Questions

**Q: How do I pin an action to a SHA?**

A:

```bash
# Find the SHA for a release tag
gh api /repos/actions/checkout/git/ref/tags/v4 --jq '.object.sha'

# Use in workflow
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4
```

**Q: When should I create a reusable workflow?**

A: When the same logic is used in 3+ workflows, or when you want to standardize
a pattern across the organization.

**Q: Can I use third-party actions?**

A: Yes, but they must be pinned to SHAs and reviewed for security. Prefer
official actions when possible.

______________________________________________________________________

## Getting Help

### Resources

**Documentation**:

- [Contributing Guidelines](../governance/CONTRIBUTING.md)
- [Testing Best Practices](testing-best-practices.md)
- [Monitoring Guide](monitoring.md)
- [Copilot Quick Start](COPILOT_QUICK_START.md)

**Reference**:

- [Agent Registry](../reference/AGENT_REGISTRY.md) - Catalog of all agents
- [Documentation Index](../INDEX.md) - Complete documentation list
- [Cleanup Roadmap](../archive/CLEANUP_ROADMAP.md) - Project status

### Community

**GitHub Discussions**:

- [Ask Questions](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions)<!-- link:github.org_discussions -->
  \- Get help from the community
- [Ideas](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions/categories/ideas)
  \- Share suggestions
- [Show and Tell](https://github.com/orgs/%7B%7BORG_NAME%7D%7D/discussions/categories/show-and-tell)
  \- Share your work

**GitHub Issues**:

- [Report Bugs](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues/new?template=bug_report.yml)<!-- link:github.bug_report -->
- [Request Features](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues/new?template=feature_request.yml)<!-- link:github.feature_request -->
- [Improve Docs](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues/new?template=documentation.yml)

### Direct Support

**When to reach out directly**:

- Security vulnerabilities (use private reporting)
- Sensitive issues
- Urgent production problems

**How to reach us**:

- Email: \[Organizational contact email\]
- Slack: \[If applicable\]
- Maintainers: Check [CODEOWNERS](../../.github/CODEOWNERS)

______________________________________________________________________

## Next Steps

Now that you've read this guide:

1. ✅ **Set up your environment** - DevContainer or local
1. ✅ **Find an issue to work on** - Start with `good first issue`
1. ✅ **Make your first contribution** - Follow the workflow above
1. ✅ **Join the community** - Introduce yourself in Discussions

### Recommended Reading Order

**For new contributors**:

1. This guide (you're here!)
1. [Contributing Guidelines](../governance/CONTRIBUTING.md)
1. [Testing Best Practices](testing-best-practices.md)

**For AI framework contributors**:

1. [Agent Architecture Guide](AGENT_ARCHITECTURE_GUIDE.md)
1. [Agent Registry](../reference/AGENT_REGISTRY.md)
1. [Copilot Quick Start](COPILOT_QUICK_START.md)

**For workflow developers**:

1. [Monitoring Guide](monitoring.md)
1. [Workflow Optimization Analysis](../workflows/COMPREHENSIVE_WORKFLOW_OPTIMIZATION_ANALYSIS.md)

______________________________________________________________________

## Thank You

We appreciate your interest in contributing! Every contribution, no matter how
small, helps improve our organization's shared infrastructure.

**Questions about this guide?** Open an issue with the `documentation` label.

**Ready to contribute?** Find a `good first issue` and get started!

______________________________________________________________________

_Last Updated: 2026-01-14_ _Maintained by: Documentation Team_ _Contributors:
\[Your name here after your first PR!\]_
