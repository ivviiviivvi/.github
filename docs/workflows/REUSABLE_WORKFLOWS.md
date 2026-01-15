# Reusable Workflows Guide

> **Comprehensive guide to using the organization's reusable workflows and
> composite actions**

## Overview

This organization provides **7 reusable workflows and composite actions** that
standardize common CI/CD patterns across all repositories. These workflows
reduce duplication, improve maintainability, and ensure consistent quality
standards.

---

## 📦 Available Reusable Workflows

### 1. Python Setup & Test

**Location:** `.github/workflows/reusable/python-setup-test.yml`

**Purpose:** Standardized Python environment setup with testing and coverage

**Use Cases:**

- Unit testing with pytest
- Integration testing
- Test coverage reporting
- Multi-version Python testing

**Inputs:**

| Input                   | Required | Default                              | Description                                              |
| ----------------------- | -------- | ------------------------------------ | -------------------------------------------------------- |
| `python-version`        | No       | `3.11`                               | Python version (3.9, 3.10, 3.11, 3.12)                   |
| `python-version-matrix` | No       | `""`                                 | JSON array for matrix builds: `["3.10", "3.11", "3.12"]` |
| `requirements-file`     | No       | `requirements.txt`                   | Path to requirements file                                |
| `install-command`       | No       | `pip install -r {requirements-file}` | Custom install command                                   |
| `test-command`          | No       | `pytest`                             | Test execution command                                   |
| `pytest-args`           | No       | `--cov --cov-report=xml`             | pytest arguments                                         |
| `cache-dependency-path` | No       | `requirements*.txt`                  | Dependency files for caching                             |

**Outputs:**

| Output                 | Description                             |
| ---------------------- | --------------------------------------- |
| `python-version`       | Python version used                     |
| `test-result`          | Test execution result (success/failure) |
| `coverage-report-path` | Path to coverage report                 |

**Example Usage:**

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    uses: ivviiviivvi/.github/.github/workflows/reusable/python-setup-test.yml@main
    with:
      python-version: "3.11"
      pytest-args: "--cov --cov-report=xml --cov-report=html"

  test-matrix:
    uses: ivviiviivvi/.github/.github/workflows/reusable/python-setup-test.yml@main
    with:
      python-version-matrix: '["3.10", "3.11", "3.12"]'
      test-command: "pytest tests/"
```

---

### 2. Node.js Setup & Build

**Location:** `.github/workflows/reusable/nodejs-setup-build.yml`

**Purpose:** Node.js environment setup with build and test capabilities

**Use Cases:**

- TypeScript/JavaScript builds
- npm/yarn/pnpm projects
- Frontend application testing
- Package publishing

**Inputs:**

| Input                   | Required | Default                       | Description                         |
| ----------------------- | -------- | ----------------------------- | ----------------------------------- |
| `node-version`          | No       | `20`                          | Node.js version (16, 18, 20, 21)    |
| `node-version-matrix`   | No       | `""`                          | JSON array for matrix builds        |
| `package-manager`       | No       | `npm`                         | Package manager: npm, yarn, or pnpm |
| `install-command`       | No       | `{package-manager} ci`        | Install command                     |
| `build-command`         | No       | `{package-manager} run build` | Build command                       |
| `test-command`          | No       | `{package-manager} test`      | Test command                        |
| `lint-command`          | No       | `{package-manager} run lint`  | Lint command                        |
| `cache-dependency-path` | No       | `package-lock.json`           | Lockfile for caching                |

**Outputs:**

| Output         | Description          |
| -------------- | -------------------- |
| `node-version` | Node.js version used |
| `build-result` | Build result         |
| `test-result`  | Test result          |

**Example Usage:**

```yaml
name: Node.js Build

on: [push, pull_request]

jobs:
  build:
    uses: ivviiviivvi/.github/.github/workflows/reusable/nodejs-setup-build.yml@main
    with:
      node-version: "20"
      package-manager: "npm"
      build-command: "npm run build"
      test-command: "npm run test:ci"

  build-matrix:
    uses: ivviiviivvi/.github/.github/workflows/reusable/nodejs-setup-build.yml@main
    with:
      node-version-matrix: '["18", "20", "21"]'
      package-manager: "pnpm"
