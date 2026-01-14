# Dependency Management Guide

> **Best practices for managing dependencies across the ivviiviivvi
> organization**

**Last Updated:** 2026-01-14

---

## Table of Contents

- [Overview](#overview)
- [Dependency Philosophy](#dependency-philosophy)
- [Version Pinning Strategy](#version-pinning-strategy)
- [Dependabot Configuration](#dependabot-configuration)
- [Pre-commit Dependencies](#pre-commit-dependencies)
- [GitHub Actions Dependencies](#github-actions-dependencies)
- [Language-Specific Guidelines](#language-specific-guidelines)
- [Security Considerations](#security-considerations)
- [Update Procedures](#update-procedures)

---

## Overview

This guide establishes standards for dependency management across all projects
in the ivviiviivvi organization. Proper dependency management ensures:

- **Security**: Known vulnerabilities are promptly addressed
- **Stability**: Predictable builds and deployments
- **Reproducibility**: Consistent environments across machines
- **Maintainability**: Clear dependency relationships

---

## Dependency Philosophy

### Core Principles

1. **Pin Everything**: All dependencies should specify exact versions
1. **Update Regularly**: Keep dependencies current with security patches
1. **Minimize Dependencies**: Only add what's truly needed
1. **Audit Dependencies**: Regularly review for security vulnerabilities
1. **Document Reasons**: Explain why each dependency is needed

### Dependency Decision Matrix

| Factor             | Add Dependency     | Use Standard Library |
| ------------------ | ------------------ | -------------------- |
| Core functionality | ✅                 | ✅ (preferred)       |
| Simple utility     | ❌                 | ✅                   |
| Complex algorithm  | ✅                 | ❌                   |
| One-time use       | ❌                 | ✅                   |
| Well-maintained    | ✅                 | N/A                  |
| Security-critical  | Evaluate carefully | ✅ (preferred)       |

---

## Version Pinning Strategy

### Pinning Formats

**Exact Version** (most restrictive):

```
package==1.2.3
```

- **Use for**: Production dependencies, CI/CD
- **Benefit**: Maximum reproducibility
- **Risk**: Miss important patches

**Compatible Version** (semantic):

```
package~=1.2.3  # Python (>=1.2.3, <1.3.0)
package^1.2.3   # npm (>=1.2.3, <2.0.0)
```

- **Use for**: Libraries, development tools
- **Benefit**: Allows patch updates
- **Risk**: Breaking changes in patches

**Range** (flexible):

```
package>=1.2.0,<2.0.0
```

- **Use for**: Framework plugins, broad compatibility
- **Benefit**: Most flexible
- **Risk**: Unpredictable behavior

### Recommended Strategy

**Production Code:**

```txt
# requirements.txt (Python)
Django==4.2.7
requests==2.31.0
psycopg2-binary==2.9.9
```

**Development Tools:**

```txt
# requirements-dev.txt
pytest~=7.4.0
black~=23.12.0
flake8~=6.1.0
```

**CI/CD:**

```yaml
# .github/workflows/ci.yml
- uses: actions/setup-python@11bd71901bbe5b1630ceea73d27597364c9af683 # ratchet:actions/setup-python@v5.0.0
```

---

## Dependabot Configuration

### Organization-Wide Settings

Dependabot should be enabled for all repositories with consistent configuration:

```yaml
# .github/dependabot.yml
version: 2
updates:
  # GitHub Actions dependencies
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "06:00"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "github-actions"
    reviewers:
      - "security-team"

  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "tuesday"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "python"
    allow:
      - dependency-type: "direct"
      - dependency-type: "indirect"

  # Node.js dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "wednesday"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "javascript"
    versioning-strategy: increase
```

### Dependabot PR Workflow

When Dependabot creates a PR:

1. **Automated Checks**:
   - CI pipeline runs automatically
   - Security scan validates no new vulnerabilities
   - Pre-commit hooks validate code quality

1. **Manual Review**:
   - Check CHANGELOG for breaking changes
   - Review security advisory (if present)
   - Validate test coverage

1. **Approval**:
   - Minor/patch updates: Auto-merge if tests pass
   - Major updates: Manual review required

1. **Merge Strategy**:

   ```
   # Batch similar updates
   git checkout -b deps/weekly-updates
   git merge dependabot/npm/package1
   git merge dependabot/npm/package2
   git push
   ```

### Grouping Updates

Group related dependencies to reduce PR noise:

```yaml
# .github/dependabot.yml
groups:
  # Group Python testing dependencies
  python-testing:
    patterns:
      - "pytest*"
      - "coverage*"
      - "mock*"

  # Group GitHub Actions
  github-actions:
    patterns:
      - "actions/*"
```

---

## Pre-commit Dependencies

### Managing Pre-commit Hooks

Pre-commit hooks have their own dependencies that must be managed:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0 # ✅ Pin to specific tag
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/psf/black
    rev: 23.12.1 # ✅ Pin to specific tag
    hooks:
      - id: black
        additional_dependencies: # ⚠️ These need pinning too!
          - click==8.1.7
```

### Additional Dependencies in Hooks

Some hooks require `additional_dependencies`:

**✅ CORRECT** (pinned versions):

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.7.1
  hooks:
    - id: mypy
      additional_dependencies:
        - types-requests==2.31.0.10
        - types-PyYAML==6.0.12.12
```

**❌ WRONG** (unpinned):

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.7.1
  hooks:
    - id: mypy
      additional_dependencies:
        - types-requests # No version!
        - types-all # Can pull yanked packages!
```

### Updating Pre-commit Hooks

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Update specific hook
pre-commit autoupdate --repo https://github.com/psf/black

# Review changes
git diff .pre-commit-config.yaml

# Test updated hooks
pre-commit run --all-files

# Commit if successful
git add .pre-commit-config.yaml
git commit -m "chore: update pre-commit hooks"
```

---

## GitHub Actions Dependencies

### SHA Pinning with Ratchet

**Why SHA Pinning?**

GitHub Action tags are mutable - they can be moved to point to different code.
SHA pinning ensures immutability:

```yaml
# ❌ BAD - Tags can be moved
- uses: actions/checkout@v4

# ✅ GOOD - Immutable SHA with context
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # ratchet:actions/checkout@v4.2.2
```

### Installing Ratchet

```bash
# Install Go (if not already installed)
# macOS: brew install go
# Linux: apt install golang-go

# Install ratchet
go install github.com/sethvargo/ratchet@latest

# Verify installation
ratchet --version
```

### Using Ratchet

**Update all workflows:**

```bash
# Pin all actions in workflows
ratchet pin .github/workflows/*.yml

# Update existing pins to latest versions
ratchet update .github/workflows/*.yml

# Unpin (convert back to tags) - not recommended
ratchet unpin .github/workflows/*.yml
```

**Example workflow:**

```bash
# 1. Update pins
cd /workspace
ratchet update .github/workflows/*.yml

# 2. Review changes
git diff .github/workflows/

# 3. Test (run workflow manually)
gh workflow run ci.yml

# 4. Commit
git add .github/workflows/
git commit -m "chore: update GitHub Action SHAs

Updated action pins to latest versions:
- actions/checkout: v4.2.1 → v4.2.2
- actions/setup-python: v5.0.0 → v5.1.0
- actions/cache: v3.3.3 → v4.0.0"
```

### Third-Party Actions

Be extra cautious with third-party actions:

```yaml
# Verify publisher and stars
- uses: octokit/request-action@v2.x # ⚠️ Evaluate carefully

# Prefer official actions when available
- uses: actions/github-script@v7 # ✅ Official action
```

**Vetting Checklist:**

- [ ] Action is from verified publisher
- [ ] Source code is available and reviewed
- [ ] Action has good reputation (stars, usage)
- [ ] Recent updates and maintenance
- [ ] No reported security issues
- [ ] SHA pinned, not tag

---

## Language-Specific Guidelines

### Python

**requirements.txt** (production):

```txt
# Core dependencies
Django==4.2.7
psycopg2-binary==2.9.9
requests==2.31.0
celery==5.3.4

# Why each dependency:
# Django: Web framework
# psycopg2: PostgreSQL adapter
# requests: HTTP client
# celery: Task queue
```

**requirements-dev.txt** (development):

```txt
# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-django==4.7.0

# Code quality
black==23.12.1
flake8==6.1.0
mypy==1.7.1

# Development tools
ipython==8.18.1
ipdb==0.13.13
```

**setup.py / pyproject.toml**:

```toml
[project]
dependencies = [
    "Django>=4.2,<4.3",  # Allow patch updates
    "requests~=2.31.0",  # Compatible versions
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "black>=23.0",
]
```

### Node.js / npm

**package.json**:

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "~4.17.21"
  },
  "devDependencies": {
    "eslint": "^8.55.0",
    "jest": "^29.7.0",
    "prettier": "^3.1.1"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

**package-lock.json**:

- Always commit `package-lock.json`
- Ensures exact versions across environments
- Run `npm ci` in CI/CD (not `npm install`)

### Go

**go.mod**:

```go
module github.com/ivviiviivvi/example

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/lib/pq v1.10.9
)

// Pin transitive dependencies if needed
require (
    golang.org/x/crypto v0.16.0 // indirect
)
```

**Updating:**

```bash
# Update all dependencies
go get -u ./...

# Update specific dependency
go get -u github.com/gin-gonic/gin@v1.10.0

# Tidy dependencies
go mod tidy

# Verify
go mod verify
```

---

## Security Considerations

### Vulnerability Scanning

**Python (pip-audit):**

```bash
# Install
pip install pip-audit

# Scan current environment
pip-audit

# Scan requirements file
pip-audit -r requirements.txt

# Output formats
pip-audit --format json -o vulnerabilities.json
pip-audit --format cyclonedx-json -o sbom.json
```

**Node.js (npm audit):**

```bash
# Scan dependencies
npm audit

# Show detailed report
npm audit --json

# Fix automatically (be careful!)
npm audit fix

# Fix including breaking changes
npm audit fix --force
```

**GitHub Advisory Database:**

- Enable Dependabot alerts
- Review security advisories
- Subscribe to notifications
- Regular manual review

### Security Update Policy

**🔴 CRITICAL** (CVE 9.0-10.0):

- Fix immediately (within hours)
- Emergency deployment if needed
- Notify users if exposed

**🟠 HIGH** (CVE 7.0-8.9):

- Fix within 24-48 hours
- Include in next regular release
- Update documentation

**🟡 MEDIUM** (CVE 4.0-6.9):

- Fix within 1 week
- Batch with other updates
- Test thoroughly

**🟢 LOW** (CVE 0.1-3.9):

- Fix in next maintenance cycle
- Monitor for exploitation
- Document for users

### Known Exceptions

Document dependencies with known issues that can't be immediately fixed:

```txt
# requirements.txt

# Known vulnerabilities requiring exceptions:
# - package-name==1.2.3
#   CVE-2023-12345 (Severity: Medium)
#   Reason: No fix available yet, mitigated by network isolation
#   Ticket: #123
#   Review Date: 2024-02-01
```

---

## Update Procedures

### Weekly Update Cycle

**Monday:**

- Review Dependabot PRs from previous week
- Merge approved updates
- Create manual PRs for pinned dependencies

**Tuesday-Wednesday:**

- Test merged updates in staging
- Monitor for issues
- Rollback if needed

**Thursday:**

- Deploy to production
- Monitor metrics
- Document any issues

**Friday:**

- Review security advisories
- Plan manual updates if needed
- Update documentation

### Monthly Security Audit

1. **Scan All Dependencies:**

   ```bash
   # Python
   pip-audit

   # Node.js
   npm audit

   # Go
   go list -m all | nancy sleuth
   ```

1. **Review Dependabot Alerts:**
   - Check GitHub Security tab
   - Verify no open critical issues
   - Document exceptions

1. **Update Pinned Actions:**

   ```bash
   ratchet update .github/workflows/*.yml
   git diff .github/workflows/
   # Review and commit
   ```

1. **Audit Pre-commit Hooks:**

   ```bash
   pre-commit autoupdate
   pre-commit run --all-files
   # Review and commit
   ```

1. **Document Findings:**
   - Update SECURITY.md
   - Create issues for needed work
   - Update this guide

### Emergency Updates

For critical security vulnerabilities:

1. **Immediate Assessment:**
   - Validate vulnerability affects us
   - Determine impact and exploitability
   - Create incident ticket

1. **Quick Fix:**

   ```bash
   # Update dependency
   pip install package-name==fixed.version
   pip freeze > requirements.txt

   # Or for npm
   npm install package-name@fixed-version
   ```

1. **Test:**
   - Run full test suite
   - Manual smoke testing
   - Verify vulnerability is fixed

1. **Deploy:**
   - Emergency deployment
   - Monitor closely
   - Document in incident report

1. **Follow-up:**
   - Update Dependabot config
   - Review similar dependencies
   - Improve detection

---

## Checklist for New Dependencies

Before adding a new dependency, verify:

- [ ] **Necessity**: Can't use standard library or existing dependency?
- [ ] **Maintenance**: Recently updated (within 6 months)?
- [ ] **Popularity**: Good stars/downloads/usage?
- [ ] **License**: Compatible with project license?
- [ ] **Security**: No known vulnerabilities?
- [ ] **Size**: Reasonable size and dependency tree?
- [ ] **Documentation**: Well-documented?
- [ ] **Alternatives**: Evaluated other options?
- [ ] **Version Pinned**: Specific version in requirements?
- [ ] **Reason Documented**: Why is it needed?

---

## Tools and Resources

### Dependency Management Tools

- **[Dependabot](https://github.com/dependabot)** - Automated dependency updates
- **[Renovate](https://github.com/renovatebot/renovate)** - Alternative to
  Dependabot
- **[pip-audit](https://github.com/pypa/pip-audit)** - Python vulnerability
  scanner
- **[npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit)** - Node.js
  vulnerability scanner
- **[Ratchet](https://github.com/sethvargo/ratchet)** - GitHub Actions SHA
  pinning

### Security Resources

- **[GitHub Advisory Database](https://github.com/advisories)** - Security
  advisories
- **[Snyk Vulnerability Database](https://security.snyk.io/)** - Comprehensive
  vulnerability DB
- **[National Vulnerability Database](https://nvd.nist.gov/)** - NIST CVE
  database
- **[OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)**
  \- Software composition analysis

### Related Documentation

- [Security Best Practices](security-best-practices.md) - Security guidelines
- [SECURITY.md](../SECURITY.md) - Security disclosure policy
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

---

## Questions or Feedback?

- **Questions**: Open a
  [discussion](https://github.com/ivviiviivvi/.github/discussions)
- **Issues**: Report in
  [issue tracker](https://github.com/ivviiviivvi/.github/issues)
- **Improvements**: Submit a [pull request](../CONTRIBUTING.md)

---

**Remember: Good dependency management is proactive, not reactive!**
