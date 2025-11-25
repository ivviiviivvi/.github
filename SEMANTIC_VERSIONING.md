# Semantic Versioning & Automated Releases

Comprehensive guide to semantic versioning (semver) and automated release management.

## Table of Contents

- [Semantic Versioning Basics](#semantic-versioning-basics)
- [Conventional Commits](#conventional-commits)
- [Automated Releases](#automated-releases)
- [Version Ranges](#version-ranges)
- [Breaking Changes](#breaking-changes)
- [Pre-release Versions](#pre-release-versions)
- [Tools & Configuration](#tools--configuration)

---

## Semantic Versioning Basics

### Format: MAJOR.MINOR.PATCH

```
1.2.3
│ │ │
│ │ └─ PATCH: Bug fixes (backward compatible)
│ └─── MINOR: New features (backward compatible)
└───── MAJOR: Breaking changes (not backward compatible)
```

### Version Increment Rules

| Change Type | Version | Example | When to Use |
|-------------|---------|---------|-------------|
| **Breaking Change** | MAJOR | 1.0.0 → 2.0.0 | API changes, removed features |
| **New Feature** | MINOR | 1.0.0 → 1.1.0 | New functionality, backward compatible |
| **Bug Fix** | PATCH | 1.0.0 → 1.0.1 | Bug fixes, security patches |

### Examples

```
0.1.0  → Initial development
0.2.0  → Added new feature
0.2.1  → Fixed bug
1.0.0  → First stable release
1.1.0  → Added backward-compatible feature
1.1.1  → Fixed bug
2.0.0  → Breaking API change
```

---

## Conventional Commits

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types and Version Impact

| Type | Version Bump | Description |
|------|--------------|-------------|
| `feat` | MINOR | New feature |
| `fix` | PATCH | Bug fix |
| `perf` | PATCH | Performance improvement |
| `docs` | PATCH | Documentation only |
| `style` | PATCH | Code style (formatting) |
| `refactor` | PATCH | Code refactoring |
| `test` | PATCH | Adding tests |
| `build` | PATCH | Build system changes |
| `ci` | PATCH | CI configuration |
| `chore` | No bump | Maintenance tasks |
| `revert` | PATCH | Revert previous commit |
| `BREAKING CHANGE` | MAJOR | Breaking change (any type) |

### Examples

**Patch Release (1.0.0 → 1.0.1)**
```bash
git commit -m "fix: resolve memory leak in user service"
git commit -m "docs: update API documentation"
git commit -m "perf: improve database query performance"
```

**Minor Release (1.0.0 → 1.1.0)**
```bash
git commit -m "feat: add user profile customization"
git commit -m "feat(api): implement new REST endpoints"
```

**Major Release (1.0.0 → 2.0.0)**
```bash
# Method 1: Using ! suffix
git commit -m "feat!: redesign authentication API"

# Method 2: Using BREAKING CHANGE footer
git commit -m "feat: redesign authentication API

BREAKING CHANGE: The authentication API has been completely redesigned.
All clients must migrate to the new OAuth2 flow.

Migration guide: docs/migration-v2.md"

# Method 3: Multiple breaking changes
git commit -m "refactor!: restructure data models

BREAKING CHANGE: User model field 'name' split into 'firstName' and 'lastName'
BREAKING CHANGE: API endpoint /users now requires authentication"
```

---

## Automated Releases

### semantic-release Configuration

**Already configured** in `.releaserc.json`

### How It Works

1. **Commit Analysis**: Analyzes commits since last release
2. **Version Calculation**: Determines next version based on commit types
3. **Changelog Generation**: Creates/updates CHANGELOG.md
4. **Version Bump**: Updates version in package.json, pyproject.toml, etc.
5. **Git Tag**: Creates git tag for the release
6. **GitHub Release**: Creates GitHub release with notes
7. **Package Publishing**: Publishes to npm, PyPI, etc. (optional)
8. **Git Commit**: Commits changelog and version changes

### Workflow Trigger

```yaml
# Automatically runs on push to main/master
on:
  push:
    branches:
      - main
      - master
```

### Manual Release

```bash
# Trigger workflow manually
gh workflow run semantic-release.yml
```

---

## Version Ranges

### NPM/JavaScript

```json
{
  "dependencies": {
    "exact": "1.2.3",           // Exact version only
    "patch": "~1.2.3",          // >=1.2.3 <1.3.0 (patch updates)
    "minor": "^1.2.3",          // >=1.2.3 <2.0.0 (minor updates)
    "latest": "*",              // Any version (avoid!)
    "range": ">=1.2.0 <2.0.0",  // Specific range
    "or": "1.2.x || 1.3.x"      // Multiple ranges
  }
}
```

### Python

```python
# requirements.txt
package==1.2.3      # Exact version
package>=1.2.3      # Minimum version
package>=1.2,<2.0   # Version range
package~=1.2.0      # Compatible version (>=1.2.0, <1.3.0)
package[extra]      # With extras
```

### Go

```go
// go.mod
require (
    github.com/user/pkg v1.2.3        // Exact version
    github.com/user/pkg v1.2.0        // Minimum version
    github.com/user/pkg v0.0.0-...-... // Commit hash
)
```

### Rust

```toml
# Cargo.toml
[dependencies]
package = "1.2.3"           # ^1.2.3 (caret by default)
package = "~1.2.3"          # >=1.2.3 <1.3.0
package = ">=1.2.0, <2.0"   # Range
package = "*"               # Latest (avoid!)
```

---

## Breaking Changes

### What Constitutes a Breaking Change?

**Breaking Changes (MAJOR bump)**:
- Removing or renaming public API
- Changing function signatures
- Removing configuration options
- Changing default behavior
- Upgrading major dependencies
- Database schema changes requiring migration
- Changed error codes/messages that clients depend on

**Not Breaking Changes**:
- Adding new features
- Adding new optional parameters
- Fixing bugs
- Performance improvements
- Internal refactoring
- Deprecation warnings (with backward compatibility)
- Documentation updates

### Breaking Change Examples

**API Changes**
```javascript
// Before (v1.x.x)
function getUser(id) { }

// After (v2.0.0) - BREAKING
function getUser(id, options) { }  // Added required parameter

// After (v1.1.0) - NOT breaking
function getUser(id, options = {}) { }  // Added optional parameter
```

**Configuration Changes**
```yaml
# Before (v1.x.x)
config:
  timeout: 5000

# After (v2.0.0) - BREAKING
config:
  timeoutMs: 5000  # Renamed field

# After (v1.1.0) - NOT breaking (with deprecation)
config:
  timeout: 5000        # Deprecated but still works
  timeoutMs: 5000      # New preferred field
```

### Communicating Breaking Changes

```markdown
## [2.0.0] - 2024-11-08

### BREAKING CHANGES

- **Authentication**: Switched from API keys to OAuth2
  - **Migration**: See [migration guide](docs/migration-v2.md)
  - **Timeline**: Support for API keys ends 2024-12-31

- **Database**: User model restructured
  - `name` field split into `firstName` and `lastName`
  - **Migration**: Run `npm run migrate` to update database

- **API**: Removed deprecated endpoints
  - `/api/v1/users` → Use `/api/v2/users` instead
  - `/api/stats` → No replacement (use analytics service)

### Migration Guide

1. Update authentication to OAuth2:
   ```javascript
   // Old
   const client = new API({ apiKey: 'xxx' });

   // New
   const client = new API({ oauthToken: 'xxx' });
   ```

2. Update database schema:
   ```bash
   npm run migrate:v2
   ```

3. Update API endpoints:
   ```javascript
   // Old
   await fetch('/api/v1/users');

   // New
   await fetch('/api/v2/users');
   ```
```

---

## Pre-release Versions

### Format

```
1.2.3-alpha.1
1.2.3-beta.2
1.2.3-rc.3

MAJOR.MINOR.PATCH-prerelease.number
```

### Pre-release Stages

| Stage | Purpose | Stability | Audience |
|-------|---------|-----------|----------|
| **alpha** | Early testing | Unstable | Developers |
| **beta** | Feature complete | Moderate | Early adopters |
| **rc** | Release candidate | Stable | QA testing |

### Examples

```
Development: 1.0.0-alpha.1 → 1.0.0-alpha.2 → 1.0.0-alpha.3
Beta: 1.0.0-beta.1 → 1.0.0-beta.2
RC: 1.0.0-rc.1 → 1.0.0-rc.2
Release: 1.0.0
```

### Creating Pre-releases

```bash
# Commit to beta branch
git checkout beta
git commit -m "feat: add new feature"
git push origin beta

# semantic-release creates: 1.0.0-beta.1
```

### Branch Strategy for Pre-releases

```
main/master  → 1.0.0, 1.1.0, 2.0.0 (stable)
next         → 1.1.0-next.1, 1.1.0-next.2 (preview)
beta         → 1.0.0-beta.1, 1.0.0-beta.2 (testing)
alpha        → 1.0.0-alpha.1, 1.0.0-alpha.2 (experimental)
```

---

## Tools & Configuration

### semantic-release (JavaScript/Node.js)

```bash
# Install
npm install --save-dev semantic-release

# Configuration in .releaserc.json (already provided)

# Run manually
npx semantic-release

# Dry run (no publish)
npx semantic-release --dry-run
```

### python-semantic-release (Python)

```bash
# Install
pip install python-semantic-release

# Configuration in pyproject.toml
[tool.semantic_release]
version_variable = "src/__init__.py:__version__"
branch = "main"
upload_to_pypi = true
upload_to_release = true
build_command = "pip install build && python -m build"

# Run
semantic-release publish
```

### GoReleaser (Go)

```yaml
# .goreleaser.yml
version: 1
builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - windows
      - darwin
    goarch:
      - amd64
      - arm64

# Run
goreleaser release --clean
```

### Cargo (Rust)

```bash
# Bump version
cargo bump patch
cargo bump minor
cargo bump major

# Publish to crates.io
cargo publish
```

---

## Version Files by Language

### JavaScript/TypeScript
```json
// package.json
{
  "name": "my-package",
  "version": "1.2.3"
}
```

### Python
```toml
# pyproject.toml
[project]
name = "my-package"
version = "1.2.3"
```

```python
# src/__init__.py
__version__ = "1.2.3"
```

### Go
```go
// version.go
package main

const Version = "1.2.3"
```

### Rust
```toml
# Cargo.toml
[package]
name = "my-package"
version = "1.2.3"
```

---

## Best Practices

### DO [x]

1. **Use Conventional Commits**: Enables automation
2. **Document Breaking Changes**: Always include migration guides
3. **Test Before Release**: Use pre-release versions
4. **Keep CHANGELOG**: Auto-generated is fine, but review it
5. **Pin Dependencies**: Use lock files
6. **Communicate**: Announce major releases
7. **Support Old Versions**: At least one major version back
8. **Version Everything**: APIs, schemas, configs

### DON'T [ ]

1. **Skip Versions**: Don't jump from 1.0 to 3.0
2. **Rewrite History**: Don't change published versions
3. **Break Minor/Patch**: Only MAJOR should break
4. **Use 0.x Forever**: Release 1.0 when stable
5. **Ignore Dependencies**: Update them regularly
6. **Rush Major Versions**: Plan breaking changes
7. **Forget Deprecation**: Warn before removing

---

## Troubleshooting

### No Release Created

**Problem**: Commits pushed but no release created

**Solution**: Check commit messages follow conventional format
```bash
# View commits
git log --oneline

# Check for feat/fix/BREAKING
# All commits must follow convention
```

### Wrong Version Bumped

**Problem**: Expected MAJOR but got MINOR

**Solution**: Ensure BREAKING CHANGE is in commit
```bash
# Correct format
git commit -m "feat!: major change"

# Or with footer
git commit -m "feat: major change

BREAKING CHANGE: This breaks everything"
```

### Release Failed

**Problem**: semantic-release fails during publish

**Solution**: Check tokens and permissions
```bash
# Verify GITHUB_TOKEN has permissions
# Settings → Actions → General → Workflow permissions
# Set to: "Read and write permissions"
```

---

## Quick Reference

```bash
# Version bumps based on commits
fix: bug → 1.0.0 to 1.0.1 (PATCH)
feat: new feature → 1.0.0 to 1.1.0 (MINOR)
feat!: breaking → 1.0.0 to 2.0.0 (MAJOR)

# Check what next version will be
npx semantic-release --dry-run

# View current version
npm version  # or
cat package.json | grep version

# Manual version bump (not recommended with semantic-release)
npm version patch  # 1.0.0 → 1.0.1
npm version minor  # 1.0.0 → 1.1.0
npm version major  # 1.0.0 → 2.0.0
npm version prerelease --preid=beta  # 1.0.0 → 1.0.1-beta.0
```

---

## Resources

- [Semantic Versioning Specification](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [semantic-release](https://semantic-release.gitbook.io/)
- [python-semantic-release](https://python-semantic-release.readthedocs.io/)
- [GoReleaser](https://goreleaser.com/)
- [Keep a Changelog](https://keepachangelog.com/)

---

**Last Updated**: 2024-11-08
