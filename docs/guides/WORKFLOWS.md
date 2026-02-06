# Workflow Guide

Comprehensive guide to GitHub Actions workflows in the {{ORG_NAME}} template.

______________________________________________________________________

## Workflow Categories Overview

The repository contains **130+ workflows** organized into functional categories:

### Core Workflows

Foundation workflows that other workflows depend on.

| Workflow         | Purpose                                 | Trigger              |
| ---------------- | --------------------------------------- | -------------------- |
| `ci.yml`         | Main CI pipeline (lint, test, security) | Push, PR             |
| `release.yml`    | Release automation                      | Tag push, manual     |
| `deployment.yml` | Deployment orchestration                | Push to main, manual |

### Reusable Workflows

Modular workflows called by other workflows (located in
`.github/workflows/reusable/`):

| Workflow                  | Purpose                  | Inputs                          |
| ------------------------- | ------------------------ | ------------------------------- |
| `python-setup-test.yml`   | Python setup and testing | `python-version`, `run-tests`   |
| `nodejs-setup-build.yml`  | Node.js setup and build  | `node-version`, `cache`         |
| `security-scanning.yml`   | Security analysis        | `scan-type`, `fail-on-severity` |
| `docker-build-push.yml`   | Docker image build/push  | `image-name`, `push`            |
| `artifact-management.yml` | Artifact handling        | `artifact-name`, `retention`    |
| `github-cli-pr-ops.yml`   | PR operations via CLI    | `operation`, `pr-number`        |

### PR Automation

Workflows that automate pull request lifecycle:

| Workflow                | Purpose                       | Trigger           |
| ----------------------- | ----------------------------- | ----------------- |
| `auto-labeler.yml`      | Auto-label PRs based on paths | PR opened         |
| `pr-title-lint.yml`     | Validate PR title format      | PR opened, edited |
| `auto-assign.yml`       | Auto-assign reviewers         | PR opened         |
| `pr-quality-checks.yml` | Quality gates for PRs         | PR sync           |
| `combine-prs.yml`       | Batch Dependabot PRs          | Schedule, manual  |
| `auto-merge.yml`        | Auto-merge approved PRs       | PR approved       |

### Issue Management

Workflows for issue lifecycle:

| Workflow               | Purpose                     | Trigger         |
| ---------------------- | --------------------------- | --------------- |
| `issue-triage.yml`     | Triage and label new issues | Issue opened    |
| `stale-management.yml` | Mark/close stale issues     | Schedule        |
| `welcome.yml`          | Welcome new contributors    | Issue/PR opened |

### Security & Compliance

Security-focused workflows:

| Workflow                | Purpose                         | Trigger            |
| ----------------------- | ------------------------------- | ------------------ |
| `security-scan.yml`     | Security vulnerability scanning | Push, PR, schedule |
| `dependency-review.yml` | Review dependency changes       | PR                 |
| `scan-for-secrets.yml`  | Detect leaked secrets           | Push, PR           |
| `sbom-generation.yml`   | Generate SBOM                   | Release, manual    |
| `semgrep.yml`           | Static analysis                 | Push, PR           |

### Reporting & Metrics

Analytics and reporting:

| Workflow                   | Purpose                      | Trigger  |
| -------------------------- | ---------------------------- | -------- |
| `metrics-collection.yml`   | Collect repository metrics   | Schedule |
| `repo-metrics.yml`         | Repository statistics        | Schedule |
| `workflow-metrics.yml`     | Workflow performance metrics | Schedule |
| `weekly-commit-report.yml` | Weekly activity report       | Schedule |

### AI/LLM Integration

AI-assisted automation:

| Workflow                 | Purpose                | Trigger      |
| ------------------------ | ---------------------- | ------------ |
| `claude.yml`             | Claude AI integration  | PR, manual   |
| `claude-code-review.yml` | AI-powered code review | PR           |
| `gemini-triage.yml`      | Gemini issue triage    | Issue opened |
| `jules.yml`              | Jules agent automation | Manual       |

______________________________________________________________________

## Common Patterns

### Workflow Structure

Standard workflow anatomy:

```yaml
name: Workflow Name

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      option:
        description: 'Optional input'
        required: false
        default: 'value'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  pull-requests: write

env:
  PYTHON_VERSION: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}

jobs:
  job-name:
    name: Display Name
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4

      - name: Setup
        run: echo "Setup step"

      - name: Main logic
        run: echo "Main logic"
```

### SHA Pinning Pattern

All actions are SHA-pinned with ratchet comments for security:

```yaml
# Format: action@SHA  # ratchet:action@version
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # ratchet:actions/checkout@v4
uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065  # ratchet:actions/setup-python@v5
```

Update pins:

```bash
python src/automation/scripts/utils/update-action-pins.py --recursive
```

### Variable Fallback Pattern

Use repository variables with fallbacks:

