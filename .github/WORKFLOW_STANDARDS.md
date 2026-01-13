# GitHub Actions Workflow Standards

## Overview
This document defines the standards for all GitHub Actions workflows in this organization to ensure security, performance, reliability, and maintainability.

## Action Version Standards

### Core Actions (Pinned to SHA)
Use these standardized versions across all workflows:

```yaml
# Checkout
actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

# Setup Actions
actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.3.0
actions/setup-go@41dfa10bad2bb2ae585af6ee5bb4d7d973ad74ed # v5.1.0

# Artifact Management
actions/upload-artifact@b4b15b8c7c6ac21ea08fcf65892d2ee8f75cf882 # v4.5.0
actions/download-artifact@fa0a91b85d4f404e444e00e005971372dc801d16 # v4.1.8

# Caching
actions/cache@1bd1e32a3bdc45362d1e726936510720a7c30a57 # v4.2.0

# GitHub Script
actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1

# CodeQL
github/codeql-action/init@f09c1c0a94de965c15400f5634aa42fac8fb8f88 # v3.27.5
github/codeql-action/autobuild@f09c1c0a94de965c15400f5634aa42fac8fb8f88 # v3.27.5
github/codeql-action/analyze@f09c1c0a94de965c15400f5634aa42fac8fb8f88 # v3.27.5

# Pages
actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b # v5.0.0
actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dda462b719fa # v3.0.1
actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e # v4.0.5

# Docker
docker/setup-buildx-action@c47758b77c9736f4b2ef4073d4d51994fabfe349 # v3.7.1
docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567 # v3.3.0
docker/metadata-action@8e5442c4ef9f78752691e2d8f8d19755c6f78e81 # v5.5.1
docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75 # v6.9.0
```

## Required Workflow Elements

### 1. Permissions (Security)
**ALWAYS** specify minimal permissions at the workflow or job level:

```yaml
permissions:
  contents: read        # Default - read repo contents
  pull-requests: write  # Only if needed
  issues: write         # Only if needed
```

### 2. Concurrency (Performance & Cost)
**ALWAYS** add concurrency controls to prevent redundant runs:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # For PRs and feature branches
  # cancel-in-progress: false # For main/production deployments
```

### 3. Timeouts (Reliability)
**ALWAYS** set timeouts to prevent hanging jobs:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # Adjust based on job needs
```

### 4. Caching (Performance)
**ALWAYS** cache dependencies to speed up workflows:

#### Node.js
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Automatic caching
```

#### Python
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'  # Automatic caching
```

#### Manual Caching
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### 5. Path Filters (Cost Reduction)
Use path filters to avoid unnecessary runs:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package*.json'
  pull_request:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package*.json'
```

## Best Practices

### Security
1. ✅ Pin all actions to commit SHAs (not tags)
2. ✅ Use minimal permissions
3. ✅ Never commit secrets to code
4. ✅ Use environment protection rules for production
5. ✅ Review third-party actions before use
6. ✅ Use OIDC for cloud deployments

### Performance
1. ✅ Enable caching for dependencies
2. ✅ Use job parallelization where possible
3. ✅ Implement path filters to reduce runs
4. ✅ Use conditional execution for expensive steps
5. ✅ Optimize Docker layer caching
6. ✅ Use build matrices efficiently

### Cost Optimization
1. ✅ Use `ubuntu-latest` for most jobs (cheapest)
2. ✅ Implement concurrency controls
3. ✅ Set appropriate timeouts
4. ✅ Use path filters to skip unnecessary runs
5. ✅ Schedule non-urgent jobs during off-peak hours
6. ✅ Clean up artifacts regularly (set retention-days)

### Reliability
1. ✅ Set timeouts on all jobs and steps
2. ✅ Use `continue-on-error` appropriately
3. ✅ Implement retry logic for flaky operations
4. ✅ Add proper error handling
5. ✅ Use status checks for critical workflows
6. ✅ Implement notifications for failures

### Maintainability
1. ✅ Use descriptive job and step names
2. ✅ Document complex workflows
3. ✅ Extract reusable workflows for common patterns
4. ✅ Keep workflows DRY
5. ✅ Use consistent naming conventions
6. ✅ Regular dependency updates

## Workflow Templates

### Standard CI Workflow
```yaml
name: CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package*.json'
  pull_request:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package*.json'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

### Reusable Workflow
```yaml
name: Reusable Build

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build
```

## Common Anti-Patterns to Avoid

### ❌ Don't Do This
```yaml
# No permissions specified
# No concurrency control
# No timeout
# Actions not pinned to SHAs
# No caching

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install
      - run: npm test
```

### ✅ Do This Instead
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: false

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci  # Faster and more reliable than npm install
      - run: npm test
```

## Deprecated Features

### ❌ Avoid These
- `::set-output` - Use `$GITHUB_OUTPUT` instead
- `::save-state` - Use `$GITHUB_STATE` instead
- `::set-env` - Use `$GITHUB_ENV` instead
- Old action versions (v1, v2, v3)

### ✅ Use These
```bash
# Deprecated
echo "::set-output name=foo::bar"

# Current
echo "foo=bar" >> $GITHUB_OUTPUT
```

## Monitoring and Maintenance

### Regular Tasks
- [ ] Review workflow execution times monthly
- [ ] Update action versions quarterly
- [ ] Audit permissions quarterly
- [ ] Review artifact retention policies
- [ ] Monitor workflow costs
- [ ] Update this document with new standards

## References
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Action Pinning](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
