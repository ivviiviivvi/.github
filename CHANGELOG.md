# Changelog

All notable changes to the `.github` organization repository will be documented
in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Documentation INDEX.md for centralized navigation
- CHANGELOG.md for tracking changes
- CLEANUP_ROADMAP.md for systematic repository cleanup

### Changed

- Updated mdformat from 1.0.0 to 0.7.17 for gfm plugin compatibility
- Consolidated `.Jules/` and `.jules/` to lowercase `.jules/`
- Deprecated duplicate `docs/guides/WORKFLOW_OPTIMIZATION_ROADMAP.md`

### Fixed

- Pre-commit mdformat dependency conflict blocking normal commits
- GitHub Actions welcome workflow SHA reference (issue #217)
- YAML syntax errors in label-sync.yml, orchestrator.yml, stale.yml
- Python security issue: hardcoded /tmp path (Bandit B108)
- Python linting: E501 line length violations, F841 unused variables
- Type hints for mypy --strict compliance

### Removed

- `.Jules/` directory (consolidated to `.jules/`)
- Unused imports and variables from Python scripts

## [1.0.0] - 2026-01-13

### Added

- Successfully merged PRs #180-227
- 98 GitHub Actions workflows
- Multiple AI agent tracking systems (Jules, palette, sentinel, bolt,
  agentsphere)
- Comprehensive pre-commit hook configuration
- Security scanning with bandit and detect-secrets

### Changed

- Reorganized documentation structure
- Improved workflow organization

---

## Legend

- **Added** - New features or files
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features or files
- **Fixed** - Bug fixes
- **Security** - Security vulnerability fixes

---

**Note:** This changelog started on January 14, 2026, following the successful
merge of PRs #180-227. Previous changes are consolidated in the [1.0.0] entry.

For detailed commit history, see:
`git log --oneline --decorate --graph`
