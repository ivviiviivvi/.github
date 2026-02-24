# Branch Strategy

Comprehensive branching strategy for collaborative development, versioning, and
archival.

## Table of Contents

- [Overview](#overview)
- [Core Branches](#core-branches)
- [Development Branches](#development-branches)
- [Release Branches](#release-branches)
- [Maintenance Branches](#maintenance-branches)
- [Archive Branches](#archive-branches)
- [Branch Lifecycle](#branch-lifecycle)
- [Visual Representation](#visual-representation)
- [Best Practices](#best-practices)

______________________________________________________________________

## Overview

This organization uses a structured branching strategy that supports:

1. **Continuous Development**: Active feature development
1. **Version Management**: Clear version progression
1. **Long-term Support**: Maintenance of older versions
1. **Historical Preservation**: Archival of past work
1. **Collaborative Workflows**: Multiple teams working simultaneously

______________________________________________________________________

## Core Branches

### `main` (or `master`)

**Purpose**: Production-ready, stable code

**Characteristics**:

- Permanent branch
- Protected: highest security level
- Only accepts merges from release and hotfix branches
- Every commit represents a production release
- Tagged with semantic version numbers (v1.0.0, v1.1.0, etc.)
- Automatically deploys to production environment

**Protection Rules**:

```yaml
- Require pull request reviews (2+ approvals)
- Require status checks to pass
- Require signed commits
- Require branch up to date before merging
- Include administrators in restrictions
- No force pushes allowed
- No deletions allowed
```

**Merge Sources**:

- `release/*` branches (normal releases)
- `production/hotfix/*` branches (critical fixes)

______________________________________________________________________

### `develop`

**Purpose**: Integration branch for ongoing development

**Characteristics**:

- Permanent branch
- Contains latest development changes
- Feature branches merge here first
- Automatically deploys to staging environment
- Source for release branches
- Always ahead of main (except immediately after release)

**Protection Rules**:

```yaml
- Require pull request reviews (1+ approval)
- Require status checks to pass
- Require branch up to date before merging
- No force pushes allowed
```

**Merge Sources**:

- `develop/feature/*` branches
- `develop/bugfix/*` branches
- `develop/enhancement/*` branches
- `release/*` branches (backmerge after release)
- `production/hotfix/*` branches (backmerge after hotfix)

______________________________________________________________________

## Development Branches

### Feature Branches

**Naming Convention**: `<lifecycle>/feature/<component>/<subcomponent>`

```bash
develop/feature/authentication/oauth-providers
develop/feature/dashboard/analytics-widget
experimental/feature/ai-assistant/nlp-engine
```

**Purpose**: Develop new features

**Lifecycle**:

1. Created from `develop`
1. Development work happens here
1. Merged back to `develop` via PR
1. Deleted after successful merge

**Best Practices**:

- Keep short-lived (max 2 weeks)
- Sync with develop regularly
- One feature per branch
- Include ticket/issue number in name when applicable

______________________________________________________________________

### Bugfix Branches

**Naming Convention**: `<lifecycle>/bugfix/<issue-description>`

```bash
develop/bugfix/login-timeout-error
maintenance/bugfix/v2.x/memory-leak-fix
```

**Purpose**: Fix non-critical bugs

**Lifecycle**:

1. Created from `develop` (or maintenance branch)
1. Fix implemented and tested
1. Merged back to source branch via PR
1. Deleted after successful merge

______________________________________________________________________

### Enhancement Branches

**Naming Convention**: `<lifecycle>/enhancement/<component>/<improvement>`

```bash
develop/enhancement/api/rate-limiting
production/enhancement/dashboard/performance
```

**Purpose**: Improve existing features without adding new functionality

**Lifecycle**: Same as feature branches

______________________________________________________________________

### Experimental Branches

**Naming Convention**: `experimental/feature/<concept>`

```bash
experimental/feature/blockchain-integration
experimental/feature/quantum-computing-algorithm
```

**Purpose**: Proof-of-concept and research

**Characteristics**:

- High risk, experimental work
- May never merge to develop
- Can be archived if unsuccessful
- Can evolve into regular feature branches if successful

______________________________________________________________________

## Release Branches

**Naming Convention**: `release/v<MAJOR>.<MINOR>.<PATCH>`

```bash
release/v1.2.0
release/v2.0.0
release/v1.5.3
```

**Purpose**: Prepare and stabilize code for production release

**Lifecycle**:

1. Created from `develop` when ready for release
1. Only bug fixes and version bumps allowed
1. No new features
1. Testing and QA happens here
1. Merged to both `main` and `develop`
1. Tagged on main with version number
1. Deleted after successful release

**Activities on Release Branch**:

```bash
# Version bumping
npm version 1.2.0

# Update changelog
# Update documentation
# Final bug fixes only

# Commit message format
git commit -m "chore(release): prepare v1.2.0"
git commit -m "fix(release): resolve last-minute bug"
```

**Merge Process**:

```bash
# 1. Merge to main
git checkout main
git merge --no-ff release/v1.2.0

# 2. Tag release
git tag -a v1.2.0 -m "Release version 1.2.0"

# 3. Push
git push origin main --tags

# 4. Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0

# 5. Cleanup
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

______________________________________________________________________

## Maintenance Branches

**Naming Convention**: `maintenance/v<MAJOR>-maintenance` or
`maintenance/v<MAJOR>.x/<purpose>`

```bash
maintenance/v1-maintenance
maintenance/v2-maintenance
maintenance/v1.x/security-patches
maintenance/v2.x/bug-fixes
```

**Purpose**: Long-term support for previous major versions

**When to Create**:

- When releasing a new major version (v2.0.0, v3.0.0)
- When customers require extended support for older versions
- For LTS (Long Term Support) versions

**Characteristics**:

- Long-lived branches (can exist for years)
- Only accept critical bug fixes and security patches
- No new features ever
- No breaking changes
- Regular patch releases (v1.2.3, v1.2.4, etc.)

**Example Workflow**:

```bash
# When releasing v2.0.0, create maintenance branch for v1.x
git checkout v1.9.5  # Last v1 release tag
git checkout -b maintenance/v1-maintenance
git push -u origin maintenance/v1-maintenance

# Apply security patch
git checkout maintenance/v1-maintenance
git checkout -b maintenance/v1.x/security-openssl-update
# Make changes
git commit -m "fix(security): update OpenSSL to patch CVE-2024-XXXX"

# Merge and tag patch release
git checkout maintenance/v1-maintenance
git merge --no-ff maintenance/v1.x/security-openssl-update
git tag -a v1.9.6 -m "Security patch: OpenSSL update"
git push origin maintenance/v1-maintenance --tags
```

**Maintenance Schedule Examples**:

```
v1.x: Maintained until 2025-12-31
v2.x: Maintained until 2026-12-31
v3.x: Current version, full support
```

______________________________________________________________________

## Archive Branches

**Naming Convention**: `archive/<context>/<descriptive-name>`

```bash
archive/v1/original-implementation
archive/legacy/old-authentication-system
archive/experimental/ml-approach-2023
archive/phase1/mvp-development
archive/deprecated/jquery-frontend
```

**Purpose**: Historical preservation without cluttering active development

**When to Archive**:

1. Old features completely replaced
1. Experimental branches that didn't pan out
1. Legacy code no longer maintained
1. Completed project phases
1. Deprecated implementations

**Archive Process**:

```bash
# Option 1: Rename existing branch
git branch -m old-feature-branch archive/v1/old-feature-implementation
git push origin archive/v1/old-feature-implementation
git push origin --delete old-feature-branch

# Option 2: Create archive branch from specific commit
git checkout -b archive/legacy/jquery-ui-implementation <commit-hash>
git push -u origin archive/legacy/jquery-ui-implementation

# Option 3: Archive with documentation
git checkout old-branch
git checkout -b archive/experimental/failed-blockchain-integration
echo "## Archive Notice

This branch contains an experimental blockchain integration attempted in Q3 2023.
The approach was abandoned in favor of traditional database storage.

**Original Author**: @username
**Date Archived**: 2023-10-15
**Reason**: Performance issues and complexity outweighed benefits
**Replacement**: See develop/feature/storage/postgresql-implementation

For historical context only - do not use in production." > ARCHIVE_README.md

git add ARCHIVE_README.md
git commit -m "docs: add archive documentation"
git push -u origin archive/experimental/failed-blockchain-integration
```

**Archive Guidelines**:

1. Always document why it was archived
1. Never delete - keep for reference
1. Include date and author information
1. Reference replacement solution if applicable
1. Update team documentation with archive notice

______________________________________________________________________

## Branch Lifecycle

### Feature Branch Lifecycle

```
develop
  │
  └─→ develop/feature/component-name ──→ (development) ──→ PR ──→ merge to develop ──→ delete
         │                                                              │
         └──────────── sync regularly ←────────────────────────────────┘
```

**Duration**: 1-14 days typical

______________________________________________________________________

### Release Branch Lifecycle

```
develop ──→ release/v1.2.0 ──→ (stabilization & testing) ──→ merge to main (tag v1.2.0)
                  │                                              │
                  │                                              └──→ merge back to develop
                  │                                                      │
                  └──────────────────────────────────────────────────────→ delete
```

**Duration**: 1-7 days typical

______________________________________________________________________

### Maintenance Branch Lifecycle

```
v1.9.5 (tag) ──→ maintenance/v1-maintenance ──→ (exists indefinitely)
                          │
                          ├──→ maintenance/v1.x/security-patch-1 ──→ merge ──→ tag v1.9.6
                          ├──→ maintenance/v1.x/bug-fix-critical ──→ merge ──→ tag v1.9.7
                          └──→ maintenance/v1.x/security-patch-2 ──→ merge ──→ tag v1.9.8
```

**Duration**: Years (until end-of-life)

______________________________________________________________________

### Archive Branch Lifecycle

```
feature/old-implementation ──→ (development complete) ──→ merged to develop
                                                              │
                                    (later replaced) ──→ archive/v1/old-implementation
                                                              │
                                                          (kept forever)
```

**Duration**: Permanent

______________________________________________________________________

## Visual Representation

### Complete Branch Strategy

```
main/master (production)
  │
  ├── v1.0.0 (tag)
  ├── v1.1.0 (tag)
  │   │
  │   └── maintenance/v1-maintenance ──→ v1.1.1 (tag), v1.1.2 (tag)
  │
  ├── v2.0.0 (tag) ←──── release/v2.0.0 ←──┐
  │                                          │
  └── v2.1.0 (tag) ←──── release/v2.1.0 ←──┤
                                             │
develop ────────────────────────────────────┘
  │
  ├── develop/feature/authentication/oauth
  ├── develop/feature/dashboard/widgets
  ├── develop/bugfix/login-issue
  ├── production/hotfix/critical-security
  │
  └── experimental/feature/ai-integration

archive/
  ├── v1/original-authentication
  ├── legacy/jquery-frontend
  └── experimental/blockchain-2023
```

### Parallel Development Example

```
Time ──────────────────────────────────────────────→

main        ●────────●─────────────●────────────●
           v1.0    v1.1          v2.0         v2.1
                     │             │
maintenance/v1   (created) ●───●───●──→
                         v1.1.1 v1.1.2

develop     ●────────────●─────────────────●──→
             │            │         │       │
feature/A    └──●────●───┘          │       │
feature/B         └──●─────────────┘        │
feature/C                  └───●────────────┘
```

______________________________________________________________________

## Best Practices

### Do's ✅

1. **Keep Branches Short-Lived**: Feature branches should live days, not months
1. **Sync Regularly**: Merge develop into feature branches frequently
1. **Descriptive Names**: `develop/feature/user-auth/oauth-google` not
   `feature/update`
1. **One Purpose Per Branch**: Single feature, fix, or enhancement
1. **Delete After Merge**: Clean up merged branches promptly
1. **Protect Core Branches**: Use branch protection rules
1. **Tag All Releases**: Every production release gets a tag
1. **Document Archives**: Explain why and when branches were archived
1. **Maintain Old Versions**: Create maintenance branches for major versions
1. **Follow Naming Conventions**: Use consistent, hierarchical naming

### Don'ts ❌

1. **Don't Commit Directly to Main**: Always use PR workflow
1. **Don't Keep Stale Branches**: Delete after merge
1. **Don't Mix Features**: One branch per feature
1. **Don't Use Generic Names**: Avoid `fix`, `update`, `test`
1. **Don't Force Push to Shared Branches**: Preserve history
1. **Don't Delete Without Archiving**: Archive before deleting important work
1. **Don't Reuse Branch Names**: Create new branches for new work
1. **Don't Skip Code Review**: All merges require review
1. **Don't Add Features to Release Branches**: Only bug fixes
1. **Don't Break Naming Conventions**: Consistency is key

______________________________________________________________________

## Integration with CI/CD

### Automated Deployments

```yaml
# Example GitHub Actions workflow
on:
  push:
    branches:
      - main # Deploy to production
      - develop # Deploy to staging
      - "maintenance/v*" # Deploy to maintenance environments

  pull_request:
    branches:
      - develop # Preview deployments
      - "maintenance/v*" # Maintenance preview
```

### Automated Versioning

```yaml
# Triggered on tags
on:
  push:
    tags:
      - "v*.*.*" # Semantic version tags

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create GitHub Release
        uses: actions/create-release@v1
```

______________________________________________________________________

## Related Documentation

- [VERSION_CONTROL_STANDARDS.md](../reference/VERSION_CONTROL_STANDARDS.md) -
  Overall version control standards
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Detailed Git workflow
- [SEMANTIC_VERSIONING.md](../reference/SEMANTIC_VERSIONING.md) - Version
  numbering rules
- [RELEASE_PROCESS.md](RELEASE_PROCESS.md) - Creating and managing releases
- [BRANCH_PROTECTION.md](../governance/BRANCH_PROTECTION.md) - Protection rule
  configuration

______________________________________________________________________

**Last Updated**: 2025-11-25
