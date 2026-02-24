# Archival Strategy

Organization-wide strategy for version archival, maintenance branches, and
long-term code preservation.

## Table of Contents

- [Overview](#overview)
- [Archive Branches](#archive-branches)
- [Maintenance Branches](#maintenance-branches)
- [Git Tags for Archival](#git-tags-for-archival)
- [GitHub Releases](#github-releases)
- [Retention Policies](#retention-policies)
- [Retrieval Procedures](#retrieval-procedures)

______________________________________________________________________

## Overview

This document establishes standards for archiving code, maintaining legacy
versions, and ensuring long-term accessibility of historical code.

### Purpose

Archival serves multiple purposes:

1. **Historical Reference**: Preserve code for future reference
1. **Compliance**: Meet regulatory and audit requirements
1. **Recovery**: Enable recovery of old implementations if needed
1. **Learning**: Provide examples of past approaches
1. **Documentation**: Maintain record of project evolution

### Core Principles

1. **Permanent Tags**: Git tags provide immutable version markers
1. **Long-lived Branches**: Maintenance branches for active support
1. **Archive Branches**: Dedicated branches for obsolete code
1. **GitHub Releases**: Formal releases with downloadable artifacts
1. **Clear Naming**: Descriptive names indicate purpose and version

______________________________________________________________________

## Archive Branches

### When to Create Archive Branches

Create archive branches when:

- Version is no longer actively supported
- Major rewrite makes old code obsolete
- Project direction changes significantly
- Migration to new architecture is complete
- Legacy system is being replaced

### Naming Convention

```
archive/[version-identifier]
archive/[system-identifier]

Examples:
archive/v1-archive
archive/v2-archive
archive/legacy-system
archive/old-implementation
archive/deprecated-api
archive/monolith-version
```

**Note**: Square brackets indicate placeholders - replace with actual values.

### Creating Archive Branches

**From Maintenance Branch**:

```bash
# Create archive from maintenance branch
git checkout maintenance/v1-maintenance
git checkout -b archive/v1-archive
git push origin archive/v1-archive

# Add archive notice to README
cat > ARCHIVE_NOTICE.md <<'EOF'
# ARCHIVED

This branch is archived and no longer maintained.
For current version, see main branch.
EOF
git add ARCHIVE_NOTICE.md
git commit -m "docs: add archive notice"
git push origin archive/v1-archive
```

**From Specific Tag**:

```bash
# Create archive from specific release
git checkout v1.9.5
git checkout -b archive/v1-archive
git push origin archive/v1-archive
```

**From Develop or Main**:

```bash
# Archive current state before major change
git checkout main
git checkout -b archive/pre-rewrite-archive
git push origin archive/pre-rewrite-archive
```

### Archive Branch Structure

Archive branches should include:

1. **ARCHIVE_NOTICE.md**: Clear indication of archive status
1. **README.md**: Updated with archive information
1. **Original Code**: Complete code as it was
1. **Documentation**: All relevant documentation
1. **Build Instructions**: How to build archived version

**ARCHIVE_NOTICE.md Template**:

```markdown
# ARCHIVED PROJECT

**Status**: Archived
**Archive Date**: 2024-11-25
**Last Supported Version**: v1.9.5
**Reason**: Superseded by v2.0.0 major rewrite

## Important Information

This branch is archived and is no longer maintained. It is kept for historical reference only.

## Migration Information

To migrate to the current version, see:

- [Migration Guide](docs/migration-v2.md)
- [Current Version](https://github.com/org/repo)

## Getting Help

For support with archived versions:

- Check archived documentation
- Review closed issues
- Contact: support@example.com

## Last Active

- Last Commit: 2024-06-15
- Last Release: v1.9.5
- Support Ended: 2024-11-01
```

### Archive Branch Protection

**Protection Rules**:

- Read-only (no new commits)
- Cannot be deleted
- No force push allowed
- Documented archive status

**GitHub Settings**:

```yaml
Branch Protection:
  - Require pull request reviews: No
  - Require status checks: No
  - Require branches up to date: No
  - Include administrators: Yes
  - Allow force pushes: No
  - Allow deletions: No
```

______________________________________________________________________

## Maintenance Branches

### Purpose

Maintenance branches provide ongoing support for previous major versions while
development continues on newer versions.

### When to Create Maintenance Branches

Create maintenance branches when:

- Releasing a new major version
- Customers require continued support for older versions
- Critical bugs need fixes in production versions
- Security patches required for legacy versions

### Naming Convention

```
maintenance/[version]-maintenance

Examples:
maintenance/v1-maintenance
maintenance/v2-maintenance
maintenance/lts-maintenance
```

### Creating Maintenance Branches

**At Major Release**:

```bash
# Just before releasing v2.0.0
git checkout main
git checkout -b maintenance/v1-maintenance
git push origin maintenance/v1-maintenance

# Continue with v2.0.0 release on main
```

**From Specific Version**:

```bash
# Create maintenance branch from last v1 release
git checkout v1.9.5
git checkout -b maintenance/v1-maintenance
git push origin maintenance/v1-maintenance
```

### Maintenance Workflow

**Applying Fixes**:

```bash
# Create fix branch
git checkout maintenance/v1-maintenance
git pull origin maintenance/v1-maintenance
git checkout -b production/hotfix/security-fix

# Make changes
git add .
git commit -m "fix: security vulnerability CVE-2024-XXXX"

# Create PR to maintenance branch
git push origin production/hotfix/security-fix
# Open PR targeting maintenance/v1-maintenance
```

**Release from Maintenance**:

```bash
# After PR merged
git checkout maintenance/v1-maintenance
git pull origin maintenance/v1-maintenance

# Tag new patch version
git tag -a v1.9.6 -m "Security fix release"
git push origin v1.9.6

# Create GitHub Release
gh release create v1.9.6 --notes "Security fix for CVE-2024-XXXX"
```

**Backporting from Main**:

```bash
# Cherry-pick commit from main
git checkout maintenance/v1-maintenance
git cherry-pick <commit-hash>
git push origin maintenance/v1-maintenance
```

### Maintenance Support Levels

**Active Support**:

- Bug fixes
- Security patches
- Documentation updates
- Customer support

**Limited Support**:

- Critical security patches only
- No feature development
- Limited customer support

**End of Life**:

- No updates
- Archive branch created
- Documentation remains available

### Support Timeline Example

```
v1.0.0 Released: 2022-01-01
v2.0.0 Released: 2023-01-01
  └─ v1 enters maintenance mode

v1 Active Support: 2023-01-01 to 2024-01-01 (1 year)
  └─ Bug fixes and security patches

v1 Limited Support: 2024-01-01 to 2024-07-01 (6 months)
  └─ Critical security patches only

v1 End of Life: 2024-07-01
  └─ Create archive/v1-archive
  └─ Delete maintenance/v1-maintenance (optional)
```

______________________________________________________________________

## Git Tags for Archival

### Purpose

Git tags provide immutable markers for specific versions, enabling easy
retrieval.

### Tag Types

**Release Tags**:

```
v1.0.0, v1.0.1, v1.1.0, v2.0.0
```

**Pre-release Tags**:

```
v1.0.0-alpha.1, v1.0.0-beta.1, v1.0.0-rc.1
```

**Archive Tags**:

```
archive/v1-final
archive/pre-migration
```

### Creating Archive Tags

**Mark Final Version Before Archive**:

```bash
git checkout maintenance/v1-maintenance
git tag -a archive/v1-final -m "Final v1 release before archival"
git push origin archive/v1-final
```

**Mark Pre-Migration State**:

```bash
git checkout main
git tag -a archive/pre-migration -m "State before v2 migration"
git push origin archive/pre-migration
```

### Retrieving Tagged Versions

**Checkout Tagged Version**:

```bash
git checkout v1.9.5
```

**Create Branch from Tag**:

```bash
git checkout v1.9.5
git checkout -b hotfix-from-v1.9.5
```

**View Tag Information**:

```bash
git show v1.9.5
git tag -l "v1.*"
```

______________________________________________________________________

## GitHub Releases

### Purpose

GitHub Releases provide:

- Clean version downloads
- Release notes
- Compiled artifacts
- Documentation snapshots
- Migration guides

### Creating Releases

**For Current Version**:

```bash
# Via GitHub CLI
gh release create v1.2.3 \
  --title "Release v1.2.3" \
  --notes "See CHANGELOG.md for details" \
  --latest

# With artifacts
gh release create v1.2.3 \
  --title "Release v1.2.3" \
  --notes "$(cat CHANGELOG.md)" \
  dist/*.zip \
  dist/*.tar.gz
```

**For Archived Version**:

```bash
gh release create v1.9.5 \
  --title "Final Release v1.9.5 (Archived)" \
  --notes "This is the final release of v1.x. Support has ended." \
  --prerelease
```

### Release Assets

Include these assets in releases:

1. Source code (automatic)
1. Compiled binaries
1. Documentation (PDF or HTML)
1. CHANGELOG.md
1. Migration guides
1. License file

### Release Notes Template

````markdown
## Release v1.2.3

**Release Date**: 2024-11-25
**Support Status**: Active

### Features

- Feature description

### Bug Fixes

- Bug fix description

### Breaking Changes

None

### Upgrade Instructions

```bash
git pull origin main
git checkout v1.2.3
npm install
```
````

### Documentation

- [Installation Guide](docs/installation.md)
- [Migration Guide](docs/migration.md)

### Support

This release is actively supported. Report issues at:
https://github.com/org/repo/issues

````

**Archived Version Template**:
```markdown
## Release v1.9.5 (Final v1.x Release)

**Release Date**: 2024-06-15
**Archive Date**: 2024-11-25
**Support Status**: End of Life

### Important Notice

This is the final release of the v1.x series. Support has ended as of 2024-11-01.

For current versions, see v2.x releases.

### Migration

To upgrade to v2.x:
- See [Migration Guide](docs/migration-v2.md)
- Current version: v2.3.0

### Historical Information

This release is preserved for:
- Historical reference
- Legacy system support
- Compliance requirements

### Getting Help

For archived version support:
- Review archived documentation
- Check closed issues
- Contact: legacy-support@example.com
````

______________________________________________________________________

## Retention Policies

### Branch Retention

| Branch Type    | Retention Period          | Deletion Policy         |
| -------------- | ------------------------- | ----------------------- |
| main/master    | Permanent                 | Never delete            |
| develop        | Permanent                 | Never delete            |
| feature/\*     | 30 days after merge       | Auto-delete after merge |
| hotfix/\*      | 30 days after merge       | Auto-delete after merge |
| release/\*     | 30 days after merge       | Auto-delete after merge |
| maintenance/\* | Support period + 6 months | Delete after archival   |
| archive/\*     | Permanent                 | Never delete            |

### Tag Retention

| Tag Type           | Retention Period |
| ------------------ | ---------------- |
| Release tags (v\*) | Permanent        |
| Pre-release tags   | Permanent        |
| Archive tags       | Permanent        |

### Release Retention

| Release Type           | Retention Period               |
| ---------------------- | ------------------------------ |
| Current major version  | Permanent                      |
| Previous major version | 2 years after EOL              |
| Older versions         | Permanent (marked as archived) |

### Artifact Retention

| Artifact Type     | Retention Period          |
| ----------------- | ------------------------- |
| Source code       | Permanent (in Git)        |
| Compiled binaries | 2 years after version EOL |
| Documentation     | Permanent                 |
| Build logs        | 90 days                   |
| Test reports      | 1 year                    |

______________________________________________________________________

## Retrieval Procedures

### Retrieving Archived Code

**By Tag**:

```bash
# List all tags
git tag -l

# Checkout specific version
git checkout v1.9.5

# Create working branch from tag
git checkout v1.9.5
git checkout -b restore-v1.9.5
```

**By Archive Branch**:

```bash
# List archive branches
git branch -r | grep archive

# Checkout archive branch
git checkout archive/v1-archive

# Create working branch from archive
git checkout archive/v1-archive
git checkout -b restore-from-archive
```

**By Release**:

```bash
# Download from GitHub Releases
gh release download v1.9.5

# Or via web
# Navigate to: https://github.com/org/repo/releases/tag/v1.9.5
```

### Searching Historical Code

**Find When File Was Deleted**:

```bash
git log --all --full-history -- path/to/file
```

**Find Specific Code in History**:

```bash
git log -S "search term" --all
```

**View File at Specific Version**:

```bash
git show v1.9.5:path/to/file
```

**Compare Versions**:

```bash
git diff v1.9.5 v2.0.0
git diff v1.9.5 v2.0.0 -- specific/file
```

### Building Archived Versions

**Prerequisites**:

1. Check ARCHIVE_NOTICE.md for requirements
1. Review archived documentation
1. Ensure compatible build environment

**Build Process**:

```bash
# Checkout archived version
git checkout archive/v1-archive

# Install dependencies (versions specified in archive)
npm install  # or pip install -r requirements.txt

# Build
npm run build  # or python setup.py build

# Test
npm test  # or pytest
```

______________________________________________________________________

## Compliance and Auditing

### Audit Trail

Git provides complete audit trail:

- Every change is tracked
- Author and timestamp recorded
- Commit messages explain changes
- Tags mark official releases

### Compliance Requirements

Ensure archived code meets:

- Regulatory retention periods
- Industry standards
- Company policies
- Legal requirements

### Documentation Requirements

Maintain for archived versions:

- Source code
- Build instructions
- Deployment procedures
- Configuration documentation
- API documentation
- Known issues
- Security advisories

______________________________________________________________________

## Best Practices

### Before Archiving

- [ ] Ensure all fixes are applied
- [ ] Create final release
- [ ] Update documentation
- [ ] Add ARCHIVE_NOTICE.md
- [ ] Update README with archive status
- [ ] Notify users of archival
- [ ] Document migration path
- [ ] Tag final version
- [ ] Create GitHub Release

### During Archival

- [ ] Create archive branch
- [ ] Set branch protection
- [ ] Mark as archived on GitHub
- [ ] Update project website
- [ ] Close milestone
- [ ] Close version-specific issues
- [ ] Update support documentation

### After Archival

- [ ] Verify all artifacts preserved
- [ ] Test retrieval procedures
- [ ] Document lessons learned
- [ ] Update organizational records
- [ ] Monitor for security issues
- [ ] Maintain emergency contact

______________________________________________________________________

## Quick Reference

### Create Archive Branch

```bash
git checkout maintenance/v1-maintenance
git checkout -b archive/v1-archive
echo "# ARCHIVED" > ARCHIVE_NOTICE.md
git add ARCHIVE_NOTICE.md
git commit -m "docs: mark as archived"
git push origin archive/v1-archive
```

### Create Maintenance Branch

```bash
git checkout v1.9.5
git checkout -b maintenance/v1-maintenance
git push origin maintenance/v1-maintenance
```

### Tag for Archival

```bash
git tag -a archive/v1-final -m "Final v1 before archival"
git push origin archive/v1-final
```

### Retrieve Archived Version

```bash
git checkout archive/v1-archive
# or
git checkout v1.9.5
# or
gh release download v1.9.5
```

______________________________________________________________________

**Last Updated**: 2024-11-25
