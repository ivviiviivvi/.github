# Configuration Guide

Complete reference for configuring the {{ORG_NAME}} GitHub template.

______________________________________________________________________

## Template Variables

The following template variables are used throughout the repository. Replace
them with your organization-specific values.

### Core Variables

| Variable       | Description              | Example           |
| -------------- | ------------------------ | ----------------- |
| `{{ORG_NAME}}` | GitHub organization slug | `my-company`      |
| `{{ORG_NAME}}` | Human-readable org name  | `My Company Inc.` |

### Replacement Script

```bash
#!/usr/bin/env bash
set -euo pipefail

ORG_NAME="your-org-name"
ORG_DISPLAY="Your Organization Name"

# Replace in all relevant files
find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) \
  ! -path "./.git/*" \
  -exec sed -i '' "s/{{ORG_NAME}}/${ORG_NAME}/g" {} \;

find . -type f \( -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) \
  ! -path "./.git/*" \
  -exec sed -i '' "s/{{ORG_NAME}}/${ORG_DISPLAY}/g" {} \;

echo "Template variables replaced successfully"
```

______________________________________________________________________

## Repository Settings

### Required Settings

Configure these in GitHub Repository Settings:

#### General Settings

| Setting        | Value                         | Location           |
| -------------- | ----------------------------- | ------------------ |
| Default branch | `main`                        | Settings > General |
| Features       | Issues, Projects, Discussions | Settings > General |
| Merge button   | Squash, Rebase                | Settings > General |

#### Branch Protection (main)

| Rule                              | Value                      |
| --------------------------------- | -------------------------- |
| Require pull request reviews      | 1 reviewer minimum         |
| Require status checks             | `lint`, `test`, `security` |
| Require branches to be up to date | Enabled                    |
| Include administrators            | Optional                   |

#### Actions Settings

| Setting                            | Value             | Location                     |
| ---------------------------------- | ----------------- | ---------------------------- |
| Actions permissions                | Allow all actions | Settings > Actions > General |
| Workflow permissions               | Read and write    | Settings > Actions > General |
| Allow GitHub Actions to create PRs | Enabled           | Settings > Actions > General |

______________________________________________________________________

## Secret Setup

### Required Secrets

Configure in **Settings > Secrets and variables > Actions > Secrets**:

| Secret         | Required | Description           | How to Obtain                      |
| -------------- | -------- | --------------------- | ---------------------------------- |
| `GITHUB_TOKEN` | Auto     | Automatic token       | Provided by GitHub                 |
| `PAT_TOKEN`    | Optional | Personal Access Token | User Settings > Developer settings |

### Optional Secrets

