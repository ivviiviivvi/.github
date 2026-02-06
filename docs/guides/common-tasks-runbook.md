# Common Tasks Runbook

> **Quick reference for frequently performed tasks in the ivviiviivvi/.github
> repository**

This runbook provides step-by-step instructions for common maintenance and
development tasks. Use this as a quick reference guide.

______________________________________________________________________

## Table of Contents

- [Repository Management](#repository-management)
- [Workflow Operations](#workflow-operations)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Documentation Maintenance](#documentation-maintenance)
- [Monitoring & Troubleshooting](#monitoring--troubleshooting)
- [Security Tasks](#security-tasks)
- [AI Framework Management](#ai-framework-management)
- [Emergency Procedures](#emergency-procedures)

______________________________________________________________________

## Repository Management

### Task: Clone and Set Up Repository

**When**: Setting up new development environment

**Steps**:

```bash
# 1. Fork and clone
gh repo fork ivviiviivvi/.github --clone

# 2. Navigate to directory
cd .github

# 3. Set up pre-commit hooks
pip install pre-commit
pre-commit install

# 4. Verify setup
pytest tests/ -v
```

**Expected Result**: All tests pass, pre-commit hooks installed

### Task: Sync Fork with Upstream

**When**: Your fork is behind the main repository

**Steps**:

```bash
# 1. Add upstream remote (one-time)
git remote add upstream https://github.com/ivviiviivvi/.github.git

# 2. Fetch upstream changes
git fetch upstream

# 3. Merge upstream/main into your main
git checkout main
git merge upstream/main

# 4. Push updates to your fork
git push origin main
```

**Expected Result**: Your fork is up to date with upstream

### Task: Clean Up Old Branches

**When**: After PRs are merged or abandoned

**Steps**:

```bash
# 1. List local branches
git branch -a

# 2. Delete local branch
git branch -d feature/old-branch

# 3. Delete remote branch
git push origin --delete feature/old-branch

# 4. Prune remote tracking branches
git fetch --prune
```

**Expected Result**: Old branches removed locally and remotely

### Task: Resolve Merge Conflicts

**When**: Git shows merge conflict during pull/merge

**Steps**:

```bash
# 1. See conflicting files
git status

# 2. Open conflicting files and resolve
# Look for <<<<<<< HEAD markers
# Choose correct version or combine both
# Remove conflict markers

# 3. Stage resolved files
git add path/to/resolved/file

# 4. Continue merge/rebase
git merge --continue
# or
git rebase --continue

# 5. Push changes
git push origin your-branch
```

**Expected Result**: Conflicts resolved, clean merge/rebase

______________________________________________________________________

## Workflow Operations

### Task: Add a New Workflow

**When**: Creating new automation

**Steps**:

```bash
# 1. Create workflow file
touch .github/workflows/my-workflow.yml

# 2. Add workflow content (see template below)
# Use editor or copy from existing workflow

# 3. Validate syntax
actionlint .github/workflows/my-workflow.yml

# 4. Commit and push
git add .github/workflows/my-workflow.yml
git commit -m "feat(ci): add my-workflow"
git push origin feature/my-workflow

# 5. Test with manual trigger
gh workflow run my-workflow.yml --ref feature/my-workflow

# 6. Check logs
gh run list --workflow my-workflow.yml --limit 1
gh run view <run-id> --log
```

**Workflow Template**:

```yaml
name: My Workflow

on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - "relevant/path/**"

permissions:
  contents: read

jobs:
  my-job:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4

      - name: Run task
        run: echo "Task complete"
```

**Expected Result**: Workflow runs successfully

### Task: Pin Action to SHA

**When**: Adding or updating actions in workflows

**Steps**:

```bash
# 1. Find the release tag SHA
gh api /repos/actions/checkout/git/ref/tags/v4 --jq '.object.sha'

# Output: 11bd71901bbe5b1630ceea73d27597364c9af683

# 2. Update workflow file
# Change: uses: actions/checkout@v4
# To: uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4

# 3. Commit change
git add .github/workflows/workflow-name.yml
git commit -m "chore(ci): pin checkout action to SHA"
git push
```

**Expected Result**: Action pinned to specific commit

### Task: Disable a Failing Workflow

**When**: Workflow is broken and blocking other work

**Steps**:

```bash
# 1. List workflows
gh workflow list

# 2. Disable workflow
gh workflow disable my-workflow.yml

# 3. Verify disabled
gh workflow list  # Check status column

# 4. Fix the workflow
# ... make necessary changes ...

# 5. Re-enable workflow
gh workflow enable my-workflow.yml
```

**Expected Result**: Workflow disabled until fixed

### Task: Check Workflow Usage/Minutes

**When**: Monitoring quota consumption

**Steps**:

```bash
# 1. View usage report
cat .github/reports/usage/latest-usage.json | jq .

# 2. Trigger usage monitoring workflow
gh workflow run usage-monitoring.yml

# 3. Check specific workflow consumption
gh api /repos/ivviiviivvi/.github/actions/workflows -q '.workflows[] | {name, path}' | \
  while read -r workflow; do
    echo "=== $workflow ==="
    gh api "/repos/ivviiviivvi/.github/actions/workflows/$(basename $workflow)/timing" --jq '.billable.UBUNTU.total_ms'
  done

# 4. View monthly summary
gh api /repos/ivviiviivvi/.github/actions/billing/usage
```

**Expected Result**: Usage statistics displayed

______________________________________________________________________

## Testing & Quality Assurance

### Task: Run All Tests

**When**: Before committing changes

**Steps**:

```bash
# 1. Run full test suite
pytest tests/ -v

# 2. With coverage report
pytest tests/ --cov --cov-report=term-missing

# 3. Generate HTML coverage report
pytest tests/ --cov --cov-report=html
open htmlcov/index.html  # View in browser
```

**Expected Result**: All tests pass, coverage ≥70%

### Task: Run Specific Test Category

**When**: Testing specific functionality

**Steps**:

```bash
# Unit tests only
pytest -m unit -v

# Integration tests only
pytest -m integration -v

# Security tests only
pytest -m security -v

# Specific test file
pytest tests/unit/test_web_crawler.py -v

# Specific test function
pytest tests/unit/test_web_crawler.py::TestSSRFProtection::test_blocks_localhost -v
```

**Expected Result**: Selected tests pass

### Task: Add Tests for New Code

**When**: Adding new Python scripts or functions

**Steps**:

```bash
# 1. Create test file
# If adding to automation/scripts/my_feature.py
# Create tests/unit/test_my_feature.py

# 2. Write tests (template below)
# Use pytest conventions

# 3. Run new tests
pytest tests/unit/test_my_feature.py -v

# 4. Check coverage
pytest tests/unit/test_my_feature.py --cov=automation/scripts/my_feature --cov-report=term-missing
```

**Test Template**:

```python
"""Tests for my_feature module."""
import pytest
from automation.scripts.my_feature import my_function


class TestMyFunction:
    """Test suite for my_function."""

    def test_basic_case(self):
        """Test basic functionality."""
        result = my_function("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            my_function("")
```

**Expected Result**: Tests pass with good coverage

### Task: Fix Pre-commit Hook Failures

**When**: `git commit` fails with hook errors

**Steps**:

```bash
# 1. Run pre-commit on all files
pre-commit run --all-files

# 2. Check what failed
# Look for FAILED or error messages

# 3. Auto-fix formatting issues
black automation/scripts/
# or
mdformat docs/

# 4. Fix linting issues manually
# Edit files based on error messages

# 5. Stage fixes
git add -A

# 6. Try commit again
git commit -m "your message"

# If still failing, check specific error
# Common issues:
# - Trailing whitespace: remove it
# - Missing newline at end of file: add it
# - Syntax errors: fix code
```

**Expected Result**: Pre-commit hooks pass

______________________________________________________________________

## Documentation Maintenance

### Task: Add New Documentation File

**When**: Creating new guide or reference

**Steps**:

```bash
# 1. Create file in appropriate directory
# guides/ for tutorials
# main docs/ for reference
touch docs/guides/my-new-guide.md

# 2. Add front matter and content
# Follow markdown standards (see NEW_CONTRIBUTOR_GUIDE.md)

# 3. Add to documentation index
# Edit docs/INDEX.md to include new doc

# 4. Verify links work
# Click through all links in new document

# 5. Commit
git add docs/guides/my-new-guide.md docs/INDEX.md
git commit -m "docs: add new guide for X"
git push
```

**Expected Result**: Documentation accessible and indexed

### Task: Fix Broken Links

**When**: Link checker reports broken links

**Steps**:

```bash
# 1. Run link checker
python3 automation/scripts/web_crawler.py docs/ --output project_meta/reports/link-check.md

# 2. Review report
cat project_meta/reports/link-check.md

# 3. Fix broken links
# Edit files to correct URLs
# Remove or replace dead links

# 4. Re-run link checker to verify
python3 automation/scripts/web_crawler.py docs/ --output project_meta/reports/link-check-verification.md

# 5. Commit fixes
git add -A
git commit -m "docs: fix broken links"
git push
```

**Expected Result**: No broken links remain

### Task: Update Documentation Index

**When**: New docs added or structure changed

**Steps**:

```bash
# 1. Open docs/INDEX.md
code docs/INDEX.md

# 2. Add new entries following pattern:
# ### Category Name
# - [Document Title](relative/path.md) - Brief description

# 3. Organize by category:
# - Setup Guides
# - User Guides
# - Reference
# - Architecture

# 4. Ensure all docs are listed
find docs/ -name "*.md" -type f | sort

# 5. Commit update
git add docs/INDEX.md
git commit -m "docs: update documentation index"
git push
```

**Expected Result**: All docs accessible via index

______________________________________________________________________

## Monitoring & Troubleshooting

### Task: Check Workflow Health

**When**: Regular monitoring or investigating issues

**Steps**:

```bash
# 1. View recent workflow runs
gh run list --limit 20

# 2. Check failure rate
gh run list --status failure --limit 10

# 3. View metrics
cat metrics/baseline-metrics.json | jq .

# 4. Check specific workflow
gh run list --workflow test-coverage.yml --limit 5

# 5. View workflow logs
gh run view <run-id> --log
```

**Expected Result**: Identify any issues

### Task: Investigate Workflow Failure

**When**: Workflow fails unexpectedly

**Steps**:

```bash
# 1. Find failed run
gh run list --workflow <workflow-name> --status failure --limit 1

# 2. View detailed logs
gh run view <run-id> --log-failed

# 3. Check for common issues:
# - Rate limiting: Wait and retry
# - Flaky tests: Re-run workflow
# - Dependency issues: Check version pins
# - Permission errors: Check workflow permissions

# 4. Re-run workflow
gh run rerun <run-id>

# 5. If persistent, disable and fix
gh workflow disable <workflow-name>
# Fix issue
gh workflow enable <workflow-name>
```

**Expected Result**: Failure cause identified and resolved

### Task: View Dashboard and Metrics

**When**: Checking project health

**Steps**:

```bash
# 1. Trigger dashboard generation
gh workflow run metrics-dashboard.yml

# 2. Wait for completion
gh run watch

# 3. Download dashboard
gh run download $(gh run list -w metrics-dashboard.yml --limit 1 --json databaseId -q '.[0].databaseId')

# 4. Open dashboard
open metrics-dashboard.html

# Or view metrics directly
cat metrics/baseline-metrics.json | jq '.'
```

**Expected Result**: Dashboard shows current metrics

### Task: Respond to Alert

**When**: Alert appears in GitHub Discussion #1

**Steps**:

```bash
# 1. Read alert details
# Check Discussion #1 for alert post

# 2. Identify alert type:
# - Workflow Failure → See "Investigate Workflow Failure" above
# - High Usage → See "Check Workflow Usage" above
# - Coverage Drop → Run coverage report
# - Security Finding → Review security scan

# 3. Follow appropriate runbook
# See docs/guides/monitoring.md for detailed runbooks

# 4. Document resolution
# Comment on Discussion with what was done

# 5. Update metrics
gh workflow run metrics-collection.yml
```

**Expected Result**: Alert resolved and documented

______________________________________________________________________

## Security Tasks

### Task: Update Pinned Actions

**When**: Security advisory or quarterly review

**Steps**:

```bash
# 1. List all workflows
find .github/workflows -name "*.yml"

# 2. Check for outdated action versions
# Look for comments like # v3 when v4 is available

# 3. Find new SHA for action
gh api /repos/<owner>/<action>/git/ref/tags/<new-tag> --jq '.object.sha'

# 4. Update workflow files
# Replace old SHA with new SHA

# 5. Test updated workflows
gh workflow run <workflow-name>

# 6. Commit updates
git add .github/workflows/
git commit -m "chore(security): update pinned actions"
git push
```

**Expected Result**: All actions up to date with SHAs

### Task: Scan for Secrets

**When**: Before committing or regular audit

**Steps**:

```bash
# 1. Run detect-secrets scan
detect-secrets scan --all-files

# 2. Review findings
# Check if any are real secrets (not test data)

# 3. If secrets found:
# - Remove from code
# - Add to .gitignore
# - Rotate the secret
# - Add to .secrets.baseline if false positive

# 4. Commit clean code
git add -A
git commit -m "chore(security): remove secrets"
git push
```

**Expected Result**: No secrets in codebase

### Task: Review Security Scan Results

**When**: After security workflow runs

**Steps**:

```bash
# 1. View security workflow runs
gh run list --workflow safeguard-5-secret-scanning.yml --limit 5

# 2. Check for failures
gh run view <run-id> --log

# 3. Review findings in metrics
cat metrics/baseline-metrics.json | jq '.security'

# 4. For each finding:
# - Assess severity
# - Plan remediation
# - Create issue if needed

# 5. Track remediation
gh issue create --title "Security: Fix X" --label security
```

**Expected Result**: Security issues tracked and resolved

______________________________________________________________________

## AI Framework Management

### Task: Add New Agent

**When**: Creating specialized AI assistant

**Steps**:

```bash
# 1. Create agent file
touch ai_framework/agents/my-agent.agent.md

# 2. Add agent definition (template below)
# Follow existing agent formats

# 3. Update agent registry
# Add entry to docs/AGENT_REGISTRY.md

# 4. Test agent
# Use in GitHub Copilot or relevant tool

# 5. Commit
git add ai_framework/agents/my-agent.agent.md docs/AGENT_REGISTRY.md
git commit -m "feat(ai): add my-agent for X tasks"
git push
```

**Agent Template**:

```markdown
---
name: MyAgent
description: Brief description of what this agent does
tools:
  - github/*
  - shell
model: claude-sonnet-4.5
---

# Agent Implementation

This agent specializes in X tasks.

## Capabilities

- Capability 1
- Capability 2

## Usage

Invoke with: @my-agent <your request>
```

**Expected Result**: New agent available for use

### Task: Update Copilot Instructions

**When**: Coding standards change

**Steps**:

```bash
# 1. Navigate to instructions
cd ai_framework/copilot-instructions

# 2. Edit relevant instruction file
# e.g., python.instructions.md

# 3. Verify YAML frontmatter is valid
# Check: description and applyTo fields

# 4. Test with Copilot
# Open a file matching the pattern
# Verify Copilot follows new instructions

# 5. Commit
git add ai_framework/copilot-instructions/
git commit -m "docs(ai): update Python coding standards"
git push
```

**Expected Result**: Copilot uses updated instructions

______________________________________________________________________

## Emergency Procedures

### Task: Emergency Workflow Disable

**When**: Critical workflow causing issues

**Steps**:

```bash
# 1. Immediately disable workflow
gh workflow disable <critical-workflow>.yml

# 2. Notify team
# Post in Discussion #1 or relevant channel

# 3. Investigate issue (offline)
# Review logs, code, recent changes

# 4. Create hotfix branch
git checkout -b hotfix/critical-workflow-fix

# 5. Fix and test thoroughly
# Verify fix resolves issue

# 6. Emergency merge (if critical)
# Follow organization emergency procedures

# 7. Re-enable workflow
gh workflow enable <critical-workflow>.yml

# 8. Monitor closely
gh run watch
```

**Expected Result**: Issue resolved, service restored

### Task: Rollback Recent Changes

**When**: Recent deploy caused issues

**Steps**:

```bash
# 1. Identify problematic commit
git log --oneline -20

# 2. Create revert
git revert <commit-sha>

# 3. Or revert to previous version
git checkout -b hotfix/rollback
git reset --hard <good-commit-sha>
git push --force-with-lease origin hotfix/rollback

# 4. Create emergency PR
gh pr create --title "HOTFIX: Rollback to working state" \
  --body "Emergency rollback due to X issue"

# 5. Monitor deployment
gh run watch
```

**Expected Result**: Stable version restored

### Task: Emergency Contact Escalation

**When**: Critical issue beyond your expertise

**Steps**:

```bash
# 1. Document the issue
# Create detailed issue with:
# - What happened
# - When it started
# - What you've tried
# - Current impact

# 2. Tag maintainers
# In issue or Discussion, tag relevant maintainers

# 3. Escalate via appropriate channel
# - GitHub Discussion for visibility
# - Email for urgent matters
# - Slack/Teams if available

# 4. Provide all context
# - Logs
# - Error messages
# - Recent changes
# - Attempted fixes

# 5. Stay available
# Be ready to provide more information
```

**Expected Result**: Issue escalated to appropriate team

______________________________________________________________________

## Quick Reference

### Most Common Commands

```bash
# Run tests
pytest tests/ -v

# Check status
git status
gh run list --limit 5

# Fix formatting
black automation/scripts/
mdformat docs/

# View metrics
cat metrics/baseline-metrics.json | jq .

# Trigger workflow
gh workflow run <workflow-name>

# View logs
gh run view <run-id> --log

# Create PR
gh pr create --fill
```

### Useful Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias gst='git status'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gp='git push'
alias gpu='git pull'
alias gcm='git commit -m'
alias pytest-cov='pytest --cov --cov-report=term-missing'
alias ghrun='gh run list --limit 5'
alias ghwatch='gh run watch'
```

______________________________________________________________________

## Additional Resources

- [New Contributor Guide](NEW_CONTRIBUTOR_GUIDE.md) - Getting started
- [Monitoring Guide](monitoring.md) - Detailed monitoring runbooks
- [Testing Best Practices](testing-best-practices.md) - Testing standards
- [Contributing Guidelines](../governance/CONTRIBUTING.md) - Contribution
  process

______________________________________________________________________

**Need help?** Check
[NEW_CONTRIBUTOR_GUIDE.md#getting-help](NEW_CONTRIBUTOR_GUIDE.md#getting-help)
or ask in GitHub Discussions.

______________________________________________________________________

_Last Updated: 2026-01-14_ _Maintained by: Documentation Team_