```yaml
env:
  PYTHON_VERSION: ${{ vars.PYTHON_VERSION_DEFAULT || '3.12' }}
  NODE_VERSION: ${{ vars.NODE_VERSION_DEFAULT || '20' }}
```

### Conditional Execution

```yaml
steps:
  - name: Run only on main
    if: github.ref == 'refs/heads/main'
    run: echo "On main branch"

  - name: Run only on PR
    if: github.event_name == 'pull_request'
    run: echo "On pull request"

  - name: Run on success only
    if: success()
    run: echo "Previous steps succeeded"
```

### Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building"

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing"

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying"
```

### Matrix Strategy

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

______________________________________________________________________

## Calling Reusable Workflows

### Basic Usage

```yaml
jobs:
  python-test:
    uses: ./.github/workflows/reusable/python-setup-test.yml
    with:
      python-version: '3.12'
      run-tests: true
```

### With Secrets

```yaml
jobs:
  security:
    uses: ./.github/workflows/reusable/security-scanning.yml
    secrets: inherit  # Pass all secrets
    # Or specific secrets:
    # secrets:
    #   SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Chaining Reusable Workflows

```yaml
jobs:
  setup:
    uses: ./.github/workflows/reusable/python-setup-test.yml
    with:
      run-tests: false

  security:
    needs: setup
    uses: ./.github/workflows/reusable/security-scanning.yml

  deploy:
    needs: [setup, security]
    uses: ./.github/workflows/reusable/docker-build-push.yml
    with:
      push: true
```

______________________________________________________________________

## Troubleshooting

### Common Issues

#### Workflow Not Triggering

**Problem**: Workflow doesn't run on push/PR.

**Solutions**:

1. Check branch/path filters match
1. Verify workflow file is on default branch
1. Check for YAML syntax errors
1. Ensure workflow is enabled in Actions settings

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/my-workflow.yml'))"
```

#### Permission Denied

**Problem**: `Error: Resource not accessible by integration`

**Solutions**:

1. Check `permissions` block in workflow
1. Verify repository Actions settings
1. Use PAT instead of GITHUB_TOKEN for cross-repo operations

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

#### Secret Not Found

**Problem**: `Error: secret not found`

**Solutions**:

1. Verify secret name (case-sensitive)
1. Check secret scope (org vs repo)
1. Ensure environment is specified if using environment secrets

#### Concurrency Issues

**Problem**: Workflows cancel each other unexpectedly.

**Solution**: Use unique concurrency groups:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}-${{ github.event_name }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

#### Action Version Mismatch

**Problem**: Action SHA doesn't match expected version.

**Solution**: Update SHA pins:

```bash
python src/automation/scripts/utils/update-action-pins.py --recursive
```

### Debugging Techniques

#### Enable Debug Logging

Set repository secrets:

- `ACTIONS_RUNNER_DEBUG`: `true`
- `ACTIONS_STEP_DEBUG`: `true`

#### Add Debug Steps

```yaml
- name: Debug info
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    env | sort
```

#### Check Workflow Run Logs

```bash
# List recent runs
gh run list --workflow=ci.yml --limit=5

# View specific run
gh run view <run-id> --log

# Download logs
gh run download <run-id>
```

______________________________________________________________________

## Best Practices

### Performance

1. **Use caching**: Cache dependencies to speed up builds
1. **Minimize checkout depth**: Use `fetch-depth: 1` when full history not
   needed
1. **Cancel redundant runs**: Use concurrency groups
1. **Use matrix sparingly**: Only test combinations that matter

### Security

1. **Pin actions by SHA**: Prevent supply chain attacks
1. **Minimal permissions**: Grant only required permissions
1. **Use secrets appropriately**: Never log secrets
1. **Review third-party actions**: Audit before adoption

### Maintainability

1. **Use reusable workflows**: Reduce duplication
1. **Document workflows**: Add comments and README
1. **Consistent naming**: Follow naming conventions
1. **Test changes**: Use feature branches

______________________________________________________________________

## Workflow Lifecycle

### Adding a New Workflow

1. Create workflow file in `.github/workflows/`
1. Follow naming convention: `<category>-<action>.yml`
1. Add proper triggers, permissions, and concurrency
1. Test on feature branch
1. Document in workflow catalog

### Modifying Existing Workflows

1. Create feature branch
1. Make changes
1. Test via PR (workflows run on PRs)
1. Review logs and fix issues
1. Merge after approval

### Deprecating Workflows

1. Add `(Deprecated)` to workflow name
1. Comment out triggers (keep `workflow_dispatch`)
1. Add deprecation notice to file
1. Move to `workflows/deprecated/` after grace period
1. Delete after confirmation no usage

______________________________________________________________________

## Next Steps

- **[Workflow Catalog](../reference/WORKFLOW_CATALOG.md)** - Complete workflow
  reference
- **[Agents Guide](AGENTS.md)** - AI agent integration
- **[Architecture Overview](../architecture/OVERVIEW.md)** - System design
