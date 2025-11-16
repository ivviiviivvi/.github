# Automation Master Guide

Complete reference for all automation, tooling, and integrations in this gold standard repository.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Automation Layers](#automation-layers)
- [Workflow Catalog](#workflow-catalog)
- [Tool Stack](#tool-stack)
- [Integration Map](#integration-map)
- [Customization Guide](#customization-guide)
- [Troubleshooting](#troubleshooting)

---

## Quick Reference

### What Happens Automatically?

| Event | Automated Actions | Workflows |
|-------|-------------------|-----------|
| **Push to main** | Security scan, deploy, metrics, release | 10+ workflows |
| **Pull Request** | Tests, linting, coverage, quality checks, review | 12+ workflows |
| **New Issue** | Auto-label, auto-assign, welcome message | 3 workflows |
| **Schedule** | Dependency updates, stale cleanup, metrics | 5 workflows |
| **Release Tag** | Changelog, GitHub release, package publish | 2 workflows |

### Automation Coverage

```
✅ 100% - Security scanning
✅ 100% - Code quality checks
✅ 100% - Dependency management
✅ 95%  - Documentation updates
✅ 90%  - Release management
✅ 85%  - Performance monitoring
```

---

## Automation Layers

### Layer 1: Pre-Commit (Local)

**Runs**: Before git commit

**Tools**: pre-commit hooks (`.pre-commit-config.yaml`)

**Checks**:
- Code formatting (Black, Prettier, etc.)
- Linting (ESLint, flake8, etc.)
- Type checking (mypy, TypeScript)
- Secrets detection
- Conventional commit format
- File size limits

**Bypass** (use sparingly):
```bash
git commit --no-verify -m "WIP: quick fix"
```

### Layer 2: CI/CD (GitHub Actions)

**Runs**: On push/PR

**Workflows**: 20+ automated workflows

**Categories**:
1. **Security**: CodeQL, Semgrep, Dependency review, Secret scanning
2. **Quality**: Linting, testing, coverage, code review
3. **Performance**: Benchmarks, bundle size, load testing
4. **Documentation**: Link checking, spell checking

### Layer 3: Scheduled Automation

**Runs**: On schedule (cron)

**Workflows**:
- Daily: Security scans
- Weekly: Dependency updates, link checks, stale management
- Monthly: Repository metrics, contributor updates

### Layer 4: Release Automation

**Runs**: On tag/merge to main

**Actions**:
- Semantic versioning
- Changelog generation
- Package publishing
- Container building
- Deployment

### Layer 5: Community Automation

**Runs**: On issue/PR/comment events

**Actions**:
- Auto-labeling
- Auto-assignment
- Welcome messages
- Stale management
- Contributor recognition

---

## Workflow Catalog

### Security Workflows (6)

#### 1. CodeQL Analysis
**File**: `.github/workflows/codeql-analysis.yml`
- **Trigger**: Push, PR, Weekly schedule
- **Languages**: JavaScript, Python (configurable)
- **Output**: SARIF to Security tab
- **Runtime**: ~5-10 minutes

#### 2. Semgrep Security
**File**: `.github/workflows/semgrep.yml`
- **Trigger**: Push, PR, Daily schedule
- **Rules**: OWASP Top 10, CWE Top 25, Custom rules
- **Output**: SARIF + PR comments
- **Runtime**: ~2-3 minutes

#### 3. Dependency Review
**File**: `.github/workflows/dependency-review.yml`
- **Trigger**: Pull requests
- **Checks**: Vulnerabilities, licenses
- **Thresholds**: Moderate+ severity
- **Runtime**: ~1 minute

#### 4. SBOM Generation
**File**: `.github/workflows/sbom-generation.yml`
- **Trigger**: Release, Push to main
- **Formats**: SPDX, CycloneDX
- **Output**: Artifacts, Dependency graph
- **Runtime**: ~2 minutes

#### 5. Secret Scanning
**Feature**: Built-in GitHub feature
- **Trigger**: Every push
- **Detection**: API keys, tokens, credentials
- **Action**: Block push (if push protection enabled)

#### 6. Container Scanning
**File**: `.github/workflows/ci-advanced.yml` (Docker job)
- **Tool**: Trivy
- **Checks**: Vulnerabilities, misconfigurations
- **Runtime**: ~3 minutes

### Quality Workflows (7)

#### 1. Advanced CI Pipeline
**File**: `.github/workflows/ci-advanced.yml`
- **Languages**: Auto-detects (Python, Node, Go, Rust)
- **Platforms**: Ubuntu, Windows, macOS
- **Versions**: Matrix testing
- **Runtime**: ~10-20 minutes

#### 2. Code Coverage
**File**: `.github/workflows/code-coverage.yml`
- **Integration**: Codecov
- **Threshold**: 70% minimum
- **Output**: PR comments, badges
- **Runtime**: ~5 minutes

#### 3. PR Quality Checks
**File**: `.github/workflows/pr-quality-checks.yml`
- **Validates**: Title, description, size, conflicts
- **Comments**: Helpful suggestions
- **Runtime**: ~1 minute

#### 4. Auto-Labeler
**File**: `.github/workflows/auto-labeler.yml`
- **Based on**: File paths, content, size
- **Labels**: Language, type, size
- **Runtime**: ~30 seconds

#### 5. Link Checker
**File**: `.github/workflows/link-checker.yml`
- **Tools**: Lychee, markdown-link-check
- **Frequency**: Weekly + on doc changes
- **Runtime**: ~2-3 minutes

#### 6. Claude Code Review
**File**: `.github/workflows/claude-code-review.yml`
- **Trigger**: Pull requests
- **Analysis**: Best practices, security, performance
- **Runtime**: ~3-5 minutes

#### 7. Performance Benchmark
**File**: `.github/workflows/performance-benchmark.yml`
- **Tests**: Benchmarks, Lighthouse, bundle size
- **Alerts**: 150% regression threshold
- **Runtime**: ~5-10 minutes

### Release Workflows (3)

#### 1. Semantic Release
**File**: `.github/workflows/semantic-release.yml`
- **Versioning**: Automatic based on commits
- **Outputs**: Tag, release, changelog
- **Publishing**: npm, PyPI, containers
- **Runtime**: ~3-5 minutes

#### 2. Release Management
**File**: `.github/workflows/release.yml`
- **Trigger**: Version tags
- **Actions**: Create release, generate notes
- **Assets**: Binaries, changelog
- **Runtime**: ~5 minutes

#### 3. Version Bump
**File**: `.github/workflows/version-bump.yml`
- **Trigger**: Manual
- **Creates**: PR with version update
- **Supports**: npm, Python, Go, Rust
- **Runtime**: ~1 minute

### Community Workflows (4)

#### 1. Welcome Bot
**File**: `.github/workflows/welcome.yml`
- **Trigger**: First issue/PR
- **Action**: Post welcome message
- **Runtime**: ~10 seconds

#### 2. Auto-Assign
**File**: `.github/workflows/auto-assign.yml`
- **PR**: Assign to author
- **Issues**: Distribute to maintainers
- **Runtime**: ~10 seconds

#### 3. Community Health
**File**: `.github/workflows/community-health.yml`
- **Frequency**: Weekly
- **Actions**: Stale management, metrics, contributors
- **Runtime**: ~2-3 minutes

#### 4. Repository Metrics
**File**: `.github/workflows/repo-metrics.yml`
- **Frequency**: Monthly
- **Generates**: Stats, contributor lists, insights
- **Runtime**: ~3-5 minutes

---

## Tool Stack

### Analysis & Security

| Tool | Purpose | Integration | Cost |
|------|---------|-------------|------|
| **CodeQL** | SAST | Workflow | Free |
| **Semgrep** | Pattern-based SAST | Workflow | Free |
| **Trivy** | Container scanning | Workflow | Free |
| **Dependabot** | Dependency updates | Config file | Free |
| **Renovate** | Advanced dependency mgmt | Config file | Free |
| **Snyk** | Multi-purpose security | Optional | Freemium |

### Code Quality

| Tool | Purpose | Integration | Cost |
|------|---------|-------------|------|
| **Prettier** | Code formatting | Pre-commit | Free |
| **ESLint** | JavaScript linting | Pre-commit | Free |
| **Black** | Python formatting | Pre-commit | Free |
| **flake8** | Python linting | Pre-commit | Free |
| **mypy** | Python type checking | Pre-commit | Free |
| **Codecov** | Coverage tracking | Workflow | Freemium |

### AI & Intelligence

| Tool | Purpose | Integration | Cost |
|------|---------|-------------|------|
| **GitHub Copilot** | Code completion | IDE | Paid |
| **Claude Code** | PR reviews | Workflow | Varies |
| **Sourcegraph** | Code search | Optional | Freemium |
| **Cody** | AI assistant | IDE | Freemium |

### Release & Versioning

| Tool | Purpose | Integration | Cost |
|------|---------|-------------|------|
| **semantic-release** | Automated releases | Workflow | Free |
| **GoReleaser** | Go releases | Workflow | Free |
| **Changesets** | Monorepo versioning | Optional | Free |

---

## Integration Map

```
┌─────────────────────────────────────────────────────┐
│                   Developer                          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Pre-commit Hooks                        │
│  • Format • Lint • Type Check • Secrets             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                 Git Push                             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              GitHub Actions                          │
│  ┌──────────────┬──────────────┬──────────────┐    │
│  │   Security   │   Quality    │  Performance  │    │
│  │  • CodeQL    │  • Tests     │  • Benchmarks │    │
│  │  • Semgrep   │  • Lint      │  • Lighthouse │    │
│  │  • Deps      │  • Coverage  │  • Bundle     │    │
│  └──────────────┴──────────────┴──────────────┘    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Pull Request                            │
│  • Auto-label • Quality checks • Reviews            │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Merge to Main                           │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│           Semantic Release                           │
│  • Version • Changelog • Tag • Publish              │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Deployment                              │
│  • Container build • SBOM • Monitoring              │
└─────────────────────────────────────────────────────┘
```

---

## Customization Guide

### Enable/Disable Workflows

**Disable a workflow**:
```yaml
# Add to workflow file
on:
  workflow_dispatch: # Only manual trigger

# Or comment out the triggers
# on:
#   push:
#   pull_request:
```

**Enable additional languages**:
```yaml
# .github/workflows/codeql-analysis.yml
matrix:
  language: [ 'javascript', 'python', 'go', 'java' ]
```

### Adjust Thresholds

**Coverage threshold**:
```yaml
# .github/workflows/code-coverage.yml
- name: Coverage check
  run: pytest --cov-fail-under=80  # Change from 70 to 80
```

**Performance threshold**:
```yaml
# .github/workflows/performance-benchmark.yml
with:
  alert-threshold: '120%'  # Change from 150% to 120%
```

### Add Custom Rules

**Semgrep custom rules**:
```yaml
# .semgrep/rules.yml
rules:
  - id: my-custom-rule
    pattern: dangerous_function($X)
    message: Don't use dangerous_function
    severity: ERROR
    languages: [javascript]
```

**Pre-commit hooks**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: my-custom-check
        name: Custom Check
        entry: ./scripts/custom-check.sh
        language: script
```

### Configure Notifications

**Slack notifications**:
```yaml
# Add to workflow
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

**Email notifications**:
```yaml
# Settings → Notifications → configure per workflow
```

---

## Troubleshooting

### Common Issues

#### Workflow Not Running

**Problem**: Workflow doesn't trigger

**Solutions**:
1. Check workflow syntax: `gh workflow view workflow-name`
2. Verify triggers match event
3. Check branch name matches trigger
4. Ensure workflow file is in `.github/workflows/`
5. Look for syntax errors: `yamllint .github/workflows/*.yml`

#### Pre-commit Hooks Failing

**Problem**: Hooks block commits

**Solutions**:
```bash
# Skip hooks temporarily (not recommended)
git commit --no-verify

# Update hooks
pre-commit autoupdate

# Clear cache
pre-commit clean

# Run specific hook
pre-commit run hook-id --all-files
```

#### Coverage Failing

**Problem**: Below threshold

**Solutions**:
1. Add tests for uncovered code
2. Adjust threshold temporarily
3. Exclude test files from coverage
4. Check coverage report: `open htmlcov/index.html`

#### Semantic Release Not Working

**Problem**: No release created

**Solutions**:
1. Verify commit message format
2. Check branch is main/master
3. Ensure commits since last release
4. Verify GitHub token permissions
5. Run locally: `npx semantic-release --dry-run`

### Debug Workflows

```bash
# View workflow runs
gh run list --workflow=ci-advanced.yml

# View specific run
gh run view <run-id>

# View logs
gh run view <run-id> --log

# Re-run failed jobs
gh run rerun <run-id> --failed

# Cancel running workflow
gh run cancel <run-id>
```

### Performance Optimization

**Slow workflows**:
```yaml
# Add concurrency limits
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Cache dependencies
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

# Use matrix strategically
strategy:
  matrix:
    os: [ubuntu-latest]  # Only Linux for faster runs
    node-version: [20]   # Only LTS version
```

---

## Maintenance Schedule

### Daily
- [ ] Review failed workflows
- [ ] Check security alerts
- [ ] Merge Dependabot PRs (if auto-merge disabled)

### Weekly
- [ ] Review stale issues/PRs
- [ ] Check coverage trends
- [ ] Update documentation
- [ ] Review performance metrics

### Monthly
- [ ] Audit workflow efficiency
- [ ] Update tool versions
- [ ] Review and update custom rules
- [ ] Clean up old artifacts
- [ ] Review access permissions

### Quarterly
- [ ] Security audit
- [ ] Dependency major version updates
- [ ] Workflow optimization review
- [ ] Tool stack evaluation
- [ ] Documentation comprehensive review

---

## Quick Commands

```bash
# Workflows
gh workflow list
gh workflow run <name>
gh workflow disable <name>
gh workflow enable <name>

# Runs
gh run list --limit 10
gh run view <id>
gh run rerun <id>
gh run cancel <id>

# Pre-commit
pre-commit run --all-files
pre-commit autoupdate
pre-commit clean

# Testing locally
act                          # Run workflows locally with act
act -l                       # List available workflows
act -j job-name             # Run specific job

# Secrets
gh secret set SECRET_NAME
gh secret list
gh secret remove SECRET_NAME
```

---

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [pre-commit Docs](https://pre-commit.com/)
- [semantic-release Docs](https://semantic-release.gitbook.io/)
- [Semgrep Rules](https://semgrep.dev/explore)

---

## Conclusion

This repository includes **20+ automated workflows**, **30+ pre-commit hooks**, and **10+ integrations** providing:

- 🔒 **Security**: 6 layers of security scanning
- ✅ **Quality**: Automated testing and coverage
- 🚀 **Performance**: Continuous monitoring
- 📦 **Releases**: Fully automated versioning
- 👥 **Community**: Welcoming and inclusive automation
- 📊 **Insights**: Data-driven metrics

**Everything runs automatically. Your job is to write great code!**

---

**Last Updated**: 2024-11-08