```

---

### 3. Docker Build & Push

**Location:** `.github/workflows/reusable/docker-build-push.yml`

**Purpose:** Multi-platform Docker image builds with layer caching

**Use Cases:**

- Container image builds
- Multi-platform images (amd64, arm64)
- Docker Hub / GHCR / ECR publishing
- Development and production builds

**Inputs:**

| Input        | Required | Default                   | Description                           |
| ------------ | -------- | ------------------------- | ------------------------------------- |
| `image-name` | Yes      | -                         | Image name (e.g., `myorg/myapp`)      |
| `dockerfile` | No       | `Dockerfile`              | Path to Dockerfile                    |
| `context`    | No       | `.`                       | Build context path                    |
| `platforms`  | No       | `linux/amd64,linux/arm64` | Target platforms                      |
| `push`       | No       | `true`                    | Push image to registry                |
| `registry`   | No       | `docker.io`               | Container registry                    |
| `tags`       | No       | Auto-generated            | Custom image tags (newline-separated) |
| `build-args` | No       | `""`                      | Build arguments (newline-separated)   |
| `cache-from` | No       | `type=registry`           | Cache source                          |
| `cache-to`   | No       | `type=inline`             | Cache destination                     |

**Secrets:**

| Secret              | Required | Description             |
| ------------------- | -------- | ----------------------- |
| `registry-username` | Yes      | Registry username       |
| `registry-password` | Yes      | Registry password/token |

**Outputs:**

| Output         | Description             |
| -------------- | ----------------------- |
| `image-digest` | Image digest            |
| `image-tags`   | Image tags (JSON array) |

**Example Usage:**

```yaml
name: Build Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    uses: ivviiviivvi/.github/.github/workflows/reusable/docker-build-push.yml@main
    with:
      image-name: "myorg/myapp"
      platforms: "linux/amd64,linux/arm64"
      tags: |
        type=ref,event=branch
        type=ref,event=pr
        type=semver,pattern={{version}}
        type=sha
    secrets:
      registry-username: ${{ secrets.DOCKER_USERNAME }}
      registry-password: ${{ secrets.DOCKER_TOKEN }}
```

---

### 4. GitHub CLI PR Operations

**Location:** `.github/workflows/reusable/github-cli-pr-ops.yml`

**Purpose:** Standardized GitHub CLI operations for Pull Requests

**Use Cases:**

- List pull requests with filters
- Merge pull requests with specific strategies
- Add PR reviews
- Comment on pull requests
- Enable auto-merge

**Inputs:**

| Input          | Required | Default       | Description                                                   |
| -------------- | -------- | ------------- | ------------------------------------------------------------- |
| `operation`    | Yes      | -             | Operation: `list`, `merge`, `review`, `comment`, `auto-merge` |
| `pr-number`    | No       | Auto-detected | PR number (auto-detects from context)                         |
| `pr-filters`   | No       | `""`          | Filters for list operation (e.g., `--state open --label bug`) |
| `merge-method` | No       | `squash`      | Merge method: `squash`, `merge`, `rebase`                     |
| `auto-merge`   | No       | `false`       | Enable auto-merge                                             |
| `comment-body` | No       | `""`          | Comment text                                                  |
| `review-event` | No       | `APPROVE`     | Review event: `APPROVE`, `REQUEST_CHANGES`, `COMMENT`         |
| `review-body`  | No       | `""`          | Review comment text                                           |

**Secrets:**

| Secret         | Required | Description                               |
| -------------- | -------- | ----------------------------------------- |
| `github-token` | No       | GitHub token (defaults to `GITHUB_TOKEN`) |

**Outputs:**

| Output    | Description                  |
| --------- | ---------------------------- |
| `pr-list` | PR list (for list operation) |
| `result`  | Operation result             |

**Example Usage:**

```yaml
name: Auto-Merge Dependabot PRs

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  auto-merge-dependabot:
    if: github.actor == 'dependabot[bot]'
    uses: ivviiviivvi/.github/.github/workflows/reusable/github-cli-pr-ops.yml@main
    with:
      operation: "auto-merge"
      merge-method: "squash"
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}

  add-review:
    uses: ivviiviivvi/.github/.github/workflows/reusable/github-cli-pr-ops.yml@main
    with:
      operation: "review"
      pr-number: ${{ github.event.pull_request.number }}
      review-event: "APPROVE"
      review-body: "LGTM! Auto-approved by workflow."
