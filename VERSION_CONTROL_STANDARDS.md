# Version Control Standards

Organization-wide standards for version control, branching, tagging, and release management.

## Table of Contents

- [Overview](#overview)
- [Semantic Versioning](#semantic-versioning)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Standards](#commit-message-standards)
- [Tagging Strategy](#tagging-strategy)
- [Release Management](#release-management)
- [Maintenance and Archival](#maintenance-and-archival)

---

## Overview

This document establishes organization-wide standards for version control practices. These standards ensure consistency, traceability, and clarity across all repositories.

### Core Principles

1. **Git History as Version Trail**: The Git commit history serves as the detailed version trail
2. **Semantic Versioning**: Use tags for releases following semver (v1.0.0, v1.0.1, v1.1.0)
3. **Descriptive Branching**: Branch names visually communicate development phase and purpose
4. **Conventional Commits**: Structured commit messages enable automated tooling
5. **Automated Releases**: Tools auto-increment versions based on commit analysis

---

## Semantic Versioning

### Version Format

```
MAJOR.MINOR.PATCH

Example: v1.2.3
```

- **MAJOR**: Incompatible API changes, breaking changes
- **MINOR**: New features, backward compatible functionality
- **PATCH**: Bug fixes, backward compatible corrections

### Version Examples

```
v0.1.0  - Initial development
v0.2.0  - Added new feature
v0.2.1  - Fixed bug
v1.0.0  - First stable release
v1.1.0  - Added backward-compatible feature
v1.1.1  - Fixed bug
v2.0.0  - Breaking API change
```

### Pre-release Versions

Pre-release versions follow this format:

```
MAJOR.MINOR.PATCH-prerelease.number

Examples:
v1.2.3-alpha.1
v1.2.3-beta.2
v1.2.3-rc.1
```

**Pre-release Stages**:
- **alpha**: Early testing, unstable, for developers
- **beta**: Feature complete, moderate stability, for early adopters
- **rc** (release candidate): Stable, for QA testing

### Version Increment Decision Tree

```
Is it a breaking change?
├─ YES → Increment MAJOR version
└─ NO → Is it a new feature?
    ├─ YES → Increment MINOR version
    └─ NO → Is it a bug fix?
        ├─ YES → Increment PATCH version
        └─ NO → No version change (documentation, chores)
```

---

## Branch Naming Conventions

### Branch Hierarchy Format

Branches follow a hierarchical naming structure that visually represents the order and purpose of development.

**Template**: `lifecycle-phase/type/descriptive-name`

**Note**: Square brackets [ ] in documentation indicate placeholders that should be replaced with actual values.

### Product Lifecycle Phases

Use these lifecycle phase prefixes to indicate the maturity and purpose:

1. **exploration/** - Experimental features, proof of concepts
2. **development/** - Active feature development
3. **testing/** - Features in testing phase
4. **staging/** - Features ready for staging environment
5. **production/** - Production-ready features (typically merged to main)
6. **maintenance/** - Long-term maintenance branches
7. **archive/** - Archived branches for historical reference

### Branch Type Indicators

Within lifecycle phases, use these type indicators:

- **feature/** - New features or enhancements
- **fix/** - Bug fixes
- **hotfix/** - Critical production fixes
- **release/** - Release preparation
- **refactor/** - Code refactoring
- **docs/** - Documentation updates
- **test/** - Test-related changes
- **chore/** - Maintenance tasks

### Branch Naming Examples

**Good Examples**:
```
development/feature/user-authentication
development/feature/payment-integration/stripe-setup
testing/feature/dashboard-redesign
maintenance/v1-maintenance
maintenance/v2-maintenance
exploration/feature/ai-integration/model-testing
production/hotfix/critical-security-fix
staging/release/v2.1.0
archive/v1-legacy
```

**Avoid These**:
```
v2                          # Use: development/feature/v2-redesign
update                      # Use: development/feature/specific-update-name
john-branch                 # Use: development/feature/descriptive-name
feature-123                 # Use: development/feature/ticket-123-description
```

### Branch Lifecycle Flow

```
exploration/feature/new-idea
    ↓
development/feature/new-idea
    ↓
testing/feature/new-idea
    ↓
staging/release/v1.2.0
    ↓
main (tagged as v1.2.0)
    ↓
maintenance/v1-maintenance (if needed)
    ↓
archive/v1-archive (when obsolete)
```

### Long-lived Branches

**Main Branches**:
- `main` or `master` - Production code, always stable
- `develop` - Integration branch for features

**Maintenance Branches**:
- `maintenance/v1-maintenance` - Support for v1.x releases
- `maintenance/v2-maintenance` - Support for v2.x releases

**Archive Branches**:
- `archive/v1-archive` - Archived v1 code for reference
- `archive/legacy-system` - Old systems preserved for history

---

## Commit Message Standards

### Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type | Description | Version Impact |
|------|-------------|----------------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation only | PATCH |
| `style` | Code style (formatting) | PATCH |
| `refactor` | Code refactoring | PATCH |
| `perf` | Performance improvement | PATCH |
| `test` | Adding or updating tests | PATCH |
| `build` | Build system changes | PATCH |
| `ci` | CI/CD changes | PATCH |
| `chore` | Maintenance tasks | No bump |
| `revert` | Revert previous commit | PATCH |

### Breaking Changes

Breaking changes trigger a MAJOR version bump. Indicate them using:

**Method 1: Exclamation mark**
```
feat!: redesign authentication API
fix!: change response format
```

**Method 2: Footer**
```
feat: redesign authentication API

BREAKING CHANGE: Authentication now requires OAuth2.
API keys are no longer supported.
```

### Commit Message Examples

**Simple commit**:
```
feat: add user authentication
```

**With scope**:
```
feat(auth): implement OAuth2 login
fix(api): resolve timeout in user service
docs(readme): update installation instructions
```

**With body and footer**:
```
fix(database): resolve race condition in user creation

The race condition occurred when multiple users were created
simultaneously. This fix implements a database lock to prevent
duplicate user creation.

Closes #123
Fixes #456
```

**Breaking change**:
```
feat(api)!: change response format for /users endpoint

BREAKING CHANGE: The /users endpoint now returns an array
instead of an object. Update all clients accordingly.

Migration guide: docs/migration-v2.md
```

### Commit Message Guidelines

**Subject Line**:
- Maximum 50 characters
- Imperative mood ("add" not "added")
- No period at the end
- Capitalize first letter
- Descriptive and specific

**Body** (optional):
- Wrap at 72 characters
- Explain what and why, not how
- Separate from subject with blank line
- Can have multiple paragraphs

**Footer** (optional):
- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-authored-by: Name <email>`

---

## Tagging Strategy

### Tag Format

Tags follow semantic versioning with a `v` prefix:

```
v[MAJOR].[MINOR].[PATCH]

Examples:
v1.0.0
v1.2.3
v2.0.0
```

### Creating Tags

**Annotated Tags** (recommended):
```bash
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

**Lightweight Tags** (not recommended):
```bash
git tag v1.2.3
git push origin v1.2.3
```

### Tag Annotations

Tag messages should include:
- Version number
- Release date
- Brief description of changes
- Link to changelog

Example:
```bash
git tag -a v1.2.3 -m "Release v1.2.3 (2024-11-25)

Features:
- User authentication system
- Dashboard redesign

Bug Fixes:
- Memory leak in data processor
- API timeout issues

See CHANGELOG.md for full details"
```

### Pre-release Tags

```bash
git tag -a v1.2.3-alpha.1 -m "Alpha release for testing"
git tag -a v1.2.3-beta.1 -m "Beta release for early adopters"
git tag -a v1.2.3-rc.1 -m "Release candidate for v1.2.3"
```

---

## Release Management

### Automated Releases

Releases are automatically created based on conventional commits using semantic-release.

**Process**:
1. Commits are analyzed for type (feat, fix, BREAKING CHANGE)
2. Next version is calculated based on commit types
3. CHANGELOG.md is automatically generated
4. Git tag is created
5. GitHub Release is published
6. Packages are published (if configured)

### Manual Release Process

For manual releases:

1. **Create Release Branch**:
```bash
git checkout develop
git pull origin develop
git checkout -b staging/release/v1.2.0
```

2. **Prepare Release**:
```bash
# Update version files
# Update CHANGELOG.md
# Final testing
git add .
git commit -m "chore(release): prepare v1.2.0"
```

3. **Merge to Main**:
```bash
git checkout main
git merge --no-ff staging/release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags
```

4. **Merge Back to Develop**:
```bash
git checkout develop
git merge --no-ff staging/release/v1.2.0
git push origin develop
```

5. **Cleanup**:
```bash
git branch -d staging/release/v1.2.0
git push origin --delete staging/release/v1.2.0
```

### Release Notes

Each release should include:
- Version number
- Release date
- Summary of changes
- New features
- Bug fixes
- Breaking changes (if any)
- Migration guide (for breaking changes)
- Known issues
- Contributors

### GitHub Releases

GitHub Releases provide clean version downloads for non-technical stakeholders:

- Source code (zip and tar.gz)
- Compiled binaries (if applicable)
- CHANGELOG.md
- Documentation
- Migration guides

---

## Maintenance and Archival

### Maintenance Branches

Create maintenance branches for long-term support of major versions:

**When to Create**:
- After releasing a new major version
- When continued support is needed for previous version
- When customers require stability for older versions

**Naming Convention**:
```
maintenance/v1-maintenance
maintenance/v2-maintenance
```

**Workflow**:
```bash
# Create maintenance branch from last v1 release
git checkout v1.9.5
git checkout -b maintenance/v1-maintenance
git push origin maintenance/v1-maintenance

# Apply hotfix
git checkout -b production/hotfix/security-fix maintenance/v1-maintenance
# Make changes
git commit -m "fix: security vulnerability"
git checkout maintenance/v1-maintenance
git merge --no-ff production/hotfix/security-fix
git tag -a v1.9.6 -m "Hotfix v1.9.6"
git push origin maintenance/v1-maintenance --tags
```

### Archive Branches

Archive old versions for historical reference:

**When to Archive**:
- Version is no longer supported
- Major rewrite makes old code obsolete
- Project direction changes significantly

**Naming Convention**:
```
archive/v1-archive
archive/legacy-system
archive/old-implementation
```

**Workflow**:
```bash
# Create archive branch
git checkout maintenance/v1-maintenance
git checkout -b archive/v1-archive
git push origin archive/v1-archive

# Optional: Delete maintenance branch
git push origin --delete maintenance/v1-maintenance
git branch -d maintenance/v1-maintenance
```

### Branch Retention Policy

**Retention Guidelines**:
- **main/master**: Permanent
- **develop**: Permanent
- **feature branches**: Delete after merge
- **release branches**: Delete after merge
- **hotfix branches**: Delete after merge
- **maintenance branches**: Keep for support period (1-2 years)
- **archive branches**: Permanent (for reference)

---

## Git History as Version Trail

### Philosophy

The Git commit history is the authoritative record of all changes. Each commit represents a discrete change with:
- What changed (files and code via diffs)
- Why it changed (commit message explaining the purpose)
- When it changed (timestamp)
- Who changed it (author)

The complete version trail includes both the commit messages and the actual code changes (diffs) in the Git history.

### Best Practices

**Atomic Commits**:
- Each commit should represent one logical change
- Commits should be complete and functional
- Don't mix unrelated changes

**Commit Frequency**:
- Commit often to capture progress
- Don't wait until end of day
- Create checkpoints at logical stages

**Commit Clarity**:
- Write clear, descriptive commit messages
- Include context in the body
- Reference issues and tickets

**History Cleanliness**:
- Avoid "WIP" or "fix typo" commits in main branches
- Use interactive rebase to clean up feature branch history
- Squash related commits before merging (if appropriate)

### Viewing History

```bash
# View commit history
git log --oneline --graph --all

# View history for specific file
git log --follow -- path/to/file

# View history with diffs
git log -p

# View history by author
git log --author="Name"

# View history by date range
git log --since="2024-01-01" --until="2024-12-31"

# Find when a line was changed
git blame path/to/file
```

---

## Quick Reference

### Branch Naming Template

```
[lifecycle-phase]/[type]/[descriptive-name]

Examples:
development/feature/user-authentication
testing/feature/payment-gateway
maintenance/v2-maintenance
archive/v1-archive
```

### Commit Message Template

```
<type>(<scope>): <subject>

<body>

<footer>

Examples:
feat(auth): add OAuth2 support
fix: resolve memory leak
docs: update API documentation
```

### Tagging Template

```
v<MAJOR>.<MINOR>.<PATCH>[-prerelease.number]

Examples:
v1.0.0
v1.2.3
v2.0.0-beta.1
```

---

## Compliance Checklist

- [ ] All releases use semantic versioning (v1.0.0 format)
- [ ] Branch names follow lifecycle/type/description format
- [ ] Commit messages follow conventional commits format
- [ ] Git history is clean and descriptive
- [ ] Tags are created for all releases
- [ ] CHANGELOG.md is maintained and updated
- [ ] Maintenance branches exist for supported versions
- [ ] Old versions are archived when no longer supported
- [ ] GitHub Releases are created for each version
- [ ] Documentation reflects current version

---

**Last Updated**: 2024-11-25
