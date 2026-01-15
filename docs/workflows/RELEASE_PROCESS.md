# Release Process

Comprehensive guide for creating, managing, and distributing releases with
automated workflows.

## Table of Contents

- [Overview](#overview)
- [Release Types](#release-types)
- [Automated Release System](#automated-release-system)
- [GitHub Releases](#github-releases)
- [Release Artifacts](#release-artifacts)
- [Current Version Documentation](#current-version-documentation)
- [Stakeholder Communication](#stakeholder-communication)
- [Release Checklist](#release-checklist)
- [Rollback Procedures](#rollback-procedures)

---

## Overview

This organization uses an automated release management system that:

1. **Generates releases** automatically based on conventional commits
1. **Creates downloadable artifacts** for each release
1. **Updates documentation** with current version information
1. **Notifies stakeholders** of new releases
1. **Maintains comprehensive changelog** with full history

---

## Release Types

### Production Releases

**Format**: `v<MAJOR>.<MINOR>.<PATCH>`

```
v1.0.0
v1.1.0
v1.2.3
v2.0.0
```

**Created from**: `main` branch via `release/*` branch merge

**Deployment**: Automatically deployed to production

**Artifacts**: Full distribution packages, binaries, documentation

---

### Pre-release Versions

**Alpha Releases** - Early development, unstable

```
v1.0.0-alpha.1
v1.0.0-alpha.2
```

**Beta Releases** - Feature complete, testing phase

```
v1.0.0-beta.1
v1.0.0-beta.2
```

**Release Candidates** - Final testing before production

```
v1.0.0-rc.1
v1.0.0-rc.2
```

**Created from**: Respective pre-release branches

**Deployment**: To pre-release environments only

**Artifacts**: Testing packages, not for production use

---

### Patch Releases

**Format**: `v<MAJOR>.<MINOR>.<PATCH>` (increment PATCH)

```
v1.2.3 → v1.2.4
```

**Purpose**: Bug fixes, security patches

**Created from**: Hotfix branches or maintenance branches

**Timeline**: As needed, often urgent

---

### Feature Releases

**Format**: `v<MAJOR>.<MINOR>.<PATCH>` (increment MINOR)

```
v1.2.0 → v1.3.0
```

**Purpose**: New features, enhancements

**Created from**: Regular release process

**Timeline**: Scheduled (e.g., monthly, quarterly)

---

### Major Releases

**Format**: `v<MAJOR>.<MINOR>.<PATCH>` (increment MAJOR)

```
v1.9.0 → v2.0.0
```

**Purpose**: Breaking changes, major overhauls

**Created from**: Carefully planned release process

**Timeline**: Planned well in advance with migration guides

---

## Automated Release System

### semantic-release Configuration

Our automated release system uses `semantic-release` configured in
`.releaserc.json`.

**Automatic Actions**:

1. **Analyzes commits** since last release
1. **Determines version bump** (MAJOR, MINOR, PATCH)
1. **Generates changelog** entries
1. **Updates version** in package files
1. **Creates git tag** with version number
1. **Generates GitHub Release** with notes
1. **Publishes packages** to registries (if configured)
1. **Commits changes** back to repository

### Trigger Conditions

Releases are triggered when:

- Commits are pushed to `main` or `master` branch
- Commits follow conventional commit format
- CI checks pass successfully

### Version Determination

```bash
# Based on commit types since last release:
fix: bug         → PATCH (1.0.0 → 1.0.1)
feat: feature    → MINOR (1.0.0 → 1.1.0)
feat!: breaking  → MAJOR (1.0.0 → 2.0.0)

# Or with footer:
BREAKING CHANGE  → MAJOR (1.0.0 → 2.0.0)
```

### Workflow Example

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches:
      - main
      - master

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: "lts/*"

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Semantic Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

---

## GitHub Releases

### Creating GitHub Releases

**Automatically Created** by semantic-release with:

- Release title (e.g., "v1.2.0")
- Comprehensive release notes
- Downloadable source code archives
- Custom release artifacts
- Links to changelog

### Release Notes Format

Automatically generated release notes include:

```markdown
## [1.2.0] - 2025-11-25

### Features

- Add user authentication with OAuth2 (#123)
- Implement dashboard analytics widget (#124)
- Add export functionality for reports (#125)

### Bug Fixes

- Fix memory leak in data processor (#126)
- Resolve login timeout issue (#127)

### Documentation

- Update API documentation (#128)
- Add migration guide for v1 to v2 (#129)

### BREAKING CHANGES

- Authentication API redesigned to use OAuth2 tokens
  - Migration guide: docs/migration-v2.md
  - Old API keys deprecated, support ends 2026-01-31

### Contributors

@user1, @user2, @user3

**Full Changelog**: https://github.com/org/repo/compare/v1.1.0...v1.2.0
```

### Manual Release Notes Enhancement

While automatic generation is primary, you can enhance release notes:

```bash
# After automatic release is created, edit on GitHub:
1. Go to Releases page
2. Click "Edit" on latest release
3. Add:
   - High-level summary
   - Screenshots/demos
   - Migration instructions
   - Known issues
   - Special thanks
```

---

## Release Artifacts

### Artifact Types

**Source Archives** (automatic)

- `source.tar.gz` - Complete source code
- `source.zip` - Complete source code

**Distribution Packages**

- `package.tgz` - npm package
- `dist.zip` - Built distribution
- `binary-linux-amd64` - Linux binary
- `binary-darwin-arm64` - macOS ARM binary
- `binary-windows-amd64.exe` - Windows binary

**Documentation**

- `documentation.pdf` - Complete documentation
- `CHANGELOG.md` - Version changelog
- `API-docs.zip` - API documentation

### Configuring Artifacts

In `.releaserc.json`:

```json
{
  "plugins": [
    [
      "@semantic-release/github",
      {
        "assets": [
          {
            "path": "dist/*.tgz",
            "label": "NPM Package"
          },
          {
            "path": "dist/binaries/*",
            "label": "Binary Distribution"
          },
          {
            "path": "CHANGELOG.md",
            "label": "Changelog"
          },
          {
            "path": "docs/api/*.pdf",
            "label": "API Documentation"
          }
        ]
      }
    ]
  ]
}
```

### Build Artifacts

**In CI/CD Pipeline**:

```yaml
- name: Build distribution
  run: |
    npm run build
    npm pack
    mv *.tgz dist/

- name: Build binaries
  run: |
    # Build for multiple platforms
    GOOS=linux GOARCH=amd64 go build -o dist/app-linux-amd64
    GOOS=darwin GOARCH=arm64 go build -o dist/app-darwin-arm64
    GOOS=windows GOARCH=amd64 go build -o dist/app-windows-amd64.exe

- name: Generate documentation
  run: |
    npm run docs:generate
    pandoc README.md -o dist/documentation.pdf
```

### Artifact Naming Convention

```
<project>-<version>-<platform>-<arch>.<ext>

Examples:
myapp-v1.2.0-linux-amd64.tar.gz
myapp-v1.2.0-darwin-arm64.tar.gz
myapp-v1.2.0-windows-amd64.zip
myapp-v1.2.0-source.tar.gz
```

---

## Current Version Documentation

### VERSION File

Create a `VERSION` file in repository root:

```
1.2.0
```

**Auto-updated** by semantic-release:

```json
// .releaserc.json
{
  "plugins": [
    [
      "@semantic-release/exec",
      {
        "prepareCmd": "echo ${nextRelease.version} > VERSION"
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["VERSION", "CHANGELOG.md"]
      }
    ]
  ]
}
```

### Documentation Version Badge

Add to README.md:

```markdown
![Version](https://img.shields.io/github/v/release/org/repo)
![GitHub Release Date](https://img.shields.io/github/release-date/org/repo)
```

### Version API Endpoint

For applications, expose version via API:

```javascript
// /api/version
{
  "version": "1.2.0",
  "buildDate": "2025-11-25T10:30:00Z",
  "commit": "abc123f",
  "branch": "main"
}
```

### Documentation Website

**Current Version Page** at `/docs/current-version`:

```markdown
# Current Version: v1.2.0

**Release Date**: November 25, 2025

**Status**: Stable

## What's New

- User authentication with OAuth2
- Dashboard analytics
- Export functionality

## Installation

\`\`\`bash
npm install @org/package@1.2.0
\`\`\`

## Documentation

- [API Reference](../api/v1.2.0)
- [Migration Guide](../migration/v1-to-v1.2)
- [Changelog](../CHANGELOG.md)

## Support

- v1.2.x: Full support until 2026-11-25
- v1.1.x: Security fixes only until 2025-12-31
- v1.0.x: End of life

## Download

- [GitHub Release](https://github.com/org/repo/releases/tag/v1.2.0)
- [NPM Package](https://www.npmjs.com/package/@org/package/v/1.2.0)
```

---

## Stakeholder Communication

### Release Announcement Template

**For Internal Stakeholders**:

```markdown
Subject: [RELEASE] Project v1.2.0 Released

Team,

Version 1.2.0 of [Project Name] has been released to production.

**Key Changes:**

- New authentication system
- Performance improvements
- Bug fixes

**Impact:**

- Users will see OAuth2 login options
- API response times improved by 40%
- Previous login issues resolved

**Action Required:**

- Update documentation links
- Test integration points
- Monitor for issues

**Resources:**

- Release Notes: [link]
- Documentation: [link]
- Support: [link]

Questions? Reply to this email or check #engineering on Slack.

—Release Bot
```

**For External Users**:

```markdown
Subject: New Release: v1.2.0 with OAuth2 Authentication

Hello,

We're excited to announce version 1.2.0 of [Project Name]!

**What's New:**

- OAuth2 authentication (Google, GitHub)
- Enhanced dashboard with analytics
- Export data to PDF/CSV
- Performance improvements

**Upgrade Guide:**
[Link to upgrade instructions]

**Breaking Changes:**
API authentication now requires OAuth2 tokens. See our
migration guide: [link]

**Download:**

- GitHub: [link]
- NPM: npm install @org/package@1.2.0
- Docker: docker pull org/package:1.2.0

**Support:**

- Documentation: [link]
- Issues: [link]
- Discussions: [link]

Thank you for using [Project Name]!
```

### Automated Notifications

**GitHub Actions Workflow**:

```yaml
- name: Notify Slack
  if: success()
  uses: 8398a7/action-slack@v3
  with:
    status: custom
    custom_payload: |
      {
        text: " New release: ${{ steps.semantic.outputs.new_release_version }}",
        attachments: [{
          color: 'good',
          text: ${{ steps.semantic.outputs.new_release_notes }}
        }]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

- name: Create announcement issue
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: ' Release v${{ steps.semantic.outputs.new_release_version }}',
        body: ${{ steps.semantic.outputs.new_release_notes }},
        labels: ['release', 'announcement']
      })
```

---

## Release Checklist

### Pre-Release

- [ ] All features merged to develop
- [ ] All tests passing
- [ ] Security scans clean
- [ ] Documentation updated
- [ ] CHANGELOG reviewed
- [ ] Migration guides written (if breaking changes)
- [ ] Staging deployment successful
- [ ] QA sign-off obtained

### Release Process

- [ ] Create release branch from develop
- [ ] Run final tests
- [ ] Update version numbers
- [ ] Generate changelog
- [ ] Create PR to main
- [ ] Get approvals
- [ ] Merge to main
- [ ] Verify automatic release creation
- [ ] Verify artifacts uploaded
- [ ] Verify deployment to production

### Post-Release

- [ ] Verify production deployment
- [ ] Smoke tests in production
- [ ] Merge release branch back to develop
- [ ] Delete release branch
- [ ] Announce release to stakeholders
- [ ] Update documentation website
- [ ] Monitor for issues
- [ ] Create maintenance branch (if major version)
- [ ] Plan next release

---

## Rollback Procedures

### Quick Rollback

If release causes issues:

```bash
# 1. Revert to previous tag
git checkout v1.1.0  # Previous stable version

# 2. Create hotfix
git checkout -b production/hotfix/rollback-v1.2.0

# 3. Tag rollback
git tag -a v1.2.1 -m "Rollback: revert to v1.1.0 due to critical bug"

# 4. Deploy
git push origin production/hotfix/rollback-v1.2.0 --tags
```

### Partial Rollback

Revert specific features:

```bash
# 1. Identify problematic commits
git log v1.1.0..v1.2.0

# 2. Create hotfix branch
git checkout main
git checkout -b production/hotfix/revert-feature-x

# 3. Revert specific commits
git revert <commit-hash>

# 4. Test and release as patch
git commit -m "fix: revert feature X due to performance issues"
git push origin production/hotfix/revert-feature-x
# Follow normal release process for v1.2.1
```

---

## Related Documentation

- [VERSION_CONTROL_STANDARDS.md](../reference/VERSION_CONTROL_STANDARDS.md) -
  Version control
  standards
- [SEMANTIC_VERSIONING.md](../reference/SEMANTIC_VERSIONING.md) - Version
  numbering rules
- [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) - Branching strategies
- [CHANGELOG.md](../CHANGELOG.md) - Changelog format
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Git workflow details

---

**Last Updated**: 2025-11-25