```

---

### 5. Security Scanning

**Location:** `.github/workflows/reusable/security-scanning.yml`

**Purpose:** Unified security scanning with multiple tools

**Use Cases:**

- CodeQL analysis
- Trivy vulnerability scanning
- Semgrep security audits
- Secret detection
- SARIF reporting

**Inputs:**

| Input              | Required | Default             | Description                                               |
| ------------------ | -------- | ------------------- | --------------------------------------------------------- |
| `scan-type`        | Yes      | -                   | Scan type: `codeql`, `trivy`, `semgrep`, `secrets`, `all` |
| `languages`        | No       | Auto-detected       | CodeQL languages (comma-separated)                        |
| `trivy-scan-type`  | No       | `fs`                | Trivy scan type: `fs`, `image`, `config`, `repo`          |
| `trivy-severity`   | No       | `CRITICAL,HIGH`     | Severity levels to report                                 |
| `semgrep-config`   | No       | `auto`              | Semgrep configuration                                     |
| `secrets-baseline` | No       | `.secrets.baseline` | Secrets baseline file path                                |

**Outputs:**

| Output         | Description              |
| -------------- | ------------------------ |
| `codeql-sarif` | CodeQL SARIF report path |
| `trivy-report` | Trivy report path        |

**Example Usage:**

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 0 * * 0" # Weekly

jobs:
  codeql:
    uses: ivviiviivvi/.github/.github/workflows/reusable/security-scanning.yml@main
    with:
      scan-type: "codeql"
      languages: "python,javascript"
    permissions:
      contents: read
      security-events: write

  trivy:
    uses: ivviiviivvi/.github/.github/workflows/reusable/security-scanning.yml@main
    with:
      scan-type: "trivy"
      trivy-scan-type: "fs"
      trivy-severity: "CRITICAL,HIGH,MEDIUM"

  full-scan:
    uses: ivviiviivvi/.github/.github/workflows/reusable/security-scanning.yml@main
    with:
      scan-type: "all"
    permissions:
      contents: read
      security-events: write
      actions: read
```

---

### 6. Artifact Management

**Location:** `.github/workflows/reusable/artifact-management.yml`

**Purpose:** Standardized artifact upload and download

**Use Cases:**

- Build artifact storage
- Test result preservation
- Cross-job artifact sharing
- Release asset preparation

**Inputs:**

| Input               | Required | Default | Description                         |
| ------------------- | -------- | ------- | ----------------------------------- |
| `operation`         | Yes      | -       | Operation: `upload` or `download`   |
| `artifact-name`     | Yes      | -       | Artifact name                       |
| `artifact-path`     | Yes      | -       | Path to upload/download             |
| `retention-days`    | No       | `30`    | Retention period (1-90 days)        |
| `if-no-files-found` | No       | `warn`  | Behavior: `warn`, `error`, `ignore` |
| `compression-level` | No       | `6`     | Compression level (0-9)             |

**Outputs:**

| Output          | Description              |
| --------------- | ------------------------ |
| `artifact-id`   | Artifact ID (upload)     |
| `download-path` | Download path (download) |

**Example Usage:**

```yaml
name: Build and Test

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - uses: ivviiviivvi/.github/.github/workflows/reusable/artifact-management.yml@main
        with:
          operation: "upload"
          artifact-name: "build-output"
          artifact-path: "dist/"
          retention-days: 7

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ivviiviivvi/.github/.github/workflows/reusable/artifact-management.yml@main
        with:
          operation: "download"
          artifact-name: "build-output"
          artifact-path: "dist/"
      - run: npm test
```

