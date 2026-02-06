# Quick Start Guide

Get up and running with the {{ORG_NAME}} GitHub template in minutes.

______________________________________________________________________

## Prerequisites

Before you begin, ensure you have:

| Requirement         | Version   | Notes                   |
| ------------------- | --------- | ----------------------- |
| GitHub Organization | -         | Admin access required   |
| Python              | >= 3.9    | 3.12 recommended        |
| Node.js             | >= 20.0.0 | For version scripts     |
| Git                 | >= 2.30   | With SSH key configured |

### Optional Tools

- **pre-commit**: For local quality checks
- **GitHub CLI (`gh`)**: For workflow management
- **Docker**: For containerized development

______________________________________________________________________

## Installation

### Step 1: Fork or Clone the Repository

```bash
# Option A: Fork via GitHub UI, then clone your fork
git clone git@github.com:{{ORG_NAME}}/.github.git
cd .github

# Option B: Use as template (recommended for new organizations)
gh repo create {{ORG_NAME}}/.github --template {{ORG_NAME}}/.github --public
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies (includes dev tools)
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify installation
python -c "import yaml; print('PyYAML OK')"
pre-commit --version
```

### Step 3: Configure Repository Variables

Set up required repository variables in GitHub Settings > Secrets and variables
\> Actions > Variables:

| Variable                 | Default | Description                      |
| ------------------------ | ------- | -------------------------------- |
| `PYTHON_VERSION_DEFAULT` | `3.12`  | Python version for workflows     |
| `NODE_VERSION_DEFAULT`   | `20`    | Node.js version for workflows    |
| `COVERAGE_THRESHOLD`     | `58`    | Minimum test coverage percentage |

### Step 4: Configure Repository Secrets

Add required secrets in GitHub Settings > Secrets and variables > Actions >
Secrets:

| Secret              | Required | Description                      |
| ------------------- | -------- | -------------------------------- |
| `GITHUB_TOKEN`      | Auto     | Automatically provided by GitHub |
| `CODECOV_TOKEN`     | Optional | For coverage reporting           |
| `SLACK_WEBHOOK_URL` | Optional | For Slack notifications          |

______________________________________________________________________

## Basic Configuration

### Update Template Variables

Replace placeholder variables throughout the repository:

```bash
# Find all template variables
grep -r "{{ORG_NAME}}" . --include="*.md" --include="*.yml"
grep -r "{{ORG_NAME}}" . --include="*.md" --include="*.yml"

# Replace with your organization name
find . -type f \( -name "*.md" -o -name "*.yml" \) \
  -exec sed -i '' 's/{{ORG_NAME}}/your-org-name/g' {} \;
find . -type f \( -name "*.md" -o -name "*.yml" \) \
  -exec sed -i '' 's/{{ORG_NAME}}/Your Organization/g' {} \;
```

### Verify Configuration

```bash
# Run pre-commit to check for issues
pre-commit run --all-files

# Run tests to verify setup
python -m pytest tests/ -v --tb=short
```

______________________________________________________________________

## First Workflow Run

### Trigger the CI Workflow

1. Make a small change to any file
1. Commit and push:

```bash
git add .
git commit -m "chore: initial configuration"
git push origin main
```

3. Navigate to **Actions** tab in GitHub to see the workflow run

### Manual Workflow Dispatch

Many workflows support manual triggering:

```bash
# List available workflows
gh workflow list

# Run a specific workflow
gh workflow run ci.yml

# Run with inputs
gh workflow run manual-reset.yml -f scope=all
```

______________________________________________________________________

## Verification Checklist

Confirm your setup is complete:

- [ ] Repository cloned/forked successfully
- [ ] Python dependencies installed
- [ ] Pre-commit hooks installed
- [ ] Repository variables configured
- [ ] First CI workflow passed
- [ ] Template variables replaced

______________________________________________________________________

## Next Steps

- **[Configuration Guide](CONFIGURATION.md)** - Detailed configuration options
- **[Customization Guide](CUSTOMIZATION.md)** - How to customize for your org
- **[Workflow Guide](../guides/WORKFLOWS.md)** - Understanding workflows
- **[Architecture Overview](../architecture/OVERVIEW.md)** - System design

______________________________________________________________________

## Troubleshooting

### Pre-commit Fails

```bash
# Clear cache and reinstall
pre-commit clean
pre-commit install
pre-commit run --all-files
```

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -e ".[dev]" --force-reinstall
```

### Workflow Permissions Error

Ensure your repository has:

- **Settings > Actions > General > Workflow permissions**: Read and write
  permissions
- **Allow GitHub Actions to create and approve pull requests**: Enabled

______________________________________________________________________

## Support

- **[Discussions](https://github.com/%7B%7BORG_NAME%7D%7D/.github/discussions)**
  \- Ask questions
- **[Issues](https://github.com/%7B%7BORG_NAME%7D%7D/.github/issues)** - Report
  bugs
- **[Support Guide](../governance/SUPPORT.md)** - Full support options