| Secret              | Purpose                    | Documentation                                                        |
| ------------------- | -------------------------- | -------------------------------------------------------------------- |
| `CODECOV_TOKEN`     | Coverage reporting         | [Codecov Docs](https://docs.codecov.com/)                            |
| `SLACK_WEBHOOK_URL` | Slack notifications        | [Slack API](https://api.slack.com/messaging/webhooks)                |
| `SLACK_BOT_TOKEN`   | Advanced Slack integration | [Slack Bot Tokens](https://api.slack.com/authentication/token-types) |
| `SONAR_TOKEN`       | SonarCloud analysis        | [SonarCloud Docs](https://docs.sonarcloud.io/)                       |

### Secret Scopes

```
Organization secrets:  Shared across all org repos
Repository secrets:    Specific to this repo only
Environment secrets:   Scoped to deployment environments
```

______________________________________________________________________

## Variable Configuration

### Repository Variables

Configure in **Settings > Secrets and variables > Actions > Variables**:

#### Version Management

| Variable                 | Default | Description                  |
| ------------------------ | ------- | ---------------------------- |
| `PYTHON_VERSION_DEFAULT` | `3.12`  | Default Python version       |
| `NODE_VERSION_DEFAULT`   | `20`    | Default Node.js version      |
| `GO_VERSION_DEFAULT`     | `1.21`  | Default Go version (if used) |

#### Quality Thresholds

| Variable               | Default | Description                 |
| ---------------------- | ------- | --------------------------- |
| `COVERAGE_THRESHOLD`   | `58`    | Minimum coverage percentage |
| `COMPLEXITY_THRESHOLD` | `10`    | Max cyclomatic complexity   |

#### Feature Flags

| Variable                     | Default | Description                      |
| ---------------------------- | ------- | -------------------------------- |
| `ENABLE_SLACK_NOTIFICATIONS` | `false` | Enable Slack integration         |
| `ENABLE_AUTO_MERGE`          | `true`  | Enable auto-merge for Dependabot |
| `ENABLE_STALE_MANAGEMENT`    | `true`  | Enable stale issue/PR management |

### Using Variables in Workflows

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          # Uses repository variable with fallback
          python-version: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}
```

______________________________________________________________________

## Environment Configuration

### Creating Environments

1. Navigate to **Settings > Environments**
1. Click **New environment**
1. Configure protection rules and secrets

### Recommended Environments

| Environment   | Purpose                | Protection Rules               |
| ------------- | ---------------------- | ------------------------------ |
| `development` | Dev deployments        | None                           |
| `staging`     | Pre-production testing | Required reviewers             |
| `production`  | Live deployments       | Required reviewers, wait timer |

### Environment-Specific Secrets

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - name: Deploy
        env:
          # Environment secret, not repository secret
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
```

______________________________________________________________________

## Pre-commit Configuration

### Configuration File

The pre-commit configuration is at `.config/pre-commit.yaml` (symlinked to
`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Custom Hooks

Add organization-specific hooks:

```yaml
  - repo: local
    hooks:
      - id: org-custom-check
        name: Organization Custom Check
        entry: python scripts/custom_check.py
        language: python
        types: [python]
```

______________________________________________________________________

## Workflow Defaults

### Centralized Version Management

Workflows reference repository variables for consistency:

```yaml
env:
  PYTHON_VERSION: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}
  NODE_VERSION: ${{ vars.NODE_VERSION_DEFAULT || '20' }}
```

### SHA Pinning

All GitHub Actions are SHA-pinned with ratchet comments:

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4
```

Update pins with:

```bash
python src/automation/scripts/utils/update-action-pins.py --recursive
```

______________________________________________________________________

## File Structure Configuration

### pyproject.toml

Primary Python configuration:

```toml
[project]
name = "org-github-template"
version = "1.0.0"
requires-python = ">=3.9"

[tool.ruff]
line-length = 120
target-version = "py39"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/automation --cov-fail-under=58"

[tool.mypy]
python_version = "3.9"
ignore_missing_imports = true
```

### package.json

Node.js configuration (version scripts):

```json
{
  "name": "org-github-template",
  "version": "1.0.0",
  "scripts": {
    "version:bump:patch": "npm version patch --no-git-tag-version",
    "version:bump:minor": "npm version minor --no-git-tag-version",
    "version:sync": "python scripts/sync_versions.py"
  }
}
```

______________________________________________________________________

## Validation

### Verify Configuration

```bash
# Check pre-commit configuration
pre-commit validate-config

# Verify Python setup
python -c "import yaml, requests, github; print('All imports OK')"

# Test workflow syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"

# Run full validation
pre-commit run --all-files
```

### Common Issues

| Issue                | Solution                               |
| -------------------- | -------------------------------------- |
| `Permission denied`  | Check workflow permissions in Settings |
| `Secret not found`   | Verify secret name and scope           |
| `Variable undefined` | Add fallback value in workflow         |

______________________________________________________________________

## Next Steps

- **[Customization Guide](CUSTOMIZATION.md)** - Customize for your org
- **[Workflow Guide](../guides/WORKFLOWS.md)** - Understanding workflows
- **[Architecture Overview](../architecture/OVERVIEW.md)** - System design