---

## 🔧 Composite Actions

### 7. Standardized Checkout

**Location:** `.github/actions/checkout/action.yml`

**Purpose:** Ratchet-pinned checkout with consistent configuration

**Use Cases:**

- Replace `actions/checkout` calls
- Ensure consistent checkout behavior
- Automatic ratchet pinning management
- Standardized security practices

**Inputs:**

| Input         | Required | Default        | Description                   |
| ------------- | -------- | -------------- | ----------------------------- |
| `fetch-depth` | No       | `1`            | Number of commits to fetch    |
| `token`       | No       | `github.token` | GitHub token                  |
| `submodules`  | No       | `false`        | Checkout submodules           |
| `lfs`         | No       | `false`        | Checkout LFS files            |
| `ref`         | No       | `""`           | Branch/tag/commit to checkout |

**Outputs:**

| Output       | Description            |
| ------------ | ---------------------- |
| `commit-sha` | Checked out commit SHA |

**Example Usage:**

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: ivviiviivvi/.github/.github/actions/checkout@main
        with:
          fetch-depth: 0 # Full history
          submodules: true

      - name: Run tests
        run: npm test
```

**Why use this instead of `actions/checkout` directly?**

- ✅ Automatically ratchet-pinned to secure SHA
- ✅ Consistent configuration across all repositories
- ✅ Centralized updates and security patches
- ✅ Outputs commit info for downstream steps

---

## 🚀 Migration Guide

### Step 1: Identify Candidates

Find workflows in your repository that match these patterns:

**Python workflows:**

```bash
grep -l "setup-python\|pytest" .github/workflows/*.yml
```

**Node.js workflows:**

```bash
grep -l "setup-node\|npm\|yarn" .github/workflows/*.yml
```

**Docker workflows:**

```bash
grep -l "docker build\|docker/build-push-action" .github/workflows/*.yml
```

### Step 2: Update Workflow Files

**Before (traditional workflow):**

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest --cov --cov-report=xml
```

**After (using reusable workflow):**

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    uses: ivviiviivvi/.github/.github/workflows/reusable/python-setup-test.yml@main
    with:
      python-version: "3.11"
      pytest-args: "--cov --cov-report=xml"
```

**Result:**

- ✅ 15 lines → 8 lines (47% reduction)
- ✅ Consistent Python setup across all repos
- ✅ Automatic updates to setup logic
- ✅ Centralized caching strategy

### Step 3: Test the Migration

1. **Create a test branch:**

   ```bash
   git checkout -b migrate-to-reusable-workflows
   ```

1. **Update 1-2 workflows first:**
   - Start with simple, non-critical workflows
   - Verify they run successfully

1. **Gradually migrate remaining workflows:**
   - Update 3-5 workflows at a time
   - Test thoroughly before merging

1. **Monitor workflow runs:**
   - Check Actions tab for any failures
   - Compare run times (should be similar or faster)

### Step 4: Update Documentation

Update your repository's documentation to reference the reusable workflows:

```markdown
## CI/CD

This repository uses [organization reusable workflows](https://github.com/ivviiviivvi/.github/blob/main/docs/workflows/REUSABLE_WORKFLOWS.md):

- Python testing: `python-setup-test.yml`
- Docker builds: `docker-build-push.yml`
- Security scanning: `security-scanning.yml`
```

---

## 📊 Benefits & Impact

### Code Reduction

| Repository Type | Before            | After       | Savings |
| --------------- | ----------------- | ----------- | ------- |
| Python project  | 50 lines/workflow | 8-12 lines  | 76-84%  |
| Node.js project | 45 lines/workflow | 8-12 lines  | 73-82%  |
| Docker project  | 60 lines/workflow | 15-20 lines | 67-75%  |

### Maintenance

- **Centralized updates**: Update once, apply everywhere
- **Consistent behavior**: Same setup across all repositories
- **Easier debugging**: Standard patterns reduce troubleshooting time
- **Security patches**: Automatic ratchet pinning updates

### Cost Optimization

- **Faster builds**: Optimized caching strategies
- **Reduced minutes**: Shorter workflows = lower costs
- **Parallel execution**: Matrix builds built-in
- **Efficient resource use**: Standardized timeouts and concurrency

---

## 🛠️ Best Practices

### Versioning

**Use commit SHA for production:**

```yaml
uses: ivviiviivvi/.github/.github/workflows/reusable/python-setup-test.yml@abc1234
```

**Use branch for development:**

```yaml
uses: ivviiviivvi/.github/.github/workflows/reusable/python-setup-test.yml@main
```

**Use tags for releases:**

```yaml
uses: ivviiviivvi/.github/.github/workflows/reusable/python-setup-test.yml@v1.0.0
```

### Permissions

Always specify permissions explicitly:

```yaml
jobs:
  security-scan:
    uses: ivviiviivvi/.github/.github/workflows/reusable/security-scanning.yml@main
    with:
      scan-type: "codeql"
    permissions:
      contents: read
      security-events: write
      actions: read
```

### Secrets

Pass secrets explicitly (they don't inherit):

```yaml
jobs:
  docker-build:
    uses: ivviiviivvi/.github/.github/workflows/reusable/docker-build-push.yml@main
    with:
      image-name: "myorg/myapp"
    secrets:
      registry-username: ${{ secrets.DOCKER_USERNAME }}
      registry-password: ${{ secrets.DOCKER_TOKEN }}
```

### Testing

Test reusable workflows with `workflow_dispatch`:

```yaml
on:
  workflow_dispatch:
    inputs:
      test-mode:
        description: "Enable test mode"
        required: false
        default: "false"
```

---

## 📖 Additional Resources

- **[GitHub Actions Documentation](https://docs.github.com/actions)<!-- link:docs.github_actions_root -->**
- **[Reusable Workflows Docs](https://docs.github.com/actions/using-workflows/reusing-workflows)**
- **[Composite Actions Docs](https://docs.github.com/actions/creating-actions/creating-a-composite-action)**
- **[Organization Workflows Guide](https://docs.github.com/actions/using-workflows/sharing-workflows-secrets-and-runners-with-your-organization)**

### Internal Resources

- **[Workflow Optimization Guide](./WORKFLOW_OPTIMIZATION.md)** - Performance
  tips
- **[Security Best Practices](../SECURITY_BEST_PRACTICES.md)** - Security
  guidelines
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute

---

## 🤝 Contributing

Have ideas for new reusable workflows? See our
[Contributing Guide](../CONTRIBUTING.md).

**Common workflow patterns to contribute:**

- [ ] Go setup and testing
- [ ] Rust build and test
- [ ] Terraform validation
- [ ] AWS deployment
- [ ] Kubernetes deployment
- [ ] Database migrations
- [ ] API integration tests
- [ ] Performance benchmarking
- [ ] Documentation generation
- [ ] Release automation

---

## 📝 Changelog

### 2026-01-14 - Initial Release

**Added:**

- 7 reusable workflows and composite actions
- Comprehensive documentation
- Migration examples
- Best practices guide

**Workflows:**

1. ✅ Python Setup & Test
1. ✅ Node.js Setup & Build
1. ✅ Docker Build & Push
1. ✅ GitHub CLI PR Operations
1. ✅ Security Scanning
1. ✅ Artifact Management
1. ✅ Checkout Composite Action

---

**Questions or Issues?**

- 📖
  [View Examples](https://github.com/ivviiviivvi/.github/tree/main/.github/workflows/reusable)
- 💬
  [Open a Discussion](https://github.com/orgs/ivviiviivvi/discussions)<!-- link:github.org_discussions -->
- 🐛
  [Report an Issue](https://github.com/ivviiviivvi/.github/issues)<!-- link:github.issues -->

---

_Last Updated: 2026-01-14_
